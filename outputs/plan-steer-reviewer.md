# Plan: Independent Steer Reviewer (P1 — Go/No-Go Gate)

**Date:** 2026-04-20
**Branch:** `feat/sdlc-gate-verify`
**Problem:** The Go/No-Go release decision is the highest-stakes deliverable in the SDLC pipeline, yet `sdlc-steer-manager` produces AND self-validates it with no independent review.

## Phases

### Phase 1 — Steer Coherence Check Skill
- [x] Create `.apm/skills/sdlc-deliverable-validation/docs/sk-coherence-check-Steer-Agents.md`
- Cross-domain accuracy checks unique to steer deliverables
- Go/No-Go vs quality-report: coverage, SAST, dependency findings accurately reflected
- Go/No-Go vs campaign-report: pass rates, critical anomalies faithfully represented
- Go/No-Go vs performance-report: threshold compliance accurately stated
- COPIL budget vs KPI baseline actuals
- Sprint risks faithfully carried into COPIL risk section
- Risk register alignment with sprint-risks evolution

### Phase 2 — Steer Reviewer Canonical Agent
- [x] Create `.apm/agents/sdlc-steer-reviewer.md`
- Read-only access to steer outputs (`outputs/docs/3-steer/**`)
- Read-only access to upstream domain reports (quality, campaign, performance, BA review, tech review)
- Write access to `outputs/docs/3-steer/reviews/**`
- Skills: `sdlc-deliverable-validation`, `sdlc-review-arbitration`
- Reference: `sk-validate-Steer-Agents.md`, `sk-coherence-check-Steer-Agents.md`
- CONFLICT detection: Go/No-Go claims don't match source data

### Phase 3 — Copilot Provider Adapter
- [x] Create `providers/github-copilot/agents/sdlc-steer-reviewer.agent.md`
- Mirror canonical agent with resource limits for A5 sandbox checks

### Phase 4 — Workflow: sdlc-steer.yml
- [x] Add `steer-review` station between `steer-copil` and `steer-go-nogo`
- Independent review of COPIL pack before the Go/No-Go decision
- `on_conflict: pause` for human arbitration
- Add `required_outputs` to existing steer stations

### Phase 5 — Workflow: sdlc-full.yml
- [x] Split the merged `copil` station into `steer-copil` + `steer-review` + `steer-go-nogo`
- Steer review sits between COPIL preparation and Go/No-Go decision
- Update inputs/outputs chain

### Phase 6 — Update review-arbitration skill scope
- [x] Add `sdlc-steer-reviewer` to the "When to use" section of `sdlc-review-arbitration/SKILL.md`

### Phase 7 — CI Validation
- [x] Run `simulate_ci.py` and verify no new blocking findings
- [ ] Commit and push

## Design Decisions

- The steer reviewer reviews the **COPIL pack** (aggregation accuracy) before the Go/No-Go decision is made, not after. This means the Go/No-Go decision benefits from a verified COPIL pack.
- In `sdlc-full.yml`, the single `copil` station must be split into three: COPIL prep → steer review → Go/No-Go. This preserves the separation of concerns.
- The coherence check is the critical new capability — it cross-references steer claims against actual upstream reports.
