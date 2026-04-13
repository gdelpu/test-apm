---
name: workflow-quality
mode: agent
description: 'Run code quality validation workflow (7 stations).'
---

# /workflow-quality

Run the Quality Validation workflow.

1. Read `.apm/workflows/quality-validation.yml` for the station sequence.
2. Execute each station: lint → static analysis → SAST → dependency audit →
   coverage check → DAST → quality report.
3. **Use `edit/editFiles` or `create_file` to write the final report as an actual file on disk** to `quality-report.md`. Do not merely display content in chat.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-quality-validation-login.md`) directly using `edit/editFiles` following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
