# Workflow: Feature Implementation

End-to-end feature delivery from constitution through specification, planning, implementation, and quality validation. Supports both brownfield (existing system) and greenfield (new) projects.

## When to use

- Starting a new feature (greenfield or brownfield)
- Delivering a complete feature with specification, implementation, and quality assurance
- When the full spec-kit flow plus actual code generation and testing is needed
- Brownfield feature work requiring context extraction and constraint mapping before specification
- Features requiring formal architecture review and capacity planning

## Stations

| # | Station | Agent | Skill | Gate | Severity | Condition |
|---|---------|-------|-------|------|----------|-----------|
| 1 | Constitution | spec-orchestrator | spec-constitution | Constitution covers architecture, quality, security, testing, observability | blocker | always |
| 2 | Brownfield Context | spec-orchestrator | brownfield-context | Existing architecture, patterns, and constraints documented | blocker | brownfield only |
| 3 | Specification | spec-orchestrator | spec-feature | Scope and out-of-scope defined, acceptance criteria testable | blocker | always |
| 4 | Clarification | spec-orchestrator | spec-clarify | No unresolved blocker questions remain | blocker | always |
| 5 | Architecture Review | architecture-governance | architecture-guardrails | Architecture principles satisfied, no unmitigated high-risk concerns | blocker | always |
| 6 | Planning | spec-orchestrator | spec-plan | Risks identified with mitigations, rollout and rollback strategies defined | blocker | always |
| 7 | Task Breakdown | spec-orchestrator | spec-tasks | Tasks traceable to plan, testing tasks included | blocker | always |
| 8 | Implementation | implementer | code-implementation | Code compiles, tests pass, implementation log maintained | blocker | always |
| 9 | Quality Validation | workflow-orchestrator | workflow-engine | Nested quality-validation workflow passes all gates | blocker | always |
| 10 | Final Quality Gate | spec-orchestrator | spec-quality-gate | Package complete and coherent, all artifacts linked | blocker | always |

## Brownfield vs Greenfield

The workflow adapts based on project context:

- **Greenfield**: Station 2 (Brownfield Context) is skipped. Constitution uses greenfield template. Specification starts from a clean slate.
- **Brownfield**: Station 2 extracts existing codebase architecture, patterns, constraints, and domain terms into `context-brief.md`. The specification station receives this as input to ensure the spec respects existing constraints and backward compatibility.

## Nested workflow

Station 8 invokes the `quality-validation` workflow as a nested sub-workflow. The workflow-orchestrator loads `quality-validation.yml` and runs all its stations (lint, static analysis, SAST, dependency audit, coverage, DAST, report).

## Outputs

All artifacts are written to `outputs/specs/features/<feature>/`:
- `constitution.md` — foundational principles and constraints
- `context-brief.md` — existing codebase context and constraints (brownfield only)
- `spec.md` — feature specification with acceptance criteria
- `clarifications.md` — resolved questions and edge cases
- `architecture-review.md` — governance review outcome
- `plan.md` — implementation plan with risk mitigations
- `tasks.md` — task breakdown traceable to plan
- `implementation-log.md` — code generation and changes record
- `quality-report.md` — from nested quality-validation (aggregated lint, static, SAST, dependency, coverage, DAST)
- `quality-gate.md` — final sign-off

## Brownfield variant

For brownfield features, the conditional brownfield-context station (station 2) extracts current-state constraints and do-not-break rules into `context-brief.md`. This feeds into the specification station to ensure backward compatibility.

## Key differences from spec-kit

- Includes Implementation station — spec-kit stops after specification
- Includes nested quality-validation station — spec-kit does not validate code
- No explicit test-strategy station — testing is covered in quality-validation
- 10 stations total (9 for greenfield, 10 for brownfield; spec-kit has 9 with test-strategy instead of implementation + quality)
