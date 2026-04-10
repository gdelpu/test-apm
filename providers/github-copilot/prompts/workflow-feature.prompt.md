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
4. Track state in `outputs/specs/features/<feature>/workflow-state.md`.
