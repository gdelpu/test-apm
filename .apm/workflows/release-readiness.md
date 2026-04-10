# Workflow: Release Readiness

Validate that a feature meets all release criteria across spec completeness, testing, security, observability, and deployment.

## When to use

- Before releasing a feature to production
- As a final validation gate after implementation is complete
- When stakeholders need a Go/No-Go decision
- Compliance or governance requires a release checklist

## Prerequisites

Expects a completed implementation with these artifacts in `outputs/specs/features/<feature>/`:
- `spec.md`, `clarifications.md`, `plan.md`, `tasks.md`
- `test-strategy.md`, `nfr-review.md` (recommended)
- `rollout-strategy.md`, `implementation-log.md`

## Stations

| # | Station | Agent | Skills | Gate | Severity |
|---|---------|-------|--------|------|----------|
| 1 | Spec Completeness | spec-orchestrator | spec-quality-gate | Spec coherent, clarifications resolved | blocker |
| 2 | Test Completeness | quality-validator | coverage-assessment, test-strategy | Coverage met, critical paths tested | blocker |
| 3 | Security Validation | quality-validator | security-scan, dependency-audit | No critical vulns or CVEs | blocker |
| 4 | Observability Readiness | architecture-governance | observability-readiness, nfr-review | Logging, metrics, alerting, tracing defined | blocker |
| 5 | Deployment Readiness | spec-orchestrator | spec-quality-gate | Rollback tested, config defined | blocker |
| 6 | Go / No-Go Decision | spec-orchestrator | spec-quality-gate, quality-report | All criteria met → release approved | blocker |

## Outputs

All artifacts are written to `outputs/specs/features/<feature>/`:
- `spec-completeness.md` — Spec coherence evaluation
- `test-completeness.md` — Test coverage and acceptance criteria mapping
- `security-report.md` — SAST + dependency audit results
- `observability-report.md` — Logging, metrics, alerting, tracing assessment
- `deployment-readiness.md` — Deployment and rollback readiness
- `release-decision.md` — Go/No-Go decision with rationale

## Composition

Follows `implementation-loop`. Can also be nested inside `feature-implementation` or invoked standalone.

## Key differences from quality-validation

- Broader scope: covers spec, observability, deployment — not just code quality
- Includes a Go/No-Go decision station
- Validates rollback and deployment procedures
- Focuses on release readiness, not just code health
