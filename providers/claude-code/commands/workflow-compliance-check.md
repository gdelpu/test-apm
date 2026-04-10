# /workflow-compliance-check

Run the Compliance Check workflow for privacy, AI governance, and security validation.

## Steps

1. Read `.apm/workflows/compliance-check.yml` for the station sequence.
2. Execute each station: PII scan → prompt injection detection → policy validation →
   risk scoring → human approval → compliance report.
3. **Write every artifact as an actual file on disk** under `outputs/specs/features/<feature>/`. Do not merely display content in chat — use file-writing tools to create each file.
4. Track state in `outputs/specs/features/<feature>/workflow-state.md`.
5. Report overall compliance status (pass / conditional / fail) with gate results.

## Outputs

- `outputs/specs/features/<feature>/pii-report.md`
- `outputs/specs/features/<feature>/prompt-injection-report.md`
- `outputs/specs/features/<feature>/policy-report.md`
- `outputs/specs/features/<feature>/risk-score.md`
- `outputs/specs/features/<feature>/approval-record.md`
- `outputs/specs/features/<feature>/compliance-report.md`
