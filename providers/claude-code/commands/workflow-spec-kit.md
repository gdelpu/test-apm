# /workflow-spec-kit

Run the Spec Kit workflow to produce a complete specification without implementation.

## Steps

1. Read `.apm/workflows/spec-kit.yml` for the station sequence.
2. Execute each station: constitution → specification → clarification →
   architecture review → plan → tasks → test strategy → quality gate.
3. Write all artifacts to `specs/features/<feature>/`.

## Inputs

- Feature name or description from user

## Outputs

- `specs/features/<feature>/constitution.md`
- `specs/features/<feature>/spec.md`
- `specs/features/<feature>/clarifications.md`
- `specs/features/<feature>/architecture-review.md`
- `specs/features/<feature>/plan.md`
- `specs/features/<feature>/tasks.md`
- `specs/features/<feature>/test-strategy.md`
- `specs/features/<feature>/quality-gate.md`
