# Workflow: Delivery Retrospective

AI-native continuous improvement cycle analyzing delivery metrics, defects, bottlenecks, and producing actionable improvements.

## When to use

- After completing a delivery cycle (sprint, release, or feature)
- Periodic health checks on the SDLC pipeline
- When defect rates or cycle times trend upward
- Feeding improvement proposals back into the constitution and playbooks

## Stations

| # | Station | Agent | Skills | Gate | Severity |
|---|---------|-------|--------|------|----------|
| 1 | Cycle Time Analysis | spec-orchestrator | delivery-metrics | Station times measured, bottlenecks identified | warning |
| 2 | Defect Analysis | spec-orchestrator | delivery-metrics, quality-report | Categories tallied, escape rate calculated | warning |
| 3 | Bottleneck Identification | spec-orchestrator | delivery-metrics | Top 3 bottlenecks ranked | warning |
| 4 | Improvement Suggestions | architecture-governance | architecture-guardrails, delivery-metrics | Proposals prioritized by effort/impact | warning |
| 5 | Constitution / Playbook Update | spec-orchestrator | knowledge-update, adr-generation | ADRs or playbook entries created | warning |

## Outputs

All artifacts are written to `specs/features/<feature>/`:
- `cycle-time-report.md` — Per-station cycle time and trends
- `defect-report.md` — Defect categories, frequencies, escape rate
- `bottleneck-report.md` — Top bottlenecks with contributing factors
- `improvement-proposals.md` — Prioritized improvement suggestions
- `retrospective-actions.md` — ADRs, playbook updates, action items

## Gate severity

All gates are `warning` severity — this is an advisory workflow. Findings are recommendations, not blockers.

## Composition

Runs standalone after any delivery workflow. Outputs feed back into `knowledge/` and `specs/decisions/` for the next cycle.

## Data sources

The workflow reads workflow state files, quality reports, and implementation logs from previous workflow runs to compute metrics. If no prior data exists, it produces a baseline report.
