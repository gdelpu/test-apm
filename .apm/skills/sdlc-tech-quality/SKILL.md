---
name: sdlc-tech-quality
description: 'Continuously monitor specification-to-code alignment through drift detection, automated code review, and E2E Playwright script generation.'
triggers: ['drift detection', 'code review', 'spec-code alignment', 'E2E scripts']
---

# Skill: sdlc-tech-quality

## Goal

Continuously monitor specification-to-code alignment through drift detection, automated code review, and E2E Playwright script generation from BA test plans.

## When to use

- During and after implementation phases (System T4)
- As continuous quality stations in the `sdlc-tech` workflow
- Triggered on code changes or specification updates
- Runs after each T3 Implementation wave gate passes

## Procedure

### Phase 1 — Drift Detection (agent t4.1)
1. Compare current codebase against specification deliverables
2. Identify discrepancies: missing implementations, extra features, specification violations
3. Produce drift report with categorized findings (critical, warning, info)
4. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/4-quality/dft-{id}-drift-report.md` with identifier `[DFT-xxx]`

### Phase 2 — Code Review (agent t4.2) — depends on Phase 1
1. Perform per-PR code review against architecture decisions and coding standards
2. Verify ADR compliance, security practices, and observability patterns
3. Produce structured review report with actionable findings

### Phase 3 — E2E Playwright Generation (agent t4.3)
1. Read BA E2E test plan `[E2E-PLAN-001]` and test scenarios `[SCE-xxx]`
2. Generate cross-US, cross-feature Playwright test scripts
3. Use the `edit/editFiles` tool to create `outputs/docs/2-tech/4-quality/e2e-scripts-001-playwright.md` with identifier `[E2E-SCRIPTS-001]`

## Output

- `outputs/docs/2-tech/4-quality/dft-{id}-drift-report.md` — `[DFT-xxx]`
- Code review reports
- `outputs/docs/2-tech/4-quality/e2e-scripts-001-playwright.md` — `[E2E-SCRIPTS-001]`

## Rules

- Drift detection runs against the latest committed code
- Code review references ADRs and stack conventions for compliance
- E2E scripts must map to BA test scenarios for traceability
- T4 agents do not block the main pipeline (gate_after: false)

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/sk-t3.1-drift-detection.md` | Detailed drift detection procedure |
| `docs/sk-t3.2-code-review.md` | Detailed code review procedure |
| `docs/sk-t3.3-e2e-playwright-gen.md` | E2E generation procedure |
