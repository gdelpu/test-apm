# /sdlc-tech

Execute the **full Tech pipeline** (Systems T0 through T3) without human gates.

## Steps

1. Read `.apm/workflows/sdlc-tech.yml` for the station sequence.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` for Tech agent compositions.
3. Read `.apm/contexts/sdlc-system-context.md` for orchestration conventions.
4. Execute all 12 stations with `gate_mode: skip`:
   - T0: Brownfield technical audit + gap analysis (optional).
   - T1: System context (C4), ADRs, stack extraction, enabler index.
   - T2: Data model, API contracts, test strategy, implementation plan.
   - T3: Drift detection, E2E Playwright generation.
5. Write all artifacts to `outputs/docs/2-tech/`.

If $ARGUMENTS contains "gated", use `gate_mode: pause` at each system boundary.
If $ARGUMENTS contains "skip-audit", start from T1 architecture (greenfield mode).

Prerequisites: BA deliverables must exist with status `validated`.

## Inputs

- BA deliverables in `outputs/docs/1-prd/`
- Existing system technical documentation or codebase (brownfield)

## Outputs

- `outputs/docs/2-tech/` — all Tech deliverables (C4 context, ADRs, stack conventions, enablers, data model, API contracts, test strategy, implementation plan)
