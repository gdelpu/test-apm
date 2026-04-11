# /workflow-feature

Run the Feature Implementation workflow for a new feature.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project). Ask the user if not already clear.

## Steps

1. Read `.apm/workflows/feature-implementation.yml` for the station sequence.
2. **Initialise workflow state** using the canonical state tracker:
   ```bash
   cd .apm/hooks && python -m engine --state init \
     --workflow feature-implementation --feature <feature> \
     --stations "constitution,brownfield-context,specification,clarification,architecture-review,plan,task-breakdown,implementation,quality-validation,final-gate" \
     --trace-file outputs/specs/features/<feature>/audit-trace.jsonl
   ```
   Capture the returned `trace_id` for all subsequent calls.
3. **Always start at station 1 (constitution)** — never skip ahead to specification.
   Use the brownfield or greenfield constitution template accordingly.
4. For brownfield projects, execute the `brownfield-context` station next
   to produce `context-brief.md` with existing architecture and constraints.
5. **Before each station**, mark it running:
   ```bash
   cd .apm/hooks && python -m engine --state update \
     --feature <feature> --station <id> --status running \
     --trace-id <tid> --workflow feature-implementation \
     --trace-file outputs/specs/features/<feature>/audit-trace.jsonl
   ```
6. **After each station**, mark it passed (or failed):
   ```bash
   cd .apm/hooks && python -m engine --state update \
     --feature <feature> --station <id> --status passed --gate pass \
     --trace-id <tid> --workflow feature-implementation \
     --trace-file outputs/specs/features/<feature>/audit-trace.jsonl
   ```
7. Continue through the remaining stations in order:
   specification → clarification → architecture review → plan → task breakdown →
   implementation → quality validation → final gate.
8. **Write every artifact as an actual file on disk** under `outputs/specs/features/<feature>/`. Do not merely display content in chat — use file-writing tools to create each file.
9. After each station, verify that declared output files exist on disk before proceeding.

If $ARGUMENTS contains "skip-brownfield", skip the brownfield-context station (greenfield mode).

## Inputs

- Feature name or description from user
- Project context: brownfield or greenfield

## Outputs

- `outputs/specs/features/<feature>/constitution.md`
- `outputs/specs/features/<feature>/context-brief.md` (brownfield only)
- `outputs/specs/features/<feature>/spec.md`
- `outputs/specs/features/<feature>/clarifications.md`
- `outputs/specs/features/<feature>/architecture-review.md`
- `outputs/specs/features/<feature>/plan.md`
- `outputs/specs/features/<feature>/tasks.md`
- `outputs/specs/features/<feature>/quality-gate.md`
