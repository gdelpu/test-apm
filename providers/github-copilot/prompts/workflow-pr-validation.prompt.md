---
name: workflow-pr-validation
mode: agent
description: 'Run PR validation pipeline — A0-A7 stations (11 stations).'
---

# /workflow-pr-validation

Run the PR Validation workflow.

1. Read `.apm/workflows/pr-validation.yml` for the station sequence.
2. Phase 1 (parallel): PR auto-validator → YAML workflow linter → test gap detector.
3. Phase 2 (sequential): A0 intake → A1 policy → A2 security → A3 prompt injection →
   A4 red team → A5 sandbox → A6 policy gate → A7 platform update.
4. **Use `edit/editFiles` or `create_file` to write reports as actual files on disk** to `outputs/station_out/`. Do not merely display content in chat.
5. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-pr-validation-mr-42.md`) directly using `edit/editFiles` following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
6. **After each station completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all stations. Never leave the initial table stale.
