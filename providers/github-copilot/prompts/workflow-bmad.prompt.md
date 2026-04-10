---
name: workflow-bmad
mode: agent
description: 'Run Build → Measure → Analyze → Decide feedback loop (4 stations).'
---

# /workflow-bmad

Run the BMAD workflow.

1. Read `.apm/workflows/bmad.yml` for the station sequence.
2. Execute each station: build → measure → analyze → decide.
3. If the decision is "retry", loop back to the build station.
4. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/specs/features/<feature>/`. Do not merely display content in chat.
