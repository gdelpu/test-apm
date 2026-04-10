# /sdlc-steer-1-planning

Execute the **Steer System P1 — Planning** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-steer.yml` — stations `steer-sprint-plan` through `steer-risk-register`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for steer-p1.0 through steer-p1.2.
3. Execute:
   - Wave 1: p1.0 (Sprint Planning — unified BA+Tech stagger).
   - Wave 2: p1.1 (Roadmap — phases, milestones, gates).
   - Wave 3: p1.2 (Risk Register — all 6 agentic risk types).
4. Write to `outputs/docs/3-steer/`.
5. Suggest gate validation by sponsor + architect.

Prerequisites: P0 (init) deliverables must exist. BA scoping deliverables recommended.

## Outputs

- `plan-001-sprint-planning.md` — feature-to-sprint batching
- `rdp-001-roadmap.md` — phases, milestones, gates
- `rsk-001-risk-register.md` — risk taxonomy with escalation thresholds
