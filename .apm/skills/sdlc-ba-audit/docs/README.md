# BA-Agents — Business Analyst Domain

Automates the work of Business Analysts: from raw business needs to a complete, structured functional specification usable by Tech-Agents and Claude Code.

## Role in the harness

BA-Agents is the **first domain** in the SDLC pipeline. It produces all functional deliverables that downstream systems consume.

```
Raw business need --> [BA-Agents] --> Functional specification --> [Tech-Agents] --> [Claude Code] --> [Test-Agents]
```

---

## Dynamic execution

### Static flow (S0 to S2 — project scope)

```
Source documents (Word, emails, meeting notes...)
         |
         v
  /ba-0-audit (brownfield only)
  +---------+
  | 0.1 --> 0.2 |                             2 agents, sequential
  +---------+
         | Human gate
         v
  /ba-1-scoping
  +---------------------------+
  | 1.1 -+-> 1.3 --> 1.4     |           4 agents
  | 1.2 -+                   |           1.1 // 1.2 parallel
  +---------------------------+
         | Human gate
         v
  /ba-2-spec
  +--------------------------------------------+
  | 2.1 --> 2.2 -+-> 2.2b(ep-001) -+-> 2.3    |  fan-out: 1 epic = N features
  |              |   2.2b(ep-002)  |           |  2.2b runs once PER EPIC
  |              |   ...           |           |  2.3 waits for ALL (fan-in)
  |              +-> 2.2b(ep-008) -+           |
  +--------------------------------------------+
         | Human gate
         v
```

### Dynamic flow (S3 — per-feature fan-out)

System 3 runs **once per feature**. With 8 epics and 39 features, it produces 39 independent sub-pipelines:

```
  /ba-3-design
  +--------------------------------------------------------------------+
  | For EACH feature (ft-001, ft-002, ..., ft-039):                    |
  |                                                                    |
  |   3.1 Stories ----+---> 3.2 Journeys  ---+                        |
  |                   |                       |                        |
  |                   +---> 3.3 Screens ------+---> 3.5 Tests --> 3.6  |
  |                   |         |             |       Seeds            |
  |                   |     3.3b Prototypes   |                        |
  |                   |                       |                        |
  |                   +---> 3.3c Batches -----+                        |
  |                   |                       |                        |
  |                   +---> 3.4 Notifs -------+                        |
  |                                                                    |
  |   (3.2 // 3.3 // 3.3c // 3.4 run in PARALLEL for each feature)    |
  +--------------------------------------------------------------------+
         |
         | Fan-in: wait for ALL 39 features to complete
         v
  +-------------------------------+
  | 3.6b E2E Plan (project scope) |   cross-feature E2E flows
  +-------------------------------+
         | Human gate (final)
         v
  [Tech-Agents]
```

**Cardinality example** with 8 epics / 39 features:
- Agent 2.2b runs **8 times** (once per epic)
- Agent 3.1 runs **39 times** (once per feature)
- Agent 3.5 runs **39 times** (once per feature)
- Agent 3.6b runs **once** (project scope, fan-in)
- Total agent executions: ~250 (not 21)

---

## Agent inventory

### Pipeline agents (19 skills)

| System | Agent | Skill | Output |
|--------|-------|-------|--------|
| S0 | 0.1 Existing Audit | `sk-0.1-existing-audit` | `[ASIS-001]` |
| S0 | 0.2 Delta Analysis | `sk-0.2-delta-analysis` | `[DELTA-001]` |
| S1 | 1.1 Product Vision | `sk-1.1-vision` | `[VIS-001]` |
| S1 | 1.2 Glossary | `sk-1.2-glossary` | `[GLO-001]` |
| S1 | 1.3 Actors & Roles | `sk-1.3-actors-roles` | `[ACT-001]` |
| S1 | 1.4 Functional Requirements | `sk-1.4-functional-requirements` | `[EXF-001]` |
| S2 | 2.1 Domain Model | `sk-2.1-domain-model` | `[DOM-001]` |
| S2 | 2.2 Epics | `sk-2.2-epics` | `[EP-xxx]` |
| S2 | 2.2b Features | `sk-2.2b-features` | `[FT-xxx]` per epic |
| S2 | 2.3 Business Rules | `sk-2.3-business-rules` | `[BRL-{type}]` (one per rule type) |
| S3 | 3.1 User Stories | `sk-3.1-user-stories` | `[US-xxx]` per feature |
| S3 | 3.2 User Journeys | `sk-3.2-user-journeys` | `[UF-xxx]` per feature |
| S3 | 3.3 Screen Specs | `sk-3.3-screen-specs` | `[SCR-xxx]` per feature |
| S3 | 3.3b HTML Prototypes | `sk-3.3b-figma-prototypes` | HTML per feature |
| S3 | 3.3c Batch Specs | `sk-3.3c-batch-specs` | `[BAT-xxx]` per feature |
| S3 | 3.4 Notifications | `sk-3.4-notifications` | `[NTF-xxx]` per feature |
| S3 | 3.5 Test Scenarios | `sk-3.5-test-scenarios` | `[SCE-xxx]` per feature |
| S3 | 3.6 Test Data | `sk-3.6-test-data` | `[DAT-TEST-xxx]` per feature |
| S3 | 3.6b E2E Plan | `sk-3.6b-e2e-plan` | `[E2E-PLAN-001]` project |

### Tool agents (17 skills)

| Tool | Skill | Description |
|------|-------|-------------|
| Discovery | `sk-discovery` | Workshop preparation + structured context `[DCO-001]` (on-demand, before scoping) |
| Review workshop | `sk-review-workshop` | Deliverable review facilitation guide (presentation guide + question grids) |
| `/validate` | `sk-validate` | Deliverable quality audit (PASS/WARN/BLOCK) |
| `/coherence` | `sk-coherence-check` | Cross-deliverable consistency |
| `/impact` | `sk-change-impact` | Change impact + re-execution sequence `[IMPACT-xxx]` |
| `/to-word` | `sk-word-conversion` | MD to Word (Pandoc) |
| Word reintegration | `sk-word-reintegration` | Annotated Word back to MD |
| Jira sync | `sk-sync-jira` | Bidirectional Jira sync |
| R4J sync | `sk-sync-r4j` | Requirements traceability |
| Xray sync | `sk-sync-xray` | Gherkin tests to Xray |
| Confluence publish | `tools/confluence-publish.js` | Publish to Confluence |
| Confluence pull | `tools/confluence-pull.js` | Sync status labels + extract comments from Confluence |
| GDPR PIA | `sk-gdpr-pia` | Privacy impact analysis |
| UAT report | `sk-uat-report` | Go/No-Go from Xray results |
| User docs | `sk-user-docs` | End-user documentation |
| Anonymization | `sk-document-anonymization` | PII anonymization |

---

## Harness structure

```
BA-Agents/
  skills/                  19 pipeline skills + 17 tool skills
    sk-0.1-existing-audit.md
    sk-1.1-vision.md
    ...
    tools/
      sk-validate.md
      sk-coherence-check.md
      sk-review-workshop.md      Workshop preparation (facilitation guide + question grids)
      ...
  refs/
    conventions/           cv-markdown, cv-domain-language, cv-brownfield, cv-output-language
    templates/             18 templates (tpl-*.md) + template-corporate.docx
                           incl. template-corporate.docx
  hooks/
    pre-input-validation.md    Phase 0: GO / WARN / STOP
    pre-amendment-mode.md      Amendment mode: surgical delta application (activated by [IMPACT-xxx])
    post-quality-control.md    Self-check + Production Confidence
    post-confluence-push.md    Push deliverable to Confluence
  README.md
```

---

## Output structure

All BA deliverables are written to `outputs/docs/1-prd/`:

```
outputs/docs/1-prd/
  0-audit/                       S0: asis-001, delta-001
  scoping/                       S1: dco-001, vis-001, glo-001, act-001, exf-001
  specification/                 S2: dom-001, brl-{type} (one per rule type)
  epics/
    ep-xxx-{slug}/               S2: epic definition
      ft-xxx-{slug}/             S2: feature spec
        user-stories/            S3: us-xxx per feature
        journeys/                S3: uf-xxx per feature
        screens/                 S3: scr-xxx per feature
        batches/                 S3: bat-xxx (if applicable)
        notifications/           S3: ntf-xxx (if applicable)
        tests/                   S3: sce-xxx + seeds-xxx per feature
  tests/                         S3: shared seeds + E2E plan (project scope)
  tools/                         On-demand: impact-xxx, validation, GDPR, UAT...
```

Traceability chain: `EXF --> EP --> FT --> US --> BR --> SCE`

---

## Human verification process

The BA pipeline alternates between **automated production** (agents) and **human verification** (gates). This section describes what the BA reviewer must do at each gate.

### Quality layers

Each deliverable passes through 3 quality layers before reaching `validated` status:

| Layer | When | Who | What |
|-------|------|-----|------|
| **Self-check** (automatic) | During production | `post-quality-control` hook | Template conformance, placeholders, minimum counts, next-reader test, Production Confidence score |
| **Confluence push** (automatic) | After self-check | `post-confluence-push` hook | Page created/updated — experts can review in Confluence |
| **Human validation** (manual) | At gates | BA reviewer + `/validate` | Structural + semantic audit, DoR verification, PASS/WARN/BLOCK verdict |

### Gate workflow

At each gate (after S0, S1, S2, S3), the coordinator stops and displays a summary. The reviewer follows this process:

```
Pipeline completes
      |
      v
1. Review the summary (deliverables produced, failures)
      |
      v
2. Run /validate on key deliverables
      |
      +---> PASS     --> switch status: draft -> validated
      +---> WARN     --> review warnings, accept or return to agent
      +---> BLOCK    --> return to agent (re-run /ba-agent N.N)
      |
      v
3. Run /coherence (cross-deliverable consistency)
      |
      v
4. Review in Confluence (expert feedback loop)
      |
      +---> Comments? --> /confluence-pull then /impact
      |
      v
5. Advance to next pipeline
```

### Gate details per system

#### After S0 — Brownfield Audit

| Action | Command | What to check |
|--------|---------|---------------|
| Validate audit | `/validate outputs/docs/1-prd/0-audit/asis-001-*.md` | Sources cited, assumptions flagged with "To validate" |
| Validate delta | `/validate outputs/docs/1-prd/0-audit/delta-001-*.md` | All ASIS elements covered, NOUVEAU/MODIFIE/PRESERVE justified |

**Key question:** Is the understanding of the existing system sufficient to start scoping?

#### After S1 — Scoping

| Action | Command | What to check |
|--------|---------|---------------|
| Validate vision | `/validate outputs/docs/1-prd/1-scoping/vis-001-*.md` | IN/OUT scope clear, objectives measurable |
| Validate glossary | `/validate outputs/docs/1-prd/1-scoping/glo-001-*.md` | No circular definitions, forbidden synonyms listed |
| Validate actors | `/validate outputs/docs/1-prd/1-scoping/act-001-*.md` | Rights matrix complete, system actors included |
| Validate requirements | `/validate outputs/docs/1-prd/1-scoping/exf-001-*.md` | MoSCoW priorities set, each requirement testable |
| Cross-check | `/coherence` | All terms in glossary used consistently, requirements traceable |

**Key question:** Is the scope sufficiently defined to structure epics and features?

#### After S2 — Specification

| Action | Command | What to check |
|--------|---------|---------------|
| Validate domain model | `/validate outputs/docs/1-prd/2-specification/dom-001-*.md` | Cardinalities specified, state diagrams for lifecycle entities |
| Validate epics | `/validate outputs/docs/1-prd/3-epics/ep-xxx-*/ep-xxx-*.md` | EAC-xxx criteria are concrete and testable, all EX-xxx covered |
| Validate features | `/validate outputs/docs/1-prd/3-epics/ep-xxx-*/ft-xxx-*/ft-xxx-*.md` | FAC-xxx criteria are concrete, functional boundaries clear |
| Validate rules | `/validate outputs/docs/1-prd/2-specification/brl-*-business-rules.md` | IF/THEN complete, calculation rules have examples |
| Cross-check | `/coherence` | EX → EP → FT coverage complete, no orphan features |

**Key question:** Is the specification detailed enough to start writing user stories?

#### After S3 — Functional Design (final BA gate)

| Action | Command | What to check |
|--------|---------|---------------|
| Validate features (DoR) | `/validate outputs/docs/1-prd/3-epics/ep-xxx-*/ft-xxx-*/ft-xxx-*.md` | **DoR READY**: all US validated, FAC covered by SCE, BR covered |
| Validate E2E plan | `/validate outputs/docs/1-prd/4-tests/e2e-plan-001.md` | All EAC/FAC covered by E2E flows, traceability matrix complete |
| Cross-check | `/coherence` | Full traceability chain EXF → EP → FT → US → BR → SCE |
| Confluence review | `/confluence-pull` then `/impact` | Expert feedback analyzed and applied |

**Key question:** Is the functional specification ready for Tech-Agents? (= all Features at DoR READY)

### Confluence review cycle

Between gates, functional experts review deliverables in Confluence. The review cycle is:

```
1. Agents produce → auto-pushed to Confluence (post-hook)
2. Experts read in Confluence, add comments, change status labels
3. BA reviewer runs /confluence-pull → status synced + comments extracted as text
4. BA reviewer runs /impact with extracted comments → amendments applied
5. Updated deliverable is auto-pushed back to Confluence
6. Experts see their feedback addressed → validate or add more comments
```

This cycle can repeat as many times as needed before the gate validation.

### Client feedback & amendment workflow

After a pipeline gate, deliverables are presented to the client in a review session. Feedback is integrated via `/impact`:

```
Gate passed (deliverables at status: validated)
      |
      v
1. Prepare review session
   /ba-agent review-workshop --scope <ft-xxx | ep-xxx | S1 | S2>
   → Presentation guide + question grids per deliverable type
      |
      v
2. Run review session with client (record transcript or take notes)
      |
      v
3. Run impact analysis (paste transcript or describe changes)
   /impact "client wants group reservations for 10+ rooms..."
   → Identifies changes, maps cascade via impact-graph.yaml
   → Proposes re-execution sequence → user confirms
   → Agents re-execute in amendment mode → /coherence runs automatically
      |
      v
4. Validate amended deliverables
   /validate <impacted files>
   → PASS → status: validated → pipeline continues
```

**Amendment mode** (activated automatically by `pre-amendment-mode.md` hook):
- Applies only the delta items from `[IMPACT-xxx]` — no rewrite of untouched sections
- Preserves all content outside the amendment scope verbatim
- Sets `status: draft` + `amended_by: IMPACT-xxx` in front matter
- Appends an `## Amendment log` section for full traceability

### Status lifecycle

```
draft ──────→ review ──────→ validated
  ↑              ↑               |
  |              |               | (agent modifies content)
  |              +───────────────+
  |                              |
  +──────────────────────────────+
```

| Transition | Triggered by |
|-----------|-------------|
| `draft` → `review` | Expert changes Confluence label (pulled via `/confluence-pull`) |
| `review` → `validated` | Expert changes Confluence label (pulled via `/confluence-pull`) |
| `validated` → `draft` | Agent modifies content (re-run or amendment) |
| `review` → `draft` | Agent modifies content (re-run or amendment) |

---

## Commands

### Pipeline commands

| Command | Description |
|---------|-------------|
| `/ba-0-audit` | Brownfield audit (S0) |
| `/ba-1-scoping` | Scoping pipeline (S1) |
| `/ba-2-spec` | Specification with epic/feature fan-out (S2) |
| `/ba-3-design` | Functional design with per-feature fan-out (S3) |
| `/ba` | Full pipeline S0-S3 without gates |
| `/ba-agent <N.N>` | Single agent (e.g., `/ba-agent 2.1`) |

### Tool commands

| Command | Description |
|---------|-------------|
| `/ba-agent review-workshop --scope <id>` | Prepare a deliverable review session (facilitation guide + questions) |
| `/impact "<change description>"` | Analyse change impact → propose & apply amendments → run `/coherence` |
| `/validate <file>` | Audit a deliverable (PASS / WARN / BLOCK) |
| `/coherence` | Cross-deliverable consistency check |
| `/confluence-pull` | Sync status labels + extract comments (ready for `/impact`) |
| `/to-word <file>` | Convert deliverable to Word |

See [.claude/commands/README.md](../.claude/commands/README.md) for full reference.
