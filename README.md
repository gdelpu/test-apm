# AI SDLC Foundation

> **AI Agent customisations for Sopra Steria**

A shared collection of AI agents, prompts, instructions, skills, hooks, and plugins maintained by Sopra Steria's Digital Solutions community. Resources are contributed from client engagements and technology factories.

---

## 🏗️ Repository Structure

```plaintext
ai-sdlc-foundation/
├── default/              # Common SDLC resources — shared across all clients & factories
│   ├── agents/           # Agent definition files (.agent.md)
│   ├── prompts/          # Reusable task prompts (.prompt.md)
│   ├── instructions/     # Coding standards & guidelines (.instructions.md)
│   ├── skills/           # Self-contained skill folders (SKILL.md + bundled assets)
│   ├── hooks/            # Automated workflow hooks (planned)
│   ├── plugins/          # Installable plugin packages (planned)
│   └── .specify/         # SpecKit constitution, templates & scripts
│
├── clients/              # Client-specific Copilot resources (one sub-folder per client)
│   └── <client>/         # Same structure as default/ — scoped to a client engagement
│
├── factories/            # Technology-factory Copilot resources
│   ├── dotnet/           # .NET factory — agents, prompts & instructions for C#/.NET
│   ├── java/             # Java factory — agents, prompts & instructions for Java/Spring
│   └── drupal/           # Drupal factory — agents, prompts & instructions for PHP/Drupal
│
└── station-workflows/    # AI-driven merge request validation pipeline
    ├── stations/         # Prompt files for each AI validation station
    ├── schemas/          # JSON schemas for agent/skill manifest validation
    ├── scripts/          # Pipeline helper scripts (extract_json, hmac, sanitize)
    └── fixtures/         # Test fixtures for security scanning
```

### How it works

| Folder | Purpose | Who contributes |
|---|---|---|
| `default/` | Cross-cutting SDLC resources: brand tooling, shared agents, common guidelines | Everyone |
| `clients/<name>/` | Resources built during a client engagement, shared back to Sopra Steria | Client teams |
| `factories/dotnet/` | .NET-specific agents, prompts & instructions | .NET factory |
| `factories/java/` | Java/Spring-specific agents, prompts & instructions | Java factory |
| `factories/drupal/` | Drupal/PHP-specific agents, prompts & instructions | Drupal factory |

---

## 🚀 What's Inside

Each folder (`default/`, per-client, per-factory) follows the same sub-structure:

- **Agents** (`.agent.md`) — Specialised AI agents for Sopra Steria workflows and technology stacks
- **Prompts** (`.prompt.md`) — Task-focused prompts for code generation, documentation, and delivery artifacts
- **Instructions** (`.instructions.md`) — Coding standards and best practices applied automatically by Copilot
- **Skills** (`SKILL.md` + assets) — Self-contained skill folders bundling instructions, scripts, and templates
- **Hooks** — Automated workflows triggered by Copilot coding agent events
- **Plugins** — Installable packages bundling related agents, prompts, and skills
- **SpecKit Constitution** (`.specify/memory/constitution.md`) — Project-wide principles for code quality, testing, UX, and performance that Copilot and agents must follow; generated and maintained with [spec-kit](https://github.com/github/spec-kit)

---

## 📦 Current Resources

### Default (Common Sopra Steria)

| Type | Name | Description |
|---|---|---|
| Agent | [Brand Styler](default/agents/brand-styler.agent.md) | Generate and convert documents to Sopra Steria brand spec with AA accessibility |
| Prompt | [Convert MD to DOCX & PDF](default/prompts/convert-md-to-docx-and-pdf.prompt.md) | Convert Markdown files to branded DOCX and PDF via Pandoc |
| Prompt | [Create One-Pager](default/prompts/create-one-pager.prompt.md) | Create a concise Sopra Steria–branded one-pager from notes |
| Skill | [Brand Styler](default/skills/brand-styler/) | Bundled CSS, LaTeX, Pandoc templates and scripts for brand-compliant document generation |
| Constitution | [Sopra Steria SpecKit Constitution](default/.specify/memory/constitution.md) | Core Sopra Steria engineering principles: code quality, testing standards, UX consistency, and performance requirements |

### Factories

| Factory | Status |
|---|---|
| `factories/dotnet/` | 🟡 Incoming — .NET factory contributions welcome |
| `factories/java/` | 🟡 Incoming — Java factory contributions welcome |
| `factories/drupal/` | 🟡 Incoming — Drupal factory contributions welcome |

### Clients

| Client | Status |
|---|---|
| `clients/` | 🟡 Incoming — add a sub-folder per client engagement |

---

## ⚙️ Prerequisites

| Tool | Version | Required For |
|------|---------|-------------|
| Python | 3.11+ | Deterministic validators, pipeline scripts |
| Git | 2.x+ | Diff generation, all validation jobs |
| Node.js | 20+ | Copilot CLI runtime (AI stations) |
| GitHub Copilot CLI | 1.0.4 | AI Agent stations (`npm install -g @github/copilot@1.0.4`) |
| jq | 1.6+ | Gate enforcement in pipeline |
| Podman + podman-compose | — | Local full pipeline execution (optional) |
| Pandoc | — | Brand Styler document conversion (optional) |

For AI station jobs, you also need a **GitHub PAT** with Copilot access set as `GH_TOKEN` / `GITHUB_TOKEN` (see [CI/CD Configuration](#cicd-configuration-gitlab)).

---

## 🔧 How to Use

### Using resources in VS Code

1. Copy or symlink the desired `agents/`, `prompts/`, `instructions/`, or `skills/` folder into your project's `.github/` directory, **or** reference them directly via the path when using Copilot Chat.

2. For workspace-level instructions, create a `.github/copilot-instructions.md` in your project referencing the desired resources.

3. For skills, reference the skill path in your agent definition or Copilot Chat session.

### Using the SpecKit constitution

[spec-kit](https://github.com/github/spec-kit) is a toolchain that generates a living **constitution** — a structured set of engineering principles and quality gates that Copilot agents follow throughout a project.

The Sopra Steria common constitution lives at `default/.specify/memory/constitution.md` and covers:
- **Code Quality Standards** — naming, documentation, complexity, SRP
- **Testing Standards** — test-first, 80 % unit coverage, CI/CD automation
- **UX Consistency** — accessibility (WCAG AA), design system, performance UX
- **Performance Requirements** — response time benchmarks, monitoring, optimisation

#### Adopting the Sopra Steria constitution in your project

1. Copy `default/.specify/` into your project root.
2. Reference the constitution in your `.github/copilot-instructions.md`:
   ```markdown
   Follow the engineering principles defined in `.specify/memory/constitution.md`.
   ```
3. Use the bundled spec-kit scripts to create feature specs and plans:
   ```powershell
   .specify/scripts/powershell/create-new-feature.ps1 -FeatureName "my-feature"
   ```

#### Sharing a constitution back to Sopra Steria

If you evolve the constitution on a client engagement or factory:
1. Copy your updated `.specify/memory/constitution.md` to `clients/<client-name>/.specify/memory/` or `factories/<name>/.specify/memory/`.
2. Open a merge request — the Sopra Steria team will review and merge improvements into `default/.specify/memory/constitution.md`.

---

### Using the Brand Styler skill

```bash
# Batch-convert all docs in skills/brand-styler/docs/ to DOCX and PDF
bash default/skills/brand-styler/tools/scripts/gen.sh
```

See [default/skills/brand-styler/SKILL.md](default/skills/brand-styler/SKILL.md) for full usage instructions.

---

## 🛡️ Validation Gating Policy

Every merge request triggers a **validation pipeline** (`.gitlab-ci.yml`) that runs six jobs concurrently in the `validate` stage. Three are deterministic Python scripts; three are **AI Agent stations** powered by GitHub Copilot CLI. Together they enforce structural, policy, and security standards before code is merged.

### Pipeline Architecture

```
merge_request_event
  └─ validate (concurrent)
       ├─ validate:pr-auto          ← Python deterministic
       ├─ validate:yaml-workflows   ← Python deterministic
       ├─ validate:test-gaps        ← Python deterministic (advisory)
       ├─ validate:ai-intake  (A0)  ← Copilot CLI AI Agent
       ├─ validate:policy     (A1)  ← Copilot CLI AI Agent  ⛔ gates
       └─ validate:security   (A2)  ← Copilot CLI AI Agent  ⛔ gates
```

### Validation Jobs

| Job | Type | Script / Prompt | Purpose | Gating |
|-----|------|----------------|---------|--------|
| `validate:pr-auto` | Deterministic | `pr_auto_validator.py` | Validates frontmatter, kebab-case naming, and internal links | **Blocking** |
| `validate:yaml-workflows` | Deterministic | `yaml_workflow_linter.py` | Validates workflow YAML structure and safety rules | **Blocking** |
| `validate:test-gaps` | Deterministic | `test_gap_detector.py` | Detects missing documentation when scripts/workflows change | **Advisory** |
| `validate:ai-intake` | AI Agent | [`A0-intake.prompt.md`](station-workflows/stations/A0-intake.prompt.md) | Classifies changed files, extracts MR context (id, priority, risks) | **Informational** |
| `validate:policy` | AI Agent | [`a1-policy-validation.prompt.md`](station-workflows/stations/a1-policy-validation.prompt.md) | Validates agent/skill manifests against JSON schemas, enforces tool allowlists and safety fields | **Blocking** — fails MR on `status: "fail"` |
| `validate:security` | AI Agent | [`a2-security-static.prompt.md`](station-workflows/stations/a2-security-static.prompt.md) | Scans MR diff for hardcoded secrets, vulnerable dependencies, and dangerous shell patterns | **Blocking** — fails MR on `status: "fail"` |

Deterministic scripts live in `default/skills/ai-backbone-pr-checks/tools/scripts/`. AI station prompts live in `station-workflows/stations/`.

### How AI Stations Work

Each AI station invokes **GitHub Copilot CLI v1.0.4** in text-only mode — no tools are available to the model (`--available-tools` with an empty allow-list), ensuring structured JSON output without agent-style tool-calling loops.

1. Copilot CLI receives the station prompt plus the MR diff/changed files as input
2. The model responds with **raw JSON only** (enforced by `--available-tools` empty allow-list + JSON-only system prompt)
3. `extract_json.py` parses the JSONL output and extracts the structured JSON object
4. For policy and security stations, `jq -r '.status'` reads the result — if `"fail"`, the pipeline exits with code 1

### Local Validation

**Deterministic validators:**

```bash
python default/skills/ai-backbone-pr-checks/tools/scripts/yaml_workflow_linter.py --root . --out reports/yaml-workflow-linter.json
python default/skills/ai-backbone-pr-checks/tools/scripts/pr_auto_validator.py --base-ref HEAD~1 --head-ref HEAD --out reports/pr-auto-validator.json
python default/skills/ai-backbone-pr-checks/tools/scripts/test_gap_detector.py --base-ref HEAD~1 --head-ref HEAD --out reports/test-gap-detector.json
```

**Full pipeline (including AI stations) via Podman:**

```bash
podman-compose up --build
```

See [LOCAL_TESTING.md](LOCAL_TESTING.md) for full setup instructions.

### CI/CD Configuration (GitLab)

The AI station jobs require a GitHub token with Copilot CLI access:

1. Go to **Settings > CI/CD > Variables** in your GitLab project
2. Create a masked variable: `GITHUB_TOKEN` with a GitHub PAT that has Copilot CLI access
3. The three AI station jobs (`ai-intake`, `policy`, `security`) use this token to authenticate with Copilot CLI

For local testing, set `GH_TOKEN` and `GITHUB_TOKEN` in your `.env` file (see [LOCAL_TESTING.md](LOCAL_TESTING.md)).

---

## 🤝 Contributing

We welcome contributions from all members, client teams, and factory leads.

### Adding resources to `default/`

1. Place agent files flat in `default/agents/<name>.agent.md`
2. Place prompt files flat in `default/prompts/<name>.prompt.md`
3. Place instruction files flat in `default/instructions/<name>.instructions.md`
4. For skills with bundled assets, create `default/skills/<name>/SKILL.md`
5. For constitution updates, edit `default/.specify/memory/constitution.md` and describe the change in your MR

### Contributing from a client engagement

1. Create `clients/<client-name>/` mirroring the `default/` structure
2. Add your agents, prompts, instructions, and skills under that folder
3. Open a merge request — the Sopra Steria team will review and promote reusable items to `default/`

### Contributing from a factory

1. Add resources under `factories/<dotnet|java|drupal>/`
2. Follow the same naming conventions as `default/`
3. Open a merge request targeting the `staged` branch

### Naming conventions

- File names: **lowercase, words separated by hyphens** (e.g. `code-review.agent.md`)
- All `.agent.md`, `.prompt.md`, and `.instructions.md` files must have valid YAML frontmatter with at least `name` and `description` fields
- All `SKILL.md` files must have `name` (matching the folder name) and `description` frontmatter fields
- Description values must be **wrapped in single quotes**

### Quick checklist before opening an MR

- [ ] Frontmatter is present and valid
- [ ] File name is lowercase with hyphens
- [ ] Paths inside files point to the correct folder (`default/`, `factories/<name>/`, or `clients/<name>/`)
- [ ] MR targets the `staged` branch, not `main`

---

## 📄 License

Resources in this repository are for internal Sopra Steria use. Consult your delivery lead for usage terms on client-contributed content.

---

*Inspired by and structured after [awesome-copilot](https://github.com/github/awesome-copilot).*
