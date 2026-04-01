# /sdlc-test-1-campaign

Execute the **Test Campaign System** (E2E/UAT).

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for test-camp.1 and test-camp.2.
2. Execute:
   - Wave 1: camp.1 (Campaign Launch — prerequisites check, seeds, Xray creation).
   - Wave 2: camp.2 (Campaign Report — anomaly classification, Go/No-Go Test).
3. Display summary with pass/fail/blocked counts and Go/No-Go recommendation.

Prerequisites: BA deliverables (E2E plan, test data) and Tech deliverables (Playwright scripts) must exist. Application must be deployed on qualification/staging environment.

$ARGUMENTS: campaign type ("e2e" or "uat", default: "e2e").

## Outputs

- `campaign-report.md` — E2E/UAT results with Go/No-Go Test recommendation
