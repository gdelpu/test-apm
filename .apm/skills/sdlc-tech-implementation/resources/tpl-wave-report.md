# Wave Completion Report — Wave {{WAVE_ID}}

---
id: WAVE-REPORT-{{WAVE_ID}}
sprint_range: "Sprint {{FIRST_SPRINT}} – Sprint {{LAST_SPRINT}}"
wave: {{WAVE_ID}}
status: PASSED | FAILED
date: {{DATE}}
---

## 1. Summary

| Metric | Value |
|--------|-------|
| Wave | {{WAVE_ID}} |
| Items completed | {{COMPLETED}} / {{TOTAL}} |
| Sprints spanned | {{SPRINT_COUNT}} |
| Total estimated effort | {{EFFORT}}h |
| Build status | PASS / FAIL |
| Test status | PASS / FAIL |
| Coverage (backend) | {{COV_BE}}% |
| Coverage (frontend) | {{COV_FE}}% |

## 2. Completed items

| Item ID | Title | Sprint | Estimate | Status |
|---------|-------|--------|----------|--------|
| {{ITEM_ID}} | {{TITLE}} | {{SPRINT}} | {{EST}}h | done |

## 3. Gate evaluation

### Wave DoD from [IMP-001]

| Criterion | Result | Evidence |
|-----------|--------|----------|
| {{CRITERION}} | PASS / FAIL | {{EVIDENCE}} |

### Cumulative quality

| Check | Result |
|-------|--------|
| All item validations passed | YES / NO |
| Secret scan clean | YES / NO |
| SAST clean (critical) | YES / NO |
| ADR compliance verified | YES / NO |

## 4. Issues and risks

| Issue | Severity | Mitigation |
|-------|----------|------------|
| — | — | — |

## 5. Next wave

- **Next wave:** {{NEXT_WAVE}}
- **Estimated items:** {{NEXT_COUNT}}
- **Prerequisites met:** YES / NO
