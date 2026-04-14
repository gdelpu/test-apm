# Hooks Setup Guide

> How to configure, use, and customise lifecycle hooks in your consumer project.

> **New to hooks?** See [Concepts & Glossary](../concepts.md#hooks) for what hooks are and how they fit into the architecture.
> **Full reference**: See [Hooks Reference](../reference/hooks.md) for the complete hook catalog and engine spec.

---

## Table of Contents

- [Overview](#overview)
- [What You Get After Install](#what-you-get-after-install)
- [Configuration](#configuration)
  - [Basic Settings](#basic-settings)
  - [PII Scanning](#pii-scanning)
  - [Risk Scoring](#risk-scoring)
  - [Client Profiles](#client-profiles)
  - [Observability (OTLP)](#observability-otlp)
- [How Hooks Run Per Provider](#how-hooks-run-per-provider)
  - [GitHub Copilot](#github-copilot)
  - [Claude Code](#claude-code)
  - [CLI](#cli)
- [Enabling and Disabling Hooks](#enabling-and-disabling-hooks)
- [Customising Hooks](#customising-hooks)
- [Environment Variables](#environment-variables)
- [Manual Usage](#manual-usage)
- [Troubleshooting](#troubleshooting)

---

## Overview

Hooks are pre/post execution interceptors that run around workflow stations. They provide:

- **PII scanning and redaction** — detects emails, phone numbers, credit cards, API keys, and more in station inputs and outputs
- **Prompt injection detection** — blocks jailbreaks, data exfiltration, and tool misuse attempts
- **Policy enforcement** — validates that agents only use allowed tools and network domains
- **Risk scoring** — aggregates findings into a risk score with optional human review escalation
- **Audit tracing** — emits structured JSONL trace records for every station execution

Hooks run automatically when you use workflows. No manual setup is required for default behaviour.

---

## What You Get After Install

After running the bootstrap or install script, your project has:

```
.apm/hooks/
├── _schema.md                    # Execution model documentation
├── config/
│   └── tool-paths.yml            # Tool path configuration
├── pre/
│   └── input-validation/         # Pre-hooks (5 files: base, ba, tech, steer, test)
├── post/
│   ├── quality-control.md        # Universal post-station quality checklist
│   └── confluence-push.md        # Optional Confluence publication (never blocks)
├── engine/                       # Python runtime engine (stdlib-only, zero deps)
│   ├── __main__.py
│   ├── pii_scanner.py
│   ├── injection_detector.py
│   ├── policy_authorizer.py
│   ├── risk_scorer.py
│   ├── trace_emitter.py
│   ├── state_tracker.py
│   ├── tool_tracker.py
│   └── schemas/
└── soprasteria-dep/              # Client overlay (Sopra Steria defaults)
```

The engine requires **Python 3.9+** with no external dependencies (stdlib only).

---

## Configuration

The install script automatically seeds a `hook-config.json` at your project root on first install. If the file already exists it is **not** overwritten, so your customisations survive updates.

> **No config file?** Hooks still work — the engine falls back to built-in defaults (everything enabled, default thresholds). The config file is only needed when you want to change behaviour.

If you need to recreate it manually:

```bash
cp .apm/templates/hook-config.json hook-config.json
```

Or on PowerShell:

```powershell
Copy-Item .apm/templates/hook-config.json hook-config.json
```

### Basic Settings

```json
{
  "enabled": true,
  "pii_scan_enabled": true,
  "injection_detection_enabled": true,
  "policy_check_enabled": true
}
```

Set `"enabled": false` to disable the entire hook framework. Individual features can be toggled independently.

### PII Scanning

```json
{
  "pii_scan_enabled": true,
  "redaction_mode": "mask",
  "pii_patterns_extra": []
}
```

| Setting | Values | Effect |
|---------|--------|--------|
| `redaction_mode` | `mask` / `hash` / `tag` | How detected PII is replaced in outputs |
| `pii_patterns_extra` | Array of regex strings | Additional PII patterns beyond the built-in set |

Built-in patterns detect: emails, phone numbers, SSN, credit cards, IPv4, IBAN, Belgian RRN, dates of birth, and API keys/tokens (GitHub PAT, OpenAI, AWS, PEM).

### Risk Scoring

```json
{
  "risk_threshold": 30,
  "risk_factor_weights": {
    "regulated_client": 2.0,
    "external_mcp": 1.5,
    "production_data": 1.8,
    "destructive_action": 2.0,
    "autonomous_execution": 1.5
  },
  "token_cost_threshold": 50000
}
```

When the aggregated risk score exceeds `risk_threshold`, the engine sets `human_review_required: true` in the trace record. Adjust weights to match your project's risk profile.

| Score range | Classification |
|-------------|---------------|
| 0–10 | `low` |
| 11–30 | `medium` |
| 31–60 | `high` |
| 61+ | `critical` |

### Client Profiles

For regulated or high-sensitivity projects:

```json
{
  "client_profile": "regulated-finance",
  "sensitivity_default": "confidential",
  "risk_factors_active": ["regulated_client", "production_data"]
}
```

Active risk factors are always scored, even when not detected from station metadata.

### Observability (OTLP)

Export traces to an OpenTelemetry-compatible collector:

```json
{
  "otlp_enabled": true,
  "otlp_endpoint": "https://otel-collector.internal:4318/v1/traces",
  "otlp_headers": {
    "Authorization": "Bearer ${OTLP_TOKEN}"
  }
}
```

When disabled, traces are written to local JSONL files only (`outputs/runs/<workflow>/audit-trace.jsonl`).

---

## How Hooks Run Per Provider

Hooks use the same `.apm/hooks/` directory regardless of provider. The invocation method differs:

### GitHub Copilot

The **Workflow Orchestrator** agent runs hooks via `runCommands`:

```bash
cd .apm/hooks && python -m engine --phase pre --trace-id <uuid> --station <id> --input <file>
```

If `runCommands` is blocked in your Copilot configuration, the orchestrator falls back to writing state files directly — hooks still fire at the agent-level (injected into prompts) but the engine-level hooks (PII scan, injection detection) are skipped. To enable full hook support, ensure `runCommands` is in the agent's tool list.

### Claude Code

Claude Code commands reference hooks through the same CLI. Commands like `/sdlc-ba`, `/sdlc-full`, and `/workflow-feature` invoke the engine if Python is available. The fallback is the same Markdown state-file approach.

### CLI

The CLI runner (`providers/cli/run-workflow.sh`) runs hooks **automatically** for every station:

1. Pre-hooks fire before station execution
2. Station runs
3. Post-hooks fire after station execution
4. Results are recorded in the audit trace

No additional configuration is needed — `run-workflow.sh` handles everything.

---

## Enabling and Disabling Hooks

All toggle settings go in `hook-config.json` at your project root (see [Configuration](#configuration) above for how to create it). If the file doesn't exist, hooks run with defaults (all enabled).

### Disable all hooks

Set `enabled` to `false` in `hook-config.json`:

```json
{
  "enabled": false
}
```

### Disable specific capabilities

Keep hooks enabled but turn off individual features in `hook-config.json`:

```json
{
  "enabled": true,
  "pii_scan_enabled": false,
  "injection_detection_enabled": true,
  "policy_check_enabled": false
}
```

### Disable a hook on a specific station

Station-level hooks are declared in workflow YAML files (`.apm/workflows/`). In **expandable** install mode, you can override workflow files via `providers-local/`. In **standard** mode, hook configuration is controlled entirely through `hook-config.json`.

---

## Customising Hooks

### Expandable mode

In expandable mode, you can override any hook by placing a file with the same relative path in your `providers-local/` directory. The projection script merges your overrides on top of upstream hooks.

### Adding custom PII patterns

Add regex patterns to `hook-config.json`:

```json
{
  "pii_patterns_extra": [
    "\\bEMP-\\d{6}\\b",
    "\\bCUST-[A-Z]{2}\\d{8}\\b"
  ]
}
```

These are scanned alongside built-in patterns during both pre and post phases.

### Adjusting allowed tools

Restrict which tools agents can use (enforced by the policy authorizer):

```json
{
  "allowed_tools": [
    "codebase", "search", "edit/editFiles", "problems"
  ]
}
```

Removing a tool from this list causes the policy hook to flag its usage.

---

## Environment Variables

### Confluence integration (optional)

The `post/confluence-push` hook publishes station outputs to Confluence. It requires:

| Variable | Description |
|----------|-------------|
| `CONFLUENCE_INSTANCE_URL` | e.g. `https://myorg.atlassian.net/wiki` |
| `CONFLUENCE_USER_EMAIL` | API authentication email |
| `CONFLUENCE_API_TOKEN` | API token (use `.env` file, never commit) |
| `CONFLUENCE_SPACE_KEY` | Target Confluence space |

Missing variables produce a `WARN` — the hook never blocks execution.

### Tool paths

Override tool locations via environment variables if they're not on `PATH`:

| Variable | Default | Description |
|----------|---------|-------------|
| `PANDOC_PATH` | `pandoc` | Pandoc binary for document conversion |
| `MMDC_PATH` | `mmdc` | Mermaid CLI for diagram rendering |
| `NODE_PATH` | `node` | Node.js runtime |

Configure these in `.apm/hooks/config/tool-paths.yml` or as environment variables.

---

## Manual Usage

You don't normally need to run hooks manually — they fire automatically during workflow execution. For debugging or retroactive scanning:

```bash
cd .apm/hooks

# Run pre-hooks on a file
python -m engine --phase pre --trace-id $(uuidgen) --station my-station --input path/to/input.md --json

# Run post-hooks on a station output
python -m engine --phase post --trace-id <same-uuid> --station my-station --output path/to/output.md --json

# Scan existing artifacts for PII (retroactive)
python -m engine --retroactive --path outputs/specs/features/my-feature/

# Pass a custom config
python -m engine --phase pre --trace-id $(uuidgen) --station test --input file.md --config ./hook-config.json
```

On PowerShell, replace `$(uuidgen)` with `(New-Guid).Guid`:

```powershell
cd .apm/hooks
python -m engine --phase pre --trace-id (New-Guid).Guid --station my-station --input path/to/input.md --json
```

---

## Troubleshooting

### Hooks don't run (Copilot)

**Symptom**: No audit trace files in `outputs/runs/`, no PII redaction in outputs.

**Cause**: `runCommands` is not in the Workflow Orchestrator's tool list, or Python is not available.

**Fix**:
1. Verify Python 3.9+ is installed: `python --version`
2. Check that `.apm/hooks/engine/__main__.py` exists in your project
3. Ensure the Workflow Orchestrator agent has `runCommands` in its `tools:` frontmatter

### Hook blocks a station unexpectedly

**Symptom**: Station fails with a blocking report instead of producing output.

**Cause**: Pre-hook detected a problem — usually missing/invalid inputs or a prompt injection pattern.

**Fix**:
1. Read the blocking report — it describes exactly what failed
2. For input validation failures: ensure input files have valid YAML frontmatter with `status: validated`
3. For injection false positives: review the flagged content and adjust if legitimate

### PII scanner flags false positives

**Symptom**: Content like reference numbers or internal codes get redacted.

**Fix**: The scanner uses regex patterns; certain data formats may match. Options:
1. Disable PII scanning: `"pii_scan_enabled": false` (not recommended)
2. Review and adjust — the scanner errs on the side of caution

### Risk score too high

**Symptom**: `human_review_required: true` on every station.

**Fix**: Raise the threshold or reduce active risk factor weights in `hook-config.json`:
```json
{
  "risk_threshold": 50,
  "risk_factor_weights": {
    "regulated_client": 1.5,
    "autonomous_execution": 1.0
  }
}
```

### Confluence push fails silently

**Symptom**: No Confluence pages created, but no errors either.

**Cause**: The `post/confluence-push` hook has `never_block: true` — failures are downgraded to warnings.

**Fix**: Check that all four Confluence environment variables are set (see [Environment Variables](#environment-variables)).
