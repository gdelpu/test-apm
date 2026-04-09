---
name: intent-capture
description: 'Capture and structure a raw idea or business goal into a clear intent document with constraints, target users, and success criteria.'
triggers: ['intent capture', 'idea capture', 'business goal', 'feature intent', 'raw idea']
---

# Skill: intent-capture

## Goal

Transform a raw idea or business goal into a structured intent document that clearly states the desired outcome, constraints, target users, and success criteria — providing a solid foundation for specification.

## When to use

- As the first station in idea-to-spec workflows
- When a stakeholder has an idea that needs structuring before specification
- When the spec-orchestrator needs to establish intent before drafting a spec

## Procedure

1. Elicit the business goal: what outcome does the stakeholder want?
2. Restate the goal in outcome terms (not solution terms).
3. Identify target users or personas.
4. Document constraints and boundaries (budget, timeline, technology, compliance).
5. Define success criteria: how will we know this succeeded?
6. Capture any initial assumptions or risks.
7. Note related existing features or systems.
8. Write the intent document.

## Output

`specs/features/<feature>/intent.md`

## Rules

- Goals must be stated as outcomes, not solutions ("reduce checkout time" not "add caching").
- Constraints must be explicit — unstated constraints become surprises later.
- Success criteria must be measurable or at least observable.
- Do not jump to solutions during intent capture.
