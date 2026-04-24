# Amendment Mode — Tech Domain Extension

> Read `amendment-mode-base.md` first — this file adds Tech-specific rules.

## Tech Identifier Namespaces

When matching delta items from the `[IMPACT-xxx]` file, use both the agent ID and these prefixes:

| System | Prefixes |
|--------|----------|
| Architecture | `CTX-`, `ADR-`, `STK-`, `SEC-` |
| Design | `DAT-`, `API-`, `ENB-`, `TST-`, `OBS-` |
| Implementation | `IMP-` |
| Quality | `DFT-`, `REL-`, `DEBT-` |
| Brownfield | `TECH-ASIS-`, `GAP-`, `MGR-` |

## BA → Tech Traceability

When amending a Tech deliverable, also update BA→Tech mapping sections if the delta impacts a cross-domain link:

| BA element | Tech artifact |
|------------|---------------|
| Entity `[ENT-xxx]` | Table in `[DAT-001]` |
| Story `[US-xxx]` | Endpoint in `[API-xxx]` |
| Rule `[BR-xxx]` | Constraint in `[DAT-001]` or validation in `[API-xxx]` |
| Actor `[ACT-xxx]` | Security role in `[SEC-001]` |

If the IMPACT delta modifies one side of a cross-domain link, update the mapping in the Tech deliverable to reflect the change. If the corresponding BA deliverable needs updating, flag it in the amendment log for the coordinator to schedule.
