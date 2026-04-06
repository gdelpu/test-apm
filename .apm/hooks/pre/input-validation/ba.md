# Pre-Hook: Input Validation — BA Domain Extension

> **Type:** pre | **Scope:** agent + station | **Domain:** ba | **Severity:** blocker
>
> Read `base.md` first — this file adds BA-specific rules.

## BA Identifier Namespaces

| System | Identifier prefixes |
|--------|---------------------|
| Scoping | `DCO-`, `VIS-`, `GLO-`, `ACT-`, `EXF-` |
| Specification | `DOM-`, `EP-`, `BRL-` |
| Design | `US-`, `UF-`, `SCR-`, `BAT-`, `NTF-`, `SCE-`, `DAT-TEST-` |
| Brownfield audit | `ASIS-`, `DELTA-` |
| Cross-cutting | `RGPD-`, `IMPACT-`, `UAT-`, `PLAN-` |

## BA-Specific Rules

- When verifying mandatory input IDs (Phase 0a), match against the BA namespace prefixes above.
- Scoping deliverables (`VIS-`, `GLO-`, `ACT-`, `EXF-`) are required before specification agents can run.
- Domain model (`DOM-`) is required before epic decomposition.
- For brownfield projects, `ASIS-` and `DELTA-` inputs follow the adaptive mode rule (base.md, special case).
