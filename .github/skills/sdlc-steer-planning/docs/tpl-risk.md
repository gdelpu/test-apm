---
id: RSK-NNN
title: "Risk — [Short factual title]"
system: p1-planning
type: risk
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
sprint: N
author: agent-p1.2-risk-register
reviewers: []
dependencies: ["PIL-001", "RDP-001"]
upstream_dependencies:
  ba: []
  tech: []
risk_level: medium
decision_owner: ""
confidence: medium
---

# [RSK-NNN] [Short factual risk title]

## 1. Identification

| Field | Value |
|-------|-------|
| ID | RSK-NNN |
| Category | <!-- functional \| technical \| agentic \| budget \| planning \| human --> |
| Agentic sub-category | <!-- R-AGT-01 Context drift \| R-AGT-02 Blocked gate \| R-AGT-03 LLM budget \| R-AGT-04 MCP unavailable \| R-AGT-05 Propagated ambiguity \| R-AGT-06 Prompt quality \| N/A --> |
| Identification date | YYYY-MM-DD |
| Detection sprint | N |
| Identified by | <!-- agent-p1.2 \| agent-p2.3 \| agent-coherence-check \| human --> |

---

## 2. Description

<!-- Factual description of the risk. Formulate as: "There is a risk that [undesirable event] if [condition], which would result in [consequence]." -->

---

## 3. Assessment

### Probability

| Level | Criteria |
|-------|---------|
| **Low** | < 20% chance of occurring — favourable context, no prior signals |
| **Medium** | 20-60% — moderate uncertainty, some signals |
| **High** | > 60% — unfavourable context, clear signals or already observed |

**Retained probability:** <!-- Low / Medium / High -->

**Justification:** <!-- -->

### Impact

| Level | Criteria |
|-------|---------|
| **Low** | Workable without significant calendar or budget impact (< 1 sprint) |
| **Medium** | Impact on 1-2 milestones, estimated additional effort < 10% of budget |
| **High** | Impact on critical path or budget > 10% |
| **Blocking** | Total project stop or impossibility of reaching go-live |

**Retained impact:** <!-- Low / Medium / High / Blocking -->

**Justification:** <!-- -->

**Deliverables impacted if materialised:**
- <!-- [PREFIX-NNN]: description of the impact -->

### Risk score

| Probability \ Impact | Low | Medium | High | Blocking |
|---------------------|-----|--------|------|---------|
| **Low** | 🟢 Minor | 🟢 Low | 🟡 Moderate | 🟡 Moderate |
| **Medium** | 🟢 Low | 🟡 Moderate | 🟠 High | 🔴 Critical |
| **High** | 🟡 Moderate | 🟠 High | 🔴 Critical | 🔴 Critical |

**Retained score:** <!-- 🟢 Minor / 🟢 Low / 🟡 Moderate / 🟠 High / 🔴 Critical -->

---

## 4. Mitigation plan

| Action | Owner | Deadline | Status |
|--------|-------|---------|--------|
| <!-- Concrete action 1 --> | <!-- Name/role --> | YYYY-MM-DD | ⬜ To do |
| <!-- Concrete action 2 --> | <!-- --> | YYYY-MM-DD | ⬜ To do |

**Residual risk after mitigation:** <!-- Expected residual score -->

---

## 5. Contingency plan (if the risk materialises)

<!-- What do we do if mitigation actions fail? -->

1. <!-- Contingency action 1 -->
2. <!-- Contingency action 2 -->

**Estimated contingency cost:** <!-- N days / X tokens / Calendar impact -->

---

## 6. Tracking

| Date | Sprint | Status | Update |
|------|--------|--------|--------|
| YYYY-MM-DD | N | `identified` | Risk created |
| <!-- --> | <!-- --> | <!-- assessed --> | <!-- --> |

**Statuses:** `identified` → `assessed` → `mitigated` → `closed` | `risk-materialized` → `escalated`

---

## Traceability

| Source deliverable | Link to this risk |
|-------------------|------------------|
| <!-- [PREFIX-NNN] --> | <!-- How this deliverable surfaced this risk --> |
