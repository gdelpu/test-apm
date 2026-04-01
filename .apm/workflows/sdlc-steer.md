# Workflow: SDLC Steer

Project steering pipeline from initialization through sprint planning, recurring sprint tracking, and governance decisions (COPIL + Go/No-Go).

## When to use

- Setting up project governance structure, team composition, and KPI baselines
- Planning sprints with feature batching and roadmap definition
- Tracking sprint progress with velocity metrics, health checks, and risk assessments
- Preparing COPIL steering committee presentations and Go/No-Go decisions
- Running alongside BA and Tech pipelines to provide continuous project oversight

## Stations

### System P0 — Project Initialization

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 1 | Project Sheet | sdlc-steer-manager | sdlc-steer-init | Team composition and capacity defined; budget structure established | blocker |
| 2 | KPI Baseline | sdlc-steer-manager | sdlc-steer-init | Effort and token baselines established; velocity targets defined | blocker |

### System P1 — Planning

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 3 | Sprint Planning | sdlc-steer-manager | sdlc-steer-planning | Features batched into sprints; `scope_items` YAML front matter present | blocker |
| 4 | Roadmap | sdlc-steer-manager | sdlc-steer-planning | Phases, milestones, and gates defined | blocker |
| 5 | Risk Register | sdlc-steer-manager | sdlc-steer-planning | All 6 agentic risk types assessed; escalation thresholds defined | blocker |

### System P2 — Sprint Tracking (recurring)

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 6 | Sprint Progress | sdlc-steer-manager | sdlc-steer-sprint | Velocity metrics and blockers documented | warning |
| 7 | System Health | sdlc-steer-manager | sdlc-steer-sprint | Health metrics compared against KPI baseline | warning |
| 8 | Sprint Risks | sdlc-steer-manager | sdlc-steer-sprint | Risks assessed against taxonomy; escalation if thresholds breached | warning |

### System P3 — Governance

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 9 | COPIL Preparation | sdlc-steer-manager | sdlc-steer-governance | Technical and sponsor sections included; key decisions documented | blocker |
| 10 | Go/No-Go Decision | sdlc-steer-manager | sdlc-steer-governance | All domain data aggregated; decision criteria explicit and traceable | blocker |

## Recurring stations

System P2 (Sprint Tracking) runs on a recurring cadence — typically once per sprint. Stations 6–8 have `severity: warning` gates, meaning they log issues but do not halt the workflow. This allows sprint tracking to proceed even when metrics are below target, while escalation decisions are generated automatically when thresholds are breached.

## Agentic risk taxonomy

The Risk Register (station 5) and Sprint Risks (station 8) assess risks across 6 categories specific to AI-assisted delivery:

1. **Hallucination risk** — AI-generated artifacts diverge from source material
2. **Drift risk** — implementation diverges from specification over time
3. **Token budget risk** — AI token consumption exceeds budget allocation
4. **Scope creep risk** — uncontrolled scope expansion during sprints
5. **Quality regression risk** — quality metrics degrade across iterations
6. **Dependency risk** — external or inter-team dependencies block progress

## Outputs

All artifacts are written to `docs/3-steer/`:
- `pil-001-project-sheet.md` — team, capacity, budget structure
- `kpi-001-baseline.md` — effort and token baselines, velocity targets
- `plan-001-sprint-planning.md` — feature-to-sprint batching
- `rdp-001-roadmap.md` — phases, milestones, gates
- `rsk-001-risk-register.md` — risk taxonomy with escalation thresholds
- `sprint-progress.md` — velocity metrics, blockers (recurring)
- `system-health.md` — health metrics vs. baseline (recurring)
- `sprint-risks.md` — current risk assessment (recurring)
- `copil.md` — steering committee preparation
- `gng-001-go-nogo.md` — final Go/No-Go decision with evidence

## Nestable

This workflow has `nestable: true` and is invoked as the Steer phase inside `sdlc-full`.

## Key differences from delivery-retrospective

- Proactive project governance, not retrospective analysis
- Includes project initialization and KPI baseline (P0)
- Sprint planning with feature batching, not post-delivery review
- Produces Go/No-Go decision documents, not improvement recommendations
- 10 stations across 4 systems (delivery-retrospective has 5 sequential stations)
- Recurring sprint tracking with warning-level gates for continuous monitoring
