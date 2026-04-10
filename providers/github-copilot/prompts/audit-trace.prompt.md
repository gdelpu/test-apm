---
name: audit-trace
description: 'Review and query structured audit traces for a feature workflow execution.'
---

# /audit-trace

Review the audit trace for a feature's workflow execution.

## Usage

```
/audit-trace <feature-name>
```

## What this does

1. Reads the audit trace file at `outputs/specs/features/<feature>/audit-trace.jsonl`
2. Summarises the workflow execution:
   - Total stations executed
   - Correlation ID (trace_id)
   - Risk scores per station
   - PII detections and redactions applied
   - Human review flags triggered
   - Model usage (tokens, latency) when available
3. Flags any anomalies:
   - Stations with high risk scores
   - Stations where PII was detected but not redacted
   - Missing trace records (gaps in station chain)
   - Unusually high token usage

## Output format

Present a summary table:

| Station | Risk | PII Found | Redacted | Review Required | Duration |
|---------|------|-----------|----------|-----------------|----------|

Followed by detailed findings for any flagged stations.

## When to use

- After completing a workflow to review the audit trail
- During compliance reviews or audits
- When investigating data handling in a feature's execution history
- Before releasing a feature that processed sensitive data
