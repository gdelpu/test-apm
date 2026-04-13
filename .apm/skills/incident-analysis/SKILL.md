---
name: incident-analysis
description: 'Analyze production incidents by reconstructing timelines, identifying affected services, classifying severity, and collecting evidence from logs and traces.'
triggers: ['incident analysis', 'production incident', 'outage analysis', 'incident triage']
---

# Skill: incident-analysis

## Goal

Analyze a production incident by reconstructing the event timeline, identifying affected services and components, classifying impact severity, and collecting evidence from logs, metrics, and traces.

## When to use

- As the first station in incident-resolution workflows
- When a production incident needs initial assessment before diagnosis
- When the analysis-agent needs to scope an incident

## Procedure

1. Gather initial incident report details (alert, user report, monitoring trigger).
2. Reconstruct the timeline of events from earliest signal to current state.
3. Identify affected services, components, and data flows.
4. Classify impact: users affected, data integrity, service availability.
5. Assign severity (SEV-1 through SEV-4) based on impact scope.
6. Collect evidence: relevant logs, metrics, traces, error messages.
7. Identify any immediate mitigation actions taken or needed.
8. Write the incident analysis document.

## Output

`outputs/specs/features/<feature>/incident-analysis.md`

## Rules

- Timeline must be based on evidence (timestamps from logs/metrics), not assumptions.
- All affected services must be explicitly listed.
- If evidence is incomplete, state what is missing and what additional data sources to check.
- Do not propose root cause during analysis — focus on facts and evidence.
