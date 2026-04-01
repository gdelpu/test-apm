---
name: code-refactoring
description: 'Execute safe, incremental refactoring of existing code to improve structure, readability, or maintainability without changing external behavior.'
triggers: ['refactoring', 'code improvement', 'maintainability', 'incremental refactoring']
---

# Skill: code-refactoring

## Goal

Execute safe, incremental refactoring of existing code to improve structure, readability, or maintainability without changing external behavior.

## When to use

- When the modernization-orchestrator needs to restructure code as part of migration
- When tech debt reduction tasks require targeted refactoring
- When code-implementation tasks involve restructuring existing modules

## Procedure

1. Load the migration plan or task breakdown for refactoring scope
2. Identify affected modules and their test coverage
3. Verify existing tests pass before refactoring (baseline)
4. Apply refactoring in small, testable increments
5. Run tests after each increment to confirm behavioral parity
6. Run build to confirm compilation and integration
7. Record changes and test results in refactoring log

## Output

Refactored code with passing tests and a refactoring log.

## Refactoring discipline

- Never change behavior and structure in the same step
- Ensure test coverage exists before refactoring; add tests first if missing
- Prefer standard refactoring patterns (extract, inline, rename, move)
- Keep commits small and reversible
- Document rationale for non-obvious structural changes

## Build and test commands

Uses the same project-specific commands as the `code-implementation` skill.
