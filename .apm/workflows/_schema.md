# Workflow Schema

Defines the YAML structure for workflow definitions in `.apm/workflows/`.

## Structure

```yaml
name: <string>                    # Unique workflow identifier (kebab-case)
description: <string>             # One-line purpose statement
type: <string>                    # Category: delivery | validation | modernization | assessment

default_hooks:                    # Optional: hooks applied to all stations unless overridden
  pre:                            #   Pre-hooks inherited by every station
    - <path>
  post:                           #   Post-hooks inherited by every station
    - <path>

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
    pre_hooks:                    # Optional: hooks that fire BEFORE station execution
      - hook: <string>            #   Path relative to .apm/hooks/ (e.g., pre/input-validation/ba)
        severity: blocker | warning
    post_hooks:                   # Optional: hooks that fire AFTER station, BEFORE gate evaluation
      - hook: <string>            #   Path relative to .apm/hooks/ (e.g., post/quality-control)
        severity: blocker | warning
    gate:                         # Quality gate evaluated after station completes
      criteria:                   # List of pass/fail conditions
        - <string>
      severity: blocker | warning # blocker = halt workflow; warning = log and continue
      reviewer: <string>          # Optional: agent that reviews gate (e.g., security-reviewer)
    allowed_tools:                # Explicit tool scope for this station (validated against policy allowlist)
      - <string>                  # Each entry must be in the station_tools_allowlist (see below)

config:
  output_dir: <string>            # Where artifacts are written (supports <feature> placeholder)
  state_file: workflow-state.md   # Tracks station completion (fallback: outputs/workflow-state-<workflow>-<feature>.md; engine: outputs/runs/<workflow>/<run>/workflow-state.md)
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

## Station Hooks

Stations can declare `pre_hooks` and `post_hooks` arrays. Hooks fire as lightweight sub-stations around the main station execution. Each hook references a file under `.apm/hooks/` and declares a severity level.

### Execution order

```
pre_hooks → station execution → post_hooks → gate evaluation
```

### Hook results

Each hook returns `GO`, `WARN`, or `STOP`:

| Hook type | Result | Effect |
|-----------|--------|--------|
| Pre-hook | `GO` | Station executes normally |
| Pre-hook | `WARN` | Station executes; warning logged in state file |
| Pre-hook | `STOP` (blocker) | Station skipped; workflow halted |
| Pre-hook | `STOP` (warning) | Station skipped; workflow continues |
| Post-hook | `GO` | Gate evaluation proceeds |
| Post-hook | `WARN` | Gate evaluation proceeds; warning logged |
| Post-hook | `STOP` (blocker) | Gate marked as failed; workflow halted |
| Post-hook | `STOP` (warning) | Warning logged; gate evaluation proceeds |

Hooks with `never_block: true` (defined in the hook file) always downgrade `STOP` to `WARN`.

### Hook file references

Hook paths are relative to `.apm/hooks/`. Example: `pre/input-validation/ba` resolves to `.apm/hooks/pre/input-validation/ba.md`.

See `.apm/hooks/_schema.md` for the full hook contract definition.

## Resource Limits

The following limits are enforced by the workflow orchestrator during YAML validation, before any station agent is invoked. Workflows exceeding any limit are rejected with a blocker-severity error.

| Limit | Value | Scope |
|-------|-------|-------|
| Max stations per workflow | 50 | Per workflow YAML file |
| Max `context` field length | 2 000 characters | Per station |
| Max `description` field length | 500 characters | Per station |
| Max nesting depth | 5 levels | Across nested workflows |
| Max `allowed_tools` per station | 10 entries | Per station |

### High-privilege tool policy

The following tools are classified as **high-privilege**: `runCommands`, `editFiles`, `fetch`.

Any station declaring a high-privilege tool in its `allowed_tools` list MUST be immediately preceded by a station with `gate.severity: blocker` and `gate.reviewer: human`. Workflow YAML that places a high-privilege station without such a preceding human-approval gate is rejected during structure validation.

### Station `allowed_tools` allowlist

Every entry in a station's `allowed_tools` array MUST be one of the following policy-controlled values:

```yaml
station_tools_allowlist:
  - codebase       # Read-only workspace search
  - search         # Text/semantic search
  - problems       # Diagnostics / lint errors
  - view           # Read files (Copilot CLI)
  - create         # Write files (Copilot CLI)
  - edit/editFiles # Modify existing files
  - runCommands    # Execute shell commands (requires preceding human-approval gate)
  - fetch          # Network requests (requires preceding human-approval gate)
  - github         # GitHub API access
  - terminal       # Terminal interaction
```

Any value not in this allowlist is rejected during YAML structure validation with a `critical` severity finding. This prevents attacker-contributed workflow YAML from introducing unknown or custom tool scopes.

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
