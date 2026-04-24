---
name: agent-policy-guard
description: 'Validate agent and skill manifest frontmatter against JSON Schema and enforce tool allowlists, safety field requirements, and structural policy rules (P-01 through P-06).'
triggers: ['policy validation', 'agent validation', 'skill validation', 'frontmatter check', 'tool allowlist', 'manifest validation']
version: '1.0.0'
---

# Skill: Agent Policy Guard

## Purpose

Enforce structural and policy rules on `*.agent.md` and `SKILL.md` files. This is the generic (non-Sopra-Steria-specific) policy guard that maps directly to the **A1 — Policy & Structure Validation** CI-gate station.

Use `soprasteria-agent-policy-guard` for the extended ruleset that also covers A2–A6 hardening. This skill focuses exclusively on A1 manifest-level rules.

## Reference Station

`ci-gates/stations/a1-policy-validation.prompt.md`

## Reference Schemas

- Agent manifest: `.apm/knowledge/governance/schemas/agent-manifest.schema.json`
- Skill manifest: `.apm/knowledge/governance/schemas/skill-manifest.schema.json`

## Policy Rules

### P-01 · Required frontmatter fields

**Agent** (`*.agent.md`) MUST have YAML frontmatter with:
- `name` — non-empty string
- `description` — non-empty string (see P-05 for length)
- `tools` — array (may be empty `[]`, but the key must exist)

**Skill** (`SKILL.md`) MUST have YAML frontmatter with:
- `name` — non-empty string
- `description` — non-empty string
- `triggers` — non-empty array of strings

**Severity if missing**: `critical`

### P-02 · Tool allowlist

Agent `tools` array MUST only contain values from:

```
codebase, search, edit/editFiles, problems, runCommands,
github, terminal, fetch, vscode
```

Any unknown tool name → `critical`.

### P-03 · No wildcard exec

When `runCommands` is in `tools`, the frontmatter MUST also declare:

```yaml
commandAllowlist:
  - <specific-command>
```

Missing or empty `commandAllowlist` when `runCommands` is present → `critical`.

### P-04 · Network safety

When `fetch` is in `tools`, the frontmatter MUST declare:

```yaml
allowedNetworkDomains:
  - example.com
```

Missing field or wildcard `"*"` → `high`.

### P-05 · Description quality

`description` shorter than 20 characters → `low`.

### P-06 · No deleted agents without issue reference

A deleted `*.agent.md` file MUST reference a GitHub/GitLab issue number in the PR/MR description (`#<number>` pattern). Missing reference → `medium`.

## Procedure

1. Read the target file's YAML frontmatter.
2. Validate against the appropriate schema (agent or skill).
3. Apply rules P-01 through P-06 in order.
4. Collect all findings with rule ID, severity, file path, and message.
5. Produce a structured policy report.

## Gate Criteria

| Condition | Status |
|-----------|--------|
| Any `critical` finding | `fail` |
| Any `high` finding | `fail` |
| Only `medium` / `low` findings | `pass` (findings still recorded) |
| No findings | `pass` |

## Output

Structured JSON report following `outputs/station_out/policy_report.json` schema:

```json
{
  "station": "A1",
  "status": "pass|fail",
  "findings": [
    {
      "rule": "P-03",
      "severity": "critical",
      "file": "<path>",
      "message": "runCommands declared without commandAllowlist"
    }
  ],
  "summary": "N critical, N high, N medium, N low"
}
```
