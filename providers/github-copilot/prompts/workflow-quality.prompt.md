---
name: workflow-quality
mode: agent
description: 'Run code quality validation workflow (7 stations).'
---

# /workflow-quality

Run the Quality Validation workflow.

1. Read `.apm/workflows/quality-validation.yml` for the station sequence.
2. Execute each station: lint → static analysis → SAST → dependency audit →
   coverage check → DAST → quality report.
3. Write the final report to `quality-report.md`.
