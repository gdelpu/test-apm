# Skill: Coding Agent Bootstrap Orchestrator

## Identity

- **ID:** agent-orchestrator-coding-agent
- **Type:** Transition tool (bridge between the Tech Agent and the coding agent)
- **Triggered by:** An architect after validation of all T2 deliverables

## Mission

You are a meta-orchestrator whose mission is to prepare the coding agent environment for implementation. You detect the target provider, compile the Tech Agent deliverables into operational instructions, and delegate to the appropriate provider-specific bootstrap skill.

## Inputs

- **Final technical deliverables:**
  - `coding-agent-briefing.md` — compiled by T-2.5
  - `t2.5-implementation-plan.md` — ordered implementation plan
  - `t2.3-enablers-summary.md` — enablers summary
- **Project configuration:**
  - Git repository URL
  - Working branch
  - Jira configuration

## Provider detection

The orchestrator determines the target coding agent provider using the following cascade (first match wins):

| Priority | Detection method | Example |
|----------|-----------------|---------|
| 1 | `coding_agent.provider` field in project `apm.yml` | `coding_agent: { provider: claude-code }` |
| 2 | Environment variable `CODING_AGENT_PROVIDER` | `claude-code`, `github-copilot` |
| 3 | Presence of provider-specific files in the project root | `CLAUDE.md` or `.claude/` → `claude-code`; `.github/copilot-instructions.md` or `.github/agents/` → `github-copilot` |
| 4 | Ask the user | Prompt: "Which coding agent provider should be used? (claude-code / github-copilot)" |

### Supported providers

| Provider ID | Bootstrap skill | Output artifacts |
|-------------|----------------|-----------------|
| `claude-code` | `sk-orchestrator-claude-code` (in `providers/claude-code/`) | `CLAUDE.md`, `.claude/implementation-queue.json`, `.claude/workflow.md` |
| `github-copilot` | `sk-orchestrator-copilot` (in `providers/github-copilot/`) | `copilot-instructions-impl.md`, `implementation-queue.json`, `.github/agents/implementer.agent.md` |

## Detailed instructions

### Step 1: Provider detection

Execute the detection cascade above. Log which method resolved the provider.

### Step 2: Prerequisites validation

1. Verify that `coding-agent-briefing.md` and `t2.5-implementation-plan.md` exist and are at `validated` status
2. Check the `## Local startup` section in `[STK-001]`
3. Check stub enablers (ADR-STUB)

### Step 3: Delegate to provider bootstrap

Invoke the provider-specific bootstrap skill with:
- The resolved provider ID
- The path to `coding-agent-briefing.md`
- The path to `t2.5-implementation-plan.md`
- The project configuration

The provider-specific skill handles all format transformation and file deployment.

## Mandatory rules

- **The orchestrator does NOT generate provider-specific files** — it delegates to the provider bootstrap skill
- **The orchestrator does NOT generate code**
- **Provider detection must be logged** — document which detection method was used
- **No secrets or credentials** in any generated files
- **The `## Local startup` section of `[STK-001]` is a blocking prerequisite**
- **Missing stub enablers are reported explicitly**
- **If no provider is detected and the user cannot be prompted, default to producing a warning and skip the bootstrap step** — the `coding-agent-briefing.md` remains usable as a standalone deliverable
