---
name: observability-readiness
description: 'Assess observability readiness by verifying logging, metrics, tracing, and alerting coverage against release requirements.'
triggers: ['observability readiness', 'monitoring check', 'observability assessment', 'logging coverage']
---

# Skill: observability-readiness

## Goal

Assess whether a feature or service meets observability requirements — verifying that logging, metrics, tracing, and alerting are in place and configured correctly before release.

## When to use

- In release-readiness workflows before go/no-go decisions
- When verifying observability NFRs are met
- Before production deployments

## Procedure

1. Load the specification and NFR review for observability requirements.
2. Check logging coverage: are critical paths logged with structured logging?
3. Check metrics: are business and technical metrics exposed?
4. Check tracing: is distributed tracing configured for cross-service calls?
5. Check alerting: are alerts defined for SLO/SLA thresholds?
6. Check dashboards: do monitoring dashboards exist for the service?
7. Identify gaps and classify severity (critical / recommended / nice-to-have).
8. Write the observability readiness report.

## Output

`outputs/specs/features/<feature>/observability-readiness.md`

## Rules

- All user-facing services must have logging, metrics, and alerting at minimum.
- Distributed systems must have tracing configured.
- Alerting must be tied to SLOs, not arbitrary thresholds.
