# Workflows (19)

> YAML-defined pipelines of sequential **stations**, each assigned to an **agent** with specific **skills**. Every station has a **quality gate** with pass/fail criteria. Workflows support resume, skip-gate (where configured), and nesting.

Schema reference: `.apm/workflows/_schema.md`.

---

## Delivery Workflows

Workflows that drive end-to-end feature or fix delivery from specification through implementation and quality validation.

---

### `feature-implementation` (10 stations)

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

**Output directory**: `outputs/specs/features/<feature>/`

---

### `modernization` (10 stations)

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

**Output directory**: `outputs/specs/features/<feature>/`

---

### `bug-fixing` (7 stations)

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

**Output directory**: `outputs/specs/bugs/<bug-id>/`

---

### `incident-resolution` (7 stations)

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

**Output directory**: `outputs/specs/features/<feature>/`

---

### `bmad` (4 stations)

> Build-Measure-Analyze-Decide feedback loop for hypothesis-driven delivery.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Build** | `implementer` | `code-implementation` | `build-log.md` | Blocker |
| 2 | **Measure** | `quality-validator` | `coverage-assessment` | `metrics.md` | Blocker |
| 3 | **Analyze** | `spec-orchestrator` | `spec-clarify` | `analysis.md` | Blocker |
| 4 | **Decide** | `spec-orchestrator` | `adr-generation` | `decision.md` | Blocker |

**Flow**: Build → Measure → Analyze → Decide (iterate)

**Output directory**: `outputs/specs/features/<feature>/`

---

### `implementation-loop` (6 stations)

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

**Output directory**: `outputs/specs/features/<feature>/`

---

## Specification Workflows

Workflows that focus on producing validated specification artifacts without implementation.

---

### `idea-to-spec` (7 stations)

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

**Output directory**: `outputs/specs/features/<feature>/`

---

### `spec-kit` (8 stations)

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

**Output directory**: `outputs/specs/features/<feature>/`

---

### `spec-to-execution` (6 stations)

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

**Output directory**: `outputs/specs/features/<feature>/`

---

## Validation Workflows

Workflows that validate quality, security, compliance, or release readiness. Can be nested inside delivery workflows.

---

### `quality-validation` (7 stations)

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

### `pr-validation` (11 stations)

> Multi-stage merge request validation pipeline with deterministic checks and AI-powered security stations.

**Phase 1 — Deterministic validators (parallel)**:

| # | Station | Agent | Skills | Outputs | Gate Severity | Parallel |
|---|---------|-------|--------|---------|---------------|----------|
| 1 | **PR Auto Validator** | `pr-validator` | `ai-backbone-pr-checks` | `outputs/reports/pr-auto-validator.json` | Blocker | ✅ |
| 2 | **YAML Workflow Linter** | `pr-validator` | `ai-backbone-pr-checks` | `outputs/reports/yaml-workflow-linter.json` | Blocker | ✅ |
| 3 | **Test Gap Detector** *(optional)* | `pr-validator` | `ai-backbone-pr-checks` | `outputs/reports/test-gap-detector.json` | Warning | ✅ |

**Phase 2 — AI stations (sequential)**:

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 4 | **A0 Intake** | `station-orchestrator` | — | `outputs/station_out/work_order.json` | Warning |
| 5 | **A1 Policy Validation** | `station-orchestrator` | `soprasteria-agent-policy-guard` | `outputs/station_out/policy_report.json` | Blocker |
| 6 | **A2 Security Static** | `station-orchestrator` | `secret-scan` | `outputs/station_out/security_report.json` | Blocker |
| 7 | **A3 Prompt Injection** | `station-orchestrator` | `injection-detection` | `outputs/station_out/promptsec_report.json` | Blocker |
| 8 | **A4 Red Team** *(optional)* | `station-orchestrator` | `red-team-simulation` | `outputs/station_out/a4_result.json` | Warning |
| 9 | **A5 Sandbox Simulation** | `station-orchestrator` | `sandbox-execution` | `outputs/station_out/sim_report.json` | Blocker |
| 10 | **A6 Policy Gate** | `station-orchestrator` | `policy-gate` | `outputs/station_out/gate_decision.json` | Blocker |
| 11 | **A7 Platform Update** *(optional)* | `station-orchestrator` | — | — | Warning |

**Flow**: PR Auto ∥ YAML Lint ∥ Test Gaps → A0 → A1 → A2 → A3 → A4 → A5 → A6 → A7

**Nestable**: Yes — can be embedded in delivery workflows.

---

### `compliance-check` (6 stations)

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

**Output directory**: `outputs/specs/features/<feature>/`

---

### `release-readiness` (6 stations)

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

**Output directory**: `outputs/specs/features/<feature>/`

---

## Assessment Workflows

Workflows that assess maturity, patterns, and process health without producing implementation artifacts.

---

### `maturity-assessment` (4 stations)

> Assess SDLC maturity across dimensions and produce a scored report with improvement roadmap.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Maturity Assessment** | `repository-analyzer` | `repo-analysis` | `assessment.md` | Blocker |
| 2 | **Scoring** | `spec-orchestrator` | `spec-clarify` | `scores.md` | Blocker |
| 3 | **Maturity Report** | `spec-orchestrator` | `spec-feature` | `maturity-report.md` | Blocker |
| 4 | **Improvement Roadmap** | `spec-orchestrator` | `spec-plan` | `roadmap.md` | Blocker |

**Flow**: Assessment → Scoring → Report → Roadmap

**Output directory**: `outputs/specs/assessments/<assessment-id>/`

---

### `delivery-retrospective` (5 stations)

> AI-native continuous improvement cycle analyzing delivery metrics, defects, bottlenecks, and producing actionable improvements.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Analyze Cycle Time** | `spec-orchestrator` | `delivery-metrics` | `cycle-time-report.md` | Warning |
| 2 | **Analyze Defects** | `spec-orchestrator` | `delivery-metrics`, `quality-report` | `defect-report.md` | Warning |
| 3 | **Identify Bottlenecks** | `spec-orchestrator` | `delivery-metrics` | `bottleneck-report.md` | Warning |
| 4 | **Suggest Improvements** | `architecture-governance` | `architecture-guardrails`, `delivery-metrics` | `improvement-proposals.md` | Warning |
| 5 | **Update Constitution / Playbooks** | `spec-orchestrator` | `knowledge-update`, `adr-generation` | `retrospective-actions.md` | Warning |

**Flow**: Cycle Time Analysis → Defect Analysis → Bottleneck Identification → Improvement Suggestions → Constitution/Playbook Update

**Output directory**: `outputs/specs/features/<feature>/`

---

## SDLC Harness Workflows

Workflows migrated from the SDLC Agentic Harness. They provide a prescriptive, deliverable-driven methodology with DAG-based orchestration, fan-out/fan-in patterns, and cross-domain traceability. Can be nested inside other delivery workflows.

---

### `sdlc-ba` (16 stations)

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

**Output directory**: `outputs/ba/`

---

### `sdlc-tech` (12 stations)

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

**Output directory**: `outputs/tech/`

---

### `sdlc-steer` (10 stations)

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

**Output directory**: `outputs/steer/`

---

### `sdlc-full` (11 stations)

> Composite SDLC pipeline orchestrating all domains end-to-end: scaffold → BA → Tech → Test → Steer governance.

| # | Station | Agent | Skills | Outputs | Gate Severity |
|---|---------|-------|--------|---------|---------------|
| 1 | **Scaffold** | `sdlc-coordinator` | `sdlc-scaffold` | `outputs/docs/project.yml` | Blocker |
| 2 | **Project Init** | `sdlc-steer-manager` | `sdlc-steer-init` | `project-sheet.md`, `kpi-baseline.md` | Blocker |
| 3 | **BA Pipeline** *(nested)* | `sdlc-ba-analyst` | `sdlc-ba-*` | `outputs/ba/` | Blocker |
| 4 | **Sprint Planning** | `sdlc-steer-manager` | `sdlc-steer-planning` | `sprint-plan.md`, `roadmap.md` | Blocker |
| 5 | **Tech Pipeline** *(nested)* | `sdlc-tech-architect` | `sdlc-tech-*` | `outputs/tech/` | Blocker |
| 6 | **Implementation** | `implementer` | `code-implementation` | implementation artifacts | Blocker |
| 7 | **Test Campaign** | `sdlc-test-executor` | `sdlc-test-campaign` | `test-campaign-report.md` | Blocker |
| 8 | **Performance Tests** | `sdlc-test-executor` | `sdlc-test-performance` | `perf-report.md` | Blocker |
| 9 | **Sprint Tracking** *(nested)* | `sdlc-steer-manager` | `sdlc-steer-sprint` | sprint metrics | Warning |
| 10 | **Quality Validation** *(nested)* | `workflow-orchestrator` | `workflow-engine` | `quality-report.md` | Blocker |
| 11 | **COPIL / Go-No-Go** | `sdlc-steer-manager` | `sdlc-steer-governance` | `go-nogo-decision.md` | Blocker |

**Flow**: Scaffold → Project Init → BA Pipeline → Sprint Planning → Tech Pipeline → Implementation → Test Campaign → Performance → Sprint Tracking → Quality Validation → COPIL

**Output directory**: `outputs/`
