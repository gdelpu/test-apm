# Workflow: Compliance Check

Validate compliance, privacy, and AI governance requirements including PII scanning, prompt injection detection, and risk scoring.

## When to use

- Before releasing AI-powered features (EU AI Act compliance)
- When processing personal data (GDPR, PII requirements)
- Periodic compliance audits on existing systems
- When prompt injection risks need formal assessment
- Required by governance policies before production deployment

## Stations

| # | Station | Agent | Skills | Gate | Severity |
|---|---------|-------|--------|------|----------|
| 1 | PII Scan | quality-validator | governance-rules | No unprotected PII, data classified | blocker |
| 2 | Prompt Injection Detection | quality-validator | governance-rules, security-scan | No unescaped user input in prompts | blocker |
| 3 | Policy Validation | workflow-orchestrator | governance-rules | All policies checked, violations listed | blocker |
| 4 | Risk Scoring | workflow-orchestrator | risk-scoring | Risk score computed and within threshold | blocker |
| 5 | Human Approval | workflow-orchestrator | governance-rules | Reviewer sign-off recorded (optional) | warning |
| 6 | Compliance Report | workflow-orchestrator | governance-rules, quality-report | Summary with pass/conditional/fail status | blocker |

## Outputs

All artifacts are written to `outputs/specs/features/<feature>/`:
- `pii-report.md` — PII scan results and data classification
- `prompt-injection-report.md` — Prompt template and AI input analysis
- `policy-report.md` — Policy compliance evaluation
- `risk-score.md` — Itemized risk factors with overall score
- `approval-record.md` — Human approval record (if applicable)
- `compliance-report.md` — Consolidated compliance status and remediation roadmap

## Governance references

This workflow validates against rules defined in:
- `knowledge/governance/secure-by-default.md`
- `knowledge/governance/architecture-principles.md`
- `knowledge/governance/observability-by-default.md`
- `knowledge/constitution/principles.md`

## Composition

Can be nested inside `release-readiness` or `feature-implementation` as an additional validation station. Can also run standalone for periodic audits.

## AI Act relevance

Station 4 (Risk Scoring) aligns with EU AI Act risk classification. The workflow produces the documentation trail required for high-risk AI systems: data governance (PII scan), robustness (prompt injection), risk management (risk scoring), and human oversight (human approval).
