---
name: sdlc-test-performance
description: 'Execute performance tests (k6/Artillery), collect results, and analyze against defined thresholds with baseline comparison to detect regressions.'
---

# Skill: sdlc-test-performance

## Goal

Execute performance tests (k6/Artillery), collect results, and analyze against defined thresholds with baseline comparison to detect regressions.

## When to use

- After implementation and campaign testing
- As System E-Perf in the `sdlc-test` workflow
- Thresholds defined in Tech test strategy `[TST-001]`

## Procedure

### Phase 1 — Performance Execution (agent perf.1)
1. Read performance thresholds from `[TST-001]` test strategy
2. Execute k6 or Artillery performance test scripts
3. Collect JSON results: response times, throughput, error rates, resource utilization

### Phase 2 — Performance Report (agent perf.2) — depends on Phase 1
1. Analyze results against defined thresholds
2. Compare with baseline measurements for regression detection
3. Identify bottlenecks and degradation patterns
4. Write `[PERF-RPT-NNN]` performance report

## Output

- `[PERF-RPT-NNN]` — performance analysis report

## Rules

- Performance baselines must be established before regression comparison
- Thresholds come from the Tech test strategy — never hardcode defaults
- Reports must include both raw metrics and trend analysis

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/sk-perf.1-execution.md` | Performance execution procedure |
| `docs/sk-perf.2-report.md` | Performance report procedure |
