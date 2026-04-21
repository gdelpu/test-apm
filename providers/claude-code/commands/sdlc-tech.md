# /sdlc-tech

Execute the **full Tech pipeline** (Systems T0 through T4) using pyramidal context isolation.

Each system is dispatched as a separate sub-command to keep context fresh. The workflow state file on disk bridges between phases.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project). Ask the user if not already clear.

## Execution sequence

Read `.apm/workflows/sdlc-tech.yml` for the authoritative station sequence.

### System T0: Brownfield Audit (brownfield only)
1. If brownfield: execute `/sdlc-tech-0-audit`.

### System T1: Architecture
2. Execute `/sdlc-tech-1-archi` — C4 system context, ADRs, stack conventions, enablers.

### System T2: Technical Design (per sprint scope)
3. Execute `/sdlc-tech-2-design` — data model, API contracts, test strategy, implementation plan.

### System T3: Implementation (iterative per sprint, per wave)
4. Execute `/sdlc-tech-3-impl` — wave-based task resolution, code gen, test impl, validation, wave gate, push/CI, MR.

### System T4: Continuous Quality
5. Execute `/sdlc-tech-4-quality` — drift detection (per wave), code review (per wave), E2E Playwright generation (per sprint).

Note: T3 and T4 interleave during execution — T4.1 runs after each wave gate, T4.3 runs after the last wave of each sprint. See `/sdlc-tech-3-impl` for the detailed loop.

## State tracking

Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-sdlc-tech-<project>.md` directly following the **exact Markdown table format** in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/`.

**After each system completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all systems.

## Context isolation

Each `/sdlc-tech-*` sub-command runs with its own context window (Level 2 worker). Only the workflow state file and produced artifacts on disk bridge between systems. T3 implementation is the most context-intensive phase — each wave runs in its own context via `/sdlc-tech-3-impl`.

If $ARGUMENTS contains "gated", use `gate_mode: pause` at each system boundary.
If $ARGUMENTS contains "skip-audit", start from T1 architecture (greenfield mode).
If $ARGUMENTS contains "inline", execute all systems in a single context (not recommended for large projects).

Prerequisites: BA deliverables must exist with status `validated`.

## Inputs

- BA deliverables in `outputs/docs/1-prd/`
- Existing system technical documentation or codebase (brownfield)

## Outputs

- `outputs/docs/2-tech/` — all Tech deliverables (C4 context, ADRs, stack conventions, enablers, data model, API contracts, test strategy, implementation plan, wave reports, E2E scripts)
