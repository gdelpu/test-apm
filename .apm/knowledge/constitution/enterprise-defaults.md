# Enterprise Defaults

Default quality expectations for enterprise delivery.

## Security

- Secure by default: auth, authorization, secrets handling, dependency review.
- OWASP Top 10 compliance for web applications.
- OWASP Top 10 for LLMs compliance for AI agents and workflows.
- No secrets in code — use environment variables or secret managers.

## Observability

- Critical flows must emit structured logs, metrics, and traces.
- Post-release verification steps are mandatory.
- Alerting thresholds defined before go-live.

## Testing

- Test-first development with ≥ 80% unit coverage (100% for critical paths).
- Integration and contract tests for all public interfaces.
- Deterministic tests only — no flaky tests in CI.

## Performance

- API endpoints: p95 < 200ms, p99 < 500ms.
- UI interactions: TTI < 3s, FCP < 1s.
- Design for 10x current load without architectural changes.

## Accessibility

- WCAG 2.1 Level AA minimum for all user-facing features.
- Keyboard navigation, screen reader support, color contrast.
