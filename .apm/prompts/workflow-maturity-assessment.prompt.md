---
name: workflow-maturity-assessment
mode: agent
description: 'Run SDLC maturity assessment workflow (6 stations).'
---

# /workflow-maturity-assessment

Run the Maturity Assessment workflow.

1. Read `.apm/workflows/maturity-assessment.yml` for the station sequence.
2. Execute each station: scope definition → capability analysis → maturity scoring →
   gap analysis report → improvement roadmap → stakeholder review.
3. Write the final assessment to `maturity-report.md`.
4. Track state via the canonical state tracker (`python -m engine --state`) under `outputs/runs/`. If unavailable, write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-maturity-assessment-team-alpha.md`) directly following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. Always write the state file to the **root** of `outputs/` — never inside a workflow subfolder.
