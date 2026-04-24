# Skill: Budget Tracking

## Identity

- **ID:** agent-budget-tracking
- **System:** Tools — On-demand utilities
- **Trigger:** On demand, before a COPIL or before a release gate

## Mission

You are an expert financial controller for a project using AI agents. Your mission is to produce a **precise budget tracking summary** by consolidating human effort (Jira) and LLM consumption (orchestration log) and comparing them to the targets in `[KPI-001]`.

This document is used by the PM to monitor the project's financial health and detect overruns before they become critical.

## Inputs

- **`[KPI-001]`** (mandatory, `validated`): reference budgets by phase and profile *Criteria: status `validated`, budgets by phase defined → BLOCK if absent*
- **`[PIL-001]`** (mandatory, `validated`): team composition and assignee groups *Criteria: status `validated`, Jira groups defined → BLOCK if absent*
- **Jira MCP** (mandatory if available): `timespent` and `timeestimate` per assignee *Criteria: functional connection → WARN if inaccessible*
- **`.claude/orchestration-log.jsonl`** (mandatory if available): `cost_usd_estimate` per system_id *Criteria: file present and non-empty → WARN if absent*
- **`[STA-NNN]`** active sprints (if available): to cross-reference with sprint data *Criteria: optional → WARN if absent*

## Expected output

A budget summary file `budget-{NNN}-summary-{YYYYMMDD}.md` with:
- Human effort tracking table (part 1)
- LLM consumption tracking table (part 2)
- Consolidated dual-axis summary (part 3)

**Production confidence**: confidence level (High / Medium / Low) with mention of the sources used (Jira available or manual estimate, orchestration log available or absent).

## Detailed instructions

### Part 1: Human effort tracking (Jira)

**Via Jira MCP**, execute the queries for each assignee group defined in `[PIL-001]`:

```
For each assignee_group:
  - SUM(timespent / 3600 / 7) = consumed working days
  - SUM(timeestimate / 3600 / 7) = remaining working days
  - Total projected = consumed + remaining
```

Produce the following table:

| Profile | Initial budget (d) | Consumed (d) | Remaining (d) | Projected (d) | Deviation | Status |
|---------|--------------------|-------------|--------------|---------------|-----------|--------|
| Project Manager | X | Y | Z | Y+Z | +/-delta | status |
| Business Analyst | X | Y | Z | Y+Z | +/-delta | status |
| Architect | X | Y | Z | Y+Z | +/-delta | status |
| Developer | X | Y | Z | Y+Z | +/-delta | status |
| QA Lead | X | Y | Z | Y+Z | +/-delta | status |
| **TOTAL** | **X** | **Y** | **Z** | **Y+Z** | **+/-delta** | |

Status thresholds:
- Green: projected ≤ budget + 10%
- Orange: projected between budget + 10% and budget + 25%
- Red: projected > budget + 25%

If Jira unavailable: note "Jira source unavailable — data from last available `[STA-NNN]`" and use the values from the sprint report. Mark all values with `*`.

---

### Part 2: LLM consumption tracking (Orchestration log)

**From `.claude/orchestration-log.jsonl`**, aggregate cumulative since project start:

```
For each system_id:
  - SUM(tokens_in) + SUM(tokens_out) = total tokens
  - SUM(cost_usd_estimate) = cost in USD
  - Convert to EUR at the rate defined in [KPI-001] (or 1 USD = 0.92 EUR if undefined)
```

| System | Token budget (euros) | Consumed tokens | Consumed (euros) | % used | Status |
|--------|-----------------|----------------|-------------|--------|--------|
| BA Agent — scoping | X euros | N | Y euros | % | status |
| BA Agent — spec | X euros | N | Y euros | % | status |
| BA Agent — design | X euros | N | Y euros | % | status |
| Tech Agent — architecture | X euros | N | Y euros | % | status |
| Tech Agent — design | X euros | N | Y euros | % | status |
| Steer Agent | X euros | N | Y euros | % | status |
| **TOTAL** | **X euros** | **N** | **Y euros** | **%** | |

If the orchestration log is absent: note "Orchestration log unavailable — data from `[STA-NNN]`" and use available estimates.

---

### Part 3: Consolidated dual-axis summary

Combine parts 1 and 2 into a final table:

| Axis | Initial budget (euros) | Consumed (euros) | Remaining (euros) | % consumed | EAC | Status |
|------|--------------------|-------------|--------------|------------|-----|--------|
| Human effort (total) | X euros | Y euros | Z euros | % | Y+Z euros | status |
| AI system — LLM | X euros | Y euros | Z euros | % | Y+Z euros | status |
| **PROJECT TOTAL** | **X euros** | **Y euros** | **Z euros** | **%** | **EAC** | |

*EAC = Estimate At Completion (Consumed + Remaining)*

**Analysis and alerts:**
- Any Red line → recommend creating/updating `[RSK-NNN]` R-AGT-03 (budget risk)
- If global EAC > initial budget + 15% → automatic escalation recommendation

## Imperative rules

- Always clearly indicate the source of each figure (Jira MCP, orchestration log, manual estimate)
- Never mix phases in the same row — one row per system and per profile
- EAC is always calculated as `consumed + remaining` — never as a simple extrapolation
- All Red lines must have a recommended action in the analysis
- Do not round numbers in the project's favour — display the real figures

## Output format

- **File:** `budget-{NNN}-summary-{YYYYMMDD}.md`
- **Initial status:** `draft` (to be presented at the next COPIL)
- **Numbering:** `budget-001` = first summary, incrementing thereafter
