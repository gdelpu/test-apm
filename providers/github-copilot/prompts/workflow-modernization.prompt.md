---
name: workflow-modernization
mode: agent
description: 'Run guided modernization workflow (10 stations).'
---

# /workflow-modernization

Run the Modernization workflow.

1. Read `.apm/workflows/modernization.yml` for the station sequence.
2. Execute each station: baseline → decisions → target state → architecture review →
   migration plan → risk clarification → task breakdown → implementation → quality validation → PR validation.
3. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/specs/features/<feature>/`. Do not merely display content in chat.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-modernization-payments.md`) directly using `edit/editFiles` following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
5. After each station, verify that declared output files exist on disk before proceeding.
