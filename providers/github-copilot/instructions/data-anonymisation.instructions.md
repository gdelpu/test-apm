---
name: data-anonymisation
description: 'Instruction for all agents to detect and redact PII and sensitive data before including in outputs or model prompts.'
applyTo: '**'
---

# Data Anonymisation Instructions

## Pre-processing rule

Before including any of the following content types in your analysis or outputs, scan for and redact PII:

- **Copied tickets/incidents** — customer names, emails, phone numbers
- **Log fragments** — IP addresses, usernames, session tokens
- **UAT evidence** — customer data in screenshots or test results
- **Customer documents** — any personal or business-sensitive information
- **Screenshots converted to text** — OCR output may contain visible PII

## Redaction format

Replace detected PII with typed placeholders:

| PII type | Placeholder |
|----------|-------------|
| Email addresses | `[REDACTED:email]` |
| Phone numbers | `[REDACTED:phone]` |
| Social Security Numbers | `[REDACTED:ssn]` |
| Credit card numbers | `[REDACTED:credit-card]` |
| IP addresses | `[REDACTED:ipv4]` |
| IBAN numbers | `[REDACTED:iban]` |
| Belgian national numbers | `[REDACTED:belgian-rrn]` |
| API keys / tokens | `[REDACTED:secret-key]` |
| Names (when identifiable) | `[REDACTED:name]` |

## Generated test data

When generating test scenarios, use synthetic data only:
- Use `user@example.com` format for emails
- Use `+1-555-0100` to `+1-555-0199` for phone numbers (reserved test range)
- Use `192.0.2.x` for IP addresses (RFC 5737 documentation range)
- Never reproduce real customer data in test cases

## Output scanning

After composing your response, verify:
1. No real email addresses, phone numbers, or IDs are included
2. No API keys, tokens, or credentials are exposed
3. No production URLs or internal hostnames are revealed
4. Test data uses clearly synthetic values

## Sensitivity classification

Tag your output with the appropriate sensitivity level:
- **public**: no sensitive data, safe for external sharing
- **internal**: contains internal references but no PII
- **confidential**: contains or derived from customer/business data
- **restricted**: contains regulated data (financial, health, legal)
