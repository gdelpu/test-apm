# Local GitLab CI Pipeline Testing

This guide explains how to run the Agent Factory pipeline locally using `gitlab-ci-local`.

## Prerequisites

### For Windows (Native Podman Runner)
- **Podman Desktop** installed and running
- **Git** installed (for repository operations)

### For Linux/WSL/Mac (gitlab-ci-local)
- **Node.js** (v16+) and **npm** installed
- **Git** installed
- **Podman Desktop** or **Docker Desktop** running

## Quick Start

### Windows Users (Recommended)

**Use the native Podman runner** (no npm/Node.js required):

```powershell
# Full pipeline (deterministic validators + all stations)
.\run-pipeline-podman.ps1

# Run only the station orchestrator (skips deterministic validators)
bash ci-gates/scripts/run_stations.sh

# Show help
.\run-pipeline-podman.ps1 -Help
```

### Linux/WSL/Mac Users

Use gitlab-ci-local for full CI simulation:

```bash
# Install
npm install -g gitlab-ci-local

# Configure test scenario
# Edit .gitlab-ci-local-variables.yml

# Run full pipeline (both phases)
gitlab-ci-local

# Run only deterministic validators
gitlab-ci-local validate:pr-auto
gitlab-ci-local validate:yaml-workflows

# Run station orchestrator (discovers all stations dynamically)
gitlab-ci-local stations:run-all
```

## Pipeline Phases

The pipeline runs in two phases:

1. **Phase 1 — `validate` stage**: Three deterministic Python validators run in parallel.
   `validate:pr-auto` and `validate:yaml-workflows` are blocking; `validate:test-gaps` is advisory.
2. **Phase 2 — `stations` stage**: The `stations:run-all` job invokes
   `ci-gates/scripts/run_stations.sh`, which dynamically discovers all
   `*.prompt.md` and `*.agent.md` files in `ci-gates/stations/`, sorts
   them by prefix (a0 → a6), and runs each sequentially via Copilot CLI.
   It starts only after the two blocking validators pass.

## Station Outputs

All stations write their results to the `station_out/` directory:

- `station_out/work_order.json` — A0 diff analysis
- `station_out/policy_report.json` — A1 validation results
- `station_out/security_report.json` — A2 security scan
- `station_out/promptsec_report.json` — A3 prompt injection checks
- `station_out/sim_report.json` — A5 sandbox test results
- `station_out/gate_decision.json` — A6 final decision

## Testing Specific Scenarios

### Test BLOCK Decision (Critical Findings)

1. Add a malicious pattern to an agent file (e.g., hardcoded token)
2. Run: `.\run-pipeline-local.ps1 A2-security-static`
3. Verify: `station_out/security_report.json` shows critical finding
4. Run: `.\run-pipeline-local.ps1 A6-policy-gate`
5. Verify: A6 exits with code 1 (BLOCK decision)

### Test REVIEW Decision (High Risk)

1. Add `allowRunCommands: true` to an agent
2. Run: `.\run-pipeline-local.ps1 A1-policy-validation`
3. Verify: `station_out/policy_report.json` flags high-risk pattern
4. Run: `.\run-pipeline-local.ps1 A6-policy-gate`
5. Verify: Decision is "REVIEW"

### Test A7 GitLab API Calls (Labels/Notes)

**Note:** A7 requires a real GitLab instance. For local testing, A7 will attempt API calls that will fail against `http://localhost` endpoints. To skip A7 during local testing, run only stations A0-A6.

If you want to test A6:
1. Set `GITLAB_TOKEN` in `.gitlab-ci-local-variables.yml`
2. Update `CI_API_V4_URL` to point to your GitLab instance
3. Set `CI_PROJECT_ID` to a real project ID
4. Run: `.\run-pipeline-local.ps1 A7-gitlab-update`

## Troubleshooting

### Windows: Git Command Not Found
```
Error: Command failed with exit code 127: git ls-files --deduplicate
```
**Root Cause:** gitlab-ci-local requires git during initialization on Windows.

**Solutions:**
1. **Install Git for Windows** and ensure it's in PATH:
   ```powershell
   git --version  # Should show version
   ```
   Download from: https://git-scm.com/download/win

2. **Use WSL2** (recommended for Windows):
   ```bash
   # From WSL2 terminal
   cd /mnt/c/Users/rasinha/source/repos/ai-sdlc-foundation
   npm install -g gitlab-ci-local
   gitlab-ci-local
   ```

3. **Manual station testing** (bypass gitlab-ci-local):
   ```powershell
   # Run stations directly with Podman
   podman run --rm -v "${PWD}:/workspace" -w /workspace python:3.12-slim bash -c "apt-get update && apt-get install -y git && cd /workspace && python ci-gates/stations/A0-intake.prompt.md"
   ```

### Container Runtime Not Running
```
Error: Cannot connect to the Docker daemon
```
**Solution:** Start Podman Desktop or Docker Desktop

The script automatically detects and uses Podman (preferred) or Docker.

### Station Artifacts Missing
If a downstream station can't find upstream artifacts (e.g., A1 can't find `work_order.json`):

```powershell
# Run stations in sequence
.\run-pipeline-local.ps1 A0-intake
.\run-pipeline-local.ps1 A1-policy-validation
# ... etc
```

### Python Dependencies Fail to Install
If you see pip errors during job execution:

```powershell
# Clear container cache (Podman)
podman system prune -a

# Or with Docker
docker system prune -a
```

### Workflow Rules Block Execution
If the pipeline doesn't start, ensure `.gitlab-ci-local-variables.yml` has:
```yaml
CI_PIPELINE_SOURCE: merge_request_event
```

## Differences from GitLab CI

| Feature | GitLab CI | gitlab-ci-local |
|---------|-----------|-----------------|
| Artifact persistence | Between jobs | ✓ Fully supported |
| `needs:` dependencies | ✓ Full DAG | ✓ Full DAG |
| `when: always` | ✓ Runs always | ✓ Runs always |
| GitLab API calls (A6) | Real API | Requires real GitLab instance |
| `interruptible: true` | ✓ Cancels on new MR push | ⚠️ Not applicable locally |
| Git context | Real MR diff | Uses local git state |

## Advanced Usage

### Run with Custom Variables

```powershell
# Override specific variables
gitlab-ci-local A0-intake --variable CI_MERGE_REQUEST_IID=42
```

### Debug Mode

```powershell
# Show verbose output
gitlab-ci-local --debug
```

### List All Jobs

```powershell
gitlab-ci-local --list
```

## CI/CD Integration Test Checklist

Before pushing to GitLab, verify locally:

- [ ] A0 generates valid `work_order.json` for your changes
- [ ] A1 passes all policy rules (or intentionally flags expected violations)
- [ ] A2 security scan runs without blocking findings (unless expected)
- [ ] A3 prompt injection checks pass
- [ ] A4 red team findings reviewed
- [ ] A5 sandbox scenarios complete without crashes
- [ ] A6 produces expected decision (APPROVE/REVIEW/BLOCK)
- [ ] All station JSON outputs are valid and complete

## Resources

- **gitlab-ci-local docs:** https://github.com/firecow/gitlab-ci-local
- **GitLab CI YAML reference:** https://docs.gitlab.com/ee/ci/yaml/
- **Pipeline file:** `.gitlab-ci.yml`
- **Station orchestrator:** `ci-gates/scripts/run_stations.sh`
