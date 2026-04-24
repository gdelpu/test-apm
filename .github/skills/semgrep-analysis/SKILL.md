---
name: semgrep-analysis
description: 'Run SemGrep SAST rules via MCP — scan code for vulnerabilities, query rule registry, and get fix suggestions.'
triggers:
  - semgrep scan
  - semgrep analysis
  - sast rules
  - semgrep security
  - code vulnerability scan
---

# Skill: semgrep-analysis

## Goal

Run SemGrep static analysis rules via the SemGrep MCP server for deeper SAST scanning, rule registry queries, and automated fix suggestions.

## MCP Server

- **Registry ID**: `semgrep-mcp`
- **Repository**: https://github.com/semgrep/semgrep/tree/develop/cli/src/semgrep/mcp
- **Auth**: API key (optional — enables Semgrep Cloud rules)
- **Env**: `SEMGREP_APP_TOKEN`
- **Prerequisites**: `pip install semgrep`

## Platform detection

Auto-detected when repo contains `.semgrep.yml`, `.semgrep/`, or `SEMGREP_APP_TOKEN` is set.

## When to use

- Running SAST scans with custom or community SemGrep rules
- Querying the SemGrep rule registry for rules matching a pattern
- Getting automated fix suggestions for detected vulnerabilities
- Supplementing existing security scanning (Checkmarx, OWASP) with SemGrep rules
- Scanning agent/skill definitions for security policy violations

## When NOT to use

- For DAST scanning (use `security-scan` skill with OWASP ZAP)
- For dependency vulnerability scanning (use `dependency-audit` skill)
- When SemGrep is not installed

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `semgrep-mcp` tool. If unavailable, skip to **Fallback**.

### Step 2 — Execute scan

Based on the user's request:
- **Full scan**: Run all configured rules against workspace files
- **Targeted scan**: Run specific rulesets (e.g., `p/owasp-top-ten`, `p/security-audit`)
- **Rule query**: Search the SemGrep registry for rules matching a vulnerability type
- **Fix suggestions**: For each finding, request automated fix suggestion

### Step 3 — Classify findings

Map SemGrep severities to the standard gate criteria:
| SemGrep severity | Gate severity |
|-----------------|---------------|
| ERROR | critical |
| WARNING | high |
| INFO | medium |

### Step 4 — Format results

Write findings to the security report with standard metadata frontmatter.

### Fallback (without MCP)

If `semgrep-mcp` is unavailable:
1. Run `semgrep` CLI directly if installed (`semgrep scan --config auto`)
2. If SemGrep CLI is also unavailable, fall back to the existing regex-based dangerous-pattern scan (A2 station S-03 rules)
3. Warn that advanced SemGrep rules and fix suggestions are unavailable
4. Instruct user to install SemGrep: `pip install semgrep`

## Gate criteria

- **Pass**: No critical or high findings
- **Fail**: One or more critical or high findings
- **Skip**: SemGrep not installed and no fallback scanner available

## Output

Use `edit/editFiles` to write: `outputs/specs/features/<feature>/semgrep-report.md`

## Security

- Restrict scans to workspace files only — never scan files outside the repository root
- Do not send source code to external SemGrep Cloud without explicit user consent
- API tokens for SemGrep Cloud are optional and controlled via `SEMGREP_APP_TOKEN`
