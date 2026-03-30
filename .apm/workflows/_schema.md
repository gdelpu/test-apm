# Workflow Schema

Defines the YAML structure for workflow definitions in `.apm/workflows/`.

## Structure

```yaml
name: <string>                    # Unique workflow identifier (kebab-case)
description: <string>             # One-line purpose statement
type: <string>                    # Category: delivery | validation | modernization | assessment

stations:
  - id: <string>                  # Unique station identifier (kebab-case)
    name: <string>                # Human-readable station name
    agent: <string>               # Agent to execute this station (from .apm/agents/)
    skills:                       # Skills the agent should invoke
      - <string>
    inputs:                       # Files or artifacts required before this station runs
      - <string>
    outputs:                      # Files or artifacts this station produces
      - <string>
    optional: <boolean>           # If true, station can be skipped (default: false)
    parallel: <boolean>           # If true, can run in parallel with adjacent parallel stations (default: false)
    gate:                         # Quality gate evaluated after station completes
      criteria:                   # List of pass/fail conditions
        - <string>
      severity: blocker | warning # blocker = halt workflow; warning = log and continue
      reviewer: <string>          # Optional: agent that reviews gate (e.g., security-reviewer)

config:
  output_dir: <string>            # Where artifacts are written (supports <feature> placeholder)
  state_file: workflow-state.md   # Tracks station completion
  allow_resume: true              # Whether --resume is supported
  allow_skip_gate: true           # Whether --skip-gate is supported
  nestable: <boolean>             # Whether this workflow can be invoked as a sub-workflow
```

## Conventions

- Each workflow has a `.yml` (machine-parseable) and optional `.md` (human-readable companion).
- Station `id` values are unique within a workflow.
- Station `agent` references must exist in `.apm/agents/`.
- Station `skills` references must exist in `.apm/skills/`.
- A station with `optional: true` and `gate.severity: warning` is fully skippable.
- Stations with `parallel: true` can run concurrently (used in validation phases).
- Nested workflows are referenced by a station that names another workflow.

## State File Format

The workflow state file tracks execution progress:

```markdown
# Workflow State: <workflow-name>

| Station | Status | Started | Completed | Gate |
|---------|--------|---------|-----------|------|
| <id>    | pending/running/passed/failed/skipped | <timestamp> | <timestamp> | pass/fail/skipped |
```

## Gate Evaluation

Gates are evaluated by reading station outputs and checking each criterion.
A **blocker** gate failure halts the workflow. A **warning** gate failure logs the issue and continues.
The `--skip-gate <station-id>` flag overrides a blocker gate (for exceptional cases).

## Station Implementation

Stations can be implemented as:
- **Prompt files** (`*.prompt.md`) — executed by an AI provider via the configured agent.
- **Agent files** (`*.agent.md`) — invoked as a sub-agent with its own tool scope.
- **Script files** (`*.sh`, `*.py`) — executed directly by the CLI runner.

For the PR validation workflow, station implementations live in `ci-gates/stations/`.
For SDLC workflows, stations are executed by the agent + skills defined in the YAML.

## Nesting

Workflows with `config.nestable: true` can be invoked from other workflows.
The parent workflow references the child by name; the runner handles dispatch.
Example: `quality-validation` is nested inside `feature-implementation` and `modernization`.
