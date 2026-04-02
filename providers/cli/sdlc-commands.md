# CLI — SDLC Workflow Commands

The generic `run-workflow.sh` runner supports all SDLC workflows directly.
No additional scripts are needed — the runner discovers `.apm/workflows/*.yml` dynamically.

## Composite workflows

```bash
# Full SDLC pipeline (all domains)
./providers/cli/run-workflow.sh sdlc-full my-project

# BA pipeline (S0-S3)
./providers/cli/run-workflow.sh sdlc-ba my-project

# Tech pipeline (T0-T3)
./providers/cli/run-workflow.sh sdlc-tech my-project

# Steer pipeline (P0-P3)
./providers/cli/run-workflow.sh sdlc-steer my-project
```

## Sub-pipeline execution (single station)

Use `--station <id>` to execute a single station from any workflow:

```bash
# BA: only the brownfield audit
./providers/cli/run-workflow.sh sdlc-ba my-project --station ba-audit-existing

# BA: only the scoping stations
./providers/cli/run-workflow.sh sdlc-ba my-project --station ba-vision
./providers/cli/run-workflow.sh sdlc-ba my-project --station ba-glossary
./providers/cli/run-workflow.sh sdlc-ba my-project --station ba-actors
./providers/cli/run-workflow.sh sdlc-ba my-project --station ba-requirements

# Tech: only the system context
./providers/cli/run-workflow.sh sdlc-tech my-project --station tech-system-context

# Tech: only the ADRs
./providers/cli/run-workflow.sh sdlc-tech my-project --station tech-adrs

# Steer: only the project sheet
./providers/cli/run-workflow.sh sdlc-steer my-project --station steer-project-sheet

# Steer: only sprint tracking
./providers/cli/run-workflow.sh sdlc-steer my-project --station steer-sprint-progress
```

## Resume and gate control

```bash
# Resume from last successful station
./providers/cli/run-workflow.sh sdlc-ba my-project --resume

# Skip a blocker gate (exceptional use)
./providers/cli/run-workflow.sh sdlc-tech my-project --skip-gate tech-adrs

# Dry run (list stations without executing)
./providers/cli/run-workflow.sh sdlc-full my-project --dry-run

# Verbose logging
./providers/cli/run-workflow.sh sdlc-ba my-project --verbose
```

## Station ID reference

### sdlc-ba.yml

| System | Station ID | Description |
|--------|-----------|-------------|
| S0 | `ba-audit-existing` | Existing system audit |
| S0 | `ba-audit-delta` | Delta analysis |
| S1 | `ba-vision` | Product vision & scope |
| S1 | `ba-glossary` | Business glossary |
| S1 | `ba-actors` | Actors & roles |
| S1 | `ba-requirements` | Functional requirements |
| S2 | `ba-domain-model` | Domain model |
| S2 | `ba-epics` | Epic decomposition |
| S2 | `ba-features` | Feature specification |
| S2 | `ba-business-rules` | Business rules |
| S3 | `ba-user-stories` | User stories |
| S3 | `ba-user-journeys` | User journeys |
| S3 | `ba-screen-specs` | Screen specifications |
| S3 | `ba-test-scenarios` | Test scenarios |
| S3 | `ba-e2e-plan` | E2E test plan |
| QG | `ba-validation` | BA deliverable validation |

### sdlc-tech.yml

| System | Station ID | Description |
|--------|-----------|-------------|
| T0 | `tech-audit` | Technical stack audit |
| T0 | `tech-gap` | Gap analysis |
| T1 | `tech-system-context` | System context (C4) |
| T1 | `tech-adrs` | Architecture decision records |
| T1 | `tech-stack` | Stack extraction |
| T1 | `tech-enablers` | Enabler index |
| T2 | `tech-data-model` | Data model |
| T2 | `tech-api-contracts` | API contracts |
| T2 | `tech-test-strategy` | Test strategy |
| T2 | `tech-impl-plan` | Implementation plan |
| T3 | `tech-drift` | Drift detection |
| T3 | `tech-e2e-gen` | E2E Playwright generation |

### sdlc-steer.yml

| System | Station ID | Description |
|--------|-----------|-------------|
| P0 | `steer-project-sheet` | Project sheet |
| P0 | `steer-kpi-baseline` | KPI baseline |
| P1 | `steer-sprint-plan` | Sprint planning |
| P1 | `steer-roadmap` | Roadmap |
| P1 | `steer-risk-register` | Risk register |
| P2 | `steer-sprint-progress` | Sprint progress |
| P2 | `steer-system-health` | System health |
| P2 | `steer-sprint-risks` | Sprint risks |
| P3 | `steer-copil` | COPIL preparation |
| P3 | `steer-go-nogo` | Go/No-Go decision |

### sdlc-full.yml

| Phase | Station ID | Description |
|-------|-----------|-------------|
| Init | `scaffold` | Directory scaffold |
| Init | `project-init` | Project initialization |
| BA | `ba-pipeline` | Nested BA pipeline |
| Plan | `sprint-planning` | Sprint planning |
| Tech | `tech-pipeline` | Nested Tech pipeline |
| Impl | `implementation` | Code implementation |
| Test | `test-campaign` | E2E/UAT campaign |
| Test | `test-performance` | Performance campaign |
| Track | `sprint-tracking` | Sprint tracking |
| QV | `quality-validation` | Quality validation |
| Gov | `copil` | COPIL & Go/No-Go |
