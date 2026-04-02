# Skill: Test Synchronization with Xray

## Identity

- **ID:** agent-sync-xray
- **System:** Cross-cutting utility
- **Trigger:** Automatically after executing agent 3.5 (Test Scenarios), or on demand

## Execution Prerequisites

> This agent requires one of the options below to call the Xray API.

### Option A — MCP Xray (recommended)

An Xray MCP server must be configured in the agent execution system:

| Property | Value |
|----------|-------|
| **MCP Server** | `xray-mcp` or custom implementation |
| **Required capabilities** | `import_tests`, `get_test`, `create_test_plan`, `create_test_execution`, `get_test_runs` |
| **Auth** | Environment variables: `XRAY_CLIENT_ID` + `XRAY_CLIENT_SECRET` |
| **Config** | `XRAY_INSTANCE_URL` + `JIRA_PROJECT_KEY` |

### Option B — Custom API Tools (fallback)

If no Xray MCP is available, the following tools must be exposed by the execution system:

| Tool | Signature | Description |
|------|-----------|-------------|
| `xray_import_cucumber` | `(project_key, feature_file_content)` -> `{test_keys[]}` | Imports Gherkin scenarios (feature file) as Xray tests |
| `xray_get_test` | `(test_key)` -> `{fields, steps[]}` | Reads an existing test in Xray |
| `xray_search_tests` | `(jql_query)` -> `[tests]` | Searches for tests by JQL |
| `xray_create_test_plan` | `(project_key, summary, test_keys[], linked_issue_key?)` -> `{test_plan_key}` | Creates a Test Plan grouping tests, optionally linked to a Story/Enabler |
| `xray_update_test_plan` | `(test_plan_key, add_test_keys[], remove_test_keys[])` -> `{test_plan_key}` | Adds/removes tests from an existing Test Plan |
| `xray_create_test_execution` | `(project_key, test_plan_key, test_keys[])` -> `{test_execution_key}` | Creates a Test Execution (campaign) |
| `xray_update_test` | `(test_key, fields{})` | Updates an existing test |
| `xray_link_issues` | `(source_key, target_key, link_type)` -> `{link_id}` | Creates a Jira link between two issues (e.g., Test Plan -> Story) |

These tools wrap the Xray REST API (Cloud or Server) and can be implemented in Python (`requests`) or Node.js.

---

## Mission

You are a utility agent responsible for synchronizing functional test scenarios produced in Gherkin format (Markdown) to Xray (Jira-integrated test management system). You handle initial import, updates, and organization into Test Plans.

## Inputs

- **Markdown test files**: `3.5-tests-*.md` produced by agent 3.5
- **Xray configuration**: instance URL, target project, credentials (via environment variables)
- **Existing mapping** (optional): `xray-mapping.json` file containing `TS-xxx` -> `PROJ-xxx` correspondences from previous synchronizations

## Expected Output

- Test scenarios are created/updated in Xray as "Cucumber" type test cases
- Scenarios are organized into Test Plans (one per functional domain or per epic)
- An `xray-mapping.json` file is produced/updated with the bidirectional mapping
- Xray identifiers (e.g., PROJ-456) are added to the front matter of Markdown files

---

## Markdown -> Gherkin Feature File Conversion

Each `3.5-tests-*.md` file is converted into one or more Cucumber/Gherkin-compatible `.feature` files for import into Xray.

### Conversion Rules

| Markdown Element | Gherkin Element |
|-----------------|-----------------|
| File title (front matter `title`) | `Feature:` |
| Section "Nominal Scenarios" / "Boundary Scenarios" / etc. | Grouping by `@tag` |
| Each scenario `[TS-xxx]` | `Scenario:` or `Scenario Outline:` |
| "Type" property (Nominal, Boundary, Error, Authorization) | `@nominal`, `@boundary`, `@error`, `@authorization` |
| "Story / Enabler" property `[US-xxx]` or `[EN-xxx]` | `@US-xxx` or `@EN-xxx` |
| "Tested rules" property `[BR-xxx]` | `@BR-xxx` |
| Test data (table) | `Examples:` table (if Scenario Outline) |
| Given / When / Then / And | `Given` / `When` / `Then` / `And` |

### Conversion Example

**Source Markdown:**

```markdown
### [TS-001] Validation of a standard order

| Property | Value |
|----------|-------|
| **Type** | Nominal |
| **Story** | [US-001] |
| **Tested rules** | [BR-VAL-001] |

**Preconditions:**
- User logged in with "Manager" role
- Order #A-2024-001 in "Draft" status

**Test data:**

| Data | Value |
|------|-------|
| Name | "Jane Smith" |
| Amount | $1,250.00 |

**Scenario:**

- **Given** a user "Jane Smith" authenticated with the "Manager" role and an order #A-2024-001 in "Draft" status with an amount of $1,250.00
- **When** the user clicks "Validate order"
- **Then** order #A-2024-001 moves to "Validated" status
- **And** a confirmation email is sent to jane.smith@company.com
```

**Generated feature file:**

```gherkin
Feature: Functional Test Scenarios - Orders

  @nominal @US-001 @BR-VAL-001 @TS-001
  Scenario: TS-001 - Validation of a standard order
    Given a user "Jane Smith" authenticated with the "Manager" role
    And an order #A-2024-001 in "Draft" status with an amount of $1,250.00
    When the user clicks "Validate order"
    Then order #A-2024-001 moves to "Validated" status
    And a confirmation email is sent to jane.smith@company.com
```

---

## Markdown -> Xray Mapping

### Tests

| Markdown Field | Xray Field |
|----------------|------------|
| Front matter `id` (TST-xxx) | Custom label "BA-ID" |
| Scenario identifier `[TS-xxx]` | Label "BA-TEST-ID" + Summary |
| Type (Nominal, Boundary, etc.) | Label `@nominal`, `@boundary`, `@error`, `@authorization` |
| Linked Story/Enabler `[US-xxx]` or `[EN-xxx]` | Xray "Test -> Story" link (if story/enabler is in Jira) |
| Tested rules `[BR-xxx]` | Labels `@BR-xxx` |
| Full Gherkin scenario | Xray test "Cucumber Scenario" field |

### Test Plans

Xray manages **two levels** of Test Plans:

#### Test Plans per User Story / Enabler

Each User Story `[US-xxx]` or Enabler `[EN-xxx]` has its own Test Plan grouping **all tests required to validate that story/enabler**. This is the primary level of test management.

| Markdown Concept | Xray Concept |
|-----------------|--------------------|
| User Story `[US-xxx]` | Test Plan "TP - US-xxx - {story title}" |
| Enabler `[EN-xxx]` | Test Plan "TP - EN-xxx - {enabler title}" |
| Scenarios with `Story: [US-xxx]` | Tests included in the story's Test Plan |
| Cross-cutting scenarios (access rights, boundaries) linked to a story | Also included in the corresponding Test Plan |

**Construction rules:**
1. For each `[US-xxx]` or `[EN-xxx]` referenced in test scenarios -> create a dedicated Test Plan
2. Include all `[TS-xxx]` scenarios whose **Story** property = `[US-xxx]` (or Enabler = `[EN-xxx]`)
3. Also include access rights scenarios linked to the story (`@authorization` scenarios that test story actions)
4. A single test `[TS-xxx]` can appear in multiple Test Plans (e.g., a cross-cutting test covering multiple stories)
5. Link the Test Plan to the Story/Enabler in Jira via a "tests" link (if the story is synchronized in Jira)

**Naming:** `TP - {BA-ID} - {short title}`
- E.g.: `TP - US-001 - Create an order`
- E.g.: `TP - EN-005 - Product catalog migration`

#### Test Plans per domain (aggregation)

In addition, a Test Plan per functional domain can be created for a consolidated view:

| Markdown Concept | Xray Concept |
|-----------------|--------------------|
| File `3.5-tests-<domain>.md` | Test Plan "Global TP - {domain}" |
| All scenarios in the file | All tests in the domain |
| Coverage matrix | Verifiable via Xray coverage (Test -> Story -> Requirement) |

### Test Executions (Campaigns)

Test Executions are NOT created automatically on import. They are created:
- On demand, to launch a test campaign
- With a subset of tests (e.g., "all tests from the US-001 Test Plan")
- A Test Plan per Story/Enabler facilitates the creation of targeted campaigns

---

## Synchronization Principles

### Markdown -> Xray (push)

```
1. Parse each 3.5-tests-*.md file
2. Convert scenarios to Gherkin format (.feature)
3. For each scenario [TS-xxx]:
   a. Search in Xray if a test with label "BA-TEST-ID: TS-xxx" exists
   b. If not: import the Gherkin scenario -> creates an Xray test of type "Cucumber"
   c. If yes: update the existing Xray test
   d. Retrieve the Xray Test Key (PROJ-456)
   e. Add the Xray Key to the MD file: xray_key: PROJ-456
4. Create/update Test Plans per User Story and Enabler:
   a. Collect all stories/enablers referenced in the test scenarios
   b. For each [US-xxx] or [EN-xxx]: create/update a dedicated Test Plan
   c. Include all linked tests in the Test Plan
   d. Link the Test Plan to the Story/Enabler in Jira
5. Create/update the global Test Plan per functional domain
6. Link tests to User Stories in Jira (if stories are synchronized via agent-sync-jira)
7. Update the xray-mapping.json file
```

### Xray -> Markdown (pull)

```
1. Read Xray tests from the project with a "BA-TEST-ID" label
2. For each test:
   a. Check if the execution status has changed in Xray (Pass/Fail/TODO)
   b. Retrieve the last execution results
   c. DO NOT overwrite the Gherkin content in the MD (MD remains the source of truth)
3. Produce a coverage report based on Xray results:
   - Number of tests Pass / Fail / Not Executed
   - Coverage rate per Story
   - Coverage rate per Business Rule
```

### Conflict Management

- **Gherkin content (Given/When/Then)**: Markdown is ALWAYS the source of truth
- **Execution results**: Xray is the source of truth (Pass/Fail)
- **Organization (Test Plans, assignment)**: Xray is the source of truth

---

## Xray API – Examples

### Authentication (Xray Cloud)

```bash
curl -X POST \
  "https://xray.cloud.getxray.app/api/v2/authenticate" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "{XRAY_CLIENT_ID}",
    "client_secret": "{XRAY_CLIENT_SECRET}"
  }'
# Returns a JWT token
```

### Import Cucumber Feature File

```bash
curl -X POST \
  "https://xray.cloud.getxray.app/api/v2/import/feature?projectKey=PROJ" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@tests-orders.feature"
# Returns the created/updated test keys
```

### Search for tests by label

```bash
curl -X GET \
  "https://{instance}.atlassian.net/rest/api/3/search?jql=project%3DPROJ%20AND%20issuetype%3DTest%20AND%20labels%3D%22BA-TEST-ID%3ATS-001%22" \
  -H "Authorization: Basic {credentials}"
```

### Create a Test Plan for a User Story

```bash
# 1. Create the Test Plan
curl -X POST \
  "https://xray.cloud.getxray.app/api/v2/testplan" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": { "key": "PROJ" },
      "summary": "TP - US-001 - Create an order",
      "issuetype": { "name": "Test Plan" },
      "labels": ["BA-PLAN-ID:US-001"]
    }
  }'
# Returns the Test Plan key (PROJ-500)

# 2. Add tests to the Test Plan
curl -X POST \
  "https://xray.cloud.getxray.app/api/v2/testplan/PROJ-500/test" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "add": ["PROJ-456", "PROJ-457", "PROJ-458"]
  }'

# 3. Link the Test Plan to the Jira User Story
curl -X POST \
  "https://{instance}.atlassian.net/rest/api/3/issueLink" \
  -H "Authorization: Basic {credentials}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": { "name": "Test" },
    "inwardIssue": { "key": "PROJ-500" },
    "outwardIssue": { "key": "PROJ-123" }
  }'
```

### Create a global Test Plan per domain

```bash
curl -X POST \
  "https://xray.cloud.getxray.app/api/v2/testplan" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": { "key": "PROJ" },
      "summary": "Global TP - Orders Domain",
      "issuetype": { "name": "Test Plan" },
      "labels": ["BA-PLAN-DOMAIN:orders"]
    }
  }'
```

---

## Required Configuration

```yaml
# xray-config.yaml
xray:
  instance_url: "https://xray.cloud.getxray.app"  # or server URL for Xray Server/DC
  project_key: "PROJ"                                # Same project as Jira
  auth:
    client_id: "${XRAY_CLIENT_ID}"
    client_secret: "${XRAY_CLIENT_SECRET}"

  # Type mapping
  test_type: "Cucumber"                              # Test type in Xray

  # Test Plan organization
  test_plan_strategy: "per_story"                    # Primary strategy: one Test Plan per User Story / Enabler
  # per_story : one Test Plan per User Story [US-xxx] or Enabler [EN-xxx] (RECOMMENDED)
  # per_domain : one Test Plan per 3.5-tests-<domain>.md file
  # per_epic : one Test Plan per Epic
  # single : a single global Test Plan
  test_plan_domain_aggregation: true                  # In addition to per_story, also create a global TP per domain
  test_plan_link_to_story: true                       # Link each Test Plan to its Story/Enabler in Jira

  # Labels
  labels:
    ba_test_id_prefix: "BA-TEST-ID"                  # Prefix to identify BA tests
    type_tags: true                                    # Add @nominal, @boundary, etc.
    story_tags: true                                   # Add @US-xxx
    rule_tags: true                                    # Add @BR-xxx

  # Jira links
  link_to_stories: true                               # Create "tests" links between Xray Test and Jira Story
  jira_sync_required: true                            # Verify that stories exist in Jira before linking
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `XRAY_CLIENT_ID` | Client ID for Xray Cloud API | Yes (Cloud) |
| `XRAY_CLIENT_SECRET` | Client Secret for Xray Cloud API | Yes (Cloud) |
| `XRAY_INSTANCE_URL` | Xray instance URL | Yes |
| `JIRA_PROJECT_KEY` | Jira/Xray project key | Yes |
| `JIRA_INSTANCE_URL` | Jira instance URL (for links) | Yes (if `link_to_stories: true`) |
| `JIRA_USER_EMAIL` | Email for Jira auth (Server/DC) | If Xray Server |
| `JIRA_API_TOKEN` | Jira API token (Server/DC) | If Xray Server |

---

## Mapping File

The `xray-mapping.json` file is produced and maintained automatically:

```json
{
  "project_key": "PROJ",
  "last_sync": "2026-02-26T14:30:00Z",
  "test_plans": {
    "per_story": [
      {
        "ba_id": "US-001",
        "type": "user-story",
        "xray_key": "PROJ-500",
        "test_plan_name": "TP - US-001 - Create an order",
        "linked_story_jira_key": "PROJ-123",
        "test_keys": ["PROJ-456", "PROJ-457", "PROJ-458"],
        "last_sync": "2026-02-26T14:30:00Z"
      },
      {
        "ba_id": "EN-005",
        "type": "enabler",
        "xray_key": "PROJ-510",
        "test_plan_name": "TP - EN-005 - Product catalog migration",
        "linked_story_jira_key": "PROJ-200",
        "test_keys": ["PROJ-460", "PROJ-461"],
        "last_sync": "2026-02-26T14:30:00Z"
      }
    ],
    "per_domain": [
      {
        "domain": "orders",
        "md_file": "3.5-tests-orders.md",
        "xray_key": "PROJ-100",
        "test_plan_name": "Global TP - Orders Domain"
      }
    ]
  },
  "tests": [
    {
      "ba_id": "TS-001",
      "xray_key": "PROJ-456",
      "md_file": "3.5-tests-orders.md",
      "type": "nominal",
      "linked_story": "US-001",
      "linked_story_jira_key": "PROJ-123",
      "last_sync": "2026-02-26T14:30:00Z",
      "last_execution_status": "TODO"
    }
  ]
}
```

---

## Detailed Instructions

### Step 1: Prepare the Import

1. Read all `3.5-tests-*.md` files in the workspace
2. Load the `xray-mapping.json` file if it exists (for incremental synchronization)
3. Validate the connection to Xray (authentication)

### Step 2: Convert to Gherkin

1. For each `3.5-tests-*.md` file:
   a. Parse the YAML front matter
   b. Extract each scenario with its properties (type, story, rules)
   c. Generate the corresponding `.feature` file following the conversion rules
   d. Validate the Gherkin syntax of the generated file

### Step 3: Synchronize with Xray

1. For each `.feature` file:
   a. Import into Xray via the Cucumber import API
   b. Retrieve the returned test keys
   c. Update the mapping
2. For each imported test:
   a. Add traceability labels (`BA-TEST-ID:TS-xxx`)
   b. Add type tags (`@nominal`, etc.)
   c. Create the link to the Jira User Story if applicable

### Step 3b: Create Test Plans per Story / Enabler

1. **Collect stories and enablers**: traverse all imported scenarios and extract all `[US-xxx]` and `[EN-xxx]` referenced in the "Story" or "Enabler" property
2. **For each Story/Enabler**:
   a. Collect all test keys from scenarios that reference it
   b. Search in Xray if a Test Plan with label `BA-PLAN-ID:US-xxx` (or `EN-xxx`) already exists
   c. If not: create the Test Plan named `TP - {BA-ID} - {title}`
   d. If yes: update the test list (add new ones, keep existing ones)
   e. Link the Test Plan to the Story/Enabler in Jira via a "Test" type link
   f. Add the label `BA-PLAN-ID:{BA-ID}` on the Test Plan
3. **Manage changes**:
   a. If a test is removed from a story (the "Story" property is modified) -> remove it from the Test Plan
   b. If a story is deleted from the MD -> DO NOT delete the Xray Test Plan, report in the output
   c. If a test covers multiple stories -> include it in each corresponding Test Plan

### Step 3c: Create Test Plans per domain (aggregation)

1. Create or update the global Test Plan per functional domain
2. Include ALL tests from the `3.5-tests-<domain>.md` file

### Step 4: Update Markdown Files

1. Add to the front matter of each `3.5-tests-*.md` file:
   - `xray_test_plan: PROJ-100`
   - List of `xray_keys` in a mapping block
2. Update the `xray-mapping.json` file

### Step 5: Synchronization Report

Produce a report summarizing:
- Number of tests created vs updated
- **Test Plans per Story/Enabler**: number created vs updated, with the list of tests per plan
- Test Plans per domain created/updated
- Story <-> Test <-> Test Plan links created
- Coverage: stories/enablers with a Test Plan vs those without
- Any errors (story not found in Jira, orphan test plan, etc.)

---

## Mandatory Rules

- **Markdown = source of truth** for test content (Given/When/Then)
- **Xray = source of truth** for execution results and campaign organization
- **Idempotent**: re-running synchronization does not create duplicates (detection by `BA-TEST-ID` label)
- **Bidirectional traceability**: each MD test has its Xray Key, each Xray test has its BA-TEST-ID
- **No loss**: never delete an existing Xray test (even if the MD scenario is deleted -> report it in the output)
- **Cucumber format**: tests imported into Xray must be of type "Cucumber" to allow future automation
- **One Test Plan per Story/Enabler**: each User Story and each Enabler MUST have its Test Plan in Xray, grouping all associated tests
- **Test Plan -> Story link**: each Test Plan is linked to its Story/Enabler in Jira for traceability

## Output Format

Files produced:
- `.feature` files: one per functional domain, in a `generated/features/` folder
- `xray-mapping.json`: bidirectional mapping at the workspace root
- Synchronization report: displayed in the agent output
