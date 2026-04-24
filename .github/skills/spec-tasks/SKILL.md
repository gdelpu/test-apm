---
name: spec-tasks
description: 'Break down the implementation plan into reviewable, sequenced tasks.'
triggers: ['task breakdown', 'task sequencing', 'implementation tasks']
---

# Skill: spec-tasks

## Goal

Break down the implementation plan into reviewable, sequenced tasks.

## When to use

- After the implementation plan is finalized
- As a station in the feature-implementation or modernization workflow

## Procedure

1. Load the plan, spec, and constitution for context
2. Load `resources/task-breakdown-template.md` as the output structure
3. Decompose plan phases into individual tasks with dependencies
4. Include test tasks using `resources/test-strategy-template.md` as reference
5. Sequence tasks respecting dependencies
6. Mark each task with type: implementation, testing, documentation, or rollout
7. Use the `edit/editFiles` tool to create `outputs/specs/features/<feature>/tasks.md`

## Output

`outputs/specs/features/<feature>/tasks.md`

## Rules

- Separate implementation, testing, documentation, and rollout tasks.
- Include explicit regression testing for brownfield work.
- Prefer small, testable tasks.

## Resources

| Resource | Purpose |
|----------|----------|
| `resources/task-breakdown-template.md` | Task breakdown output template |
| `resources/test-strategy-template.md` | Test task reference template |
