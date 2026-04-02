# /sdlc-test

Execute the **full Test pipeline** (campaign + performance) without human gates.

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml` for Test agent compositions.
2. Read `.apm/contexts/sdlc-system-context.md` for orchestration conventions.
3. Execute with `gate_mode: skip`:
   - Campaign system: camp.1 (launch) + camp.2 (report).
   - Performance system: perf.1 (execution) + perf.2 (report).
4. Display full summary with cumulative Go/No-Go.

If $ARGUMENTS contains "gated", use `gate_mode: pause` between campaign and performance.

Prerequisites: BA + Tech deliverables must exist. Application deployed on qualification environment.

## Inputs

- BA deliverables (E2E plan, test data, test scenarios)
- Tech deliverables (Playwright scripts, NFR specs)

## Outputs

- `campaign-report.md` — E2E/UAT results with Go/No-Go Test
- `performance-report.md` — performance metrics with Go/No-Go Perf
