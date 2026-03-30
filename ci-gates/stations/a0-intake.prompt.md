---
name: 'A0 – Intake'
description: 'Extract PR context (metadata, changed files, diff) and emit station_out/work_order.json for all downstream stations.'
---

# Station A0 — Intake

## Goal

Produce `station_out/work_order.json` summarising everything downstream stations need to know about this PR.

## Inputs

- GitHub PR metadata: number, title, author, base branch, head branch, creation timestamp
- `git diff --name-only` (list of changed files)
- `git diff` (unified diff, scoped to relevant file types)
- PR description body

## Processing

### 1 — Identify changed artefact types

Classify each changed file by path pattern:

| Pattern | Type |
|---------|------|
| `**/agents/**/*.agent.md` | `"agent"` |
| `**/skills/**/SKILL.md` | `"skill"` |
| `**/prompts/**/*.prompt.md` | `"prompt"` |
| `**/instructions/**/*.instructions.md` | `"instruction"` |
| `.github/workflows/**/*.yml` | `"workflow"` |
| Anything else | `"other"` |

Record each file's `change` as `"added"`, `"modified"`, or `"deleted"`.

### 2 — Compute risk hints

Scan the diff content for any of the following patterns and append the corresponding flag
to `risk_hints[]` (deduplicated):

| Pattern (regex / keyword) | Risk hint |
|---------------------------|-----------|
| `tools:` array contains `runCommands` | `"exec-tool"` |
| `allowedNetworkDomains` absent or set to `"*"` | `"unconstrained-network"` |
| `allowedFilePaths` absent or set to `"**"` | `"unconstrained-files"` |
| `/(curl\|wget\|bash\|sh)\s.*\|/` in prompt body | `"shell-pipe"` |
| `/eval\s*\(/` anywhere in the diff | `"eval-usage"` |
| any `*.agent.md` file deleted | `"agent-removed"` |

### 3 — Determine scope

- If no files of type `"agent"`, `"skill"`, `"prompt"`, or `"instruction"` are in `changed_files`,
  set `"scope": "non-agent"` — downstream stations SHOULD set `"status": "skipped"`.
- Otherwise set `"scope": "agent-change"`.

### 4 — Write output

Create `station_out/` if it does not exist, then write `station_out/work_order.json`.

## Output Schema

```json
{
  "station": "A0",
  "pr_number": 42,
  "pr_title": "feat: add data-pipeline-helper agent",
  "author": "github-handle",
  "base_branch": "main",
  "head_branch": "feature/data-pipeline-agent",
  "created_at": "2026-03-04T10:00:00Z",
  "scope": "agent-change",
  "changed_files": [
    {
      "path": ".github/agents/data-pipeline-helper.agent.md",
      "type": "agent",
      "change": "added"
    }
  ],
  "risk_hints": ["exec-tool"],
  "diff_summary": "Added agent with runCommands tool; no commandAllowlist declared."
}
```
