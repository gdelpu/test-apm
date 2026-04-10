# /workflow-spec-kit

Run the Spec Kit workflow to produce a complete specification without implementation.

## Steps

1. Read `.apm/workflows/spec-kit.yml` for the station sequence.
2. Execute each station: constitution → specification → clarification →
   architecture review → plan → tasks → test strategy → quality gate.
3. Write all artifacts to `outputs/specs/features/<feature>/`.

## Inputs

- Feature name or description from user

## Outputs

- `outputs/specs/features/<feature>/constitution.md`
- `outputs/specs/features/<feature>/spec.md`
- `outputs/specs/features/<feature>/clarifications.md`
- `outputs/specs/features/<feature>/architecture-review.md`
- `outputs/specs/features/<feature>/plan.md`
- `outputs/specs/features/<feature>/tasks.md`
- `outputs/specs/features/<feature>/test-strategy.md`
- `outputs/specs/features/<feature>/quality-gate.md`
