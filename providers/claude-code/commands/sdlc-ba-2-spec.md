# /sdlc-ba-2-spec

Execute the **BA System S2 — Specification** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-ba.yml` — stations `ba-domain-model` through `ba-business-rules`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for ba-2.1 through ba-2.3.
3. Execute:
   - 2.1 (domain model) alone.
   - 2.2 (epic decomposition) — produces `epics/`.
   - 2.2b (feature spec) per epic — fan-out, up to max_concurrency in parallel.
   - 2.3 (business rules) — fan-in, waits for all features.
4. Write to `docs/1-prd/`.
5. Suggest `/sdlc-validate`.

Prerequisites: S1 (scoping) deliverables must exist with status `validated`.

$ARGUMENTS supports:
- `--scope sprint-N` — process only epics/features planned for sprint N.

## Outputs

- `dom-001-domain-model.md` — domain model with Mermaid ER
- `epics/` — epic decomposition
- `features/` — per-feature specifications
- `business-rules/` — classified and dispatched rules
