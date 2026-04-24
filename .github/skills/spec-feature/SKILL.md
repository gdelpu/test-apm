---
name: spec-feature
description: 'Produce a functional feature specification that explains what should be built, for whom, why, and how success will be judged.'
triggers: ['feature specification', 'feature spec', 'requirements documentation']
---

# Skill: spec-feature

## Goal

Produce a functional feature specification that explains what should be built, for whom, why, and how success will be judged.

## When to use

- When a new feature needs a formal specification before planning
- As a station in the feature-implementation or modernization workflow

## Procedure

1. Load the constitution and any reverse brief for context
2. Select the matching template from `resources/` based on work type:
   - Standard feature → `resources/feature-spec-template.md`
   - API extension → `resources/api-extension-template.md`
   - Modernization → `resources/modernization-template.md`
3. Define scope, out-of-scope, user stories, and acceptance criteria
4. Include NFR expectations where applicable
5. Use the `edit/editFiles` tool to create `outputs/specs/features/<feature>/spec.md`

## Output

`outputs/specs/features/<feature>/spec.md`

## Rules

- Focus on outcomes and behavior, not implementation detail.
- Include scope and out-of-scope.
- State acceptance criteria in testable language.

## Resources

| Resource | Purpose |
|----------|----------|
| `resources/feature-spec-template.md` | Standard feature spec template |
| `resources/api-extension-template.md` | API extension spec template |
| `resources/modernization-template.md` | Modernization spec template |
