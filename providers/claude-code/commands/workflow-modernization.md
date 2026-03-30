# /workflow-modernization

Run the Modernization workflow for migrating an existing system.

## Steps

1. Read `.apm/workflows/modernization.yml` for the station sequence.
2. Execute each station: baseline assessment → target state → architecture review →
   migration plan → risk clarification → task breakdown → quality validation.
3. Write all artifacts to `specs/features/<initiative>/`.
4. Track state in workflow-state.md.

## Inputs

- Modernization initiative name or description
- Existing codebase and technology stack context

## Outputs

- `specs/features/<initiative>/baseline.md`
- `specs/features/<initiative>/target-state.md`
- `specs/features/<initiative>/architecture-review.md`
- `specs/features/<initiative>/migration-plan.md`
- `specs/features/<initiative>/risk-clarifications.md`
- `specs/features/<initiative>/tasks.md`
- `specs/features/<initiative>/quality-gate.md`
