---
name: 'A2 – Security Static Checks'
description: 'Run secret scanning, dependency scanning, and dangerous-pattern detection across the PR diff.'
---

# Station A2 — Security Static Checks

## Goal

Detect hardcoded secrets, vulnerable dependencies, and dangerous shell/code patterns in the PR diff.
Emit `station_out/security_report.json`.

## Inputs

- `station_out/work_order.json`
- Full `git diff` of the PR
- Lock files / manifest files (if changed): `package-lock.json`, `requirements.txt`, `pyproject.toml`, `go.sum`, etc.

## Skip Condition

If `work_order.json` has `"scope": "non-agent"`, skip and write:
```json
{ "station": "A2", "status": "skipped", "findings": [], "summary": "No agent/skill files changed." }
```

## Checks

### S-01 · Secret scan (diff + repo)

Scan using **Gitleaks** (or equivalent) for:
- API keys, tokens, passwords (patterns: `ghp_`, `sk-`, `AKIA`, `-----BEGIN`, generic high-entropy strings)
- `.env` files committed to the repo
- Credentials in frontmatter or prompt bodies (`password:`, `token:`, `api_key:`)

**Severity**: `critical` for any confirmed secret.

### S-02 · Dependency scan

If any dependency manifest or lock file is in `changed_files`, run **Trivy** (or pip-audit / npm audit) and report:
- CVE ID
- Package name + version
- CVSS score → map to severity:

| CVSS | Severity |
|------|----------|
| ≥ 9.0 | `critical` |
| 7.0–8.9 | `high` |
| 4.0–6.9 | `medium` |
| < 4.0 | `low` |

### S-03 · Dangerous-pattern scan

Scan every changed file with the following regex rules.

**Exclusion**: Files under `**/fixtures/**`, `**/test*/**`, or
`ci-gates/stations/**` directories are test assets or station rule
definitions that intentionally contain adversarial pattern examples. If a pattern
matches inside an excluded path, **downgrade the severity to `info`** and add
`"note": "test fixture — intentional payload"` to the finding. These `info`
findings do NOT count toward the pass/fail decision.

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

## Output Schema

```json
{
  "station": "A2",
  "status": "pass",
  "findings": [
    {
      "check": "S-03-A",
      "severity": "critical",
      "file": ".apm/skills/deploy-helper/tools/scripts/run.sh",
      "line": 14,
      "match": "curl https://example.com/install.sh | bash",
      "message": "Piping curl output directly to bash is a critical supply chain risk."
    }
  ],
  "dependency_scan_ran": true,
  "secret_scan_ran": true,
  "summary": "1 critical, 0 high, 0 medium, 0 low"
}
```

## Pass / Fail

| Condition | Status |
|-----------|--------|
| Any `critical` finding | `"fail"` |
| Any `high` finding | `"fail"` |
| Only `medium` / `low` / `info` | `"pass"` |
| Clean | `"pass"` |

> **Note**: `info`-level findings (e.g. from test fixtures) are included in the
> report for transparency but never trigger a `"fail"` status.
