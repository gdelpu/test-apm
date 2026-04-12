---
name: sdlc-scaffold
mode: agent
description: 'Create docs/ directory structure for SDLC project and configure Confluence.'
---

# /sdlc-scaffold

Create the docs/ directory scaffold for the project, configure the working language, and initialise the Confluence page hierarchy.

## Steps

1. Read and follow **all steps** defined in `.apm/skills/sdlc-scaffold/docs/sk-scaffold.md`.

   This includes, in order:
   a. Collect `project_name`, `lang`, and `doc_depth` from the session context or by asking the user.
   b. Create all directories (Mode 1 — base scaffold).
   c. Create `docs/project.yml` if it does not already exist (use the flat schema with `lang`, `project_name`, `doc_depth`, `confluence_enabled`).
   d. Copy the language-appropriate `README.md` to `docs/0-inputs/` if it does not already exist.
   e. Run the **Confluence configuration check** (Steps 1–4 of the Confluence section):
      - Check `.env` for `CONFLUENCE_INSTANCE_URL`, `CONFLUENCE_USER_EMAIL`, `CONFLUENCE_API_TOKEN`, `CONFLUENCE_SPACE_KEY`.
      - If credentials are missing, ask the user to provide them or type `skip`.
      - If credentials are present, run: `node .apm/skills/sdlc-confluence-sync/tools/confluence-publish.js --scaffold`
      - Set `confluence_enabled: true` or `false` in `docs/project.yml` accordingly.
   f. Display the Confluence configuration status report.

2. If the `features` argument is provided, also run Mode 2 — feature scaffold for each listed feature path.
