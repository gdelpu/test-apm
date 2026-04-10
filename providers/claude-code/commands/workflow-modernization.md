# /workflow-modernization

Run the Modernization workflow for migrating an existing system.

## Steps

1. Read `.apm/workflows/modernization.yml` for the station sequence.
2. Execute each station: baseline assessment → target state → architecture review →
   migration plan → risk clarification → task breakdown → quality validation.
3. Write all artifacts to `outputs/specs/features/<initiative>/`.
4. Track state in workflow-state.md.

## Inputs

- Modernization initiative name or description
- Existing codebase and technology stack context

## Outputs

- `outputs/specs/features/<initiative>/baseline.md`
- `outputs/specs/features/<initiative>/target-state.md`
- `outputs/specs/features/<initiative>/architecture-review.md`
- `outputs/specs/features/<initiative>/migration-plan.md`
- `outputs/specs/features/<initiative>/risk-clarifications.md`
- `outputs/specs/features/<initiative>/tasks.md`
- `outputs/specs/features/<initiative>/quality-gate.md`
