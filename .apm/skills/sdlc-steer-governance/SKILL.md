# Skill: sdlc-steer-governance

## Goal

Prepare steering committee (COPIL) presentation packs and produce Go/No-Go release decisions by aggregating quality, security, test, and risk data from all domains.

## When to use

- At project milestones for committee preparation (System P3)
- Before release decisions
- As governance stations in the `sdlc-steer` workflow

## Procedure

### Phase 1 — COPIL Preparation (agent p3.1)
1. Load the COPIL template from `resources/`
2. Read sprint reports `[STA-*]`, risk registers `[RSK-*]`, and domain deliverables
3. Produce steering committee presentation pack with both:
   - **Technical section**: architecture health, quality metrics, debt indicators
   - **Sponsor section**: progress overview, budget status, key decisions needed
4. Write `docs/3-steer/1-committees/cop-{NNN}-copil.md` with identifier `[COP-NNN]`

### Phase 2 — Go/No-Go Decision (agent p3.2) — depends on Phase 1
1. Load the Go/No-Go template from `resources/`
2. Aggregate from all domains:
   - BA: specification completeness and validation status
   - Tech: code quality, test coverage, security posture
   - Test: campaign results `[CAMP-RPT-*]`, performance `[PERF-RPT-*]`
   - Steer: risk status, budget status, open decisions
3. Produce structured Go/No-Go decision with criteria matrix
4. Write `docs/3-steer/1-committees/gng-001-go-nogo.md` with identifier `[GNG-001]`

## Output

- `docs/3-steer/1-committees/cop-{NNN}-copil.md` — `[COP-NNN]`
- `docs/3-steer/1-committees/gng-001-go-nogo.md` — `[GNG-001]`

## Rules

- COPIL pack must include both technical and sponsor perspectives
- Go/No-Go must aggregate ALL domain data — never skip quality or security
- Decision criteria must be explicit and traceable to evidence
- COPIL numbering `NNN` increments with each committee meeting

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-steering-committee.md` | COPIL presentation template |
| `docs/tpl-go-nogo.md` | Go/No-Go decision template |
| `docs/sk-p3.1-copil.md` | COPIL preparation procedure |
| `docs/sk-p3.2-go-nogo.md` | Go/No-Go procedure |
