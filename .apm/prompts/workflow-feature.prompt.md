---
name: workflow-feature
mode: agent
description: 'Run end-to-end feature implementation workflow (9 stations).'
---

# /workflow-feature

Run the Feature Implementation workflow.

1. Read `.apm/workflows/feature-implementation.yml` for the station sequence.
2. Execute each station: constitution → specification → clarification →
   architecture review → plan → task breakdown → implementation → quality validation → final gate.
3. Write all artifacts to `outputs/specs/features/<feature>/`.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-feature-implementation-login.md`) directly following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
