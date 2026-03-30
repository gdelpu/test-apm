# Workflow: Spec Kit

Specification-only pipeline producing a complete spec package without implementation or code validation.

## When to use

- When only specification artifacts are needed (no code generation)
- Preparing a spec package for manual implementation or external team handoff
- When the full feature-implementation workflow is too broad
- Greenfield scoping that requires formal gates before committing to implementation
- Creating a detailed roadmap or RFP document for contracted work

## Stations

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 1 | Constitution | spec-orchestrator | spec-constitution | Constitution covers architecture, quality, security, testing, observability | blocker |
| 2 | Feature Specification | spec-orchestrator | spec-feature | Scope and out-of-scope defined, acceptance criteria testable | blocker |
| 3 | Clarification | spec-orchestrator | spec-clarify | No unresolved blocker questions | blocker |
| 4 | Architecture Review | architecture-governance | architecture-guardrails | Architecture principles satisfied, no unmitigated high-risk concerns | blocker |
| 5 | Planning | spec-orchestrator | spec-plan | Risks identified with mitigations, rollout and rollback strategies defined | blocker |
| 6 | Task Breakdown | spec-orchestrator | spec-tasks | Tasks traceable to plan, verification steps included | blocker |
| 7 | Test Strategy | spec-orchestrator | test-strategy | Test levels (unit/integration/e2e) and coverage targets stated | warning |
| 8 | Quality Gate | spec-orchestrator | spec-quality-gate | Package complete, coherent, and self-contained | blocker |

## Outputs

All artifacts are written to `specs/features/<feature>/`:
- `constitution.md` — foundational principles and constraints
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
- **Test strategy focus** — explicit station for test planning to help downstream implementation
- **Specification-only gate** — final gate is coherence and completeness of documents, not code metrics

## Differences from feature-implementation

- No implementation station — stops after specification package
- No nested quality-validation — no code to validate
- Includes explicit test-strategy station (station 7) — guides downstream testing
- 8 stations total (vs. 9 in feature-implementation)
- Emphasizes documentation hand-off and external team readiness

## Differences from quality-validation

- This workflow is about *defining* quality (spec phase), not *validating* quality
- Outputs are specification artifacts, not code quality reports
- No external tool integrations (no linters, SonarQube, etc.)
- Can run without a git repository or compiled code
