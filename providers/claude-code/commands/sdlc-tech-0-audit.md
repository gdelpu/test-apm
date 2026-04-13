# /sdlc-tech-0-audit

Execute the **Tech System T0 — Brownfield Technical Audit** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-audit` and `tech-gap`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for tech-t0.1 and tech-t0.2.
3. Execute:
   - Wave 1: t0.1 (Technical Stack Audit — reverse-engineering AS-IS).
   - Wave 2: t0.2 (Gap Analysis — migration paths, zero-downtime strategy).
4. **Write every artifact as an actual file on disk** under `outputs/docs/2-tech/`. Do not merely display content in chat — use file-writing tools to create each file.
5. Suggest `/sdlc-validate`.

This pipeline is for brownfield projects only.

$ARGUMENTS: path to existing system technical documentation or codebase.

## Outputs

- `tech-asis-001-technical-audit.md` — current stack assessment
- `gap-001-technical-gap.md` — gap analysis with migration paths and effort estimates
