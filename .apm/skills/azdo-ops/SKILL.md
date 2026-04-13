---
name: azdo-ops
description: 'Interact with Azure DevOps via MCP — manage work items, boards, pipelines, and artifact feeds. Supports both local and remote MCP endpoints.'
triggers:
  - azure devops work items
  - azure devops pipeline
  - azure boards
  - azure devops artifacts
  - ado backlog
---

# Skill: azdo-ops

## Goal

Interact with Azure DevOps via MCP for work item CRUD, board management, pipeline triggers, and artifact feed queries. Supports both self-hosted (local MCP) and Azure-hosted (remote MCP) endpoints.

## MCP Servers

- **Registry IDs**: `azdo-local-mcp` (self-hosted), `azdo-remote-mcp` (Azure-hosted)
- **Repositories**:
  - Local: https://github.com/microsoft/azure-devops-mcp
  - Remote: https://learn.microsoft.com/en-us/azure/devops/mcp-server/remote-mcp-server
- **Auth**: Personal Access Token (local) or Azure Identity (remote)
- **Env**: `AZURE_DEVOPS_ORG`, `AZURE_DEVOPS_PAT` (local); `AZURE_DEVOPS_MCP_URL` (remote)

## Platform detection

Auto-detected when repo contains `azure-pipelines.yml` or `AZURE_DEVOPS_ORG` is set.

## When to use

- Creating, updating, or querying Azure DevOps work items
- Managing sprint boards and backlogs
- Checking pipeline build/release status
- Querying artifact feeds for package versions
- Syncing sprint velocity and burndown data

## When NOT to use

- For GitHub Issues/PRs (use `github-ops` skill)
- For GitLab MRs/pipelines (use `gitlab-ops` skill)
- For Jira/Confluence (use `atlassian-ops` skill)

## Procedure

### Step 1 — Check MCP availability

Try `azdo-remote-mcp` first (if `AZURE_DEVOPS_MCP_URL` is set), then `azdo-local-mcp`. If neither is available, skip to **Fallback**.

### Step 2 — Execute operation

Based on the user's request:
- **Work items**: Create, update, query work items (user stories, bugs, tasks) via WIQL or direct ID
- **Boards**: Read sprint backlog, board columns, swimlanes, iteration paths
- **Pipelines**: Check build/release pipeline status, trigger runs, retrieve logs
- **Artifacts**: Query feed packages, check versions, list upstream sources
- **Sprint data**: Pull velocity, burndown, cumulative flow data

### Step 3 — Format results

Write results to the appropriate output file or integrate into the current workflow deliverable.

### Fallback (without MCP)

If neither ADO MCP is available:
1. Use local work-item files in `outputs/` as the source of truth
2. Parse `azure-pipelines.yml` for pipeline structure (no live status)
3. Warn that ADO-specific operations (work items, boards, sprint data) are unavailable
4. Instruct user to use Azure DevOps web UI or `az boards` CLI

## Output

Integrates into the calling workflow's output files. For standalone use:
`outputs/specs/features/<feature>/azdo-ops-report.md`

## Security

- Never expose Azure DevOps PATs or organization URLs in output files
- Only access projects the authenticated user has permission to read
- Do not delete work items or pipelines without explicit user confirmation
