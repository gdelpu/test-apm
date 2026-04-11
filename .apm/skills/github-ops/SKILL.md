---
name: github-ops
description: 'Interact with GitHub via MCP — manage issues, PRs, code search, Actions status, and releases.'
triggers:
  - github issues
  - github pull request
  - github actions status
  - github code search
  - github release management
---

# Skill: github-ops

## Goal

Interact with GitHub repositories via the GitHub MCP server for issue/PR management, cross-repo code search, Actions pipeline status, and release management.

## MCP Server

- **Registry ID**: `github-mcp`
- **Repository**: https://github.com/github/github-mcp-server
- **Auth**: Personal Access Token
- **Env**: `GITHUB_TOKEN`

## Platform detection

Auto-detected when repo contains `.github/` directory or `GITHUB_TOKEN` is set.

## When to use

- Creating, updating, or querying GitHub issues and pull requests
- Searching code across GitHub repositories for reference implementations
- Checking GitHub Actions workflow run status
- Managing GitHub releases and tags
- Reading PR review comments and requested changes

## When NOT to use

- For GitLab MRs (use `gitlab-ops` skill)
- For Azure DevOps work items (use `azdo-ops` skill)
- When working with local-only git operations (no GitHub remote)

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `github-mcp` tool. If unavailable, skip to **Fallback**.

### Step 2 — Execute operation

Based on the user's request:
- **Issue management**: Create, update, list, or search issues with labels and milestones
- **PR management**: Create PRs, read review comments, check merge status, list changed files
- **Code search**: Search across organization/user repos for patterns, functions, or reference implementations
- **Actions status**: Check workflow run status, retrieve logs for failed runs
- **Release management**: Create releases, list tags, generate changelogs

### Step 3 — Format results

Write results to the appropriate output file or integrate into the current workflow deliverable.

### Fallback (without MCP)

If `github-mcp` is unavailable:
1. Use local `git` operations (log, diff, branch) for repository data
2. Parse local diff/patch files for PR-related analysis
3. Warn that GitHub-specific operations (issues, Actions, releases) are unavailable
4. For code search, fall back to local `grep`/`rg` across workspace

## Output

Integrates into the calling workflow's output files. For standalone use:
`outputs/specs/features/<feature>/github-ops-report.md`

## Security

- Only access repositories the authenticated user has read permission for
- Never expose tokens in output files
- Do not perform destructive operations (repo deletion, force push) without explicit user confirmation
