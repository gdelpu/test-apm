---
name: audit-tracing
description: 'Emit structured audit traces for every workflow station execution with correlation IDs, input/output hashes, sensitivity tags, risk scores, model metadata, and redaction status. Supports local JSONL persistence and optional OTLP export.'
triggers: ['audit trace', 'structured trace', 'audit trail', 'correlation ID', 'execution trace', 'observability', 'trace record', 'audit log']
version: '1.0.0'
---

# Skill: audit-tracing

## Goal

Produce a structured, machine-readable audit trail for every station execution in a workflow pipeline — capturing who did what, with what data sensitivity, at what risk level, and whether redaction was applied.

## When to use

- Automatically by the hook framework after every station execution
- When compliance requires a tamper-evident execution log
- When reviewing workflow execution history for a feature
- During incident investigation to trace data flow through stations

## Trace record fields

Each trace record captures:

| Field | Description |
|-------|-------------|
| `trace_id` | UUID correlation ID for the entire workflow run |
| `span_id` | UUID for this specific invocation |
| `parent_span_id` | Links to parent span (workflow → station → tool) |
| `timestamp` | ISO 8601 UTC |
| `workflow` / `station` / `agent` / `skill` | Execution context |
| `tool_invoked` | Tool name if applicable |
| `input_hash` / `output_hash` | SHA-256 hashes (never raw content) |
| `sensitivity.level` | public / internal / confidential / restricted |
| `sensitivity.tags` | e.g. pii, credentials, production-data |
| `sensitivity.pii_types` | Types of PII found (email, phone, etc.) |
| `risk.score` | Weighted numeric risk score |
| `risk.level` | low / medium / high / critical |
| `risk.factors` | Contributing factors |
| `risk.human_review_required` | Whether human review is needed |
| `model.provider` | github-copilot / claude-code / cli |
| `model.tokens_in` / `tokens_out` | Token counts (when available) |
| `model.cost_usd` / `latency_ms` | Cost and latency (when available) |
| `redaction.status` | applied / skipped / not-required |

## Storage

- **Local**: One JSONL file per workflow run at `specs/features/<feature>/audit-trace.jsonl`
- **Remote**: Optional OTLP export when `otlp_endpoint` configured in `hook-config.json`

## Schema

Validated against `.apm/hooks/engine/schemas/trace-record.schema.json`.

## Rules

- Raw content is NEVER stored in trace records — only SHA-256 hashes.
- Trace files are append-only during a workflow run.
- Correlation IDs propagate from workflow start through all station executions.
- OTLP export is optional and requires `opentelemetry-api` and `opentelemetry-exporter-otlp-proto-http`.
