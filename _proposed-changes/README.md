# Proposed Changes — Manual Integration Required

These files come from the `ai-ssg-sdlc-agentic-system` repo (branch `master`, commit `00f7b94`).
Their exact counterparts in this repo could not be determined automatically because the two repositories have diverged in structure.

## Files to integrate

| Source file (original repo) | Description | Suggested action |
|-----------------------------|-------------|------------------|
| `BA-Agents/hooks/post-quality-control.md` | Post-quality hook — adds `doc_depth` awareness (essential/standard/full) with adapted checklists | Find the equivalent in `.apm/` and merge |
| `BA-Agents/hooks/post-confluence-push.md` | Post-Confluence-push hook | Find the equivalent in `.apm/` and merge |
| `BA-Agents/skills/sk-2.2-epics.md` | Epic generation skill | Find the equivalent in `.apm/skills/sdlc-ba-specification/docs/` |
| `orchestration/agents.yaml` | Agent registry — adds `min_depth` field on all agents + `template_variants` | Compare with `.apm/contexts/sdlc-agent-registry.yaml` |
| `orchestration/coordinator.md` | Orchestration guide — adds DAG filtering by `doc_depth` + mandatory Confluence push rule | Compare with `.apm/contexts/sdlc-orchestration-guide.md` |
| `orchestration/pipelines.yaml` | Pipeline definitions | Compare with `.apm/contexts/sdlc-pipelines.yaml` |

## Context

These changes implement `doc_depth` support (`essential | standard | full`), which adapts the number of
deliverables produced based on the project type (POC, standard project, full SDLC).

The `_proposed-changes/` directory can be deleted once integration is complete.
