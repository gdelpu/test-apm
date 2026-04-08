# AI SDLC Foundation — Consumer Usage Guide

> How to install, configure, and use the AI SDLC Foundation in your project.

The **AI SDLC Foundation** (`ssg-ai-backbone`) is a cross-provider collection of
agents, skills, workflows, prompts, and foundational knowledge for AI-assisted
software delivery. It provides specification-driven delivery, quality validation,
security governance, brand compliance, and full-lifecycle SDLC support — all
packaged as installable bundles that integrate directly with GitHub Copilot,
Claude Code, or a CLI runner.

This guide is for **consumers** — teams that install the foundation into their
own repositories and use the agents and prompts it provides.

---

## Which Install Mode Should I Use?

```
                    ┌──────────────────────┐
                    │  Do you need to       │
                    │  customize agents,    │
                    │  prompts, or          │
                    │  instructions?        │
                    └──────────┬───────────┘
                         │           │
                        YES          NO
                         │           │
                         ▼           ▼
                    Expandable    Standard
```

| Aspect | Standard | Expandable |
|--------|----------|------------|
| **Use case** | Just want AI capabilities in your project | Need to customize agent behaviors, add local prompts, or contribute changes back |
| **What's installed** | Self-contained runtime directory (`.github/`) + lock file | Full source tree (`.apm/`, `providers/`, `knowledge/`) plus an overlay system (`providers-local/`) |
| **Customization** | None — use the agents and prompts as-is | Full — add, override, or extend any agent, prompt, or instruction via `providers-local/` |
| **Update story** | Replace runtime dir, commit new `.github/` | Replace upstream source, preserve `providers-local/`, re-project |
| **What to commit** | `.github/` and `.apm.lock.yaml` | Source dirs (`.apm/`, `providers/`, `knowledge/`, `providers-local/`) and `.apm.lock.yaml` — **not** `.github/` (generated) |

> **Rule of thumb:** If you don't know yet, start with **Standard**. You can
> switch to Expandable later by re-running the installer with `--mode expandable`.

---

## Quick Start — Standard Mode

Standard mode gives you a ready-to-use runtime projection. Copilot discovers
agents, prompts, and instructions from the `.github/` directory — no extra
steps required.

### 1. Download or curl the installer

```bash
# Download from the GitLab Generic Package Registry
curl --fail --silent \
  --header "JOB-TOKEN: ${CI_JOB_TOKEN}" \
  -o ssg-ai-backbone-copilot.tar.gz \
  "${CI_API_V4_URL}/projects/<SOURCE_PROJECT_ID>/packages/generic/ssg-ai-backbone/<VERSION>/ssg-ai-backbone-copilot.tar.gz"

tar -xzf ssg-ai-backbone-copilot.tar.gz -C .apm-dist/
```

Or use the installer script directly if you have it locally:

### 2. Run the installer

**Bash (Linux / macOS):**
```bash
./scripts/install-apm-bundle.sh \
  -v 1.2.0 \
  --target copilot \
  --project-id "$APM_PROJECT_ID" \
  --token "$GITLAB_TOKEN"
```

**PowerShell (Windows):**
```powershell
.\scripts\install-apm-bundle.ps1 `
  -Version 1.2.0 `
  -Target copilot `
  -ProjectId $env:APM_PROJECT_ID `
  -Token $env:GITLAB_TOKEN
```

The installer downloads the versioned archive, extracts it, runs projection,
and writes `.apm.lock.yaml`.

### 3. Commit the result

```bash
git add .github/ .apm.lock.yaml
git commit -m "feat: install AI SDLC Foundation v1.2.0 (standard)"
```

### 4. Done

Copilot automatically discovers the agents and prompts in `.github/agents/`,
`.github/prompts/`, and `.github/instructions/`. You can now invoke agents
such as `@hub-orchestrator` or slash-commands like `/workflow-feature`.

---

## Quick Start — Expandable Mode

Expandable mode installs the full source tree so you can inspect, customize,
and extend the foundation.

### 1. Download or curl the installer

Same as Standard — see above.

### 2. Run the installer with `--mode expandable`

**Bash (Linux / macOS):**
```bash
./scripts/install-apm-bundle.sh \
  -v 1.2.0 \
  --mode expandable \
  --target copilot \
  --project-id "$APM_PROJECT_ID" \
  --token "$GITLAB_TOKEN"
```

**PowerShell (Windows):**
```powershell
.\scripts\install-apm-bundle.ps1 `
  -Version 1.2.0 `
  -Mode expandable `
  -Target copilot `
  -ProjectId $env:APM_PROJECT_ID `
  -Token $env:GITLAB_TOKEN
```

The installer extracts the full source tree (`.apm/`, `providers/`, `knowledge/`),
scaffolds `providers-local/` for your customizations, runs projection to
generate `.github/`, and writes `.apm.lock.yaml`.

### 3. Commit the source (not the generated runtime)

The `.gitignore` already excludes the generated `.github/agents/`,
`.github/prompts/`, and `.github/instructions/` directories. Commit everything
else:

```bash
git add .apm/ providers/ knowledge/ providers-local/ scripts/ .apm.lock.yaml apm.yml
git commit -m "feat: install AI SDLC Foundation v1.2.0 (expandable)"
```

### 4. Customize via `providers-local/`

Add your own agents, prompts, or instructions to `providers-local/github-copilot/`.
See [Working with `providers-local/`](#working-with-providers-local) below.

### 5. Re-project when needed

After editing files in `providers-local/`, regenerate the runtime:

```bash
./scripts/project-copilot.sh --provider github-copilot --clean
```

---

## Working with `providers-local/`

The `providers-local/` directory is the **overlay system** for expandable mode.
Files placed here are merged on top of upstream provider files during projection,
allowing you to add new assets or override existing ones without modifying the
upstream source.

### Directory Structure

```
providers-local/
└── github-copilot/
    ├── agents/          # Custom or overridden agent files
    ├── prompts/         # Custom or overridden prompt files
    └── instructions/    # Custom or overridden instruction files
```

The installer scaffolds this directory with placeholder `README.md` files in
each subdirectory.

### How the Overlay Works

During projection (`project-copilot.sh` / `project-copilot.ps1`):

1. **Upstream files** are copied first — from `providers/<provider>/` into the
   runtime directory (`.github/`).
2. **Local overlay files** are copied second — from `providers-local/<provider>/`
   into the same runtime directory, **overwriting** any upstream file with the
   same name.

This means:
- **New files** in `providers-local/` are added to the runtime.
- **Files with the same name** as an upstream file replace that upstream file.
- **Upstream files without a local override** pass through unchanged.

### Adding a Custom Agent

1. Create the agent file:

   ```
   providers-local/github-copilot/agents/my-custom-agent.agent.md
   ```

   Use the standard agent format (YAML frontmatter + Markdown body):

   ```markdown
   ---
   name: My Custom Agent
   description: Handles project-specific code review patterns
   tools:
     - codebase
   ---

   You are a code reviewer specialized in our project's conventions...
   ```

2. Re-run projection:

   ```bash
   ./scripts/project-copilot.sh --provider github-copilot --clean
   ```

3. The agent appears in `.github/agents/my-custom-agent.agent.md` and is
   discoverable by Copilot as `@my-custom-agent`.

### Overriding an Upstream Prompt

To change the behavior of an existing upstream prompt (e.g., `workflow-feature`):

1. Copy the upstream file as a starting point:

   ```bash
   cp providers/github-copilot/prompts/workflow-feature.prompt.md \
      providers-local/github-copilot/prompts/workflow-feature.prompt.md
   ```

2. Edit the copy in `providers-local/` to suit your needs.

3. Re-project — your version replaces the upstream version in `.github/prompts/`.

### Adding a Custom Instruction

1. Create an instruction file:

   ```
   providers-local/github-copilot/instructions/our-conventions.instructions.md
   ```

   ```markdown
   ---
   applyTo: "src/**/*.ts"
   ---

   - Use strict TypeScript with no `any` types.
   - All functions must have JSDoc comments.
   ```

2. Re-project. The instruction is now active for all matching files.

---

## Re-projection Guide

**Projection** is the process of generating the Copilot runtime directory
(`.github/`) from the provider adapter layer and any local overlays.

### When to Re-project

- After editing any file in `providers-local/`
- After pulling an upstream update (new version install)
- After modifying files in `providers/github-copilot/`
- When `.github/agents/`, `.github/prompts/`, or `.github/instructions/`
  appear empty or stale

### Commands

**Bash (Linux / macOS):**
```bash
# Standard projection (provider adapter + local overlay)
./scripts/project-copilot.sh --provider github-copilot --clean

# Full projection (includes canonical content: skills, workflows, knowledge)
./scripts/project-copilot.sh --provider github-copilot --full --clean
```

**PowerShell (Windows):**
```powershell
# Standard projection
.\.apm\scripts\powershell\project-copilot.ps1 -Provider github-copilot -Clean

# Full projection
.\.apm\scripts\powershell\project-copilot.ps1 -Provider github-copilot -Full -Clean
```

### What Each Flag Does

| Flag | Effect |
|------|--------|
| `--clean` / `-Clean` | Removes `.github/agents/`, `.github/prompts/`, `.github/instructions/` before copying — ensures deleted upstream files are cleaned up |
| `--full` / `-Full` | Also copies canonical content (`.apm/skills/`, `.apm/workflows/`, `knowledge/`) into the runtime and rewrites path references in Markdown files |
| `--provider` / `-Provider` | Selects the provider adapter from `apm.yml` (default: `github-copilot`) |

> **Standard mode consumers** should use `--full` to get a complete runtime.
> **Expandable mode consumers** typically use the default (no `--full`) since
> they already have the canonical directories in their tree.

---

## Updating to a New Version

### How Updates Work

The installer reads `.apm.lock.yaml` to detect the current installation:

- **Installed version** and mode
- **Provider** used
- **Archive checksum** for integrity

### Standard Mode Update

Replace the runtime directory and write a new lock file:

```bash
./scripts/install-apm-bundle.sh \
  -v 1.3.0 \
  --target copilot \
  --project-id "$APM_PROJECT_ID" \
  --token "$GITLAB_TOKEN"

git add .github/ .apm.lock.yaml
git commit -m "chore: update AI SDLC Foundation to v1.3.0"
```

### Expandable Mode Update

The installer preserves `providers-local/`, replaces the upstream source
directories, and re-projects:

```bash
./scripts/install-apm-bundle.sh \
  -v 1.3.0 \
  --mode expandable \
  --target copilot \
  --project-id "$APM_PROJECT_ID" \
  --token "$GITLAB_TOKEN"

git add .apm/ providers/ knowledge/ .apm.lock.yaml
git commit -m "chore: update AI SDLC Foundation to v1.3.0 (expandable)"
```

> **Important:** Review the changelog before updating. If upstream renamed or
> removed files that you overrode in `providers-local/`, your overrides may
> become orphaned. Check that your local overlay files still match upstream
> filenames after the update.

---

## `.gitignore` Recommendations

### Standard Mode — Commit Everything

```gitignore
# No special .gitignore needed for APM artifacts.
# .github/ and .apm.lock.yaml should be committed.
```

### Expandable Mode — Ignore Generated Runtime

The generated `.github/` sub-directories should not be committed because they
are projection artifacts that can be regenerated:

```gitignore
# Generated by APM projection — do not commit
.github/agents/
.github/prompts/
.github/instructions/
```

> **Note:** The upstream `.gitignore` already includes these patterns. If you
> installed in expandable mode the correct ignores are in place.

---

## CI Integration Template

Automate installation in your CI/CD pipeline so every pipeline run has the
correct AI foundation version.

### GitLab CI Example

```yaml
variables:
  APM_VERSION: "1.2.0"
  APM_TARGET: "copilot"
  APM_PROJECT_ID: "<SOURCE_PROJECT_ID>"

stages:
  - setup
  - build
  - test

install-apm:
  stage: setup
  script:
    - |
      curl --fail --silent \
        --header "JOB-TOKEN: ${CI_JOB_TOKEN}" \
        -o ssg-ai-backbone-copilot.tar.gz \
        "${CI_API_V4_URL}/projects/${APM_PROJECT_ID}/packages/generic/ssg-ai-backbone/${APM_VERSION}/ssg-ai-backbone-copilot.tar.gz"
    - tar -xzf ssg-ai-backbone-copilot.tar.gz -C .apm-dist/
    - ./scripts/install-apm-bundle.sh -v $APM_VERSION -t $APM_TARGET --project-id $APM_PROJECT_ID --token $CI_JOB_TOKEN
  artifacts:
    paths:
      - .github/
      - .apm.lock.yaml
```

### Environment Variable Reference

| Variable | Description | Source |
|----------|-------------|--------|
| `APM_VERSION` | Semantic version to install (e.g., `1.2.0`) | Pipeline variable |
| `APM_TARGET` | Bundle target: `copilot`, `claude`, or `all` | Pipeline variable |
| `APM_PROJECT_ID` | GitLab project ID of the source repo | Pipeline variable |
| `CI_JOB_TOKEN` | Auto-injected GitLab CI job token | GitLab CI |
| `GITLAB_TOKEN` | Personal/project access token (alternative to job token) | CI/CD secret |

---

## Provider-Agnostic Design

The AI SDLC Foundation supports multiple AI providers through a single
canonical layer and per-provider adapters.

### Supported Providers

| Provider | Runtime Directory | Adapter Path | Invocation |
|----------|-------------------|--------------|------------|
| `github-copilot` | `.github/` | `providers/github-copilot/` | `@agent-name` / `/prompt-name` |
| `claude-code` | N/A (context file) | `providers/claude-code/` | `CLAUDE.md` + `/commands/` |
| `cli` | N/A | `providers/cli/` | `./providers/cli/run-workflow.sh <workflow>` |

### How Provider Selection Works

- The `apm.yml` at the repository root defines all providers and their
  adapter → runtime mappings.
- The `--provider` flag on both the installer and projection scripts selects
  which adapter to use.
- Default provider is `github-copilot`.

### Switching Providers

To switch from one provider to another, re-run the installer with the desired
`--provider` flag:

```bash
# Switch to Claude Code
./scripts/install-apm-bundle.sh \
  -v 1.2.0 \
  --target claude \
  --provider claude-code \
  --project-id "$APM_PROJECT_ID" \
  --token "$GITLAB_TOKEN"
```

You can also install for multiple providers by running the installer once per
target.

---

## Troubleshooting

### "Projection script not found"

The archive may be incomplete or extracted to an unexpected directory.

- Verify the archive was fully downloaded (check file size, checksum).
- Ensure `scripts/project-copilot.sh` (Bash) or
  `.apm/scripts/powershell/project-copilot.ps1` (PowerShell) exists.
- Re-download the archive and extract again.

### "Provider not found in apm.yml"

The `--provider` value must match a key under `providers:` in `apm.yml`.

- Check spelling: `github-copilot`, `claude-code`, `cli`.
- Open `apm.yml` and verify the provider entry exists.

### "agents/ not appearing in .github/"

Projection may not have run, or ran without `--clean`.

- Run projection with `--clean` to force a fresh copy:
  ```bash
  ./scripts/project-copilot.sh --provider github-copilot --clean
  ```
- Verify that `providers/github-copilot/agents/` contains `.agent.md` files.

### After update, custom agents are missing

The `providers-local/` directory should be preserved during updates, but
verify:

- Check that `providers-local/github-copilot/agents/` still contains your
  custom files.
- Re-run projection — local overlay files are only included in the runtime
  after projection.
- If `providers-local/` was accidentally deleted, restore from version control.

### Checksum verification fails

- Re-download the archive — the file may be corrupted or truncated.
- Use `--no-verify` to skip checksum verification (not recommended for
  production).
- Compare the downloaded file's SHA-256 against the `SHA256SUMS` file
  published alongside the archive.

### Lock file conflicts

If `.apm.lock.yaml` has merge conflicts after a branch merge:

- Accept the version from the branch with the newer `version:` field.
- Re-run the installer to regenerate a clean lock file if needed.
