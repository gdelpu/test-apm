# Quick Start Guide

> Hands-on guide to install the AI SDLC Foundation and start using it immediately.

---

## Table of Contents

- [Install in 60 Seconds](#install-in-60-seconds)
- [Updating](#updating)
- [Three Ways to Use It](#three-ways-to-use-it)
- [Using the Hub Orchestrator](#using-the-hub-orchestrator)
- [Common Workflows](#common-workflows)
- [Using Agents Directly](#using-agents-directly)
- [Spotlight: Branding Agent](#spotlight-branding-agent)
- [Provider-Specific Usage](#provider-specific-usage)
  - [GitHub Copilot (VS Code)](#github-copilot-vs-code)
  - [CLI](#cli)
  - [Claude Code](#claude-code)
- [Learn More](#learn-more)

---

## Install in 60 Seconds

You need one thing: a **GitLab Personal Access Token** (scopes: `read_api` + `read_registry`).
Create one at: GitLab → avatar → **Edit profile** → **Personal Access Tokens** → **Add new token**.

### PowerShell (Windows)

```powershell
# 1. Set your token
$env:GITLAB_TOKEN = "glpat-xxxxxxxxxxxxxxxxxxxx"

# 2. Download & run the bootstrap (this is the only file you need)
Invoke-WebRequest `
  -Uri "https://innersource.soprasteria.com/api/v4/projects/545119/repository/files/scripts%2Fbootstrap-apm.ps1/raw?ref=main" `
  -Headers @{ 'PRIVATE-TOKEN' = $env:GITLAB_TOKEN } -OutFile bootstrap-apm.ps1

.\bootstrap-apm.ps1

# 3. Commit (optional)
git add .github/ .apm.lock.yaml
git commit -m "feat: install AI SDLC Foundation"
```

### Bash (Linux / macOS)

```bash
# 1. Set your token
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"

# 2. Download & run the bootstrap (this is the only file you need)
curl --fail --silent \
  --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  -o bootstrap-apm.sh \
  "https://innersource.soprasteria.com/api/v4/projects/545119/repository/files/scripts%2Fbootstrap-apm.sh/raw?ref=main"
chmod +x bootstrap-apm.sh

./bootstrap-apm.sh

# 3. Commit (optional)
git add .github/ .apm.lock.yaml
git commit -m "feat: install AI SDLC Foundation"
```

**That's it.** Copilot auto-discovers everything in `.github/`. Open the chat panel and try `@hub-orchestrator`.

---

## Updating

Re-run the bootstrap script. It detects the existing install and replaces it.

**PowerShell:**
```powershell
$env:GITLAB_TOKEN = "glpat-xxxx"
.\bootstrap-apm.ps1 -Version 0.0.2
```

**Bash:**
```bash
export GITLAB_TOKEN="glpat-xxxx"
./bootstrap-apm.sh --version 0.0.2
```

Commit `.github/` and `.apm.lock.yaml` when ready.

> Lost the bootstrap script? Re-download it using the same `Invoke-WebRequest` / `curl` command from the install step.
>
> Need expandable mode, CI integration, or customization? See the [APM Consumer Guide](apm-consumer-guide.md).

---

## Three Ways to Use It

The AI SDLC Foundation gives you three entry points — pick the one that matches your situation.

### 1. Ask the Hub Orchestrator (recommended start)

Don't know which workflow to use? Just describe what you need. The Hub Orchestrator classifies your intent and dispatches the right workflow automatically.

```
@hub-orchestrator I need to add a payment processing feature
```

Best when: you're new, unsure which workflow fits, or want guided discovery.

### 2. Run a workflow directly

Already know which workflow you need? Skip the Hub and invoke it as a slash command or CLI call. Workflows are multi-station pipelines — each station runs an agent with specific skills and a quality gate.

```
/workflow-feature                    ← Copilot slash command
/workflow-spec-kit                   ← specification only
./providers/cli/run-workflow.sh feature-implementation user-auth   ← CLI
```

Best when: you know the workflow name and want to start immediately.

### 3. Use a specific agent or skill

For focused tasks that don't need a full pipeline, invoke an agent directly. Each agent bundles one or more skills — reusable knowledge packages with tools, templates, and domain expertise.

```
@branding audit this application for brand compliance
@spec-orchestrator write a specification for user authentication
@security-reviewer review this agent definition for vulnerabilities
@repository-analyzer give me an overview of this codebase
```

Best when: you need a single capability (brand audit, security review, codebase analysis) without a multi-station workflow.

> **Skills** are the knowledge units that power agents. You don't invoke skills directly — you invoke the agent that bundles them. See the [Skills catalog](../reference/skills.md) for the full list of 94 skills across 11 categories.

---

## Using the Hub Orchestrator

The **Hub Orchestrator** is the single entry point. Tell it what you need — it classifies your intent and recommends the right workflow.

### How it works

1. You describe what you want to do (e.g., _"I need to build a user authentication feature"_)
2. Hub Orchestrator matches your intent to an available workflow
3. It presents the recommended workflow with station count and purpose
4. You confirm → it dispatches execution

### Invocation

| Provider | How to invoke |
|----------|---------------|
| **GitHub Copilot** | Type `@hub-orchestrator` in the Copilot Chat panel |
| **Claude Code** | Type `/hub-orchestrator` in the Claude Code chat |
| **CLI** | Browse the catalog: `cat .apm/contexts/hub-catalog.yaml`, then run the workflow directly |

### Example intents

| What you say | Workflow it recommends |
|-------------|----------------------|
| _"Build a new feature"_ | `feature-implementation` (10 stations) |
| _"Fix a bug"_ | `bug-fixing` (7 stations) |
| _"Modernize this codebase"_ | `modernization` (10 stations) |
| _"Write a specification"_ | `spec-kit` (8 stations) |
| _"Run quality checks"_ | `quality-validation` (7 stations) |
| _"Assess project maturity"_ | `maturity-assessment` (4 stations) |

---

## Common Workflows

Workflows are multi-station pipelines with quality gates at each step. Here are the most common ones and how to invoke them across providers:

| Workflow | Copilot | Claude Code | CLI |
|----------|---------|-------------|-----|
| **Feature Implementation** | `/workflow-feature` | `/workflow-feature` | `./providers/cli/run-workflow.sh feature-implementation my-feature` |
| **Specification Only** | `/workflow-spec-kit` | `/workflow-spec-kit` | `./providers/cli/run-workflow.sh spec-kit my-feature` |
| **Bug Fixing** | `/workflow-bug-fixing` | `/workflow-bug-fixing` | `./providers/cli/run-workflow.sh bug-fixing bug-123` |
| **Quality Validation** | `/workflow-quality` | `/workflow-quality` | `./providers/cli/run-workflow.sh quality-validation my-feature` |
| **Modernization** | `/workflow-modernization` | `/workflow-modernization` | `./providers/cli/run-workflow.sh modernization my-feature` |
| **PR Validation** | `/workflow-pr-validation` | `/workflow-pr-validation` | `./providers/cli/run-workflow.sh pr-validation my-feature` |

All workflow outputs are written to `outputs/specs/features/<feature-name>/`.

> **Full list**: See the [Workflows catalog](../reference/workflows.md) for all 19 workflows.

---

## Using Agents Directly

Sometimes you want a specific agent rather than a full workflow. Agents are autonomous roles that handle focused tasks.

| Agent | Purpose | Copilot | Claude Code |
|-------|---------|---------|-------------|
| **Hub Orchestrator** | Routes you to the right workflow | `@hub-orchestrator` | `/hub-orchestrator` |
| **Spec Orchestrator** | Drives specification flows (constitution, spec, plan, tasks) | `@spec-orchestrator` | `/sdlc-ba-2-spec` |
| **Implementer** | Writes code from task breakdowns | `@implementer` | _(used within workflows)_ |
| **Quality Validator** | Runs lint, SAST, coverage, dependency audit | `@quality-validator` | `/workflow-quality` |
| **Security Reviewer** | Audits for prompt injection, data exfiltration, OWASP LLM Top 10 | `@security-reviewer` | _(used within workflows)_ |
| **Repository Analyzer** | Produces architectural overview of a codebase | `@repository-analyzer` | _(used within workflows)_ |
| **Bug Fixer** | Structured bug diagnosis from triage to regression testing | `@bug-fixer` | `/workflow-bug-fixing` |
| **Branding Agent** | Audits and generates brand-compliant documents, apps, presentations | `@branding` | _(used within workflows)_ |

> **CLI note**: The CLI provider runs workflows, not individual agents. Use `run-workflow.sh` with a workflow that invokes the agent you need.

---

## Spotlight: Branding Agent

The **`branding`** agent is designed for **standalone use in any project** — no workflow required. Point it at an application, document, or presentation and it will:

- **Audit** brand compliance (colours, typography, logo usage, WCAG 2.1 AA contrast)
- **Refactor** styling to match brand guidelines (CSS, design tokens, Tailwind themes)
- **Generate** branded documents — convert Markdown to Word, PowerPoint, or PDF with correct templates
- **Manipulate** Office files — create/edit DOCX (tracked changes, comments), build PPTX decks, merge/split PDFs, fill PDF forms

**Default brand: Sopra Steria.** Out of the box, it loads the official visual identity from `knowledge/brand/soprasteria/`. Add a `knowledge/brand/<client>/` directory with client-specific assets to adapt automatically.

### Try it now

```
@branding audit this application for brand compliance
@branding convert docs/spec.md to a branded Word document
@branding create a PowerPoint deck from this markdown
@branding check the colour contrast of this component
```

### What powers it

10 skills: `brand-core`, `brand-assets`, `brand-app`, `brand-document`, `brand-accessibility`, `brand-audit`, `docx`, `pptx`, `pdf`, `office-common`.

> See the [full agent catalog](../reference/agents.md#spotlight-branding-agent) for technical details.

---

## Provider-Specific Usage

The AI SDLC Foundation supports three providers. You choose which one to use — or use multiple.

### GitHub Copilot (VS Code)

This is the primary provider. After installation, agents and prompts are auto-discovered from `.github/`.

**Agents** — invoke with `@agent-name` in the Copilot Chat panel:
```
@hub-orchestrator I need to add a payment processing feature
```

**Workflows** — invoke with `/prompt-name` as slash commands:
```
/workflow-feature
```

**How it works**: The bootstrap installs agent files into `.github/agents/` and prompt files into `.github/prompts/`. Copilot reads these automatically — no configuration needed.

### CLI

The CLI provider runs workflows from the terminal using a shell script. It does not provide interactive agent chat — it executes workflow stations sequentially.

**Entry point**:
```bash
./providers/cli/run-workflow.sh <workflow> <feature-name> [options]
```

**Flags**:

| Flag | Effect |
|------|--------|
| `--station <id>` | Run a single station only |
| `--resume` | Continue from last successful station |
| `--dry-run` | List stations without executing |
| `--verbose` | Detailed logging |
| `--skip-gate <id>` | Force past a blocker gate (exceptional use) |

**Examples**:

```bash
# Full feature workflow
./providers/cli/run-workflow.sh feature-implementation user-auth

# Run only the specification station
./providers/cli/run-workflow.sh feature-implementation user-auth --station spec

# Resume after interruption
./providers/cli/run-workflow.sh feature-implementation user-auth --resume

# Preview what will run
./providers/cli/run-workflow.sh feature-implementation user-auth --dry-run
```

**Discover available workflows**:
```bash
cat .apm/contexts/hub-catalog.yaml
```

### Claude Code

Claude Code uses `CLAUDE.md` as its context file and provides slash commands for workflows.

**Workflows** — invoke with `/command-name` in Claude Code chat:
```
/hub-orchestrator
/workflow-feature
/workflow-spec-kit
```

**SDLC pipelines** — full and sub-pipeline commands:
```
/sdlc-full              # Complete 11-station SDLC
/sdlc-ba                # Business analysis (16 stations)
/sdlc-tech              # Technical architecture (12 stations)
/sdlc-steer             # Steering & governance (10 stations)
```

**SDLC sub-pipelines** — run individual stages:
```
/sdlc-ba-0-audit        # Brownfield audit
/sdlc-ba-1-scoping      # Vision, glossary, actors, requirements
/sdlc-ba-2-spec          # Domain model, epics, features, rules
/sdlc-ba-3-design       # Per-feature functional design
/sdlc-tech-0-audit      # Technical stack audit
/sdlc-tech-1-archi      # Architecture (C4, ADRs, stack)
/sdlc-tech-2-design     # Data model, APIs, test strategy
/sdlc-tech-3-quality    # Drift detection, E2E generation
```

**How it works**: Commands are defined in `providers/claude-code/commands/`. The `CLAUDE.md` file at `providers/claude-code/CLAUDE.md` provides system context that Claude Code reads automatically.

---

## Learn More

| Resource | What it covers |
|----------|---------------|
| [Concepts & Glossary](../concepts.md) | What are agents, workflows, skills, prompts, instructions, hooks, and other building blocks |
| [APM Consumer Guide](apm-consumer-guide.md) | Extended reference: install modes, customization, `providers-local/` overlay, CI integration, troubleshooting |
| [Distribution Guide](../contributor/distribution.md) | Registry details, checksums, CI/CD pipeline examples |
| [Reference Catalogs](../reference/agents.md) | Full agent/skill/workflow catalog with descriptions |
