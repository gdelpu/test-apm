# /sdlc-tech-4-quality

Execute the **Tech System T4 — Continuous Quality** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-drift` and `tech-e2e-gen`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for tech-t4.1 and tech-t4.2.
3. Execute:
   - Wave 1: t4.1 (Drift Detection — specs vs code comparison).
   - Wave 2: t4.2 (E2E Playwright script generation).
4. **Write every report as an actual file on disk** under `outputs/docs/2-tech/4-quality/`. Do not merely display content in chat — use file-writing tools to create each file.
5. Display summary with drift findings.

This pipeline can be run repeatedly (per PR or before release).

Prerequisites: T2 deliverables must exist. Source code must be available.

## Outputs

- `drift-report.md` — spec-vs-code discrepancies
- `e2e-scripts-001-playwright.md` — generated E2E scripts
