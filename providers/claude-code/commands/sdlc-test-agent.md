# /sdlc-test-agent

Execute a **single Test agent** identified by its ID.

$ARGUMENTS = agent ID (e.g., "camp.1", "camp.2", "perf.1", "perf.2")

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find agent `test-$ARGUMENTS`.
2. Assemble the agent's full prompt:
   a. Load hooks from `.apm/instructions/sdlc-hooks.md`.
   b. Load conventions from `.apm/contexts/sdlc-conventions/`.
   c. Load skill from `.apm/skills/sdlc-test-*/docs/`.
   d. Resolve upstream file paths from agent registry.
3. Launch the assembled prompt.
4. Display the result and output file path.
