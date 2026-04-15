# Convention: Test Agent Conventions

## Objective

Defines identifier prefixes, reporting conventions, and execution rules for Test agents.

---

## Identifier prefixes

| Prefix | Type | Produced by |
|--------|------|-------------|
| `CAM-E2E-` | Xray campaign | camp.1-launch |
| `CAMP-RPT-` | Campaign report | camp.2-report |
| `QUAL-GNG-` | Test Go/No-Go | camp.2-report |
| `PERF-EXEC-` | Performance execution context | perf.1-execution |
| `PERF-RPT-` | Performance report | perf.2-report |
| `DAST-RPT-` | DAST report | agent-dast |
| `DAST-VUL-` | DAST vulnerability | agent-dast |

## Upstream identifiers (read-only)

| Prefix | Type | Produced by |
|--------|------|-------------|
| `E2E-PLAN-` | E2E test plan | BA agent-3.6b |
| `E2E-FLX-` | E2E flow | BA agent-3.6b |
| `E2E-TST-` | E2E test case | BA agent-3.6b |
| `E2E-SCRIPTS-` | Playwright scripts | Tech agent-t4.3 |
| `DAT-TEST-` | Test seeds | BA agent-3.6 |
| `NFR-TEST-` | NFR test specs | Tech agent-nfr-test-specs |

## Key principles

1. **This system executes, it does not design** — plans and scripts come from upstream
2. **Xray is the source of truth** for functional test statuses
3. **A cumulative Go/No-Go** — `[QUAL-GNG-001]` aggregates functional + perf + security
4. **Never in production** — everything on qualification or staging environment
5. **Strict BLOCK on prerequisites** — never bypass entry criteria

## Report output location

All Test reports go to `outputs/docs/1-prd/4-tests/` (campaign/perf) or `outputs/docs/1-prd/5-tools/` (DAST).
Raw test results go to `tests/results/` (gitignored for JSON/XML, kept for Markdown).
