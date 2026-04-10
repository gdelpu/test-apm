# /workflow-bug-fixing

Run the Bug Fixing workflow for structured diagnosis and resolution.

## Steps

1. Read `.apm/workflows/bug-fixing.yml` for the station sequence.
2. Execute each station: triage → reproduce → root cause → fix →
   regression testing → quality validation → knowledge capture.
3. Write artifacts to `outputs/specs/bugs/<bug-id>/`.

## Inputs

- Bug description or issue reference
- Reproduction steps (if known)

## Outputs

- `outputs/specs/bugs/<bug-id>/triage.md`
- `outputs/specs/bugs/<bug-id>/reproduction.md`
- `outputs/specs/bugs/<bug-id>/root-cause.md`
- `outputs/specs/bugs/<bug-id>/fix-summary.md`
- `outputs/specs/bugs/<bug-id>/regression-tests.md`
- `outputs/specs/bugs/<bug-id>/quality-gate.md`
- `outputs/specs/bugs/<bug-id>/knowledge-update.md`
