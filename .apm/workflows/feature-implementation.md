# Workflow: Feature Implementation

End-to-end feature delivery from constitution through specification, planning, implementation, and quality validation.

## When to use

- Starting a new feature (greenfield or brownfield)
- Delivering a complete feature with specification, implementation, and quality assurance
- When the full spec-kit flow plus actual code generation and testing is needed
- Features requiring formal architecture review and capacity planning

## Stations

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 1 | Constitution | spec-orchestrator | spec-constitution | Constitution covers architecture, quality, security, testing, observability | blocker |
| 2 | Specification | spec-orchestrator | spec-feature | Scope and out-of-scope defined, acceptance criteria testable | blocker |
| 3 | Clarification | spec-orchestrator | spec-clarify | No unresolved blocker questions remain | blocker |
| 4 | Architecture Review | architecture-governance | architecture-guardrails | Architecture principles satisfied, no unmitigated high-risk concerns | blocker |
| 5 | Planning | spec-orchestrator | spec-plan | Risks identified with mitigations, rollout and rollback strategies defined | blocker |
| 6 | Task Breakdown | spec-orchestrator | spec-tasks | Tasks traceable to plan, testing tasks included | blocker |
| 7 | Implementation | implementer | code-implementation | Code compiles, tests pass, implementation log maintained | blocker |
| 8 | Quality Validation | workflow-orchestrator | workflow-engine | Nested quality-validation workflow passes all gates | blocker |
| 9 | Final Quality Gate | spec-orchestrator | spec-quality-gate | Package complete and coherent, all artifacts linked | blocker |

## Nested workflow

Station 8 invokes the `quality-validation` workflow as a nested sub-workflow. The workflow-orchestrator loads `quality-validation.yml` and runs all its stations (lint, static analysis, SAST, dependency audit, coverage, DAST, report).

## Outputs

All artifacts are written to `outputs/specs/features/<feature>/`:
- `constitution.md` — foundational principles and constraints
- `spec.md` — feature specification with acceptance criteria
- `clarifications.md` — resolved questions and edge cases
- `architecture-review.md` — governance review outcome
- `plan.md` — implementation plan with risk mitigations
- `tasks.md` — task breakdown traceable to plan
- `implementation-log.md` — code generation and changes record
- `quality-report.md` — from nested quality-validation (aggregated lint, static, SAST, dependency, coverage, DAST)
- `quality-gate.md` — final sign-off

## Brownfield variant

For brownfield features, a reverse brief may be generated during a pre-station step using the `brownfield-context` skill to document current-state constraints and do-not-break rules.

## Key differences from spec-kit

- Includes Implementation station (station 7) — spec-kit stops after specification
- Includes nested quality-validation station (station 8) — spec-kit does not validate code
- No explicit test-strategy station — testing is covered in quality-validation
- 9 stations total (spec-kit has 8, with test-strategy instead of implementation + quality)
