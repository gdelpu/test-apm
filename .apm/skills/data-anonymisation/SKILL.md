---
name: data-anonymisation
description: 'Detect and redact PII and sensitive data in content before model submission (pre-hook) and in model outputs (post-hook) using configurable regex patterns and redaction modes.'
triggers: ['data anonymisation', 'data anonymization', 'PII scan', 'PII redaction', 'redact sensitive data', 'mask PII', 'anonymise', 'anonymize', 'sensitive data scan']
version: '1.0.0'
---

# Skill: data-anonymisation

## Goal

Prevent PII and sensitive data from being sent to models unredacted (pre-hook) and from leaking into stored outputs (post-hook).  Operates as a configurable scanner and redactor with three modes.

## When to use

- **Pre-hook**: Before sending content to a model — scan and redact copied tickets, incident logs, customer documents, UAT evidence, screenshots-to-text OCR output
- **Post-hook**: After receiving model output — scan for leaked real data in generated test scenarios, synthetic responses, reports
- **Retroactive**: Scan and audit existing spec artifacts created before the hook framework was enabled

## Supported PII patterns

| Type | Pattern | Example |
|------|---------|---------|
| `email` | Standard email format | user@example.com |
| `phone` | International phone with optional + prefix | +32 2 123 4567 |
| `ssn` | US Social Security Number | 123-45-6789 |
| `credit-card` | Visa, MC, Amex card numbers | 4111 1111 1111 1111 |
| `ipv4` | IPv4 addresses | 192.168.1.1 |
| `iban` | International Bank Account Number | BE68 5390 0754 7034 |
| `belgian-rrn` | Belgian national number (rijksregisternummer) | 85.07.15-123.45 |
| `date-of-birth` | Date patterns (YYYY-MM-DD, DD/MM/YYYY) | 1985-07-15 |
| `secret-key` | GitHub PATs, OpenAI keys, AWS keys, PEM headers | ghp_abc123... |
| `generic-token` | token/api_key/secret/password assignments | api_key=abc123... |

Custom patterns can be added via `pii_patterns_extra` in `hook-config.json`.

## Redaction modes

| Mode | Behaviour | Use case |
|------|-----------|----------|
| `mask` (default) | Replace with `[REDACTED:<type>]` | General purpose, readable output |
| `hash` | Replace with `[HASH:<hex8>]` (deterministic SHA-256 prefix) | Re-identifiable by authorised party |
| `tag` | Annotate without modifying content | Audit-only, no redaction needed |

## Configuration

Configured via `hook-config.json` (or client overlay at `clients/<client>/hook-config.json`):

```json
{
  "redaction_mode": "mask",
  "pii_scan_enabled": true,
  "pii_patterns_extra": ["\\bCUSTOM_PATTERN\\b"]
}
```

## Retroactive mode

Scan existing spec artifacts for PII without modifying them:

```bash
python -m engine --retroactive --path specs/features/my-feature/
```

## Rules

- PII scan runs on ALL content before model submission — no opt-out for pre-hook.
- Redaction mode is configurable per client via client overlay.
- Secret patterns (API keys, PEM headers) always trigger critical risk scoring.
- Match values are never stored in trace records — only type labels and counts.
