---
name: root-cause-analysis
description: 'Systematically investigate failures to identify root causes with evidence, contributing factors, and prevention recommendations.'
triggers: ['root cause analysis', 'root cause', 'RCA', 'failure analysis', 'why analysis']
---

# Skill: root-cause-analysis

## Goal

Systematically investigate a failure, incident, or bug to identify its root cause with evidence, document contributing factors, and recommend preventive measures.

## When to use

- In incident-resolution workflows after initial analysis
- In bug-fixing workflows to understand why a bug occurred
- Whenever a postmortem or failure investigation is needed

## Procedure

1. Gather evidence: logs, traces, error messages, timeline of events.
2. State the observed symptoms and their impact.
3. Formulate hypotheses for the root cause.
4. For each hypothesis:
   - Identify supporting evidence
   - Identify contradicting evidence
   - Rule in or rule out
5. Apply the "5 Whys" technique to drill past surface symptoms.
6. Identify contributing factors (conditions that enabled the root cause).
7. State the root cause with confidence level (high / medium / low).
8. Recommend preventive measures and monitoring improvements.

## Output

`outputs/specs/features/<feature>/root-cause.md`

## Rules

- Always consider and document at least one alternative hypothesis.
- Root cause must be supported by evidence, not intuition.
- Contributing factors are not the root cause — distinguish clearly.
- Recommendations must be actionable and testable.
