# Skill: spec-clarify

## Goal

Turn ambiguity into explicit decisions, assumptions, or open questions.

## When to use

- After a spec draft reveals gaps, contradictions, or undefined edge cases
- When the spec-orchestrator detects unresolved items before planning
- When NFR review surfaces questions that need stakeholder input

## Procedure

1. Load the current spec and any reverse brief
2. Walk through `resources/clarify-checklist.md` to identify functional gaps
3. Walk through `resources/nfr-clarify-checklist.md` to identify non-functional gaps
4. Categorize each item as: decision (resolved), assumption (stated), or open question
5. Write `specs/features/<feature>/clarifications.md`

## Output

`specs/features/<feature>/clarifications.md`

## Resources

| Resource | Purpose |
|----------|----------|
| `resources/clarify-checklist.md` | Functional clarification checklist |
| `resources/nfr-clarify-checklist.md` | Non-functional clarification checklist |
