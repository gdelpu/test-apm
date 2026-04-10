---
name: sdlc-tech-architecture
description: 'Define the system architecture through C4 context diagrams, architecture decision records (ADRs), technology stack extraction, and enabler identification.'
triggers: ['system architecture', 'C4 diagrams', 'ADR', 'architecture decision record', 'technology stack']
---

# Skill: sdlc-tech-architecture

## Goal

Define the system architecture through C4 context diagrams, architecture decision records (ADRs), technology stack extraction, and enabler identification — with fan-out per ADR and fan-in for consolidation.

## When to use

- After technical audit (T0) or at the start of greenfield tech engagement
- As System T1 in the `sdlc-tech` workflow
- Prerequisite: Tech discovery workshop document `[DCO-TECH-001]` should exist

## Procedure

### Phase 1 — System Context (agent t1.1)
1. Load the system context template from `resources/`
2. Read BA deliverables and tech audit results as input
3. Produce C4 Level 1 and Level 2 diagrams with Mermaid
4. Document integrations, external systems, and data flows
5. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/1-architecture/ctx-001-system-context.md` with identifier `[CTX-001]`

### Phase 2 — Architecture Decisions (agent t1.2) — produces ADR collection
1. Load the ADR template from `resources/`
2. Read system context `[CTX-001]` and BA requirements
3. Produce N ADR files covering: architecture, security, observability decisions
4. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/1-architecture/adr/adr-{id}-{slug}.md` per ADR with identifier `[ADR-xxx]`
5. Register the `adrs` collection for downstream fan-out

### Phase 3 — Stack Extraction (agent t1.3) — fan-out per ADR
1. For each ADR, extract the technology stack implied by that decision
2. Keep context small (~150 lines per instance) for efficiency
3. Write to staging directory for consolidation

### Phase 4 — Stack Consolidation (agent t1.3b) — fan-in
1. Consolidate all per-ADR stack extractions into a unified stack document
2. Resolve conflicts between ADR stacks
3. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/1-architecture/stk-001-stack-conventions.md` with identifier `[STK-001]`

### Phase 5 — Enabler Extraction (agent t1.4) — fan-out per ADR
1. For each ADR, extract required enablers (cross-cutting concerns, infrastructure)
2. Keep context small (~250 lines per instance)
3. Write to staging directory for consolidation

### Phase 6 — Enabler Index (agent t1.4b) — fan-in
1. Consolidate all enablers into a prioritized index with wave resolution
2. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/1-architecture/enb-000-index.md`

## Output

- `outputs/docs/2-tech/1-architecture/ctx-001-system-context.md` — `[CTX-001]`
- `outputs/docs/2-tech/1-architecture/adr/adr-{id}-{slug}.md` — `[ADR-xxx]` (N ADRs)
- `outputs/docs/2-tech/1-architecture/stk-001-stack-conventions.md` — `[STK-001]`
- `outputs/docs/2-tech/1-architecture/enb-000-index.md` — enabler index

## Rules

- Phase 2 depends on Phase 1
- Phases 3 and 5 are fan-out per ADR and can run in parallel
- Phases 4 and 6 are fan-in consolidations
- ADRs must have: context, decision, rationale, confidence level, consequences
- Stack consolidation must detect and resolve contradictions

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-system-context.md` | C4 system context template |
| `docs/tpl-adr.md` | Architecture decision record template |
| `docs/tpl-stack-conventions.md` | Stack conventions template |
| `docs/tpl-enabler.md` | Enabler definition template |
| `docs/skill-registry/` | Composable stack-specific skills (React, AWS, PostgreSQL, etc.) |
