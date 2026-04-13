# /workflow-bug-fixing

Run the Bug Fixing workflow for structured diagnosis and resolution.

## Steps

1. Read `.apm/workflows/bug-fixing.yml` for the station sequence.
2. **Initialise workflow state**:
   ```bash
   cd .apm/hooks && python -m engine --state init \
     --workflow bug-fixing --feature <bug-id> \
     --stations "triage,reproduce,root-cause,fix,regression,quality,knowledge"
   ```
   Capture the returned `trace_id` and `run_dir`. State and trace files are auto-created under `outputs/runs/bug-fixing/<timestamp>-<bug-id>-<short-tid>/`.
3. Before each station, run `python -m engine --state update --station <id> --status running --trace-id <tid> --workflow bug-fixing`.
   After each station, run `python -m engine --state update --station <id> --status passed --gate pass --trace-id <tid> --workflow bug-fixing`.
4. Execute each station: triage → reproduce → root cause → fix →
   regression testing → quality validation → knowledge capture.
5. **Write every artifact as an actual file on disk** under the run directory returned by init. Do not merely display content in chat — use file-writing tools to create each file.

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
