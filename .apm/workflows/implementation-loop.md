# Workflow: Implementation Loop

Agent-assisted development loop from task selection through code generation, review, testing, and commit readiness.

## When to use

- Executing tasks from a `spec-to-execution` output
- Agent-assisted coding with built-in self-review and quality checks
- Iterative development where each task goes through a complete cycle
- When you want lightweight quality validation without the full quality-validation workflow

## Prerequisites

Expects these artifacts to already exist in `outputs/specs/features/<feature>/`:
- `tasks.md` — Decomposed, sequenced tasks
- `plan.md` — Implementation plan

## Stations

| # | Station | Agent | Skills | Gate | Severity |
|---|---------|-------|--------|------|----------|
| 1 | Task Selection | implementer | code-implementation | Prerequisites met, scope clear | blocker |
| 2 | Code Generation | implementer | code-implementation | Compiles, scope respected | blocker |
| 3 | Self-Review | implementer | code-implementation, lint-analysis | No smells, style followed, no vulns | warning |
| 4 | Test Generation | implementer | code-implementation, coverage-assessment | Acceptance criteria covered | blocker |
| 5 | Local Validation | quality-validator | lint-analysis, coverage-assessment | Build + tests + coverage pass | blocker |
| 6 | Commit Readiness | implementer | code-implementation | All gates passed, commit ready | blocker |

## Outputs

All artifacts are written to `outputs/specs/features/<feature>/`:
- `current-task.md` — Selected task context
- `implementation-log.md` — Code changes and decisions
- `review-notes.md` — Self-review findings
- `test-log.md` — Test generation results
- `validation-report.md` — Lint, build, test, coverage results
- `commit-summary.md` — Summary for commit message

## Iteration

This workflow processes one task at a time. For multiple tasks, invoke it iteratively — the workflow-orchestrator handles task sequencing via `--resume`.

## Composition

Follows `spec-to-execution`. For full quality validation before release, chain with `release-readiness`.

## Key differences from feature-implementation

- Focused on the dev loop only — no spec or planning stations
- Self-review station provides immediate agent feedback
- Lightweight quality (lint + coverage) instead of the full quality-validation workflow
- Produces commit-ready output for each task iteration
