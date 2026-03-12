# Agent Factory — Station-Gate Workflow

A PR-driven, multi-station pipeline that validates every **agent** and **skill** change before merge.
Each _station_ runs its own checks and writes a structured JSON report to `station_out/`.
The **Policy Gate (A5)** aggregates all reports and either approves, blocks, or escalates for human review.

## Architecture

```
PR opened / updated
        │
        ▼
┌─────────────────────┐
│  A0 · Intake        │  Extract PR metadata → work_order.json
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  A1 · Policy &      │  JSON Schema validation · tool allowlists
│  Structure          │  → policy_report.json
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  A2 · Security      │  Secret scan · dependency scan
│  Static Checks      │  · dangerous-pattern scan
│                     │  → security_report.json
└────────┬────────────┘
         │
         ▼
┌──────────────────────────┐
│  A3 · Prompt Injection   │  Deterministic injection scanners +
│  & Exfil Hardening       │  optional Red Team Agent (read-only)
│                          │  → promptsec_report.json
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────┐
│  A4 · Sandbox       │  Simulate agent against malicious inputs
│  Simulation         │  / prompt-injection payloads
│                     │  → sim_report.json
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  A5 · Policy Gate   │  Aggregate all reports → APPROVE / BLOCK / REVIEW
│                     │  → gate_decision.json
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  A6 · GitHub Update │  Comment on PR · apply labels
│                     │  → (GitHub API side effects)
└─────────────────────┘
```

## Station Outputs

All station outputs are written to `station_out/` (created by A0).

| File | Station | Purpose |
|------|---------|---------|
| `work_order.json` | A0 | PR metadata, changed files, diff summary, risk hints |
| `policy_report.json` | A1 | Schema validation results |
| `security_report.json` | A2 | Secret / dependency / dangerous-pattern scan |
| `promptsec_report.json` | A3 | Prompt injection & exfil findings |
| `sim_report.json` | A4 | Sandbox simulation results |
| `gate_decision.json` | A5 | Final gate decision + justification |

## Station Files

| Station | File | Type |
|---------|------|------|
| A0 Intake | `stations/a0-intake.prompt.md` | Prompt |
| A1 Policy Validation | `stations/a1-policy-validation.prompt.md` | Prompt |
| A2 Security Static | `stations/a2-security-static.prompt.md` | Prompt |
| A3 Prompt Injection (deterministic) | `stations/a3-prompt-injection.prompt.md` | Prompt |
| A3 Red Team (AI) | `stations/a3-red-team.agent.md` | Agent |
| A4 Sandbox Simulation | `stations/a4-sandbox-simulation.prompt.md` | Prompt |
| A5 Policy Gate | `stations/a5-policy-gate.agent.md` | Agent |
| A6 GitHub Update | `stations/a6-github-update.prompt.md` | Prompt |

## Schemas

- `schemas/agent-manifest.schema.json` — required fields and constraints for `*.agent.md` frontmatter
- `schemas/skill-manifest.schema.json` — required fields and constraints for `SKILL.md` frontmatter

## Fixtures

- `fixtures/malicious-inputs.json` — structured malicious user inputs for sandbox simulation
- `fixtures/prompt-injection-payloads.json` — known injection payload patterns for A3/A4

## GitHub Actions

The CI orchestrator lives at `.github/workflows/agent-factory.yml`.
It triggers on PRs that touch `**/agents/**`, `**/skills/**`, `**/prompts/**`, or `**/instructions/**`.

## Severity Levels

| Level | Meaning | Gate outcome |
|-------|---------|-------------|
| `critical` | Immediate security risk; must be fixed before merge | ❌ BLOCK |
| `high` | Significant risk; requires explicit human approval | ⚠️ REVIEW |
| `medium` | Non-blocking; recommended fix | 🟡 WARN |
| `low` | Informational | ℹ️ INFO |
