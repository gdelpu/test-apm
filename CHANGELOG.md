# Changelog

All notable changes to the **SSG AI SDLC Foundation** will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/) and follows
[Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

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
- Distribution documentation (`docs/distribution.md`)
- Security hardening against A2–A5 pipeline findings
