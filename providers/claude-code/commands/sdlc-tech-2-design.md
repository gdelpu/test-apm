# /sdlc-tech-2-design

Execute the **Tech System T2 — Technical Design** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-data-model` through `tech-impl-plan`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for tech-t2.1 through tech-t2.5.
3. Execute:
   - Wave 1: t2.1 (Data Model).
   - Wave 2: t2.2 // t2.3 // t2.6 (API + Enablers + Observability, parallel).
   - Wave 3: t2.4 (Test Strategy).
   - Wave 4: t2.5 (Implementation Plan + coding agent briefing compilation).
4. **Write every artifact as an actual file on disk** under `outputs/docs/2-tech/`. Do not merely display content in chat — use file-writing tools to create each file.
5. Detect the coding agent provider (check `apm.yml` → `CODING_AGENT_PROVIDER` env var → project files) and run the appropriate provider bootstrap to transform `coding-agent-briefing.md` into provider-specific artifacts.
6. Suggest `/sdlc-validate`.

Prerequisites: T1 (architecture) deliverables must exist with status `validated`.

## Outputs

- `dat-001-data-model.md` — DDL-like data model with FK/indexes
- `api-contracts/` — OpenAPI-compliant per-endpoint contracts
- `tst-001-test-strategy.md` — test pyramid with coverage thresholds
- `imp-001-implementation-plan.md` — ordered wave implementation plan
- `coding-agent-briefing.md` — provider-neutral coding agent briefing
- Provider-specific artifacts (e.g. `CLAUDE.md` for Claude Code, Copilot agent files for GitHub Copilot)
