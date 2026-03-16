# Agent Factory — Station-Gate Workflow

An MR-driven, multi-station pipeline that validates every **agent** and **skill** change before merge.
Each _station_ runs its own checks and writes a structured JSON report to `station_out/`.
The **Policy Gate (A6)** aggregates all reports and either approves, blocks, or escalates for human review.

## Architecture

The pipeline runs in two phases:

1. **Validate** — deterministic Python scripts run in parallel.
2. **Stations** — once the blocking validators pass, the station orchestrator
   dynamically discovers every `*.prompt.md` / `*.agent.md` file in
   `station-workflows/stations/`, sorts by prefix, and executes them
   sequentially via GitHub Copilot CLI.

```
merge_request_event
  │
  ├─ validate (parallel)               ← Phase 1
  │   ├─ validate:pr-auto               Python deterministic   ⛔ gates
  │   ├─ validate:yaml-workflows        Python deterministic   ⛔ gates
  │   └─ validate:test-gaps             Python deterministic   advisory
  │
  └─ stations (sequential)             ← Phase 2 (needs pr-auto + yaml-workflows)
      └─ stations:run-all
           ├─ a0-intake.prompt.md       → work_order.json
           ├─ a1-policy-validation      → a1_result.json    ⛔ gates
           ├─ a2-security-static        → a2_result.json    ⛔ gates
           ├─ a3-prompt-injection       → a3_result.json    ⛔ gates
           ├─ a4-red-team.agent         → a4_result.json
           ├─ a5-sandbox-simulation     → a5_result.json    ⛔ gates
           ├─ a6-policy-gate.agent      → a6_result.json    ⛔ gates
           └─ a7-gitlab-update          → (GitLab API side effects)
```

Adding or removing a station requires **no CI YAML changes** — just add/remove
the file in `stations/` and the orchestrator picks it up automatically.

## Station Outputs

All station outputs are written to `station_out/` (created by A0).

| File | Station | Purpose |
|------|---------|---------|
| `work_order.json` | A0 | PR metadata, changed files, diff summary, risk hints |
| `policy_report.json` | A1 | Schema validation results |
| `security_report.json` | A2 | Secret / dependency / dangerous-pattern scan |
| `promptsec_report.json` | A3/A4 | Prompt injection & exfil findings |
| `sim_report.json` | A5 | Sandbox simulation results |
| `gate_decision.json` | A6 | Final gate decision + justification |

## Station Files

| Station | File | Type |
|---------|------|------|
| A0 Intake | `stations/a0-intake.prompt.md` | Prompt |
| A1 Policy Validation | `stations/a1-policy-validation.prompt.md` | Prompt |
| A2 Security Static | `stations/a2-security-static.prompt.md` | Prompt |
| A3 Prompt Injection (deterministic) | `stations/a3-prompt-injection.prompt.md` | Prompt |
| A4 Red Team (AI) | `stations/a4-red-team.agent.md` | Agent |
| A5 Sandbox Simulation | `stations/a5-sandbox-simulation.prompt.md` | Prompt |
| A6 Policy Gate | `stations/a6-policy-gate.agent.md` | Agent |
| A7 GitLab Update | `stations/a7-gitlab-update.prompt.md` | Prompt |

## Schemas

- `schemas/agent-manifest.schema.json` — required fields and constraints for `*.agent.md` frontmatter
- `schemas/skill-manifest.schema.json` — required fields and constraints for `SKILL.md` frontmatter

## Fixtures

- `fixtures/malicious-inputs.json` — structured malicious user inputs for sandbox simulation
- `fixtures/prompt-injection-payloads.json` — known injection payload patterns for A3/A4

## GitLab CI Pipeline

The CI orchestrator lives in `.gitlab-ci.yml` at the repository root.
It triggers on merge requests and runs in two phases:

1. **`validate` stage** — three deterministic Python validators run in parallel.
2. **`stations` stage** — `stations:run-all` invokes `station-workflows/scripts/run_stations.sh`,
   which discovers all station files dynamically and runs them in sequence.

The `stations:run-all` job uses `needs:` to depend only on the two blocking
Python validators (`validate:pr-auto` and `validate:yaml-workflows`).
The advisory `validate:test-gaps` job does not gate the station phase.

## Severity Levels

| Level | Meaning | Gate outcome |
|-------|---------|-------------|
| `critical` | Immediate security risk; must be fixed before merge | ❌ BLOCK |
| `high` | Significant risk; requires explicit human approval | ⚠️ REVIEW |
| `medium` | Non-blocking; recommended fix | 🟡 WARN |
| `low` | Informational | ℹ️ INFO |
