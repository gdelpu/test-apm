# SSG AI SDLC Foundation — Context

This repository is the Sopra Steria Group AI SDLC Foundation: a cross-provider
collection of agents, skills, workflows, prompts, and foundational knowledge
supporting the full software development lifecycle.

## Architecture (three layers)

```
┌─────────────────────────────────────────────────────────────┐
│                    CANONICAL LAYER                           │
│  .apm/agents/  .apm/skills/  .apm/workflows/  .apm/knowledge/│
│  (6 agents)    (26 skills)   (8 workflows)    (principles,  │
│                                                governance,   │
│                                                playbooks)    │
└──────────────┬──────────────────────┬───────────────────────┘
               │                      │
  ┌────────────▼──────────────────────▼──────────────────┐
  │                  PROVIDER ADAPTERS                    │
  │                                                      │
  │  providers/github-copilot/   providers/claude-code/  │
  │    conventions.md              CLAUDE.md             │
  │    sync-map.md                 commands/ (7)         │
  │    → .github/ (runtime)                              │
  │      agents/ (6)             providers/cli/          │
  │      prompts/ (12)             lib/ (5)              │
  │      instructions/ (5)         run-workflow.sh       │
  │                                                      │
  └──────────────────────┬───────────────────────────────┘
                         │
            ┌────────────▼──────────────┐
            │      Outputs: specs/      │
            │  features/  decisions/    │
            └───────────────────────────┘
```

## Key Paths

| Path | Purpose |
|------|---------|
| `.apm/agents/` | Canonical agent definitions (provider-agnostic) |
| `.apm/skills/` | Skill packages with SKILL.md + tools |
| `.apm/prompts/` | Reusable prompt templates |
| `.apm/workflows/` | YAML workflow definitions with stations and gates |
| `.apm/instructions/` | Shared behavioral instructions |
| `.apm/knowledge/` | Constitution, governance, playbooks, brand guidelines |
| `providers/github-copilot/` | Copilot adapter docs (conventions.md, sync-map.md) |
| `.github/` | Copilot runtime projection (agents, prompts, instructions) |
| `providers/claude-code/` | Claude Code adapter (CLAUDE.md, commands) |
| `providers/cli/` | CLI workflow runner (run-workflow.sh, lib/) |
| `ci-gates/` | PR validation station implementations (A0–A7) |
| `.apm/templates/` | Spec-kit workflow templates |
| `.apm/scripts/` | Workflow automation scripts |
| `clients/` | Per-client overlay customizations |

## Available Workflows

| Workflow | Type | Purpose |
|----------|------|---------|
| pr-validation | validation | A0–A7 merge request validation pipeline |
| feature-implementation | delivery | End-to-end feature delivery |
| quality-validation | validation | Code quality, security, compliance checks |
| modernization | modernization | Baseline → target → migration |
| spec-kit | delivery | Specification-only flow |
| bmad | delivery | Build → Measure → Analyze → Decide |
| bug-fixing | delivery | Bug triage through resolution |
| maturity-assessment | assessment | SDLC maturity evaluation |

## Schema Integration

The `.apm/knowledge/governance/schemas/` directory contains JSON schemas that validate
canonical asset manifests:

| Schema | Path | Validates |
|--------|------|----------|
| Agent Manifest | `.apm/knowledge/governance/schemas/agent-manifest.schema.json` | `.apm/agents/*.md` frontmatter |
| Skill Manifest | `.apm/knowledge/governance/schemas/skill-manifest.schema.json` | `.apm/skills/*/SKILL.md` frontmatter |

These schemas are referenced from `apm.yml` under the `schemas:` key and used
by the PR validation pipeline (A0 station) to enforce structural correctness.

## Nestable Workflows

Workflows with `config.nestable: true` can be embedded as sub-workflows inside
other workflow stations using the `workflow-engine` skill.

| Nestable Workflow | Nested From |
|-------------------|-------------|
| `quality-validation` | feature-implementation (station 8), modernization (station 9) |
| `pr-validation` | feature-implementation (station 9, optional), modernization (station 10, optional) |

The `workflow-orchestrator` agent with the `workflow-engine` skill handles
nested dispatch. Each nested workflow runs in its own state context and
reports results back to the parent station's gate.

## Station Prompt Mapping

The `ci-gates/stations/` directory contains the original A0–A7 prompt
files that power the PR validation pipeline. These map to the canonical
`pr-validation.yml` workflow stations:

| Station | Prompt File | Canonical Station ID |
|---------|-------------|---------------------|
| A0 | `a0-intake.prompt.md` | `a0-intake` |
| A1 | `a1-policy-validation.prompt.md` | `a1-policy-validation` |
| A2 | `a2-security-static.prompt.md` | `a2-security-static` |
| A3 | `a3-prompt-injection.prompt.md` | `a3-prompt-injection` |
| A4 | `a4-red-team.agent.md` | `a4-red-team` |
| A5 | `a5-sandbox-simulation.prompt.md` | `a5-sandbox-simulation` |
| A6 | `a6-policy-gate.agent.md` | `a6-policy-gate` |
| A7 | `a7-gitlab-update.prompt.md` | `a7-update` |
