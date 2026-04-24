---
name: governance-rules
description: 'Evaluate compliance against organizational governance policies including PII protection, prompt security, data classification, and regulatory requirements.'
triggers: ['governance rules', 'compliance check', 'policy validation', 'PII scan', 'data governance']
---

# Skill: governance-rules

## Goal

Evaluate artifacts and source code against organizational governance policies, covering PII protection, prompt security, data classification, and regulatory compliance requirements.

## When to use

- In compliance-check workflows for PII scanning and policy validation
- When the quality-validator or workflow-orchestrator needs governance assessment
- During human-approval gates when risk level triggers review

## Procedure

1. Load applicable governance policies from `.apm/knowledge/governance/`.
2. Scan source files for PII patterns (email, phone, SSN, IP addresses, names in datasets).
3. Check prompt templates for unescaped user inputs and injection vectors.
4. Verify data classification labels are applied where required.
5. Validate against organizational policy rules.
6. List violations with remediation steps.
7. Determine if human approval is required based on risk level.
8. Write the governance assessment.

## Output

Depends on station context:
- `pii-report.md` (PII scan station)
- `policy-report.md` (policy validation station)
- `approval-record.md` (human approval station)

## Rules

- PII detection uses pattern matching — flag uncertain matches for human review.
- All policy violations must include specific remediation guidance.
- High-risk findings require human sign-off before proceeding.
