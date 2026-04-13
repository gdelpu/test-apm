# Testing Policy

Testing is risk-based but never optional.

## Requirements

- Test-first development: write tests before implementation (Red-Green-Refactor).
- Critical flows require automated verification — no exceptions.
- Brownfield changes require regression awareness and coverage.
- Tests must be deterministic and executable in isolation.

## Coverage targets

- Unit tests: ≥ 80% for all new code, 100% for critical paths.
- Integration tests: all API contracts, database operations, external services.
- Contract tests: all public interfaces and cross-service boundaries.

## Naming and structure

- Test names describe the scenario (Given-When-Then preferred).
- Tests run in CI/CD pipeline — no manual-only tests.
- Flaky tests are treated as bugs and fixed immediately.

## Agent/skill validation

- All agent definitions validated against JSON Schema manifests.
- Prompt injection payloads tested via sandbox simulation (A5 station).
- Policy compliance verified via deterministic validators (Phase 1 CI).
