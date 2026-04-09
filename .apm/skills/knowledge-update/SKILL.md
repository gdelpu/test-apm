---
name: knowledge-update
description: 'Capture lessons learned from incidents or retrospectives as ADRs, playbook entries, or monitoring improvements for institutional knowledge.'
triggers: ['knowledge update', 'lessons learned', 'postmortem documentation', 'knowledge capture']
---

# Skill: knowledge-update

## Goal

Capture lessons learned from incidents, bug fixes, or retrospectives as permanent knowledge artifacts — ADRs, playbook entries, or monitoring improvement recommendations.

## When to use

- As the final station in incident-resolution workflows
- In delivery-retrospective workflows to document improvements
- After any significant production event that produced new insights

## Procedure

1. Load the incident analysis, root cause, fix plan, and validation report.
2. Determine the appropriate knowledge artifact type:
   - ADR — if an architectural decision was made or revealed
   - Playbook entry — if a new operational procedure was established
   - Monitoring improvement — if observability gaps were discovered
3. Write the knowledge artifact using the appropriate template.
4. Document preventive measures to avoid recurrence.
5. Recommend monitoring or alerting improvements.

## Output

`specs/features/<feature>/knowledge-update.md`

## Rules

- Every incident must produce at least one knowledge artifact.
- Preventive measures must be actionable, not aspirational.
- Link back to the original incident analysis and root cause.
