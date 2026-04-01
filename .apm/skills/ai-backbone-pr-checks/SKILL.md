---
name: ai-backbone-pr-checks
description: 'Deterministic merge request validation for Copilot assets: frontmatter, workflow YAML quality, and repository-specific test-gap advisories. Runs on GitLab CI.'
triggers: ['PR validation', 'merge request checks', 'frontmatter validation', 'YAML lint', 'test gap detection']
---

# AI Backbone Merge Request Checks

Shared SDLC validation skill for this repository, automated via GitLab CI/CD pipeline.

## Scripts

All scripts output JSON reports following a shared contract.

- `tools/scripts/pr_auto_validator.py` — validates frontmatter, naming, and links in changed files
- `tools/scripts/yaml_workflow_linter.py` — validates workflow YAML structure and safety
- `tools/scripts/test_gap_detector.py` — advisory-only: detects documentation gaps

## Report Contract

Each script writes JSON with these top-level keys:

- `status`: `pass`, `warn`, or `fail` (fail blocks MR, warn is advisory)
- `summary`: short human-readable bullets
- `blocking_issues`: deterministic failures (empty if no blocks)
- `warnings`: advisory findings (empty if no warnings)
- `metadata`: script-specific metadata dict
- `checked_files`: list of file paths inspected

## Local Usage (Development)

Test validators locally before pushing changes:

```bash
# Lint all workflow files (no git diff needed)
python .apm/skills/ai-backbone-pr-checks/tools/scripts/yaml_workflow_linter.py --root . --out reports/yaml-workflow-linter.json

# Validate changed files between HEAD~1 and HEAD
python .apm/skills/ai-backbone-pr-checks/tools/scripts/pr_auto_validator.py --base-ref HEAD~1 --head-ref HEAD --out reports/pr-auto-validator.json

# Detect documentation gaps
python .apm/skills/ai-backbone-pr-checks/tools/scripts/test_gap_detector.py --base-ref HEAD~1 --head-ref HEAD --out reports/test-gap-detector.json
```

## CI Usage (GitLab)

The GitLab CI pipeline (`.gitlab-ci.yml` at repository root) automatically runs all three validators on merge requests:

1. **Pipeline trigger**: Merge request events (opened, synchronized, ready_for_review)
2. **Execution**: Runs on `python:3.11` image with PyYAML dependency
3. **Output**: Writes reports to `reports/` directory and uploads as artifacts (14-day retention)
4. **Comment**: Posts aggregated summary comment on the merge request
5. **Gating**: Only blocking issues cause MR to fail; warnings are advisory only

### CI/CD Variables

To enable optional features in CI:

- `ENABLE_COPILOT_CLI`: Set to `true` to run Copilot CLI advisory mode (requires additional setup)
- `COPILOT_CI_TOKEN`: (Optional) GitLab secret for GitHub Copilot token if using advisory mode

## Validation Gating Policy

| Category | Issue Type | Behavior |
|----------|-----------|----------|
| **Frontmatter** | Missing or malformed | Blocking (fail) |
| **Naming** | Non-kebab-case filenames | Blocking (fail) |
| **Links** | Broken relative links in markdown | Warning (advisory) |
| **Workflow Structure** | Missing name, on, jobs, or steps | Blocking (fail) |
| **Workflow Safety** | Missing permissions, @main references | Warning (advisory) |
| **Documentation Gaps** | Scripts/workflows without docs updates | Warning (advisory) |

