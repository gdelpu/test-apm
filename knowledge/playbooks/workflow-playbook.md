# Workflow Playbook

How to use, extend, and compose the workflow orchestration system.

## Available workflows

### End-to-end (monolithic)

| Workflow | Purpose | Stations |
|----------|---------|----------|
| `feature-implementation` | Full feature delivery | 9: constitution → spec → clarify → review → plan → tasks → implement → quality → gate |
| `modernization` | Guided migration | 7: baseline → target → review → plan → risk → tasks → quality |
| `bug-fixing` | Bug resolution | 7: triage → reproduce → root-cause → fix-plan → implement → regression → quality |
| `bmad` | Build-Measure-Analyze-Decide loop | 4: build → measure → analyze → decide |

### Composable (chain as needed)

| Workflow | Purpose | Stations |
|----------|---------|----------|
| `spec-kit` | Specification package | 8: constitution → spec → clarify → review → plan → tasks → test-strategy → gate |
| `quality-validation` | Quality and security | 7: lint → static → SAST → deps → coverage → DAST → report |
| `maturity-assessment` | Codebase maturity | 6: discovery → architecture → quality → security → debt → report |

### Operational

| Workflow | Purpose | Stations |
|----------|---------|----------|
| `pr-validation` | PR/MR security gating | 8: intake → policy → security → prompt-injection → red-team → sandbox → gate → update |

## Running a workflow

### Via GitHub Copilot (VS Code)

Use the workflow prompts or invoke `@workflow-orchestrator`:
- `/workflow-feature` — Feature implementation
- `/workflow-modernization` — Modernization
- `/workflow-quality` — Quality validation

### Via Claude Code

Use Claude commands:
- `/workflow-feature`, `/workflow-modernization`, `/workflow-quality`, etc.

### Via CLI

```bash
# Run a full workflow
./providers/cli/run-workflow.sh feature-implementation my-feature

# Dry run — list stations
./providers/cli/run-workflow.sh quality-validation my-feature --dry-run

# Resume from last pass
./providers/cli/run-workflow.sh modernization spring-upgrade --resume

# Run a single station
./providers/cli/run-workflow.sh pr-validation my-branch --station a1-policy-validation

# Force past a blocker gate
./providers/cli/run-workflow.sh feature-implementation my-feature --skip-gate quality-validation
```

## Extending workflows

### Add a new workflow

1. Create `.apm/workflows/<name>.yml` following the schema in `_schema.md`.
2. Add a corresponding `.apm/workflows/<name>.md` companion doc.
3. Create provider projections:
   - `providers/github-copilot/prompts/workflow-<name>.prompt.md`
   - `providers/claude-code/commands/workflow-<name>.md`
4. Update this playbook and the README.

### Add a station to an existing workflow

1. Add the station entry in the workflow YAML.
2. Create or reference the agent/skill for the station.
3. Define gate criteria and severity.
4. Test with `--dry-run` and then `--station <id>`.

## Quality gates

- **Blocker** gates halt the workflow — the issue must be resolved before continuing.
- **Warning** gates log findings and continue — review at your discretion.
- Use `--skip-gate <station-id>` to force past a blocker (emergency only, audit trail logged).

## Nesting

Quality validation can be nested inside feature-implementation, modernization,
bug-fixing, and other end-to-end workflows. The workflow engine delegates to
the quality-validation sub-workflow at the appropriate station.

## PR validation pipeline

The `pr-validation` workflow (A0–A7 stations) runs in CI/CD:
- **Phase 1** (parallel): Deterministic Python validators (frontmatter, YAML, test gaps)
- **Phase 2** (sequential): AI-powered validation stations (policy, security, prompt injection, red team, sandbox, gate)

Station implementations live in `ci-gates/stations/`.
See `ci-gates/README.md` for details.
