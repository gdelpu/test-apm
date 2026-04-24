---
id: STA-NNN
title: "Sprint N Report — [Project Name]"
system: p2-monitoring
type: sprint-report
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
sprint: N
date_debut_sprint: YYYY-MM-DD
date_fin_sprint: YYYY-MM-DD
author: agent-p2.1-sprint-progress
reviewers: []
dependencies: ["PIL-001", "KPI-001", "RDP-001"]
upstream_dependencies:
  ba: []
  tech: []
confidence: high
---

# [STA-NNN] Sprint N Report — [Project Name]

---

## SPONSOR VERSION

> This section is written in business language, without technical terms. It is intended for the sponsor and the steering committee.

### Overall progress

**Project status:** <!-- 🟢 On track / 🟡 Attention required / 🔴 Intervention needed -->

<!-- Summary in 3-5 sentences: what was accomplished this sprint, what fell behind, what is expected from the sponsor. -->

### Functional progress

| Feature / Epic | Status | Planned delivery |
|---------------|--------|----------------|
| <!-- [EP-NNN] Epic name --> | <!-- Specified / In development / Complete / In UAT --> | <!-- --> |

### Budget and consumption

| Axis | Total budget | Consumed | Remaining work | End projection | Status |
|------|-------------|----------|----------------|----------------|--------|
| Human effort (d) | <!-- --> | <!-- (source Jira) --> | <!-- (Jira remaining) --> | <!-- --> | 🟢/🟡/🔴 |
| LLM – tokens (M) | <!-- --> | <!-- (source JSONL) --> | — | <!-- --> | 🟢/🟡/🔴 |
| LLM – estimated cost (€) | <!-- --> | <!-- (source JSONL) --> | — | <!-- --> | 🟢/🟡/🔴 |

### Attention points for the sponsor

<!-- The 1-3 points requiring sponsor attention or decision. -->

| Point | Nature | Action requested | Deadline |
|-------|--------|----------------|---------|
| <!-- --> | <!-- Information / Decision required --> | <!-- --> | YYYY-MM-DD |

---

## TECHNICAL VERSION

> This section is intended for the project team (PM, architect, lead dev, QA).

### 1. Sprint gates and milestones

| Gate / Milestone | Planned date | Actual date | Status | Comment |
|-----------------|-------------|------------|--------|---------|
| <!-- Gate BA S1 — Vision validated --> | <!-- --> | <!-- --> | ✅/🔄/🚫/⏩ | <!-- --> |
| <!-- --> | <!-- --> | <!-- --> | | <!-- --> |

**Gate velocity this sprint:** <!-- Average days late on sprint gates (0 = on track) -->

### 2. Agentic progress metrics

| Metric | Sprint value | Target ([KPI-001]) | Trend |
|--------|-------------|-------------------|-------|
| Deliverables produced | <!-- N --> | — | — |
| Deliverables validated | <!-- N --> | — | — |
| Validated/produced ratio | <!-- N% --> | ≥ 85% | 📈/📉/➡️ |
| Average replay rate | <!-- N iterations/agent --> | ≤ 1.5 | — |
| Agents in error | <!-- N --> | 0 | — |

### 3. Agentic system health

<!-- Provided by agent-p2.2-system-health -->

| Indicator | Status | Detail |
|----------|--------|--------|
| Cross-deliverable consistency | ✅/🟡/🔴 | <!-- agent-coherence-check result --> |
| Critical MCPs available | ✅/🟡/🔴 | <!-- Jira, Xray, etc. --> |
| Blocked agents | ✅/🟡/🔴 | <!-- N agents in blocked status --> |
| Orchestration log up to date | ✅/🟡/🔴 | <!-- Last entry: YYYY-MM-DD --> |

**Top 3 token-consuming agents this sprint:**

| Agent | Tokens (in+out) | Estimated cost | Iterations | Observation |
|-------|----------------|---------------|-----------|-------------|
| <!-- agent-id --> | <!-- --> | <!-- --> | <!-- --> | <!-- Normal / To optimise --> |

### 4. Human effort consumption (Jira)

| Profile | Total budget (d) | Consumed (d) | Jira RtC (d) | Projection | Status |
|---------|-----------------|-------------|-------------|-----------|--------|
| BA / PO | <!-- --> | <!-- --> | <!-- --> | <!-- --> | 🟢/🟡/🔴 |
| Architect | <!-- --> | <!-- --> | <!-- --> | <!-- --> | 🟢/🟡/🔴 |
| Dev | <!-- --> | <!-- --> | <!-- --> | <!-- --> | 🟢/🟡/🔴 |
| QA | <!-- --> | <!-- --> | <!-- --> | <!-- --> | 🟢/🟡/🔴 |
| PM | <!-- --> | <!-- --> | <!-- --> | <!-- --> | 🟢/🟡/🔴 |

> Source: Jira MCP — `timespent` / `timeestimate` on project issues `<!-- PROJ_KEY -->`

### 5. Active risks

| ID | Title | Score | Status | Current action | Deadline |
|----|-------|-------|--------|---------------|---------|
| [RSK-NNN] | <!-- --> | 🟡/🟠/🔴 | <!-- assessed / mitigated --> | <!-- --> | YYYY-MM-DD |

**Risks materialised this sprint:** <!-- None / [RSK-NNN] materialised on YYYY-MM-DD -->

### 6. Open decisions

| ID | Subject | Owner | Deadline | Status |
|----|---------|-------|---------|--------|
| [DEC-NNN] | <!-- --> | <!-- --> | YYYY-MM-DD | `open` |

### 7. Upcoming milestones (sprint N+1)

| Milestone | Date | Prerequisites |
|----------|------|--------------|
| <!-- Gate xxx --> | YYYY-MM-DD | <!-- --> |
| <!-- Deliverable yyy --> | YYYY-MM-DD | <!-- --> |
