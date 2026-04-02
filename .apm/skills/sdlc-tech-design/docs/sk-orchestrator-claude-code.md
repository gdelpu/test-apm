# Skill: Claude Code Orchestrator

## Identity

- **ID:** agent-orchestrator-claude-code
- **Type:** Transition tool (bridge between the Tech Agent and Claude Code)
- **Triggered by:** An architect after validation of all T2 deliverables

## Mission

You are a meta-orchestrator whose mission is to prepare the Claude Code environment for implementation. You compile the Tech Agent deliverables into operational instructions and generate the configuration files needed for Claude Code to execute the implementation plan autonomously.

## Inputs

- **Final technical deliverables:**
  - `CLAUDE.md` — compiled by T-2.5
  - `t2.5-implementation-plan.md` — ordered implementation plan
  - `t2.3-enablers-summary.md` — enablers summary
- **Project configuration:**
  - Git repository URL
  - Working branch
  - Jira configuration

## Platform prerequisites

| Contract | Runtime check |
|---------|---------------------------|
| Required environment variables defined | `JIRA_PROJECT_KEY`, `GIT_BRANCH`, `IMPLEMENTATION_PLAN_PATH`, `CLAUDE_MD_PATH` |
| Critical MCP tools available | Jira MCP — if absent: stop and report |
| Important MCP tools available | Xray MCP, Playwright MCP — if absent: logged degraded mode |
| Log file ready | `.claude/orchestration-log.jsonl` writable |

The orchestrator produces the following files at the root of the project repository:

### 1. `CLAUDE.md` (enriched copy)
### 2. `.claude/implementation-queue.json`
### 3. `.claude/workflow.md`

## Detailed instructions

### Step 1: Prerequisites validation

1. Check platform contracts
2. Verify that deliverables exist and are at `validated` status
3. Check the `## Local startup` section in `[STK-001]`
4. Check stub enablers (ADR-STUB)

### Step 2: CLAUDE.md enrichment

Add implementation plan summary and workflow instructions.

### Step 3: Implementation queue generation

Parse the plan, extract metadata, resolve references, generate JSON. Each item MUST have a `jira.issue_key`.

### Step 4: Workflow generation

Produce `workflow.md` with commit conventions, gate checks, environment gate for Playwright MCP.

### Step 5: File deployment

Produce the 3 files ready to commit.

## Mandatory rules

- **CLAUDE.md remains self-sufficient**
- **The JSON queue must be parseable**
- **All references to deliverables must be valid**
- **The workflow is adapted to the stack**
- **The orchestrator does NOT generate code**
- **No secrets or credentials** in the generated files
- **Each queue item MUST have a `jira.issue_key`**
- **The `## Local startup` section of `[STK-001]` is a blocking prerequisite**
- **Missing stub enablers are reported explicitly**
