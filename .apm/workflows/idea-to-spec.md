# Workflow: Idea to Spec

Transform a raw idea into a validated, unambiguous specification with NFRs and architecture sketch.

## When to use

- Turning a business idea or initiative into a structured specification
- Early-stage feature exploration before committing to implementation
- When the biggest leverage is in getting the specification right
- Brownfield or greenfield — domain enrichment adapts automatically

## Stations

| # | Station | Agent | Skills | Gate | Severity |
|---|---------|-------|--------|------|----------|
| 1 | Intent Capture | spec-orchestrator | intent-capture | Business goal, constraints, personas defined | blocker |
| 2 | Domain / Context Enrichment | spec-orchestrator | brownfield-context, repo-analysis | Existing patterns documented (optional for greenfield) | warning |
| 3 | Feature Specification | spec-orchestrator | spec-feature | Scope, acceptance criteria, scenarios defined | blocker |
| 4 | Clarification Loop | spec-orchestrator | spec-clarify | No unresolved blockers or ambiguities | blocker |
| 5 | NFR Definition | spec-orchestrator | nfr-review | Security, perf, resilience, observability defined | blocker |
| 6 | Architecture Sketch | architecture-governance | architecture-guardrails | Principles satisfied, risks mitigated | blocker |
| 7 | Spec Quality Gate | spec-orchestrator | spec-quality-gate | Package complete and coherent | blocker |

## Outputs

All artifacts are written to `specs/features/<feature>/`:
- `intent.md` — Business goal, constraints, target users
- `context-brief.md` — Domain context, existing codebase patterns (brownfield)
- `spec.md` — Feature specification with scope and acceptance criteria
- `clarifications.md` — Resolved ambiguities and Q&A
- `nfr-review.md` — Non-functional requirements with measurable targets
- `architecture-review.md` — Architecture sketch and risk assessment
- `quality-gate.md` — Spec quality gate evaluation

## Key differences from spec-kit

- Starts with explicit intent capture (business goal, constraints, personas)
- Includes domain/context enrichment as an early station
- Dedicated NFR station before architecture sketch
- Stops at spec — no plan or task decomposition (hand off to `spec-to-execution`)

## Composition

Chain with `spec-to-execution` for the full idea → plan → tasks pipeline.
Chain further with `implementation-loop` for end-to-end delivery.

## Brownfield variant

Station 2 (Domain Enrichment) activates brownfield-context and repo-analysis skills to capture the existing codebase state. For greenfield, this station is optional and can be skipped.
