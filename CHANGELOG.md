# Changelog

All notable changes to the **SSG AI SDLC Foundation** will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/) and follows
[Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

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
