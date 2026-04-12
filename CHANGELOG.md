# Changelog

All notable changes to the **SSG AI SDLC Foundation** will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/) and follows
[Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

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
- Trace record JSON schema for structured audit metadata
- **C-01** correction record and policy rules **P-07a/b/c** ensuring agent file-write capability

### Changed
- Expanded `allowedFilePaths` on 12 agents to include `src/**`, `tests/**`, `docs/**`, `specs/**` for consumer workspaces
- Removed restrictive "Direct source-code modification" Out of Scope language from 5 agents
- Workflow-orchestrator upgraded from `tools: []` to `['codebase', 'search', 'edit/editFiles']`
- Claude Code workflow commands updated to use new Python state tracker for init/update

### Fixed
- `LOCAL_TESTING.md` was misplaced at repo root — removed (content moved to docs)

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

### Changed
- Enhance workflows and enforce file output requirements

### Fixed
- Update version to 0.0.6 and enhance README for CI pipeline clarity


## [0.0.5] — 2026-04-10

### Added
- `file-output.instructions.md`: mandate that document-producing agents write deliverables to disk as files
- `output-metadata.instructions.md`: structured YAML frontmatter metadata required on all `outputs/` files
- Canonical instructions: `.apm/instructions/file-output.md` and `.apm/instructions/output-metadata.md`
- Output metadata JSON schema (`knowledge/governance/schemas/output-metadata.schema.json`)
- CI gate: changelog enforcement — `release:tag-and-publish` now fails if `CHANGELOG.md` has no entry for the releasing version

### Changed
- Refactored agents and prompts to enforce file output mandates (no more chat-only deliverables)
- SDLC agents updated: BA Analyst, Steering Manager, Tech Architect, Spec Orchestrator, Station Orchestrator, Workflow Orchestrator
- Hub catalog and SDLC agent registry updated for output-metadata awareness
- Multiple skills updated with consistent frontmatter and output-metadata references

## [0.0.4] — 2026-04-09

### Fixed
- All 27 canonical agents now projected to `providers/github-copilot/agents/` (15 were missing in v0.0.2)
- Consumer install: `.github/` and `.apm.lock.yaml` now land at repo root in both standard and expandable modes (previously nested inside `.apm-dist/`)
- Consumer install: `.apm-dist/` staging directory removed after install (no longer left behind)
- Bundle now includes `.apm/scripts/` and `scripts/project-copilot.sh` (projection script was missing, causing "Projection script not found" error)
- Bootstrap default version changed from `0.0.1` to `latest`

### Added
- `project-copilot.ps1` parity check: warns when canonical agents lack provider counterparts
- `validate_copilot_assets.py`: missing agent projection is now a blocking error (was a warning)
- `provider-parity.instructions.md`: explicit agent parity rules and checklist for all three providers

## [0.0.3] — 2026-04-09

### Added
- Hook engine framework: context classifier, PII scanner, injection detector, policy authorizer, risk scorer, trace emitter (`.apm/hooks/engine/`)
- Hook configuration template (`.apm/templates/hook-config.json`)
- Trace record JSON schema (`.apm/hooks/engine/schemas/trace-record.schema.json`)
- Station Orchestrator agent (`.apm/agents/station-orchestrator.md`) for hybrid deterministic + LLM pipeline execution
- PR Validator agent (`.apm/agents/pr-validator.md`)
- 20+ new skills: audit-tracing, data-anonymisation, adaptive-decision, ADR generation, brownfield-context, bug-triage, bug-reproduction, fix-planning, incident-analysis, intent-capture, iteration-scoring, knowledge-update, NFR review, observability-readiness, parity-validation, risk-scoring, root-cause-analysis, test-strategy, workflow-engine, governance-rules, delivery-metrics, drift-detection, soprasteria-dep
- Copilot provider agents: Analysis, Architecture Governance, BMAD Orchestrator, Bug Fixer, Implementer, Modernization Agent/Orchestrator, Quality Validator, SDLC BA/Coordinator/Steering/Tech/Test, Spec Orchestrator, Workflow Orchestrator
- Copilot instructions: `audit-tracing.instructions.md`, `data-anonymisation.instructions.md`
- Copilot prompt: `audit-trace.prompt.md`
- Claude Code command: `audit-trace.md`
- CLI provider: gate-checker library, enhanced station-runner and workflow runner
- Security constraints and resource limits for agent definitions
- Observability-by-default and secure-by-default governance documents
- Workflow playbook additions
- Compliance-check and feature-implementation workflow hook integrations

### Changed
- README expanded with hook framework, new agents, and updated workflow documentation
- Hub catalog updated with new agent and workflow entries

## [0.0.2] — 2026-04-08

### Added
- Usage documentation (`docs/ai-foundation-usage.md`) with TL;DR install guide and updating instructions
- Consumer bootstrap scripts: `scripts/bootstrap-apm.ps1` and `scripts/bootstrap-apm.sh`

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
