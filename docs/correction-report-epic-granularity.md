---
title: "Granularity Defect Report — Epic & Feature Decomposition"
type: correction-report
severity: high
affected_skills:
  - sdlc-ba-specification/SKILL.md
  - sdlc-ba-specification/docs/sk-2.2-epics.md
  - sdlc-ba-specification/docs/sk-2.2b-features.md
  - sdlc-ba-scoping/docs/sk-1.4-functional-requirements.md
date: 2026-04-21
project_context: SUMER (DARES occupational health survey platform)
---

# Granularity Defect Report — Epic & Feature Decomposition

## 1. Problem Statement

During execution of the `sdlc-full` workflow on a greenfield project (SUMER), the BA specification pipeline (S2) produced a decomposition with **11 epics and 36 features** instead of the expected **2–4 epics and 16–24 features**.

The generated "features" were at **user story granularity** — individual CRUD operations or single-actor actions — rather than coherent, demonstrable business capabilities decomposable into 2–8 user stories each.

### Observed vs Expected

| Dimension | Constraint in `sk-2.2-epics.md` | Produced | Delta |
|---|---|---|---|
| Epic count | 2–4 (max 5 if genuinely independent domains) | **11** | +175% over max |
| Features per epic | 4–8 | **2–4** | Below minimum → epics too thin |
| Feature granularity | End-to-end testable capability → 2–8 user stories | Single-action items (= user stories) | Wrong level |
| Total features | ~16–32 (4 epics × 4–8 features) | **36** | +12 over theoretical max |

### Examples of Misclassified Artefacts

| Produced as Feature | Correct Classification | Reason |
|---|---|---|
| `FT-004 Password management` | User Story under a broader "Account Lifecycle" feature | Cannot be decomposed into 2+ user stories — it IS a story |
| `FT-014 Automated enrollment reminders` | User Story under "Campaign Coordination" feature | Single automated behaviour, not a demonstrable capability |
| `FT-031 S3 upload audit log` | Acceptance criterion or technical story | Not user-facing; part of "Data Export" feature |
| `FT-032 NAF import` / `FT-033 PCS import` | Two stories under a single "Reference Data Management" feature | Identical pattern, different data set — one feature, two stories |

### Examples of Over-Decomposed Epics

| Produced Epics (separate) | Should Be (merged) | Rationale |
|---|---|---|
| EP-003 Survey Unit Management + EP-004 Enrollment & Participation + EP-005 Worker Sampling + EP-006 Questionnaire Management | **Single epic: "Field Survey Execution"** | One end-to-end stakeholder journey (RU conducts survey) |
| EP-009 Data Export + EP-010 Reference Data Management | **Single epic: "Data Collection & Export"** | Same stakeholder (Admin), same business domain (data flow) |
| EP-011 Notification & Reminder System | **Not an epic — transversal technical service** | Notifications support all epics; should be features distributed across each |

---

## 2. Root Cause Analysis

### RC-1 — Detailed skill file not loaded before production (Primary)

The `SKILL.md` file for `sdlc-ba-specification` lists `docs/sk-2.2-epics.md` as a **Resource** reference — not as a mandatory pre-read. The agent read only `SKILL.md` (the summary) and proceeded to generate epics without loading `sk-2.2-epics.md`, which contains the critical granularity rules:

> *"Target: 2 to 4 Epics per project. Only exceed 4 if the scope contains genuinely independent business domains with different stakeholders."*
>
> *"An Epic should contain between 4 and 8 Features. Below 4 features, the epic is too thin — merge it with a related one."*

**Impact**: All downstream granularity constraints were invisible during generation.

**File**: `.github/skills/sdlc-ba-specification/SKILL.md` — Resources section

---

### RC-2 — Epics structured by entity/module, not by business capability

Without the granularity rules, the agent defaulted to a **domain model decomposition** pattern: one epic per entity cluster (User, Campaign, Unit, Enrollment, Sampling, QP, Training, Dashboard, Export, Ref Data, Notifications).

This is the explicit anti-pattern called out in `sk-2.2-epics.md`:

> *"❌ Do NOT create one Epic per functional screen or per entity — that produces dozens of tiny Epics and hundreds of micro User Stories."*

**Impact**: 11 entity-aligned epics instead of 3–4 capability-aligned epics.

**File**: `.github/skills/sdlc-ba-specification/docs/sk-2.2-epics.md` — Step 1

---

### RC-3 — No litmus test distinguishing features from user stories

`sk-2.2b-features.md` describes the feature granularity criterion:

> *"A Feature is a coherent and demonstrable user functionality... small enough to be broken down into 2-8 User Stories"*

But there is no **negative test** — no instruction to ask: "Can this feature be further decomposed into 2+ stories? If not, it IS a story." Without this check, fine-grained items pass as features.

**Impact**: 36 story-level items classified as features.

**File**: `.github/skills/sdlc-ba-specification/docs/sk-2.2b-features.md` — Step 2

---

### RC-4 — Requirements catalogue too granular, causing downstream cascade

The S1 functional requirements catalogue (`EXF-001`) was produced with **72 individual requirements** at a very fine grain (e.g., `REQ-005 Password expiry after 12 months`, `REQ-010 No duplicate email addresses`). The epics skill instructs:

> *"Re-read the functional requirements catalogue [EXF-001]: each functional domain is an Epic candidate."*

With 72 requirements spread across 11 "functional domains", the agent naturally produced 11 epics and near-1:1 requirement-to-feature mapping.

**Impact**: Over-granular input amplified into over-granular output at every subsequent level.

**File**: `.github/skills/sdlc-ba-scoping/docs/sk-1.4-functional-requirements.md` (if granularity guidance exists there)

---

### RC-5 — No pre-write validation gate

There is no step in the workflow that counts epics and features before writing files and validates they fall within the declared thresholds. The agent produced all 11 epic files in a single pass without self-checking.

**Impact**: No opportunity to self-correct before artefact proliferation.

**File**: `.github/skills/sdlc-ba-specification/docs/sk-2.2-epics.md` — missing between Step 1 and Step 2

---

## 3. Recommended Corrections

### Action 1 — Make skill detail files mandatory pre-reads (RC-1)

**File**: `.github/skills/sdlc-ba-specification/SKILL.md`

**Current state**: `sk-2.2-epics.md` and `sk-2.2b-features.md` are listed under `## Resources` as optional references.

**Proposed change**: Add an explicit **mandatory pre-read** instruction in each Phase:

```markdown
### Phase 2 — Epic Decomposition (agent 2.2)
> ⚠️ **MANDATORY**: Read `docs/sk-2.2-epics.md` in full BEFORE producing any epic file.
1. Load the epic template from `resources/`
2. **Read `docs/sk-2.2-epics.md`** — this contains binding granularity rules
3. Read upstream: `[DOM-001]` domain model
...
```

Same pattern for Phase 3 with `docs/sk-2.2b-features.md`.

---

### Action 2 — Add hard caps and a pre-write validation gate (RC-2, RC-5)

**File**: `.github/skills/sdlc-ba-specification/docs/sk-2.2-epics.md`

**Where**: Insert new Step 1b between current Step 1 (Epic identification) and Step 2 (Feature decomposition).

**Proposed addition**:

```markdown
### Step 1b: Granularity validation gate (BLOCKING)

Before writing any epic file, validate:

1. **Epic count**: must be between 2 and 5 inclusive.
   - If > 5: STOP. Merge epics that share the same primary stakeholder or
     the same end-to-end business journey. Common merges:
     - All survey-execution capabilities (unit, enrollment, sampling,
       questionnaires) → single epic
     - All data-flow capabilities (export, import, reference data) → single epic
     - Transversal services (notifications, reminders) are NOT epics —
       distribute as features across the epics they serve
   - If < 2: the scope may be too narrow for the sdlc-full workflow.

2. **Feature count per epic**: must be between 4 and 8.
   - If < 4: the epic is too thin — merge it into a related epic.
   - If > 8: consider splitting ONLY if features serve genuinely
     different stakeholders.

3. **Feature litmus test**: for each feature, ask:
   "Can this feature be decomposed into 2–8 distinct user stories?"
   - If NO → it is a user story, not a feature. Promote it down.
   - If YES → it is a feature. Keep it.

Only proceed to Step 2 (file writing) after all three checks pass.
```

---

### Action 3 — Add explicit anti-patterns with examples (RC-2)

**File**: `.github/skills/sdlc-ba-specification/docs/sk-2.2-epics.md`

**Where**: Expand the existing anti-pattern note in Step 1 with concrete examples.

**Proposed addition** (after the existing "❌ Do NOT create one Epic per functional screen or per entity"):

```markdown
#### Common anti-patterns and corrections

| ❌ Anti-pattern (entity-per-epic) | ✅ Correct (capability-per-epic) |
|---|---|
| EP: User Management, EP: Survey Unit, EP: Enrollment, EP: Sampling, EP: Questionnaire | **EP: Field Survey Execution** (one RU end-to-end journey) |
| EP: Campaign Management, EP: Dashboards, EP: Notifications | **EP: Campaign Orchestration** (Admin drives a campaign) |
| EP: Data Export, EP: Reference Data | **EP: Data Collection & Export** (Admin manages data flow) |
| EP: Notifications (standalone) | Not an epic — distribute notification features into each epic they support |

**Grouping heuristic**: If two candidate epics share the same primary actor
AND the same business goal, they belong in the same epic.
```

---

### Action 4 — Add feature/story litmus test (RC-3)

**File**: `.github/skills/sdlc-ba-specification/docs/sk-2.2b-features.md`

**Where**: Step 2, before producing each feature file.

**Proposed addition**:

```markdown
#### Feature granularity check (per feature, BLOCKING)

Before writing the feature file, apply this litmus test:

1. **Decomposition test**: Can this feature be broken down into 2–8
   distinct user stories, each with a different Given/When/Then?
   - ✅ "Training management" → US: create session, US: register for
     session, US: cancel registration, US: mark attendance, US: enforce
     training gate → 5 stories → valid feature
   - ❌ "Password management" → US: reset password... and that's it →
     this IS a user story, not a feature

2. **Actor test**: Does this feature serve a clearly identified actor
   with a demonstrable end-to-end capability?
   - ✅ "AQ import and worker matching" → Admin imports a file AND
     reviews match results → demonstrable flow
   - ❌ "S3 upload audit log" → no actor interaction; this is a
     technical acceptance criterion of the "Data Export" feature

3. **Demonstration test**: Could you show this feature to a stakeholder
   in a 5-minute demo and they would understand the business value?
   - ✅ "Worker sampling and inclusion" → show form, show algorithm
     result, show worker record created
   - ❌ "Automated enrollment reminders" → cannot demo in isolation;
     part of the broader "Campaign Coordination" feature

If a candidate feature fails any of these three tests, demote it to a
user story under its parent feature.
```

---

### Action 5 — Calibrate requirements catalogue granularity (RC-4)

**File**: `.github/skills/sdlc-ba-scoping/docs/sk-1.4-functional-requirements.md`

**Proposed addition** (in the granularity guidelines section, or create one if absent):

```markdown
### Requirements granularity guideline

Requirements in [EXF-001] should be at **capability level**, not at
individual-rule level. Each requirement should map to a feature (not a
user story).

**Target**: 15–30 requirements for a typical project.

| ❌ Too granular (rule-level) | ✅ Correct (capability-level) |
|---|---|
| REQ: Admin can create ADMIN accounts | REQ: The system shall manage the full lifecycle of user accounts across all role types (creation, activation, credential management, suspension) |
| REQ: Password expires after 12 months | *(covered by the above — this is a business rule, not a requirement)* |
| REQ: No duplicate email addresses | *(covered by the above — this is a validation rule)* |

**Distinction**: A *requirement* describes WHAT capability the system
must provide. A *business rule* describes HOW or under what constraints.
Business rules are captured in [BRL-xxx], not in [EXF-001].
```

---

### Action 6 — Add a worked example to `sk-2.2-epics.md`

**File**: `.github/skills/sdlc-ba-specification/docs/sk-2.2-epics.md`

**Where**: After Step 1, as an illustrative reference.

**Proposed addition**:

```markdown
### Worked example — Survey management platform (4 epics)

For a platform managing annual surveys with field doctors, admin
coordination, and statistical data export:

| Epic | Business Capability | Primary Actor | Features (count) |
|---|---|---|---|
| EP-001 Campaign Orchestration | Create and drive annual survey campaigns end-to-end | Admin | 5: Campaign lifecycle · Doctor invitation & enrollment · Monitoring dashboards · Notifications · Geographical hierarchy |
| EP-002 Field Survey Execution | Conduct the survey in the field | RU (Doctor) | 6: Survey unit management · Worker sampling · Professional questionnaire · AQ import & matching · Training management · Unit member management |
| EP-003 User & Access Management | Manage identities and authorisations | Admin / All | 4: Account lifecycle · Self-registration flow · Role-based access control · Password & credential management |
| EP-004 Data Collection & Export | Collect, store, and export survey data | Admin / System | 4: Automated weekly export · Manual export · Reference data management (NAF/PCS) · Batch processing (purge, email dispatch) |

**Total: 4 epics, 19 features** — each feature decomposes into 2–8
user stories in S3.
```

---

## 4. Summary of Changes

| # | Action | File | Type | Priority |
|---|---|---|---|---|
| A1 | Make `sk-2.2-epics.md` and `sk-2.2b-features.md` mandatory pre-reads | `sdlc-ba-specification/SKILL.md` | Instruction reinforcement | **Critical** |
| A2 | Add hard caps + pre-write validation gate (Step 1b) | `sk-2.2-epics.md` | New blocking gate | **Critical** |
| A3 | Add anti-pattern table with concrete examples | `sk-2.2-epics.md` Step 1 | Guidance expansion | High |
| A4 | Add feature/story litmus test (3 checks) | `sk-2.2b-features.md` Step 2 | New blocking check | **Critical** |
| A5 | Calibrate requirements catalogue granularity (15–30 target) | `sk-1.4-functional-requirements.md` | Guidance expansion | High |
| A6 | Add worked example for a 4-epic project | `sk-2.2-epics.md` | Illustrative reference | Medium |

---

## 5. Verification Criteria

After applying these corrections, re-run the S2 pipeline on the same SUMER inputs. The output should satisfy:

- [ ] Epic count: 3–5
- [ ] Features per epic: 4–8
- [ ] Total features: 15–25
- [ ] Every feature passes the 3-test litmus (decomposition, actor, demonstration)
- [ ] No "feature" that is actually a user story
- [ ] Requirements catalogue: 15–30 capability-level requirements
- [ ] Notifications are NOT a standalone epic — distributed as features across relevant epics
