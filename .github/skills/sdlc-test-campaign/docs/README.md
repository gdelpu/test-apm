# Test-Agents — Qualification Campaigns Domain

Executes system qualification campaigns — E2E tests, performance tests, and DAST security scans — once the application is fully assembled. **This system executes and reports; it does not design test cases.**

## Role in the harness

Test-Agents is the **third domain**, positioned after implementation. It consumes plans from BA-Agents and scripts from Tech-Agents.

```
[BA-Agents]  --> [E2E-PLAN-001] + [DAT-TEST-001] --+
                                                     +--> [Test-Agents] --> [QUAL-GNG-001]
[Tech-Agents] --> [E2E-SCRIPTS-001] + k6/ZAP scripts+                         |
                                                                               v
                                                                      [Steer-Agents Go/No-Go]
```

---

## Dynamic execution

### Campaign + Performance — parallel systems

```
  /test-1-campaign                              /test-2-perf
  +----------------------------+                +----------------------------+
  | camp.1 Campaign Launch     |                | perf.1 Perf Execution      |
  |   - Prerequisites check    |                |   - Runs k6/Artillery      |
  |   - Load seeds             |    CAN RUN     |   - Collects JSON results  |
  |   - Create Xray campaign   |   IN PARALLEL  |                            |
  |   - Execute E2E scripts    |  <-----------> | perf.2 Perf Report         |
  |   - Log anomalies in Jira  |                |   - Analysis vs thresholds |
  |                            |                |   - Baseline comparison    |
  | camp.2 Campaign Report     |                |   - [PERF-RPT-NNN]        |
  |   - Anomaly classification |                +----------------------------+
  |   - Pass/Fail/Blocked      |
  |   - [CAMP-RPT-NNN]        |
  |   - [QUAL-GNG-001]        |
  +----------------------------+
              |                                         |
              +------- Both feed into --------+         |
                                              v         v
                                   /steer-3-copil (Go/No-Go)

  /dast (on-demand, typically pre-release)
  +----------------------------+
  | agent-dast                 |
  |   - OWASP ZAP scan        |
  |   - Alert triage by        |
  |     severity               |
  |   - [DAST-RPT-NNN]        |
  +----------------------------+
```

### Cardinality

Test-Agents has **no fan-out** — each agent runs once per campaign. But the same pipeline can be invoked multiple times:
- Internal E2E campaign (team runs tests)
- UAT campaign (client runs acceptance) — same pipeline, different actor
- Regression campaign (after a hotfix)

The `/test-1-campaign uat` argument changes the campaign type, not the pipeline structure.

---

## Agent inventory

### Pipeline agents (4 skills)

| System | Agent | Skill | Output |
|--------|-------|-------|--------|
| E1 | camp.1 Campaign Launch | `sk-camp.1-launch` | Xray campaign created, anomalies logged |
| E1 | camp.2 Campaign Report | `sk-camp.2-report` | `[CAMP-RPT-NNN]` + `[QUAL-GNG-001]` |
| E2 | perf.1 Perf Execution | `sk-perf.1-execution` | k6/Artillery results in `tests/results/` |
| E2 | perf.2 Perf Report | `sk-perf.2-report` | `[PERF-RPT-NNN]` |

### Tool agents (1 skill)

| Tool | Skill | Description |
|------|-------|-------------|
| `/dast` | `sk-dast` | OWASP ZAP scan + alert triage `[DAST-RPT-NNN]` |

---

## Cross-domain dependencies

| Input | Produced by | Used by |
|-------|-------------|---------|
| `[E2E-PLAN-001]` | BA agent-3.6b | camp.1, camp.2 |
| `[DAT-TEST-001]` | BA agent-3.6 | camp.1 (seeds) |
| `[E2E-SCRIPTS-001]` | Tech agent-t4.3 | camp.1 (Playwright execution) |
| `[NFR-TEST-xxx]` + k6 scripts | Tech T2.4 | perf.1, agent-dast |
| Drift report | Tech T4.1 | camp.1 (entry criterion) |
| `[QUAL-GNG-001]` | camp.2 | Steer agent-p3.2 (Go/No-Go) |

---

## Key principles

1. **Executes, does not design** — plans and scripts come from upstream
2. **Xray = source of truth** for functional test statuses
3. **Cumulative Go/No-Go** — `[QUAL-GNG-001]` aggregates E2E + perf + DAST
4. **Never in production** — qualification/staging environment only
5. **Strict BLOCK on prerequisites** — never bypass entry criteria

---

## Harness structure

```
Test-Agents/
  skills/                  4 pipeline skills + 1 tool skill
    sk-camp.1-launch.md
    sk-camp.2-report.md
    sk-perf.1-execution.md
    sk-perf.2-report.md
    tools/
      sk-dast.md
  refs/
    conventions/           cv-test-conventions
  hooks/                   pre-input-validation, post-quality-control, post-confluence-push
  README.md
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/test-1-campaign` | E2E/UAT campaign launch + report (E1) |
| `/test-2-perf` | Performance execution + report (E2) |
| `/test` | Full test pipeline (E1 + E2) |
| `/test-agent <id>` | Single agent (e.g., `/test-agent camp.1`) |
| `/dast` | OWASP ZAP security scan (on-demand) |
