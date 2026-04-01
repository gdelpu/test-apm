# Workflow: SDLC BA

Full business analysis pipeline from brownfield audit through scoping, specification, and per-feature functional design with fan-out/fan-in orchestration.

## When to use

- Starting or auditing a brownfield application that needs a complete functional specification
- Producing a full PRD from existing system audit to user stories, journeys, and test scenarios
- Projects requiring traceability from requirements through epics, features, stories, and test scenarios
- When deliverables must follow the `EXF → EP → FT → US → BR → SCE` traceability chain
- Feeding the Tech pipeline (`sdlc-tech`) with a validated BA baseline

## Stations

### System S0 — Brownfield Audit (optional)

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 1 | Existing System Audit | sdlc-ba-analyst | sdlc-ba-audit | AS-IS snapshot covers all modules; integration points documented | blocker |
| 2 | Delta Analysis | sdlc-ba-analyst | sdlc-ba-audit | Every functional area classified (new/evolving/preserved/deprecated) | blocker |

### System S1 — Scoping

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 3 | Product Vision & Scope | sdlc-ba-analyst | sdlc-ba-scoping | Measurable objectives; clear IN/OUT scope boundaries | blocker |
| 4 | Business Glossary | sdlc-ba-analyst | sdlc-ba-scoping | Ubiquitous language terms defined (parallel) | blocker |
| 5 | Actors & Roles | sdlc-ba-analyst | sdlc-ba-scoping | All human/system actors identified; permissions matrix defined | blocker |
| 6 | Functional Requirements | sdlc-ba-analyst | sdlc-ba-scoping | Requirements testable and traceable; R4J anchors present | blocker |

### System S2 — Specification

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 7 | Domain Model | sdlc-ba-analyst | sdlc-ba-specification | Entities/attributes/relationships complete; Mermaid ER diagram included | blocker |
| 8 | Epic Decomposition | sdlc-ba-analyst | sdlc-ba-specification | Epics cover all functional requirements | blocker |
| 9 | Feature Specification | sdlc-ba-analyst | sdlc-ba-specification | Each feature scoped within parent epic; IDs sequential and unique | blocker |
| 10 | Business Rules | sdlc-ba-analyst | sdlc-ba-specification | Rules deduplicated, classified, dispatched per feature | blocker |

### System S3 — Functional Design (per feature)

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 11 | User Stories | sdlc-ba-analyst | sdlc-ba-functional-design | Atomic stories with GWT acceptance criteria; trace to features | blocker |
| 12 | User Journeys | sdlc-ba-analyst | sdlc-ba-functional-design | Journeys chain stories into E2E flows; Mermaid diagrams | blocker |
| 13 | Screen Specifications | sdlc-ba-analyst | sdlc-ba-functional-design | Components, fields, validation rules defined (optional: `has_screens`) | blocker |
| 14 | Test Scenarios | sdlc-ba-analyst | sdlc-ba-functional-design | Gherkin scenarios cover stories and rules; coverage matrix | blocker |
| 15 | E2E Test Plan | sdlc-ba-analyst | sdlc-ba-functional-design | Cross-feature E2E journeys; Xray campaign structure | blocker |

### Quality Gate

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 16 | BA Deliverable Validation | sdlc-ba-analyst | sdlc-deliverable-validation | All deliverables pass quality audit; cross-deliverable coherence; traceability chain complete | blocker |

## Fan-out / fan-in

Systems S2 and S3 use a fan-out pattern:

1. **Epic decomposition** (S2) produces `epics/` — each epic gets its own directory.
2. **Feature specification** fans out per epic, producing `features/`.
3. **Functional design** (S3) fans out per feature — stories, journeys, screen specs, and test scenarios are generated per feature directory.
4. **E2E Test Plan** and **BA Validation** fan back in to produce project-level deliverables.

This mirrors the original SDLC Harness DAG orchestration with S3 running once per feature.

## Brownfield vs. greenfield

- **Brownfield**: Start at station 1 (S0 audit). The audit and delta analysis stations produce the AS-IS baseline that informs all downstream scoping.
- **Greenfield**: Skip S0 (stations 1–2 are `optional: true`). Start directly at S1 (station 3 — Product Vision).

## Outputs

All artifacts are written to `docs/1-prd/`:
- `asis-001-existing-audit.md` — brownfield functional snapshot (optional)
- `delta-001-delta-analysis.md` — brownfield delta analysis (optional)
- `vis-001-product-vision.md` — vision, objectives, scope
- `glo-001-glossary.md` — ubiquitous language glossary
- `act-001-actors-roles.md` — actors and permissions matrix
- `exf-001-functional-requirements.md` — testable requirements with traceability
- `dom-001-domain-model.md` — domain model with ER diagram
- `epics/` — epic decomposition directory
- `features/` — per-feature specifications
- `business-rules/` — classified and dispatched business rules
- `user-stories/` — atomic stories with GWT criteria (per feature)
- `user-journeys/` — E2E journey flows with Mermaid (per feature)
- `screen-specs/` — UI specifications (per feature, optional)
- `test-scenarios/` — Gherkin scenarios with coverage matrix (per feature)
- `e2e-plan-001.md` — cross-feature E2E test plan
- `ba-validation-report.md` — final quality audit

## Nestable

This workflow has `nestable: true` and is invoked as the BA phase inside `sdlc-full`.

## Key differences from spec-kit

- Designed for large-scale PRD production with multiple epics and features, not single-feature specification
- Includes brownfield audit system (S0) for AS-IS analysis
- Uses fan-out/fan-in orchestration for per-feature functional design
- Produces full Gherkin test scenarios and E2E test plans
- 16 stations (spec-kit has 8)
- Traceability chain: `EXF → EP → FT → US → BR → SCE`
