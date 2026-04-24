---
name: security-scan
description: 'Run security scanning tools (SAST and/or DAST) to detect vulnerabilities in source code and running applications.'
triggers: ['security scan', 'SAST', 'DAST', 'vulnerability detection']
---

# Skill: security-scan

## Goal

Run security scanning tools (SAST and/or DAST) to detect vulnerabilities in source code and running applications.

## Adapters

| Adapter | Tool | Type |
|---------|------|------|
| `checkmarx-sast-adapter.md` | Checkmarx | SAST (static) |
| `owasp-zap-dast-adapter.md` | OWASP ZAP | DAST (dynamic) |

## Procedure

### SAST (station: security-sast)

1. Check that Checkmarx CLI is installed
2. Run SAST scan against source code
3. Parse results for vulnerability severities
4. Produce `sast-report.md`

### DAST (station: security-dast)

1. Check that OWASP ZAP is installed
2. Verify target URL is reachable
3. Run DAST scan against running application
4. Parse results for alert risk levels
5. Produce `dast-report.md`

## Gate criteria

### SAST gate
- **Pass**: No high or critical vulnerabilities
- **Fail**: One or more high or critical vulnerabilities
- **Skip**: Tool not installed

### DAST gate
- **Pass**: No high-risk alerts
- **Fail**: One or more high-risk alerts
- **Skip**: Tool not installed or target not reachable

## Output

Use `edit/editFiles` to write:
- `outputs/specs/features/<feature>/sast-report.md` (for SAST station)
- `outputs/specs/features/<feature>/dast-report.md` (for DAST station)
