---
name: workflow-sdlc-steer
mode: agent
description: 'Run full Steer pipeline — project init through Go/No-Go (10 stations).'
---

# /workflow-sdlc-steer

Run the Steer pipeline (Systems P0 through P3).

1. Read `.apm/workflows/sdlc-steer.yml` for the station sequence.
2. Execute all 10 stations: init (project sheet, KPIs) → planning (sprints, roadmap, risks) → tracking (progress, health, risks) → governance (COPIL, Go/No-Go).
3. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/docs/3-steer/`. Do not merely display content in chat.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-sdlc-steer-crm.md`) directly using `edit/editFiles` following the **exact Markdown table format** defined in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder. Do **not** invent alternative formats (e.g. YAML frontmatter with `stations_completed`/`stations_remaining`).
5. After each station, verify that declared output files exist on disk before proceeding.
6. **After each station completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all stations. Never leave the initial table stale.
