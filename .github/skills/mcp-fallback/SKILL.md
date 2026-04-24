---
name: mcp-fallback
description: 'Canonical reference for fallback behavior when MCP servers are unavailable — documents what happens per category and server.'
triggers:
  - mcp fallback
  - mcp unavailable
  - without mcp
  - mcp degradation
---

# Skill: mcp-fallback

## Goal

Canonical reference for the graceful degradation behavior of all MCP-dependent features. Every agent and skill that uses MCP tools must follow these fallback contracts.

## Core principle

> MCP tools are **optional enrichments**. The primary deliverables are always local files written to `outputs/`. No workflow ever fails because an MCP server is unavailable.

## Fallback matrix

| MCP Server | Category | With MCP | Without MCP (Fallback) |
|------------|----------|----------|------------------------|
| `azure-mcp` | Cloud | Live resource queries, IaC drift detection, service health | Local IaC templates (Bicep/ARM/Terraform), manual Azure portal |
| `aws-mcp` | Cloud | Live resource queries, stack drift detection, quota checks | Local CloudFormation/CDK templates, manual AWS console |
| `github-mcp` | DevOps | Issue/PR management, code search, Actions status, releases | Local git operations, diff/patch files, manual GitHub UI |
| `gitlab-mcp` | DevOps | MR management, pipeline status, registry, wiki | Local git operations, `.gitlab-ci.yml` parsing, manual GitLab UI |
| `azdo-local-mcp` | DevOps | Work items, boards, pipelines, artifact feeds | Local Markdown work-item files, `azure-pipelines.yml` parsing |
| `azdo-remote-mcp` | DevOps | Same as local via remote endpoint | Falls back to `azdo-local-mcp`, then to local Markdown files |
| `atlassian-mcp` | Collaboration | Jira CRUD, Confluence pages, Bitbucket integration | Local Markdown files — all deliverables remain file-first |
| `work-iq-mcp` | Collaboration | M365 emails, meetings, Teams messages, OneDrive, people | Manual input of meeting notes and email summaries |
| `mslearn-mcp` | Documentation | Current .NET/Azure/M365 API references | Agent training knowledge, `[DOCS-NOT-VERIFIED]` markers |
| `context7` | Documentation | Up-to-date docs for any library/framework | Agent training knowledge, `[DOCS-NOT-VERIFIED]` markers |
| `playwright-mcp` | Testing | Live browser interaction, accessibility snapshots, test recording | Playwright CLI execution, static HTML analysis |
| `semgrep-mcp` | Testing | Advanced SAST rules, rule registry, fix suggestions | SemGrep CLI, then regex-based A2 station S-03 rules |
| `figma-mcp` | Design | Figma design import, token extraction, prototype sync | Local HTML/CSS prototypes, `.apm/knowledge/brand/` tokens |

## Fallback cascade pattern

For tools with multiple fallback levels:

```
MCP tool → CLI tool → Built-in analysis → Manual instruction
```

Example for SemGrep:
1. `semgrep-mcp` (MCP) → richest: interactive rules, fix suggestions
2. `semgrep scan --config auto` (CLI) → good: same engine, no interactivity
3. Regex-based S-03 rules (built-in) → basic: pattern matching only
4. Manual review instruction → minimal: tell user to run SemGrep manually

## Implementation pattern

Every skill that uses MCP MUST follow this pattern in its procedure:

```markdown
### Step N — Check MCP availability

Attempt to invoke the `<server-id>` tool. If unavailable, skip to **Fallback**.

### Step N+1 — [MCP-enhanced operation]

...

### Fallback (without MCP)

If `<server-id>` is unavailable:
1. [Primary fallback — local tool or file-based]
2. [Secondary fallback — manual instruction]
3. Warn that [specific capability] is unavailable
4. [Quality marker if applicable, e.g., [DOCS-NOT-VERIFIED]]
```

## Quality markers

When degrading, skills should add markers to output content:

| Marker | Meaning |
|--------|---------|
| `[DOCS-NOT-VERIFIED]` | Code examples not verified against current documentation |
| `[LIVE-STATE-NOT-CHECKED]` | IaC not validated against deployed resources |
| `[MANUAL-SYNC-REQUIRED]` | Deliverable not synced to external tool (Jira, Confluence, Figma) |
| `[BROWSER-NOT-TESTED]` | E2E tests generated but not executed against live app |
| `[SAST-BASIC-ONLY]` | Only basic pattern matching used, not full SAST engine |
