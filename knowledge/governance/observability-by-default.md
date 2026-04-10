# Observability by Default

Critical flows should be observable from day one.

## Requirements

- Structured logs with correlation IDs for request tracing.
- Relevant metrics: latency, throughput, error rates for critical paths.
- Distributed traces for cross-service flows.
- Post-release verification steps defined before deployment.
- Alerting thresholds set based on SLOs, not arbitrary values.

## Audit tracing

- Every workflow station execution MUST emit a structured trace record.
- Traces use correlation IDs (UUID) propagated from workflow start through all stations.
- Trace records contain input/output hashes (SHA-256), never raw content.
- Trace records include sensitivity tags, risk scores, redaction status, and model metadata.
- Local persistence as JSONL at `outputs/specs/features/<feature>/audit-trace.jsonl`.
- Optional OTLP export to external collectors when configured.
- Schema: `.apm/hooks/engine/schemas/trace-record.schema.json`.

## Monitoring

- Health check endpoints for all services.
- Dashboard per service with key business and technical metrics.
- Anomaly detection for traffic patterns and error rates.
