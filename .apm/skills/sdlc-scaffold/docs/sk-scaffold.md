# Tool: Project Scaffold

## Identity

- **ID:** tool-scaffold
- **Type:** Utility tool — idempotent directory creation
- **Trigger:** Called automatically by the coordinator before wave 1 of any pipeline, and after fan-out discovery (epics/features)

## Mission

Create the `docs/` directory structure required by the SDLC agentic harness. This tool is **idempotent**: it only creates directories that do not already exist. It never deletes or modifies existing files.

## Modes

### Mode 1 — Base scaffold (called before wave 1)

Creates the full deliverable tree and the client input directories.

**Directories to create:**

```bash
# Client inputs (docs/0-inputs/)
docs/0-inputs/ba/_source/
docs/0-inputs/ba/0-audit/
docs/0-inputs/ba/1-scoping/
docs/0-inputs/ba/2-spec/
docs/0-inputs/ba/3-design/
docs/0-inputs/tech/_source/
docs/0-inputs/tech/0-audit/
docs/0-inputs/tech/1-archi/
docs/0-inputs/tech/2-design/
docs/0-inputs/steer/

# BA deliverables (outputs/docs/1-prd/)
outputs/docs/1-prd/0-audit/
outputs/docs/1-prd/1-scoping/
outputs/docs/1-prd/2-specification/
outputs/docs/1-prd/3-epics/
outputs/docs/1-prd/4-tests/
outputs/docs/1-prd/5-tools/
outputs/docs/1-prd/6-workshops/

# Tech deliverables (outputs/docs/2-tech/)
outputs/docs/2-tech/0-audit/
outputs/docs/2-tech/1-architecture/adr/
outputs/docs/2-tech/2-design/api/
outputs/docs/2-tech/2-design/enablers/
outputs/docs/2-tech/3-implementation/
outputs/docs/2-tech/4-quality/
outputs/docs/2-tech/5-workshops/

# Steer deliverables (outputs/docs/3-steer/)
outputs/docs/3-steer/0-sprint-reports/
outputs/docs/3-steer/1-committees/

# Word output
output/word/
```

### Mode 2 — Feature scaffold (called after fan-out discovery)

When epics and features have been discovered (after agents `ba-2.2` / `ba-2.2b`), create per-feature directories for both client inputs and agent outputs.

**Input:** list of feature paths discovered (e.g., `outputs/docs/1-prd/3-epics/ep-001-auth/ft-001-login/`)

**For each feature path `{feature_path}`**, create directories based on the `doc_depth` setting in `docs/project.yml`:

```bash
# Client input directory (all depths)
docs/0-inputs/ba/3-design/{feature_id}/

# --- essential depth: no sub-directories (stories and BR are inline in the feature file) ---

# --- full depth: all agent output directories ---
{feature_path}/user-stories/
{feature_path}/journeys/
{feature_path}/screens/
{feature_path}/prototypes/
{feature_path}/batches/
{feature_path}/notifications/
{feature_path}/tests/
```

Where `{feature_id}` is the directory name of the feature (e.g., `ft-001-login`).

**Summary by depth:**

| Depth | Sub-directories created per feature |
|-------|-------------------------------------|
| `essential` | `user-stories/` |
| `full` | `user-stories/`, `journeys/`, `screens/`, `prototypes/`, `batches/`, `notifications/`, `tests/` |

## Execution

Run the following bash command (idempotent — `mkdir -p` does nothing if directory exists):

```bash
mkdir -p <list of directories>
```

## Project configuration file

After creating the directory structure, create `docs/project.yml` if it does not already exist.

This file is the **persistent project configuration** — it stores the working language and project name so that all agents can read them automatically across sessions, without requiring the user to re-declare the language each time.

### Collecting the values

Before writing `docs/project.yml`, collect three pieces of information:

1. **`project_name`** — if not provided in the session prompt, ask the user: *"What is the project name?"*
2. **`lang`** — determine using the following priority order:
   1. Explicit session declaration (e.g. `"Target language: English"`, `"Langue cible : français"`)
   2. `lang` field in an existing deliverable's YAML front matter (scan `outputs/docs/1-prd/`, `outputs/docs/2-tech/`)
   3. If neither available, ask the user: *"What is the working language for deliverables? (e.g. en, fr, de, es)"*
3. **`doc_depth`** — determine using the following priority order:
   1. Explicit session declaration (e.g. `"depth: essential"`)
   2. `doc_depth` field in an existing `docs/project.yml`
   3. If neither available, ask the user:
      > *"What documentation depth do you need?"*
      > - **essential** — Features + User Stories + Architecture. Good balance for most projects (~60 files)
      > - **full** — Complete SDLC documentation with journeys, screens, prototypes, test scenarios, enablers (~150+ files)

   Default to `full` if the user does not answer or skips.

### File to create

```yaml
# docs/project.yml
lang: {lang}              # ISO 639-1 code — en | fr | de | es | pt | nl | it | pl | ...
project_name: {project_name}
doc_depth: {doc_depth}    # essential | full — controls agent selection and template verbosity
confluence_enabled: true   # set to false to disable Confluence push globally
```

The `confluence_enabled` field **must always be present** — either `true` or `false`. It is read by the `post-confluence-push` hook to decide whether to push. If the user skips Confluence setup, set it to `false`. If credentials are provided and verified, set it to `true`.

This file is read by all agents as the first source of truth for language and Confluence status. Do not overwrite it if it already exists.

## README language detection

After creating `docs/0-inputs/`, if `docs/0-inputs/README.md` does not exist, copy the language-appropriate template from `orchestration/templates/0-inputs-readme/`.

Use the `lang` value resolved above (from `docs/project.yml` or from the collection step).

Template selection:

```
orchestration/templates/0-inputs-readme/README.{lang}.md
```

If no template exists for the detected language, fall back to `README.en.md`.

Currently available templates: `README.fr.md`, `README.en.md`.

## Confluence configuration check

After creating the directory structure and `docs/project.yml`, verify that Confluence publishing is properly configured. This check runs **once per scaffold** and is idempotent.

### Step 1: Check `.env`

Read the `.env` file at the project root. Verify that the following keys are **present and non-empty**:

| Key | Purpose |
|-----|---------|
| `CONFLUENCE_INSTANCE_URL` | Base URL of the Confluence instance (e.g. `https://xxx.atlassian.net/wiki`) |
| `CONFLUENCE_USER_EMAIL` | Service account email for API authentication |
| `CONFLUENCE_API_TOKEN` | Atlassian API token |
| `CONFLUENCE_SPACE_KEY` | Target Confluence space key |

**If all keys are present and non-empty:** set `confluence_enabled: true` in `docs/project.yml` (if the field is not already set).

**If `.env` is missing or any key is absent/empty:**
1. Ask the user: *"Confluence publishing requires credentials. Please provide the following (or type 'skip' to disable Confluence push):"*
   - Instance URL
   - User email
   - API token
   - Space key
2. If the user provides values, **append** them to `.env` (create the file if it does not exist). Never overwrite existing values. Then set `confluence_enabled: true` in `docs/project.yml`.
3. If the user types `skip`, set `confluence_enabled: false` in `docs/project.yml`. The post-hook will read this and skip push without further checks.

**In all cases**, `confluence_enabled` must be explicitly present in `docs/project.yml` after the Confluence check completes — never leave it absent.

### Step 2: Check `tools/confluence-config.yaml`

Verify that `tools/confluence-config.yaml` exists and contains a `confluence.instance_url` and `confluence.space_key`.

**If missing:** create it from `.env` values with sensible defaults:

```yaml
confluence:
  instance_url: "{CONFLUENCE_INSTANCE_URL}"
  publishing:
    publish_only_validated: false
    update_existing_pages: true
    add_status_banner: true
    mermaid_render_method: "image"
  scroll_documents:
    enabled: false
    version: ""
    on_version_missing: "create"
```

Note: `space_key` and `root_page_id` are **project-specific** — they are stored in `docs/confluence-pages.yaml` under the `target:` section, not in `tools/confluence-config.yaml`.

**If it already exists:** do not modify it.

### Step 3: Create Confluence page hierarchy

If Confluence is enabled (credentials present and user did not skip), create the **root project page** and **top-level section pages** in Confluence by running:

```bash
node tools/confluence-publish.js --scaffold
```

This command is **idempotent**: it looks up existing pages by ID (from `tools/confluence-pages.yaml`) before creating. Re-running scaffold never duplicates pages.

What it does:
1. Creates a **root page** named after `project_name` from `docs/project.yml`
2. Creates 3 child section pages (PRD, Tech, Steer) using the project language from `docs/project.yml`
3. Writes page IDs to `docs/confluence-pages.yaml` (page registry)
4. Writes `space_key` and `root_page_id` to the `target:` section of `docs/confluence-pages.yaml`

The sub-sections (Scoping, Specification, Architecture, etc.) are **not** created at scaffold time. They are created on demand when a deliverable is first published with `confluence-publish.js --file`.

### Step 4: Report

Display the Confluence configuration status:

```
Confluence: ENABLED
  Instance: https://xxx.atlassian.net/wiki
  Space:    SPACE_KEY
  Config:   tools/confluence-config.yaml
  Root page: <page_id> (<project_name>)
  Sections:  PRD, Tech, Steer
```

Or, if disabled:

```
Confluence: DISABLED (user skipped or credentials missing)
```

---

## Rules

- **Idempotent**: running twice produces the same result. Never error on existing directories or Confluence pages.
- **Never delete**: this tool only creates, never removes.
- **Never write files**: this tool only creates directories and configuration files (`docs/project.yml`, `tools/confluence-config.yaml`, `tools/confluence-pages.yaml`). Deliverable files are written by agents.
- **Silent on success**: only report directories that were actually created (did not exist before).
- **README language**: follow the language detection logic above to copy the correct README template.
