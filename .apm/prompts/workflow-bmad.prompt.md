---
name: workflow-bmad
mode: agent
description: 'Run Build → Measure → Analyze → Decide feedback loop (4 stations).'
---

# /workflow-bmad

Run the BMAD workflow.

1. Read `.apm/workflows/bmad.yml` for the station sequence.
2. Execute each station: build → measure → analyze → decide.
3. If the decision is "retry", loop back to the build station.
4. Write all artifacts to `outputs/specs/features/<feature>/`.
5. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-bmad-login.md`) directly following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
