# /audit-trace — Review workflow audit traces

Review the structured audit trace for a feature's workflow execution.

## Usage

```
/audit-trace <feature-name>
```

## Steps

1. Read `outputs/specs/features/<feature>/audit-trace.jsonl`
2. Parse each JSONL line as a trace record
3. Summarise:
   - Correlation ID (trace_id)
   - Total stations executed
   - Risk scores per station
   - PII detections and redactions applied
   - Human review flags triggered
   - Model usage (tokens, latency) when available
4. Flag anomalies:
   - Stations with high risk scores (≥30)
   - PII detected but not redacted
   - Missing trace records (gaps in station chain)
   - Unusually high token usage
5. Present summary table and detailed findings

## Output format

```
| Station | Risk Score | Level | PII Found | Redacted | Review Required |
|---------|-----------|-------|-----------|----------|-----------------|
```

## When to use

- After completing a workflow to review the audit trail
- During compliance reviews
- When investigating data handling in a feature's execution history
- Before releasing a feature that processed sensitive data
