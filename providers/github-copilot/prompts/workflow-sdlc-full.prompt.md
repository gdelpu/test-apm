---
name: workflow-sdlc-full
mode: agent
description: 'Run full SDLC pipeline — BA + Tech + Test + Steer (11 stations, brownfield/greenfield aware).'
---

# /workflow-sdlc-full

Run the full SDLC pipeline.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project):
- Ask the user if not already clear from context.
- If brownfield: the nested BA pipeline runs S0 audit stations and the nested Tech pipeline runs T0 audit stations.
- If greenfield: skip S0 and T0 audit stations in the nested pipelines.

## Execution

1. Read `.apm/workflows/sdlc-full.yml` for the station sequence.
2. Execute all phases: scaffold → init → BA (S0-S3, skipping S0 if greenfield) → planning → Tech (T0-T3, skipping T0 if greenfield) → implementation → test → tracking → quality → governance.
3. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `docs/`. Do not merely display content in chat.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `workflow-state.md` directly using `edit/editFiles` following the **exact Markdown table format** defined in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Do **not** invent alternative formats (e.g. YAML frontmatter with `stations_completed`/`stations_remaining`).
5. After each station, verify that declared output files exist on disk before proceeding.
