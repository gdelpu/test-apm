---
name: workflow-sdlc-tech
mode: agent
description: 'Run full Tech pipeline — architecture through sprint-iterative implementation and continuous quality (17 stations, brownfield/greenfield aware).'
---

# /workflow-sdlc-tech

Run the Tech pipeline (Systems T0 through T4).

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project):
- Ask the user if not already clear from context.
- If brownfield: start with **T0 audit stations** (tech-audit, tech-gap) to document existing technical state.
- If greenfield: skip T0 and start directly from **T1 architecture** (tech-system-context).

## Execution

1. Read `.apm/workflows/sdlc-tech.yml` for the station sequence.
2. For brownfield: execute T0 audit stations first, then proceed through T1–T4.
3. For greenfield: skip T0, start at T1 architecture.
4. Execute remaining stations: architecture (C4, ADRs, stack, enablers) → design (data model, APIs, tests, impl plan) → implementation (task resolution, code gen, tests, validation, wave gate) → quality (drift, E2E).
5. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/docs/2-tech/`. Do not merely display content in chat.
6. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-sdlc-tech-crm.md`) directly using `edit/editFiles` following the **exact Markdown table format** defined in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder. Do **not** invent alternative formats (e.g. YAML frontmatter with `stations_completed`/`stations_remaining`).
7. After each station, verify that declared output files exist on disk before proceeding.
8. **After each station completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all stations. Never leave the initial table stale.
