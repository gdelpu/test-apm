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

1. **Complete enabler inventory** — all enablers with ID, title, source ADR, wave, dependencies
2. **Wave summary** — enablers grouped by wave with dependency arrows
3. **Coverage check** — every ADR's `### Required enablers` items accounted for
4. **Duplicate detection** — flag any overlapping enablers from different ADRs
5. **Dependency graph** — Mermaid diagram of enabler→enabler dependencies across waves

## Detailed instructions

### Step 1: Inventory

Read the YAML front matter of each enabler file in `outputs/docs/2-tech/2-design/enablers/`. Extract: `id`, `title`, `adr_source`, `wave`.

### Step 2: Cross-ADR dependency resolution

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

## Output format

- File: `outputs/docs/2-tech/2-design/enablers/enb-000-index.md`
- YAML front matter: `id: ENB-INDEX`, `type: enabler-index`, `total_enablers: {N}`, `total_waves: {N}`, `status: draft`
