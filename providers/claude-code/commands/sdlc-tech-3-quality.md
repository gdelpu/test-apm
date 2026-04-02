# /sdlc-tech-3-quality

Execute the **Tech System T3 — Continuous Quality** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-drift` and `tech-e2e-gen`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for tech-t3.1 and tech-t3.2.
3. Execute:
   - Wave 1: t3.1 (Drift Detection — specs vs code comparison).
   - Wave 2: t3.2 (E2E Playwright script generation).
4. Display summary with drift findings.

This pipeline can be run repeatedly (per PR or before release).

Prerequisites: T2 deliverables must exist. Source code must be available.

## Outputs

- `drift-report.md` — spec-vs-code discrepancies
- `e2e-scripts-001-playwright.md` — generated E2E scripts
