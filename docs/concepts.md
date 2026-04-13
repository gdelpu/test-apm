# Concepts & Glossary

> Overview of the building blocks used in the AI SDLC Foundation.

The AI SDLC Foundation is built from a set of composable concepts. This page explains each one, where to find it, and how it fits into the system.

---

## Summary

| Concept | Canonical Path | Count | Role |
|---------|---------------|-------|------|
| [Agents](#agents) | `.apm/agents/` | 23 | Autonomous roles that execute tasks |
| [Workflows](#workflows) | `.apm/workflows/` | 19 | Multi-station pipelines with quality gates |
| [Skills](#skills) | `.apm/skills/` | 89 | Reusable knowledge packages consumed by agents |
| [Knowledge](#knowledge) | `.apm/knowledge/` | 4 areas | Constitution, governance, playbooks, brand |
| [Prompts](#prompts) | `.apm/prompts/` | 4 | Slash-command templates that trigger workflows |
| [Instructions](#instructions) | `.apm/instructions/` | 7 | Behavioral rules auto-applied to matching files |
| [Hooks](#hooks) | `.apm/hooks/` | 8 | Pre/post lifecycle hooks around stations |
| [Templates](#templates) | `.apm/templates/` | 6 | Document templates for workflow outputs |
| [Contexts](#contexts) | `.apm/contexts/` | 10 | Reference catalogs auto-loaded by agents |
| [MCP Servers](#mcp-servers) | `.apm/contexts/mcp-registry.yaml` | 14 | Optional external-tool connectors for live data and services |
| [Scripts](#scripts) | `scripts/`, `.apm/scripts/` | — | Automation for build, projection, validation |

---

## Agents

**What**: An agent is an autonomous role definition — a persona with a specific purpose, paired with one or more skills that give it domain knowledge and tools. Agents are provider-agnostic: the same definition works in Copilot, Claude Code, and CLI.

**Where**: `.apm/agents/<name>.md`

**How they're used**: In Copilot, agents are invoked as `@agent-name` in the chat panel. In Claude Code, they run behind `/command` invocations. In CLI, they execute within workflow stations.

**Examples**:
- `hub-orchestrator` — Central triage agent that classifies your intent and routes you to the right workflow
- `implementer` — Reads task breakdowns and produces code following project constraints
- `quality-validator` — Runs lint, static analysis, SAST, dependency audit, and coverage checks
- `security-reviewer` — Audits code for prompt injection, data exfiltration, and OWASP LLM Top 10 risks

---

## Workflows

**What**: A workflow is a YAML-defined pipeline of sequential **stations**. Each station is assigned to an agent with specific skills, produces defined outputs, and has a **quality gate** with pass/fail criteria. Workflows support resume (pick up where you left off), skip-gate (where configured), and nesting (one workflow can invoke another).

**Where**: `.apm/workflows/<name>.yml`

**How they're used**: Invoked via `/workflow-<name>` (Copilot/Claude) or `./providers/cli/run-workflow.sh <name> <feature>` (CLI). The Hub Orchestrator can also recommend and dispatch workflows based on your intent.

**Examples**:
- `feature-implementation` — 10 stations from constitution through implementation to quality gate
- `spec-kit` — 8 stations for specification-only flows (no implementation)
- `bug-fixing` — 7 stations from triage through root-cause, fix, and regression testing
- `quality-validation` — 7 stations for lint, static analysis, SAST, dependency audit, coverage, DAST, and reporting

**Key concept: Stations and gates**

A workflow is a sequence of stations. Each station:
1. Is executed by a specific **agent** using specific **skills**
2. Produces defined **output artifacts** (e.g., `spec.md`, `plan.md`, `tasks.md`)
3. Has a **quality gate** that must pass before the next station runs

If a gate fails, the workflow pauses and reports what needs to be fixed.

---

## Skills

**What**: A skill is a reusable knowledge and tool package. It contains domain-specific instructions, patterns, and optionally tool definitions that an agent uses to perform its work. Skills are the "how-to" knowledge that agents consume.

**Where**: `.apm/skills/<name>/SKILL.md` (manifest) + optional `tools/` and `docs/` subdirectories

**How they're used**: Skills are referenced by agents in their definitions. When an agent runs, it loads the skills assigned to it for that station. You don't invoke skills directly — agents use them.

**Examples**:
- `spec-feature` — Generates feature specifications with scope, acceptance criteria, and user stories
- `code-implementation` — Guides code production following project constraints and standards
- `security-scan` — SAST/DAST scanning patterns and tool integration
- `hub-classification` — Classifies user intent against available workflows and agents

---

## Knowledge

**What**: The knowledge base contains foundational documents that define principles, governance rules, playbooks, and brand guidelines. These are reference materials that agents and skills consult — they establish the "what" and "why" behind decisions.

**Where**: `.apm/knowledge/`

**Areas**:
- `.apm/knowledge/constitution/` — Engineering constitutions (architecture, quality, security, testing, observability principles)
- `.apm/knowledge/governance/` — Architecture principles, testing policy, secure-by-default rules, observability requirements
- `.apm/knowledge/playbooks/` — Step-by-step playbooks for greenfield, brownfield, modernization, and workflow execution
- `.apm/knowledge/brand/` — Brand guidelines, asset inventories, templates (e.g., Sopra Steria brand)

**Examples**:
- `speckit-constitution.md` — The master constitution template covering architecture decisions, quality standards, and testing requirements
- `architecture-principles.md` — Governance rules that the Architecture Governance agent validates against
- `brownfield-playbook.md` — Step-by-step guide for approaching existing codebases

---

## Prompts

**What**: A prompt is a reusable slash-command template. When invoked, it sets up the context and instructions for a specific task or workflow invocation. Prompts are the user-facing entry points in Copilot (`/prompt-name`) and Claude Code (`/command-name`).

**Where**: `.apm/prompts/` (canonical), projected to `.github/prompts/` (Copilot runtime) and `providers/claude-code/commands/` (Claude Code)

**How they're used**: Type `/prompt-name` in the chat to invoke. The prompt loads the relevant agent, skills, and context automatically.

**Examples**:
- `/workflow-feature` — Launches the feature-implementation workflow
- `/workflow-spec-kit` — Launches the specification-only workflow
- `/hub-orchestrator` — Starts the Hub Orchestrator for intent classification

---

## Instructions

**What**: An instruction is a set of behavioral rules that are automatically applied to files matching a glob pattern. They modify how the AI behaves when working with specific files or directories — enforcing coding standards, naming conventions, or architectural constraints.

**Where**: `.apm/instructions/<name>.instructions.md` (canonical), projected to `.github/instructions/` (Copilot runtime)

**Key property**: Each instruction has an `applyTo` field (a glob pattern) that controls which files it activates for. When you open or edit a matching file, the instruction's rules are automatically loaded.

**Examples**:
- `apm-layer.instructions.md` (`applyTo: ".apm/**"`) — Rules for working inside the canonical APM packaging layer
- `workflow.instructions.md` (`applyTo: ".apm/workflows/**"`) — Rules for defining station-based workflow pipelines
- `knowledge-base.instructions.md` (`applyTo: ".apm/knowledge/**"`) — Rules for working inside the foundational knowledge base

---

## Hooks

**What**: Hooks are pre/post execution scripts that run around workflow stations or complete workflows. They handle setup, teardown, environment checks, or side effects (e.g., notifications, artifact signing) outside the agent's main task.

**Where**: `.apm/hooks/` — organized into `pre/`, `post/`, and `config/` subdirectories. Schema defined in `_schema.md`.

**How they're used**: Hooks are configured in workflow YAML definitions. When a station runs, its pre-hooks execute first, then the agent, then the post-hooks. Hooks are optional — most workflows work without them.

---

## Templates

**What**: Templates are document scaffolds used by workflow stations to produce consistently structured output artifacts. When an agent creates a specification, plan, or task breakdown, it uses the corresponding template as the starting structure.

**Where**: `.apm/templates/`

**Examples**:
- `spec-template.md` — Structure for feature specifications (scope, acceptance criteria, user stories)
- `plan-template.md` — Structure for implementation plans (phases, risks, rollback strategy)
- `tasks-template.md` — Structure for task breakdowns (ordered tasks with dependencies and verification)
- `checklist-template.md` — Quality gate checklist format
- `template-corporate.docx` — Word template for branded document generation

---

## Contexts

**What**: Contexts are reference documents and metadata catalogs that agents automatically load for situational awareness. They provide registries of available assets, system context, and orchestration guides so agents know what's available and how things connect.

**Where**: `.apm/contexts/`

**Examples**:
- `hub-catalog.yaml` — Auto-generated registry of all workflows and agents (read by Hub Orchestrator to classify intents)
- `sdlc-agent-registry.yaml` — Agent manifest with capabilities and skill mappings
- `sdlc-pipelines.yaml` — Workflow definitions with station sequences and dependencies
- `repository-context.md` — System-level documentation about the repository structure

---

## MCP Servers

**What**: MCP (Model Context Protocol) is an open standard that lets AI agents talk to external tools and services — think of it as a universal adapter. Instead of being limited to what the agent knows on its own, MCP lets it reach out to live systems: query a cloud dashboard, check a CI pipeline, browse documentation, or interact with a project management board.

**Where**: `.apm/contexts/mcp-registry.yaml` (server catalog), `.apm/skills/mcp-configuration/` (setup skill), `.apm/skills/mcp-fallback/` (graceful degradation)

**Key point — all MCP servers are optional**: Every workflow and agent works without any MCP server configured. MCP servers add enrichments (live data, platform integrations, browser automation) but are never required. If an MCP server is unavailable, agents automatically fall back to built-in capabilities.

**How they're used**: The Hub Orchestrator can auto-detect your environment and recommend which servers to enable. Alternatively, teams configure servers manually via `.vscode/mcp.json`. Once configured, agents transparently use MCP servers when they need external data — no extra steps for the user.

**Available server categories**:
- **Cloud platforms** — Azure, AWS: query resources, check deployments, inspect configurations
- **DevOps platforms** — GitHub, GitLab, Azure DevOps: manage work items, pull requests, pipelines
- **Collaboration** — Atlassian (Jira/Confluence), Microsoft 365: access project boards, documents, wikis
- **Quality & security** — SemGrep, SonarQube: run code analysis, retrieve findings
- **Documentation** — Context7, MsLearn: look up current library docs and technical references
- **Browser automation** — Playwright: interact with web UIs for testing or data gathering
- **Design** — Figma: access design assets and specifications

**Examples**:
- An agent checking deployment health can query Azure resources via the Azure MCP server
- A business analyst agent can pull the latest Jira tickets via the Atlassian MCP server
- A quality agent can fetch SonarQube findings without leaving the workflow

> **Further reading**: [MCP Setup Guide](consumer/mcp-setup-guide.md) (consumer) · [MCP Integration Guide](contributor/mcp-integration-guide.md) (contributor)

---

## Scripts

**What**: Scripts automate building, projection, validation, and distribution of the AI SDLC Foundation. They are the operational tooling that keeps the system consistent and deployable.

**Where**: `scripts/` (cross-layer tools) and `.apm/scripts/` (canonical automation)

**Key scripts**:
- `project-copilot.ps1` / `project-copilot.sh` — Generates the Copilot runtime (`.github/`) from provider adapters and local overlays
- `bootstrap-apm.ps1` / `bootstrap-apm.sh` — One-command installer for consumers
- `validate_all.py` — Runs all cross-layer validators to verify canonical ↔ projection consistency
- `apm-build.sh` / `apm-publish.sh` — Build and publish APM bundles to the package registry

---

## How They Fit Together

```
User intent
    │
    ▼
┌─────────────────┐
│  Hub Orchestrator │ ← reads Contexts (hub-catalog.yaml)
│     (Agent)       │
└────────┬─────────┘
         │ dispatches to
         ▼
┌─────────────────┐
│   Workflow       │ ← defined in .apm/workflows/
│  (station pipeline) │
└────────┬─────────┘
         │ each station runs
         ▼
┌─────────────────┐
│     Agent        │ ← loads Skills for domain knowledge
│  (at station)    │   ← reads Knowledge for principles
│                  │   ← uses Templates for output structure
│                  │   ← Hooks run pre/post
│                  │   ← MCP Servers provide live external data (optional)
└────────┬─────────┘
         │ passes quality gate
         ▼
      Next station → ... → Final output in specs/
```

**Prompts** are the user-facing entry points (`/workflow-feature`).
**Instructions** shape agent behavior for specific file types.
**MCP Servers** optionally connect agents to external tools and live data.
**Scripts** build and project everything into the provider runtime.

---

## Further Reading

- [Quick Start Guide](quick-start.md) — Install and start using the foundation
- [APM Consumer Guide](apm-consumer-guide.md) — Extended reference for installation modes, customization, and CI integration
- [README](../README.md) — Full catalog of all agents, skills, and workflows
