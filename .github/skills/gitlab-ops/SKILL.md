---
name: gitlab-ops
description: 'Interact with GitLab via MCP — manage merge requests, pipeline status, container registry, and wiki integration.'
triggers:
  - gitlab merge request
  - gitlab pipeline
  - gitlab registry
  - gitlab wiki
  - gitlab CI status
---

# Skill: gitlab-ops

## Goal

Interact with GitLab via the GitLab MCP server for merge request management, pipeline monitoring, container registry access, and wiki integration.

## MCP Server

- **Registry ID**: `gitlab-mcp`
- **Repository**: https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_server/
- **Auth**: Personal Access Token or OAuth
- **Env**: `GITLAB_TOKEN`, `GITLAB_URL`

## Platform detection

Auto-detected when repo contains `.gitlab-ci.yml` or `GITLAB_TOKEN` is set.

## When to use

- Creating, updating, or querying GitLab merge requests
- Checking CI/CD pipeline status and logs
- Querying container registry images and tags
- Reading or updating GitLab wiki pages
- Validating `.gitlab-ci.yml` against running pipelines

## When NOT to use

- For GitHub PRs (use `github-ops` skill)
- For Azure DevOps pipelines (use `azdo-ops` skill)
- When working with local-only git operations

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `gitlab-mcp` tool. If unavailable, skip to **Fallback**.

### Step 2 — Execute operation

Based on the user's request:
- **MR management**: Create, update, list MRs; read review comments and approvals
- **Pipeline monitoring**: Check pipeline status, retrieve job logs, trigger pipelines
- **Registry access**: List container images, check tags, read manifests
- **Wiki integration**: Read/update wiki pages for documentation sync
- **CI validation**: Validate `.gitlab-ci.yml` syntax and stage resolution

### Step 3 — Format results

Write results to the appropriate output file or integrate into the current workflow deliverable.

### Fallback (without MCP)

If `gitlab-mcp` is unavailable:
1. Use local `git` operations for repository data
2. Parse local `.gitlab-ci.yml` for pipeline structure (no live status)
3. Warn that GitLab-specific operations (MRs, pipelines, registry) are unavailable
4. Use local diff/patch files for MR-related analysis

## Output

Integrates into the calling workflow's output files. For standalone use:
`outputs/specs/features/<feature>/gitlab-ops-report.md`

## Security

- Only access projects the authenticated user has permission to read
- Never expose tokens or internal GitLab URLs in output files
- Use `[REDACTED:url]` for internal GitLab hostnames
