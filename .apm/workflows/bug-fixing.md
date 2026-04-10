# Workflow: Bug Fixing

Structured bug resolution from triage through root-cause analysis, fix implementation, regression testing, and quality validation.

## When to use

- Fixing reported bugs with structured diagnosis and evidence
- When root-cause analysis and regression coverage are required before closing
- When fix needs documented justification and rollback readiness
- Ensuring fixes don't introduce new regressions

## Stations

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 1 | Triage | spec-orchestrator | spec-clarify | Severity, priority, components identified, reproduction steps documented | blocker |
| 2 | Reproduce | implementer | code-implementation | Bug reliably reproduced, environment recorded | blocker |
| 3 | Root Cause Analysis | spec-orchestrator | repo-analysis | Root cause identified with evidence, impact scope assessed | blocker |
| 4 | Fix Implementation | implementer | code-implementation | Fix addresses root cause, code compiles, existing tests pass | blocker |
| 5 | Regression Testing | implementer | code-implementation | Regression test added, all tests pass, original issue resolved | blocker |
| 6 | Quality Validation | workflow-orchestrator | workflow-engine | Nested quality-validation passes all gates | blocker |
| 7 | Close | spec-orchestrator | adr-generation | Fix documented with decision record and justification | blocker |

## Nested workflow

Station 6 invokes the `quality-validation` workflow as a nested sub-workflow for comprehensive quality checks on the fix.

## Outputs

All artifacts are written to `outputs/specs/features/<feature>/`:
- `triage.md` — severity, priority, affected components
- `reproduction-log.md` — how to reproduce the bug
- `root-cause.md` — root cause analysis with evidence
- `fix-log.md` — fix implementation details
- `regression-report.md` — regression test coverage
- `quality-report.md` — from nested quality-validation
- `decision.md` — fix justification and decision record

## Key differences from feature-implementation

- Starts with bug report triage, not greenfield specification
- Includes explicit root-cause analysis requiring evidence
- Regression testing is a mandatory station
- No architecture review (assumes existing system)
- Includes decision record on the fix approach
- Shorter total flow (7 stations vs. 9 in feature-implementation)
