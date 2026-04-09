---
name: risk-scoring
description: 'Compute an overall risk score by aggregating findings from PII scans, security reviews, and policy validations with weighted risk factors.'
triggers: ['risk scoring', 'risk assessment', 'risk score', 'compliance risk', 'risk aggregation']
---

# Skill: risk-scoring

## Goal

Compute an aggregate risk score from PII scan results, security review findings, and policy validation reports — providing a single numeric risk indicator with itemized factors.

## When to use

- In compliance-check workflows after PII scanning, injection detection, and policy validation
- When the workflow-orchestrator needs a go/no-go risk assessment
- Before human-approval gates to determine if review is required

## Procedure

1. Load all input reports (PII scan, prompt injection, policy validation).
2. For each finding, assign a risk weight based on severity:
   - Critical: 10 points
   - High: 7 points
   - Medium: 4 points
   - Low: 1 point
3. Apply category multipliers (security findings × 1.5, PII findings × 1.3).
4. Sum weighted scores to produce the aggregate risk score.
5. Classify the overall risk level:
   - 0–10: Low risk (auto-approve eligible)
   - 11–30: Medium risk (review recommended)
   - 31+: High risk (human approval required)
6. Itemize the top contributing risk factors.
7. Write the risk score report.

## Output

`risk-score.md`

## Gate criteria

- **Pass**: Risk score within acceptable threshold (configurable, default ≤ 30)
- **Fail**: Risk score exceeds threshold
- **Review**: Medium risk — proceed with human review

## Rules

- All input reports must be present before scoring — missing inputs are scored as critical gaps.
- Risk weights and thresholds should be configurable per project.
- The score formula must be transparent and reproducible.
