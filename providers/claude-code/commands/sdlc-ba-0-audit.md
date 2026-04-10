# /sdlc-ba-0-audit

Execute the **BA System S0 — Brownfield Audit** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-ba.yml` — stations `ba-audit-existing` and `ba-audit-delta`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for ba-0.1 and ba-0.2.
3. Execute:
   - Wave 1: agent 0.1 (Existing System Audit) — uses brownfield conventions.
   - Wave 2: agent 0.2 (Delta Analysis) — depends on 0.1 output.
4. Write to `outputs/docs/1-prd/`.
5. Suggest `/sdlc-validate` on both deliverables.

This pipeline is for brownfield projects only. Skip to `/sdlc-ba-1-scoping` for greenfield.

$ARGUMENTS: path to existing system documents (Word, PDF, or Markdown).

## Outputs

- `asis-001-existing-audit.md` — AS-IS functional snapshot
- `delta-001-delta-analysis.md` — delta analysis (new/evolving/preserved/deprecated)
