# Convention: Agentic Steering

## Objective

Defines risks, metrics, and thresholds specific to agentic project steering.

---

## Agentic risk taxonomy

| ID | Risk | Description |
|----|------|-------------|
| R-AGT-01 | Context drift | Agent produces content contradicting a validated upstream deliverable |
| R-AGT-02 | Blocked gate | Human validation overdue, blocking dependent agents |
| R-AGT-03 | LLM budget overrun | Token consumption > 130% of phase budget |
| R-AGT-04 | Critical MCP unavailable | Jira, Xray, or other MCP server down |
| R-AGT-05 | Unresolved business ambiguity | BA grey zones propagated to Tech without clarification |
| R-AGT-06 | Prompt quality drift | Agent requires > 3 iterations to produce acceptable output |

---

## Agentic metrics

| Metric | Source | Threshold |
|--------|--------|-----------|
| Gate passage speed | Jira MCP | <= 2 days overdue |
| Validated deliverable ratio | Git + YAML status | >= 85% at end of phase |
| Average replay rate | orchestration-log.jsonl | <= 1.5 iterations/agent |
| Gate resolution time | Jira MCP | <= 2 business days |
| Token consumption | orchestration-log.jsonl | Within phase budget |

---

## Alert and escalation thresholds

| Condition | Level | Action |
|-----------|-------|--------|
| Effort > 80% with > 50% phases remaining | Yellow | Risk entry [RSK-NNN] |
| Effort > 100% | Red | Escalation [DEC-NNN] |
| Tokens > 110% current phase | Yellow | Alert |
| Tokens > 130% | Red | Escalation [RSK-NNN] |
| Replay rate > 1.5 | Yellow | Alert |
| Replay rate > 2.5 | Red | Escalation |
| Gate overdue 1-2 days | Yellow | Alert |
| Gate overdue >= 3 days | Red | Sponsor escalation |

---

## Token cost reference

| Model | Input ($/M tokens) | Output ($/M tokens) |
|-------|--------------------|--------------------|
| claude-opus-4 | 15.00 | 75.00 |
| claude-sonnet-4-5 | 3.00 | 15.00 |
| claude-haiku-3-5 | 0.80 | 4.00 |
