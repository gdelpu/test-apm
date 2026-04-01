# Workflow: Modernization

Guided modernization from baseline assessment through staged migration, implementation, parity validation, and quality assurance.

## When to use

- Upgrading frameworks, languages, or platforms in existing systems
- Migrating from legacy to modern architecture
- Major code refactoring with formal assessment and ADR-driven decisions
- Any brownfield work requiring migration safety, rollback readiness, and coexistence planning
- Technology stack transitions (e.g., Spring Boot 2 → 3, Java 8 → 21, monolith → microservices)

## Stations

| # | Station | Agent | Skills | Gate | Severity |
|---|---------|-------|--------|------|----------|
| 1 | Baseline Assessment | modernization-agent | repo-analysis | Reverse brief covers current-state snapshot, affected modules identified, do-not-break constraints listed | blocker |
| 2 | Architecture Decisions | modernization-agent | adr-generation | ADRs capture all significant decisions with rationale and consequences | blocker |
| 3 | Target State | modernization-agent | spec-feature | Target state defined, acceptance criteria testable | blocker |
| 4 | Architecture Review | architecture-governance | architecture-guardrails | Migration approach satisfies principles, coexistence strategy viable | blocker |
| 5 | Migration Plan | modernization-agent | spec-plan | Rollback path for every stage, data migration risks addressed, critical path identified | blocker |
| 6 | Risk Clarification | modernization-agent | spec-clarify | All blockers mitigated, compatibility risks resolved, spikes identified | blocker |
| 7 | Task Breakdown | modernization-agent | spec-tasks | Sequenced tasks with verification checklists and rollback procedures | blocker |
| 8 | Implementation | modernization-agent | code-implementation | Code compiles, tests pass, migration record maintained | blocker |
| 9 | Parity Validation | modernization-agent | spec-clarify | No critical parity violations between old and new systems | warning |
| 10 | Quality Validation | workflow-orchestrator | workflow-engine | Nested quality-validation passes all gates | blocker |

## Nested workflow

Station 10 invokes the `quality-validation` workflow as a nested sub-workflow for comprehensive quality checks on the modernized code.

## Outputs

All artifacts are written to `specs/features/<feature>/`:
- `reverse-brief.md` — baseline assessment with current-state snapshot and constraints
- `decisions.md` — architecture decision summary (detailed ADRs in `refactor/docs/adr/`)
- `spec.md` — target state specification
- `architecture-review.md` — governance review and approval
- `plan.md` — phased migration plan with dependency graph and rollback procedures
- `clarifications.md` — resolved risks, compatibility issues, spike outcomes
- `tasks.md` — sequenced task breakdown with verification checkpoints
- `implementation-log.md` — migration execution record with coexistence notes
- `parity-report.md` — old vs. new system behavior comparison (optional)
- `quality-report.md` — from nested quality-validation

## Key strategy

**Coexistence approach**: Modern and legacy systems run in parallel during transition. Each task includes:
- Deployment step (feature flag or dual deployment)
- Verification against legacy system
- Rollback procedure if verification fails

**Data migration**: Separate task sequence for data schema/content migration with validation checkpoints.

## Key differences from feature-implementation

- Starts with comprehensive codebase assessment (14 items) instead of greenfield constitution
- Includes ADR-driven decision capture station (station 2)
- Migration stages drive planning (station 5 captures rollback and coexistence)
- Risk clarification focuses on compatibility and migration-specific concerns (station 6)
- Includes optional parity validation station for old vs. new comparison (station 9)
- 10 stations total (vs. 9 in feature-implementation)
- Longer cycle due to coexistence requirements and parity validation
