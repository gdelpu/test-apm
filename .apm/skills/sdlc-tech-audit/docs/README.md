# Tech-Agents — Technical Architecture & Design Domain

Automates technical design upstream of coding. Takes validated BA deliverables as input and produces a complete technical dossier + implementation plan for Claude Code.

## Role in the harness

Tech-Agents is the **second domain**. It sits between functional specification (BA) and implementation (Claude Code).

```
[BA-Agents] --> Functional specs --> [Tech-Agents] --> Technical dossier + CLAUDE.md --> [Claude Code] --> Code
```

---

## Dynamic execution

### T0 to T1 — Sequential with parallelism

```
Validated BA deliverables + technical constraints
         |
         v
  /tech-0-audit (brownfield only)
  +-------------+
  | t0.1 --> t0.2 |                               2 agents, sequential
  +-------------+
         | Human gate
         v
  /tech-1-archi
  +-----------------------------------------------------------+
  | t1.1 System Context (2 BA files)                          |
  |   |                                                       |
  | t1.2 ADRs (3 BA files → N ADR files, incl. sécu + obs)   |
  |   |                                                       |
  | t1.3 Stack Extraction (foreach ADR → 1 ADR per run)      |  parallel
  |   |                                                       |
  | t1.3b Stack Consolidation (fan-in → STK-001)             |
  |   |                                                       |
  | t1.4 Enabler Extraction (foreach ADR → 1 ADR per run)    |  parallel
  |   |                                                       |
  | t1.4b Enabler Index (fan-in → enb-000-index.md)          |
  +-----------------------------------------------------------+
         | Human gate (Architecture Review)
         v
```

### T2 — Incremental design per sprint

T2 now runs **incrementally per sprint batch** (scoped by the sprint plan from `/steer-1-planning`). Each run extends the existing deliverables rather than rewriting them.

```
  /tech-2-design --scope sprint-N
  +--------------------------------------------------+
  | t2.1 Data Model --> t2.2 API Contracts            |  incremental: adds
  |                          |                        |  tables/endpoints for
  |                     t2.4 Test Strategy             |  this sprint's items
  |                          |                        |
  |                     t2.5 Implementation Plan       |  appends new waves
  |                          + CLAUDE.md (updated)    |
  +--------------------------------------------------+
         | Human gate (Technical Review)
         v
  Claude Code Implementation (sprint's waves only)
         |
         v
```

Note: Enablers (ex-t2.3) and observability (ex-t2.6) are now in **T1** — enablers as t1.4, observability as ADR-OBS-* in t1.2.

### T3 — Continuous quality (recurring, per PR)

```
  /tech-3-quality (can run repeatedly)
  +----------------------------+
  | t3.1 Drift Detection       |               specs vs code comparison
  |         |                  |
  | t3.2 Code Review           |               per PR or before release
  |         |                  |
  | t3.3 E2E Playwright Gen    |               cross-US scripts for Test-Agents
  +----------------------------+
         |
         v
  [Test-Agents] (consumes [E2E-SCRIPTS-001])
```

---

## Agent inventory

### Pipeline agents (15 skills)

| System | Agent | Skill | Output | Context per run | Notes |
|--------|-------|-------|--------|----------------|-------|
| T0 | t0.1 Technical Audit | `sk-t0.1-technical-audit` | `[TECH-ASIS-001]` | — | brownfield only |
| T0 | t0.2 Technical Gap | `sk-t0.2-technical-gap` | `[GAP-001]` | — | brownfield only |
| T1 | t1.1 System Context | `sk-t1.1-system-context` | `[CTX-001]` | ~400 lines (2 BA files) | |
| T1 | t1.2 ADRs | `sk-t1.2-architecture-decisions` | `[ADR-xxx]` (1 file per ADR) | ~600 lines (3 BA files) | incl. security + observability |
| T1 | **t1.3 Stack Extraction** | `sk-t1.3-stack-extraction` | stack extractions | **~150 lines (1 ADR)** | **foreach ADR, sonnet** |
| T1 | **t1.3b Stack Consolidation** | `sk-t1.3b-stack-consolidation` | `[STK-001]` | ~800 lines (N extractions + GLO) | fan-in, opus |
| T1 | **t1.4 Enabler Extraction** | `sk-t1.4-enablers` | `[ENB-xxx]` | **~250 lines (1 ADR + STK)** | **foreach ADR, sonnet** |
| T1 | **t1.4b Enabler Index** | `sk-t1.4b-enabler-index` | `enb-000-index.md` | ~400 lines (N front matters) | fan-in, opus |
| T2 | t2.1 Data Model | `sk-t2.1-data-model` | `[DAT-001]` | — | incremental per sprint |
| T2 | t2.2 API Contracts | `sk-t2.2-api-contracts` | `[API-xxx]` | — | incremental per sprint |
| T2 | t2.4 Test Strategy | `sk-t2.4-test-strategy` | `[TST-001]` | — | incremental per sprint |
| T2 | t2.5 Implementation Plan | `sk-t2.5-implementation-plan` | `[IMP-001]` + `CLAUDE.md` | — | incremental per sprint |
| T3 | t3.1 Drift Detection | `sk-t3.1-drift-detection` | `[DFT-xxx]` | — | |
| T3 | t3.2 Code Review | `sk-t3.2-code-review` | Review report per PR | — | |
| T3 | t3.3 E2E Playwright Gen | `sk-t3.3-e2e-playwright-gen` | `[E2E-SCRIPTS-001]` | — | |

### Tool agents (14 skills)

| Tool | Skill | Description |
|------|-------|-------------|
| Review workshop | `sk-review-workshop-tech` | Tech deliverable review facilitation guide (presentation guide + question grids) |
| `/validate` | `sk-validate` | Tech deliverable quality audit (PASS/WARN/BLOCK) |
| `/coherence tech` | `sk-coherence-check-tech` | Tech cross-deliverable consistency (BA→Tech traceability, internal coherence) |
| `/impact` | `sk-change-impact` | Change impact + re-execution sequence `[IMPACT-xxx]` (shared with BA, bi-domain) |
| `/to-word` | `sk-word-conversion` | MD to Word (Pandoc) |
| `/confluence-push` | `tools/confluence-publish.js` | Push to Confluence |
| `/confluence-pull` | `tools/confluence-pull.js` | Sync status labels + extract comments from Confluence |
| NFR workshop prep | `sk-nfr-workshop-prep` | Prepare NFR workshop (thresholds, benchmarks) |
| NFR test specs | `sk-nfr-test-specs` | Post-workshop NFR test specs |
| Jira sync | `sk-sync-jira-tech` | Architecture tasks + enabler stories |
| Release manager | `sk-release-manager` | Release orchestration `[REL-001]` |
| Orchestrator | `sk-orchestrator-claude-code` | T1-T2 pipeline within Claude Code |
| Tech debt | `sk-tech-debt` | Clustering + impact scoring `[DEBT-001]` |

---

## Key design differences vs BA

| Aspect | BA-Agents | Tech-Agents |
|--------|-----------|-------------|
| Deliverables | Pure Markdown (specs) | Quasi-code (DDL, OpenAPI, CLAUDE.md) |
| Skills | Universal conventions | **Composable by stack** (skill-registry) |
| Fan-out | Per epic, per feature | None (project-scope) |
| Terminal deliverable | Test folder | `CLAUDE.md` + Implementation Plan |
| Amendment mode | Applies to all agents | Applies to all agents (quasi-code preservation) |
| Review prep | Question grids: VIS/GLO/ACT/EP/FT/US/SCR/BRL | Question grids: CTX/ADR/STK/ENB/DAT/API/TST/IMP |
| Coherence check | BA chains: EXF→EP→FT→US→BR→SCE | Tech chains: ENT→DAT, US→API, BR→constraints, ADR→ENB, ACT→roles |

### Composable skill-registry

Tech-Agents includes a **stack-specific skill registry** in `refs/skill-registry/`. The t2.5 agent selects and compiles relevant skills into `CLAUDE.md`:

```
refs/skill-registry/
  frameworks/     sk-react.md, ...
  infrastructure/ sk-aws.md, ...
  patterns/       sk-clean-architecture.md, ...
  data/           sk-postgresql.md, sk-schema-evolution.md
  testing/        sk-jest-rtl.md, sk-playwright.md, sk-vitest.md
```

---

## Harness structure

```
Tech-Agents/
  skills/                  15 pipeline skills + 14 tool skills
    sk-t0.1-technical-audit.md
    sk-t1.1-system-context.md
    ...
    tools/
      sk-validate.md
      sk-review-workshop-tech.md    Workshop preparation (facilitation guide + question grids)
      sk-coherence-check-tech.md    BA→Tech traceability + internal consistency
      sk-nfr-workshop-prep.md
      ...
  refs/
    conventions/           cv-tech-markdown, cv-ba-integration
    templates/             10 templates (tpl-*.md)
    skill-registry/        Composable stack-specific skills
  hooks/
    pre-input-validation.md    Phase 0: GO / WARN / STOP
    pre-amendment-mode.md      Amendment mode: surgical delta application (activated by [IMPACT-xxx])
    post-quality-control.md    Self-check + BA traceability verification
    post-confluence-push.md    Push deliverable to Confluence
  README.md
```

---

## Output structure

All Tech deliverables are written to `docs/2-tech/`:

```
docs/2-tech/
  0-audit/                         T0: tech-asis-001, gap-001
  1-architecture/                  T1: ctx-001, stk-001
    adr/                           T1: adr-xxx-{slug}.md (incl. security + observability ADRs)
  2-design/                        T2: dat-001, tst-001, imp-001 (incremental per sprint)
    api/                           T2: api-xxx-{slug}.md (multiple contracts)
    enablers/                      T1.4: enb-xxx-{slug}.md (produced by T1, consumed by sprint plan)
  3-quality/                       T3: dft-xxx, review reports
  tools/                           On-demand: coh-tech-001, impact-xxx, validation reports
```

Traceability chain: `DOM → DAT`, `US → API`, `BR → constraints`, `ADR → ENB`, `ACT → auth roles`

---

## Human verification process

The Tech pipeline alternates between **automated production** (agents) and **human verification** (gates). This section describes what the Tech reviewer (Architect / Tech Lead) must do at each gate.

### Quality layers

Each deliverable passes through 3 quality layers before reaching `validated` status:

| Layer | When | Who | What |
|-------|------|-----|------|
| **Self-check** (automatic) | During production | `post-quality-control` hook | Template conformance, BA traceability section, quasi-code validity, Production Confidence score |
| **Confluence push** (automatic) | After self-check | `post-confluence-push` hook | Page created/updated — experts can review in Confluence |
| **Human validation** (manual) | At gates | Architect + `/validate` | Structural + semantic audit, BA→Tech traceability, PASS/WARN/BLOCK verdict |

### Gate workflow

At each gate (after T0, T1, T2), the coordinator stops and displays a summary. The reviewer follows this process:

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
      +---> BLOCK    --> return to agent (re-run /tech-agent tN.N)
      |
      v
3. Run /coherence tech (Tech cross-deliverable consistency)
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

#### After T0 — Brownfield Technical Audit

| Action | Command | What to check |
|--------|---------|---------------|
| Validate audit | `/validate docs/2-tech/0-audit/tech-asis-001-*.md` | Stack assessment complete, compliance gaps flagged |
| Validate gap | `/validate docs/2-tech/0-audit/gap-001-*.md` | Migration paths justified, effort estimates plausible |

**Key question:** Is the understanding of the existing technical landscape sufficient to start architecture?

#### After T1 — Architecture

| Action | Command | What to check |
|--------|---------|---------------|
| Validate system context | `/validate docs/2-tech/1-architecture/ctx-001-*.md` | C4 L1/L2 consistent, all integrations listed |
| Validate ADRs | `/validate docs/2-tech/1-architecture/adr/adr-xxx-*.md` | Alternatives evaluated, consequences honest |
| Validate stack | `/validate docs/2-tech/1-architecture/stk-001-*.md` | Stack aligns with team skills, onboarding procedure complete |
| Validate enablers | `/validate docs/2-tech/2-design/enablers/enb-*.md` | All ADR enablers specified, wave assignment correct |
| Cross-check | `/coherence tech` | ADR decisions reflected in STK, security/obs ADRs present (>= 2 each), BA actors mapped to auth roles |

**Key question:** Is the architecture sufficiently defined to start technical design?

#### After T2 — Technical Design (main Tech gate)

| Action | Command | What to check |
|--------|---------|---------------|
| Validate data model | `/validate docs/2-tech/2-design/dat-001-*.md` | All DOM-001 entities mapped, FK/indexes defined, migrations viable |
| Validate API contracts | `/validate docs/2-tech/2-design/api/api-xxx-*.md` | All interactive US covered, error format standardised, OpenAPI valid |
| Validate enablers | `/validate docs/2-tech/2-design/enablers/enb-xxx-*.md` | Acceptance criteria testable, wave assignment correct |
| Validate test strategy | `/validate docs/2-tech/2-design/tst-001-*.md` | Test pyramid appropriate, NFR-TEST items resolved |
| Validate impl. plan | `/validate docs/2-tech/2-design/imp-001-*.md` | Wave order respects dependencies, CLAUDE.md compiles correctly |
| Cross-check | `/coherence tech` | Full BA→Tech traceability: ENT→table, US→API, BR→constraints, ENB→plan |
| Confluence review | `/confluence-pull` then `/impact` | Expert feedback analyzed and applied |

**Key question:** Is the technical dossier ready for Claude Code implementation? (= all deliverables validated, coherence score > 90%)

### Confluence review cycle

Between gates, technical experts review deliverables in Confluence. The review cycle is:

```
1. Agents produce → auto-pushed to Confluence (post-hook)
2. Experts (architects, lead devs, DevOps) read in Confluence, add comments
3. Tech reviewer runs /confluence-pull → status synced + comments extracted as text
4. Tech reviewer runs /impact with extracted comments → amendments applied
5. Updated deliverable is auto-pushed back to Confluence
6. Experts see their feedback addressed → validate or add more comments
```

This cycle can repeat as many times as needed before the gate validation.

### Client feedback & amendment workflow

After a pipeline gate, deliverables are presented to technical stakeholders in a review session. Feedback is integrated via `/impact`:

```
Gate passed (deliverables at status: validated)
      |
      v
1. Prepare review session
   /tech-agent review-workshop --scope <T1 | T2 | adr-xxx | dat-001>
   → Presentation guide + question grids per deliverable type
      |
      v
2. Run review session with architects / lead devs / DevOps (record transcript or take notes)
      |
      v
3. Run impact analysis (paste transcript or describe changes)
   /impact "ADR-003 caching strategy needs revision for new refund flow..."
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
- **Quasi-code preservation**: SQL DDL, OpenAPI YAML, k6 scripts are edited surgically (targeted lines only)
- **BA traceability update**: amendments that change BA→Tech mappings also update the traceability section
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
| `/tech-0-audit` | Brownfield technical audit (T0) |
| `/tech-1-archi` | Architecture: context, ADRs (incl. security + observability), stack, enablers (T1) |
| `/tech-2-design` | Technical design — incremental per sprint: data model, APIs, test strategy, impl plan (T2) |
| `/tech-3-quality` | Continuous quality — drift + code review (T3, recurring) |
| `/tech` | Full pipeline T0-T3 without gates |
| `/tech-agent <TN.N>` | Single agent (e.g., `/tech-agent t2.5`) |

### Tool commands

| Command | Description |
|---------|-------------|
| `/tech-agent review-workshop --scope <id>` | Prepare a Tech deliverable review session (facilitation guide + questions) |
| `/impact "<change description>"` | Analyse change impact → propose & apply amendments → run `/coherence` |
| `/validate <file>` | Audit a Tech deliverable (PASS / WARN / BLOCK) — auto-routed for `docs/2-tech/` |
| `/coherence tech` | Tech cross-deliverable consistency check |
| `/confluence-pull` | Sync status labels + extract comments (ready for `/impact`) |
| `/to-word <file>` | Convert deliverable to Word |

See [.claude/commands/README.md](../.claude/commands/README.md) for full reference.
