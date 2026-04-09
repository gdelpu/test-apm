# AI SDLC Foundation

> **Cross-provider AI SDLC toolkit for specification-driven delivery, quality gating, and secure agent governance.**

A shared collection of AI agents, prompts, skills, workflows, instructions, and foundational knowledge — provider-agnostic by design, consumable from GitHub Copilot, Claude Code, CLI, or future MCP server.

<!-- ╔══════════════════════════════════════════════════════════════╗
     ║  SELF-MAINTENANCE: Keep this README in sync with the repo. ║
     ║  Counts and tables below must match actual files.          ║
     ║  After adding/removing any asset, update the relevant      ║
     ║  section AND the Repository Layout counts.                 ║
     ║  Run `python scripts/validate_all.py` to verify.          ║
     ╚══════════════════════════════════════════════════════════════╝ -->

| Asset | Count | Canonical Path |
|-------|------:|----------------|
| Agents | 23 | `.apm/agents/` |
| Skills | 89 | `.apm/skills/` |
| Workflows | 19 | `.apm/workflows/` |
| Hooks | 8 | `.apm/hooks/` |
| Prompts | 4 | `.apm/prompts/` |
| Instructions | 7 | `.apm/instructions/` |
| Knowledge areas | 4 | `knowledge/` |

---

## Table of Contents

- [Architecture](#architecture)
- [Repository Layout](#repository-layout)
- [Agents (23)](#agents-23)
- [Skills (89)](#skills-89)
- [Workflows (19)](#workflows-19)
  - [Delivery Workflows](#delivery-workflows)
    - [feature-implementation](#feature-implementation-10-stations)
    - [modernization](#modernization-10-stations)
    - [bug-fixing](#bug-fixing-7-stations)
    - [incident-resolution](#incident-resolution-7-stations)
    - [bmad](#bmad-4-stations)
    - [implementation-loop](#implementation-loop-6-stations)
  - [Specification Workflows](#specification-workflows)
    - [idea-to-spec](#idea-to-spec-7-stations)
    - [spec-kit](#spec-kit-8-stations)
    - [spec-to-execution](#spec-to-execution-6-stations)
  - [Validation Workflows](#validation-workflows)
    - [quality-validation](#quality-validation-7-stations)
    - [pr-validation](#pr-validation-11-stations)
    - [compliance-check](#compliance-check-6-stations)
    - [release-readiness](#release-readiness-6-stations)
  - [Assessment Workflows](#assessment-workflows)
    - [maturity-assessment](#maturity-assessment-4-stations)
    - [delivery-retrospective](#delivery-retrospective-5-stations)
  - [SDLC Harness Workflows](#sdlc-harness-workflows)
    - [sdlc-ba](#sdlc-ba-16-stations)
    - [sdlc-tech](#sdlc-tech-12-stations)
    - [sdlc-steer](#sdlc-steer-10-stations)
    - [sdlc-full](#sdlc-full-11-stations)
- [Prompts (4)](#prompts-4)
- [Knowledge Base](#knowledge-base)
- [Quick Start Guide](#quick-start-guide)
- [Concepts & Glossary](#concepts--glossary)
- [Provider Setup](#provider-setup)
- [PR Validation Pipeline](#pr-validation-pipeline)
- [Cross-Layer Validation](#cross-layer-validation)
- [Distribution & Installation](#distribution--installation)
  - [Quick Start — Consumers](#quick-start--consumers)
- [Prerequisites](#prerequisites)
- [Adding Capabilities](#adding-capabilities)
- [Contributing](#contributing)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CANONICAL LAYER                         │
│  .apm/agents/  .apm/skills/  .apm/workflows/  knowledge/    │
│  .apm/hooks/  .apm/templates/  .apm/scripts/  .apm/prompts/  │
│  (23 agents)  (89 skills)  (19 workflows)  (8 hooks)        │
│                                                governance,  │
│                                                playbooks)   │
└──────────────┬──────────────────────┬───────────────────────┘
               │                      │
  ┌────────────▼──────────────────────▼──────────────────┐
  │                  PROVIDER ADAPTERS                   │
  │                                                      │
  │  providers/github-copilot/   providers/claude-code/  │
  │    conventions.md              CLAUDE.md             │
│    sync-map.md                 commands/ (40)        │
│    → .github/ (runtime)                              │
│      agents/ (7)             providers/cli/          │
│      prompts/ (45)             lib/ (5)              │
│      instructions/ (6)         run-workflow.sh       │
  │                                                      │
  └──────────────────────┬───────────────────────────────┘
                         │
            ┌────────────▼──────────────┐
            │      Outputs: specs/      │
            │  features/  decisions/    │
            └───────────────────────────┘
```

**Two layers**:
1. **Canonical** — `.apm/` + `knowledge/` define all capabilities (source of truth)
2. **Adapter** — `providers/` document provider-specific conventions and mappings
3. **Runtime** — `.github/` (Copilot), `providers/claude-code/commands/` (Claude), `providers/cli/` (CLI)

---

## Repository Layout

<!-- UPDATE these counts when adding/removing files -->

| Path | Purpose |
|------|---------|
| `.apm/agents/` | Cross-provider agent definitions (23 agents) |
| `.apm/skills/` | Skill packages: `SKILL.md` + optional `tools/`, `docs/` (89 skills) |
| `.apm/prompts/` | Reusable prompt templates (4 prompts) |
| `.apm/instructions/` | Shared behavioral instructions (7 files) |
| `.apm/contexts/` | Reference documents for agents |
| `.apm/workflows/` | YAML workflow definitions with stations + gates (19 workflows) |
| `.apm/hooks/` | Pre/post execution hooks with schema and config (8 hooks) |
| `.apm/templates/` | Spec-kit workflow templates (plan, spec, tasks, checklist, agent-file) |
| `.apm/scripts/` | Workflow automation scripts (PowerShell) |
| `knowledge/` | Constitution, governance, playbooks, brand |
| `providers/github-copilot/` | Copilot adapter: agents, prompts, instructions, docs |
| `.github/` | Copilot runtime projection (generated by `project-copilot.ps1`) |
| `providers/claude-code/` | Claude Code adapter (`CLAUDE.md`, 40 commands) |
| `providers/cli/` | CLI workflow runner (`run-workflow.sh` + `lib/`) |
| `clients/` | Per-client overlay directories |
| `ci-gates/` | PR validation station implementations (A0–A7) |
| `scripts/` | Cross-layer validation scripts, APM build/publish/install helpers |
| `docs/` | [Quick Start](docs/quick-start.md), [Concepts](docs/concepts.md), [APM Consumer Guide](docs/apm-consumer-guide.md), [Distribution](docs/distribution.md) |

---

## Agents (23)

Agents are provider-agnostic definitions that pair with one or more skills to perform a role in workflows.

<!-- UPDATE this table when adding/removing agents in .apm/agents/ -->

| Agent | Description | Key Skills |
|-------|-------------|------------|
| `analysis-agent` | Diagnose production incidents by reconstructing timelines, analyzing logs/traces, identifying affected services, and forming root-cause hypotheses | `incident-analysis`, `root-cause-analysis`, `repo-analysis`, `bug-reproduction` |
| `architecture-governance` | Review specifications and plans against architecture principles, NFRs, and delivery guardrails | — |
| `bmad-orchestrator` | Drive the BMAD (Build → Measure → Analyze → Decide) feedback loop with evaluation scoring and adaptive decision-making | `iteration-scoring`, `drift-detection`, `adaptive-decision` |
| `brand-styler` | Generate and convert documents to Sopra Steria brand spec with AA accessibility compliance | `brand-styler`, `soprasteria-brand-core`, `soprasteria-assets-and-templates` |
| `bug-fixer` | Drive structured bug diagnosis and resolution from triage through root-cause analysis, fix planning, and regression testing | `bug-triage`, `bug-reproduction`, `root-cause-analysis`, `fix-planning` |
| `hub-orchestrator` | Central triage agent — discovers available workflows and agents, classifies user intent, and dispatches execution | `hub-classification` |
| `implementer` | Execute implementation tasks by reading task breakdowns and producing/modifying code following constitution and plan constraints | `code-implementation` |
| `modernization-agent` | Guide modernization through baseline assessment, target definition, migration planning, and task breakdown (workflow-native) | `brownfield-context`, `repo-analysis`, `codebase-assessment`, `spec-feature`, `spec-plan`, `migration-planning`, `spec-clarify`, `spec-tasks` |
| `modernization-orchestrator` | Coordinate specialised sub-agents for assessment, planning, implementation, and parity validation in brownfield modernization | `codebase-assessment`, `brownfield-context`, `repo-analysis`, `adr-generation`, `migration-planning`, `spec-feature`, `spec-plan`, `spec-tasks`, `code-implementation`, `code-refactoring`, `parity-validation`, `test-strategy`, `nfr-review` |
| `quality-validator` | Execute quality and security validation stations using external tool adapters; produce structured pass/fail reports | `lint-analysis`, `static-analysis`, `security-scan`, `dependency-audit`, `coverage-assessment`, `quality-report` |
| `refactor-parity-checker` | Verify refactored application matches original behaviour and visual appearance via side-by-side comparison | `parity-validation` |
| `repository-analyzer` | Analyze a code repository to provide a high-level architectural and functional overview | `repo-analysis` |
| `reverse-backlog` | Analyze legacy code repositories and create a consolidated, business-focused product backlog | `repo-analysis` |
| `reverse-user-story` | Create detailed user stories with acceptance criteria from existing codebases | `repo-analysis` |
| `security-reviewer` | Review prompts, agents, instructions, and code for prompt injection, data exfiltration, privilege escalation (OWASP Top 10 LLMs) | `soprasteria-agent-policy-guard`, `injection-detection`, `secret-scan` |
| `soprasteria-branding` | Assess, adapt, and refactor applications, documents, and presentations for Sopra Steria brand compliance | `soprasteria-brand-core`, `soprasteria-brand-assets`, `soprasteria-app-branding`, `soprasteria-document-branding`, `soprasteria-web-accessibility`, `soprasteria-audit-checklist` |
| `spec-orchestrator` | Lead structured, specification-driven flows for software changes and new initiatives | `brownfield-context`, `spec-constitution`, `spec-feature`, `spec-clarify`, `spec-plan`, `spec-tasks`, `spec-quality-gate`, `adr-generation`, `test-strategy`, `nfr-review`, `architecture-guardrails` |
| `workflow-orchestrator` | Execute workflow definitions by driving stations sequentially, evaluating quality gates, and managing workflow state | `workflow-engine` |
| `sdlc-coordinator` | Orchestrate the full SDLC lifecycle — DAG resolution, wave scheduling, fan-out/fan-in, gate management across BA/Tech/Steer/Test domains | All `sdlc-*` skills |
| `sdlc-ba-analyst` | Business analysis from brownfield audit through scoping, specification, and per-feature functional design | `sdlc-ba-audit`, `sdlc-ba-scoping`, `sdlc-ba-specification`, `sdlc-ba-functional-design` |
| `sdlc-tech-architect` | Technical architecture from audit through ADR fan-out, design, and continuous quality | `sdlc-tech-audit`, `sdlc-tech-architecture`, `sdlc-tech-design`, `sdlc-tech-quality` |
| `sdlc-steer-manager` | Steering and project management across initialization, planning, sprint tracking, and governance | `sdlc-steer-init`, `sdlc-steer-planning`, `sdlc-steer-sprint`, `sdlc-steer-governance` |
| `sdlc-test-executor` | Test execution for E2E/UAT campaigns and performance testing | `sdlc-test-campaign`, `sdlc-test-performance` |

Canonical definitions: `.apm/agents/`. Copilot runtime projection: `.github/agents/` (7 user-facing agents).

---

## Skills (89)

Skills are reusable knowledge and tool packages. Each skill has a `SKILL.md` manifest + optional `tools/` and `docs/` directories.

<!-- UPDATE this table when adding/removing skills in .apm/skills/ -->

### Orchestration Skills

| Skill | Description |
|-------|-------------|
| `hub-classification` | Classify user intent against available workflows and agents, then recommend the best match for dispatch |

### SDLC & Specification Skills

| Skill | Description |
|-------|-------------|
| `spec-constitution` | Generate engineering constitutions covering architecture, quality, security, testing, observability |
| `spec-feature` | Produce feature specifications with scope, acceptance criteria, and user stories |
| `spec-clarify` | Resolve ambiguities through structured clarification loops |
| `spec-plan` | Generate implementation plans with risk analysis and rollout/rollback strategies |
| `spec-tasks` | Decompose plans into traceable, ordered task breakdowns |
| `spec-quality-gate` | Evaluate specification completeness and coherence |
| `plan-writing` | Structured plan composition |
| `planning-with-files` | File-based planning workflows |

### Architecture & Design Skills

| Skill | Description |
|-------|-------------|
| `architecture-guardrails` | Validate against architecture principles and delivery guardrails |
| `domain-driven-design` | DDD patterns and bounded-context modelling |
| `docs-architect` | Documentation architecture and structure |

### Implementation Skills

| Skill | Description |
|-------|-------------|
| `code-implementation` | Produce or modify code following project constraints and standards |
| `code-refactoring` | General code refactoring patterns |
| `code-refactoring-refactor-clean` | Clean refactoring techniques |
| `code-refactoring-tech-debt` | Technical debt reduction strategies |

### Quality & Validation Skills

| Skill | Description |
|-------|-------------|
| `lint-analysis` | Execute and interpret lint tool results |
| `static-analysis` | Run and interpret static analysis tools |
| `security-scan` | SAST/DAST security scanning |
| `dependency-audit` | Audit dependencies for known CVEs |
| `coverage-assessment` | Assess test coverage against thresholds |
| `quality-report` | Generate aggregated quality reports |
| `test-validation` | Test validation utilities |
| `ai-backbone-pr-checks` | Deterministic MR validators (frontmatter, YAML, test gaps) |

### .NET Skills

| Skill | Description |
|-------|-------------|
| `dotnet-architect` | .NET architecture patterns and decisions |
| `dotnet-backend` | .NET backend development |
| `dotnet-backend-patterns` | .NET backend design patterns |

### React & Frontend Skills

| Skill | Description |
|-------|-------------|
| `react-best-practices` | React best practices and idioms |
| `react-flow-architect` | React Flow architecture design |
| `react-flow-node-ts` | React Flow TypeScript node patterns |
| `react-modernization` | React modernization strategies |
| `react-native-architecture` | React Native architecture patterns |
| `react-patterns` | React component and hook patterns |
| `react-state-management` | React state management approaches |
| `react-ui-patterns` | React UI/UX component patterns |
| `frontend-developer` | General frontend development |
| `frontend-dev-guidelines` | Frontend coding guidelines |
| `frontend-security-coder` | Frontend security practices |
| `frontend-ui-dark-ts` | Dark-mode TypeScript UI development |

### API Skills

| Skill | Description |
|-------|-------------|
| `api-design-principles` | API design principles and standards |
| `api-documentation` | API documentation generation |
| `api-patterns` | API implementation patterns |
| `api-security-best-practices` | API security hardening |

### Claude Code Skills

| Skill | Description |
|-------|-------------|
| `cc-skill-backend-patterns` | Claude Code backend development patterns |
| `cc-skill-coding-standards` | Claude Code coding standards |
| `cc-skill-frontend-patterns` | Claude Code frontend development patterns |

### Branding & Accessibility Skills

| Skill | Description |
|-------|-------------|
| `brand-styler` | Pandoc-based DOCX/PDF generation with brand compliance |
| `soprasteria-agent-policy-guard` | Shift-left policy enforcement (A1–A6 rules) |
| `soprasteria-app-branding` | Application branding audit and refactoring |
| `soprasteria-assets-and-templates` | Brand asset and template management |
| `soprasteria-audit-checklist` | Compliance audit checklists |
| `soprasteria-brand-assets` | Brand asset library |
| `soprasteria-brand-core` | Core brand guidelines and colour/typography rules |
| `soprasteria-document-branding` | Document branding refactoring |
| `soprasteria-web-accessibility` | WCAG 2.1 AA validation |

### SDLC Harness Skills

| Skill | Description |
|-------|-------------|
| `sdlc-ba-audit` | Brownfield functional audit — AS-IS snapshot and evolution delta analysis (S0) |
| `sdlc-ba-scoping` | Product scoping — vision, glossary, actors & roles, functional requirements (S1) |
| `sdlc-ba-specification` | Specification — domain model, epic decomposition, features, business rules (S2) |
| `sdlc-ba-functional-design` | Per-feature functional design — user stories, journeys, screens, test scenarios (S3) |
| `sdlc-tech-audit` | Technical stack audit and gap analysis (T0) |
| `sdlc-tech-architecture` | System context (C4), ADR generation with fan-out, stack extraction, enablers (T1) |
| `sdlc-tech-design` | Data model DDL, API contracts, test strategy, implementation plan (T2) |
| `sdlc-tech-quality` | Continuous quality — drift detection, code review, E2E Playwright generation (T3) |
| `sdlc-steer-init` | Project initialization — project sheet, KPI baseline (P0) |
| `sdlc-steer-planning` | Iteration planning — sprint plan, roadmap, risk register (P1) |
| `sdlc-steer-sprint` | Sprint tracking — progress metrics, system health, sprint risks (P2) |
| `sdlc-steer-governance` | Governance — COPIL preparation, Go/No-Go decisions (P3) |
| `sdlc-test-campaign` | E2E/UAT test campaign launch and reporting |
| `sdlc-test-performance` | Performance test execution and reporting |
| `sdlc-deliverable-validation` | Cross-domain deliverable quality audit |
| `sdlc-change-impact` | Impact analysis and amendment flow |
| `sdlc-confluence-sync` | Confluence push/pull with Pandoc conversion |
| `sdlc-scaffold` | Project directory scaffolding |

Canonical definitions: `.apm/skills/<name>/SKILL.md`.

---

## Workflows (19)

Workflows are YAML-defined pipelines of sequential **stations**, each assigned to an **agent** with specific **skills**. Every station has a **quality gate** with pass/fail criteria. Workflows support resume, skip-gate (where configured), and nesting.

Schema reference: `.apm/workflows/_schema.md`.

### Delivery Workflows

Workflows that drive end-to-end feature or fix delivery from specification through implementation and quality validation.

---

#### `feature-implementation` (10 stations)

> End-to-end feature delivery from constitution through specification, planning, implementation, and quality validation.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Constitution** | `spec-orchestrator` | `spec-constitution` | `constitution.md` | Blocker |
| 2 | **Feature Specification** | `spec-orchestrator` | `spec-feature` | `spec.md` | Blocker |
| 3 | **Clarification** | `spec-orchestrator` | `spec-clarify` | `clarifications.md` | Blocker |
| 4 | **Architecture Review** | `architecture-governance` | `architecture-guardrails` | `architecture-review.md` | Blocker |
| 5 | **Implementation Plan** | `spec-orchestrator` | `spec-plan` | `plan.md` | Blocker |
| 6 | **Task Breakdown** | `spec-orchestrator` | `spec-tasks` | `tasks.md` | Blocker |
| 7 | **Implementation** | `implementer` | `code-implementation` | `implementation-log.md` | Blocker |
| 8 | **Quality Validation** | `workflow-orchestrator` | `workflow-engine` | `quality-report.md` | Blocker |
| 9 | **PR Validation** *(optional)* | `workflow-orchestrator` | `workflow-engine` | `pr-validation-report.md` | Blocker |
| 10 | **Final Quality Gate** | `spec-orchestrator` | `spec-quality-gate` | `quality-gate.md` | Blocker |

**Flow**: Constitution → Specification → Clarification → Architecture Review → Plan → Tasks → Implementation → Quality Validation → PR Validation → Final Gate

**Output directory**: `specs/features/<feature>/`

---

#### `modernization` (10 stations)

> Guided modernization from baseline assessment through target definition, migration planning, implementation, and quality assurance.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Baseline Assessment** | `modernization-agent` | `repo-analysis` | `reverse-brief.md` | Blocker |
| 2 | **Architecture Decisions** | `modernization-agent` | `adr-generation` | `decisions.md` | Blocker |
| 3 | **Target State Definition** | `modernization-agent` | `spec-feature` | `spec.md` | Blocker |
| 4 | **Architecture Review** | `architecture-governance` | `architecture-guardrails` | `architecture-review.md` | Blocker |
| 5 | **Migration Plan** | `modernization-agent` | `spec-plan` | `plan.md` | Blocker |
| 6 | **Risk Clarification** | `modernization-agent` | `spec-clarify` | `clarifications.md` | Blocker |
| 7 | **Task Breakdown** | `modernization-agent` | `spec-tasks` | `tasks.md` | Blocker |
| 8 | **Implementation** | `implementer` | `code-implementation` | `implementation-log.md` | Blocker |
| 9 | **Quality Validation** | `workflow-orchestrator` | `workflow-engine` | `quality-report.md` | Blocker |
| 10 | **PR Validation** *(optional)* | `workflow-orchestrator` | `workflow-engine` | `pr-validation-report.md` | Blocker |

**Flow**: Baseline → Decisions → Target State → Architecture Review → Migration Plan → Risk Clarification → Tasks → Implementation → Quality Validation → PR Validation

**Output directory**: `specs/features/<feature>/`

---

#### `bug-fixing` (7 stations)

> Structured bug resolution from triage through root-cause analysis, fix, regression testing, and quality validation.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Triage** | `spec-orchestrator` | `spec-clarify` | `triage.md` | Blocker |
| 2 | **Reproduce** | `implementer` | `code-implementation` | `reproduction-log.md` | Blocker |
| 3 | **Root Cause Analysis** | `spec-orchestrator` | `repo-analysis` | `root-cause.md` | Blocker |
| 4 | **Fix Implementation** | `implementer` | `code-implementation` | `fix-log.md` | Blocker |
| 5 | **Regression Testing** | `implementer` | `code-implementation` | `regression-report.md` | Blocker |
| 6 | **Quality Validation** | `workflow-orchestrator` | `workflow-engine` | `quality-report.md` | Blocker |
| 7 | **Close** | `spec-orchestrator` | `spec-quality-gate` | `closure.md` | Blocker |

**Flow**: Triage → Reproduce → Root Cause → Fix → Regression → Quality Validation → Close

**Output directory**: `specs/bugs/<bug-id>/`

---

#### `incident-resolution` (7 stations)

> Structured incident diagnosis and resolution from analysis through fix, regression testing, and knowledge capture.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Incident Analysis** | `analysis-agent` | `incident-analysis`, `repo-analysis` | `incident-analysis.md` | Blocker |
| 2 | **Root Cause Hypothesis** | `analysis-agent` | `root-cause-analysis` | `root-cause.md` | Blocker |
| 3 | **Reproduction Scenario** | `analysis-agent` | `incident-analysis`, `bug-reproduction` | `reproduction.md` | Blocker |
| 4 | **Fix Proposal** | `implementer` | `fix-planning`, `code-implementation` | `plan.md`, `tasks.md` | Blocker |
| 5 | **Regression Test Creation** | `implementer` | `code-implementation`, `test-strategy` | `regression-tests.md` | Blocker |
| 6 | **Patch Validation** | `quality-validator` | `lint-analysis`, `coverage-assessment`, `security-scan` | `validation-report.md` | Blocker |
| 7 | **Knowledge Update** | `spec-orchestrator` | `knowledge-update`, `adr-generation` | `knowledge-update.md` | Warning |

**Flow**: Incident Analysis → Root Cause Hypothesis → Reproduction → Fix Proposal → Regression Tests → Patch Validation → Knowledge Update

**Output directory**: `specs/features/<feature>/`

---

#### `bmad` (4 stations)

> Build-Measure-Analyze-Decide feedback loop for hypothesis-driven delivery.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Build** | `implementer` | `code-implementation` | `build-log.md` | Blocker |
| 2 | **Measure** | `quality-validator` | `coverage-assessment` | `metrics.md` | Blocker |
| 3 | **Analyze** | `spec-orchestrator` | `spec-clarify` | `analysis.md` | Blocker |
| 4 | **Decide** | `spec-orchestrator` | `adr-generation` | `decision.md` | Blocker |

**Flow**: Build → Measure → Analyze → Decide (iterate)

**Output directory**: `specs/features/<feature>/`

---

#### `implementation-loop` (6 stations)

> Agent-assisted development loop from task selection through code generation, review, testing, and commit readiness.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Task Selection** | `implementer` | `code-implementation` | `current-task.md` | Blocker |
| 2 | **Code Generation** | `implementer` | `code-implementation` | `implementation-log.md` | Blocker |
| 3 | **Self-Review** | `implementer` | `code-implementation`, `lint-analysis` | `review-notes.md` | Warning |
| 4 | **Test Generation** | `implementer` | `code-implementation`, `coverage-assessment` | `test-log.md` | Blocker |
| 5 | **Local Validation** | `quality-validator` | `lint-analysis`, `coverage-assessment` | `validation-report.md` | Blocker |
| 6 | **Commit Readiness** | `implementer` | `code-implementation` | `commit-summary.md` | Blocker |

**Flow**: Task Selection → Code Generation → Self-Review → Test Generation → Local Validation → Commit Readiness

**Output directory**: `specs/features/<feature>/`

---

### Specification Workflows

Workflows that focus on producing validated specification artifacts without implementation.

---

#### `idea-to-spec` (7 stations)

> Transform a raw idea into a validated, unambiguous specification with NFRs and architecture sketch.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Intent Capture** | `spec-orchestrator` | `intent-capture` | `intent.md` | Blocker |
| 2 | **Domain / Context Enrichment** *(optional)* | `spec-orchestrator` | `brownfield-context`, `repo-analysis` | `context-brief.md` | Warning |
| 3 | **Feature Specification** | `spec-orchestrator` | `spec-feature` | `spec.md` | Blocker |
| 4 | **Clarification Loop** | `spec-orchestrator` | `spec-clarify` | `clarifications.md` | Blocker |
| 5 | **NFR Definition** | `spec-orchestrator` | `nfr-review` | `nfr-review.md` | Blocker |
| 6 | **Architecture Sketch** | `architecture-governance` | `architecture-guardrails` | `architecture-review.md` | Blocker |
| 7 | **Spec Quality Gate** | `spec-orchestrator` | `spec-quality-gate` | `quality-gate.md` | Blocker |

**Flow**: Intent Capture → Domain Enrichment → Specification → Clarification → NFRs → Architecture Sketch → Quality Gate

**Output directory**: `specs/features/<feature>/`

---

#### `spec-kit` (8 stations)

> Specification-only flow — produce a complete spec package without implementation.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Constitution** | `spec-orchestrator` | `spec-constitution` | `constitution.md` | Blocker |
| 2 | **Feature Specification** | `spec-orchestrator` | `spec-feature` | `spec.md` | Blocker |
| 3 | **Clarification** | `spec-orchestrator` | `spec-clarify` | `clarifications.md` | Blocker |
| 4 | **Architecture Review** | `architecture-governance` | `architecture-guardrails` | `architecture-review.md` | Blocker |
| 5 | **Implementation Plan** | `spec-orchestrator` | `spec-plan` | `plan.md` | Blocker |
| 6 | **Task Breakdown** | `spec-orchestrator` | `spec-tasks` | `tasks.md` | Blocker |
| 7 | **Test Strategy** | `spec-orchestrator` | `test-strategy` | `test-strategy.md` | Blocker |
| 8 | **Spec Quality Gate** | `spec-orchestrator` | `spec-quality-gate` | `quality-gate.md` | Blocker |

**Flow**: Constitution → Specification → Clarification → Architecture Review → Plan → Tasks → Test Strategy → Quality Gate

**Output directory**: `specs/features/<feature>/`

---

#### `spec-to-execution` (6 stations)

> Transform a validated specification into an executable plan with risk analysis, rollback strategy, and decomposed tasks.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Plan Generation** | `spec-orchestrator` | `spec-plan` | `plan.md` | Blocker |
| 2 | **Risk Analysis** | `architecture-governance` | `architecture-guardrails`, `nfr-review` | `risk-analysis.md` | Blocker |
| 3 | **Rollout / Rollback Definition** | `spec-orchestrator` | `spec-plan` | `rollout-strategy.md` | Blocker |
| 4 | **Task Decomposition** | `spec-orchestrator` | `spec-tasks` | `tasks.md` | Blocker |
| 5 | **Test Strategy Alignment** | `spec-orchestrator` | `test-strategy` | `test-strategy.md` | Warning |
| 6 | **Execution Readiness Gate** | `spec-orchestrator` | `spec-quality-gate` | `execution-readiness.md` | Blocker |

**Flow**: Plan → Risk Analysis → Rollout/Rollback → Tasks → Test Strategy → Execution Readiness

**Output directory**: `specs/features/<feature>/`

---

### Validation Workflows

Workflows that validate quality, security, compliance, or release readiness. Can be nested inside delivery workflows.

---

#### `quality-validation` (7 stations)

> Validate code quality, security, and compliance using external tool adapters.

| # | Station | Agent | Skills | Outputs | Gate Severity | Parallel |
|---|---------|-------|--------|---------|---------------|----------|
| 1 | **Lint Analysis** | `quality-validator` | `lint-analysis` | `lint-report.md` | Blocker | ✅ |
| 2 | **Static Analysis** | `quality-validator` | `static-analysis` | `static-analysis-report.md` | Blocker | ✅ |
| 3 | **Security SAST Scan** | `quality-validator` | `security-scan` | `sast-report.md` | Blocker | ✅ |
| 4 | **Dependency Audit** | `quality-validator` | `dependency-audit` | `dependency-report.md` | Blocker | ✅ |
| 5 | **Test Coverage Assessment** | `quality-validator` | `coverage-assessment` | `coverage-report.md` | Blocker | |
| 6 | **Security DAST Scan** *(optional)* | `quality-validator` | `security-scan` | `dast-report.md` | Warning | |
| 7 | **Quality Report** | `quality-validator` | `quality-report` | `quality-report.md` | Blocker | |

**Flow**: Lint ∥ Static Analysis ∥ SAST ∥ Dependency Audit → Coverage → DAST → Quality Report

**Nestable**: Yes — embedded by `feature-implementation`, `modernization`, `bug-fixing`.

---

#### `pr-validation` (11 stations)

> Multi-stage merge request validation pipeline with deterministic checks and AI-powered security stations.

**Phase 1 — Deterministic validators (parallel)**:

| # | Station | Agent | Skills | Outputs | Gate Severity | Parallel |
|---|---------|-------|--------|---------|---------------|----------|
| 1 | **PR Auto Validator** | `pr-validator` | `ai-backbone-pr-checks` | `reports/pr-auto-validator.json` | Blocker | ✅ |
| 2 | **YAML Workflow Linter** | `pr-validator` | `ai-backbone-pr-checks` | `reports/yaml-workflow-linter.json` | Blocker | ✅ |
| 3 | **Test Gap Detector** *(optional)* | `pr-validator` | `ai-backbone-pr-checks` | `reports/test-gap-detector.json` | Warning | ✅ |

**Phase 2 — AI stations (sequential)**:

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 4 | **A0 Intake** | `station-orchestrator` | — | `station_out/work_order.json` | Warning |
| 5 | **A1 Policy Validation** | `station-orchestrator` | `soprasteria-agent-policy-guard` | `station_out/policy_report.json` | Blocker |
| 6 | **A2 Security Static** | `station-orchestrator` | `secret-scan` | `station_out/security_report.json` | Blocker |
| 7 | **A3 Prompt Injection** | `station-orchestrator` | `injection-detection` | `station_out/promptsec_report.json` | Blocker |
| 8 | **A4 Red Team** *(optional)* | `station-orchestrator` | `red-team-simulation` | `station_out/a4_result.json` | Warning |
| 9 | **A5 Sandbox Simulation** | `station-orchestrator` | `sandbox-execution` | `station_out/sim_report.json` | Blocker |
| 10 | **A6 Policy Gate** | `station-orchestrator` | `policy-gate` | `station_out/gate_decision.json` | Blocker |
| 11 | **A7 Platform Update** *(optional)* | `station-orchestrator` | — | — | Warning |

**Flow**: PR Auto ∥ YAML Lint ∥ Test Gaps → A0 → A1 → A2 → A3 → A4 → A5 → A6 → A7

**Nestable**: Yes — can be embedded in delivery workflows.

---

#### `compliance-check` (6 stations)

> Validate compliance, privacy, and AI governance requirements including PII scanning, prompt injection detection, and risk scoring.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **PII Scan** | `quality-validator` | `governance-rules` | `pii-report.md` | Blocker |
| 2 | **Prompt Injection Detection** | `quality-validator` | `governance-rules`, `security-scan` | `prompt-injection-report.md` | Blocker |
| 3 | **Policy Validation** | `workflow-orchestrator` | `governance-rules` | `policy-report.md` | Blocker |
| 4 | **Risk Scoring** | `workflow-orchestrator` | `risk-scoring` | `risk-score.md` | Blocker |
| 5 | **Human Approval** *(optional)* | `workflow-orchestrator` | `governance-rules` | `approval-record.md` | Warning |
| 6 | **Compliance Report** | `workflow-orchestrator` | `governance-rules`, `quality-report` | `compliance-report.md` | Blocker |

**Flow**: PII Scan → Injection Detection → Policy Validation → Risk Scoring → Human Approval → Compliance Report

**Output directory**: `specs/features/<feature>/`

---

#### `release-readiness` (6 stations)

> Validate that a feature meets all release criteria across spec completeness, testing, security, observability, and deployment.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Spec Completeness Check** | `spec-orchestrator` | `spec-quality-gate` | `spec-completeness.md` | Blocker |
| 2 | **Test Completeness** | `quality-validator` | `coverage-assessment`, `test-strategy` | `test-completeness.md` | Blocker |
| 3 | **Security Validation** | `quality-validator` | `security-scan`, `dependency-audit` | `security-report.md` | Blocker |
| 4 | **Observability Readiness** | `architecture-governance` | `observability-readiness`, `nfr-review` | `observability-report.md` | Blocker |
| 5 | **Deployment Readiness** | `spec-orchestrator` | `spec-quality-gate` | `deployment-readiness.md` | Blocker |
| 6 | **Go / No-Go Decision** | `spec-orchestrator` | `spec-quality-gate`, `quality-report` | `release-decision.md` | Blocker |

**Flow**: Spec Completeness → Test Completeness → Security → Observability → Deployment Readiness → Go/No-Go

**Output directory**: `specs/features/<feature>/`

---

### Assessment Workflows

Workflows that assess maturity, patterns, and process health without producing implementation artifacts.

---

#### `maturity-assessment` (4 stations)

> Assess SDLC maturity across dimensions and produce a scored report with improvement roadmap.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Maturity Assessment** | `repository-analyzer` | `repo-analysis` | `assessment.md` | Blocker |
| 2 | **Scoring** | `spec-orchestrator` | `spec-clarify` | `scores.md` | Blocker |
| 3 | **Maturity Report** | `spec-orchestrator` | `spec-feature` | `maturity-report.md` | Blocker |
| 4 | **Improvement Roadmap** | `spec-orchestrator` | `spec-plan` | `roadmap.md` | Blocker |

**Flow**: Assessment → Scoring → Report → Roadmap

**Output directory**: `specs/assessments/<assessment-id>/`

---

#### `delivery-retrospective` (5 stations)

> AI-native continuous improvement cycle analyzing delivery metrics, defects, bottlenecks, and producing actionable improvements.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Analyze Cycle Time** | `spec-orchestrator` | `delivery-metrics` | `cycle-time-report.md` | Warning |
| 2 | **Analyze Defects** | `spec-orchestrator` | `delivery-metrics`, `quality-report` | `defect-report.md` | Warning |
| 3 | **Identify Bottlenecks** | `spec-orchestrator` | `delivery-metrics` | `bottleneck-report.md` | Warning |
| 4 | **Suggest Improvements** | `architecture-governance` | `architecture-guardrails`, `delivery-metrics` | `improvement-proposals.md` | Warning |
| 5 | **Update Constitution / Playbooks** | `spec-orchestrator` | `knowledge-update`, `adr-generation` | `retrospective-actions.md` | Warning |

**Flow**: Cycle Time Analysis → Defect Analysis → Bottleneck Identification → Improvement Suggestions → Constitution/Playbook Update

**Output directory**: `specs/features/<feature>/`

---

### SDLC Harness Workflows

Workflows migrated from the SDLC Agentic Harness. They provide a prescriptive, deliverable-driven methodology with DAG-based orchestration, fan-out/fan-in patterns, and cross-domain traceability. Can be nested inside other delivery workflows.

---

#### `sdlc-ba` (16 stations)

> Full business analysis pipeline from brownfield audit through scoping, specification, and per-feature functional design with fan-out/fan-in orchestration.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Existing System Audit** *(optional)* | `sdlc-ba-analyst` | `sdlc-ba-audit` | `asis-001-existing-audit.md` | Blocker |
| 2 | **Delta Analysis** *(optional)* | `sdlc-ba-analyst` | `sdlc-ba-audit` | `delta-001-delta-analysis.md` | Blocker |
| 3 | **Product Vision & Scope** | `sdlc-ba-analyst` | `sdlc-ba-scoping` | `vis-001-product-vision.md` | Blocker |
| 4 | **Business Glossary** | `sdlc-ba-analyst` | `sdlc-ba-scoping` | `glo-001-glossary.md` | Blocker |
| 5 | **Actors & Roles** | `sdlc-ba-analyst` | `sdlc-ba-scoping` | `act-001-actors-roles.md` | Blocker |
| 6 | **Functional Requirements** | `sdlc-ba-analyst` | `sdlc-ba-scoping` | `exf-001-requirements.md` | Blocker |
| 7 | **Domain Model** | `sdlc-ba-analyst` | `sdlc-ba-specification` | `dom-001-domain-model.md` | Blocker |
| 8 | **Epic Decomposition** | `sdlc-ba-analyst` | `sdlc-ba-specification` | `ep-xxx-epics.md` | Blocker |
| 9 | **Feature Specification** *(fan-out)* | `sdlc-ba-analyst` | `sdlc-ba-specification` | `ft-xxx-features.md` | Blocker |
| 10 | **Business Rules** | `sdlc-ba-analyst` | `sdlc-ba-specification` | `brl-xxx-rules.md` | Blocker |
| 11 | **User Stories** *(per-feature)* | `sdlc-ba-analyst` | `sdlc-ba-functional-design` | `us-xxx-stories.md` | Blocker |
| 12 | **User Journeys** *(per-feature)* | `sdlc-ba-analyst` | `sdlc-ba-functional-design` | `uf-xxx-journeys.md` | Blocker |
| 13 | **Screen Specifications** *(per-feature)* | `sdlc-ba-analyst` | `sdlc-ba-functional-design` | `scr-xxx-screens.md` | Blocker |
| 14 | **Test Scenarios** *(per-feature)* | `sdlc-ba-analyst` | `sdlc-ba-functional-design` | `sce-xxx-scenarios.md` | Blocker |
| 15 | **E2E Test Plan** | `sdlc-ba-analyst` | `sdlc-ba-functional-design` | `e2e-plan-001.md` | Blocker |
| 16 | **Validation Gate** | `sdlc-coordinator` | `sdlc-deliverable-validation` | `ba-validation-report.md` | Blocker |

**Flow**: Audit → Delta → Vision ∥ Glossary → Actors → Requirements → Domain Model → Epics → Features (fan-out) → Rules → Stories ∥ Journeys ∥ Screens (per feature) → Scenarios → E2E Plan → Validation

**Nestable**: Yes

**Output directory**: `docs/ba/`

---

#### `sdlc-tech` (12 stations)

> Full technical pipeline from audit through architecture (ADR fan-out), incremental design, and continuous quality.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Technical Audit** | `sdlc-tech-architect` | `sdlc-tech-audit` | `tech-asis-001.md` | Blocker |
| 2 | **Gap Analysis** | `sdlc-tech-architect` | `sdlc-tech-audit` | `gap-001.md` | Blocker |
| 3 | **System Context (C4)** | `sdlc-tech-architect` | `sdlc-tech-architecture` | `ctx-001-system-context.md` | Blocker |
| 4 | **Architecture Decisions** *(fan-out)* | `sdlc-tech-architect` | `sdlc-tech-architecture` | `adr-xxx.md` | Blocker |
| 5 | **Stack Extraction** | `sdlc-tech-architect` | `sdlc-tech-architecture` | `stk-001-stack.md` | Blocker |
| 6 | **Enabler Extraction** | `sdlc-tech-architect` | `sdlc-tech-architecture` | `enb-xxx-enablers.md` | Blocker |
| 7 | **Data Model** | `sdlc-tech-architect` | `sdlc-tech-design` | `dat-001-data-model.md` | Blocker |
| 8 | **API Contracts** | `sdlc-tech-architect` | `sdlc-tech-design` | `api-xxx-contracts.md` | Blocker |
| 9 | **Test Strategy** | `sdlc-tech-architect` | `sdlc-tech-design` | `tst-001-test-strategy.md` | Blocker |
| 10 | **Implementation Plan** | `sdlc-tech-architect` | `sdlc-tech-design` | `imp-001-plan.md` | Blocker |
| 11 | **Drift Detection** | `sdlc-tech-architect` | `sdlc-tech-quality` | `drift-report.md` | Warning |
| 12 | **E2E Generation** | `sdlc-tech-architect` | `sdlc-tech-quality` | `e2e-tests/` | Warning |

**Flow**: Audit → Gap Analysis → System Context → ADRs (fan-out) → Stack → Enablers → Data Model → API Contracts → Test Strategy → Implementation Plan → Drift Detection → E2E Generation

**Nestable**: Yes

**Output directory**: `docs/tech/`

---

#### `sdlc-steer` (10 stations)

> Steering and project management pipeline from initialization through planning, sprint tracking, and governance.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Project Sheet** | `sdlc-steer-manager` | `sdlc-steer-init` | `project-sheet.md` | Blocker |
| 2 | **KPI Baseline** | `sdlc-steer-manager` | `sdlc-steer-init` | `kpi-baseline.md` | Blocker |
| 3 | **Sprint Planning** | `sdlc-steer-manager` | `sdlc-steer-planning` | `sprint-plan.md` | Blocker |
| 4 | **Roadmap** | `sdlc-steer-manager` | `sdlc-steer-planning` | `roadmap.md` | Blocker |
| 5 | **Risk Register** | `sdlc-steer-manager` | `sdlc-steer-planning` | `risk-register.md` | Blocker |
| 6 | **Sprint Progress** | `sdlc-steer-manager` | `sdlc-steer-sprint` | `sprint-progress.md` | Warning |
| 7 | **System Health** | `sdlc-steer-manager` | `sdlc-steer-sprint` | `system-health.md` | Warning |
| 8 | **Sprint Risks** | `sdlc-steer-manager` | `sdlc-steer-sprint` | `sprint-risks.md` | Warning |
| 9 | **COPIL Preparation** | `sdlc-steer-manager` | `sdlc-steer-governance` | `steering-committee.md` | Blocker |
| 10 | **Go / No-Go** | `sdlc-steer-manager` | `sdlc-steer-governance` | `go-nogo-decision.md` | Blocker |

**Flow**: Project Sheet → KPI Baseline → Sprint Planning → Roadmap → Risk Register → Sprint Progress → System Health → Sprint Risks → COPIL → Go/No-Go

**Nestable**: Yes

**Output directory**: `docs/steer/`

---

#### `sdlc-full` (11 stations)

> Composite SDLC pipeline orchestrating all domains end-to-end: scaffold → BA → Tech → Test → Steer governance.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Scaffold** | `sdlc-coordinator` | `sdlc-scaffold` | `docs/project.yml` | Blocker |
| 2 | **Project Init** | `sdlc-steer-manager` | `sdlc-steer-init` | `project-sheet.md`, `kpi-baseline.md` | Blocker |
| 3 | **BA Pipeline** *(nested)* | `sdlc-ba-analyst` | `sdlc-ba-*` | `docs/ba/` | Blocker |
| 4 | **Sprint Planning** | `sdlc-steer-manager` | `sdlc-steer-planning` | `sprint-plan.md`, `roadmap.md` | Blocker |
| 5 | **Tech Pipeline** *(nested)* | `sdlc-tech-architect` | `sdlc-tech-*` | `docs/tech/` | Blocker |
| 6 | **Implementation** | `implementer` | `code-implementation` | implementation artifacts | Blocker |
| 7 | **Test Campaign** | `sdlc-test-executor` | `sdlc-test-campaign` | `test-campaign-report.md` | Blocker |
| 8 | **Performance Tests** | `sdlc-test-executor` | `sdlc-test-performance` | `perf-report.md` | Blocker |
| 9 | **Sprint Tracking** *(nested)* | `sdlc-steer-manager` | `sdlc-steer-sprint` | sprint metrics | Warning |
| 10 | **Quality Validation** *(nested)* | `workflow-orchestrator` | `workflow-engine` | `quality-report.md` | Blocker |
| 11 | **COPIL / Go-No-Go** | `sdlc-steer-manager` | `sdlc-steer-governance` | `go-nogo-decision.md` | Blocker |

**Flow**: Scaffold → Project Init → BA Pipeline → Sprint Planning → Tech Pipeline → Implementation → Test Campaign → Performance → Sprint Tracking → Quality Validation → COPIL

**Output directory**: `docs/`

---

## Prompts (4)

<!-- UPDATE this table when adding/removing prompts in .apm/prompts/ -->

| Prompt | Purpose |
|--------|---------|
| `convert-md-to-docx-and-pdf` | Pandoc-based document conversion with branding |
| `create-one-pager` | Generate concise branded one-pagers |
| `soprasteria-brand-audit` | Comprehensive brand compliance audit |
| `soprasteria-brand-refactor` | Automated brand refactoring guidance |

Canonical definitions: `.apm/prompts/`. Copilot projection: `.github/prompts/` (4 standalone + 8 workflow prompts).

---

## Knowledge Base

| Directory | Content |
|-----------|---------|
| `knowledge/constitution/` | Principles, greenfield/brownfield rules, enterprise defaults, SpecKit constitution |
| `knowledge/governance/` | Architecture principles, security, testing, observability, schemas |
| `knowledge/playbooks/` | Workflow, greenfield, brownfield, modernization playbooks |
| `knowledge/brand/` | Brand guidelines (Sopra Steria) |

---

## Quick Start Guide

See [`docs/quick-start.md`](docs/quick-start.md) — a hands-on guide covering:

- **Install in 60 seconds** — one script, one command
- **Updating** — re-run the bootstrap
- **Hub Orchestrator** — the single entry point that routes you to the right workflow
- **Common workflows** — invocation table across all providers
- **Using agents directly** — key agents and when to use them
- **Per-provider usage** — GitHub Copilot, CLI, and Claude Code

---

## Concepts & Glossary

See [`docs/concepts.md`](docs/concepts.md) — explains each building block:

Agents, Workflows, Skills, Knowledge, Prompts, Instructions, Hooks, Templates, Contexts, Scripts — what they are, where to find them, and how they fit together.

---

## Provider Setup

### GitHub Copilot (three-layer)

- **Provider layer** (source of truth for Copilot-format files):
  - Agents: `providers/github-copilot/agents/*.agent.md` (7 agents)
  - Prompts: `providers/github-copilot/prompts/*.prompt.md` (5 standalone + 14 workflow + 26 SDLC)
  - Instructions: `providers/github-copilot/instructions/*.instructions.md` (6 files, with `applyTo` patterns)
  - Docs: `providers/github-copilot/conventions.md` + `sync-map.md`
- **Runtime projection** (generated — gitignored):
  - Run `.apm/scripts/powershell/project-copilot.ps1` to copy into `.github/`
  - Hub context: `.github/copilot-instructions.md` (not generated, lives directly in `.github/`)
- Consult `sync-map.md` for the full canonical → provider mapping.

### Claude Code

- Context file: `providers/claude-code/CLAUDE.md`
- Commands: `providers/claude-code/commands/*.md` (8 workflow + 31 SDLC + 1 hub)

### CLI

```bash
# Run a workflow
./providers/cli/run-workflow.sh feature-implementation my-feature

# Dry run
./providers/cli/run-workflow.sh quality-validation my-feature --dry-run

# Resume from last pass
./providers/cli/run-workflow.sh modernization spring-upgrade --resume

# Single station
./providers/cli/run-workflow.sh pr-validation my-branch --station a1-policy-validation
```

---

## PR Validation Pipeline

Every merge request triggers a **two-phase validation pipeline** (`.gitlab-ci.yml`).

### Pipeline Architecture

```text
merge_request_event
  │
  ├─ validate (parallel)                  ← Phase 1
  │   ├─ validate:pr-auto                  Python   ⛔ gates
  │   ├─ validate:yaml-workflows           Python   ⛔ gates
  │   └─ validate:test-gaps                Python   advisory
  │
  └─ stations (sequential)                ← Phase 2
      └─ stations:run-all
           A0 → A1 → A2 → … → A7
           Fails fast on any status: "fail"
```

### Stations (A0–A7)

| Station | Type | Purpose | Gate |
|---------|------|---------|------|
| A0 Intake | Prompt | PR metadata + work order | — |
| A1 Policy | Prompt | Frontmatter, tools, structure | Blocker |
| A2 Security | Prompt | Static security scanning | Blocker |
| A3 Prompt Injection | Prompt | Jailbreak + injection hardening | Blocker |
| A4 Red Team | Agent | Adversarial simulation | Advisory |
| A5 Sandbox | Prompt | Agent execution simulation | Blocker |
| A6 Policy Gate | Agent | Final decision across all reports | Blocker |
| A7 GitLab Update | Prompt | MR status update | Info |

Station implementations: `ci-gates/stations/`.
Schemas: `knowledge/governance/schemas/` (agent-manifest, skill-manifest).
Scripts: `ci-gates/scripts/` (orchestrator, extract, sanitize).

### Local Validation

```bash
# Deterministic validators
python .apm/skills/ai-backbone-pr-checks/tools/scripts/pr_auto_validator.py \
  --base-ref HEAD~1 --head-ref HEAD --out reports/pr-auto-validator.json
python .apm/skills/ai-backbone-pr-checks/tools/scripts/yaml_workflow_linter.py \
  --root . --out reports/yaml-workflow-linter.json
python .apm/skills/ai-backbone-pr-checks/tools/scripts/test_gap_detector.py \
  --base-ref HEAD~1 --head-ref HEAD --out reports/test-gap-detector.json

# Cross-layer validation
python scripts/validate_all.py

# Full pipeline via Podman
podman-compose up --build
```

### CI/CD Configuration (GitLab)

1. **Settings > CI/CD > Variables**: create masked `GITHUB_TOKEN` with Copilot CLI access
2. Set `ENABLE_COPILOT_CLI=true` to enable AI stations
3. The `stations:run-all` job authenticates via this token for A0–A7

---

## Cross-Layer Validation

Scripts in `scripts/` verify canonical ↔ projection consistency:

| Script | Purpose |
|--------|---------|
| `validate_core_assets.py` | Canonical `.apm/` layer completeness |
| `validate_copilot_assets.py` | Copilot projection sync with canonical |
| `validate_claude_assets.py` | Claude adapter sync with canonical |
| `validate_all.py` | Run all validators with summary |

---

## Distribution & Installation

APM bundles are built and distributed via the GitLab CI/CD pipeline. Two channels are available:

| Channel | Trigger | Use Case |
|---------|---------|----------|
| **Job Artifacts** | Every branch/tag push | Short-lived CI consumption, previews |
| **Package Registry** | Tag push (`v*`) | Versioned cross-project distribution |

The build stage runs `apm pack` for three targets: **copilot**, **claude**, and **all**. Tag pushes additionally publish versioned packages to the [GitLab Generic Package Registry](https://docs.gitlab.com/ee/user/packages/generic_packages/).

### Quick Start — Consumers

> **Hands-on guide**: See [`docs/quick-start.md`](docs/quick-start.md) for step-by-step install, usage with Hub Orchestrator, per-provider examples (Copilot, CLI, Claude Code), and how to use agents directly.
> **New to the concepts?** See [`docs/concepts.md`](docs/concepts.md) for an overview of agents, workflows, skills, and other building blocks.

You need a **GitLab Personal Access Token** (scopes: `read_api`, `read_registry`).
Create one at: GitLab → avatar → **Edit profile** → **Personal Access Tokens** → **Add new token** (scopes: `read_api`, `read_registry`).

**PowerShell (Windows):**

```powershell
$env:GITLAB_TOKEN = "glpat-xxxxxxxxxxxxxxxxxxxx"   # your token

# Download & run bootstrap
Invoke-WebRequest `
  -Uri "https://innersource.soprasteria.com/api/v4/projects/545119/repository/files/scripts%2Fbootstrap-apm.ps1/raw?ref=main" `
  -Headers @{ 'PRIVATE-TOKEN' = $env:GITLAB_TOKEN } -OutFile bootstrap-apm.ps1

.\bootstrap-apm.ps1 -Version 0.0.1

# Commit
git add .github/ .apm.lock.yaml
git commit -m "feat: install AI SDLC Foundation v0.0.1"
```

**Bash (Linux / macOS):**

```bash
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"   # your token

# Download & run bootstrap
curl --fail --silent \
  --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  -o bootstrap-apm.sh \
  "https://innersource.soprasteria.com/api/v4/projects/545119/repository/files/scripts%2Fbootstrap-apm.sh/raw?ref=main"
chmod +x bootstrap-apm.sh
./bootstrap-apm.sh --version 0.0.1

# Commit
git add .github/ .apm.lock.yaml
git commit -m "feat: install AI SDLC Foundation v0.0.1"
```

Then open Copilot and try `@hub-orchestrator` or `/workflow-feature`.

> **Quick start**: See [`docs/quick-start.md`](docs/quick-start.md) for hands-on install, usage, and per-provider examples.
> **Full guide**: See [`docs/apm-consumer-guide.md`](docs/apm-consumer-guide.md) for expandable mode, CI integration, customization, and updating.
> **Distribution details**: See [`docs/distribution.md`](docs/distribution.md) for registry, checksums, CI/CD pipeline examples, and troubleshooting.

---

## Prerequisites

| Tool | Version | Required For |
|------|---------|-------------|
| Python | 3.11+ | Validators, validation scripts |
| Git | 2.x+ | Diff generation, validation |
| Node.js | 20+ | Copilot CLI (AI stations), APM |
| APM CLI | latest | Bundle building and distribution |
| GitHub Copilot CLI | 1.0.4 | AI station execution |
| jq | 1.6+ | Gate enforcement |
| curl | — | Package registry publishing / consumption |
| Podman | — | Local pipeline execution (optional) |
| Pandoc | — | Brand Styler document conversion (optional) |

---

## Adding Capabilities

<!-- These checklists are the canonical self-maintenance protocol.
     Follow them exactly when extending the repository. -->

### New agent

1. Create `.apm/agents/<name>.md` (canonical, provider-agnostic)
2. Create `.github/agents/<name>.agent.md` (Copilot runtime, with frontmatter) — if user-facing
3. Update `providers/github-copilot/sync-map.md`
4. Update this README: **Agents table** (count in heading + new row)

### New skill

1. Create `.apm/skills/<name>/SKILL.md` (+ optional `tools/`, `docs/`)
2. Update this README: **Skills table** (count in heading + new row in correct category)

### New workflow

1. Create `.apm/workflows/<name>.yml` following `_schema.md`
2. Create `.github/prompts/workflow-<name>.prompt.md` (Copilot runtime)
3. Add provider commands: `providers/claude-code/commands/workflow-<name>.md`
4. Update `providers/github-copilot/sync-map.md`
5. Update this README: **Workflows section** (count in heading + detailed station table under correct category)

### New prompt

1. Create `.apm/prompts/<name>.md` (canonical)
2. Create `.github/prompts/<name>.prompt.md` (Copilot runtime)
3. Update `providers/github-copilot/sync-map.md`
4. Update this README: **Prompts table** (count in heading + new row)

### After any change

```bash
# Always run cross-layer validation after changes
python scripts/validate_all.py
```

### Self-Maintenance Checklist

When modifying this repository, update all affected sections:

- [ ] **Asset summary table** (top of README) — counts match actual files
- [ ] **Architecture diagram** — counts in the ASCII art match reality
- [ ] **Repository Layout table** — counts in parentheses are current
- [ ] **Section heading counts** — e.g., `## Agents (17)` matches actual agent count
- [ ] **Workflow detail tables** — station counts in headings match table rows
- [ ] **Provider Setup** — Copilot/Claude file counts are current
- [ ] **Cross-layer validation passes** — `python scripts/validate_all.py`

---

## Contributing

### From shared resources

1. Canonical definitions go in `.apm/` (agents, skills, prompts, workflows, templates, scripts)
2. Copilot runtime projections go in `.github/` (agents, prompts, instructions)
3. Adapter docs go in `providers/<provider>/` (conventions, sync-map, CLAUDE.md)
4. Brand assets live in `knowledge/brand/`
5. Open an MR targeting the `staged` branch

### From a client engagement

1. Create `clients/<client-name>/` with client-specific overrides
2. Open an MR — reusable items get promoted to `.apm/`

### Naming conventions

- **lowercase, hyphens**: `code-review.agent.md`, `brand-styler/SKILL.md`
- YAML frontmatter required: `name`, `description` (single-quoted)
- Copilot instructions need `applyTo` in frontmatter

---

## License

Internal Sopra Steria use. Consult your delivery lead for client-contributed content terms.
