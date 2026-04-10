---
name: sdlc-dast
mode: agent
description: 'Run OWASP ZAP DAST security scan.'
---

# /sdlc-dast

Run a DAST security scan with OWASP ZAP.

1. Load DAST skill from `.apm/skills/sdlc-test-campaign/docs/`.
2. Execute ZAP scan against the target URL, triage alerts by severity.
3. Write report to `outputs/docs/1-prd/4-tests/dast-rpt-{NNN}.md`.
