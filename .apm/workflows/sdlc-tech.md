# Workflow: SDLC Tech

Full technical architecture and design pipeline from brownfield audit through architecture decisions, incremental design, sprint-iterative implementation, and continuous quality monitoring.

## When to use

- Defining the target technical architecture for a new or modernized system
- Producing C4 system context, ADRs, stack conventions, and enabler plans
- Creating data models, API contracts, test strategies, and implementation plans
- When technical deliverables must trace back to BA functional requirements
- Feeding the implementation phase with an ordered wave plan and compiled entry point

## Stations

### System T0 — Brownfield Technical Audit (optional)

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 1 | Technical Stack Audit | sdlc-tech-architect | sdlc-tech-audit | Current stack fully assessed; compliance gaps identified | blocker |
| 2 | Gap Analysis | sdlc-tech-architect | sdlc-tech-audit | Migration paths defined with effort estimates | blocker |

### System T1 — Architecture

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 3 | System Context (C4) | sdlc-tech-architect | sdlc-tech-architecture | C4 Level 1-2 diagrams; all integrations documented | blocker |
| 4 | Architecture Decision Records | sdlc-tech-architect | sdlc-tech-architecture | Each ADR has context, decision, rationale, confidence; security + observability ADRs included | blocker |
| 5 | Stack Extraction | sdlc-tech-architect | sdlc-tech-architecture | Unified stack document; no contradictions; skills selected from registry | blocker |
| 6 | Enabler Extraction | sdlc-tech-architect | sdlc-tech-architecture | Enablers prioritized with wave resolution | blocker |

### System T2 — Technical Design

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 7 | Data Model | sdlc-tech-architect | sdlc-tech-design | DDL-like model with FK/indexes; migration strategy; traces to BA domain model | blocker |
| 8 | API Contracts | sdlc-tech-architect | sdlc-tech-design | OpenAPI-compliant contracts; standardized errors; traces to user stories | blocker |
| 9 | Test Strategy | sdlc-tech-architect | sdlc-tech-design | Test pyramid with coverage thresholds; BA scenarios mapped to technical tests | blocker |
| 10 | Implementation Plan | sdlc-tech-architect | sdlc-tech-design | Ordered wave plan; coding agent briefing compiled | blocker |
| 10b | Provider Bootstrap | sdlc-tech-architect | sdlc-tech-design | Provider-specific artifacts generated (optional) | warning |

### System T3 — Implementation (iterative per sprint)

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 10c | Branch Creation | implementer | sdlc-tech-implementation | Feature branch created from main; branch name follows convention | blocker |
| 11 | Task Resolution | implementer | sdlc-tech-implementation | Task prerequisites verified; context resolved; scope ≤ 8h | blocker |
| 12 | Code Generation | implementer | sdlc-tech-implementation | Code compiles; matches STK-001, DAT-001, API-xxx; no out-of-scope changes | blocker |
| 13 | Test Implementation | implementer | sdlc-tech-implementation | All mapped test IDs have test files; tests pass; BA traceability present | blocker |
| 14 | Build & Validate | implementer | sdlc-tech-implementation | Build passes; coverage met; 0 secrets; 0 critical SAST | blocker |
| 15 | Wave Gate | implementer | sdlc-tech-implementation | All wave items done; wave DoD met; no blockers | blocker |
| 15b | CI Validation | implementer | sdlc-tech-implementation | CI pipeline green: SAST, quality gate, secret scan, full test suite | blocker |
| 15c | Merge Request | implementer | sdlc-tech-implementation | MR created, approved, and merged to main | blocker |

Station 10c creates a feature branch per wave. Stations 11–14 loop **per item** with a commit after each item. Station 15 fires the wave gate. After drift detection (T4.1), station 15b validates via CI pipeline and station 15c creates and merges the MR.

### System T4 — Continuous Quality

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 16 | Drift Detection | sdlc-tech-architect | sdlc-tech-quality | Spec-vs-code discrepancies identified | warning |
| 17 | E2E Playwright Campaign Generation | sdlc-tech-architect | sdlc-tech-quality | E2E campaign scripts generated for testable flows; testability filter applied | warning |

Station 16 (Drift Detection) runs **per wave** on the wave branch (between T3.5 and T3.6). Station 17 (E2E Campaign Generation) runs **once per sprint** after the last wave gate.

## BA → Tech traceability

The Tech pipeline consumes BA deliverables and maintains bidirectional traceability:

- **Domain model** (T2) traces to BA domain model (`dom-001-domain-model.md`)
- **API contracts** (T2) trace to BA user stories and functional requirements
- **Test strategy** (T2) maps BA Gherkin scenarios to technical test types
- **Drift detection** (T4) checks implementation against both BA and Tech specifications

## Brownfield vs. greenfield

- **Brownfield**: Start at station 1 (T0 audit). The technical audit produces a gap analysis with migration paths and effort estimates.
- **Greenfield**: Skip T0 (stations 1–2 are `optional: true`). Start directly at T1 (station 3 — System Context).

## ADR fan-out

Station 4 (Architecture Decision Records) may produce multiple ADRs. Each significant decision gets its own ADR in the `adr/` directory. The subsequent Stack Extraction and Enabler stations consolidate these into unified deliverables.

## Outputs

All artifacts are written to `outputs/docs/2-tech/`:
- `tech-asis-001-technical-audit.md` — current stack assessment (optional)
- `gap-001-technical-gap.md` — gap analysis with migration paths (optional)
- `ctx-001-system-context.md` — C4 Level 1-2 system context
- `adr/` — architecture decision records
- `stk-001-stack-conventions.md` — unified stack and conventions
- `enb-000-index.md` — enabler index with wave priorities
- `dat-001-data-model.md` — DDL-like data model
- `api-contracts/` — OpenAPI-compliant per-endpoint contracts
- `tst-001-test-strategy.md` — test pyramid and coverage thresholds
- `imp-001-implementation-plan.md` — ordered wave implementation plan
- `coding-agent-briefing.md` — provider-neutral coding agent entry point
- `3-implementation/wave-state.json` — implementation progress tracking
- `3-implementation/wave-{id}-report.md` — wave completion reports
- `3-implementation/sprint-{id}-summary.md` — sprint summaries
- `drift-report.md` — spec-vs-code drift (continuous)
- `e2e-scripts-001-playwright.md` — generated E2E scripts (continuous)
- Feature branches: `feat/W{id}-{slug}` per wave
- Merge requests: one MR per wave, gated by CI + pr-validation

## Nestable

This workflow has `nestable: true` and is invoked as the Tech phase inside `sdlc-full`.

## SCM Strategy

The T3 implementation system follows a wave-scoped branching strategy:

### Branch lifecycle

1. **Branch creation (T3.0/10c)**: At the start of each wave, create `feat/W{id}-{slug}` from `main`
2. **Item commits (T3.1–T3.4)**: Each item produces a commit after local validation passes: `feat(W{id}): {item_id} — {item_title}`
3. **Wave gate (T3.5)**: Validates all wave items are complete
4. **Drift detection (T4.1)**: Runs on the branch (non-blocking)
5. **Push & CI (T3.6/15b)**: Push branch, wait for CI pipeline (SonarQube, SAST, secret scan, full test suite)
6. **Merge Request (T3.7/15c)**: Create MR, await approval + pipeline green, merge to main

### Naming conventions

| Element | Convention | Example |
|---------|-----------|--------|
| Branch | `feat/W{id}-{slug}` | `feat/W2-ep001-user-auth` |
| Commit | `feat(W{id}): {item_id} — {title}` | `feat(W1): IMP-W1-004 — JWT auth filter` |

### Wave ordering and merge sequence

Waves merge to main in strict order: W0 → W1 → W2 → WNFR. Each wave branch is created from the updated main after the previous wave's MR is merged.

## Key differences from feature-implementation

- Focused on architecture and design, not end-to-end feature delivery
- Produces ADRs, C4 diagrams, stack conventions, enabler plans, and executes implementation — not just code
- T3 (implementation) executes the plan wave-by-wave, iterating per sprint
- T4 (continuous quality) runs during implementation as a feedback loop, not a one-shot gate
- 17 stations organized in 5 systems (vs. 9 sequential stations in feature-implementation)
- Designed to consume BA pipeline outputs and feed the implementation phase
