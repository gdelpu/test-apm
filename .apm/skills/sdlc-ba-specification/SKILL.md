---
name: sdlc-ba-specification
description: 'Build the domain model, decompose into epics and features, and consolidate business rules — transforming scoping deliverables into a structured specification ready for functional design.'
---

# Skill: sdlc-ba-specification

## Goal

Build the domain model, decompose into epics and features, and consolidate business rules — transforming scoping deliverables into a structured specification ready for functional design.

## When to use

- After scoping (S1) is complete and validated
- As System S2 in the `sdlc-ba` workflow
- Produces the fan-out collections (epics, features) consumed by S3

## Procedure

### Phase 1 — Domain Model (agent 2.1)
1. Load the domain model template from `resources/`
2. Read upstream: `[VIS-001]`, `[GLO-001]`, `[ACT-001]`, `[DELTA-001]` (if brownfield)
3. Build functional domain model with entities, attributes, relationships, and lifecycle diagrams
4. Generate Mermaid ER diagram
5. Write `docs/1-prd/2-specification/dom-001-domain-model.md` with identifier `[DOM-001]`

### Phase 2 — Epic Decomposition (agent 2.2)
1. Load the epic template from `resources/`
2. Read upstream: `[DOM-001]` domain model
3. Decompose into N epic files with hierarchical structure
4. Write `docs/1-prd/3-epics/ep-{id}-{slug}/ep-{id}-{slug}.md` per epic with identifier `[EP-xxx]`
5. Register the `epics` collection for downstream fan-out

### Phase 3 — Feature Specification (agent 2.2b) — fan-out per epic
1. Load the feature template from `resources/`
2. For each epic in the `epics` collection, produce feature specifications
3. Write `docs/1-prd/3-epics/{epic}/ft-{id}-{slug}/ft-{id}-{slug}.md` per feature with identifier `[FT-xxx]`
4. Register the `features` collection for S3 fan-out

### Phase 4 — Business Rules Consolidation (agent 2.3) — fan-out per rule type
1. Discover rule types from staging directory: `docs/1-prd/2-specification/_rules-staging/*/`
2. Rule types: VAL (validation), CAL (calculation), TRG (trigger), COH (coherence), AUT (authorization)
3. For each rule type, consolidate and deduplicate rules across all features
4. Write `docs/1-prd/2-specification/brl-{type}-business-rules.md` per type with identifier `[BRL-{type}]`
5. Dispatch consolidated rules back to per-feature directories (via script)

## Output

- `docs/1-prd/2-specification/dom-001-domain-model.md` — `[DOM-001]`
- `docs/1-prd/3-epics/ep-{id}-{slug}/ep-{id}-{slug}.md` — `[EP-xxx]` (N epics)
- `docs/1-prd/3-epics/{epic}/ft-{id}-{slug}/ft-{id}-{slug}.md` — `[FT-xxx]` (N features)
- `docs/1-prd/2-specification/brl-{type}-business-rules.md` — `[BRL-{type}]` (per rule type)

## Rules

- Phase 2 depends on Phase 1 (domain model required for epic decomposition)
- Phase 3 runs per-epic in parallel (fan-out)
- Phase 4 depends on both Phase 1 and Phase 3
- Epic and feature identifiers must be sequential and unique
- Feature specifications must reference their parent epic

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-domain-model.md` | Domain model with ERD template |
| `docs/tpl-epic.md` | Epic definition template |
| `docs/tpl-feature.md` | Feature specification template |
| `docs/tpl-business-rules.md` | Business rules by type template |
| `docs/sk-2.1-domain-model.md` | Detailed domain model procedure |
| `docs/sk-2.2-epics.md` | Detailed epic procedure |
| `docs/sk-2.2b-features.md` | Detailed feature procedure |
| `docs/sk-2.3-business-rules.md` | Detailed rules procedure |
