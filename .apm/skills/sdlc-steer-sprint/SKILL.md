---
name: sdlc-steer-sprint
description: 'Track sprint progress, monitor system health metrics, and assess evolving risks — producing recurring reports for steering committee preparation.'
---

# Skill: sdlc-steer-sprint

## Goal

Track sprint progress, monitor system health metrics, and assess evolving risks — producing recurring reports that feed into steering committee preparation.

## When to use

- During every sprint (System P2, recurring)
- As recurring stations in the `sdlc-steer` workflow
- Reads BA/Tech/Test outputs without modifying them

## Procedure

### Phase 1 — Sprint Progress (agent p2.1)
1. Read completed deliverables across BA, Tech, and Test domains
2. Calculate velocity metrics: planned vs delivered, throughput, blockers
3. Write `docs/3-steer/0-sprint-reports/sta-{NNN}-sprint-progress.md` with identifier `[STA-NNN]`

### Phase 2 — System Health (agent p2.2) — depends on Phase 1
1. Read code quality metrics, technical debt indicators, and test coverage data
2. Assess system health against KPI baseline thresholds
3. Update sprint report `[STA-NNN]` with health metrics section

### Phase 3 — Sprint Risks (agent p2.3) — depends on Phase 1 and Phase 2
1. Read sprint progress and system health data
2. Assess current sprint risks against the agentic risk taxonomy
3. Generate escalation decisions `[DEC-NNN]` if thresholds are breached
4. Write `docs/3-steer/0-sprint-reports/rsk-{NNN}-sprint-risks.md` with identifier `[RSK-NNN]`

## Output

- `docs/3-steer/0-sprint-reports/sta-{NNN}-sprint-progress.md` — `[STA-NNN]`
- `docs/3-steer/0-sprint-reports/rsk-{NNN}-sprint-risks.md` — `[RSK-NNN]`
- `[DEC-NNN]` decisions (when escalation is triggered)

## Rules

- Sprint numbering `NNN` increments with each sprint
- Never modify BA, Tech, or Test deliverables — read-only consumption
- Health metrics compare against `[KPI-001]` baseline
- Risk escalation triggers are automated based on thresholds
- Reports accumulate across sprints (not overwritten)

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-sprint-report.md` | Sprint report template |
| `docs/sk-p2.1-sprint-progress.md` | Sprint progress procedure |
| `docs/sk-p2.2-system-health.md` | System health procedure |
| `docs/sk-p2.3-sprint-risks.md` | Sprint risk assessment procedure |
