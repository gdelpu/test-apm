# Sprint 3 & 4 Test Plan

## Overview

| Scenario | Sprint 3 (Fix Suggestions) | Sprint 4 (Attempt Counter) | Gate Triggered |
|----------|---------------------------|---------------------------|----------------|
| 1 - All validators fire | 6+ suggestions | `[AI-FIX-ATTEMPT:1]` | No |
| 2 - Partial fix | 2 suggestions | `[AI-FIX-ATTEMPT:2]` | No |
| 3 - Warnings only | Advisory suggestions only | Counter stays same | No |
| 4 - Human gate (x3 pushes) | 3 suggestions each | `[AI-FIX-ATTEMPT:3]` | **YES - exit 1** |
| 5 - YAML parse error | `yaml_parse_error` suggestion | `[AI-FIX-ATTEMPT:1]` | No |
| 6 - Clean pass | No suggestions section | No tag | No |

---

## How to Run Each Scenario

> All scenarios use branch `test/gitlab-ci-validation` and MR #4.
> Run commands from repo root. After each push, check the `report:summary` job artifacts (`comment.md`).

---

## Scenario 1 — All Validators Fire

**Goal**: Verify all 3 validators detect issues and Sprint 3 generates 6+ fix suggestions on first push.

**Files**: `scenarios/scenario-1-all-validators-fire/`
- `SKILL.md` — no frontmatter (pr_auto_validator)
- `workflow.yml` — no `on` trigger, no permissions, uses `@main` (yaml_workflow_linter)
- `tools/scripts/helper.py` — script with no docs (test_gap_detector)

**Steps**:
```bash
git add default/skills/test-validation/scenarios/scenario-1-all-validators-fire/
git commit -m "test(s1): all validators fire"
git push
```

**Expected Sprint 3 output** in `comment.md`:
```
### Structured Fix Suggestions
1. **skill_frontmatter_missing** (default/skills/test-validation/scenarios/scenario-1-all-validators-fire/SKILL.md)
   - Proposed fix: Add SKILL frontmatter: ---\nname: skill-name\n...
2. **workflow_on_missing** (...)
   - Proposed fix: Add an 'on:' trigger block...
3. **workflow_permissions_missing** (...)
   - Proposed fix: Add minimal permissions block...
4. **workflow_uses_main** (...)
   - Proposed fix: Pin action version by tag or SHA...
5. **scripts_without_docs** (docs/README scope)
   - Proposed fix: Add or update markdown docs/examples...
```

**Expected Sprint 4 output**:
```
[AI-FIX-ATTEMPT:1]
```

---

## Scenario 2 — Partial Fix (Attempt 2)

**Goal**: Fix the SKILL frontmatter. Workflow issues remain. Counter increments to 2.

**Files**: `scenarios/scenario-2-partial-fix/`
- `SKILL.md` — now has correct frontmatter ✅
- `workflow.yml` — still missing permissions, still uses `@main` ❌

**Steps**:
```bash
git add default/skills/test-validation/scenarios/scenario-2-partial-fix/
git commit -m "test(s2): partial fix - frontmatter resolved, workflow issues remain"
git push
```

**Expected Sprint 3 output**: 2 fix suggestions (only workflow issues)

**Expected Sprint 4 output**:
```
[AI-FIX-ATTEMPT:2]
```

---

## Scenario 3 — Warnings Only (No Blocking)

**Goal**: Verify that advisory warnings do NOT increment the attempt counter.

**Files**: `scenarios/scenario-3-warnings-only/`
- `SKILL.md` — valid frontmatter ✅
- `workflow.yml` — fully valid (pinned SHA, permissions, `on` trigger) ✅
- `tools/scripts/undocumented.py` — script without docs (warning only) ⚠️

**Steps**:
```bash
git add default/skills/test-validation/scenarios/scenario-3-warnings-only/
git commit -m "test(s3): warnings only - no blocking issues"
git push
```

**Expected Sprint 3 output**: Only advisory suggestion (`scripts_without_docs`)

**Expected Sprint 4 output**: **No `[AI-FIX-ATTEMPT:N]` tag** — counter must NOT increment for warnings-only runs.

---

## Scenario 4 — Human Gate (3 Pushes)

**Goal**: Trigger the Sprint 4 human review gate by pushing the same blocking issue 3 times.

**Files**: `scenarios/scenario-4-human-gate/`
- `SKILL.md` — valid frontmatter ✅
- `workflow.yml` — missing top-level `on`, uses `@main`, no permissions ❌ (intentionally kept broken)

**Push 1**:
```bash
git add default/skills/test-validation/scenarios/scenario-4-human-gate/
git commit -m "test(s4-attempt1): keep blocking workflow issues"
git push
```
Expected: `[AI-FIX-ATTEMPT:1]`

**Push 2** (touch something to force a diff):
```bash
# Edit SKILL.md description slightly
git add default/skills/test-validation/scenarios/scenario-4-human-gate/SKILL.md
git commit -m "test(s4-attempt2): still blocking"
git push
```
Expected: `[AI-FIX-ATTEMPT:2]`

**Push 3**:
```bash
# Touch again
git add default/skills/test-validation/scenarios/scenario-4-human-gate/SKILL.md
git commit -m "test(s4-attempt3): should trigger human gate"
git push
```
**Expected Sprint 4 output**:
```
[AI-FIX-ATTEMPT:3]

### Human Review Gate
AI reached iteration 3 - human review required.
```
**Expected Sprint 3 output**: 3 suggestions (`workflow_on_missing`, `uses_main_reference`, `permissions_missing`)

**Expected pipeline result**: `report:summary` exits with code 1 — blocking MR merge.

---

## Scenario 5 — YAML Parse Error

**Goal**: Verify yaml_workflow_linter handles malformed YAML gracefully and suggests a fix.

**Files**: `scenarios/scenario-5-yaml-parse-error/`
- `workflow.yml` — intentionally malformed YAML (unclosed string, colon in env value)

**Steps**:
```bash
git add default/skills/test-validation/scenarios/scenario-5-yaml-parse-error/
git commit -m "test(s5): malformed workflow YAML"
git push
```

**Expected Sprint 3 output**:
```
1. **yaml_parse_error** (scenarios/scenario-5-yaml-parse-error/workflow.yml)
   - Proposed fix: Fix YAML syntax error - check indentation, quotes, and special characters
```

---

## Scenario 6 — Clean Pass (Happy Path)

**Goal**: Verify the pipeline passes cleanly with zero suggestions when all files are correct.

**Files**: `scenarios/scenario-6-clean-pass/`
- `SKILL.md` — valid frontmatter ✅
- `workflow.yml` — pinned SHA, explicit permissions, `on` trigger ✅

**Steps**:
```bash
git add default/skills/test-validation/scenarios/scenario-6-clean-pass/
git commit -m "test(s6): clean pass - all validators green"
git push
```

**Expected `comment.md`**:
```
## MR Validation Summary

### PR Auto Validator
**Status:** PASS

### YAML Workflow Linter
**Status:** PASS

### Test Gap Detector
**Status:** PASS
```
No `Structured Fix Suggestions` section. No `[AI-FIX-ATTEMPT:N]` tag.

---

## Verification Checklist

After each pipeline run, download the `report:summary` artifacts and check:

**Sprint 3**:
- [ ] `comment.md` contains `### Structured Fix Suggestions` when issues exist
- [ ] Each suggestion has `file`, `issue key` (bold), and `Proposed fix:` text
- [ ] Number of suggestions matches number of detected issues
- [ ] No suggestions section when pipeline is clean (Scenario 6)

**Sprint 4**:
- [ ] `[AI-FIX-ATTEMPT:N]` tag appears in comment when blocking issues exist
- [ ] Counter increments correctly across pushes (1 → 2 → 3)
- [ ] Counter does NOT increment when only warnings present (Scenario 3)
- [ ] `attempt-state.json` contains correct `current_attempt`, `has_blocking`, `human_review_required`
- [ ] `report:summary` exits code 1 at attempt 3 (Scenario 4, push 3)
- [ ] MR comment shows Human Review Gate section at attempt 3
