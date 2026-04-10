---
name: workflow-pr-validation
mode: agent
description: 'Run PR validation pipeline — A0-A7 stations (11 stations).'
---

# /workflow-pr-validation

Run the PR Validation workflow.

1. Read `.apm/workflows/pr-validation.yml` for the station sequence.
2. Phase 1 (parallel): PR auto-validator → YAML workflow linter → test gap detector.
3. Phase 2 (sequential): A0 intake → A1 policy → A2 security → A3 prompt injection →
   A4 red team → A5 sandbox → A6 policy gate → A7 platform update.
4. Write reports to `outputs/station_out/`.
