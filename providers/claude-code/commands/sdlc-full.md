# /sdlc-full

Execute the **full SDLC pipeline** (BA + Tech + Test + Steer) using pyramidal context isolation.

Each phase is dispatched as a separate sub-command to keep context fresh and avoid window saturation. The workflow state file on disk (`outputs/workflow-state-sdlc-full-*.md`) serves as the inter-phase handoff.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project). Ask the user if not already clear. This affects:
- BA pipeline: brownfield runs S0 audit; greenfield skips to S1 scoping.
- Tech pipeline: brownfield runs T0 audit; greenfield skips to T1 architecture.

## Execution sequence

Read `.apm/workflows/sdlc-full.yml` for the authoritative station sequence.

### Phase 1: Project Initialization
1. Execute `/sdlc-steer-0-init` — scaffold + project sheet + KPI baselines.

### Phase 2: BA Specification (S0-S2)
2. If brownfield: execute `/sdlc-ba-0-audit`.
3. Execute `/sdlc-ba-1-scoping` — vision, glossary, actors, requirements.
4. Execute `/sdlc-ba-2-spec` — domain model, epics, features, business rules.

### Phase 3: Technical Architecture (T0-T1)
5. If brownfield: execute `/sdlc-tech-0-audit`.
6. Execute `/sdlc-tech-1-archi` — C4 context, ADRs, stack conventions, enablers.

### Phase 4: Sprint Planning (P1)
7. Execute `/sdlc-steer-1-planning` — sprint planning, roadmap, risk register.

### Phase 5: Sprint Loop
For each sprint defined in `plan-001-sprint-planning.md`:

8. Execute `/sdlc-ba-3-design --scope sprint-N` — functional design for sprint scope.
9. Execute `/sdlc-tech-2-design --scope sprint-N` — data model, APIs, test strategy, impl plan.
10. Execute `/sdlc-tech-3-impl --scope sprint-N` — wave-based implementation.
11. Execute `/sdlc-tech-4-quality --scope sprint-N` — drift detection + E2E script gen.
12. Execute `/sdlc-steer-2-sprint` — sprint tracking + risk assessment.

Repeat steps 8-12 for each sprint.

### Phase 6: Test Campaigns
13. Execute `/sdlc-test-1-campaign` — E2E/UAT campaign execution + report.
14. Execute `/sdlc-test-2-perf` — performance tests + report.

### Phase 7: Quality & Governance
15. Execute `/sdlc-steer-3-copil` — COPIL preparation + Go/No-Go decision.

## State tracking

Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-sdlc-full-<project>.md` directly following the **exact Markdown table format** in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/`.

**After each phase completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all phases.

## Context isolation

Each `/sdlc-*` sub-command runs with its own context window (Level 2 worker). Only the workflow state file and produced artifacts on disk bridge between phases. This ensures the context window never exceeds Level 0 (~150 lines) + 1 worker (~1000 lines).

If $ARGUMENTS contains "gated", pause at each phase boundary for human review.
If $ARGUMENTS contains "inline", execute all phases in a single context (not recommended for large projects).

## Inputs

- Project context or existing codebase (brownfield)
- Client input documents in `docs/0-inputs/`

## Outputs

- `outputs/docs/1-prd/` — BA deliverables (via nested `sdlc-ba`)
- `outputs/docs/2-tech/` — Tech deliverables (via nested `sdlc-tech`)
- `outputs/docs/3-steer/` — Steer deliverables (project sheet, KPIs, sprint plans, COPIL, Go/No-Go)
- `outputs/docs/4-test/` — Test results (campaign + performance reports)
- `gng-001-go-nogo.md` — final Go/No-Go decision
