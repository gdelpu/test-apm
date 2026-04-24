# Skill: Requirements Synchronization with Jira R4J

## Identity

- **ID:** agent-sync-r4j
- **System:** Cross-cutting utility
- **Trigger:** After human validation of the Scoping Dossier (System 1), then at each update of the requirements catalog

## Execution Prerequisites

> This agent requires the Jira plugin **R4J – Requirements Management for Jira** (Appfire/eazyBI) installed on the target Jira instance, as well as one of the API access options below.

### Required Jira Plugin

| Property | Value |
|----------|-------|
| **Plugin** | R4J – Requirements Management for Jira (Appfire) |
| **Minimum version** | Compatible with Jira Cloud or Jira Server 8.x+ |
| **Jira issue type** | `Requirement` (created by R4J upon installation) |
| **R4J traceability links** | `implements`, `tested by`, `derived from` (configurable in R4J) |

### Option A — MCP Jira (recommended)

A Jira MCP server must be configured in the agent execution system:

| Property | Value |
|----------|-------|
| **MCP Server** | `jira-mcp` or `atlassian-mcp` (open source) |
| **Required capabilities** | `create_issue`, `update_issue`, `search_issues`, `get_issue`, `link_issues`, `add_label` |
| **Auth** | Environment variables: `JIRA_USER_EMAIL` + `JIRA_API_TOKEN` |
| **Config** | `JIRA_INSTANCE_URL` + `JIRA_PROJECT_KEY` + `JIRA_R4J_REQUIREMENT_ISSUETYPE` |

### Option B — Custom API Tools (fallback)

If no Jira MCP is available, the following tools must be exposed by the execution system:

| Tool | Signature | Description |
|------|-----------|-------------|
| `jira_create_issue` | `(project_key, summary, type, description, labels[], priority)` -> `{issue_key}` | Creates a `Requirement` type issue |
| `jira_update_issue` | `(issue_key, fields{})` | Updates an existing issue |
| `jira_search` | `(jql_query)` -> `[issues]` | Search by JQL (e.g.: `labels = "BA-EX-001"`) |
| `jira_get_issue` | `(issue_key)` -> `{fields}` | Reads an issue (to check before update) |
| `jira_link_issues` | `(source_key, target_key, link_type)` -> `{link_id}` | Creates an R4J link between two issues |
| `jira_add_label` | `(issue_key, label)` | Adds a label to an issue |

These tools wrap the Jira v3 REST API and can be implemented in Python (`requests`) or Node.js.

---

## Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `JIRA_INSTANCE_URL` | Jira instance URL | `https://mycompany.atlassian.net` |
| `JIRA_USER_EMAIL` | Service account email | `ba-agent@mycompany.com` |
| `JIRA_API_TOKEN` | Jira API token | `ATATxxxxxxxx` |
| `JIRA_PROJECT_KEY` | Target Jira project key | `PROJ` |
| `JIRA_R4J_REQUIREMENT_ISSUETYPE` | Exact name of R4J issue type | `Requirement` (default) |

---

## Mission

You are a utility agent responsible for synchronizing the Markdown functional requirements catalog (`1.4-functional-requirements.md`) to Jira, creating `Requirement` type issues managed by the R4J plugin, and establishing **traceability links** between these requirements and other Jira project components (Epics, Stories, Tests, Bugs).

The complete traceability assured by this process is:

```
EX-xxx (R4J Requirement)
    -> implements
  EP-xxx / FT-xxx (Jira Epic / Story)
    -> implements
  US-xxx (Jira User Story)
    -> tested by
  TS-xxx (Xray Test)
    -> (automatic via Jira dev panel)
  Code commits / Pull Requests
    ->
  Bugs (linked Jira issues)
```

## Inputs

- **`1.4-functional-requirements.md`**: requirements catalog validated by System 1 human gate
- **Jira configuration**: environment variables (URL, project, credentials)
- **`r4j-mapping.json`** (optional): existing mapping file from previous synchronizations
- **`jira-mapping.json`** (optional): existing mapping of Epics/Stories to create links

---

## Expected Output

1. All `EX-xxx` requirements created/updated in Jira as `Requirement` issues
2. R4J links created between requirements and Epics/Stories already synchronized via `agent-sync-jira.md`
3. The **`r4j-mapping.json`** file produced/updated with the bidirectional mapping
4. Jira identifiers (`PROJ-xxx`) added to the `Jira R4J` field of the source Markdown file

---

## Markdown -> Jira R4J Mapping

### Requirements -> Requirement Issues

| Markdown Field (`EX-xxx`) | Jira Field |
|---------------------------|------------|
| Front matter `id` (EX-xxx) | Label `BA-ID` (e.g.: `BA-EX-001`) |
| `title` field (requirement title) | Summary |
| "Description" section | Description |
| `priority` field (MoSCoW) | Priority (mapping below) |
| `criticality` field | Label `criticality-critical` / `criticality-high` / `criticality-standard` |
| `category` field | Category label (e.g.: `cat-functional`) |
| `domain` field | Domain label (e.g.: `domain-orders`) |
| `source` field | "Source" text field (custom field) or Description |
| `depends_on` field (EX-yyy) | Jira `depends on` link to corresponding issue |
| Front matter `status` | Jira Status (mapping below) |

### MoSCoW Priorities -> Jira Priority

| Markdown Priority | Suggested Jira Priority |
|-------------------|------------------------|
| `Must` | Highest |
| `Should` | High |
| `Could` | Medium |
| `Won't` | Low |

### Statuses -> Jira Status

| Markdown Status | Suggested Jira Status |
|-----------------|----------------------|
| `draft` | To Do / Backlog |
| `review` | In Review |
| `validated` | Done / Approved |

---

## Detailed Instructions

### Step 1: Load Existing Mapping

1. Check if `r4j-mapping.json` exists
2. If yes, load the `EX-xxx` -> `PROJ-xxx` mapping to identify already synchronized requirements
3. If no, initialize an empty mapping

### Step 2: Traverse the Requirements Catalog

For each requirement `EX-xxx` in `1.4-functional-requirements.md`:

#### Case A — Requirement not yet synchronized (not in mapping)

1. **Verify** via `jira_search` (JQL: `project = PROJ AND labels = "BA-EX-xxx"`) that it doesn't already exist (protection against duplicates)
2. If it doesn't exist: **Create** the issue via `jira_create_issue` with mapped fields
3. Retrieve the generated Jira key (`PROJ-xxx`)
4. Add the label `BA-EX-xxx` to the issue
5. Record the mapping in `r4j-mapping.json`
6. **Update** the Markdown file: fill the `Jira R4J` field with the key `PROJ-xxx`

#### Case B — Requirement already synchronized (present in mapping)

1. Retrieve the Jira key from `r4j-mapping.json`
2. **Compare** the Markdown content with the existing Jira issue (summary, description, priority)
3. If differences are detected: **Update** the issue via `jira_update_issue`
4. Log the modifications made

### Step 3: Create R4J Traceability Links

After synchronizing all requirements, create traceability links to existing components:

#### 3a. Requirements -> Epics/Features Links

For each requirement with downstream traceability (`[EP-xxx]`, `[FT-xxx]`):
1. Look up the corresponding Jira key in `jira-mapping.json`
2. Create an R4J `implements` link between the Requirement issue and the Epic/Story Jira:
   ```
   jira_link_issues(
     source_key = "PROJ-R4J-xxx",   # Requirement issue
     target_key = "PROJ-yyy",        # Epic issue
     link_type  = "implements"
   )
   ```

#### 3b. Dependent Requirements Links

For each pair `EX-xxx depends_on EX-yyy`:
1. Retrieve both Jira keys from `r4j-mapping.json`
2. Create a `depends on` link:
   ```
   jira_link_issues(
     source_key = "PROJ-R4J-xxx",
     target_key = "PROJ-R4J-yyy",
     link_type  = "depends on"
   )
   ```

#### 3c. Requirements -> Tests Links (if `agent-sync-xray.md` has already been executed)

For each requirement with associated test scenarios (`[TS-xxx]`):
1. Look up the corresponding Xray/Jira key in `xray-mapping.json`
2. Create an R4J `tested by` link:
   ```
   jira_link_issues(
     source_key = "PROJ-R4J-xxx",
     target_key = "PROJ-TEST-yyy",
     link_type  = "tested by"
   )
   ```

### Step 4: Produce the Mapping File

Update `r4j-mapping.json` with the complete structure:

```json
{
  "last_sync": "YYYY-MM-DDTHH:MM:SSZ",
  "project_key": "PROJ",
  "jira_instance": "https://mycompany.atlassian.net",
  "requirements": [
    {
      "ba_id": "EX-001",
      "jira_key": "PROJ-123",
      "summary": "The system must allow...",
      "status": "validated",
      "last_synced": "YYYY-MM-DDTHH:MM:SSZ",
      "links": {
        "implements": ["PROJ-456", "PROJ-457"],
        "tested_by": ["PROJ-789"],
        "depends_on": []
      }
    }
  ],
  "sync_log": [
    {
      "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
      "action": "created",
      "ba_id": "EX-001",
      "jira_key": "PROJ-123"
    }
  ]
}
```

### Step 5: Synchronization Report

Produce a Markdown report summarizing operations performed:

```markdown
## R4J Synchronization Report — YYYY-MM-DD

| Operation | Count |
|-----------|-------|
| Requirements created | X |
| Requirements updated | X |
| Requirements unchanged | X |
| Traceability links created | X |
| Errors | X |

### Operation Details
...

### Errors Encountered
...
```

---

## Error Management

| Situation | Behavior |
|-----------|---------|
| R4J issue already existing with same `BA-ID` label | Update instead of create |
| Jira key of referenced Epic not found in `jira-mapping.json` | Log a warning, do not block synchronization |
| Jira API error (rate limiting, timeout) | Retry with exponential backoff (3 attempts), then log error |
| `Requirement` issue type unavailable | Stop with explicit message: "R4J plugin is not installed or 'Requirement' issue type does not exist in the project" |
| `BA-ID` label found on multiple issues | Stop with explicit message: duplicate detected, human arbitration required |

---

## Recommended Scheduled Execution

| Moment | Recommended Action |
|--------|------------------|
| Right after **System 1 human gate** | Initial sync: creation of all validated requirements in R4J |
| After executing **`agent-sync-jira.md`** (Epics/Stories) | Sync of R4J `implements` links to Epics/Features |
| After executing **`agent-sync-xray.md`** (Tests) | Sync of R4J `tested by` links to Tests |
| At each **catalog update** `1.4-functional-requirements.md` | Incremental sync (update of modified issues only) |
