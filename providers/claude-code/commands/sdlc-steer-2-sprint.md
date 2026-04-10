# /sdlc-steer-2-sprint

Execute the **Steer System P2 — Sprint Tracking** pipeline (recurring).

## Steps

1. Read `.apm/workflows/sdlc-steer.yml` — stations `steer-sprint-progress` through `steer-sprint-risks`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for steer-p2.1 through steer-p2.3.
3. Execute:
   - Wave 1: p2.1 (Sprint Progress).
   - Wave 2: p2.2 (System Health).
   - Wave 3: p2.3 (Sprint Risks).
4. **Write every artifact as an actual file on disk** under `outputs/docs/3-steer/`. Do not merely display content in chat — use file-writing tools to create each file.

$ARGUMENTS: sprint number (e.g., "3" for Sprint 3). Sets the sprint context.

Prerequisites: P0 (init) and P1 (planning) deliverables must exist.

## Outputs

- `sprint-progress.md` — velocity metrics, blockers
- `system-health.md` — health metrics vs baseline
- `sprint-risks.md` — current risk assessment with escalation decisions
