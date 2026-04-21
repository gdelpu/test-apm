---
name: sdlc-review-arbitration
description: 'Conflict escalation protocol for independent review — structures human arbitration when reviewer and producer disagree.'
triggers: ['review conflict', 'arbitration', 'four-eyes review', 'status promotion']
---

# Skill: sdlc-review-arbitration

## Goal

Define the conflict escalation protocol for independent review. When a reviewer agent's assessment conflicts with the producer agent's self-assessment, this skill structures the human arbitration workflow and manages the `draft → validated` status promotion lifecycle.

## When to use

- After `sdlc-ba-reviewer`, `sdlc-tech-reviewer`, or `sdlc-steer-reviewer` produces a review report
- When the review report contains any CONFLICT verdicts
- When the coordinator needs to process status promotions from a PASS review

## Procedure

### Phase 1: Review Report Processing

1. Read the review report produced by the reviewer agent
2. Parse the `verdicts` section: extract per-deliverable PASS / WARN / CONFLICT
3. Parse the `status_promotions` section: extract files eligible for promotion
4. Parse the `conflicts` section: extract disagreements

### Phase 2: Auto-Promote on PASS

If all verdicts are PASS or WARN (no CONFLICT):

1. For each file in `status_promotions`:
   - Read the file
   - Update YAML frontmatter: `status: draft` → `status: validated`
   - Write the file back
2. Log the promotions in the workflow state file
3. Continue the workflow to the next station

### Phase 3: Conflict Escalation (human-in-the-loop)

If any verdict is CONFLICT:

1. **Present the conflict summary** to the human:

```markdown
## Review Conflict — Human Arbitration Required

### Conflicting Deliverables

| Deliverable | Producer Assessment | Reviewer Assessment | Conflict Reason |
|-------------|--------------------|--------------------|-----------------|
| [US-001] user-story-checkout.md | 3/3 CONFIDENT | INSUFFICIENT | Missing GWT for error path |
| [BRL-001] business-rules.md | 2/3 (scope PARTIAL) | CONFLICT | Rule BR-VAL-003 lacks IF/THEN |

### Producer's Position
<!-- Extract from producer's Production Confidence section -->

### Reviewer's Position
<!-- Extract from reviewer's conflict findings -->

### Options
1. **Accept producer** — Override reviewer, promote to `validated`
2. **Accept reviewer** — Send back to producer for rework
3. **Partial** — Accept some deliverables, rework others
```

2. **Wait for human decision** (workflow halts at the review gate)

3. **Process the decision**:

| Decision | Action |
|----------|--------|
| Accept producer | Promote all listed files to `validated`, log override with justification |
| Accept reviewer | Mark review station as `failed`, loop back to the producing station |
| Partial | Promote accepted files, loop back rejected files to producer |

### Phase 4: Rework Loop

When the human accepts the reviewer's assessment (full or partial):

1. The coordinator re-dispatches the producing agent for the rejected deliverables only
2. The producing agent reads the reviewer's findings as input (knows what to fix)
3. After rework, the reviewer agent runs again on the updated deliverables
4. The cycle repeats until PASS or human override

Maximum rework iterations: **2**. After 2 rework cycles without resolution, the conflict escalates to the COPIL/Go-No-Go station with a mandatory human decision.

## Output

### Review Report Format

The reviewer agent must produce the review report in this structure:

```markdown
# Review Report — [domain] Pipeline

**Reviewer:** sdlc-[domain]-reviewer
**Date:** YYYY-MM-DD
**Scope:** [list of deliverables reviewed]

## Overall Verdict: PASS | WARN | CONFLICT

## Verdicts

| # | Deliverable | File | Verdict | Producer Score | Reviewer Score | Findings |
|---|-------------|------|---------|---------------|----------------|----------|
| 1 | [VIS-001] | vis-001-product-vision.md | PASS | 3/3 | CONFIDENT | — |
| 2 | [US-001] | us-001-checkout.md | CONFLICT | 3/3 | INSUFFICIENT | Missing error path GWT |

## Conflicts

### Conflict 1: [US-001] us-001-checkout.md

**Producer says:** Production confidence 3/3 CONFIDENT — "All acceptance criteria defined"
**Reviewer finds:** Acceptance criterion CA-003 has non-observable Then clause ("works correctly")
**Impact:** Test scenario cannot be derived from this criterion
**Recommendation:** Rewrite CA-003 with specific observable outcome

## Status Promotions

Files eligible for `draft → validated` (only if overall verdict is PASS or WARN):

```yaml
status_promotions:
  - file: outputs/docs/1-prd/vis-001-product-vision.md
    verdict: PASS
  - file: outputs/docs/1-prd/glo-001-glossary.md
    verdict: WARN
    warnings: ["GLO-T012 term used only once"]
```

## Coherence Summary

| Check | Result | Critical | Major | Minor |
|-------|--------|----------|-------|-------|
| Referential integrity | PASS | 0 | 0 | 2 |
| Orphan detection | WARN | 0 | 1 | 0 |
| Coverage chains | PASS | 0 | 0 | 0 |
| Testability | CONFLICT | 1 | 0 | 0 |
```

## Rules

- The reviewer MUST produce the report as a file on disk, never only in chat
- CONFLICT verdict requires at least one specific finding with evidence
- PASS verdict with warnings must document every warning
- Status promotions are only listed when overall verdict is PASS or WARN
- The rework loop maximum is 2 iterations — after that, escalate to COPIL

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/sk-review-report-template.md` | Review report template (this skill defines the format inline above) |
