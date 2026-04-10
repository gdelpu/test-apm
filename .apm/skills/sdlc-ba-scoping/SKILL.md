---
name: sdlc-ba-scoping
description: 'Define the product scope through vision statement, business glossary (DDD ubiquitous language), actor/role identification, and functional requirements catalogue.'
triggers: ['product scoping', 'vision statement', 'business glossary', 'DDD ubiquitous language', 'functional requirements']
---

# Skill: sdlc-ba-scoping

## Goal

Define the product scope through vision statement, business glossary (DDD ubiquitous language), actor/role identification, and functional requirements catalogue — the foundational layer for all downstream specification and design.

## When to use

- After brownfield audit (S0) or at the start of greenfield BA engagement
- As System S1 in the `sdlc-ba` workflow
- Prerequisite: Discovery workshop document `[DCO-001]` must exist

## Procedure

### Phase 1 — Product Vision (agent 1.1)
1. Load the vision template from `resources/`
2. Read discovery document `[DCO-001]` and client inputs from `docs/0-inputs/ba/1-scoping/`
3. Define measurable objectives, clear IN/OUT scope, success criteria
4. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/1-scoping/vis-001-product-vision.md` with identifier `[VIS-001]`

### Phase 2 — Business Glossary (agent 1.2)
1. Load the glossary template from `resources/`
2. Read vision `[VIS-001]` and discovery `[DCO-001]` as upstream
3. Build the ubiquitous language (DDD) with precise term definitions, synonyms, and relationships
4. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/1-scoping/glo-001-glossary.md` with identifier `[GLO-001]`

### Phase 3 — Actors & Roles (agent 1.3)
1. Load the actors template from `resources/`
2. Read upstream: `[VIS-001]`, `[GLO-001]`, `[DCO-001]`
3. Identify human and system actors, define roles, and build the permissions matrix
4. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/1-scoping/act-001-actors-roles.md` with identifier `[ACT-001]`

### Phase 4 — Functional Requirements (agent 1.4)
1. Load the requirements template from `resources/`
2. Read upstream: `[VIS-001]`, `[GLO-001]`, `[ACT-001]`
3. Produce the structured requirements catalogue with traceability anchors (R4J Jira compatible)
4. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/1-scoping/exf-001-functional-requirements.md` with identifier `[EXF-001]`

## Output

- `outputs/docs/1-prd/1-scoping/vis-001-product-vision.md` — `[VIS-001]`
- `outputs/docs/1-prd/1-scoping/glo-001-glossary.md` — `[GLO-001]`
- `outputs/docs/1-prd/1-scoping/act-001-actors-roles.md` — `[ACT-001]`
- `outputs/docs/1-prd/1-scoping/exf-001-functional-requirements.md` — `[EXF-001]`

## Rules

- Phases 1 and 2 can run in parallel (no dependency between them)
- Phase 3 depends on Phase 2 (glossary needed for actor definitions)
- Phase 4 depends on all three previous phases
- Prerequisite: `[DCO-001]` discovery workshop document must exist; if missing, run the `ba-discovery` tool agent first
- Use DDD ubiquitous language as defined in the glossary throughout all deliverables

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-product-vision.md` | Product vision template |
| `docs/tpl-glossary.md` | Business glossary template |
| `docs/tpl-actors-roles.md` | Actors & permissions matrix template |
| `docs/tpl-functional-requirements.md` | Requirements catalogue template |
| `docs/sk-1.1-vision.md` | Detailed vision procedure |
| `docs/sk-1.2-glossary.md` | Detailed glossary procedure |
| `docs/sk-1.3-actors-roles.md` | Detailed actors procedure |
| `docs/sk-1.4-functional-requirements.md` | Detailed requirements procedure |
