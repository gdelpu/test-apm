# Orchestration Layer

This directory contains the portable orchestration logic of the SDLC agentic harness. These 4 files are tool-agnostic — they are consumed by the Claude Code adapter (`.claude/`) today, and can be consumed by any other adapter tomorrow.

---

## Files

| File | Role | Read by |
|------|------|---------|
| `system-prompt.md` | **Level 0 — Apex.** Project context, conventions, command registry. Always in LLM context. | Claude Code (via CLAUDE.md) |
| `coordinator.md` | **Level 1 — Coordinator skill.** DAG resolution, fan-out/fan-in, scope filtering, gate management. | Slash commands |
| `pipelines.yaml` | Pipeline definitions: agent sequences, dependencies, parallelism, composites. | Coordinator |
| `agents.yaml` | Agent registry: each agent's skill + refs + tools + hooks. | Coordinator |

---

## How the coordinator works

### 1. Receive a command

The user types a slash command (e.g., `/ba-3-design --scope sprint-1`). The adapter reads `coordinator.md` and passes it the pipeline name + arguments.

### 2. Resolve the pipeline

```
pipelines.yaml
  ba-3-design:
    agents:
      "3.1": { foreach: features, scope: feature }
      "3.2": { depends_on: ["3.1"], foreach: features }
      ...
```

If the command is a **composite** (e.g., `/ba`), the coordinator merges all sub-pipelines into a single DAG.

### 3. Resolve the static DAG into waves

```
Dependencies:         Resolved waves:

3.1 (no deps)         Wave 1: [3.1]
3.2 -> 3.1            Wave 2: [3.2, 3.3, 3.3c, 3.4]   (parallel)
3.3 -> 3.1            Wave 3: [3.3b]
3.3b -> 3.3           Wave 4: [3.5]
3.3c -> 3.1           Wave 5: [3.6 // 3.6b]            (parallel)
3.4 -> 3.1
3.5 -> 3.2,3.3,...
3.6 -> 3.5
3.6b -> 3.5
```

### 4. Discover items (dynamic fan-out)

When an agent with `produces: <collection>` completes, the coordinator scans the filesystem:

```
Agent 2.2 completes
  --> produces: epics
  --> output_pattern: "outputs/docs/1-prd/3-epics/ep-{id}-{slug}/"
  --> SCAN: ls outputs/docs/1-prd/3-epics/ep-*/
  --> DISCOVERS: ep-001, ep-002, ..., ep-008
  --> REGISTERS: epics = [ep-001, ..., ep-008]

Agent 2.2b(ep-001) completes
  --> produces: features
  --> output_pattern: "outputs/docs/1-prd/3-epics/{epic}/ft-{id}-{slug}/"
  --> SCAN: ls outputs/docs/1-prd/3-epics/ep-001-*/ft-*/
  --> DISCOVERS: ft-001, ft-002, ..., ft-006
  --> REGISTERS: features += [ft-001, ..., ft-006]

After all 2.2b instances complete:
  --> features = [ft-001, ft-002, ..., ft-039]
```

For `foreach: <collection>` agents, the coordinator creates **one instance per item**:
- Agent 3.1 with 39 features = 39 instances
- Each instance sees only its own feature path

### 5. Apply scope filter (optional)

When `--scope sprint-1` is provided, the coordinator reads the sprint plan:

```
outputs/docs/3-steer/plan-001-sprint-planning.md   (BA Sprint 1)
  scope_items:
    features:
      - .../ft-001-create-modify-bookings
      - .../ft-011-room-catalogue
      - .../ft-018-process-standard-checkin
```

Instead of 81 instances, only **3 instances** are created. The rest are skipped.

```
Without --scope:     81 features --> 81 x (3.1 + 3.2 + 3.3 + ...) = ~500 agent runs
With --scope sprint-1: 3 features -->  3 x (3.1 + 3.2 + 3.3 + ...) = ~20 agent runs
```

This is how Steer agent `p1.3` (Sprint Planning) integrates with the orchestrator: it produces a unified BA+Tech sprint plan that the orchestrator consumes as a scope filter. BA sprints feed `--scope` for `/ba-3-design`, Tech sprints feed `--scope` for `/tech-2-design`.

### 6. Handle fan-in

When a `scope: project` agent depends on a `foreach` agent, it waits for ALL instances:

```
3.5(ft-001) ---+
3.5(ft-002)    +--> 3.6b E2E Plan (waits for ALL, runs ONCE)
...            |
3.5(ft-039) --+
```

With `--scope sprint-1`, fan-in waits only for the scoped instances (3 instead of 39).

### 7. Manage concurrency

`max_concurrency: 5` (from `pipelines.yaml` defaults) limits parallel agents:

```
Wave 1 with 39 features and max_concurrency=5:

  Batch 1: [3.1(ft-001), 3.1(ft-002), 3.1(ft-003), 3.1(ft-004), 3.1(ft-005)]
  Batch 2: [3.1(ft-006), 3.1(ft-007), 3.1(ft-008), 3.1(ft-009), 3.1(ft-010)]
  ...
  Batch 8: [3.1(ft-036), 3.1(ft-037), 3.1(ft-038), 3.1(ft-039)]
```

### 8. Assemble agent prompts

For each agent instance, the coordinator reads `agents.yaml` and builds the prompt:

```
agents.yaml:
  ba-3.1:
    skill: BA-Agents/skills/sk-3.1-user-stories.md
    refs:
      conventions: [cv-markdown, cv-domain-language, cv-output-language]
      template: tpl-user-story.md
      upstream_scope: ["{feature_path}/ft-*.md", "brl-*-business-rules.md", ...]
    hooks:
      pre: [pre-input-validation.md]
      post: [post-quality-control.md, post-confluence-push.md]
    model: opus

Assembled prompt for 3.1(ft-005):
  [1] pre-input-validation.md        (hook)
  [2] cv-markdown.md                 (convention)
  [3] cv-domain-language.md          (convention)
  [4] cv-output-language.md          (convention)
  [5] tpl-user-story.md             (template)
  [6] sk-3.1-user-stories.md        (skill — the core logic)
  [7] post-quality-control.md        (hook)
  [8] post-confluence-push.md       (hook)
  [9] Scope context:
      feature_path = outputs/docs/1-prd/3-epics/ep-001-.../ft-005-packages-tarifaires
      upstream files resolved for this feature
```

The assembled prompt is launched via the **Agent tool** with `model: opus`. The worker sees a coherent, complete instruction set — it doesn't know it was assembled from 4 components.

### 9. Manage gates

If `gate_after: true` and `gate_mode: pause`:
- Coordinator stops execution
- Displays: "Human gate required. N deliverables produced. Run `/validate` before proceeding."
- Does NOT chain the next pipeline

If `gate_mode: skip` (composites like `/ba`): gates are ignored, execution continues.

---

## Pipeline definition format

```yaml
# pipelines.yaml

pipelines:
  ba-3-design:
    domain: BA
    system: S3
    gate_after: true                    # human gate at the end
    agents:
      "3.1":
        foreach: features              # run once per feature
        scope: feature                 # scoped to one feature
      "3.2":
        depends_on: ["3.1"]            # depends on 3.1 of SAME feature
        foreach: features
        scope: feature
      "3.5":
        depends_on: ["3.2", "3.3", "3.3b", "3.3c", "3.4"]
        foreach: features
        scope: feature
      "3.6b":
        depends_on: ["3.5"]
        scope: project                  # fan-in: waits for ALL features

composites:
  ba:
    compose: [ba-0-audit, ba-1-scoping, ba-2-spec, ba-3-design]
    gate_mode: skip                     # no gates between sub-pipelines
```

**Key fields:**

| Field | Description |
|-------|-------------|
| `depends_on` | List of agents that must complete before this one starts |
| `produces` | Declares that this agent creates a collection of items (triggers discovery) |
| `foreach` | Run one instance per item in the named collection |
| `scope` | `feature` (per-item) or `project` (waits for all, runs once) |
| `output_pattern` | Filesystem pattern for discovering produced items |
| `condition` | Optional condition (e.g., `has_screens`) — ask user if unclear |
| `gate_after` | Stop for human validation after this pipeline |
| `recurring` | Pipeline can be invoked multiple times (e.g., sprint tracking) |

---

## Agent registry format

```yaml
# agents.yaml

agents:
  ba-3.1:
    name: User Stories
    domain: BA
    system: S3
    skill: BA-Agents/skills/sk-3.1-user-stories.md          # SKILL
    refs:                                                      # REFS
      conventions: [cv-markdown, cv-domain-language, ...]
      template: BA-Agents/refs/templates/tpl-user-story.md
      upstream_scope: ["{feature_path}/ft-*.md", ...]
    tools:                                                     # TOOLS
      required: [file-read, file-write]
      optional: [jira-mcp, r4j-api]
    hooks:                                                     # HOOKS
      pre: [.apm/hooks/pre/input-validation/base.md,
            .apm/hooks/pre/input-validation/ba.md]
      post: [.apm/hooks/post/quality-control.md,
             .apm/hooks/post/confluence-push.md]
    model: opus
    output_pattern: "{feature_path}/user-stories/"
```

Each agent = **skill + refs + tools + hooks**, assembled at runtime by the coordinator.

**New fields (doc_depth):**
- `min_depth` — minimum `doc_depth` required for this agent to run (`essential`, `standard`, or `full`; default `full`)
- `template_variants` — map of `{depth: template_path}` overrides for the default template

---

## Doc depth filtering

The coordinator applies `doc_depth` filtering before resolving the DAG into waves.

1. Read `doc_depth` from `outputs/docs/project.yml` (default: `full`).
2. Define the depth hierarchy: `essential` < `standard` < `full`.
3. For each agent, read `min_depth` from the registry (default: `full`). If the agent's `min_depth` exceeds the current `doc_depth`, remove it from the DAG.
4. For remaining agents with `template_variants.{depth}`, resolve the variant template instead of the default.
5. Re-wire the DAG: remove references to filtered-out agents from `depends_on` lists. Orphaned agents become root nodes.
6. Pass `doc_depth` as scope context to all agents.

Example at `essential` depth: only ~12 agents run (vision, epics, features, system context, ADRs, sprint planning) out of ~40 total.

---

## Hook execution model

Hooks operate at two levels:

### Agent-level (prompt assembly)

During prompt assembly (section 8), the coordinator injects hook content into the agent's prompt. The pre-hooks appear before the skill and the post-hooks appear after. The agent sees a single coherent instruction set.

Hook files are resolved from `.apm/hooks/`:
- **Pre:** `.apm/hooks/pre/input-validation/base.md` + domain-specific extension (e.g., `ba.md`)
- **Post:** `.apm/hooks/post/quality-control.md` + `.apm/hooks/post/confluence-push.md`

### Station-level (workflow YAML)

Workflow stations can declare `pre_hooks` and `post_hooks` arrays. These fire as sub-stations in the workflow lifecycle — before/after the station's main action. See `.apm/workflows/_schema.md` for the station hook contract.

Hook results use the GO/WARN/STOP protocol:
- **GO**: proceed without modification
- **WARN**: proceed, but log the warning in the station report
- **STOP**: halt the station and escalate to the coordinator

For the full hook contract, see `.apm/hooks/_schema.md`.

---

## Typical execution flow

```
User types: /ba-3-design --scope sprint-1

Coordinator:
  1. Read pipelines.yaml --> ba-3-design, 10 agent definitions
  2. Read scope plan --> sprint-1 = [ft-001, ft-002, ft-007]
  3. Resolve DAG --> 6 waves
  4. Display execution plan:
     "Execution plan for ba-3-design (scope: sprint-1, 3 features):
       Wave 1: 3.1 x3
       Wave 2: 3.2 x3 // 3.3 x3 // 3.4 x2 (parallel)
       Wave 3: 3.3b x3
       Wave 4: 3.5 x3
       Wave 5: 3.6 x3 // 3.6b x1
       Wave 5: 3.6 x3 // 3.6b x1"
  5. Execute wave by wave, max_concurrency=5
  6. Final report: 3 features completed, 0 failed
  7. "Human gate required. Run /validate on deliverables."
```

---

## Portability

These 4 files contain zero tool-specific logic. To use them with a different tool:

1. `system-prompt.md` becomes the tool's system prompt (e.g., `.cursorrules`)
2. `coordinator.md` is loaded by the tool's command mechanism
3. `pipelines.yaml` and `agents.yaml` are read as data — any YAML parser works

The tool adapter only needs to implement:
- A way to trigger the coordinator with a pipeline name
- A way to launch sub-agents (the equivalent of Claude Code's Agent tool)
- A way to read files and scan directories
