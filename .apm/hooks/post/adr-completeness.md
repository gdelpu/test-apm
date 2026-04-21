# Post-Hook: ADR Completeness Check

> **Type:** post | **Scope:** station | **Domain:** tech | **Severity:** blocker

## Objective

Executed **after** the `tech-adrs` station produces its ADR outputs. Verifies that the mandatory ADR categories are complete, the 3-environment pattern is respected, and DEP integration fields are populated when applicable.

This hook is station-specific — it should only fire on the `tech-adrs` station (use `condition: "station.id == 'tech-adrs'"` if applied via `default_hooks`; or declare it directly in the station's `post_hooks`).

---

## Check 1 — Mandatory ADR categories exist

Scan `outputs/docs/2-tech/1-architecture/adr/` for files matching `adr-*.md`. Verify:

- [ ] At least 1 ADR with `category: architecture` (ADR-ARCH-*)
- [ ] At least 1 ADR with `category: data` (ADR-DATA-*)
- [ ] At least 1 ADR with `category: auth` (ADR-AUTH-* or ADR-SEC-AUTH)
- [ ] At least 1 ADR with `category: comm` (ADR-COMM-*)
- [ ] At least 1 ADR with `category: env-dev` (ADR-ENV-DEV)
- [ ] At least 1 ADR with `category: env-qualif` (ADR-ENV-QUALIF)
- [ ] At least 1 ADR with `category: env-client` (ADR-ENV-CLIENT)
- [ ] At least 1 ADR with `category: stubs` (ADR-STUB-*)
- [ ] At least 1 ADR with `category: cicd` (ADR-CICD-*)
- [ ] At least 1 ADR with `category: deployment` (ADR-DEPLOY-*)
- [ ] At least 2 ADRs with `category: security` (ADR-SEC-*)
- [ ] At least 2 ADRs with `category: observability` (ADR-OBS-*)
- [ ] At least 1 ADR with `category: testing` (ADR-TEST-*)

**If any mandatory category is missing → STOP.**

## Check 2 — 3-environment pattern

Verify that the three environment ADRs cover distinct tiers:

| ADR | Required YAML field | Expected value |
|-----|---------------------|----------------|
| ADR-ENV-DEV | `ownership` | `team` |
| ADR-ENV-QUALIF | `ownership` | `team` |
| ADR-ENV-CLIENT | `ownership` | `client` |

- [ ] ADR-ENV-CLIENT has `ownership: client` in YAML front matter
- [ ] ADR-ENV-QUALIF has `ownership: team` in YAML front matter

**If ownership fields are missing or incorrect → STOP.**

## Check 3 — DEP integration fields (ADR-ENV-QUALIF)

Read the YAML front matter of ADR-ENV-QUALIF:

- [ ] `dep_access` field is present and set to one of: `full`, `partial`, `none`

**If `dep_access` is missing → STOP.** (This means Step 0 was skipped — the DEP question must always be asked, even if the answer is `none`.)

If `dep_access` is `full` or `partial`:
- [ ] `pb_coverage` field is present and set to one of: `full`, `partial`, `none`
- [ ] The `## Infrastructure provisioning plan` section exists and contains a table listing every infrastructure need with a "Coverable by PB?" column

**If `pb_coverage` is missing when `dep_access` ≠ `none` → STOP.** (This means Step 2d-ii was skipped.)

If `dep_access` is `none`:
- `pb_coverage` is not required (may be absent or set to `none`)
- The `## Infrastructure provisioning plan` section must still exist, but all entries should show manual provisioning methods
- No `pb-provisioning-plan.json` is expected

## Check 4 — PB provisioning plan (conditional)

If `pb_coverage` is `full` or `partial`:

- [ ] File `outputs/docs/2-tech/1-architecture/adr/pb-provisioning-plan.json` exists
- [ ] The JSON is valid and contains a non-empty `operations` array
- [ ] Each operation has `order`, `need`, and either `pb_scenario` (non-null) or `manual_action`

**If the JSON is missing or malformed → STOP.**

If `pb_coverage` is `none`: skip this check entirely.

## Check 5 — ADR index consistency

Read `adr-000-index.md`:

- [ ] `dep_access` field in index front matter matches ADR-ENV-QUALIF's `dep_access`
- [ ] Total ADR count in index matches actual file count in `adr/` directory
- [ ] Every ADR file has a corresponding entry in the index

**If inconsistent → WARN.**

## Check 6 — Project Booster reference inputs

If `dep_access` ≠ `none`:

- [ ] At least one reference to PB scenario types (from `sk-dep4.1` or the example at `.apm/skills/soprasteria-dep/refs/`) is present in ADR-ENV-QUALIF's infrastructure provisioning plan

**If no PB reference found when dep_access is full/partial → WARN.**

---

## Decision matrix

| Checks 1-4 | Check 5-6 | Decision |
|-------------|-----------|----------|
| All pass | All pass | **GO** |
| All pass | WARN | **WARN** — log gaps, continue |
| Any STOP | — | **STOP** — produce completeness report |

## STOP report format

```markdown
## ⛔ ADR Completeness Check — BLOCKED

Station: tech-adrs
Timestamp: [YYYY-MM-DD]

### Missing mandatory categories:
- [category] — no ADR found matching category pattern

### Missing DEP fields:
- ADR-ENV-QUALIF: [field] not set

### Missing artifacts:
- pb-provisioning-plan.json: [reason]

### Resolution:
Re-run the tech-adrs station. Ensure Step 0 (DEP check) and Step 2d (environment ADRs) are completed before finalising.
```
