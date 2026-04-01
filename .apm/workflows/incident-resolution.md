# Workflow: Incident Resolution

Structured incident diagnosis and resolution from analysis through fix, regression testing, and knowledge capture.

## When to use

- Production incidents requiring structured root-cause analysis
- High-severity outages where timeline reconstruction matters
- When you need to capture lessons learned and prevent recurrence
- Incidents that require both a fix and a knowledge update (ADR/playbook)

## Key differences from bug-fixing

- Starts with incident analysis (logs, traces, timeline) instead of bug triage
- Includes a dedicated knowledge update station for ADR/playbook generation
- Focuses on production incidents with broader impact analysis
- Emphasizes prevention and monitoring improvements alongside the fix

## Stations

| # | Station | Agent | Skills | Gate | Severity |
|---|---------|-------|--------|------|----------|
| 1 | Incident Analysis | analysis-agent | incident-analysis, repo-analysis | Services identified, timeline reconstructed | blocker |
| 2 | Root Cause Hypothesis | analysis-agent | root-cause-analysis | Hypothesis stated with evidence | blocker |
| 3 | Reproduction Scenario | analysis-agent | incident-analysis, bug-reproduction | Steps documented, env specified | blocker |
| 4 | Fix Proposal | implementer | fix-planning, code-implementation | Minimal fix, blast radius assessed | blocker |
| 5 | Regression Test | implementer | code-implementation, test-strategy | Regression test passes with fix | blocker |
| 6 | Patch Validation | quality-validator | lint-analysis, coverage-assessment, security-scan | Build + tests pass, no side effects | blocker |
| 7 | Knowledge Update | spec-orchestrator | knowledge-update, adr-generation | ADR created, preventive measures documented | warning |

## Outputs

All artifacts are written to `specs/features/<feature>/`:
- `incident-analysis.md` — Timeline, affected services, logs/traces
- `root-cause.md` — Root cause with evidence and alternatives
- `reproduction.md` — Steps to reproduce with environment details
- `plan.md`, `tasks.md` — Fix proposal and implementation tasks
- `regression-tests.md` — Regression test documentation
- `validation-report.md` — Build, test, security validation
- `knowledge-update.md` — ADR, playbook entry, monitoring improvements

## Composition

Can trigger `quality-validation` as a nested workflow in station 6 for thorough validation.
The knowledge update feeds back into `knowledge/` and `specs/decisions/` for organizational learning.
