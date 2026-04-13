---
name: workflow-sdlc-test
mode: agent
description: 'Run full Test pipeline — E2E/UAT campaign + performance.'
---

# /workflow-sdlc-test

Run the Test pipeline (campaign + performance).

1. Read `.apm/contexts/sdlc-agent-registry.yaml` for Test agent compositions.
2. Execute campaign system (launch + report) then performance system (execution + report).
3. **Use `edit/editFiles` or `create_file` to write all test reports as actual files on disk.** Do not merely display content in chat.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-sdlc-test-login.md`) directly using `edit/editFiles` following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
5. **After each station completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all stations. Never leave the initial table stale.
6. Display cumulative Go/No-Go recommendation.
