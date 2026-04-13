# Agents (23)

> Provider-agnostic agent definitions that pair with one or more skills to perform a role in workflows.

Canonical definitions: `.apm/agents/`. Copilot runtime projection: `.github/agents/` (7 user-facing agents).

---

<!-- UPDATE this table when adding/removing agents in .apm/agents/ -->

| Agent | Description | Key Skills |
|-------|-------------|------------|
| `analysis-agent` | Diagnose production incidents by reconstructing timelines, analyzing logs/traces, identifying affected services, and forming root-cause hypotheses | `incident-analysis`, `root-cause-analysis`, `repo-analysis`, `bug-reproduction` |
| `architecture-governance` | Review specifications and plans against architecture principles, NFRs, and delivery guardrails | — |
| `bmad-orchestrator` | Drive the BMAD (Build → Measure → Analyze → Decide) feedback loop with evaluation scoring and adaptive decision-making | `iteration-scoring`, `drift-detection`, `adaptive-decision` |
| `branding` | Audit, refactor, and generate brand-compliant applications, documents, and presentations. Default brand: Sopra Steria | `brand-core`, `brand-assets`, `brand-app`, `brand-document`, `brand-accessibility`, `brand-audit`, `docx`, `pptx`, `pdf`, `office-common` |
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
| `spec-orchestrator` | Lead structured, specification-driven flows for software changes and new initiatives | `brownfield-context`, `spec-constitution`, `spec-feature`, `spec-clarify`, `spec-plan`, `spec-tasks`, `spec-quality-gate`, `adr-generation`, `test-strategy`, `nfr-review`, `architecture-guardrails` |
| `workflow-orchestrator` | Execute workflow definitions by driving stations sequentially, evaluating quality gates, and managing workflow state | `workflow-engine` |
| `sdlc-coordinator` | Orchestrate the full SDLC lifecycle — DAG resolution, wave scheduling, fan-out/fan-in, gate management across BA/Tech/Steer/Test domains | All `sdlc-*` skills |
| `sdlc-ba-analyst` | Business analysis from brownfield audit through scoping, specification, and per-feature functional design | `sdlc-ba-audit`, `sdlc-ba-scoping`, `sdlc-ba-specification`, `sdlc-ba-functional-design` |
| `sdlc-tech-architect` | Technical architecture from audit through ADR fan-out, design, and continuous quality | `sdlc-tech-audit`, `sdlc-tech-architecture`, `sdlc-tech-design`, `sdlc-tech-quality` |
| `sdlc-steer-manager` | Steering and project management across initialization, planning, sprint tracking, and governance | `sdlc-steer-init`, `sdlc-steer-planning`, `sdlc-steer-sprint`, `sdlc-steer-governance` |
| `sdlc-test-executor` | Test execution for E2E/UAT campaigns and performance testing | `sdlc-test-campaign`, `sdlc-test-performance` |

---

## Spotlight: Branding Agent

The **`branding`** agent is designed for standalone use in any project — no workflow required. Point it at an application, document, or presentation and it will audit brand compliance, refactor styling, generate design tokens, or convert Markdown into branded DOCX/PDF files. It ships with full Office document manipulation capabilities: create and edit Word documents (tracked changes, comments), build PowerPoint decks from scratch or from templates, process PDFs (merge, split, fill forms), and validate OOXML output — all via the `docx`, `pptx`, `pdf`, and `office-common` skills.

**Default brand: Sopra Steria.** Out of the box the agent loads the official Sopra Steria visual identity — colours, typography, logo rules, PowerPoint/Word templates, and WCAG 2.1 AA contrast matrix — from `.apm/knowledge/brand/soprasteria/`. The brand is extensible: add a `.apm/knowledge/brand/<client>/` directory with client-specific assets and the agent adapts automatically.

> **Quick start**: `@branding audit this application for brand compliance` or `@branding convert docs/spec.md to a branded Word document`.
