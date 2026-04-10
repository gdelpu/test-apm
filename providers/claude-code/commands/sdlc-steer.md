# /sdlc-steer

Execute the **full Steer pipeline** (Systems P0 through P3) without human gates.

## Steps

1. Read `.apm/workflows/sdlc-steer.yml` for the station sequence.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` for Steer agent compositions.
3. Read `.apm/contexts/sdlc-system-context.md` for orchestration conventions.
4. Execute all 10 stations with `gate_mode: skip`:
   - P0: Project sheet, KPI baseline.
   - P1: Sprint planning, roadmap, risk register.
   - P2: Sprint progress, system health, sprint risks (recurring).
   - P3: COPIL preparation, Go/No-Go decision.
5. **Write every artifact as an actual file on disk** under `outputs/docs/3-steer/`. Do not merely display content in chat — use file-writing tools to create each file.

If $ARGUMENTS contains "gated", use `gate_mode: pause` at each system boundary.

## Inputs

- BA and Tech deliverables (for planning and governance)
- Sprint metrics (for P2 tracking)

## Outputs

- `outputs/docs/3-steer/` — all Steer deliverables (project sheet, KPIs, sprint plans, roadmap, risk register, COPIL, Go/No-Go)
