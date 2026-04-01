# Steer-Agents — Project Steering Domain

Automates project steering for agentic software development. Reads and aggregates deliverables from BA, Tech, and Test domains to produce progress reports, risk assessments, and Go/No-Go decisions. **Never modifies upstream deliverables.**

## Role in the harness

Steer-Agents is the **fourth domain**, positioned **above** the other three. It consumes their outputs to produce a consolidated steering view.

```
[BA-Agents] -----+
                  |
[Tech-Agents] ----+--> [Steer-Agents] --> Sponsor / Steering Committee
                  |
[Test-Agents] ----+
```

---

## Dynamic execution

### P0 + P1 — One-shot initialization

```
  /steer-0-init (once, at project start)
  +---------------------------+
  | p0.1 Project Sheet        |               team, capacity, LLM budget
  |         |                 |
  | p0.2 KPI Baseline         |               effort + token budgets per phase
  +---------------------------+
         |
         v
  /steer-1-planning (once, after BA S2 — needs validated Epics)
  +---------------------------+
  | p1.3 Sprint Planning      |               batch features into parallel design sprints
  |   (AI-native batching)    |               reads Epic Feature Index tables only
  |         |                 |
  | p1.1 Roadmap              |               phases, milestones, gates
  |         |                 |
  | p1.2 Risk Register        |               BA + Tech + agentic risks
  +---------------------------+
         | Human gate (validate sprint plan + roadmap)
         v
```

### P2 — Recurring sprint loop

System P2 is **not sequential** — it runs at **every sprint** with an incremented sprint number:

```
  /steer-2-sprint N (recurring — runs at each sprint)

  Sprint 1        Sprint 2        Sprint 3        ...     Sprint N
  +--------+      +--------+      +--------+              +--------+
  | p2.1   |      | p2.1   |      | p2.1   |              | p2.1   |
  | p2.2   |      | p2.2   |      | p2.2   |              | p2.2   |
  | p2.3   |      | p2.3   |      | p2.3   |              | p2.3   |
  +--------+      +--------+      +--------+              +--------+
  [STA-001]       [STA-002]       [STA-003]               [STA-00N]
       |               |               |                       |
       v               v               v                       v
    Human gate      Human gate      Human gate              Human gate
  (sprint review) (sprint review) (sprint review)         (sprint review)
```

Each sprint produces:
- `[STA-NNN]` — Sprint progress + system health
- `[RSK-NNN]` — Updated risk assessment
- `[DEC-NNN]` — Decisions if escalation needed

### P3 — Steering committee + Go/No-Go

```
  /steer-3-copil (after test campaigns)
  +-------------------------------------------+
  | p3.1 COPIL Preparation                    |
  |   - Technical section (velocity, debt,    |
  |     test coverage, token consumption)     |
  |   - Sponsor section (functional progress, |
  |     budget, business language)            |
  |         |                                 |
  | p3.2 Go/No-Go Release                    |
  |   - Aggregates: [QUAL-GNG-001]           |  <-- from Test-Agents
  |                  [PERF-RPT-NNN]          |  <-- from Test-Agents
  |                  [DEBT-001]              |  <-- from Tech-Agents
  |                  [STA-NNN] (all sprints) |  <-- from P2 loop
  |   - Verdict: GO / CONDITIONAL GO / NO-GO |
  +-------------------------------------------+
         | Human gate (sponsor + architect + QA)
         v
  Production deployment
```

---

## What changes in agentic steering

| Dimension | Classic steering | Agentic steering |
|-----------|-----------------|-----------------|
| **Bottleneck** | Human production time | Review and validation of agent outputs |
| **Cadence** | Dev sprints (2 weeks) | Dual: agentic phases (days) + human gates |
| **Risks** | Delays, bad estimates | Context drift, blocked gates, LLM costs |
| **Speed metrics** | Velocity (story points) | Validated/replayed deliverable ratio + gate speed |
| **Budget** | Person-days (Jira) | Person-days **+** LLM token consumption |
| **Quality** | Tests, bugs, coverage | Iterations per deliverable, cross-deliverable consistency |

---

## Agent inventory

### Pipeline agents (11 skills)

| System | Agent | Skill | Output | Input |
|--------|-------|-------|--------|-------|
| P0 | p0.1 Project Sheet | `sk-p0.1-project-sheet` | `[PIL-001]` + `[CAP-001]` | `docs/0-inputs/steer/` |
| P0 | p0.2 KPI Baseline | `sk-p0.2-kpi-baseline` | `[KPI-001]` | `[PIL-001]` |
| **P1** | **p1.3 Sprint Planning** | `sk-p1.3-sprint-planning-design` | **`[PLAN-001]`** — unified BA+Tech sprint plan | **Epic files only** (`ep-*/ep-*.md`) |
| P1 | p1.1 Roadmap | `sk-p1.1-roadmap` | `[RDP-001]` | `[PLAN-001]` |
| P1 | p1.2 Risk Register | `sk-p1.2-risk-register` | `[RSK-001]` | `[RDP-001]` |
| P2 | p2.1 Sprint Progress | `sk-p2.1-sprint-progress` | `[STA-NNN]` |
| P2 | p2.2 System Health | `sk-p2.2-system-health` | Updates `[STA-NNN]` |
| P2 | p2.3 Sprint Risks | `sk-p2.3-sprint-risks` | `[RSK-NNN]` + `[DEC-NNN]` |
| P3 | p3.1 COPIL Preparation | `sk-p3.1-copil` | `[COP-NNN]` |
| P3 | p3.2 Go/No-Go | `sk-p3.2-go-nogo` | `[GNG-001]` |

### Tool agents (7 skills)

| Tool | Skill | Description |
|------|-------|-------------|
| Scope arbitration | `sk-scope-arbitration` | A/B options on `[IMPACT-xxx]` for committee `[DEC-NNN]` |
| Budget tracking | `sk-budget-tracking` | Effort (Jira) + LLM (JSONL) dual-axis report |
| Risk escalation | `sk-risk-escalation` | Sponsor escalation dossier |
| Stakeholder report | `sk-stakeholder-report` | Non-technical version of `[STA-NNN]` |
| Sprint retrospective | `sk-sprint-retrospective` | Facilitation guide + minutes (4Ls + SMART actions) |
| Retrospective | `sk-retrospective` | Post-release: agent iterations + token cost analysis |
| Validate | `sk-validate` | Steering deliverable quality audit |

---

## Agentic risk taxonomy

| ID | Risk | Alert threshold |
|----|------|----------------|
| R-AGT-01 | Context drift | Agent output contradicts validated upstream |
| R-AGT-02 | Blocked gate | Human validation overdue > 2 days |
| R-AGT-03 | LLM budget overrun | Token consumption > 130% of phase budget |
| R-AGT-04 | Critical MCP unavailable | Jira, Xray down |
| R-AGT-05 | Unresolved business ambiguity | BA grey zones propagated to Tech |
| R-AGT-06 | Prompt quality drift | Agent requires > 3 iterations |

---

## Harness structure

```
Steer-Agents/
  skills/                  12 pipeline skills + 7 tool skills
    sk-p0.1-project-sheet.md
    sk-p2.1-sprint-progress.md
    ...
    tools/
      sk-scope-arbitration.md
      sk-budget-tracking.md
      ...
  refs/
    conventions/           cv-pilotage-conventions, cv-pilotage-agentique
    templates/             6 templates (tpl-*.md)
  hooks/                   pre-input-validation, post-quality-control, post-confluence-push
  README.md
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/steer-0-init` | Project initialization (P0, once) |
| `/steer-1-planning` | Sprint batching (design) + roadmap + risk register (P1, once after S2) |
| `/steer-2-sprint N` | Sprint tracking (P2, recurring) |
| `/steer-3-copil` | Steering committee + Go/No-Go (P3) |
| `/steer-agent <PN.N>` | Single agent (e.g., `/steer-agent p2.1`) |
