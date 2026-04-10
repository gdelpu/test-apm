---
name: sdlc-steer-planning
description: 'Create the sprint plan, project roadmap, and initial risk register — establishing the execution framework for all downstream domain pipelines.'
triggers: ['sprint planning', 'project roadmap', 'risk register', 'feature batching']
---

# Skill: sdlc-steer-planning

## Goal

Create the sprint plan (batching features for parallel execution), project roadmap, and initial risk register — establishing the execution framework for all downstream domain pipelines.

## When to use

- After project initialization (P0) is complete
- As System P1 in the `sdlc-steer` workflow
- Run once; sprint plan is consumed by `--scope` filtering in BA/Tech pipelines

## Procedure

### Phase 1 — Sprint Planning (agent p1.3)
1. Load the sprint planning template from `resources/`
2. Read only epic files (NOT full BA deliverables) from `outputs/docs/1-prd/3-epics/`
3. Batch features into parallel sprints based on dependencies, complexity, and capacity
4. Produce unified BA+Tech sprint plan with scope_items YAML front matter
5. Use the `edit/editFiles` tool to create `outputs/docs/3-steer/plan-001-sprint-planning.md` with identifier `[PLAN-001]`

### Phase 2 — Roadmap (agent p1.1) — depends on Phase 1
1. Load the roadmap template from `resources/`
2. Read sprint plan `[PLAN-001]` for phase structure
3. Define phases, milestones, and quality gates
4. Use the `edit/editFiles` tool to create `outputs/docs/3-steer/rdp-001-roadmap.md` with identifier `[RDP-001]`

### Phase 3 — Risk Register (agent p1.2) — depends on Phase 2
1. Load the risk register template from `resources/`
2. Read roadmap `[RDP-001]` for timeline context
3. Assess initial risks using the agentic risk taxonomy:
   - Review bottleneck, scope drift, quality regression
   - Hallucination propagation, token budget overrun, integration debt
4. Use the `edit/editFiles` tool to create `outputs/docs/3-steer/rsk-001-risk-register.md` with identifier `[RSK-001]`

## Output

- `outputs/docs/3-steer/plan-001-sprint-planning.md` — `[PLAN-001]`
- `outputs/docs/3-steer/rdp-001-roadmap.md` — `[RDP-001]`
- `outputs/docs/3-steer/rsk-001-risk-register.md` — `[RSK-001]`

## Rules

- Sprint planning reads epic-level data only — never full S3 deliverables
- Sprint plan YAML front matter must include `scope_items` for downstream filtering
- Risk register must use the agentic risk taxonomy (6 risk types)
- Roadmap milestones must align with sprint boundaries

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-roadmap.md` | Roadmap template |
| `docs/tpl-risk.md` | Risk register template |
| `docs/sk-p1.0-iteration-planning.md` | Iteration planning procedure |
| `docs/sk-p1.1-roadmap.md` | Roadmap procedure |
| `docs/sk-p1.2-risk-register.md` | Risk register procedure |
| `docs/sk-p1.3-sprint-planning-design.md` | Sprint planning procedure |
