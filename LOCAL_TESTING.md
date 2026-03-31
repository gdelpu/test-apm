# Local Pipeline Testing

Run the full CI pipeline locally using `podman-compose` (or `docker-compose`).

## Prerequisites

- **Podman Desktop** installed with a running machine (`podman machine info` → `MachineState: Running`)
- **Python 3.10+** with a virtual environment (for `podman-compose`)
- **Git** installed and on PATH
- A **GitHub Personal Access Token** with Copilot scope (for AI stations)

## Setup

```powershell
# 1. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# 2. Install podman-compose
pip install podman-compose

# 3. Create .env from the example below
```

### `.env` file (required)

Create a `.env` file in the repository root:

```env
GH_TOKEN=github_pat_YOUR_TOKEN_HERE
GITHUB_TOKEN=github_pat_YOUR_TOKEN_HERE
CI_MERGE_REQUEST_TARGET_BRANCH_NAME=main
CI_COMMIT_SHA=HEAD
CI_MERGE_REQUEST_IID=1
ENABLE_COPILOT_CLI=true
```

Set `ENABLE_COPILOT_CLI=false` to skip Copilot CLI invocations (stations will be listed but not executed).

## Quick Start

> **Important:** Always activate the venv first — `podman-compose` is installed there.

```powershell
.\.venv\Scripts\activate
```

### Run everything (validators + stations)

Due to `--abort-on-container-exit` terminating all containers when the first one exits,
run validators and stations separately:

```powershell
# Step 1: Run the three Python validators
podman-compose up validate-pr-auto validate-yaml-workflows validate-test-gaps

# Step 2: Run the AI station orchestrator (A0–A7)
podman-compose up stations-run-all
```

### Run only the Python validators (no token needed)

```powershell
podman-compose up validate-pr-auto validate-yaml-workflows validate-test-gaps
```

### Run only the AI stations

```powershell
podman-compose up stations-run-all
```

### Clean up between runs

```powershell
podman-compose down
Remove-Item station_out\*_raw.json, station_out\*_result.json -ErrorAction SilentlyContinue
```

## Pipeline Phases

### Phase 1 — Python Validators (`validate` stage)

Three deterministic validators run in parallel inside `python:3.11` containers:

| Service | Script | Blocking? |
|---------|--------|-----------|
| `validate-pr-auto` | `pr_auto_validator.py` | Yes |
| `validate-yaml-workflows` | `yaml_workflow_linter.py` | Yes |
| `validate-test-gaps` | `test_gap_detector.py` | Advisory |

### Phase 2 — AI Station Orchestrator (`stations` stage)

The `stations-run-all` container (`node:20-bookworm-slim`) installs Copilot CLI
and invokes `ci-gates/scripts/run_stations.sh`, which:

1. Discovers all `*.prompt.md` and `*.agent.md` files in `ci-gates/stations/`
2. Sorts them by prefix (a0 → a7)
3. Runs each sequentially via Copilot CLI with per-station model selection
4. Sleeps 30s between stations (rate-limit throttle)
5. Aborts the pipeline if any station returns `status: fail`

| Station | Model | Purpose |
|---------|-------|---------|
| A0 — Intake | Haiku | Classify PR scope, extract changed files |
| A1 — Policy Validation | Sonnet | Validate agent/skill frontmatter against policy rules |
| A2 — Security Static | Haiku | Static security scan (secrets, dependencies) |
| A3 — Prompt Injection | Sonnet | Deterministic jailbreak/exfil pattern scan |
| A4 — Red Team | Sonnet | Adversarial red team assessment (advisory, non-blocking) |
| A5 — Sandbox Simulation | Sonnet | Simulated attack scenarios |
| A6 — Policy Gate | Sonnet | Aggregate all reports → APPROVE / REVIEW / BLOCK |
| A7 — GitLab Update | Haiku | Post labels/notes to GitLab MR (skipped locally without `GITLAB_TOKEN`) |

## Station Outputs

All outputs are written to `station_out/`:

| File | Station | Content |
|------|---------|---------|
| `a0_result.json` | A0 | Work order: PR metadata, changed files, scope classification |
| `a1_result.json` | A1 | Policy findings (P-01 through P-06) |
| `a2_result.json` | A2 | Security scan findings |
| `a3_result.json` | A3 | Prompt injection findings (PI-01 through PI-06) |
| `a4_result.json` | A4 | Red team findings (advisory) |
| `a5_result.json` | A5 | Sandbox simulation results |
| `a6_result.json` | A6 | Gate decision (APPROVE/REVIEW/BLOCK) |
| `a7_result.json` | A7 | GitLab update status (or skipped) |
| `changed_files.txt` | Shared | Git diff name-status |
| `diff.patch` | Shared | Full diff fed to stations |

Validator reports are written to `reports/`:

| File | Validator |
|------|-----------|
| `pr-auto-validator.json` | PR structural checks |
| `yaml-workflow-linter.json` | Workflow YAML lint |
| `test-gap-detector.json` | Test coverage gaps |

## Troubleshooting

### `podman-compose` not recognized

Always activate the venv first:
```powershell
.\.venv\Scripts\activate
```

### Podman machine not running

```powershell
podman machine start
```

### Stations skip with "ENABLE_COPILOT_CLI != true"

Ensure `.env` has `ENABLE_COPILOT_CLI=true` and a valid `GITHUB_TOKEN`.

### Rate limit hit

The orchestrator retries up to 3 times with 70s waits. If it persists, increase `COPILOT_INTER_STATION_SLEEP` in `.env` (default: 30s).

### Stale containers block re-runs

```powershell
podman-compose down
```

### Container can't find git

The `stations-run-all` container installs git automatically. If validators fail with git errors, ensure the repo is a valid git working tree.

## Environment Variables

Override these in `.env` as needed:

| Variable | Default | Purpose |
|----------|---------|---------|
| `ENABLE_COPILOT_CLI` | `false` | Set `true` to run AI stations |
| `GITHUB_TOKEN` | — | GitHub PAT with Copilot scope |
| `CI_MERGE_REQUEST_TARGET_BRANCH_NAME` | `main` | Base branch for diff |
| `CI_COMMIT_SHA` | `HEAD` | Head commit for diff |
| `CI_MERGE_REQUEST_IID` | `0` | MR identifier |
| `STATION_TIMEOUT` | `900` | Per-station timeout (seconds) |
| `COPILOT_MAX_DIFF_LINES` | `2000` | Max diff lines fed to stations |
| `COPILOT_INTER_STATION_SLEEP` | `30` | Seconds between stations |
| `COPILOT_RATE_LIMIT_WAIT` | `70` | Seconds to wait on rate limit |
| `COPILOT_RATE_LIMIT_RETRIES` | `3` | Max retries per station |
| `COPILOT_MODEL_DEFAULT` | `claude-haiku-4.5` | Default model |
| `GITLAB_TOKEN` | — | GitLab API token (A7 only) |

## CI/CD Integration Checklist

Before pushing, verify locally:

- [ ] `validate-pr-auto` passes (0 blocking issues)
- [ ] `validate-yaml-workflows` passes
- [ ] A0 generates valid work order classifying your changes
- [ ] A1 passes all policy rules (0 critical/high)
- [ ] A2 security scan has no blocking findings
- [ ] A3 prompt injection checks pass
- [ ] A4 red team findings reviewed (advisory)
- [ ] A5 sandbox scenarios pass
- [ ] A6 decision is APPROVE (or REVIEW with justification)
- [ ] All station JSON outputs are valid and complete
- **Station orchestrator:** `ci-gates/scripts/run_stations.sh`
