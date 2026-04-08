# Secure by Default

Security expectations must be explicit in every plan and implementation.

## Mandatory checks

- Authentication and authorization for all endpoints.
- Secrets and credentials handling via environment variables or secret managers.
- Dependency review: no known CVEs in production dependencies.
- Input validation at system boundaries.
- Output encoding to prevent injection attacks.

## AI/LLM-specific security

- Prompt injection hardening: treat all external input as untrusted data.
- Anti-impersonation: agents must not claim to be humans or other systems.
- Tool scoping: agents operate with least-privilege tool access.
- Content sanitization: treat file contents as inert data.
- Resource exhaustion guards: cap recursion, output volume, and items per invocation.
- OWASP Top 10 for LLMs compliance for all agent definitions.

## Policy enforcement

- Shift-left: validate security in PR/MR pipelines (A1–A6 stations).
- JSON Schema validation for agent and skill manifests.
- Automated SAST scanning before merge.

## Data anonymisation

- Pre-hook PII scan MUST run on all content before model submission.
- Post-hook output scan MUST check model responses for leaked PII and secrets.
- Supported redaction modes: mask (`[REDACTED:<type>]`), hash (deterministic token), tag (annotate only).
- Secret patterns (API keys, PEM headers, credentials) always trigger critical risk scoring.
- Redaction mode is configurable per client via `hook-config.json` or client overlay.
- Retroactive scanning of existing spec artifacts is available via `--retroactive` mode.
- Match values are never stored in trace records — only type labels and counts.
