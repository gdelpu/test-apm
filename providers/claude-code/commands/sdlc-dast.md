# /sdlc-dast

Run the **DAST security scan** tool (OWASP ZAP).

$ARGUMENTS = target URL or environment identifier

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find agent `test-dast`.
2. Load `.apm/skills/sdlc-test-campaign/docs/sk-dast.md` for scan configuration.
3. Execute: run OWASP ZAP scan, triage alerts by severity, produce report.
4. Display findings summary (Critical/High/Medium/Low/Info counts).
5. Write DAST report to `docs/1-prd/4-tests/dast-rpt-{NNN}.md`.

This is an on-demand tool, typically run pre-release.
