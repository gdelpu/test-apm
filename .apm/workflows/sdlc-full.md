# Workflow: SDLC Full

Composite SDLC pipeline orchestrating all four domains — BA specification, Tech architecture, Test campaigns, and Steer governance — with inter-domain quality gates.

## When to use

- Running the complete SDLC lifecycle for a project from initialization to Go/No-Go
- Orchestrating BA, Tech, Test, and Steer domains in sequence with inter-domain gates
- When a single entry point is needed to drive the full pipeline across all domains
- Large projects requiring formal governance, traceability, and quality validation at every phase

## Stations

| # | Phase | Station | Agent | Skills | Gate | Severity |
|---|-------|---------|-------|--------|------|----------|
| 1 | Init | Directory Scaffold | sdlc-coordinator | sdlc-scaffold | Directory structure created | blocker |
| 2 | Init | Project Initialization (P0) | sdlc-steer-manager | sdlc-steer-init | Project sheet and KPI baselines established | blocker |
| 3 | BA | BA Pipeline (S0-S3) | sdlc-coordinator | sdlc-ba-audit, sdlc-ba-scoping, sdlc-ba-specification, sdlc-ba-functional-design | All BA systems complete; traceability chain verified | blocker |
| 4 | Planning | Sprint Planning (P1) | sdlc-steer-manager | sdlc-steer-planning | Features batched into sprints; roadmap and risk register complete | blocker |
| 5 | Tech | Tech Pipeline (T0-T4) | sdlc-coordinator | sdlc-tech-audit, sdlc-tech-architecture, sdlc-tech-design, sdlc-tech-implementation, sdlc-tech-quality | All Tech systems complete; BA-Tech traceability; implementation plan compiled and executed | blocker |
| 6 | Impl | Code Implementation | implementer | code-implementation | Code compiles; all tests pass | blocker |
| 7 | Test | E2E/UAT Campaign | sdlc-test-executor | sdlc-test-campaign | Campaign pass rate above threshold; critical anomalies resolved | blocker |
| 8 | Test | Performance Campaign | sdlc-test-executor | sdlc-test-performance | Performance within defined thresholds (parallel with station 7) | blocker |
| 9 | Track | Sprint Tracking (P2) | sdlc-steer-manager | sdlc-steer-sprint | Sprint progress documented; risks assessed | warning |
| 10 | Quality | Quality Validation | workflow-orchestrator | workflow-engine | Nested quality-validation passes all gates | blocker |
| 11 | Gov | COPIL & Go/No-Go (P3) | sdlc-steer-manager | sdlc-steer-governance | All domain data aggregated; Go/No-Go decision documented | blocker |

## Phase flow

```
┌─────────┐   ┌──────┐   ┌──────────┐   ┌──────┐   ┌──────────┐
│  Init   │──▶│  BA  │──▶│ Planning │──▶│ Tech │──▶│   Impl   │
│ (1-2)   │   │ (3)  │   │   (4)    │   │ (5)  │   │   (6)    │
└─────────┘   └──────┘   └──────────┘   └──────┘   └──────────┘
                                                         │
    ┌──────────┐   ┌─────────┐   ┌─────────┐   ┌───────▼───────┐
    │   Gov    │◀──│ Quality │◀──│  Track  │◀──│     Test      │
    │  (11)    │   │  (10)   │   │   (9)   │   │  (7∥8)        │
    └──────────┘   └─────────┘   └─────────┘   └───────────────┘
```

## Nested workflows

- **Station 3** (BA Pipeline) invokes the `sdlc-ba` workflow as a nested sub-workflow, running all 16 BA stations.
- **Station 5** (Tech Pipeline) invokes the `sdlc-tech` workflow as a nested sub-workflow, running all 17 Tech stations.
- **Station 10** (Quality Validation) invokes the `quality-validation` workflow for comprehensive code quality checks (lint, static analysis, SAST, dependency audit, coverage, DAST, report).

## Parallel stations

Station 7 (E2E/UAT Campaign) and Station 8 (Performance Campaign) can run in parallel. Both consume the implementation log and produce independent reports that feed into sprint tracking and governance.

## Inter-domain traceability

The full workflow maintains traceability across domains:

- **BA → Tech**: Domain model → data model, user stories → API contracts, test scenarios → test strategy
- **Tech → Impl**: Implementation plan → code changes
- **BA → Test**: Gherkin scenarios → E2E campaigns, acceptance criteria → UAT
- **All → Steer**: Sprint metrics, quality reports, test results → COPIL preparation → Go/No-Go

## Outputs

Artifacts are distributed across domain output directories:
- `docs/` — directory scaffold (root)
- `outputs/docs/3-steer/` — project sheet, KPIs, sprint plans, roadmap, risks, COPIL, Go/No-Go
- `outputs/docs/1-prd/` — all BA deliverables (via nested `sdlc-ba`)
- `outputs/docs/2-tech/` — all Tech deliverables (via nested `sdlc-tech`)
- `implementation-log.md` — code implementation record
- `campaign-report.md` — E2E/UAT campaign results
- `performance-report.md` — performance test results
- `sprint-progress.md`, `sprint-risks.md` — sprint tracking
- `quality-report.md` — from nested quality-validation
- `gng-001-go-nogo.md` — final Go/No-Go decision

## Key differences from feature-implementation

- Orchestrates 4 domains (BA, Tech, Test, Steer) — not a single feature lifecycle
- Includes formal project governance with COPIL and Go/No-Go decisions
- Uses nested workflows for BA, Tech, and Quality phases
- 11 top-level stations (with 40+ effective stations via nesting)
- Sprint tracking with recurring cadence and warning-level gates
- Not nestable itself — this is the top-level composite pipeline
