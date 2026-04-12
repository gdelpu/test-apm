---
name: workflow-sdlc-ba
mode: agent
description: 'Run full BA pipeline — brownfield audit through functional design (16 stations, brownfield/greenfield aware).'
---

# /workflow-sdlc-ba

Run the BA pipeline (Systems S0 through S3).

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project):
- Ask the user if not already clear from context.
- If brownfield: start with **S0 audit stations** (ba-audit-existing, ba-audit-delta) to document the current system.
- If greenfield: skip S0 and start directly from **S1 scoping** (ba-vision).

## Execution

1. Read `.apm/workflows/sdlc-ba.yml` for the station sequence.
2. For brownfield: execute S0 audit stations first, then proceed through S1–S3.
3. For greenfield: skip S0, start at S1 scoping.
4. Execute remaining stations: scoping → specification (with fan-out) → functional design (per feature) → validation.
5. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/docs/1-prd/`. Do not merely display content in chat.
6. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `workflow-state.md` directly using `edit/editFiles` following the **exact Markdown table format** defined in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Do **not** invent alternative formats (e.g. YAML frontmatter with `stations_completed`/`stations_remaining`).
7. After each station, verify that declared output files exist on disk before proceeding.
