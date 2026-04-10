---
name: hub-orchestrator
mode: agent
description: 'Discover available workflows and agents, classify your intent, and start execution. Start here if unsure which workflow to use.'
---

# /hub-orchestrator

Central triage and routing — discover the right workflow or agent for your task.

1. Read `.apm/contexts/hub-catalog.yaml` for the full catalog of workflows and agents.
2. Read `.apm/skills/hub-classification/SKILL.md` for the classification protocol.
3. Read `.apm/agents/hub-orchestrator.md` for the dispatch protocol.
4. Check `outputs/specs/features/*/workflow-state.md` for in-progress workflows — offer to resume if found.
5. Classify the user's intent using fast-path matching or structured interview.
6. Present the recommendation (name, type, stations, purpose, matching "when to use").
7. On user confirmation, dispatch:
   - **Workflows**: read the `.apm/workflows/<name>.yml` and execute the station sequence.
     Write artifacts to `outputs/specs/features/<feature>/`. Track state in `workflow-state.md`.
   - **SDLC harness** (`sdlc-ba`, `sdlc-tech`, `sdlc-steer`, `sdlc-full`): read the
     workflow YAML and execute with DAG resolution and wave scheduling.
   - **Standalone agents**: invoke the agent directly.
8. Pass through any flags: `--resume`, `--station <id>`, `--skip-gate <id>`, `--dry-run`.
