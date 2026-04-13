---
name: workflow-spec-kit
mode: agent
description: 'Run specification-only workflow (8 stations).'
---

# /workflow-spec-kit

Run the Spec Kit workflow.

1. Read `.apm/workflows/spec-kit.yml` for the station sequence.
2. Execute each station: constitution → specification → clarification →
   architecture review → plan → task breakdown → test strategy → quality gate.
3. Write all artifacts to `outputs/specs/features/<feature>/`.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-spec-kit-login.md`) directly following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
