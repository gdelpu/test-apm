# Skill: spec-plan

## Goal

Produce an implementation plan that explains how the feature will be delivered.

## When to use

- After the feature spec and clarifications are complete
- As a station in the feature-implementation or modernization workflow

## Procedure

1. Load the constitution, spec, and clarifications for context
2. Load `resources/implementation-plan-template.md` as the output structure
3. Define architectural approach, component breakdown, and sequencing
4. Assess risks using `resources/risk-template.md`
5. Define rollout and rollback strategy using `resources/rollout-template.md`
6. Include observability and monitoring considerations
7. Write `specs/features/<feature>/plan.md`

## Output

`specs/features/<feature>/plan.md`

## Rules

- Greenfield: choose the simplest viable architecture.
- Brownfield: reuse existing boundaries and patterns unless explicitly changing them.
- Include risks, rollout, rollback, and observability.

## Resources

| Resource | Purpose |
|----------|----------|
| `resources/implementation-plan-template.md` | Implementation plan template |
| `resources/risk-template.md` | Risk assessment template |
| `resources/rollout-template.md` | Rollout and rollback template |
