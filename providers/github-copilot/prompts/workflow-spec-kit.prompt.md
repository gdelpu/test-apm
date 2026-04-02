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
3. Write all artifacts to `specs/features/<feature>/`.
