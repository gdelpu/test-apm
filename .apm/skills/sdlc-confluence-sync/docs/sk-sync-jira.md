# Skill: Jira Synchronization

## Identity

- **ID:** agent-sync-jira
- **System:** Cross-cutting utility
- **Trigger:** On demand, after validating Epics, Features and User Stories

## Execution Prerequisites

> This agent requires one of the options below to call the Jira API.

### Option A — MCP Jira (recommended)

A Jira MCP server must be configured in the agent execution system:

| Property | Value |
|----------|-------|
| **MCP Server** | `jira-mcp` or `atlassian-mcp` (open source) |
| **Required capabilities** | `create_issue`, `update_issue`, `search_issues`, `get_issue`, `add_label` |
| **Auth** | Environment variables: `JIRA_USER_EMAIL` + `JIRA_API_TOKEN` |
| **Config** | `JIRA_INSTANCE_URL` + `JIRA_PROJECT_KEY` |

### Option B — Custom API Tools (fallback)

If no Jira MCP is available, the following tools must be exposed by the execution system:

| Tool | Signature | Description |
|------|-----------|-------------|
| `jira_create_issue` | `(project_key, summary, type, description, labels[], epic_link)` | Creates an issue |
| `jira_update_issue` | `(issue_key, fields{})` | Updates an issue |
| `jira_search` | `(jql_query)` -> `[issues]` | Search by JQL (e.g.: by BA-ID label) |
| `jira_get_issue` | `(issue_key)` -> `{fields}` | Reads an issue (for reverse sync) |

These tools wrap the Jira v3 REST API and can be implemented in Python (`requests`) or Node.js.

---

## Mission

You are a utility agent responsible for synchronizing Epics, Features and User Stories from Markdown format to Jira, and vice versa.

## Inputs

- **Markdown files**: Epics [EP-xxx], Features [FT-xxx], User Stories [US-xxx] produced by BA agents
- **Jira configuration**: instance URL, target project, credentials (via environment variables)

## Expected Output

- Epics, Features and User Stories created/updated in Jira
- Jira identifiers (e.g.: PROJ-123) added back to Markdown files for bidirectional traceability

## Markdown -> Jira Mapping

### Epics

| Markdown Field | Jira Field |
|----------------|------------|
| Front matter `id` (EP-xxx) | Custom label "BA-ID" |
| Front matter `title` | Summary |
| "Description" section | Description |
| Front matter `priority` | Priority |
| Front matter `status` | Status (mapping to configure) |

### Features

| Markdown Field | Jira Field |
|----------------|------------|
| Front matter `id` (FT-xxx) | Custom label "BA-ID" |
| Front matter `title` | Summary |
| Front matter `epic` (EP-xxx) | Parent Epic link |
| "Description" section | Description |
| Front matter `priority` | Priority |
| Front matter `status` | Status (mapping to configure) |

### User Stories

| Markdown Field | Jira Field |
|----------------|------------|
| Front matter `id` (US-xxx) | Custom label "BA-ID" |
| Story "As a... I want... so that..." | Summary + Description |
| Front matter `epic` | Epic Link |
| Front matter `priority` | Priority |
| "Acceptance Criteria" section | "Acceptance Criteria" field or Description |
| "Business Rules" field | Labels or links to "Business Rule" issue type |

### Statuses

| Markdown Status | Suggested Jira Status |
|-----------------|----------------------|
| `draft` | To Do / Backlog |
| `review` | In Review |
| `validated` | Ready for Dev |

## Synchronization Principle

### Markdown -> Jira (push)

```
1. Parse the YAML front matter of the MD file
2. Search in Jira if an item with label "BA-ID: US-xxx" exists
3. If not: create the Jira issue
4. If yes: update the Jira issue
5. Retrieve the Jira ID (PROJ-123)
6. Add the Jira ID to the MD file front matter: jira_id: PROJ-123
```

### Jira -> Markdown (pull)

```
1. Read Jira issues with a "BA-ID" label
2. For each issue:
   a. Check if status changed in Jira -> update MD
   b. Check if priority changed -> update MD
   c. DO NOT overwrite MD content (MD remains the source of truth for content)
3. Only management fields (status, priority, assignee) are synced from Jira to MD
```

### Conflict Management

- **Content (description, criteria)**: Markdown is ALWAYS the source of truth
- **Management fields (status, priority, sprint)**: Jira is the source of truth
- In case of changes on both sides: last modified wins for management fields; MD always wins for content

## Jira API — Examples

### Create a story

```bash
curl -X POST \
  "https://{instance}.atlassian.net/rest/api/3/issue" \
  -H "Authorization: Basic {credentials}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": { "key": "PROJ" },
      "summary": "US-001 - Create an order as a Manager",
      "issuetype": { "name": "Story" },
      "description": {
        "type": "doc",
        "version": 1,
        "content": [...]
      },
      "labels": ["BA-ID:US-001"],
      "customfield_10014": "PROJ-10"  // Epic Link
    }
  }'
```

### Search by BA-ID

```bash
curl -X GET \
  "https://{instance}.atlassian.net/rest/api/3/search?jql=labels%3D%22BA-ID%3AUS-001%22" \
  -H "Authorization: Basic {credentials}"
```

## Required Configuration

```yaml
# jira-config.yaml
jira:
  instance_url: "https://your-instance.atlassian.net"
  project_key: "PROJ"
  auth:
    type: "api_token"  # or "oauth2"
    # Credentials are in environment variables:
    # JIRA_USER_EMAIL and JIRA_API_TOKEN

  mapping:
    story_issue_type: "Story"
    epic_issue_type: "Epic"
    acceptance_criteria_field: "customfield_10100"  # Adapt for your instance
    ba_id_label_prefix: "BA-ID"

  sync:
    direction: "bidirectional"  # or "md-to-jira" / "jira-to-md"
    content_source_of_truth: "markdown"
    piloting_source_of_truth: "jira"
```

## Security

- Jira credentials are NEVER stored in Markdown files or in the Git repo
- Use environment variables or a secrets manager
- The API token must have minimum necessary permissions (read/write on target project only)
