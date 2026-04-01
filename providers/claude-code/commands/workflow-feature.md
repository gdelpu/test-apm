# /workflow-feature

Run the Feature Implementation workflow for a new feature.

## Steps

1. Read `.apm/workflows/feature-implementation.yml` for the station sequence.
2. Execute each station in order: constitution → specification → clarification →
   architecture review → plan → task breakdown → implementation → quality validation → final gate.
3. Write all artifacts to `specs/features/<feature>/`.
4. Track state in `specs/features/<feature>/workflow-state.md`.

## Inputs

- Feature name or description from user
- Existing codebase context (for brownfield work)

## Outputs

- `specs/features/<feature>/constitution.md`
- `specs/features/<feature>/spec.md`
- `specs/features/<feature>/clarifications.md`
- `specs/features/<feature>/architecture-review.md`
- `specs/features/<feature>/plan.md`
- `specs/features/<feature>/tasks.md`
- `specs/features/<feature>/quality-gate.md`
