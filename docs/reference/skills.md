# Skills (94)

> Reusable knowledge and tool packages. Each skill has a `SKILL.md` manifest + optional `tools/` and `docs/` directories.

Canonical definitions: `.apm/skills/<name>/SKILL.md`.

---

<!-- UPDATE this table when adding/removing skills in .apm/skills/ -->

## Orchestration Skills

| Skill | Description |
|-------|-------------|
| `hub-classification` | Classify user intent against available workflows and agents, then recommend the best match for dispatch |

## SDLC & Specification Skills

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

## Architecture & Design Skills

| Skill | Description |
|-------|-------------|
| `architecture-guardrails` | Validate against architecture principles and delivery guardrails |
| `domain-driven-design` | DDD patterns and bounded-context modelling |
| `docs-architect` | Documentation architecture and structure |

## Implementation Skills

| Skill | Description |
|-------|-------------|
| `code-implementation` | Produce or modify code following project constraints and standards |
| `code-refactoring` | General code refactoring patterns |
| `code-refactoring-refactor-clean` | Clean refactoring techniques |
| `code-refactoring-tech-debt` | Technical debt reduction strategies |

## Quality & Validation Skills

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

## .NET Skills

| Skill | Description |
|-------|-------------|
| `dotnet-architect` | .NET architecture patterns and decisions |
| `dotnet-backend` | .NET backend development |
| `dotnet-backend-patterns` | .NET backend design patterns |

## React & Frontend Skills

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

## API Skills

| Skill | Description |
|-------|-------------|
| `api-design-principles` | API design principles and standards |
| `api-documentation` | API documentation generation |
| `api-patterns` | API implementation patterns |
| `api-security-best-practices` | API security hardening |

## Claude Code Skills

| Skill | Description |
|-------|-------------|
| `cc-skill-backend-patterns` | Claude Code backend development patterns |
| `cc-skill-coding-standards` | Claude Code coding standards |
| `cc-skill-frontend-patterns` | Claude Code frontend development patterns |

## Branding & Accessibility Skills

| Skill | Description |
|-------|-------------|
| `brand-core` | Core brand guidelines, colour/typography rules (default: Sopra Steria) |
| `brand-assets` | Brand asset discovery, inventory, and template management |
| `brand-app` | Application branding audit and refactoring |
| `brand-document` | Document branding and Pandoc-based DOCX/PDF generation |
| `brand-accessibility` | WCAG 2.1 AA validation for web applications |
| `brand-audit` | Compliance audit checklists |
| `docx` | Word document creation (docx-js), editing (XML unpack/repack), tracked changes, comments |
| `pptx` | PowerPoint creation (pptxgenjs), editing (XML unpack/repack), thumbnailing |
| `pdf` | PDF reading, merging, splitting, form filling, creation |
| `xlsx` | Excel creation (openpyxl), formulas, recalculation via LibreOffice |
| `office-common` | Shared OOXML pack/unpack/validate/convert utilities for docx/pptx/xlsx |
| `soprasteria-agent-policy-guard` | Shift-left policy enforcement (A1–A6 rules) |

## SDLC Harness Skills

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
