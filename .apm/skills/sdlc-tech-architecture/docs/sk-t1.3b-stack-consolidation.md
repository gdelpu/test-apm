# Skill T-1.3b: Stack Consolidation

## Identity

- **ID:** agent-t1.3b-stack-consolidation
- **System:** System T1 – Architecture & Technical Scoping
- **Execution order:** 3b (fan-in — after all t1.3 extractions complete)

## Mission

You are a senior lead developer. Your mission is to consolidate all per-ADR stack extractions into a single, coherent stack & conventions document `[STK-001]`. You also map business terminology to technical naming using the glossary.

> **Context budget:** you read N small extraction files (~50 lines each) + GLO-001 + skill registry index + repository structure. You do NOT re-read the ADR files.

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| **Stack extractions** | `docs/2-tech/1-architecture/_stack-extractions/stack-from-*.md` — all files produced by t1.3 | Yes |
| **`[GLO-001]`** | Glossary — for terminology mapping | WARN if absent |
| **Skill registry index** | `skill-registry/registry-index.md` — to validate skill activation | Yes |
| **Repository structure** | `shared/skills/sk-repository-structure.md` — canonical project tree | Yes |
| **IT department constraints** (if provided) | Imposed technologies, minimum versions | Optional |

No ADR files, no BA deliverables (except GLO-001).

## Expected output

A single Markdown file following the template `tpl-stack-conventions.md`, containing:
1. The selected stack by layer (front, back, data, infra, test) — merged from all extractions
2. The list of technical skills activated from the registry
3. The standard project structure (directory tree)
4. Naming conventions by layer (back, DB, API, front, tests)
5. Code conventions (general rules, commits)
6. Terminology mapping: BA glossary -> technical naming
7. A mandatory `## Local startup` section (from the ADR-ENV extraction)
8. The `Production confidence` section

## Detailed instructions

### Step 1: Merge stack choices

1. Read all extraction files from `_stack-extractions/`
2. For each layer (backend, frontend, data, infra, test, auth, monitoring...):
   - Collect all technology choices across extractions
   - If consistent: adopt the choice
   - If conflicting: flag as "conflict — requires resolution" and propose the most coherent option
   - If "Not specified": resolve based on coherence with other choices and team skills (if known)

### Step 2: Skill registry selection

1. Read `skill-registry/registry-index.md`
2. Collect all "Skills to activate" from the extractions
3. Validate each skill exists in the registry
4. Deduplicate and list with activation reason

### Step 3: Project structure

1. Read `shared/skills/sk-repository-structure.md` as the mandatory base
2. Adapt `src/` to the selected stack and architecture style
3. Preserve all other directories exactly as defined

### Step 4: Naming conventions

Define conventions for each layer, consistent with the activated skills.

### Step 5: Terminology mapping

1. Read `[GLO-001]`
2. For each key business term: define the technical correspondence (class name, table name, endpoint name)

### Step 6: Local startup section

1. Find the ADR-ENV extraction — it contains the full startup procedure
2. Find the ADR-STUB extraction — it contains the list of external system stubs
3. Combine into the `## Local startup` section

## Imperative rules

- **Every stack choice MUST trace to an ADR extraction** — no technology choice without architectural justification
- **Never contradict an extraction** — if it says "PostgreSQL", do not propose MongoDB
- **Respect IT department constraints** — if a technology is imposed, use it
- **The `## Local startup` section is mandatory**
- **Conventions must be applicable by an AI agent** — no ambiguity

## Output format

- File: `docs/2-tech/1-architecture/stk-001-stack-conventions.md`
- Template: `tpl-stack-conventions.md`
- Status: `draft`
