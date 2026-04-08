# Changelog

All notable changes to the **SSG AI SDLC Foundation** will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/) and follows
[Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- APM bundle distribution pipeline (`build:apm-bundles`, `test:apm-smoke`, `publish:apm-registry`)
- Build helper script (`scripts/apm-build.sh`)
- Publish helper script (`scripts/apm-publish.sh`)
- Cross-platform consumer install scripts (`scripts/install-apm-bundle.sh`, `scripts/install-apm-bundle.ps1`)
- Distribution documentation (`docs/distribution.md`)
- Bundle smoke-test stage in CI pipeline
- SHA-256 checksum generation for all distribution archives
- CHANGELOG.md

### Changed
- Extended `.gitlab-ci.yml` with `build`, `test`, and `publish` stages
- Updated README with Distribution & Installation section
- Updated `.gitignore` with `dist/` entry

## [1.0.0] — Initial Release

### Added
- Canonical layer: 23 agents, 89 skills, 19 workflows, 8 hooks
- Knowledge base: constitution, governance, playbooks, brand assets
- Provider adapters: GitHub Copilot, Claude Code, CLI
- PR validation pipeline (validate + AI stations)
- Cross-layer validation scripts
