---
name: secret-scan
description: 'Scan PR diffs and repository files for hardcoded secrets, API keys, tokens, credentials, vulnerable dependencies, and dangerous shell/code patterns (S-01 through S-04).'
triggers: ['secret scan', 'credential detection', 'secret detection', 'API key scan', 'dependency scan', 'security static', 'dangerous pattern']
version: '1.0.0'
---

# Skill: Secret Scan

## Purpose

Detect hardcoded secrets, vulnerable dependencies, and dangerous shell/code patterns in PR diffs and repository files. Maps directly to the **A2 — Security Static Checks** CI-gate station.

## Reference Station

`ci-gates/stations/a2-security-static.prompt.md`

## Checks

### S-01 · Secret scan (diff + repo)

Scan for hardcoded credentials using Gitleaks (or equivalent):

- API keys and tokens: `ghp_`, `sk-`, `AKIA`, `-----BEGIN`
- `.env` files committed to the repo
- Credentials in frontmatter or prompt bodies: `password:`, `token:`, `api_key:`
- Generic high-entropy strings in sensitive contexts

**Severity**: `critical` for any confirmed secret.

### S-02 · Dependency scan

If any dependency manifest or lock file is in the changed files, scan with Trivy (or pip-audit / npm audit):

| CVSS Score | Severity |
|------------|----------|
| ≥ 9.0 | `critical` |
| 7.0–8.9 | `high` |
| 4.0–6.9 | `medium` |
| < 4.0 | `low` |

Report: CVE ID, package name + version, CVSS score.

### S-03 · Dangerous-pattern scan

Scan every changed file with the following regex rules:

**Exclusion**: Files under `**/fixtures/**`, `**/test*/**`, or `ci-gates/stations/**` are test assets. Matches in excluded paths are downgraded to `info` severity with `"note": "test fixture — intentional payload"`.

| Rule ID | Pattern | Description | Severity |
|---------|---------|-------------|----------|
| S-03-A | `curl .* \| (bash\|sh)` | Piping curl to shell | `critical` |
| S-03-B | `wget .* \| (bash\|sh)` | Piping wget to shell | `critical` |
| S-03-C | `\beval\s*\(` | Use of eval() | `high` |
| S-03-D | `subprocess\.call\(.*shell=True` | Python shell=True subprocess | `high` |
| S-03-E | `os\.system\(` | os.system() call | `high` |
| S-03-F | `\/\*\*` in `allowedFilePaths` | Wildcard file access | `high` |
| S-03-G | `\brm\s+-rf\s+\/` | Recursive delete from root | `critical` |
| S-03-H | `chmod\s+777` | World-writable permissions | `medium` |

### S-04 · Sensitive path access

Check for references to sensitive paths in agent tool configurations:
- `/etc/passwd`, `/etc/shadow`, `~/.ssh/`, `~/.aws/credentials`, `~/.config/`

**Severity**: `high`

## Procedure

1. Obtain the PR diff (or list of changed files).
2. Run S-01 secret scan across the diff and full repo.
3. If dependency manifests changed, run S-02 dependency scan.
4. Apply S-03 regex patterns to every changed file (with fixture exclusions).
5. Check S-04 sensitive path references.
6. Collect all findings and produce a structured security report.

## Gate Criteria

| Condition | Status |
|-----------|--------|
| Any `critical` finding | `fail` |
| Any `high` finding | `fail` |
| Only `medium` / `low` / `info` | `pass` |
| Clean | `pass` |

`info`-level findings (from test fixtures) are included for transparency but never trigger a `fail`.

## Output

Structured JSON report following `station_out/security_report.json` schema:

```json
{
  "station": "A2",
  "status": "pass|fail",
  "findings": [
    {
      "check": "S-03-A",
      "severity": "critical",
      "file": "<path>",
      "line": 14,
      "match": "<matched text>",
      "message": "Piping curl output directly to bash is a critical supply chain risk."
    }
  ],
  "dependency_scan_ran": true,
  "secret_scan_ran": true,
  "summary": "N critical, N high, N medium, N low"
}
```
