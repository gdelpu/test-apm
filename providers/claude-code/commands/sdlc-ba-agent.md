# /sdlc-ba-agent

Execute a **single BA agent** identified by its number.

$ARGUMENTS = agent number (e.g., "1.2", "2.1", "3.5")

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find agent `ba-$ARGUMENTS`.
2. Assemble the agent's full prompt:
   a. Load pre-hooks from `.apm/instructions/sdlc-hooks.md`.
   b. Load conventions from `.apm/contexts/sdlc-conventions/`.
   c. Load template (if declared in agent registry).
   d. Load skill from `.apm/skills/sdlc-ba-*/docs/`.
   e. Load post-hooks from `.apm/instructions/sdlc-hooks.md`.
   f. Resolve upstream file paths from agent registry.
3. Launch the assembled prompt.
4. Display the result and output file path.

For per-feature agents (3.x), specify the feature path as a second argument:
  `/sdlc-ba-agent 3.1 outputs/docs/1-prd/3-epics/ep-001/ft-001`
