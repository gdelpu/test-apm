# /sdlc-ba

Execute the **full BA pipeline** (Systems S0 through S3) without human gates.

## Steps

1. Read `.apm/workflows/sdlc-ba.yml` for the station sequence.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` for BA agent compositions.
3. Read `.apm/contexts/sdlc-system-context.md` for orchestration conventions.
4. Execute all 16 stations with `gate_mode: skip`:
   - Merge all BA systems (S0-S3) into one DAG.
   - Resolve waves and execute sequentially/in parallel per dependencies.
   - Handle fan-out for epics (S2) and features, then per-feature design (S3).
   - Handle fan-in for project-level deliverables (business rules, E2E plan).
5. Write all artifacts to `docs/1-prd/`.
6. At the end, suggest `/sdlc-coherence` for global consistency check.

If $ARGUMENTS contains "gated", use `gate_mode: pause` at each system boundary.
If $ARGUMENTS contains "skip-audit", start from S1 scoping (greenfield mode).

## Inputs

- Client input documents in `docs/0-inputs/ba/_source/`
- Existing system documents (brownfield) or project brief (greenfield)

## Outputs

- `docs/1-prd/` — all BA deliverables (vision, glossary, actors, requirements, domain model, epics, features, stories, journeys, test scenarios, E2E plan)
- `docs/1-prd/ba-validation-report.md` — final quality audit
