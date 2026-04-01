# /sdlc-tech-agent

Execute a **single Tech agent** identified by its number.

$ARGUMENTS = agent number (e.g., "t1.1", "t2.3", "t3.1")

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find agent `tech-$ARGUMENTS`.
2. Assemble the agent's full prompt:
   a. Load hooks from `.apm/instructions/sdlc-hooks.md`.
   b. Load conventions from `.apm/contexts/sdlc-conventions/`.
   c. Load skill from `.apm/skills/sdlc-tech-*/docs/`.
   d. Resolve upstream file paths from agent registry.
3. Launch the assembled prompt.
4. Display the result and output file path.
