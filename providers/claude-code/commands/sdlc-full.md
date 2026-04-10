# /sdlc-full

Execute the **full SDLC pipeline** (BA + Tech + Test + Steer) without human gates.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project). Ask the user if not already clear. This affects:
- BA pipeline: brownfield runs S0 audit; greenfield skips to S1 scoping.
- Tech pipeline: brownfield runs T0 audit; greenfield skips to T1 architecture.

## Steps

1. Read `.apm/workflows/sdlc-full.yml` for the station sequence.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` for agent compositions.
3. Read `.apm/contexts/sdlc-system-context.md` for orchestration conventions.
4. Execute all 11 stations: scaffold → project init → BA pipeline (S0-S3, skipping S0 if greenfield) → sprint planning → Tech pipeline (T0-T3, skipping T0 if greenfield) → implementation → test campaigns → sprint tracking → quality validation → COPIL/Go-No-Go.
5. **Write every artifact as an actual file on disk** under `outputs/docs/`. Do not merely display content in chat — use file-writing tools to create each file.
6. Track state in `docs/workflow-state.md`.

If $ARGUMENTS contains "gated", pause at each phase boundary for human review.

## Inputs

- Project context or existing codebase (brownfield)
- Client input documents in `docs/0-inputs/`

## Outputs

- `outputs/docs/1-prd/` — BA deliverables (via nested `sdlc-ba`)
- `outputs/docs/2-tech/` — Tech deliverables (via nested `sdlc-tech`)
- `outputs/docs/3-steer/` — Steer deliverables (project sheet, KPIs, sprint plans, COPIL, Go/No-Go)
- `campaign-report.md`, `performance-report.md` — test results
- `quality-report.md` — from nested quality-validation
- `gng-001-go-nogo.md` — final Go/No-Go decision
