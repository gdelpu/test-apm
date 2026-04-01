# /workflow-bug-fixing

Run the Bug Fixing workflow for structured diagnosis and resolution.

## Steps

1. Read `.apm/workflows/bug-fixing.yml` for the station sequence.
2. Execute each station: triage → reproduce → root cause → fix →
   regression testing → quality validation → knowledge capture.
3. Write artifacts to `specs/bugs/<bug-id>/`.

## Inputs

- Bug description or issue reference
- Reproduction steps (if known)

## Outputs

- `specs/bugs/<bug-id>/triage.md`
- `specs/bugs/<bug-id>/reproduction.md`
- `specs/bugs/<bug-id>/root-cause.md`
- `specs/bugs/<bug-id>/fix-summary.md`
- `specs/bugs/<bug-id>/regression-tests.md`
- `specs/bugs/<bug-id>/quality-gate.md`
- `specs/bugs/<bug-id>/knowledge-update.md`
