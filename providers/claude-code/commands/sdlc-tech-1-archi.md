# /sdlc-tech-1-archi

Execute the **Tech System T1 — Architecture** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-system-context` through `tech-enablers`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for tech-t1.1 through tech-t1.4.
3. Execute:
   - Wave 1: t1.1 (System Context — C4 Level 1-2).
   - Wave 2: t1.2 (Architecture Decision Records).
   - Wave 3: t1.3 // t1.4 (Stack Extraction & Enablers, parallel).
4. Write to `docs/2-tech/`.
5. Suggest `/sdlc-validate`.

Prerequisites: BA deliverables (scoping + specification) must exist with status `validated`.

## Outputs

- `ctx-001-system-context.md` — C4 Level 1-2 system context
- `adr/` — architecture decision records
- `stk-001-stack-conventions.md` — unified stack and conventions
- `enb-000-index.md` — enabler index with wave priorities
