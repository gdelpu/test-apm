# Workflow: Spec Kit

Specification-only pipeline producing a complete spec package without implementation or code validation. Supports both brownfield (existing system) and greenfield (new) projects.

## When to use

- When only specification artifacts are needed (no code generation)
- Preparing a spec package for manual implementation or external team handoff
- When the full feature-implementation workflow is too broad
- Greenfield scoping that requires formal gates before committing to implementation
- Brownfield specification requiring context extraction and constraint mapping before spec authoring
- Creating a detailed roadmap or RFP document for contracted work

## Stations

| # | Station | Agent | Skill | Gate | Severity | Condition |
|---|---------|-------|-------|------|----------|-----------|
| 1 | Constitution | spec-orchestrator | spec-constitution | Constitution covers architecture, quality, security, testing, observability | blocker | always |
| 2 | Brownfield Context | spec-orchestrator | brownfield-context | Existing architecture, patterns, and constraints documented | blocker | brownfield only |
| 3 | Feature Specification | spec-orchestrator | spec-feature | Scope and out-of-scope defined, acceptance criteria testable | blocker | always |
| 4 | Clarification | spec-orchestrator | spec-clarify | No unresolved blocker questions | blocker | always |
| 5 | Architecture Review | architecture-governance | architecture-guardrails | Architecture principles satisfied, no unmitigated high-risk concerns | blocker | always |
| 6 | Planning | spec-orchestrator | spec-plan | Risks identified with mitigations, rollout and rollback strategies defined | blocker | always |
| 7 | Task Breakdown | spec-orchestrator | spec-tasks | Tasks traceable to plan, verification steps included | blocker | always |
| 8 | Test Strategy | spec-orchestrator | test-strategy | Test levels (unit/integration/e2e) and coverage targets stated | warning | always |
| 9 | Quality Gate | spec-orchestrator | spec-quality-gate | Package complete, coherent, and self-contained | blocker | always |

## Brownfield vs Greenfield

The workflow adapts based on project context:

- **Greenfield**: Station 2 (Brownfield Context) is skipped. Constitution uses greenfield template. Specification starts from a clean slate.
- **Brownfield**: Station 2 extracts existing codebase architecture, patterns, constraints, and domain terms into `context-brief.md`. The specification station receives this as input to ensure the spec respects existing constraints and backward compatibility.

## Outputs

All artifacts are written to `outputs/specs/features/<feature>/`:
- `constitution.md` — foundational principles and constraints
- `context-brief.md` — existing codebase context and constraints (brownfield only)
- `spec.md` — feature specification with acceptance criteria
- `clarifications.md` — resolved questions and edge cases
- `architecture-review.md` — governance review outcome
- `plan.md` — implementation plan with risk mitigations
- `tasks.md` — task breakdown from plan
- `test-strategy.md` — testing approach and coverage targets
- `quality-gate.md` — specification package sign-off

## Key characteristics

- **No code generation** — outputs are pure specification documents
- **No quality validation** — no linting, SAST, or dependency checks (no code exists yet)
- **Brownfield-aware** — conditional station extracts existing codebase context before specification
- **Test strategy focus** — explicit station for test planning to help downstream implementation
- **Specification-only gate** — final gate is coherence and completeness of documents, not code metrics

## Differences from feature-implementation

- No implementation station — stops after specification package
- No nested quality-validation — no code to validate
- Adds brownfield-context station (conditional) for existing system awareness
- Includes explicit test-strategy station — guides downstream testing
- 9 stations total (8 for greenfield, 9 for brownfield; vs. 10 in feature-implementation)
- Emphasizes documentation hand-off and external team readiness

## Differences from quality-validation

- This workflow is about *defining* quality (spec phase), not *validating* quality
- Outputs are specification artifacts, not code quality reports
- No external tool integrations (no linters, SonarQube, etc.)
- Can run without a git repository or compiled code
