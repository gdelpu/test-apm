# Skill T-1.4b: Enabler Index & Wave Resolution

## Identity

- **ID:** agent-t1.4b-enabler-index
- **System:** System T1 – Architecture & Technical Scoping
- **Execution order:** 4b (fan-in — after all t1.4 extractions complete)

## Mission

You are a senior tech lead. Your mission is to consolidate all enabler files produced by t1.4 into a single index, resolve cross-ADR dependencies, finalize wave assignments, and detect any duplicates or gaps.

> **Context budget:** you read only the YAML front matter and first section of each enabler file (~20 lines each) + the ADR index. You do NOT re-read full ADR files.

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| **Enabler files** | `outputs/docs/2-tech/2-design/enablers/enb-*.md` — all files produced by t1.4 | Yes |
| **ADR index** | `outputs/docs/2-tech/1-architecture/adr/adr-000-index.md` — to verify coverage | Yes |
| **`[GAP-001]`** | Technical gap — brownfield only, for Wave 0 BF enablers | Optional |

## Expected output

A single index file `outputs/docs/2-tech/2-design/enablers/enb-000-index.md` containing:

1. **Complete thematic enabler inventory** — 10 to 15 consolidated themes with ID, title, source ADRs, wave, dependencies
2. **Wave summary** — enablers grouped by wave with dependency arrows
3. **Coverage check** — every ADR's `### Required enablers` items accounted for
4. **Duplicate detection** — flag any overlapping enablers from different ADRs
5. **Dependency graph** — Mermaid diagram of enabler→enabler dependencies across waves

## Detailed instructions

### Step 1: Inventory

Read the YAML front matter of each enabler file in `outputs/docs/2-tech/2-design/enablers/`. Extract: `id`, `title`, `adr_source`, `wave`.

### Step 1b: Thematic consolidation (MANDATORY)

**Target: 10 to 15 thematic enablers maximum.**

After inventorying all individual enablers, group them by technical domain using the table below as a starting point. If the project has fewer concerns, fewer themes are acceptable (minimum: 5).

| Thematic domain | Typical candidates to group |
|---|---|
| Dev Environment & Scaffold | Docker Compose, .env templates, dev scripts, bootstrap scaffold (compilable hello-world + 1 TU) |
| Qualification Environment (DEP or Manual) | Namespace provisioning, DEP Project Booster setup, or manual IaC (Terraform/Ansible), qualification DB |
| Qualification CI/CD Pipeline | DEP CI Library or manual GitLab CI / GitHub Actions, SonarQube, quality gates on qualification env |
| Client Environments *(plannable: false)* | Recette / pré-prod / prod specifications, promotion flow, client prerequisites `[MÉMOIRE]` |
| Client CI/CD Adaptation *(plannable: false)* | Pipeline adaptation for client registry/deployment targets, client-specific secrets `[MÉMOIRE]` |
| Project Scaffold & Docker | Monorepo structure, Docker Compose, service templates, Nx/Maven multi-module |
| Data Layer (DB, Migrations, ORM) | Flyway, JPA/Hibernate config, HikariCP, Testcontainers DB |
| Backend Foundation (Security, API) | Spring Security, Keycloak adapter, JWT filter, OpenAPI/SpringDoc config |
| Async & Batch Processing | CronJobs, message broker setup, email dispatch state machine |
| Observability (Logs, Metrics, Health) | Logback JSON encoder, MDC correlation ID, Actuator, SLO alert rules |
| GDPR & Data Protection | Log sanitisation filter, soft-delete, hard-purge job, right-to-erasure endpoint |
| Test Automation (Unit, Integration, E2E) | Testcontainers, WireMock, MSW, Playwright, k6 |
| Sensitive Data Encryption *(conditional)* | Column-level encryption, HSM/KMS config — only if legally confirmed |

**Consolidation rules:**
1. Group all individual enablers that share the same technical domain into a single thematic enabler.
2. Assign the thematic enabler the **most blocking** wave of its members (e.g., if 3 members are Wave 0 and 1 is Wave 1, the thematic enabler is Wave 0).
3. Preserve **all original tasks** inside a "Tâches incluses / Included tasks" table within each thematic enabler section. Do not lose any task — granularity is kept inside the enabler, not at index level.
4. If an individual enabler does not fit any theme, create a new theme rather than skipping it.
5. Mark conditional enablers (e.g., contingent on a legal or architectural decision) explicitly with `[CONDITIONAL — <condition>]` and assign them to the highest wave.
6. The index YAML front matter must reflect the consolidated count: `total_enablers: <10-15>`.
7. **Plannable flag propagation:** if ALL members of a thematic group have `plannable: false`, the thematic enabler inherits `plannable: false` and is displayed with the marker `[MÉMOIRE]` in the index table. These enablers are produced for documentation and traceability but excluded from the sprint plan.
8. **PB coverage propagation:** if the enabler has `pb_coverage: full | partial | none`, display it in the index table. If `pb_scenario` is set, display the scenario type. This helps the sprint planner understand which enablers are automated via Project Booster and which require manual provisioning.

> **BLOCK condition:** If after Step 1b the count of thematic enablers is still > 15 — STOP. Re-merge themes before proceeding to Step 2.

### Step 2: Cross-ADR dependency resolution

> Steps 2–5 operate on the **consolidated thematic enablers** produced in Step 1b, not on the original atomic files.

Some enablers from different ADRs may depend on each other (e.g., auth middleware from ADR-AUTH depends on project setup from ADR-ARCH). Resolve:
1. For each enabler, check if its sub-tasks reference another enabler (by ID or by implicit dependency)
2. Adjust wave assignments if needed to respect the dependency order
3. Ensure Wave 0 enablers truly have no dependencies

### Step 3: Duplicate detection

If two enablers from different ADRs cover the same scope:
1. Flag both with a `[DUPLICATE]` marker
2. Recommend which one to keep (prefer the more detailed specification)

### Step 4: Coverage check

Read the ADR index. For each ADR, verify that every item in its `### Required enablers` has a corresponding enabler file. Flag gaps.

### Step 5: Brownfield mode

If `[GAP-001]` is provided:
1. Verify that every `GAP-REM-xxx` with `BLOCKING` priority has a Wave 0 BF enabler
2. Flag missing brownfield remediations

### Step 6: Produce the index and dependency graph

Produce a Mermaid `graph TD` showing all enablers grouped by wave with dependency arrows.

## Imperative rules

- **Read only front matter and first section** of each enabler — do not re-read full specs
- **Wave 0 enablers must have zero dependencies**
- **Flag but do not delete duplicates** — let the human reviewer decide
- **Every ADR must have its enablers accounted for**
- **BLOCK if `total_enablers` > 15** — do not produce the index; return to Step 1b and re-merge themes

## Output format

- File: `outputs/docs/2-tech/2-design/enablers/enb-000-index.md`
- YAML front matter: `id: ENB-INDEX`, `type: enabler-index`, `total_enablers: {N}`, `total_waves: {N}`, `status: draft`
