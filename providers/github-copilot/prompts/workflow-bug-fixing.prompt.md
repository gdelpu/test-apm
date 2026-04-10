---
name: workflow-bug-fixing
mode: agent
description: 'Run structured bug diagnosis and resolution workflow (7 stations).'
---

# /workflow-bug-fixing

Run the Bug Fixing workflow.

1. Read `.apm/workflows/bug-fixing.yml` for the station sequence.
2. Execute each station: triage → reproduce → root cause → fix →
   regression testing → quality validation → summary.
3. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/specs/bugs/<bug>/`. Do not merely display content in chat.
