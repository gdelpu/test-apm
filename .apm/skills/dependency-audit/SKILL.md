# Skill: dependency-audit

## Goal

Scan project dependencies for known vulnerabilities (CVEs). Select the appropriate scanner based on available tools and project type.

## Adapters

| Adapter | Tool | Focus |
|---------|------|-------|
| `owasp-depcheck-adapter.md` | OWASP Dependency-Check | Java, .NET, Node.js, Python, Ruby |
| `snyk-adapter.md` | Snyk | Multi-language, container images |
| `trivy-adapter.md` | Trivy | Containers, filesystems, git repos |

## Procedure

1. Detect available adapter tools (check which are installed)
2. Prefer the first available: Snyk → OWASP Dependency-Check → Trivy
3. Run the dependency scan
4. Parse results for vulnerability severities
5. Produce `dependency-report.md`

## Gate criteria

- **Pass**: No critical CVEs in dependencies
- **Fail**: One or more critical CVEs detected
- **Skip**: No dependency scanner installed

## Output

`dependency-report.md` following the quality-validator report format.
