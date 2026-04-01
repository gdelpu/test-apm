# Skill: sdlc-tech-audit

## Goal

Perform a technical stack assessment and gap analysis for brownfield projects, identifying compliance gaps, migration paths, and estimated effort.

## When to use

- At the start of any brownfield technical engagement (System T0)
- Before architecture decisions to understand the existing technical landscape
- As the first station in the `sdlc-tech` workflow when condition `brownfield_only` is met

## Procedure

### Phase 1 — Technical Audit (agent t0.1)
1. Load the technical audit template from `resources/`
2. Read client-provided technical documentation from `docs/0-inputs/tech/0-audit/`
3. Assess current stack: languages, frameworks, infrastructure, CI/CD, observability
4. Identify compliance gaps against governance standards
5. Write `docs/2-tech/0-audit/tech-asis-001-technical-audit.md` with identifier `[TECH-ASIS-001]`

### Phase 2 — Gap Analysis (agent t0.2)
1. Load the gap analysis template from `resources/`
2. Read upstream: `[TECH-ASIS-001]` technical audit
3. Define migration paths for each identified gap
4. Estimate effort and risk for each migration path
5. Write `docs/2-tech/0-audit/gap-001-technical-gap.md` with identifier `[GAP-001]`

## Output

- `docs/2-tech/0-audit/tech-asis-001-technical-audit.md` — `[TECH-ASIS-001]`
- `docs/2-tech/0-audit/gap-001-technical-gap.md` — `[GAP-001]`

## Rules

- Only runs for brownfield projects — skip entirely for greenfield
- Must verify BA traceability: tech audit references functional modules from BA audit
- Gap analysis must include effort estimates with confidence levels

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-technical-audit.md` | Technical audit template |
| `docs/sk-t0.1-technical-audit.md` | Detailed audit procedure |
| `docs/sk-t0.2-technical-gap.md` | Detailed gap analysis procedure |
