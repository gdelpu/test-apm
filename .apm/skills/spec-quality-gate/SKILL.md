---
name: spec-quality-gate
description: 'Confirm that the specification package is complete, coherent, and safe enough for implementation.'
triggers: ['spec gate', 'specification review', 'go/no-go decision']
---

# Skill: spec-quality-gate

## Goal

Confirm that the specification package is complete, coherent, and safe enough for implementation.

## When to use

- As the final spec station before implementation begins
- When the spec-orchestrator needs a go/no-go decision on the spec package

## Procedure

1. Load all spec artifacts: constitution, spec, clarifications, plan, tasks, test strategy
2. Walk through `resources/quality-gate-checklist.md` to verify completeness
3. Check cross-references between spec, plan, and tasks for coherence
4. Verify NFR coverage against constitution expectations
5. Produce the quality gate report using `resources/pr-review-template.md` format
6. Use the `edit/editFiles` tool to create `outputs/specs/features/<feature>/quality-gate.md`

## Gate criteria

- **Pass**: All checklist items satisfied, no blocking gaps
- **Fail**: Missing critical sections, unresolved contradictions, or inadequate NFR coverage
- **Conditional**: Minor gaps noted with explicit assumptions

## Output

`outputs/specs/features/<feature>/quality-gate.md`

## Resources

| Resource | Purpose |
|----------|----------|
| `resources/quality-gate-checklist.md` | Completeness and coherence checklist |
| `resources/pr-review-template.md` | Review output template |
