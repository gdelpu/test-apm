# /workflow-compliance-check

Run the Compliance Check workflow for privacy, AI governance, and security validation.

## Steps

1. Read `.apm/workflows/compliance-check.yml` for the station sequence.
2. **Initialise workflow state**:
   ```bash
   cd .apm/hooks && python -m engine --state init \
     --workflow compliance-check --feature <feature> \
     --stations "pii-scan,injection-detection,policy-validation,risk-scoring,approval,report"
   ```
   Capture the returned `trace_id` and `run_dir`. State and trace files are auto-created under `outputs/runs/compliance-check/<timestamp>-<feature>-<short-tid>/`.
3. Before each station, run `python -m engine --state update --station <id> --status running --trace-id <tid> --workflow compliance-check`.
   After each station, run `python -m engine --state update --station <id> --status passed --gate pass --trace-id <tid> --workflow compliance-check`.
4. Execute each station: PII scan → prompt injection detection → policy validation →
   risk scoring → human approval → compliance report.
5. **Write every artifact as an actual file on disk** under the run directory returned by init. Do not merely display content in chat — use file-writing tools to create each file.
6. Report overall compliance status (pass / conditional / fail) with gate results.
7. **After each station completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all stations. Never leave the initial table stale.

## Outputs

- `outputs/specs/features/<feature>/pii-report.md`
- `outputs/specs/features/<feature>/prompt-injection-report.md`
- `outputs/specs/features/<feature>/policy-report.md`
- `outputs/specs/features/<feature>/risk-score.md`
- `outputs/specs/features/<feature>/approval-record.md`
- `outputs/specs/features/<feature>/compliance-report.md`
