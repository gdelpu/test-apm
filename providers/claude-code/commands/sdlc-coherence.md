# /sdlc-coherence

Run the **cross-deliverable coherence check** on BA and/or Tech deliverables.

$ARGUMENTS = optional domain scope:
- `ba` — check BA deliverables only (default)
- `tech` — check Tech deliverables only
- `all` — run both BA and Tech checks

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml`.
2. **Route by scope:**
   - `ba` (default): load `.apm/skills/sdlc-deliverable-validation/docs/sk-coherence-check.md`. Scan `docs/1-prd/`.
   - `tech`: load `.apm/skills/sdlc-deliverable-validation/docs/sk-coherence-check-tech.md`. Scan `docs/2-tech/` + key BA files for traceability.
   - `all`: run both sequentially — BA first, then Tech.
3. Load conventions from `.apm/contexts/sdlc-conventions/`.
4. Execute: build identifier registry, check referential integrity, orphans, coverage, terminology, status consistency, diagram consistency.
5. Display the consistency score and anomaly summary.

Best run before each human gate or after significant changes.
