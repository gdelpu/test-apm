# /hub-orchestrator

Central triage and routing — discover the right workflow or agent for your task.

## When to use

- You don't know which workflow or agent to use
- You want to see what's available
- You want to compare workflows
- You want to resume in-progress work
- First-time users starting with the SDLC Foundation

## Steps

1. **Load catalog**: Read `.apm/contexts/hub-catalog.yaml` for all available workflows
   (name, description, type, stations, when_to_use) and agents (name, description, tools).
   If the file is missing, fall back to reading `.apm/workflows/*.yml` and
   `.apm/agents/*.md` directly.

2. **Load classification protocol**: Read `.apm/skills/hub-classification/SKILL.md`
   for the full intent classification logic.

3. **Load dispatch protocol**: Read `.apm/agents/hub-orchestrator.md` for dispatch rules.

4. **Check for in-progress work**: Scan `outputs/runs/*/latest/workflow-state.md`.
   If any exist, offer to resume before starting a new workflow.

5. **Classify intent**: Use the fast-path keyword matching table from the
   classification skill. If ambiguous, ask structured interview questions
   (max 4) to narrow down.

6. **Recommend**: Present the best match with:
   - Name, type, station count
   - One-line description
   - Matching "when to use" reason
   - Ask for confirmation

7. **Dispatch** (on confirmation):
   - **Workflows**: Execute `/workflow-feature`, `/workflow-bug-fixing`,
     `/workflow-modernization`, `/workflow-quality`, `/workflow-spec-kit`,
     `/workflow-maturity-assessment`, `/workflow-bmad`, or the matching
     workflow command.
   - **SDLC harness**: Execute `/sdlc-full`, `/sdlc-ba`, `/sdlc-tech`,
     `/sdlc-steer`, or `/sdlc-test`.
   - **Standalone agents**: Invoke the agent directly.
   - **Pass-through flags**: Forward `--resume`, `--station`, `--scope`,
     `--skip-gate`, `--dry-run` to the dispatched command.

## Informational queries

- **"List all workflows"** → Show full catalog grouped by type.
- **"Compare X vs Y"** → Side-by-side comparison.
- **"What workflows for quality?"** → Filter by type.

## Inputs

- User's request or question (natural language)
- `.apm/contexts/hub-catalog.yaml` (auto-generated catalog)
- `.apm/skills/hub-classification/SKILL.md` (classification protocol)
- `.apm/agents/hub-orchestrator.md` (dispatch rules)
- `outputs/runs/*/latest/workflow-state.md` (optional, for resume detection)

## Outputs

- Workflow or agent recommendation with justification
- Dispatched execution of the selected workflow or agent
- Catalog listing (if informational query)
