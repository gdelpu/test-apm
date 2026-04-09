---
name: parity-validation
description: 'Validate behavioral and API parity between old and new system implementations during modernization or refactoring.'
triggers: ['parity validation', 'parity check', 'behavioral parity', 'API parity', 'migration validation']
---

# Skill: parity-validation

## Goal

Validate that a new or refactored implementation maintains behavioral and API parity with the old system, catching regressions and contract violations before they reach production.

## When to use

- In modernization workflows after implementation to verify migration correctness
- In refactoring workflows to ensure behavior is preserved
- When the refactor-parity-checker agent needs to validate a migration

## Procedure

1. Load the migration plan and implementation log for context.
2. Identify parity dimensions to validate:
   - API contract parity (endpoints, request/response schemas, status codes)
   - Behavioral parity (same inputs produce same outputs)
   - Data parity (data migration completeness and correctness)
   - Performance parity (response times within acceptable variance)
3. For each dimension, compare old vs new system behavior.
4. Document any intentional divergences (from ADRs or spec).
5. Flag unintentional divergences as parity violations.
6. Classify violations by severity (critical / warning / informational).
7. Write the parity report.

## Output

`specs/features/<feature>/parity-report.md`

## Gate criteria

- **Pass**: No critical parity violations, all intentional divergences documented
- **Fail**: Critical parity violations detected
- **Warning**: Non-critical divergences that may need review

## Rules

- Intentional divergences must be traceable to an ADR or spec decision.
- API contract changes are critical violations unless explicitly approved.
- Performance variance > 20% from baseline is a warning; > 50% is critical.
