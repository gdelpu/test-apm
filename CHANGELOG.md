# Changelog

All notable changes to the **SSG AI SDLC Foundation** will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/) and follows
[Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Changed
- Agent updates: `workflow-orchestrator`
- Copilot provider agent updates: `workflow-orchestrator.agent`
- 2 Copilot prompt(s) updated

### Fixed
- Re-display progress table after each station transition


## [0.0.18] — 2026-04-12

### Changed
- Script updates: `install-apm-bundle.ps1`, `install-apm-bundle.sh`, `project-copilot.sh`

### Fixed
- Project hooks into runtime dir, add rewrite pairs, bump to 0.0.18


## [0.0.17] — 2026-04-12

### Changed
- Documentation updates: `apm-consumer-guide.md`, `quick-start.md`
- Script updates: `bootstrap-apm.ps1`, `bootstrap-apm.sh`

### Fixed
- Bundle hooks+templates in distribution, add CI smoke checks


## [0.0.16] — 2026-04-12

### Added
- `docs/consumer/hooks-setup.md`

### Changed
- Data anonymisation handling updated: 2 docs file(s)
- Script updates: `install-apm-bundle.ps1`, `install-apm-bundle.sh`


## [0.0.15] — 2026-04-12

### Changed
- Workflow state tracking standardised: 4 Claude Code command(s), 14 Copilot prompt(s), 1 Copilot agent(s), 1 docs file(s), 8 prompts file(s), 1 workflows file(s)
- Hook engine updates: `workflow-state.schema.md`
- Script updates: `generate-changelog-entry.py`


## [0.0.14] — 2026-04-12

### Changed
- SDLC workflow state tracking standardised: 4 Claude Code commands (`sdlc-ba`, `sdlc-full`, `sdlc-steer`, `sdlc-tech`) and 4 Copilot prompts (`workflow-sdlc-ba`, `workflow-sdlc-full`, `workflow-sdlc-steer`, `workflow-sdlc-tech`) now use the canonical state tracker (`python -m engine --state`) under `outputs/runs/` with fallback to Markdown table format from `workflow-state.schema.md`
- `readme.instructions.md`: removed redundant rule about updating `docs/README.md` on doc additions
- `generate-changelog-entry.py`: rewritten to use diff-based analysis for accurate changelog generation


## [0.0.13] — 2026-04-12

### Added
- **SonarQube MCP server** (`sonarqube-mcp`) in MCP registry with Docker-based install, auth configuration, and security notes
- SonarQube MCP added to all MCP profiles: `github-stack`, `gitlab-stack`, `azure-devops-stack`, `full`
- `docs/reference/workflow-tracking.md` — reference documentation for centralized workflow state tracking
- `docs/concepts.md` — high-level concepts documentation
- Workflow state schema: run directory layout (`outputs/runs/`), `latest` symlink convention, `run-manifest.json` index, auto-derived trace file

### Changed
- Hub Orchestrator dispatch protocol refactored: removed rigid Dispatch Prompt Reference table, introduced dual-path dispatch (handoff buttons OR direct execution when user confirms textually)
- Workflow state management centralized under `outputs/runs/<workflow>/<timestamp>-<name>-<tid>/` with automatic run directory resolution
- State tracker (`state_tracker.py`): added `resolve_run_dir()` and `find_latest_run()` for automatic latest-run discovery; `--state-file` no longer required for non-init operations
- State tracker CLI: improved error messages, auto-discovery of active runs, auto-derived trace file paths
- Spec Orchestrator: output path corrected from `specs/` to `outputs/specs/features/<feature>/`
- Workflow Orchestrator: state tracking redirected to canonical state tracker under `outputs/runs/<workflow>/`
- Quality Validator: `static-analysis` skill now references SonarQube MCP adapter (`sonarqube-mcp`)
- Static-analysis skill updated with SonarQube MCP reference
- Claude Code workflow commands (8 commands) updated with centralized run-directory state tracking
- Provider agents (hub-orchestrator, spec-orchestrator, workflow-orchestrator) synced with canonical changes
- MCP setup guide expanded with SonarQube configuration steps
- Changelog generation script (`generate-changelog-entry.py`) enhanced for better diff analysis
- Install scripts: consumer workspace detection improvements

## [0.0.12] — 2026-04-12

### Fixed
- Install scripts (`install-apm-bundle.ps1`, `.sh`): old runtime directory is now removed unconditionally before copying new runtime so stale files (renamed/deleted upstream) do not persist
- Lock-file detection now checks both repo root and destination so updates are found regardless of prior install mode
- `$repoRoot` variable hoisted to script top to avoid scoping issues in standard-mode runtime resolution

## [0.0.11] — 2026-04-11

### Changed
- Hub Orchestrator: added Dispatch Prompt Reference table with exact, copy-safe prompts for all 9 workflows
- Hub Orchestrator: added CRITICAL dispatch rules (never fabricate prompts, never reference `.github/workflows/`, always use `outputs/`)
- Hub Orchestrator guardrail updated to remove `docs/` as an alternative output root

### Fixed
- Removed blanket "Out of Scope" entries from 11 provider agent files that contradicted their declared tools
- Added **PI-02b** rule to `a3-prompt-injection.prompt.md` and `a3_injection.py`: flags `high` when Out of Scope entries contradict the agent's frontmatter `tools` declarations
- Updated **A5** sandbox simulation to treat agents using declared tools for their intended purpose as expected behavior
- Added **C-02** correction record documenting the overly broad Out of Scope hardening pattern

## [0.0.10] — 2026-04-11

### Added
- Python-based workflow state tracker (`state_tracker.py`) replacing the deprecated bash state manager
- Tool invocation tracker (`tool_tracker.py`) for audit-trace logging of tool and skill events
- Workflow state file schema (`workflow-state.schema.md`) standardising state entry structure
- **C-01** correction record and policy rules **P-07a/b/c** ensuring agent file-write capability

### Changed
- Expanded `allowedFilePaths` on 12 agents (hub-orchestrator, modernization-agent, workflow-orchestrator, + 6 Copilot provider agents) to include `src/**`, `tests/**`, `docs/**`, `specs/**` for consumer workspaces
- Removed restrictive "Direct source-code modification" Out of Scope language from 5 agents
- Hook engine `__main__.py` expanded with state tracker CLI integration (+205 lines)
- 8 Claude Code workflow commands updated to use new Python state tracker for init/update
- CI gate policy rules (`a1_policy.py`, `a1-policy-validation.prompt.md`) updated with P-07a/b/c

### Removed
- `LOCAL_TESTING.md` at repo root (content previously moved to `docs/contributor/local-testing.md`)

## [0.0.9] — 2026-04-11

### Added
- MCP setup guide for consumers (`docs/consumer/mcp-setup-guide.md`) with server configuration profiles
- MCP integration guide for contributors (`docs/contributor/mcp-integration-guide.md`)
- `configure-mcp` command for Claude Code and matching Copilot prompt
- MCP registry context (`mcp-registry.yaml`) cataloguing available MCP servers
- MCP configuration skill (`mcp-configuration`) and fallback skill (`mcp-fallback`)
- 10 new MCP-backed skills: `atlassian-ops`, `aws-resource-query`, `azdo-ops`, `azure-resource-query`, `context7-docs`, `figma-design-sync`, `github-ops`, `gitlab-ops`, `m365-data-query`, `mslearn-docs-lookup`
- `playwright-browser-automation` and `semgrep-analysis` skills
- PR Validator and Station Orchestrator agents for GitHub Copilot provider
- `security-hardening.md` and `mcp-integration.md` canonical instructions

### Changed
- Brand assets relocated under `.apm/knowledge/brand/soprasteria/` with icons, logos, and templates
- Governance documents and playbooks moved under `.apm/knowledge/` (constitution, governance, playbooks)
- Agent security and tool declarations tightened across 12 canonical agents
- Quick-start and consumer guides expanded with MCP configuration steps

## [0.0.8] — 2026-04-11

### Added
- Reference documentation: `docs/reference/prompts.md`, `skills.md`, `workflows.md`, `agents.md`, `hooks.md`
- Contributor documentation: `architecture.md`, `ci-pipeline.md`, `contributing.md`, `provider-setup.md`
- GitHub Copilot provider `config.yml` for model specification and defaults
- `project-copilot.sh` bash projection script (parity with `.ps1`)
- `docs/README.md` documentation hub page

### Changed
- Hub Orchestrator added `edit/editFiles` tool with `allowedFilePaths: outputs/**` (canonical + provider)
- Hub Orchestrator guardrail updated from "pure triage only" to "prefer dispatch; execute directly when handoff unavailable"
- `README.md` significantly reduced — detailed content moved to `docs/` reference pages

## [0.0.7] — 2026-04-11

### Fixed
- All document-producing agents now have `edit/editFiles` in tools and `allowedFilePaths` in frontmatter
- Added `allowedFilePaths` to 9 canonical agents missing path restrictions (analysis-agent, bmad-orchestrator, modernization-agent, modernization-orchestrator, reverse-backlog, reverse-user-story, security-reviewer, repository-analyzer, refactor-assessor, refactor-planner)
- Resolved canonical/provider tool mismatches for repository-analyzer, reverse-backlog, reverse-user-story, security-reviewer (canonical lacked `edit/editFiles`)
- Clarified analysis-agent and quality-validator "read-only" constraints to mean production systems, not file output
- Workflow-orchestrator upgraded from `tools: []` to `['codebase', 'search', 'edit/editFiles']`

### Added
- **Branding Agent** (`branding.md`): unified agent replacing `brand-styler` and `soprasteria-branding`, with consolidated brand compliance responsibilities
- **Office product skills**: `docx` (comments, tracked changes, accept/reject), `pptx` (slide editing, thumbnail generation), `xlsx` (formula recalculation via LibreOffice), `pdf` (forms, bounding boxes, field extraction), `office-common` (OOXML schema validation, pack/unpack, merge runs, redlining)
- PowerPoint thumbnail grid generator (`pptx/scripts/thumbnail.py`)
- Excel formula recalculation script (`xlsx/scripts/recalc.py`)
- Word comment injection and tracked-changes acceptance scripts (`docx/scripts/`)
- File Creation Mandate section added to all 24 document-producing provider agents
- `file-output.instructions.md`: self-diagnosis for conflicting session-level `reminderInstructions` that block file writes
- `install-apm-bundle.ps1`: automated detection of conflicting Copilot settings on consumer install

### Changed
- Branding skills restructured: `brand-app` and `brand-document` replace old `app-branding`, `document-branding`, `brand-styler`, and `soprasteria-*` variants
- "Out of Scope" wording updated from "Direct code modification or file writes" to "Direct source-code modification outside `outputs/`" (6 agents)

### Removed
- `brand-styler.md` and `soprasteria-branding.md` agents (consolidated into `branding.md`)
- `app-branding`, `brand-styler`, `document-branding`, `soprasteria-app-branding`, `soprasteria-brand-assets`, `soprasteria-brand-core`, `soprasteria-document-branding` skills (replaced by restructured `brand-*` skills)

## [0.0.6] — 2026-04-10

### Added
- `scripts/generate-changelog-entry.py` — automated changelog generation from git history
- `scripts/simulate_ci.py` — local CI simulation runner

### Changed
- `feature-implementation` workflow expanded with file-output enforcement and brownfield detection
- `spec-kit` workflow expanded with quality gate improvements
- Workflow-orchestrator agent updated with enhanced execution modes
- Hub Orchestrator and Workflow Orchestrator Copilot provider agents updated
- 5 Copilot prompts and 5 Claude Code commands updated for workflow consistency
- CI gates README significantly expanded
- `.gitlab-ci.yml` expanded with new pipeline stages


## [0.0.5] — 2026-04-10

### Added
- `file-output.instructions.md`: mandate that document-producing agents write deliverables to disk as files
- `output-metadata.instructions.md`: structured YAML frontmatter metadata required on all `outputs/` files
- Canonical instructions: `.apm/instructions/file-output.md` and `.apm/instructions/output-metadata.md`
- Output metadata JSON schema (`knowledge/governance/schemas/output-metadata.schema.json`)
- Reference documentation: `docs/output-metadata.md`
- CI gate: changelog enforcement — `release:tag-and-publish` now fails if `CHANGELOG.md` has no entry for the releasing version

### Changed
- 7 canonical agents updated to enforce file output mandates: PR Validator, SDLC BA Analyst, Steering Manager, Tech Architect, Spec Orchestrator, Station Orchestrator, Workflow Orchestrator
- 17 skills updated with consistent frontmatter and output-metadata references
- 8 Copilot provider agents synced with canonical file-output changes
- 9 Claude Code commands updated
- CI gate station prompts updated across all A0–A7 stations
- PR validation and SDLC workflows updated
- Bootstrap and install scripts enhanced (`bootstrap-apm.ps1`, `install-apm-bundle.ps1`)

### Removed
- Stale result files: `pr_auto_result.json`, `test_gap_result.json`, `yaml_lint_result.json`

## [0.0.4] — 2026-04-09

### Added
- CI gate Python scripts: `a0_intake.py`, `a1_policy.py`, `a3_injection.py`, `a6_gate.py` (~1000 lines of PR validation pipeline logic)

### Changed
- `ci-gates/scripts/run_stations.sh` refactored for new Python-based station runners
- `scripts/project-copilot.sh` syntax simplification

### Fixed
- Increment syntax for count and rewrite_count variables in `project-copilot.sh`

## [0.0.3] — 2026-04-09

### Added
- Hook engine framework: context classifier, PII scanner, injection detector, policy authorizer, risk scorer, trace emitter (`.apm/hooks/engine/`)
- Trace record JSON schema (`.apm/hooks/engine/schemas/trace-record.schema.json`)
- Canonical agents: `station-orchestrator` and `pr-validator`
- 23 new skills: `adaptive-decision`, `adr-generation`, `audit-tracing`, `brownfield-context`, `bug-reproduction`, `bug-triage`, `data-anonymisation`, `delivery-metrics`, `drift-detection`, `fix-planning`, `governance-rules`, `incident-analysis`, `intent-capture`, `iteration-scoring`, `knowledge-update`, `nfr-review`, `observability-readiness`, `parity-validation`, `risk-scoring`, `root-cause-analysis`, `soprasteria-dep`, `test-strategy`, `workflow-engine`
- Copilot instructions: `audit-tracing.instructions.md`, `data-anonymisation.instructions.md`
- Claude Code command: `audit-trace`
- CLI provider: gate-checker library, enhanced station-runner and workflow runner
- Observability-by-default and secure-by-default governance documents

### Changed
- Security constraints and resource limits added to 16 existing Copilot provider agent files
- Compliance-check and feature-implementation workflow hook integrations
- README expanded with hook framework and updated workflow documentation
- Hub catalog updated with new agent and workflow entries

## [0.0.2] — 2026-04-08

### Added
- 15 GitHub Copilot provider agents: Analysis Agent, Architecture Governance, BMAD Orchestrator, Bug Fixer, Implementer, Modernization Agent/Orchestrator, Quality Validator, SDLC BA/Coordinator/Steering/Tech/Test, Spec Orchestrator, Workflow Orchestrator
- Consumer quick-start guide (`docs/quick-start.md`)
- Concepts documentation (`docs/concepts.md`)

### Changed
- Usage documentation renamed from `ai-foundation-usage.md` to `apm-consumer-guide.md`
- Provider parity validation and projection scripts updated

## [0.0.1] — 2026-04-08

Initial release of the SSG AI SDLC Foundation.

### Added
- Canonical layer: 23 agents, 89 skills, 19 workflows, 8 hooks
- Knowledge base: constitution, governance, playbooks, brand assets
- Provider adapters: GitHub Copilot, Claude Code, CLI
- Hub Orchestrator agent with dynamic dispatch and self-maintaining catalog
- Refactoring agents and orchestrator for structured migration
- DEP platform specialized agents and templates
- Doc-depth support (essential/standard/full)
- SpecKit Constitution for development standards
- GitLab CI/CD station-gate pipeline with Copilot CLI integration
- PR validation pipeline (validate + AI stations A0–A7)
- Deterministic validators: PR-auto, YAML-workflows, test-gaps
- APM bundle distribution pipeline (`build`, `test`, `publish` stages)
- Automated release tagging on merge to main (`release:auto-tag`)
- Build and publish scripts (`scripts/apm-build.sh`, `scripts/apm-publish.sh`)
- Cross-platform consumer install scripts (bash + PowerShell)
- SHA-256 checksum generation for distribution archives
- Local testing infrastructure with Podman Compose
- Structured prompts for branding audits, refactoring, and workflows
- Distribution documentation (`docs/contributor/distribution.md`)
- Security hardening against A2–A5 pipeline findings
