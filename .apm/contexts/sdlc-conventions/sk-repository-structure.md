# Skill: Repository Structure

## Objective

This skill defines the **canonical directory structure** of the target project repository. It is the **single source of truth** used by all agent systems (BA / Tech / Test / Steer) to determine where to read and write deliverables and code artefacts.

> **No file path convention should be defined in individual agent instructions or system-specific skills.** Always reference this skill.

---

## 1. Monorepo principle

All project artefacts — functional documentation, technical documentation, steering reports, source code, and tests — live in a **single Git repository**. This enables:
- Full traceability across systems without cross-repo links
- A single `CLAUDE.md` entry point for Claude Code
- Unified GitLab navigation (auto-rendered `README.md` at each folder level)

---

## 2. Full directory tree

```
{project-root}/
├── CLAUDE.md                                 # Claude Code entry point (produced by T-2.5)
├── README.md                                 # Project overview
├── api/
│   └── openapi.yaml                          # Generated OpenAPI spec (T-2.2)
│
├── docs/
│   ├── prd/                                  # Product Requirements Document (BA system output)
│   │   ├── README.md                         # Static PRD index — auto-rendered by GitLab
│   │   ├── 0-audit/                          # Brownfield projects only
│   │   │   ├── asis-001-existing-audit.md
│   │   │   └── delta-001-delta-analysis.md
│   │   ├── scoping/                          # Project-level scoping (System 1)
│   │   │   ├── dco-001-discovery.md
│   │   │   ├── vis-001-product-vision.md
│   │   │   ├── glo-001-glossary.md
│   │   │   ├── act-001-actors-roles.md
│   │   │   └── exf-001-functional-requirements.md
│   │   ├── specification/                    # Project-level cross-cutting specs (System 2)
│   │   │   ├── dom-001-domain-model.md
│   │   │   └── brl-{type}-business-rules.md   # One file per rule type (dynamic)
│   │   ├── epics/                            # Business hierarchy: epic > feature > artefacts
│   │   │   └── ep-xxx-{slug}/
│   │   │       ├── ep-xxx-{slug}.md          # Epic definition + feature index table (agent-2.2)
│   │   │       ├── brl-ep-xxx.md             # Business rules scoped to this epic (if any)
│   │   │       └── ft-xxx-{slug}/            # One folder per feature (agent-2.2b)
│   │   │           ├── ft-xxx-{slug}.md      # Feature specification (agent-2.2b)
│   │   │           ├── brl-ft-xxx.md         # Business rules scoped to this feature (if any)
│   │   │           ├── user-stories/
│   │   │           │   └── us-xxx-{slug}.md
│   │   │           ├── journeys/
│   │   │           │   └── uf-xxx-{slug}.md
│   │   │           ├── screens/
│   │   │           │   └── scr-xxx-{slug}.md
│   │   │           ├── batches/              # If applicable
│   │   │           │   └── bat-xxx-{slug}.md
│   │   │           ├── notifications/        # If applicable
│   │   │           │   └── ntf-xxx-{slug}.md
│   │   │           └── tests/
│   │   │               ├── sce-xxx-{slug}.md       # Gherkin test scenarios
│   │   │               └── seeds-xxx-{slug}.md     # Test data for this feature
│   │   ├── tests/                            # Campaign-level test artefacts (project scope)
│   │   │   ├── dat-test-001-shared-seeds.md  # Seeds shared across features
│   │   │   └── e2e-plan-001.md               # E2E test plan and campaign flows
│   │   └── tools/                            # On-demand BA tool outputs
│   │       ├── impact-{NNN}-{slug}.md
│   │       ├── val-{id}-{date}.md
│   │       ├── gdpr-001-pia.md
│   │       ├── uat-001-acceptance-report.md
│   │       ├── udoc-001-user-docs.md
│   │       ├── plan-001-sprint-planning.md
│   │       ├── confluence-mapping.md
│   │       └── xray-mapping.json
│   │
│   ├── tech/                                 # Technical documentation (Tech system output)
│   │   ├── README.md                         # Static tech doc index — auto-rendered by GitLab
│   │   ├── 0-audit/                          # Brownfield projects only
│   │   │   ├── tech-asis-001-audit.md
│   │   │   └── gap-001-technical-gap.md
│   │   ├── 1-architecture/
│   │   │   ├── ctx-001-system-context.md
│   │   │   ├── adr/                          # One file per Architecture Decision Record
│   │   │   │   └── adr-xxx-{slug}.md
│   │   │   ├── stk-001-stack-conventions.md
│   │   │   └── sec-001-security-architecture.md
│   │   ├── 2-design/
│   │   │   ├── dat-001-data-model.md
│   │   │   ├── api/                          # One file per API contract
│   │   │   │   └── api-xxx-{slug}.md
│   │   │   ├── enablers/                     # One file per technical enabler
│   │   │   │   └── enb-xxx-{slug}.md
│   │   │   ├── tst-001-test-strategy.md
│   │   │   ├── imp-001-implementation-plan.md
│   │   │   └── obs-001-observability.md
│   │   ├── 3-implementation/                 # Wave-based implementation outputs
│   │   │   ├── wave-state.json
│   │   │   ├── current-task-{item_id}.md
│   │   │   ├── impl-log-{item_id}.md
│   │   │   ├── test-log-{item_id}.md
│   │   │   ├── validation-{item_id}.md
│   │   │   ├── wave-{wave_id}-report.md
│   │   │   └── sprint-{sprint_id}-summary.md
│   │   └── 4-quality/                        # Per-PR and on-demand quality reports
│   │       ├── drift-report-{YYYY-MM-DD}.md
│   │       ├── code-review-{PR-ID}-{YYYY-MM-DD}.md
│   │       └── debt-001-backlog.md
│   │
│   └── steer/                                # Steering documentation (Steer system output)
│       ├── README.md                         # Static steer index — auto-rendered by GitLab
│       ├── pil-001-project-sheet.md
│       ├── kpi-001-baseline-kpis.md
│       ├── rdp-001-roadmap.md
│       ├── rsk-001-risk-register.md
│       ├── sprint-reports/
│       │   └── sta-{NNN}-sprint-{nn}.md
│       ├── committees/
│       │   └── cop-{NNN}-{date}.md
│       └── gng-001-release-gonogo.md
│
├── src/                                      # Source code (structure defined by T-1.3 / STK-001)
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   │   ├── flows/                            # Playwright specs [E2E-FLX-xxx].spec.ts (T-3.3)
│   │   ├── fixtures/
│   │   │   └── seeds.ts
│   │   ├── helpers/
│   │   │   └── auth.ts
│   │   └── selectors/
│   │       └── {E2E-FLX-xxx}.ts
│   ├── nfr/
│   │   ├── load/                             # k6 / Artillery scripts
│   │   ├── security/                         # OWASP ZAP scripts
│   │   └── accessibility/                    # axe-core scripts
│   └── results/                              # Generated results (see .gitignore rules below)
│       ├── performance/
│       └── campaigns/
│
├── migrations/                               # Database migration files
│
└── .claude/
    ├── orchestration-log.jsonl               # LLM token tracking (read by Steer agents)
    └── implementation-queue.json             # Wave execution state (Claude Code orchestrator)
```

---

## 3. File naming conventions

### PRD artefacts (`outputs/docs/1-prd/`)

| Artefact type | Pattern | Example |
|---|---|---|
| Any scoping / specification deliverable | `{id}-{slug}.md` | `vis-001-product-vision.md` |
| Epic folder | `ep-{NNN}-{slug}/` | `ep-003-order-management/` |
| Epic file | `ep-{NNN}-{slug}.md` | `ep-003-order-management.md` |
| Feature folder | `ft-{NNN}-{slug}/` | `ft-012-place-order/` |
| Feature file | `ft-{NNN}-{slug}.md` | `ft-012-place-order.md` |
| User story | `us-{NNN}-{slug}.md` | `us-042-place-order-as-customer.md` |
| User journey | `uf-{NNN}-{slug}.md` | `uf-007-order-checkout-journey.md` |
| Screen spec | `scr-{NNN}-{slug}.md` | `scr-015-checkout-screen.md` |
| Test scenario | `sce-{NNN}-{slug}.md` | `sce-031-place-order-nominal.md` |
| Test seeds (feature) | `seeds-{NNN}-{slug}.md` | `seeds-012-place-order.md` |
| Business rules (epic) | `brl-ep-{NNN}.md` | `brl-ep-003.md` |
| Business rules (feature) | `brl-ft-{NNN}.md` | `brl-ft-012.md` |
| Batch spec | `bat-{NNN}-{slug}.md` | `bat-002-invoice-generation.md` |
| Notification spec | `ntf-{NNN}-{slug}.md` | `ntf-005-order-confirmation.md` |
| Change impact report | `impact-{NNN}-{slug}.md` | `impact-001-add-payment-options.md` |
| Validation report | `val-{id}-{YYYYMMDD}.md` | `val-vis-001-20260310.md` |

### Technical artefacts (`outputs/docs/2-tech/`)

| Artefact type | Pattern | Example |
|---|---|---|
| System context | `ctx-{NNN}-{slug}.md` | `ctx-001-system-context.md` |
| ADR | `adr-{NNN}-{slug}.md` | `adr-003-authentication-strategy.md` |
| Stack conventions | `stk-{NNN}-{slug}.md` | `stk-001-stack-conventions.md` |
| Security architecture | `sec-{NNN}-{slug}.md` | `sec-001-security-architecture.md` |
| Data model | `dat-{NNN}-{slug}.md` | `dat-001-data-model.md` |
| API contract | `api-{NNN}-{slug}.md` | `api-005-orders-contract.md` |
| Enabler | `enb-{NNN}-{slug}.md` | `enb-002-oauth2-setup.md` |
| Test strategy | `tst-{NNN}-{slug}.md` | `tst-001-test-strategy.md` |
| Implementation plan | `imp-{NNN}-{slug}.md` | `imp-001-implementation-plan.md` |
| Observability | `obs-{NNN}-{slug}.md` | `obs-001-observability-strategy.md` |
| Drift report | `drift-report-{YYYY-MM-DD}.md` | `drift-report-2026-03-11.md` |
| Code review | `code-review-{PR-ID}-{YYYY-MM-DD}.md` | `code-review-pr-47-2026-03-11.md` |
| Debt backlog | `debt-{NNN}-{slug}.md` | `debt-001-backlog.md` |

### Steering artefacts (`outputs/docs/3-steer/`)

| Artefact type | Pattern | Example |
|---|---|---|
| Sprint report | `sta-{NNN}-sprint-{nn}.md` | `sta-003-sprint-03.md` |
| Steering committee | `cop-{NNN}-{YYYY-MM-DD}.md` | `cop-002-2026-04-15.md` |
| All other steering | `{prefix}-{NNN}-{slug}.md` | `rsk-001-risk-register.md` |

---

## 4. `outputs/docs/1-prd/README.md` — static PRD index

This file is **created once and never updated by agents**. It is auto-rendered by GitLab when navigating to `outputs/docs/1-prd/`. It describes the expected PRD structure without listing individual epics, features or user stories.

```markdown
# PRD — Product Requirements Document

This PRD is composed of specialised, traceable artefacts — not a single monolithic document.
For a consolidated export: run `/confluence-push` (Confluence) or `/to-word` (Word).

## Structure

outputs/docs/1-prd/
├── 0-audit/          # (brownfield) As-is system audit and gap analysis
├── scoping/          # Product vision, glossary, actors, functional requirements
├── specification/    # Domain model, cross-cutting business rules
├── epics/            # Business hierarchy: epics → features → user stories,
│                     #   user journeys, screen specs, test scenarios, test data
├── tests/            # Campaign-level test artefacts (shared seeds, E2E plan)
└── tools/            # On-demand outputs: change impact, validation, GDPR/PIA,
                      #   UAT report, user docs, sprint planning, Jira/Xray mappings
```

---

## 5. Multi-domain variant (DDD)

For projects with **more than ~10 epics** or **more than 2 bounded contexts**, add a `{domain}/` level inside `epics/` to group epics by bounded context:

```
outputs/docs/1-prd/3-epics/
└── {domain}/
    └── ep-xxx-{slug}/
        ├── ep-xxx-{slug}.md
        └── ft-xxx-{slug}/
            └── ...
```

The same domain level applies to `src/`:
```
src/
└── {domain}/
    ├── domain/
    ├── application/
    ├── infrastructure/
    └── presentation/
```

**This variant is activated explicitly during Phase 0 of agent T-1.3** when the project scope is analysed. Once activated, it applies consistently across `outputs/docs/1-prd/3-epics/` and `src/`.

---

## 6. `.gitignore` recommendations

```gitignore
# Generated test results (raw data) — keep Markdown reports
tests/results/performance/*.json
tests/results/performance/*.html
tests/results/campaigns/*.xml

# LLM orchestration log — tracked intentionally, not ignored
# .claude/orchestration-log.jsonl  ← do NOT ignore

# Local environment
.env
.env.local
node_modules/
```

---

## 7. PRD is not a single file

> The PRD is the logical sum of `outputs/docs/1-prd/1-scoping/` + `outputs/docs/1-prd/2-specification/` + `outputs/docs/1-prd/3-epics/`.
>
> There is no standalone `prd.md` file to maintain. A compiled PRD export (for stakeholder communication or governance gates) is produced on demand by:
> - `/confluence-push` → Confluence pages (automatic via post-hook, or manual)
> - `/to-word` → `.docx` file

---

## 8. Scope boundaries by system

| System | Writes to | Reads from |
|---|---|---|
| BA Agents | `outputs/docs/1-prd/` | — |
| Tech Agents | `outputs/docs/2-tech/`, `api/`, `migrations/`, `CLAUDE.md`, `.claude/` | `outputs/docs/1-prd/` |
| Test Agents | `tests/e2e/`, `tests/nfr/`, `tests/results/` | `outputs/docs/1-prd/4-tests/`, `outputs/docs/1-prd/3-epics/**/tests/` |
| Steer Agents | `outputs/docs/3-steer/` | `outputs/docs/1-prd/`, `outputs/docs/2-tech/`, `.claude/orchestration-log.jsonl` |
| Claude Code | `src/`, `tests/unit/`, `tests/integration/`, `migrations/`, `api/openapi.yaml` | `CLAUDE.md`, `outputs/docs/2-tech/`, `outputs/docs/1-prd/` |
