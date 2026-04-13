# /sdlc-ba-1-scoping

Execute the **BA System S1 — Scoping** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-ba.yml` — stations `ba-vision` through `ba-requirements`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for ba-1.1 through ba-1.4.
3. Execute:
   - **Resolve prerequisites**: if discovery document does not exist, produce it from raw sources in `docs/0-inputs/ba/_source/`.
   - Resolve DAG into waves (1.1 // 1.2 parallel, then 1.3, then 1.4).
   - For each agent: assemble prompt (hooks + conventions + template + skill), then launch.
   - Verify output file exists before proceeding to next agent.
4. **Write every artifact as an actual file on disk** under `outputs/docs/1-prd/1-scoping/`. Do not merely display content in chat — use file-writing tools to create each file.
5. Suggest `/sdlc-validate` on each deliverable.

$ARGUMENTS: path to source documents (optional, used as context for agents 1.1 and 1.2).

## Outputs

- `vis-001-product-vision.md` — vision, objectives, scope
- `glo-001-glossary.md` — ubiquitous language glossary
- `act-001-actors-roles.md` — actors and permissions matrix
- `exf-001-functional-requirements.md` — testable requirements with traceability
