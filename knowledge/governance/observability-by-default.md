# Observability by Default

Critical flows should be observable from day one.

## Requirements

- Structured logs with correlation IDs for request tracing.
- Relevant metrics: latency, throughput, error rates for critical paths.
- Distributed traces for cross-service flows.
- Post-release verification steps defined before deployment.
- Alerting thresholds set based on SLOs, not arbitrary values.

## Monitoring

- Health check endpoints for all services.
- Dashboard per service with key business and technical metrics.
- Anomaly detection for traffic patterns and error rates.
