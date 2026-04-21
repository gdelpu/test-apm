# /sdlc-ba

Execute the **full BA pipeline** (Systems S0 through S3) using pyramidal context isolation.

Each system is dispatched as a separate sub-command to keep context fresh. The workflow state file on disk bridges between phases.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project). Ask the user if not already clear.

## Execution sequence

Read `.apm/workflows/sdlc-ba.yml` for the authoritative station sequence.

### System S0: Brownfield Audit (brownfield only)
1. If brownfield: execute `/sdlc-ba-0-audit`.

### System S1: Scoping
2. Execute `/sdlc-ba-1-scoping` — vision, glossary, actors, requirements.

### System S2: Specification
3. Execute `/sdlc-ba-2-spec` — domain model, epics, features, business rules.

### System S3: Functional Design (per feature)
4. Execute `/sdlc-ba-3-design` — stories, journeys, screen specs, prototypes, batch specs, notifications, test scenarios, test data, E2E plan.

### Quality Gate
5. Execute `/sdlc-validate` on all deliverables.
6. At the end, suggest `/sdlc-coherence` for global consistency check.

## State tracking

Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-sdlc-ba-<project>.md` directly following the **exact Markdown table format** in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/`.

**After each system completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all systems.

## Context isolation

Each `/sdlc-ba-*` sub-command runs with its own context window (Level 2 worker). Only the workflow state file and produced artifacts on disk bridge between systems. This prevents context window saturation on large projects with many features.

If $ARGUMENTS contains "gated", use `gate_mode: pause` at each system boundary.
If $ARGUMENTS contains "skip-audit", start from S1 scoping (greenfield mode).
If $ARGUMENTS contains "inline", execute all systems in a single context (not recommended for large projects).

## Inputs

- Client input documents in `docs/0-inputs/ba/_source/`
- Existing system documents (brownfield) or project brief (greenfield)

## Outputs

- `outputs/docs/1-prd/` — all BA deliverables (vision, glossary, actors, requirements, domain model, epics, features, stories, journeys, screen specs, prototypes, test scenarios, test data, E2E plan)
- `outputs/docs/1-prd/ba-validation-report.md` — final quality audit
