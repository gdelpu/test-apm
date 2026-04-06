# /workflow-compliance-check

Run the Compliance Check workflow for privacy, AI governance, and security validation.

## Steps

1. Read `.apm/workflows/compliance-check.yml` for the station sequence.
2. Execute each station: PII scan → prompt injection detection → policy validation →
   risk scoring → human approval → compliance report.
3. Write all artifacts to `specs/features/<feature>/`.
4. Track state in `specs/features/<feature>/workflow-state.md`.
5. Report overall compliance status (pass / conditional / fail) with gate results.

## Outputs

- `specs/features/<feature>/pii-report.md`
- `specs/features/<feature>/prompt-injection-report.md`
- `specs/features/<feature>/policy-report.md`
- `specs/features/<feature>/risk-score.md`
- `specs/features/<feature>/approval-record.md`
- `specs/features/<feature>/compliance-report.md`
