# Skill: sdlc-steer-init

## Goal

Initialize the project steering framework with team composition, capacity allocation, budget structure, and KPI baselines for effort and token cost tracking.

## When to use

- At the start of a project (System P0)
- As the first station in the `sdlc-steer` workflow
- Run once; outputs are referenced by all subsequent steering activities

## Procedure

### Phase 1 — Project Sheet (agent p0.1)
1. Load the project sheet template from `resources/`
2. Define team composition, roles, and capacity allocation
3. Establish budget structure (effort + token cost dual-axis)
4. Write `docs/3-steer/pil-001-project-sheet.md` with identifiers `[PIL-001]`, `[CAP-001]`

### Phase 2 — KPI Baseline (agent p0.2) — depends on Phase 1
1. Load the KPI baseline template from `resources/`
2. Read project sheet `[PIL-001]` for capacity and budget data
3. Establish baseline KPIs: effort budget, token budget, velocity targets
4. Write `docs/3-steer/kpi-001-baseline.md` with identifier `[KPI-001]`

## Output

- `docs/3-steer/pil-001-project-sheet.md` — `[PIL-001]`, `[CAP-001]`
- `docs/3-steer/kpi-001-baseline.md` — `[KPI-001]`

## Rules

- Run exactly once per project
- Project sheet must cover both human and agentic capacity
- KPI baseline must include token cost tracking for agentic execution
- Budget tracking uses dual-axis: effort hours + token consumption

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-project-sheet.md` | Project sheet template |
| `docs/sk-p0.1-project-sheet.md` | Detailed project sheet procedure |
| `docs/sk-p0.2-kpi-baseline.md` | Detailed KPI baseline procedure |
