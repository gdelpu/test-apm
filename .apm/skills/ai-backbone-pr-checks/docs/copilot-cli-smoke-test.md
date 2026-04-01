# Copilot CLI Smoke Test

This file is a minimal PR trigger for validating AI Backbone PR checks and optional Copilot CLI advisory mode.

## Expected CI behavior

- Deterministic validators run and produce JSON reports.
- Copilot advisory runs only when `ENABLE_COPILOT_CLI=true`.
- Advisory output is uploaded as `reports/copilot-advisory.md`.

## Test marker

Created for controlled CI verification on 2026-03-11.
