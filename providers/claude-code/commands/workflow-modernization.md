# /workflow-modernization

Run the Modernization workflow for migrating an existing system.

## Steps

1. Read `.apm/workflows/modernization.yml` for the station sequence.
2. **Initialise workflow state**:
   ```bash
   cd .apm/hooks && python -m engine --state init \
     --workflow modernization --feature <initiative> \
     --stations "baseline,target-state,architecture-review,migration-plan,risk,tasks,quality" \
     --trace-file outputs/specs/features/<initiative>/audit-trace.jsonl
   ```
3. Before each station, run `python -m engine --state update --station <id> --status running ...`.
   After each station, run `python -m engine --state update --station <id> --status passed --gate pass ...`.
4. Execute each station: baseline assessment → target state → architecture review →
   migration plan → risk clarification → task breakdown → quality validation.
5. **Write every artifact as an actual file on disk** under `outputs/specs/features/<initiative>/`. Do not merely display content in chat — use file-writing tools to create each file.

## Inputs

- Modernization initiative name or description
- Existing codebase and technology stack context

## Outputs

- `outputs/specs/features/<initiative>/baseline.md`
- `outputs/specs/features/<initiative>/target-state.md`
- `outputs/specs/features/<initiative>/architecture-review.md`
- `outputs/specs/features/<initiative>/migration-plan.md`
- `outputs/specs/features/<initiative>/risk-clarifications.md`
- `outputs/specs/features/<initiative>/tasks.md`
- `outputs/specs/features/<initiative>/quality-gate.md`
