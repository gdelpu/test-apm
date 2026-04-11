# /workflow-bug-fixing

Run the Bug Fixing workflow for structured diagnosis and resolution.

## Steps

1. Read `.apm/workflows/bug-fixing.yml` for the station sequence.
2. **Initialise workflow state**:
   ```bash
   cd .apm/hooks && python -m engine --state init \
     --workflow bug-fixing --feature <bug-id> \
     --stations "triage,reproduce,root-cause,fix,regression,quality,knowledge" \
     --trace-file outputs/specs/bugs/<bug-id>/audit-trace.jsonl
   ```
3. Before each station, run `python -m engine --state update --station <id> --status running ...`.
   After each station, run `python -m engine --state update --station <id> --status passed --gate pass ...`.
4. Execute each station: triage → reproduce → root cause → fix →
   regression testing → quality validation → knowledge capture.
5. **Write every artifact as an actual file on disk** under `outputs/specs/bugs/<bug-id>/`. Do not merely display content in chat — use file-writing tools to create each file.

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
