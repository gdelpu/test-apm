# /sdlc-ba

Execute the **full BA pipeline** (Systems S0 through S3) without human gates.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project). Ask the user if not already clear.

## Steps

1. Read `.apm/workflows/sdlc-ba.yml` for the station sequence.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` for BA agent compositions.
3. Read `.apm/contexts/sdlc-system-context.md` for orchestration conventions.
4. For brownfield: start with S0 audit stations (ba-audit-existing, ba-audit-delta).
5. For greenfield: skip S0 and start from S1 scoping.
6. Execute remaining stations with `gate_mode: skip`:
   - S1: scoping (vision, glossary, actors, requirements).
   - S2: specification with fan-out for epics and features.
   - S3: per-feature functional design (stories, journeys, screens, tests, E2E plan).
   - Handle fan-in for project-level deliverables (business rules, E2E plan).
7. **Write every artifact as an actual file on disk** under `outputs/docs/1-prd/`. Do not merely display content in chat — use file-writing tools to create each file.
8. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-sdlc-ba-crm.md`) directly following the **exact Markdown table format** in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
9. At the end, suggest `/sdlc-coherence` for global consistency check.

If $ARGUMENTS contains "gated", use `gate_mode: pause` at each system boundary.
If $ARGUMENTS contains "skip-audit", start from S1 scoping (greenfield mode).

## Inputs

- Client input documents in `docs/0-inputs/ba/_source/`
- Existing system documents (brownfield) or project brief (greenfield)

## Outputs

- `outputs/docs/1-prd/` — all BA deliverables (vision, glossary, actors, requirements, domain model, epics, features, stories, journeys, test scenarios, E2E plan)
- `outputs/docs/1-prd/ba-validation-report.md` — final quality audit
