---
name: 'A1 – Policy & Structure Validation'
description: 'Validate agent and skill manifests against JSON Schema; enforce tool allowlists, safety field requirements, and structural rules.'
---

# Station A1 — Policy & Structure Validation

## Goal

Validate every changed agent and skill manifest against workspace policy rules.
Emit `outputs/station_out/policy_report.json`.

## Inputs

- `outputs/station_out/work_order.json`
- Changed files where `type == "agent"` or `type == "skill"`
- `.apm/knowledge/governance/schemas/agent-manifest.schema.json`
- `.apm/knowledge/governance/schemas/skill-manifest.schema.json`

## Target Selection

From `work_order.json` → `changed_files`, collect entries where `type == "agent"` or `type == "skill"`.
**Exclude any file whose path starts with `ci-gates/stations/`** — those are pipeline
infrastructure files, not user-authored agents or skills. Validating them produces false positives.

## Skip Condition

If `work_order.json` has `"scope": "non-agent"`, or if no eligible files remain after the exclusion above:

```json
{ "station": "A1", "status": "skipped", "findings": [], "summary": "No user-authored agent/skill files changed." }
```

## Policy Rules

### P-01 · Required frontmatter fields

**Agent** `*.agent.md` MUST have YAML frontmatter with:
- `name` — non-empty string
- `description` — non-empty string (see P-05 for length)
- `tools` — array (may be empty `[]`, but the key must exist)

**Skill** `SKILL.md` MUST have YAML frontmatter with:
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
Any unknown tool name → `critical` finding per tool.

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

A deleted `*.agent.md` file MUST reference a GitHub issue number in the PR description
(`#<number>` pattern). Missing reference → `medium`.

## Output Schema

```json
{
  "station": "A1",
  "status": "pass",
  "findings": [
    {
      "rule": "P-03",
      "severity": "critical",
      "file": ".github/agents/data-pipeline-helper.agent.md",
      "message": "runCommands declared without commandAllowlist",
      "line": null
    }
  ],
  "summary": "1 critical, 0 high, 0 medium, 0 low"
}
```

## Pass / Fail

| Condition | Status |
|-----------|--------|
| Any `critical` finding | `"fail"` |
| Any `high` finding | `"fail"` |
| Only `medium` / `low` findings | `"pass"` (findings still recorded) |
| No findings | `"pass"` |
