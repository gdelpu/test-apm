---
name: sdlc-tech-design
description: 'Produce the technical design dossier: data model with DDL and migrations, OpenAPI-compliant API contracts, test strategy, and the implementation plan.'
triggers: ['technical design', 'data model', 'API contracts', 'implementation plan', 'test strategy']
---

# Skill: sdlc-tech-design

## Goal

Produce the technical design dossier: data model with DDL and migrations, OpenAPI-compliant API contracts, test strategy, and the implementation plan that compiles into the CLAUDE.md entry point.

## When to use

- After architecture (T1) is complete and validated
- As System T2 in the `sdlc-tech` workflow
- Runs incrementally per sprint scope

## Procedure

### Phase 1 — Data Model (agent t2.1)
1. Load the data model template from `resources/`
2. Read upstream: `[DOM-001]` BA domain model, `[STK-001]` stack conventions
3. Produce DDL-like data model with tables, columns, types, FK/indexes
4. Define migration strategy (incremental per sprint)
5. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/2-design/dat-001-data-model.md` with identifier `[DAT-001]`

### Phase 2 — API Contracts (agent t2.2) — depends on Phase 1
1. Load the API contract template from `resources/`
2. Read upstream: `[DAT-001]`, `[US-xxx]` user stories, `[ACT-001]` actors
3. Produce OpenAPI-compliant API contract files
4. Standardize error responses across all endpoints
5. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/2-design/api-{id}-{slug}.md` per API group with identifier `[API-xxx]`

### Phase 3 — Test Strategy (agent t2.4) — depends on Phase 2
1. Load the test strategy template from `resources/`
2. Read upstream: `[API-xxx]`, `[SCE-xxx]` BA test scenarios, `[BRL-*]` business rules
3. Define the test pyramid: unit, integration, E2E, performance thresholds
4. Map BA scenarios to technical test implementations
5. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/2-design/tst-001-test-strategy.md` with identifier `[TST-001]`

### Phase 4 — Implementation Plan (agent t2.5) — depends on Phase 3
1. Load the implementation plan template from `resources/`
2. Read upstream: all T1 + T2 deliverables, BA specifications
3. Produce ordered wave plan for Claude Code implementation
4. Compile `CLAUDE.md` as the entry point for code generation
5. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/2-design/imp-001-implementation-plan.md` with identifier `[IMP-001]`
6. Use the `edit/editFiles` tool to create project root `CLAUDE.md`

## Output

- `outputs/docs/2-tech/2-design/dat-001-data-model.md` — `[DAT-001]`
- `outputs/docs/2-tech/2-design/api-{id}-{slug}.md` — `[API-xxx]` (per API group)
- `outputs/docs/2-tech/2-design/tst-001-test-strategy.md` — `[TST-001]`
- `outputs/docs/2-tech/2-design/imp-001-implementation-plan.md` — `[IMP-001]`
- `CLAUDE.md` — Claude Code entry point

## Rules

- Phases are sequential: data model → APIs → test strategy → implementation plan
- Data model must trace to BA domain model (every entity maps to a domain concept)
- API contracts must trace to user stories (every endpoint serves at least one US)
- Test strategy must integrate both BA scenarios and technical test concerns
- Implementation plan must include wave ordering suitable for automated code generation

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-data-model.md` | Data model DDL template |
| `docs/tpl-api-contract.md` | OpenAPI contract template |
| `docs/tpl-test-strategy.md` | Test strategy template |
| `docs/tpl-implementation-plan.md` | Implementation plan template |
