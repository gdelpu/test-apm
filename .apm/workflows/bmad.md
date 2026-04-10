# Workflow: BMAD

Build → Measure → Analyze → Decide feedback loop. Drives hypothesis-driven delivery with continuous quality feedback and adaptive decision-making.

## When to use

- Iterative delivery with continuous measurement and adaptation
- When acceptance criteria need measurable validation across iterations
- When quality drift detection and hypothesis-driven decisions are required
- Exploring uncertain or experimental features with real-world measurement

## Stations

| # | Station | Agent | Skill | Inputs | Outputs | Gate | Severity |
|---|---------|-------|-------|--------|---------|------|----------|
| 1 | Build | implementer | code-implementation | hypothesis.md | build-log.md | Minimum viable change deployed, instrumentation in place | blocker |
| 2 | Measure | quality-validator | coverage-assessment | build-log.md | metrics.md | Key metrics collected, data meaningful | blocker |
| 3 | Analyze | spec-orchestrator | spec-clarify | metrics.md, hypothesis.md | analysis.md | Metrics interpreted against criteria, root causes identified | blocker |
| 4 | Decide | spec-orchestrator | adr-generation | analysis.md | decision.md | Decision recorded (pivot/persevere/stop), next actions documented | blocker |

## Loop behavior

The BMAD cycle supports up to 3 retry iterations based on the Decide station outcome:

- **Persevere**: Proceed to close or move to next hypothesis
- **Pivot**: Return to Build station with updated hypothesis
- **Stop**: End the cycle with documented rationale
- **Escalate**: Route to human review
- **Revise**: Return to Measure with improved instrumentation

## Outputs

All artifacts are written to `outputs/specs/features/<feature>/`:
- `hypothesis.md` (input, initial hypothesis statement)
- `build-log.md` (from Build)
- `metrics.md` (from Measure)
- `analysis.md` (from Analyze)
- `decision.md` (from Decide)

## Key differences from feature-implementation

- No specification or architecture review stations — assumption is pre-agreed hypothesis
- Focuses on empirical measurement and outcome-driven decisions
- Supports up to 3 iterations allowing adaptive refinement
- Output is a decision record and supporting data, not production code (unless Decide approves perseverance)
