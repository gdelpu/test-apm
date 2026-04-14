# Workflow: SDLC Tech

Full technical architecture and design pipeline from brownfield audit through architecture decisions, incremental design, and continuous quality monitoring.

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

### System T3 — Continuous Quality

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 11 | Drift Detection | sdlc-tech-architect | sdlc-tech-quality | Spec-vs-code discrepancies identified | warning |
| 12 | E2E Playwright Generation | sdlc-tech-architect | sdlc-tech-quality | E2E scripts trace to BA test scenarios | warning |

## BA → Tech traceability

The Tech pipeline consumes BA deliverables and maintains bidirectional traceability:

- **Domain model** (T2) traces to BA domain model (`dom-001-domain-model.md`)
- **API contracts** (T2) trace to BA user stories and functional requirements
- **Test strategy** (T2) maps BA Gherkin scenarios to technical test types
- **Drift detection** (T3) checks implementation against both BA and Tech specifications

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
- `drift-report.md` — spec-vs-code drift (continuous)
- `e2e-scripts-001-playwright.md` — generated E2E scripts (continuous)

## Nestable

This workflow has `nestable: true` and is invoked as the Tech phase inside `sdlc-full`.

## Key differences from feature-implementation

- Focused on architecture and design, not end-to-end feature delivery
- Produces ADRs, C4 diagrams, stack conventions, and enabler plans — not code
- T3 (continuous quality) runs during implementation as a feedback loop, not a one-shot gate
- 12 stations organized in 4 systems (vs. 9 sequential stations in feature-implementation)
- Designed to consume BA pipeline outputs and feed the implementation phase
