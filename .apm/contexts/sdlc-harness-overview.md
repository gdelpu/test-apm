# SDLC Agentic Harness

A portable, pyramidal agentic system that covers the full software development lifecycle — from business requirements to production Go/No-Go — through 4 specialized domains orchestrated by a single coordinator.

---

## How it works

### The pyramid: 3 levels for context control

An LLM has a limited context window. Loading 75 agents simultaneously would saturate it. The harness uses a **3-level pyramid** that loads only what's needed, when it's needed:

```
Level 0 — Apex (always loaded, ~150 lines)
  orchestration/system-prompt.md
  Knows EVERYTHING that exists. Contains NOTHING in detail.
  = project context + command registry + file conventions.

Level 1 — Coordinator (loaded on command invocation)
  orchestration/coordinator.md + pipelines.yaml + agents.yaml
  Knows WHICH agents to chain, in WHAT ORDER, with what PARALLELISM.
  Produces NOTHING — only orchestrates.

Level 2 — Worker (one agent at a time, ~1000 lines)
  Assembled dynamically: pre-hook + conventions + template + skill + post-hooks
  Sees ONLY its scope. Produces ONE deliverable, then returns control.
```

At any given moment, context contains: Level 0 (~150 lines) + one Level 2 worker (~1000 lines) = ~1150 lines. The other 74 agents are not loaded.

### Agent = Skill + Refs + Tools + Hooks

Each agent is decomposed into 4 portable components:

| Component | Role | Location |
|-----------|------|----------|
| **Skill** | Core production logic (what to produce, how to reason) | `{Domain}-Agents/skills/sk-*.md` |
| **Refs** | Conventions and templates the agent must follow | `{Domain}-Agents/refs/conventions/` + `refs/templates/` |
| **Tools** | External capabilities (Jira MCP, Pandoc, Xray API...) | Declared in `orchestration/agents.yaml` |
| **Hooks** | Systematic actions before/after production | `.apm/hooks/` |

The coordinator assembles these 4 components into a single prompt at runtime. The agent never knows it's decomposed — it receives a complete, coherent instruction set.

### Three reusable hooks

Extracted from the agents to avoid duplication (previously copy-pasted in every agent file):

| Hook | When | What it does |
|------|------|-------------|
| `pre-input-validation` | Before production | Checks all upstream deliverables exist, are validated, and meet sufficiency criteria. GO / WARN / STOP. |
| `post-quality-control` | After production | Runs quality checklist (form, content, template conformance, next-reader test). Adds Production Confidence section. |
| `post-confluence-push` | After production | Pushes the deliverable to Confluence (create or update page, Mermaid → PNG, status labels). |

### DAG-based orchestration with fan-out

Pipelines are defined as dependency graphs, not flat sequences. The coordinator resolves them into **waves** and maximizes parallelism:

```
/ba-2-spec pipeline:

  Wave 1: [2.1 Domain Model]
  Wave 2: [2.2 Epics]                         produces N epics
  Wave 3: [2.2b(ep-001) // 2.2b(ep-002) // ...] fan-out per epic, produces M features
  Wave 4: [2.3 Business Rules]                  fan-in (project scope)

/ba-3-design pipeline:

  Wave 1: [3.1(ft-001) // 3.1(ft-002) // ...]   fan-out per feature
  Wave 2: [3.2 // 3.3 // 3.3c // 3.4] x M       parallel design per feature
  Wave 3: [3.3b] x M                             depends on 3.3
  Wave 4: [3.5] x M                              convergence point
  Wave 5: [3.6 // 3.6b]                          per-feature + project E2E plan
```

---

## The 4 domains

### BA — Business Analyst

Transforms raw business needs into a complete, structured functional specification.

| System | Command | Agents | Deliverables |
|--------|---------|--------|-------------|
| S0 Brownfield Audit | `/ba-0-audit` | 0.1, 0.2 | `[ASIS-001]`, `[DELTA-001]` |
| S1 Scoping | `/ba-1-scoping` | 1.1 to 1.4 | Vision, Glossary, Actors, Requirements |
| S2 Specification | `/ba-2-spec` | 2.1 to 2.3 | Domain Model, Epics/Features (fan-out), Business Rules |
| S3 Functional Design | `/ba-3-design` | 3.1 to 3.6b | User Stories, Journeys, Screens, Tests, Seeds (per-feature fan-out) |

**Full pipeline:** `/ba` (skip gates) or `/ba gated` (pause at each system boundary)

### Tech — Technical Architecture & Design

Transforms validated BA deliverables into a technical dossier + implementation plan for Claude Code.

| System | Command | Agents | Deliverables |
|--------|---------|--------|-------------|
| T0 Brownfield Audit | `/tech-0-audit` | t0.1, t0.2 | `[TECH-ASIS-001]`, `[GAP-001]` |
| T1 Architecture | `/tech-1-archi` | t1.1 to t1.4 | System Context, ADRs, Stack, Security |
| T2 Technical Design | `/tech-2-design` | t2.1 to t2.6 | Data Model, API, Enablers, Tests, Observability, Implementation Plan |
| T3 Implementation | `/tech-3-impl` | t3.1 to t3.5 | Task Resolution, Code, Tests, Validation, Wave Gate |
| T4 Continuous Quality | `/tech-4-quality` | t4.1, t4.2 | Drift Detection, Code Review (per PR) |

**Full pipeline:** `/tech` or `/tech gated`

### Test — Qualification Campaigns

Executes (does not design) system tests once the application is assembled. Consumes plans from BA and scripts from Tech.

| System | Command | Agents | Deliverables |
|--------|---------|--------|-------------|
| E1 Campaign | `/test-1-campaign` | camp.1, camp.2 | `[CAMP-RPT-NNN]`, `[QUAL-GNG-001]` |
| E2 Performance | `/test-2-perf` | perf.1, perf.2 | `[PERF-RPT-NNN]` |
| DAST (on-demand) | `/dast` | agent-dast | `[DAST-RPT-NNN]` |

**Full pipeline:** `/test`

### Steer — Project Steering

Reads and aggregates deliverables from all other domains. Never modifies them.

| System | Command | Agents | Deliverables |
|--------|---------|--------|-------------|
| P0 Initialization | `/steer-0-init` | p0.1, p0.2 | Project Sheet, KPI Baseline |
| P1 Planning | `/steer-1-planning` | p1.1, p1.2 | Roadmap, Risk Register |
| P2 Sprint Tracking | `/steer-2-sprint` | p2.1 to p2.3 | Sprint Report, System Health, Risks (recurring) |
| P3 Steering Committee | `/steer-3-copil` | p3.1, p3.2 | COPIL Deck, Release Go/No-Go |

---

## Cross-domain execution

| Command | What it chains |
|---------|---------------|
| `/sdlc` | BA (S0-S3) then Tech (T0-T4) — no gates |
| `/sdlc gated` | Same, with human gates between systems |

Full value chain:
```
Raw need --> [BA] --> [Tech] --> [Claude Code] --> [Test] --> [Steer Go/No-Go]
```

---

## Utility tools

| Command | Description |
|---------|-------------|
| `/validate <file>` | Quality audit of a deliverable: PASS / WARN / BLOCK |
| `/coherence` | Cross-deliverable consistency: references, orphans, coverage |
| `/impact <change>` | Change impact analysis with re-execution sequence |
| `/to-word <file>` | Markdown to Word conversion (Pandoc) |

See [.claude/commands/README.md](.claude/commands/README.md) for the full command reference with examples.

---

## Repository structure

```
orchestration/                         Portable orchestration layer (Level 0 + 1)
  system-prompt.md                     Level 0 — project context + command registry
  coordinator.md                       Level 1 — DAG resolution + fan-out logic
  pipelines.yaml                       Pipeline definitions (dependencies, parallelism)
  agents.yaml                          Agent registry (skill + refs + tools + hooks)

BA-Agents/                             Business Analyst domain
  skills/          21 pipeline + 13 tools
  refs/            conventions/ + templates/
  hooks/           pre-input-validation + post-quality-control + post-confluence-push
  README.md

Tech-Agents/                           Technical Architecture domain
  skills/          15 pipeline + 7 tools
  refs/            conventions/ + templates/ + skill-registry/
  hooks/           (same 3 hooks)
  README.md

Test-Agents/                           Qualification Campaigns domain
  skills/          4 pipeline + 1 tool
  refs/            conventions/
  hooks/           (same 3 hooks)
  README.md

Steer-Agents/                          Project Steering domain
  skills/          12 pipeline + 7 tools
  refs/            conventions/ + templates/
  hooks/           (same 3 hooks)
  README.md

.claude/                               Claude Code adapter (thin, tool-specific)
  commands/        26 slash commands (see commands/README.md)

docs/                                  Produced deliverables (output)
  prd/             BA deliverables
  tech/            Tech deliverables
  steer/           Steering deliverables

zz-old-agents-french/                  Archive: original French agent definitions
```

---

## Portability

The harness is designed for tool migration. **95% of the system is portable:**

| Layer | Files | Portable? |
|-------|-------|-----------|
| `orchestration/` | 4 | 100% — consumed by any adapter |
| `{Domain}-Agents/` | ~130 | 100% — pure Markdown, no tool dependency |
| `.claude/` + `CLAUDE.md` | 27 | 0% — Claude Code specific, rewrite in ~2-3h |

To migrate to another tool (Cursor, Aider, Agent SDK...):
1. Copy everything except `.claude/` and `CLAUDE.md`
2. Write equivalent thin wrappers for the new tool
3. Done

---

## Design principles

| Principle | Implementation |
|-----------|---------------|
| **Markdown = single source of truth** | All deliverables in structured MD with YAML front matter, stored in Git |
| **Human gates between systems** | Each pipeline can stop for validation (`gate_after: true`) |
| **Embedded quality** | 3 hooks (input validation, quality control, Jira review) on every agent |
| **Traceability** | Full chain: `EXF -> EP -> FT -> US -> BR -> SCE` |
| **Context isolation** | Each worker sees only its scope (one feature, one epic, one project-level task) |
| **Fan-out / fan-in** | 1 epic produces N features, each with its own design sub-pipeline |
| **Composable conventions** | Tech skill-registry allows stack-specific rules (React, PostgreSQL, AWS...) |
| **Dual register (Steer)** | Every steering deliverable has a technical section + a sponsor section |
| **Read-only cross-domain** | Steer never modifies BA/Tech; Test never modifies BA/Tech |

---

## SDLC coverage

| # | Phase | Agent(s) |
|---|-------|----------|
| 1 | Opportunity & Business Case | Out of scope |
| 2-6 | Requirements Discovery to Functional Requirements | BA 1.0 to 1.4 |
| 7-9 | Business Rules, Domain Model, Epics & Features | BA 2.1 to 2.3 |
| 10-13 | User Stories, Journeys, UI/UX, Test Scenarios | BA 3.1 to 3.6b |
| 14-17 | System Architecture, ADRs, Security, Stack | Tech T1.1 to T1.4 |
| 18-22 | Data Model, API, Enablers, Test Strategy, Impl Plan | Tech T2.1 to T2.6 |
| 23 | Implementation | Tech T3.1 to T3.5 (implementer agent) |
| 24 | Continuous Quality | Tech T4.1 + T4.2 |
| 25-26 | System E2E + Performance Tests | Test camp.1/2 + perf.1/2 |
| 27 | DAST Security | Test agent-dast (on-demand) |
| 28 | Release Management | Tech agent-release-manager (on-demand) |

---

## Getting started

```bash
# 1. Run the BA scoping pipeline on your source documents
/ba-1-scoping path/to/cahier-des-charges.md

# 2. Validate the scoping deliverables
/validate outputs/docs/1-prd/1-scoping/vis-001-product-vision.md
/validate outputs/docs/1-prd/1-scoping/glo-001-glossary.md

# 3. Continue with specification (fan-out: epics then features)
/ba-2-spec

# 4. Run the full design pipeline (per-feature fan-out)
/ba-3-design

# 5. Check global consistency
/coherence

# Or run everything at once
/ba skip-audit
```
