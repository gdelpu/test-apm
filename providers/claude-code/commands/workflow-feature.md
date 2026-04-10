# /workflow-feature

Run the Feature Implementation workflow for a new feature.

## Steps

1. Read `.apm/workflows/feature-implementation.yml` for the station sequence.
2. Execute each station in order: constitution → specification → clarification →
   architecture review → plan → task breakdown → implementation → quality validation → final gate.
3. Write all artifacts to `outputs/specs/features/<feature>/`.
4. Track state in `outputs/specs/features/<feature>/workflow-state.md`.

## Inputs

- Feature name or description from user
- Existing codebase context (for brownfield work)

## Outputs

- `outputs/specs/features/<feature>/constitution.md`
- `outputs/specs/features/<feature>/spec.md`
- `outputs/specs/features/<feature>/clarifications.md`
- `outputs/specs/features/<feature>/architecture-review.md`
- `outputs/specs/features/<feature>/plan.md`
- `outputs/specs/features/<feature>/tasks.md`
- `outputs/specs/features/<feature>/quality-gate.md`
