---
name: workflow-compliance-check
mode: agent
description: 'Run compliance, privacy, and AI governance validation workflow (6 stations).'
---

# /workflow-compliance-check

Run the Compliance Check workflow.

1. Read `.apm/workflows/compliance-check.yml` for the station sequence.
2. Execute each station: PII scan → prompt injection detection → policy validation →
   risk scoring → human approval → compliance report.
3. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/specs/features/<feature>/`. Do not merely display content in chat.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-compliance-check-login.md`) directly using `edit/editFiles` following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
5. Report overall compliance status (pass / conditional / fail) with gate results.
