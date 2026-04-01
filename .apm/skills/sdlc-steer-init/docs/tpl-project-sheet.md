---
id: PIL-001
title: "Project Sheet — [Project Name]"
system: p0-initialization
type: project-sheet
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-p0.1-project-sheet
reviewers: []
dependencies: []
upstream_dependencies:
  ba: []
  tech: []
---

# [PIL-001] Project Sheet — [Project Name]

## 1. Project context

| Field | Value |
|-------|-------|
| Project name | <!-- Official name --> |
| Sponsor | <!-- Name + role --> |
| Project manager | <!-- Name --> |
| Start date | YYYY-MM-DD |
| Target go-live date | YYYY-MM-DD |
| Project type | <!-- Greenfield / Brownfield / Migration --> |
| Priority | <!-- P1 – Critical / P2 – High / P3 – Standard --> |
| Jira link | <!-- Jira project URL --> |
| Jira key | <!-- e.g.: PROJ --> |
| Git repositories | <!-- URLs of BA Agent, Tech Agent, Code repos --> |

---

## 2. Project team

| Profile | Name | Project role | Jira assignee | Availability (%) |
|---------|------|-------------|--------------|-----------------|
| Product Owner / Sponsor | <!-- --> | Gate validation, scope arbitration | <!-- username --> | <!-- --> |
| Business Analyst | <!-- --> | BA Agent deliverable reviewer | <!-- username --> | <!-- --> |
| Architect | <!-- --> | Tech gate validation, ADRs | <!-- username --> | <!-- --> |
| Lead developer | <!-- --> | Claude Code implementation supervision | <!-- username --> | <!-- --> |
| Developer(s) | <!-- --> | Claude Code wave execution | <!-- username --> | <!-- --> |
| QA / Tester | <!-- --> | UAT testing, scenario validation | <!-- username --> | <!-- --> |
| Project manager / PM | <!-- --> | Steering, STEERING COMMITTEE | <!-- username --> | <!-- --> |

### Jira assignee groups (for MCP reading)

```yaml
jira_groups:
  business: ["username1", "username2"]   # BA, PO, Sponsor
  tech: ["username3", "username4"]       # Architect, Lead dev, Dev
  qa: ["username5"]                       # QA
  pm: ["username6"]                       # PM
```

---

## 3. Available MCP tools

| MCP tool | Criticality | URL / Config | Status |
|----------|------------|-------------|--------|
| Jira MCP | Critical | <!-- --> | 🟢 Available |
| Xray MCP | Important | <!-- --> | 🟢 Available |
| GitHub/GitLab MCP | Important | <!-- --> | 🟢 Available |
| Confluence MCP | Optional | <!-- --> | <!-- --> |
| Figma MCP | Optional | <!-- --> | <!-- --> |
| Playwright MCP | Important | <!-- --> | <!-- --> |

---

## 4. Calendar constraints

| Constraint type | Description | Impact |
|----------------|-------------|--------|
| Imposed date | <!-- E.g.: Go-live before January 1st (regulation) --> | Blocking |
| Code freeze | <!-- E.g.: Code freeze Dec 20 – Jan 03 --> | Planning |
| Team unavailability | <!-- E.g.: PO absent week 32 --> | Gate P1 to shift |
| External dependency | <!-- E.g.: Client UAT testing from J+90 --> | External milestone |

---

## 5. Scope of agentic systems used

| System | Activated | Skipped agents (if partial) |
|--------|----------|-----------------------------|
| BA Agent — System 0 (Brownfield audit) | ☐ Yes / ☐ No | <!-- --> |
| BA Agent — System 1 (Scoping) | ☑ Yes | — |
| BA Agent — System 2 (Specification) | ☑ Yes | — |
| BA Agent — System 3 (Functional design) | ☑ Yes | <!-- --> |
| Tech Agent — System T0 (Technical audit) | ☐ Yes / ☐ No | <!-- --> |
| Tech Agent — System T1 (Architecture) | ☑ Yes | — |
| Tech Agent — System T2 (Technical design) | ☑ Yes | <!-- --> |
| Tech Agent — System T3 (Continuous quality) | ☑ Yes | — |

---

## 6. Initially identified risks

<!-- Risks known at project start, before formal analysis. Will be formalised in [RSK-001]. -->

| Suspected risk | Category | Uncertainty level |
|---------------|----------|------------------|
| <!-- --> | <!-- functional / technical / agentic / planning --> | <!-- Low / Medium / High --> |

---

## Traceability

| Jointly produced deliverable | Description |
|-----------------------------|-------------|
| [CAP-001] | Team capacity snapshot (produced simultaneously) |
| [KPI-001] | Baseline KPIs (produced by agent-p0.2 next) |

---

# [CAP-001] Team Capacity Snapshot

<!-- This document is produced jointly with [PIL-001] by the same agent. -->

---
id: CAP-001
title: "Team Capacity — [Project Name]"
system: p0-initialization
type: capacity
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-p0.1-project-sheet
dependencies: ["PIL-001"]
---

## Capacity by profile and phase

<!-- Formula: Capacity (days) = Σ(working_days × availability% × focus_factor) -->
<!-- Recommended focus factor: 0.7 (meetings, unforeseen, context switching) -->

| Profile | Scoping phase (d) | Design phase (d) | Implementation phase (d) | UAT phase (d) | Total (d) |
|---------|------------------|-----------------|------------------------|--------------|-----------|
| BA / PO | <!-- --> | <!-- --> | <!-- --> | <!-- --> | <!-- --> |
| Architect | <!-- --> | <!-- --> | <!-- --> | <!-- --> | <!-- --> |
| Lead Dev | <!-- --> | <!-- --> | <!-- --> | <!-- --> | <!-- --> |
| Dev | <!-- --> | <!-- --> | <!-- --> | <!-- --> | <!-- --> |
| QA | <!-- --> | <!-- --> | <!-- --> | <!-- --> | <!-- --> |
| PM | <!-- --> | <!-- --> | <!-- --> | <!-- --> | <!-- --> |
| **Total** | | | | | |

## Calculation assumptions

| Assumption | Value |
|------------|-------|
| Working days per sprint (2 weeks) | 10 |
| Applied focus factor | 0.70 |
| Mandatory reserve per sprint | 20% |
| Hours per working day | 7h |
