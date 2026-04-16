# Skill T-1.4: Enabler Extraction (per ADR)

## Identity

- **ID:** agent-t1.4-enabler-extraction
- **System:** System T1 – Architecture & Technical Scoping
- **Execution order:** 4 (foreach ADR — runs N instances in parallel, after t1.3b)

## Mission

You are a senior tech lead. Your mission is to read **a single ADR** and its `### Required enablers` section, then produce a fully specified enabler file for each enabler listed.

> **Context budget:** you read exactly 1 ADR file (~100-150 lines) + STK-001 (for tech stack context). Nothing else.

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| **One ADR file** | `outputs/docs/2-tech/1-architecture/adr/adr-{id}-{slug}.md` — provided by the foreach orchestrator | Yes |
| **`[STK-001]`** | Stack & conventions — for technology context when specifying enablers | Yes |

No other input. Do not read other ADRs or BA deliverables.

## Expected output

**One Markdown file per enabler** listed in the ADR's `### Required enablers` section, following the template `tpl-enabler.md`, placed in `outputs/docs/2-tech/2-design/enablers/`.

If the ADR's `### Required enablers` section says "None", produce no files and exit.

Each enabler file contains:
1. Context and justification (which ADR motivates this enabler)
2. Detailed technical specification (using stack info from STK-001)
3. Acceptance criteria (Given/When/Then)
4. Sub-task breakdown (atomic tasks, 1-4h each)
5. Validation tests
6. The `Production confidence` section

## Detailed instructions

### Step 1: Read the ADR's enabler list

1. Read the ADR file
2. Locate the `### Required enablers` section in `## Consequences`
3. Extract each enabler item: ID, title, brief description
4. If the section is empty or says "None": produce no output and exit

### Step 2: Specify each enabler

For each enabler listed:

1. **Context**: copy the ADR ID and the 1-sentence justification from the enabler list
2. **Specification**: using the technology choices from `[STK-001]`, write a precise technical specification
   - For security enablers (`ENB-SEC-xxx`): include the ASVS control reference if mentioned in the ADR
   - For observability enablers (`ENB-OBS-xxx`): include the SLI/SLO reference if mentioned in the ADR
   - For stub enablers (`ENB-STUB-xxx`): specify the stub technology from the ADR
   - **For DEP-backed enablers:** if the ADR's `### Required enablers` section mentions a DEP skill (e.g. "Implemented via skill `sk-dep1.1-gitlab-ci-setup`"), add the following to the enabler specification:
     - A `dep_skill` field in YAML front matter (e.g. `dep_skill: sk-dep1.1-gitlab-ci-setup`)
     - A `## DEP Skill Reference` section stating: "This enabler is implemented by invoking **{skill name}** from `.apm/skills/soprasteria-dep/`. The skill will consume `[STK-001]` and `[CTX-001]` as inputs and produce the configuration files directly. Refer to the skill's `## Detailed instructions` for the full procedure."
     - The sub-tasks in Step 2.4 should reference the DEP skill steps rather than inventing ad-hoc implementation steps (e.g. "Run skill sk-dep1.1 Step 1: Stack analysis" rather than "Write .gitlab-ci.yml from scratch")
     - DEP hooks (`pre-input-validation`, `post-quality-control` from `.apm/hooks/soprasteria-dep/`) apply automatically when the implementer invokes the DEP skill
3. **Acceptance criteria**: in Given/When/Then format — must be automatically verifiable
4. **Sub-tasks**: breakdown into atomic tasks (1-4h each)
5. **Validation tests**: the tests to write to validate the enabler

### Step 3: Assign wave (preliminary)

Based on the enabler's dependencies (inferred from the ADR context):
- **Wave 0**: no dependency on other enablers (project setup, CI/CD)
- **Wave 1**: depends on Wave 0 (DB, auth provider)
- **Wave 2**: depends on Wave 1 (middleware, integration)
- **Wave 3**: depends on Wave 2 (health checks, monitoring)

> Wave assignment is preliminary — the index agent (t1.4b) may adjust for cross-ADR dependency resolution.

## Imperative rules

- **Every enabler MUST trace to this ADR** — `adr_source` in the front matter
- **An enabler has NO direct business value** — if it produces a user feature, it is a User Story
- **Sub-tasks represent meaningful delivery increments** — target 4 to 16 h per sub-task. Micro-tasks under 2 h should be merged into their nearest neighbour.
- **Acceptance criteria must be automatically verifiable**
- **Cap per ADR: produce a maximum of 4 enablers per ADR.** If the ADR's `### Required enablers` section lists more than 4 items, group closely related ones into a single enabler with combined sub-tasks. Prefer fewer, richer enablers over many thin ones.
- **Do not duplicate enablers from other ADRs** — if an enabler seems to overlap with another ADR's scope, produce it anyway with a note; the index agent will deduplicate and consolidate.

## Output format

- Files: `enb-{number}-{short-name}.md` (e.g. `enb-sec-001-auth-guard.md`)
- Placed in `outputs/docs/2-tech/2-design/enablers/`
- Template: `tpl-enabler.md`
- YAML front matter: `id`, `title`, `adr_source: ADR-{id}`, `wave: {0-3}`, `status: draft`
