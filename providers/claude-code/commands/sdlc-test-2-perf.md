# /sdlc-test-2-perf

Execute the **Test Performance System**.

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for test-perf.1 and test-perf.2.
2. Execute:
   - Wave 1: perf.1 (Performance Campaign Execution — k6/Artillery scripts).
   - Wave 2: perf.2 (Performance Report — analysis vs thresholds, baseline comparison).
3. Display summary with metrics and Go/No-Go Perf recommendation.

Prerequisites: Tech deliverables (NFR test specs, k6/ZAP scripts) must exist. Application must be deployed on qualification/staging environment.

## Outputs

- `performance-report.md` — performance metrics with baseline comparison and Go/No-Go
