---
name: pr-checks
description: 'Generic PR/MR validation checks: frontmatter validation, naming conventions, broken link detection, YAML workflow linting, and test gap advisories. Delegates to ai-backbone-pr-checks for repository-specific implementations.'
triggers: ['PR checks', 'merge request validation', 'frontmatter validation', 'naming convention', 'YAML lint', 'broken links']
version: '1.0.0'
---

# Skill: PR Checks

## Purpose

Generic pull request / merge request validation covering structural quality, naming conventions, and documentation gaps. This is the provider-agnostic skill definition; for the repository-specific implementation with scripts and CI integration, see `ai-backbone-pr-checks`.

## Relationship to ai-backbone-pr-checks

| Skill | Scope |
|-------|-------|
| `pr-checks` (this skill) | Generic PR validation rules applicable to any repository |
| `ai-backbone-pr-checks` | Repository-specific implementation with Python scripts and GitLab CI integration |

## Checks

### Frontmatter Validation

- All `*.agent.md`, `SKILL.md`, `*.prompt.md`, and `*.instructions.md` files MUST have valid YAML frontmatter.
- Required fields depend on file type (see `agent-policy-guard` for agent/skill specifics).
- Malformed YAML → `blocking`.

### Naming Conventions

- Agent files: lowercase kebab-case (`my-agent.agent.md`)
- Skill folders: lowercase kebab-case (`my-skill/`)
- Prompt files: lowercase kebab-case (`my-prompt.prompt.md`)
- Non-kebab-case filenames → `blocking`.

### Link Validation

- Relative markdown links (`[text](path)`) must resolve to existing files.
- Broken links → `warning` (advisory).

### YAML Workflow Linting

- Workflow YAML files must have `name`, `on` (or `stations`), and `jobs` (or `stations`).
- Missing required fields → `blocking`.
- Missing `permissions`, use of `@main` instead of pinned versions → `warning`.

### Test Gap Detection

- Changed scripts or workflow files should have corresponding documentation updates.
- Missing documentation → `warning` (advisory only).

## Procedure

1. Identify changed files in the PR diff.
2. Apply frontmatter validation to all relevant file types.
3. Check naming conventions on all changed files.
4. Validate relative links in changed markdown files.
5. Lint workflow YAML files if any were changed.
6. Check for documentation gaps.
7. Produce a structured validation report.

## Gate Criteria

| Category | Behavior |
|----------|----------|
| Frontmatter violations | Blocking |
| Naming convention violations | Blocking |
| Broken links | Warning (advisory) |
| YAML structure errors | Blocking |
| YAML safety warnings | Warning (advisory) |
| Documentation gaps | Warning (advisory) |

## Output

Structured JSON report:

```json
{
  "status": "pass|warn|fail",
  "summary": ["..."],
  "blocking_issues": [...],
  "warnings": [...],
  "checked_files": ["..."]
}
```
