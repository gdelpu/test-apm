---
name: workflow-modernization
mode: agent
description: 'Run guided modernization workflow (10 stations).'
---

# /workflow-modernization

Run the Modernization workflow.

1. Read `.apm/workflows/modernization.yml` for the station sequence.
2. Execute each station: baseline → decisions → target state → architecture review →
   migration plan → risk clarification → task breakdown → implementation → quality validation → PR validation.
3. Write all artifacts to `outputs/specs/features/<feature>/`.
4. Track state in `outputs/specs/features/<feature>/workflow-state.md`.
