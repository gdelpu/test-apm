# Workflow: Spec to Execution

Transform a validated specification into an executable plan with risk analysis, rollback strategy, and decomposed tasks.

## When to use

- After `idea-to-spec` produces a validated spec
- When a specification exists and needs to be turned into implementable tasks
- Planning sprints or iterations from an approved spec
- When risk analysis and rollback strategy are required before development

## Prerequisites

Expects these artifacts to already exist in `outputs/specs/features/<feature>/`:
- `spec.md` — Feature specification
- `clarifications.md` — Resolved ambiguities
- `architecture-review.md` — Architecture assessment
- `nfr-review.md` — Non-functional requirements (optional, used if present)

## Stations

| # | Station | Agent | Skills | Gate | Severity |
|---|---------|-------|--------|------|----------|
| 1 | Plan Generation | spec-orchestrator | spec-plan | Requirements addressed, risks identified | blocker |
| 2 | Risk Analysis | architecture-governance | architecture-guardrails, nfr-review | High risks mitigated, residual risk accepted | blocker |
| 3 | Rollout / Rollback | spec-orchestrator | spec-plan | Rollout + rollback procedures defined | blocker |
| 4 | Task Decomposition | spec-orchestrator | spec-tasks | Tasks traceable, acceptance criteria defined | blocker |
| 5 | Test Strategy | spec-orchestrator | test-strategy | Test levels + coverage expectations stated | warning |
| 6 | Execution Readiness | spec-orchestrator | spec-quality-gate | All readiness criteria met | blocker |

## Outputs

All artifacts are written to `outputs/specs/features/<feature>/`:
- `plan.md` — Implementation plan with dependencies
- `risk-analysis.md` — Risk register with mitigations
- `rollout-strategy.md` — Rollout and rollback procedures
- `tasks.md` — Decomposed, sequenced tasks
- `test-strategy.md` — Test levels, coverage, NFR validation
- `execution-readiness.md` — Readiness gate evaluation

## Composition

Follows `idea-to-spec` and precedes `implementation-loop` in the composable pipeline.

## Key differences from feature-implementation

- Dedicated risk analysis station with governance reviewer
- Explicit rollout/rollback definition as a separate station
- Stops before implementation — produces a ready-to-execute task package
- Execution readiness gate ensures the full package is implementable
