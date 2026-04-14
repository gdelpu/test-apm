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
3. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/specs/bugs/<bug>/`. Do not merely display content in chat.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-bug-fixing-null-pointer.md`) directly using `edit/editFiles` following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
5. **After each station completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all stations. Never leave the initial table stale.
