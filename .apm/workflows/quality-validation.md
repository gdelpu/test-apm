# Workflow: Quality Validation

Validate code quality, security, and compliance using external tool adapters.

## When to use

- Before merging a feature branch to main
- After implementation station in a delivery workflow
- As a standalone quality check on any codebase
- As a nested workflow inside feature-implementation or modernization
- During CI/CD pipelines as a gate before production deployment

## Stations

| # | Station | Agent | Skill | Gate | Severity | Parallel |
|---|---------|-------|-------|------|----------|----------|
| 1 | Lint Analysis | quality-validator | lint-analysis | No lint errors (warnings acceptable) | blocker | ✓ |
| 2 | Static Analysis | quality-validator | static-analysis | No blocker or critical issues | blocker | ✓ |
| 3 | Security SAST Scan | quality-validator | security-scan | No high or critical vulnerabilities | blocker | ✓ |
| 4 | Dependency Audit | quality-validator | dependency-audit | No known critical CVEs in dependencies | blocker | ✓ |
| 5 | Test Coverage Assessment | quality-validator | coverage-assessment | Coverage meets or exceeds configured threshold | blocker | ✗ |
| 6 | Security DAST Scan | quality-validator | security-scan | No critical DAST findings | warning | ✗ |
| 7 | Quality Report | quality-validator | quality-report | Aggregated pass with executive summary | blocker | ✗ |

## Tool adapters per station

| Station | Adapters |
|---------|----------|
| Lint | ESLint (JS/TS), Pylint (Python), Clippy (Rust), language-detected |
| Static Analysis | SonarQube, SonarCloud, Pylint |
| SAST | Checkmarx, Semgrep, OWASP Dependency-Check |
| Dependency Audit | Snyk, Trivy, OWASP Dependency-Check |
| Coverage | JaCoCo (Java), Istanbul (JS), Coverage.py (Python) |
| DAST | OWASP ZAP, Burp Suite |

## Outputs

All reports are written to `specs/features/<feature>/`:
- `lint-report.md` — linting violations with severity
- `static-analysis-report.md` — code smells, complexity, maintainability issues
- `sast-report.md` — source code vulnerabilities
- `dependency-report.md` — vulnerable dependencies with severity and remediation
- `coverage-report.md` — line/branch coverage metrics vs. threshold
- `dast-report.md` — runtime security findings (optional, generated only if DAST runs)
- `quality-report.md` — aggregated summary with pass/fail and trend indicators

## Configuration

- **Station 6 (DAST)** is optional and marked `warning` severity — requires a running application endpoint and is typically skipped for unit/integration test phases
- All other stations run against source code and build artifacts
- Lint station allows warnings (blocker gates only on errors)
- Coverage threshold is configurable per project (e.g., 75%, 80%)

## Parallel execution

Stations 1–4 can run in parallel (no inter-dependencies). Station 5 requires compiled artifacts. Station 6 (DAST) requires deployed app. Station 7 aggregates all prior results.

## Nestable

This workflow is nestable inside:
- `feature-implementation` (station 8)
- `modernization` (station 10)
- `bug-fixing` (station 6)
