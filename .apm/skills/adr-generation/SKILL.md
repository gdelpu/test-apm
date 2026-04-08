---
name: adr-generation
description: 'Generate Architecture Decision Records (ADRs) capturing architecturally significant decisions with rationale, alternatives, and consequences.'
triggers: ['ADR', 'architecture decision', 'decision record', 'technical decision', 'architecture decision record']
---

# Skill: adr-generation

## Goal

Produce Architecture Decision Records that capture significant technical decisions with their context, rationale, alternatives considered, and consequences — ensuring institutional memory and traceability.

## When to use

- During modernization workflows when migration decisions need to be recorded
- In bug-fixing or incident-resolution when a fix reveals an architectural gap
- In BMAD workflows for decision tracking across iterations
- During delivery retrospectives to document lessons as decisions
- Any time an architecturally significant choice is made

## Procedure

1. Identify the decision to be recorded — what changed or was chosen, and why.
2. Capture context: what forces or constraints drove the decision.
3. Document alternatives considered with pros/cons for each.
4. State the decision clearly with its rationale.
5. List consequences — what follows from this decision (positive, negative, neutral).
6. Assign a confidence level (high / medium / low) based on evidence quality.
7. Link the ADR to related specs, plans, or prior ADRs.
8. Write the ADR using the standard template format.

## Output

`specs/features/<feature>/decisions/<ADR-ID>-<short-title>.md`

## ADR Template

```markdown
# ADR-<ID>: <Title>

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-<ID>

## Context
<What forces or constraints drive this decision?>

## Decision
<What was decided?>

## Rationale
<Why this option over alternatives?>

## Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|

## Consequences
- <What follows from this decision?>

## Confidence
High | Medium | Low

## References
- <Links to specs, plans, prior ADRs>
```

## Rules

- One ADR per decision — do not bundle unrelated decisions.
- ADRs are immutable once accepted — supersede with a new ADR if reversed.
- Every ADR must state at least one alternative that was considered.
- Confidence level must be justified with evidence or reasoning.
