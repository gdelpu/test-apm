# /sdlc-tech

Execute the **full Tech pipeline** (Systems T0 through T3) without human gates.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project). Ask the user if not already clear.

## Steps

1. Read `.apm/workflows/sdlc-tech.yml` for the station sequence.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` for Tech agent compositions.
3. Read `.apm/contexts/sdlc-system-context.md` for orchestration conventions.
4. For brownfield: start with T0 audit stations (tech-audit, tech-gap).
5. For greenfield: skip T0 and start from T1 architecture.
6. Execute remaining stations with `gate_mode: skip`:
   - T1: System context (C4), ADRs, stack extraction, enabler index.
   - T2: Data model, API contracts, test strategy, implementation plan.
   - T3: Drift detection, E2E Playwright generation.
7. **Write every artifact as an actual file on disk** under `outputs/docs/2-tech/`. Do not merely display content in chat — use file-writing tools to create each file.
8. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-sdlc-tech-crm.md`) directly following the **exact Markdown table format** in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.

If $ARGUMENTS contains "gated", use `gate_mode: pause` at each system boundary.
If $ARGUMENTS contains "skip-audit", start from T1 architecture (greenfield mode).

Prerequisites: BA deliverables must exist with status `validated`.

## Inputs

- BA deliverables in `outputs/docs/1-prd/`
- Existing system technical documentation or codebase (brownfield)

## Outputs

- `outputs/docs/2-tech/` — all Tech deliverables (C4 context, ADRs, stack conventions, enablers, data model, API contracts, test strategy, implementation plan)
