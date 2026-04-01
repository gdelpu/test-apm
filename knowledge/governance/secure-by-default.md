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
