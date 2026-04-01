---
id: RDP-001
title: "Roadmap — [Project Name]"
system: p1-planning
type: roadmap
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-p1.1-roadmap
reviewers: []
dependencies: ["PIL-001", "KPI-001"]
upstream_dependencies:
  ba: ["VIS-001", "EXF-001", "EP-001"]
  tech: ["IMP-001", "PLAN-001"]
confidence: high
---

# [RDP-001] Roadmap — [Project Name]

## 1. Calendar summary

| Phase | Start date | End date | Duration | Exit gate | Status |
|-------|-----------|---------|---------|----------|--------|
| P0 — Steering Initialization | <!-- --> | <!-- --> | <!-- --> | Project sheet validated | ⬜ To do |
| BA S0 — Brownfield audit | <!-- --> | <!-- --> | <!-- --> | Delta validated by sponsor | ⬜ To do |
| BA S1 — Scoping | <!-- --> | <!-- --> | <!-- --> | Vision validated by sponsor | ⬜ To do |
| BA S2 — Specification | <!-- --> | <!-- --> | <!-- --> | Specs validated by sponsor + BA | ⬜ To do |
| BA S3 — Functional design | <!-- --> | <!-- --> | <!-- --> | Design validated + Xray sync | ⬜ To do |
| Tech T0 — Technical audit | <!-- --> | <!-- --> | <!-- --> | Gap analysed by architect | ⬜ To do |
| Tech T1 — Architecture | <!-- --> | <!-- --> | <!-- --> | ADRs validated by architect | ⬜ To do |
| Tech T2 — Technical design | <!-- --> | <!-- --> | <!-- --> | Implementation plan validated | ⬜ To do |
| Implementation — Wave 1 | <!-- --> | <!-- --> | <!-- --> | Wave 1 tested | ⬜ To do |
| Implementation — Wave 2 | <!-- --> | <!-- --> | <!-- --> | Wave 2 tested | ⬜ To do |
| Implementation — Wave N | <!-- --> | <!-- --> | <!-- --> | All waves tested | ⬜ To do |
| UAT | <!-- --> | <!-- --> | <!-- --> | Go/No-Go validated | ⬜ To do |
| Release | <!-- --> | <!-- --> | <!-- --> | Go-live | ⬜ To do |

**Statuses:** ✅ Complete | 🔄 In progress | ⬜ To do | 🚫 Blocked | ⏩ Deferred

---

## 2. Key milestones

| # | Milestone | Planned date | Actual date | Impact if delayed |
|---|-----------|-------------|------------|------------------|
| M1 | Gate BA S1 — Vision validated | <!-- --> | <!-- --> | <!-- E.g.: Shifts T1 by N weeks, budget impact +X days --> |
| M2 | Gate Tech T1 — Architecture validated | <!-- --> | <!-- --> | <!-- --> |
| M3 | Gate T2 — Implementation plan validated | <!-- --> | <!-- --> | <!-- --> |
| M4 | End of Claude Code wave 1 | <!-- --> | <!-- --> | <!-- --> |
| M5 | End of all waves + tests | <!-- --> | <!-- --> | <!-- --> |
| M6 | Go/No-Go release | <!-- --> | <!-- --> | <!-- --> |
| M7 | Go-live | <!-- --> | <!-- --> | <!-- Imposed / contractual date --> |

---

## 3. Critical path

<!-- Identify the sequence of tasks whose delay would directly impact the go-live date -->

```
[Critical milestone 1] → [Critical milestone 2] → [Critical milestone 3] → Go-live
```

**Total available margin:** <!-- N days between planned end date and imposed date -->

---

## 4. Implementation waves (from [IMP-001])

<!-- To be populated after [IMP-001] is validated by Tech Agent -->

| Wave | Content (Epics/Features) | Stories `[US-xxx]` | Estimated duration | Prerequisites |
|------|--------------------------|---------------------|-------------------|--------------|
| Wave 1 — Foundation | <!-- --> | <!-- --> | <!-- --> | Architecture validated |
| Wave 2 — Core features | <!-- --> | <!-- --> | <!-- --> | Wave 1 complete |
| Wave 3 — Secondary features | <!-- --> | <!-- --> | <!-- --> | Wave 2 complete |
| Wave N — Polish & NFR | <!-- --> | <!-- --> | <!-- --> | Waves N-1 complete |

---

## 5. External dependencies

| Dependency | Type | Impact | Owner | Deadline |
|-----------|------|--------|-------|---------|
| <!-- E.g.: Third-party API available --> | <!-- Technical / Organisational --> | <!-- --> | <!-- --> | <!-- --> |

---

## 6. Version history

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | agent-p1.1-roadmap | Initial version |

<!-- Every roadmap update must increment the version number and document the changes here -->

---

## Traceability

| Deliverable | Role in the roadmap |
|------------|-------------------|
| [PIL-001] | Calendar constraints and team |
| [KPI-001] | Target budgets per phase |
| [IMP-001] | Implementation waves and dependencies |
| [PLAN-001] | Initial sprint schedule (BA tools) |
| [EXF-001] | Requirement criticality (milestone priority) |
