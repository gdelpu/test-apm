# /sdlc-steer-agent

Execute a **single Steer agent** identified by its number.

$ARGUMENTS = agent number (e.g., "p0.1", "p1.1", "p2.1", "p3.2")

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find agent `steer-$ARGUMENTS`.
2. Assemble the agent's full prompt:
   a. Load hooks from `.apm/instructions/sdlc-hooks.md`.
   b. Load conventions from `.apm/contexts/sdlc-conventions/`.
   c. Load skill from `.apm/skills/sdlc-steer-*/docs/`.
   d. Resolve upstream file paths from agent registry.
3. Launch the assembled prompt.
4. Display the result and output file path.
