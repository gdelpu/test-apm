---
name: workflow-feature
mode: agent
description: 'Run end-to-end feature implementation workflow (10 stations, brownfield/greenfield aware).'
---

# /workflow-feature

Run the Feature Implementation workflow.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project):
- Ask the user if not already clear from context.
- If brownfield: the `brownfield-context` station is **mandatory** — do not skip it.
- If greenfield: skip the `brownfield-context` station.

## Execution

1. Read `.apm/workflows/feature-implementation.yml` for the station sequence.
2. **Always start at station 1 (constitution)** — never skip ahead to specification.
   Read the `spec-constitution` skill and use the brownfield or greenfield
   constitution template accordingly.
3. For brownfield projects, execute the `brownfield-context` station next:
   produce `context-brief.md` with existing architecture and constraints.
4. Continue through the remaining stations in order:
   specification → clarification → architecture review → plan → task breakdown →
   implementation → quality validation → final gate.
5. The specification station receives `context-brief.md` as input for brownfield
   projects (ensuring the spec respects existing constraints).
6. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/specs/features/<feature>/`. Do not merely display content in chat.
7. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If `runCommands` is unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-feature-implementation-login.md`) directly using `edit/editFiles` following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
8. After each station, verify that declared output files exist on disk before proceeding.
