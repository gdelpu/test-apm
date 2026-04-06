---
name: workflow-compliance-check
mode: agent
description: 'Run compliance, privacy, and AI governance validation workflow (6 stations).'
---

# /workflow-compliance-check

Run the Compliance Check workflow.

1. Read `.apm/workflows/compliance-check.yml` for the station sequence.
2. Execute each station: PII scan → prompt injection detection → policy validation →
   risk scoring → human approval → compliance report.
3. Write all artifacts to `specs/features/<feature>/`.
4. Track state in `specs/features/<feature>/workflow-state.md`.
5. Report overall compliance status (pass / conditional / fail) with gate results.
