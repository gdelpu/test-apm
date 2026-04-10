---
name: static-analysis
description: 'Run static analysis tools to detect code quality issues, bugs, code smells, and security vulnerabilities.'
triggers: ['static analysis', 'code quality', 'code smells', 'SonarQube']
---

# Skill: static-analysis

## Goal

Run static analysis tools to detect code quality issues, bugs, code smells, and security vulnerabilities. Evaluate the tool's quality gate status.

## Adapters

| Adapter | Tool | Mode |
|---------|------|------|
| `sonarqube-adapter.md` | SonarQube | Self-hosted server |
| `sonarcloud-adapter.md` | SonarCloud | Cloud-hosted |

## Procedure

1. Detect whether SonarQube or SonarCloud is configured (look for `sonar-project.properties` or environment variables)
2. Check that the scanner is installed
3. Run the analysis
4. Retrieve quality gate status from the API
5. Produce `static-analysis-report.md`

## Gate criteria

- **Pass**: Quality gate status is "passed", no blocker or critical issues
- **Fail**: Quality gate status is "failed" or blocker/critical issues exist
- **Skip**: Scanner not installed or server not reachable

## Output

Use `edit/editFiles` to write: `outputs/specs/features/<feature>/static-analysis-report.md`
