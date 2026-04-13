# Workflow: PR Validation

Multi-stage merge request/pull request validation pipeline with deterministic checks and AI-powered security stations acting as a CI/CD gate on code changes.

## When to use

- **Mandatory CI/CD gate** on merge requests/pull requests to any protected branch
- Validating changes to agents, skills, workflows, or instructions in this repository
- Security hardening before code integration into main branch
- Compliance checking for naming conventions and documentation standards
- Red-team and sandbox simulation of agent/skill behavioral safety

## Workflow phases

### Phase 1: Deterministic Validators (parallel)

Runs in parallel, must both pass to proceed to Phase 2:

| Station | Purpose | Blocker | Details |
|---------|---------|---------|---------|
| PR Auto Validator | Frontmatter + naming + links | ✓ blocker | Validates YAML frontmatter, kebab-case naming, no broken links |
| YAML Workflow Linter | YAML syntax + schema validation | ✓ blocker | Validates `.yml` structure, required fields, unsafe patterns |
| Test Gap Detector | Documentation gaps | ⚠ advisory | Identifies if tests exist for behavior changes (non-blocking) |

### Phase 2: AI Stations (sequential)

Runs only after deterministic validators pass. Stages A0–A7 execute in sequence:

| # | Station | Purpose | Blocker | Details |
|---|---------|---------|---------|---------|
| A0 | Intake | PR context extraction | ⚠ warning | Generates work order with changed files, diffs, risk hints |
| A1 | Policy Validation | Agent/skill manifests | ✓ blocker | Enforces tool allowlists, safety field requirements, structures (P-01–P-06) |
| A2 | Security Static | Secrets + dangerous patterns | ✓ blocker | Detects hardcoded credentials, shell injection, eval usage |
| A3 | Prompt Injection | Jailbreak resistance | ✓ blocker | Detects jailbreak phrases, validates refusal anchors, checks sanitization |
| A4 | Red Team | Adversarial simulation | ⚠ optional | Generates exploit prompts against agent definitions (non-blocking) |
| A5 | Sandbox Simulation | Tool scoping + execution | ✓ blocker | Runs agent against malicious inputs, validates tool confinement |
| A6 | Policy Gate | Final decision | ✓ blocker | Aggregates A0–A5, decides PASS/CONDITIONAL_PASS/BLOCK |
| A7 | Platform Update | Apply labels + comments | ⚠ optional | Updates GitLab/GitHub with results and recommendation labels |

## Execution

**When triggered**: On push to merge request or pull request (any branch).

**Outputs**: All reports written to `outputs/station_out/`:
- `work_order.json` — PR metadata, changed files, diff summary, risk hints
- `policy_report.json` — manifest validation results
- `security_report.json` — secrets + pattern scans
- `promptsec_report.json` — jailbreak/injection findings
- `a4_result.json` — red team simulation output
- `sim_report.json` — sandbox execution results
- `gate_decision.json` — final gate decision with justification

**Exit codes**:
- **0** (PASS): PR is approved for merge
- **1** (BLOCK): PR is rejected; critical findings must be fixed
- **2** (CONDITIONAL_PASS): PR may merge with manual review approval

## Why this workflow

This repository (`ai-sdlc-foundation`) contains executable agents, skills, and CI/CD configurations that directly influence behavior across projects. The multi-station pipeline ensures:

1. **Safety**: Agents cannot have unrestricted tool access or unsafe patterns
2. **Compliance**: Naming, structure, documentation follow foundation standards  
3. **Security**: Secrets, shell injection, eval usage are detected pre-merge
4. **Resilience**: Sandbox simulation verifies agents behave safely under adversarial conditions
5. **Traceability**: Every PR has a detailed audit trail (work order → decision record)

## Adding or removing stations

To add/remove a station: add/delete the corresponding file in `ci-gates/stations/` (e.g., `a0-intake.prompt.md`). The orchestrator automatically discovers and sorts by prefix (A0 → A7). No `.gitlab-ci.yml` edits needed.

## Local testing

See [`docs/contributor/local-testing.md`](../../docs/contributor/local-testing.md) for instructions to run the pipeline locally using Podman/Docker or gitlab-ci-local.
