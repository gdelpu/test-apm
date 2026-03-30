# Workflow: Maturity Assessment

Assess SDLC maturity across key dimensions and produce a scored report with an improvement roadmap.

## When to use

- Evaluating current-state SDLC capabilities across architecture, quality, security, testing, observability, and compliance
- Establishing organizational baselines for governance improvements
- Identifying quick wins and long-term strategic initiatives
- Measuring improvements between assessments (trend analysis)
- Justifying investment in tooling, training, or process improvements

## Stations

| # | Station | Agent | Skill | Gate | Severity |
|---|---------|-------|-------|------|----------|
| 1 | Assessment | repository-analyzer | repo-analysis | All dimensions evaluated, evidence collected | blocker |
| 2 | Scoring | spec-orchestrator | spec-clarify | Scores assigned (1–5 scale) per dimension, rationale documented | blocker |
| 3 | Report | spec-orchestrator | spec-feature | Executive summary, dimension breakdown, current vs. target visualized | blocker |
| 4 | Roadmap | spec-orchestrator | spec-plan | Quick wins (< 1 mo), medium-term (1–3 mo), long-term (3–12 mo) identified | blocker |

## Maturity Dimensions

The assessment evaluates:

| Dimension | Focus | Examples |
|-----------|-------|----------|
| **Architecture** | Design patterns, modularity, dependency management | Types of coupling, cohesion, service boundaries |
| **Quality** | Code standards, linting, static analysis adoption | Linting coverage, CC policies, code review rigor |
| **Security** | Secret scanning, vulnerability tracking, secure by default | SAST/SCA integration, pen testing frequency |
| **Testing** | Test pyramid implementation, coverage thresholds, test automation | Unit/integration/e2e balance, pipeline gates |
| **Observability** | Logging, monitoring, tracing instrumentation | Log aggregation, alerting, SLO/SLI tracking |
| **Compliance** | Policy enforcement, audit trails, governance gates | Data lineage tracking, regulatory checkpoints |

## Outputs

All artifacts are written to `specs/assessments/<assessment-id>/`:
- `assessment.md` — dimension-by-dimension findings with supporting evidence
- `scores.md` — maturity scores (1–5) per dimension with justification
- `maturity-report.md` — executive summary with visualizations (trends, gaps, strengths)
- `roadmap.md` — improvement initiatives sequenced by timeline and impact

## Improvement Roadmap Phases

1. **Quick Wins** — < 1 month, high impact, low effort
   - Example: Enable linting in CI/CD (if not already done)
   
2. **Medium-term** — 1–3 months, moderate effort, process/tooling changes
   - Example: Implement SonarQube gates for static analysis
   
3. **Long-term Strategic** — 3–12 months, high effort, architectural changes
   - Example: Microservices migration, observability platform adoption

Each initiative is mapped to affected dimensions and estimated effort.

## Standalone vs. nested

- **Standalone**: Run independently to assess current maturity for reporting/planning
- **Not typically nested**: This is an assessment workflow, not a delivery workflow (no code changes output)

## Use with feature-implementation

After a feature is delivered via feature-implementation, consider running maturity-assessment to evaluate how delivery processes and tooling contributed to project success.
