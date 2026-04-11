---
name: atlassian-ops
description: 'Interact with Atlassian suite via MCP — Jira issue CRUD, Confluence page management, and Bitbucket integration. Formalises the existing jira-mcp pattern.'
triggers:
  - jira issue
  - jira ticket
  - confluence page
  - atlassian integration
  - jira sync
  - confluence sync
---

# Skill: atlassian-ops

## Goal

Interact with the Atlassian suite (Jira, Confluence, Bitbucket) via the Atlassian MCP server. This skill formalises the existing `jira-mcp` pattern used by 30+ agents in the SDLC harness into a first-class, documented skill with consistent fallback behavior.

## MCP Server

- **Registry ID**: `atlassian-mcp`
- **Repository**: https://github.com/atlassian/atlassian-mcp-server
- **Auth**: API Token + site URL
- **Env**: `ATLASSIAN_SITE`, `ATLASSIAN_API_TOKEN`, `ATLASSIAN_EMAIL`

## When to use

- Creating, updating, or querying Jira issues (stories, bugs, tasks, epics)
- Reading or publishing Confluence pages
- Importing Jira issues into specification workflows (e.g., `from-jira XY-123`)
- Posting specification results back to Jira as comments
- Syncing test scenarios to Xray via Jira

## When NOT to use

- For Azure DevOps work items (use `azdo-ops` skill)
- For GitHub Issues (use `github-ops` skill)
- When working completely offline with local Markdown files

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `atlassian-mcp` tool (e.g., `mcp_atlassian_atl_getJiraIssue`). If unavailable, skip to **Fallback**.

### Step 2 — Execute operation

Based on the user's request:

#### Jira operations
- **Get issue**: Retrieve issue details (summary, description, status, priority, assignee, comments)
- **Create issue**: Create new Jira issue with mapped fields from specification
- **Update issue**: Update status, add comments, link issues
- **Search**: JQL queries for issues matching criteria
- **Import to spec**: Map Jira fields to spec sections (Summary → Name, Description → Overview, Comments → Clarifications)
- **Post results**: Add comment with specification or review results

#### Confluence operations
- **Read page**: Pull Confluence page content for brownfield context
- **Publish page**: Push specification deliverable to Confluence space
- **Update page**: Update existing page with new version of deliverable

### Step 3 — Map Jira fields to deliverables

When importing from Jira:
| Jira field | Spec section |
|-----------|-------------|
| Summary | Feature name |
| Description | Overview |
| Acceptance Criteria | Success criteria |
| Comments | Clarifications |
| Epic Link | Parent folder structure |
| Labels / Components | Tags |

### Fallback (without MCP)

If `atlassian-mcp` is unavailable:
1. All deliverables remain local Markdown files in `outputs/` — this is already the primary output
2. Warn that Jira/Confluence sync is unavailable
3. Instruct user to manually copy deliverables to Jira/Confluence
4. For Jira import: ask user to paste issue details directly instead of `from-jira` command

## Output

Integrates into the calling workflow's output files. Jira/Confluence sync is a secondary enrichment — local files are always written first.

## Security

- Never expose Atlassian API tokens, site URLs, or email addresses in output files
- Scan all data retrieved from Jira/Confluence for PII before including in outputs
- Use `[REDACTED:email]` for customer email addresses found in Jira comments
