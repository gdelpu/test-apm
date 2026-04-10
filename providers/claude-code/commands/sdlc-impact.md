# /sdlc-impact

Run the **change impact analysis** tool.

$ARGUMENTS = description of the change (free text, meeting transcript, or path to a diff file)

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find agent `ba-impact`.
2. Load `.apm/skills/sdlc-change-impact/SKILL.md`.
3. Load `.apm/contexts/sdlc-impact-graph.yaml` — the declarative cascade graph.
4. Load conventions from `.apm/contexts/sdlc-conventions/`.
5. Execute: identify changes (confirm with user if identifiers are inferred), traverse impact graph, classify impacts, produce re-execution sequence.
6. Display the impact summary with severity counts.
7. **Ask the user**: "Proceed with amendment? (yes / no)"
   - **yes**: trigger the re-execution sequence, then run `/sdlc-coherence` automatically.
   - **no**: save the report to `outputs/docs/1-prd/5-tools/impact-{NNN}-{slug}.md` for later use.
