---
name: delivery-metrics
description: 'Collect and analyze delivery metrics including cycle time, defect rates, throughput, and bottleneck identification for retrospectives.'
triggers: ['delivery metrics', 'cycle time', 'throughput analysis', 'delivery performance', 'retrospective metrics']
---

# Skill: delivery-metrics

## Goal

Collect and analyze delivery metrics to identify performance trends, bottlenecks, and improvement opportunities for delivery retrospectives.

## When to use

- In delivery-retrospective workflows to establish a data-driven baseline
- When measuring team delivery performance across sprints
- When identifying process bottlenecks

## Procedure

1. Collect raw metrics from available sources (Git history, issue trackers, CI/CD logs).
2. Calculate key delivery metrics:
   - Cycle time (idea to production)
   - Lead time (commit to deploy)
   - Throughput (features/stories per sprint)
   - Defect escape rate
   - Change failure rate
3. Identify trends (improving, stable, degrading).
4. Detect bottlenecks (longest phase in the pipeline).
5. Compare against team baselines or industry benchmarks.
6. Write the metrics report.

## Output

`specs/retrospectives/<sprint>/metrics.md`

## Rules

- Metrics must be based on data, not estimates.
- Always show trends over time, not just point-in-time values.
- Identify the top 3 bottlenecks with evidence.
