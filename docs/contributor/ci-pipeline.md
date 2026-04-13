# CI Pipeline

> PR validation pipeline architecture — deterministic validators and AI-powered security stations.

For deep technical details on station implementations, scripts, schemas, and fixtures, see [`ci-gates/README.md`](../../ci-gates/README.md).

---

## Pipeline Architecture

Every merge request triggers a **two-phase validation pipeline** (`.gitlab-ci.yml`).

```text
merge_request_event
  │
  ├─ validate (parallel)                  ← Phase 1
  │   ├─ validate:pr-auto                  Python   ⛔ gates
  │   ├─ validate:yaml-workflows           Python   ⛔ gates
  │   └─ validate:test-gaps                Python   advisory
  │
  └─ stations (sequential)                ← Phase 2
      └─ stations:run-all
           A0 → A1 → A2 → … → A7
           Fails fast on any status: "fail"
```

## Stations (A0–A7)

| Station | Type | Purpose | Gate |
|---------|------|---------|------|
| A0 Intake | Prompt | PR metadata + work order | — |
| A1 Policy | Prompt | Frontmatter, tools, structure | Blocker |
| A2 Security | Prompt | Static security scanning | Blocker |
| A3 Prompt Injection | Prompt | Jailbreak + injection hardening | Blocker |
| A4 Red Team | Agent | Adversarial simulation | Advisory |
| A5 Sandbox | Prompt | Agent execution simulation | Blocker |
| A6 Policy Gate | Agent | Final decision across all reports | Blocker |
| A7 GitLab Update | Prompt | MR status update | Info |

Station implementations: `ci-gates/stations/`.
Schemas: `.apm/knowledge/governance/schemas/` (agent-manifest, skill-manifest).
Scripts: `ci-gates/scripts/` (orchestrator, extract, sanitize).

## Local Validation

```bash
# Deterministic validators
python .apm/skills/ai-backbone-pr-checks/tools/scripts/pr_auto_validator.py \
  --base-ref HEAD~1 --head-ref HEAD --out outputs/reports/pr-auto-validator.json
python .apm/skills/ai-backbone-pr-checks/tools/scripts/yaml_workflow_linter.py \
  --root . --out outputs/reports/yaml-workflow-linter.json
python .apm/skills/ai-backbone-pr-checks/tools/scripts/test_gap_detector.py \
  --base-ref HEAD~1 --head-ref HEAD --out outputs/reports/test-gap-detector.json

# Cross-layer validation
python scripts/validate_all.py

# Full pipeline via Podman — see local-testing.md for full details
podman-compose up --build
```

> **Full local testing guide**: [local-testing.md](local-testing.md) — Podman setup, environment variables, Phase 1/2 breakdown, troubleshooting.

## CI/CD Configuration (GitLab)

1. **Settings > CI/CD > Variables**: create masked `GITHUB_TOKEN` with Copilot CLI access
2. Set `ENABLE_COPILOT_CLI=true` to enable AI stations
3. The `stations:run-all` job authenticates via this token for A0–A7

## Cross-Layer Validation

Scripts in `scripts/` verify canonical ↔ projection consistency:

| Script | Purpose |
|--------|---------|
| `validate_core_assets.py` | Canonical `.apm/` layer completeness |
| `validate_copilot_assets.py` | Copilot projection sync with canonical |
| `validate_claude_assets.py` | Claude adapter sync with canonical |
| `validate_all.py` | Run all validators with summary |
