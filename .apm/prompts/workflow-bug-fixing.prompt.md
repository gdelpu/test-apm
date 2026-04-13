---
name: workflow-bug-fixing
mode: agent
description: 'Run structured bug diagnosis and resolution workflow (7 stations).'
---

# /workflow-bug-fixing

Run the Bug Fixing workflow.

1. Read `.apm/workflows/bug-fixing.yml` for the station sequence.
2. Execute each station: triage → reproduce → root cause → fix →
   regression testing → quality validation → summary.
3. Write all artifacts to `outputs/specs/features/<bug>/`.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-bug-fixing-null-pointer.md`) directly following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
