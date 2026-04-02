---
id: GNG-001
title: "Go/No-Go Release — [Project Name] v[X.Y]"
system: p3-committee
type: go-nogo
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-p3.2-go-nogo
reviewers: []
dependencies: ["PIL-001", "KPI-001", "RDP-001"]
upstream_dependencies:
  ba: ["EXF-001", "UAT-001", "BRL-001"]
  tech: ["DEBT-001", "TST-001", "IMP-001", "OBS-001"]
confidence: high
---

# [GNG-001] Go/No-Go Release — [Project Name] v[X.Y]

**Evaluation date:** YYYY-MM-DD | **Target version:** vX.Y | **Decision-makers:** Sponsor + Architect + Lead QA

---

## FINAL RECOMMENDATION

> **[  ] GO** — The release can be deployed to production.
>
> **[  ] CONDITIONAL GO** — The release can be deployed after resolving the conditions listed in §6.
>
> **[  ] NO-GO** — The release cannot be deployed. Blockers listed in §7.

**Justification:** <!-- 2-3 sentences summarising the basis for the recommendation -->

---

## 1. UAT results (from [UAT-001])

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Scenarios executed | N/Total | 100% | ✅/🔴 |
| Scenarios passed | N/Total | <!-- target [KPI-001] --> | ✅/🟡/🔴 |
| P1 requirements covered | N/N | 100% | ✅/🔴 |
| P2 requirements covered | N/N | ≥ 90% | ✅/🟡/🔴 |
| Open blocking defects | N | 0 | ✅/🔴 |
| Open major defects | N | ≤ 2 | ✅/🟡/🔴 |

**UAT summary:** <!-- 1-2 sentences -->

**Weighting by criticality [EXF-001]:**

| Criticality | Requirements covered | Not covered | Weight |
|-------------|--------------------|-----------|----|
| P1 — Critical | N/N | N | 50% |
| P2 — High | N/N | N | 30% |
| P3 — Standard | N/N | N | 20% |

**Weighted UAT score:** <!-- X% -->

---

## 2. Technical debt (from [DEBT-001])

| Debt cluster | Criticality | Release status | Comment |
|-------------|------------|---------------|---------|
| <!-- Cluster 1 --> | 🔴 Blocking | <!-- Resolved / Not resolved --> | <!-- --> |
| <!-- Cluster 2 --> | 🟠 Major | <!-- Resolved / Not resolved / Accepted --> | <!-- --> |
| <!-- Cluster 3 --> | 🟡 Minor | <!-- Accepted for v+1 --> | <!-- --> |

**Unresolved blocking debt:** <!-- None / [DEBT-NNN] clusters X, Y -->

---

## 3. Tests and NFR (from [TST-001])

| Dimension | Coverage | Result | Required threshold | Status |
|-----------|---------|--------|--------------------|--------|
| Unit tests | <!-- X% --> | <!-- PASS/FAIL --> | <!-- ≥ 80% --> | ✅/🔴 |
| Integration tests | <!-- X% --> | <!-- PASS/FAIL --> | <!-- ≥ 90% --> | ✅/🔴 |
| Performance tests (k6) | <!-- X percentile --> | <!-- PASS/FAIL --> | <!-- p95 < 200ms --> | ✅/🔴 |
| Security tests (ZAP) | <!-- N vulnerabilities --> | <!-- PASS/FAIL --> | <!-- 0 critical --> | ✅/🔴 |
| Accessibility tests (axe) | <!-- Score --> | <!-- PASS/FAIL --> | <!-- ≥ AA --> | ✅/🔴 |
| Fitness functions | <!-- X/N passed --> | <!-- PASS/WARN/BLOCK --> | <!-- 100% PASS --> | ✅/🔴 |

---

## 4. Observability and monitoring (from [OBS-001])

| Prerequisite | Status | Comment |
|-------------|--------|---------|
| SLOs defined and configured | ✅/🔴 | <!-- --> |
| Critical alerts active | ✅/🔴 | <!-- --> |
| Monitoring dashboard accessible | ✅/🔴 | <!-- --> |
| Rollback plan documented | ✅/🔴 | <!-- See [REL-001] --> |
| Smoke tests defined (< 10 min) | ✅/🔴 | <!-- --> |

---

## 5. Operational prerequisites

| Prerequisite | Status | Owner |
|-------------|--------|-------|
| SQL migrations verified and tested | ✅/🔴 | <!-- --> |
| Production environment variables configured | ✅/🔴 | <!-- --> |
| Secrets managed (no plaintext credentials) | ✅/🔴 | <!-- --> |
| User documentation up to date | ✅/🔴 | <!-- --> |
| Go-live communication prepared | ✅/🔴 | <!-- --> |
| Level-1 support briefed | ✅/🔴 | <!-- --> |
| Maintenance window defined | ✅/🔴 | <!-- --> |

---

## 6. Conditions (if CONDITIONAL GO)

<!-- Fill only if the recommendation is CONDITIONAL GO -->

| # | Condition | Owner | Deadline | Verification |
|---|-----------|-------|---------|--------------|
| 1 | <!-- --> | <!-- --> | YYYY-MM-DD | <!-- By whom / how --> |

---

## 7. Blockers (if NO-GO)

<!-- Fill only if the recommendation is NO-GO -->

| # | Blocker | Criticality | Estimated resolution effort | Owner |
|---|---------|------------|----------------------------|-------|
| 1 | <!-- --> | 🔴 Blocking | <!-- N days --> | <!-- --> |

**New estimated Go/No-Go date:** YYYY-MM-DD

---

## 8. Decision history

| Date | Recommendation | Decision taken | By whom |
|------|---------------|---------------|---------|
| YYYY-MM-DD | <!-- --> | <!-- GO / NO-GO / Defer --> | <!-- --> |

---

## Traceability

| Deliverable | Contribution to this decision |
|------------|------------------------------|
| [UAT-001] | Functional acceptance results |
| [DEBT-001] | Technical debt status |
| [TST-001] | Test coverage and results |
| [EXF-001] | Weighting by requirement criticality |
| [OBS-001] | Observability prerequisites |
| [IMP-001] | Complete waves and release gate prerequisites |
