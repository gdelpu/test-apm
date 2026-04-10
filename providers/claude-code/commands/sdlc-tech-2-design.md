# /sdlc-tech-2-design

Execute the **Tech System T2 — Technical Design** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-data-model` through `tech-impl-plan`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for tech-t2.1 through tech-t2.5.
3. Execute:
   - Wave 1: t2.1 (Data Model).
   - Wave 2: t2.2 // t2.3 // t2.6 (API + Enablers + Observability, parallel).
   - Wave 3: t2.4 (Test Strategy).
   - Wave 4: t2.5 (Implementation Plan + CLAUDE.md compilation).
4. Write to `outputs/docs/2-tech/`.
5. Suggest `/sdlc-validate`.

Prerequisites: T1 (architecture) deliverables must exist with status `validated`.

## Outputs

- `dat-001-data-model.md` — DDL-like data model with FK/indexes
- `api-contracts/` — OpenAPI-compliant per-endpoint contracts
- `tst-001-test-strategy.md` — test pyramid with coverage thresholds
- `imp-001-implementation-plan.md` — ordered wave implementation plan
