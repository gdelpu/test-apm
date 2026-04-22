# /sdlc-scaffold

Create the **docs/ directory structure** for the project (client inputs + deliverables).

$ARGUMENTS = (optional) none for base scaffold, or "features" to scaffold per-feature directories.

## Steps

1. Read `.apm/skills/sdlc-scaffold/SKILL.md` for scaffold logic.
2. **Project configuration** (always, before creating directories):
   - Collect `project_name` and `lang`, create `docs/project.yml` if it does not exist.
   - The user can declare the language in the prompt (e.g., `/sdlc-scaffold use English`). If undeclared, ask.
3. **Mode 1 — Base scaffold** (always):
   - Create client input directories: `inputs/ba/_source/`, `inputs/tech/_source/`, etc.
   - Create deliverable directories: `outputs/docs/1-prd/`, `outputs/docs/2-tech/`, `outputs/docs/3-steer/`, `output/word/`.
   - Idempotent — safe to run multiple times.
4. **Mode 2 — Feature scaffold** (if $ARGUMENTS contains "features"):
   - Scan `outputs/docs/1-prd/3-epics/` for existing feature directories.
   - For each feature, create design subdirectories (`user-stories/`, `journeys/`, `screens/`, etc.).
5. Report created directories.
6. Remind: "Deposit client documents in `inputs/` before launching a pipeline."
