---
id: COP-NNN
title: "STEERING COMMITTEE N — [Project Name] — [Date]"
system: p3-committee
type: copil
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
sprint: N
date_copil: YYYY-MM-DD
author: agent-p3.1-steering-committee-prep
reviewers: []
dependencies: ["STA-NNN", "RSK-NNN", "KPI-001", "RDP-001"]
upstream_dependencies:
  ba: ["VIS-001", "EXF-001"]
  tech: []
---

# [COP-NNN] STEERING COMMITTEE N — [Project Name]

**Date:** YYYY-MM-DD | **Sprint:** N | **Planned duration:** 45 min

**Participants:** <!-- Sponsor, PM, Architect, Lead Dev, QA --> | **Facilitator:** <!-- PM -->

---

## 0. Agenda (5 min)

1. Overall progress — project status (10 min)
2. Budget and consumption (5 min)
3. Active risks (10 min)
4. Decisions requested (15 min)
5. Upcoming milestones (5 min)

---

## 1. Overall progress

**Project status:** <!-- 🟢 On track / 🟡 Attention required / 🔴 Intervention needed -->

### Executive summary

<!-- Maximum 5 lines. Business language only. What the sponsor needs to take away. -->

### Phase progress

| Phase | Progress | Milestones passed | Next milestone | Date |
|-------|---------|-----------------|----------------|------|
| Functional scoping | <!-- X% --> | <!-- M1 ✅ --> | <!-- M2 --> | <!-- --> |
| Technical design | <!-- X% --> | <!-- --> | <!-- --> | <!-- --> |
| Implementation | <!-- X% / Wave N in progress --> | <!-- --> | <!-- --> | <!-- --> |
| UAT | <!-- Pending / In progress / Complete --> | <!-- --> | <!-- --> | <!-- --> |

### Visual roadmap (current state)

```
PAST                             TODAY                          FUTURE
─────────────────────────────────────┼────────────────────────────────────
  ✅ Scoping  ✅ Arch    🔄 Dev.Wave1  ⬜ Dev.Wave2   ⬜ UAT   ⬜ Go-live
                                     ↑
                              Sprint N — [Date]
```

---

## 2. Budget and consumption

| Axis | Total budget | Consumed | End projection | Status |
|------|-------------|----------|----------------|--------|
| Human effort (d) | <!-- --> | <!-- --> | <!-- --> | 🟢/🟡/🔴 |
| LLM – tokens (M) | <!-- --> | <!-- --> | <!-- --> | 🟢/🟡/🔴 |
| LLM – estimated cost (€) | <!-- --> | <!-- --> | <!-- --> | 🟢/🟡/🔴 |

<!-- If indicator is 🟡 or 🔴: one line of plain-language explanation. -->

---

## 3. Active risks

<!-- Present only risks with score 🟠 High or 🔴 Critical -->

| ID | Risk | Score | Mitigation in place | Decision required? |
|----|------|-------|--------------------|--------------------|
| [RSK-NNN] | <!-- Risk title --> | 🟠/🔴 | <!-- Action in progress --> | Yes / No |

**Risks materialised since last STEERING COMMITTEE:** <!-- None / [RSK-NNN] → see decisions -->

---

## 4. Decisions requested

<!-- Each decision must be clearly formulated with options and their impacts. -->

### Decision 4.1 — [Subject]

| | |
|---|---|
| **Context** | <!-- Why this decision is needed now --> |
| **Option A** | <!-- Description + impact on planning/budget --> |
| **Option B** | <!-- Description + impact on planning/budget --> |
| **Team recommendation** | <!-- Option X — justification in 1 line --> |
| **Deadline** | YYYY-MM-DD |
| **Associated deliverable** | [DEC-NNN] |

---

### Decision 4.2 — [Subject] *(if applicable)*

<!-- Same structure -->

---

## 5. Upcoming milestones

| Event | Date | Prerequisites | Owner |
|-------|------|--------------|-------|
| Sprint N+1 review | YYYY-MM-DD | — | PM |
| Gate xxx | YYYY-MM-DD | <!-- Deliverables to validate --> | <!-- --> |
| Next STEERING COMMITTEE | YYYY-MM-DD | `[STA-NNN+1]` | PM |
| <!-- --> | <!-- --> | <!-- --> | <!-- --> |

---

## 6. Decision log (to fill during the STEERING COMMITTEE)

| # | Subject | Decision taken | By whom | Effective date |
|---|---------|---------------|---------|---------------|
| 1 | <!-- --> | <!-- --> | <!-- --> | <!-- --> |

---

## Traceability

| Deliverable | Contribution to this STEERING COMMITTEE |
|------------|----------------------------------------|
| [STA-NNN] | Progress and budget data |
| [RSK-NNN] | Active risks presented |
| [KPI-001] | Budget reference targets |
| [RDP-001] | Roadmap and milestones |
