# /sdlc-ba-3-design

Execute the **BA System S3 — Functional Design** pipeline (per feature).

## Steps

1. Read `.apm/workflows/sdlc-ba.yml` — stations `ba-user-stories` through `ba-e2e-plan`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for ba-3.1 through ba-3.6b.
3. Execute:
   - Discover all features from `docs/1-prd/3-epics/*/ft-*/`.
   - For each feature, run the per-feature sub-pipeline:
     Wave 1: 3.1 (user stories)
     Wave 2: 3.2 // 3.3 // 3.3c // 3.4 (parallel, with conditions)
     Wave 3: 3.3b (depends on 3.3)
     Wave 4: 3.5 (test scenarios)
     Wave 5: 3.6 (test data)
   - Features processed up to max_concurrency in parallel.
   - Fan-in: 3.6b (E2E test plan) at project scope.
4. Write to `docs/1-prd/`.
5. Suggest `/sdlc-validate` + `/sdlc-coherence`.

Prerequisites: S2 (specification) deliverables must exist with status `validated`.

$ARGUMENTS supports:
- `--scope sprint-N` — process only features planned for sprint N.

## Outputs

- `user-stories/` — atomic stories with GWT acceptance criteria (per feature)
- `user-journeys/` — E2E journey flows with Mermaid (per feature)
- `screen-specs/` — UI specifications (per feature, optional)
- `test-scenarios/` — Gherkin scenarios (per feature)
- `e2e-plan-001.md` — cross-feature E2E test plan
