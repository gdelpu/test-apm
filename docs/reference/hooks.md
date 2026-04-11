# Hooks (7 + engine)

> Pre/post execution interceptors that fire around workflow stations. They operate at two levels: **agent-level** (injected into the agent's system prompt) and **station-level** (fire as sub-stations before/after execution).

See `.apm/hooks/_schema.md` for the full execution model.

Canonical definitions: `.apm/hooks/`. Engine: `.apm/hooks/engine/`.

---

## Hook Definitions

<!-- UPDATE this table when adding/removing hooks in .apm/hooks/ -->

| Hook | Type | Domain | Description |
|------|------|--------|-------------|
| `pre/input-validation/base` | Pre | Universal | Shared input validation protocol for all domains |
| `pre/input-validation/ba` | Pre | BA | Business analysis input validation extensions |
| `pre/input-validation/tech` | Pre | Tech | Technical domain input validation extensions |
| `pre/input-validation/steer` | Pre | Steer | Steering/project management validation extensions |
| `pre/input-validation/test` | Pre | Test | Test domain validation extensions (strict mode) |
| `post/quality-control` | Post | Universal | Universal quality checklist applied after station execution |
| `post/confluence-push` | Post | Universal | Best-effort Confluence publication (`never_block: true`) |

## Client Overlays

| Overlay | Source Hook | Description |
|---------|------------|-------------|
| `soprasteria-dep/pre-input-validation` | `pre/input-validation/*` | Sopra Steria pre-validation overlay |
| `soprasteria-dep/post-quality-control` | `post/quality-control` | Sopra Steria post-QC overlay |

## Engine (`engine/`)

The Python runtime engine provides audit tracing, PII detection/redaction, injection detection, policy authorisation, and risk scoring. It runs as station-level hooks during workflow execution (stdlib-only, zero external dependencies).

### Pre-hook chain (runs before station execution)

Hooks execute sequentially. A **block** from any hook aborts the station.

| # | Module | What it does | Can block? |
|---|--------|-------------|------------|
| 1 | `context_classifier` | Assembles station metadata: sensitivity level (`internal`/`confidential`/`restricted`), risk factors, client profile. Detects execution-mode indicators: **autonomous execution**, **destructive actions**, **production data exposure**, **external MCP tools**. Escalates sensitivity for regulated clients. | No |
| 2 | `pii_scanner` | Scans input content for PII using regex patterns: email, phone (international), SSN, credit card, IPv4, IBAN, Belgian RRN, date of birth, API keys/tokens (GitHub PAT, OpenAI, AWS, PEM). Redacts matches using configured mode (`mask` / `hash` / `tag`). | No (redacts) |
| 3 | `injection_detector` | Detects prompt injection attempts across 6 categories: **PI-01** jailbreak (12 patterns, critical), **PI-03** unconstrained input (3 patterns, high), **PI-04** data exfiltration (4 patterns, high — **blocks**), **PI-05** resource exhaustion (2 patterns, medium), **PI-06** tool misuse (4 patterns, high). | **Yes** (PI-04) |
| 4 | `policy_authorizer` | Enforces agent policy rules: **P-02** tool allowlist (hard block), **P-03** `commandAllowlist` advisory, **P-04** `allowedNetworkDomains` advisory. Advisories feed into risk scoring. | **Yes** (P-02) |

### Post-hook chain (runs after station execution)

| # | Module | What it does | Can block? |
|---|--------|-------------|------------|
| 5 | `pii_scanner` | Scans station **output** for leaked PII/secrets using the same patterns as pre-hook 2. Redacts before output is persisted. | No (redacts) |
| 6 | `risk_scorer` | Aggregates all findings into a weighted risk score: injection severity × security multiplier (1.5×), PII count × PII multiplier (1.3×), policy violations, plus **context risk factors** (see below). Classifies result as `low` (0–10) / `medium` (11–30) / `high` (31–60) / `critical` (61+). Sets `human_review_required` when score ≥ threshold (default 30). | No (advisory) |
| 7 | `trace_emitter` | Emits structured audit trace record to JSONL (one file per workflow run). Includes: trace/span IDs, timestamps, input/output SHA-256 hashes, sensitivity tags, risk score, redaction status, model metadata. Optional OTLP export. | No |

### Risk factors scored by hook 6

These are **not separate hooks** — they are weighted inputs to the risk scorer, detected by the context classifier (hook 1) and scored in hook 6.

| Risk factor | Weight | Human review forced? | How detected |
|-------------|--------|---------------------|--------------|
| **Regulated client** | ×2.0 | **Yes** | Client profile set in `hook-config.json` or client overlay |
| **Destructive actions** | ×2.0 | **Yes** | `extra_context.destructive` flag from station/workflow |
| **Production data exposure** | ×1.8 | **Yes** | `extra_context.production_data` flag; sensitivity escalated to `restricted` |
| **External MCP tools** | ×1.5 | No (score only) | `extra_context.external_mcp` flag |
| **Autonomous execution** | ×1.5 | No (score only) | `extra_context.autonomous` flag |
| **High token/tool cost** | threshold | No (score only) | `token_cost_threshold` in config (default: 50 000 tokens) |

### PII patterns detected (hooks 2 + 5)

| Pattern | Redaction placeholder | Example |
|---------|----------------------|---------|
| Email | `[REDACTED:email]` | `user@example.com` |
| Phone (international) | `[REDACTED:phone]` | `+32 2 123 4567` |
| SSN (US) | `[REDACTED:ssn]` | `123-45-6789` |
| Credit card | `[REDACTED:credit-card]` | `4111 1111 1111 1111` |
| IPv4 | `[REDACTED:ipv4]` | `192.168.1.1` |
| IBAN | `[REDACTED:iban]` | `BE68 5390 0754 7034` |
| Belgian RRN | `[REDACTED:belgian-rrn]` | `85.07.15-123.45` |
| Date of birth | `[REDACTED:date-of-birth]` | `1985-07-15` |
| API keys / tokens | `[REDACTED:secret-key]` | GitHub PAT, OpenAI key, AWS access key, PEM private keys |

### Usage

```bash
# Hooks run automatically via run-workflow.sh
# Manual invocation:
cd .apm/hooks
python -m engine --phase pre --trace-id <uuid> --station <id> --input <file> --json
python -m engine --phase post --trace-id <uuid> --station <id> --output <file> --json
python -m engine --retroactive --path outputs/specs/features/my-feature/   # scan existing artifacts
```

**Schema**: `engine/schemas/trace-record.schema.json` · **Config template**: `.apm/templates/hook-config.json`
