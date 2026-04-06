# Hook Schema

Defines the structure and execution model for lifecycle hooks in `.apm/hooks/`.

## Dual-Level Execution Model

Hooks operate at two complementary levels:

### 1. Agent-Level Hooks (Prompt Assembly)

Injected into the agent's system prompt by the coordinator at runtime. Defined in the agent registry (`sdlc-agent-registry.yaml`) under each agent's `hooks.pre` and `hooks.post` arrays.

- **Pre-hooks** are prepended to the assembled prompt before the skill instructions.
- **Post-hooks** are appended after the skill instructions.
- The agent sees one coherent prompt — it does not know which parts came from hooks vs. skills.
- Used for behavioral guards that must always be part of the agent's context (e.g., input validation rules, quality checklists).

### 2. Workflow-Level Station Hooks (Station Lifecycle)

Declared on individual stations in workflow YAML files via `pre_hooks` and `post_hooks` arrays. Fire as lightweight sub-stations before/after the main station execution.

- Each hook entry references a hook file and declares a severity level.
- Hooks have access to the station's input/output context.
- Hook returns: `GO` (proceed), `WARN` (log and proceed), `STOP` (halt).
- A `STOP` from a **pre-hook** → the station is skipped; downstream stations see it as `failed` or `skipped` depending on the hook severity.
- A `STOP` from a **post-hook** → the station's gate is marked as failed.
- Hooks fire **before** the station's `gate` evaluation. If a post-hook returns `STOP`, the gate is not reached.

```yaml
# Station-level hook syntax in workflow YAML
stations:
  - id: ba-vision
    name: Product Vision & Scope
    agent: sdlc-ba-analyst
    skills: [sdlc-ba-scoping]
    pre_hooks:
      - hook: pre/input-validation/ba     # Path relative to .apm/hooks/
        severity: blocker                  # blocker | warning
    post_hooks:
      - hook: post/quality-control
        severity: blocker
      - hook: post/confluence-push
        severity: warning                  # never_block hooks should use warning
    gate:
      criteria: [...]
      severity: blocker
```

## Hook File Structure

Each hook is a Markdown file with the following conventions:

```yaml
# Required sections:
# - Objective: what the hook does and when it fires
# - Decision: GO / WARN / STOP criteria
# - (Pre-hooks) Blocking report format: what to produce on STOP
# - (Post-hooks) Error handling: what to do on failure
```

## Hook Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | `pre` \| `post` | Yes | When the hook fires relative to station execution |
| `scope` | `agent` \| `station` | Yes | Whether injected into prompt (agent) or run as sub-station (station) |
| `domain` | `ba` \| `tech` \| `steer` \| `test` \| `universal` | Yes | Which agent domain this hook applies to. `universal` applies to all. |
| `severity` | `blocker` \| `warning` | Yes | Impact of a STOP/failure result |
| `never_block` | `boolean` | No | If `true`, hook failures are always downgraded to WARN. Used for best-effort integrations (e.g., Confluence push). Default: `false` |
| `config_refs` | `string[]` | No | Tool path variables this hook requires from `config/tool-paths.yml` |

## Directory Layout

```
.apm/hooks/
├── _schema.md                          # This file
├── config/
│   └── tool-paths.yml                  # Centralized tool path + env var config
├── pre/
│   └── input-validation/
│       ├── base.md                     # Shared validation protocol (all domains)
│       ├── ba.md                       # BA-specific extensions
│       ├── tech.md                     # Tech-specific extensions
│       ├── steer.md                    # Steer-specific extensions
│       └── test.md                     # Test-specific extensions (strict mode)
└── post/
    ├── quality-control.md              # Universal quality checklist
    └── confluence-push.md              # Best-effort Confluence publication
```

## Interaction with Gates

| Scenario | Result |
|----------|--------|
| Pre-hook returns GO | Station executes normally |
| Pre-hook returns WARN | Station executes; WARN logged in state file |
| Pre-hook returns STOP (severity: blocker) | Station skipped; workflow halted |
| Pre-hook returns STOP (severity: warning) | Station skipped; WARN logged; workflow continues |
| Post-hook returns GO | Gate evaluation proceeds |
| Post-hook returns WARN | Gate evaluation proceeds; WARN logged |
| Post-hook returns STOP (severity: blocker) | Gate marked as failed; workflow halted |
| Post-hook returns STOP (severity: warning) | Gate evaluation proceeds; WARN logged |
| Post-hook with `never_block: true` returns STOP | Always downgraded to WARN; gate evaluation proceeds |

## Conventions

- Hook files live under `.apm/hooks/pre/` or `.apm/hooks/post/`.
- Domain-specific hooks extend a `base.md` — read the base first, then the domain extension.
- Hook references in workflow YAML use paths relative to `.apm/hooks/` (e.g., `pre/input-validation/ba`).
- Hook references in the agent registry use the same relative paths.
- All external tool paths must come from `config/tool-paths.yml` — never hardcode paths.
- Post-hooks that integrate with external systems (Confluence, Jira, etc.) should set `never_block: true`.
