# Pre-Hook: Input Validation — Tech Domain Extension

> **Type:** pre | **Scope:** agent + station | **Domain:** tech | **Severity:** blocker
>
> Read `base.md` first — this file adds Tech-specific rules.

## BA Deliverable Consumption

Tech agents consume validated BA deliverables as inputs. The pre-hook must additionally verify:
- BA deliverables have `status: validated` (not just present)
- Required BA deliverables are present per the agent's declared inputs
- Traceability from BA identifiers is maintained in the produced output

## Tech Identifier Namespaces

| System | Identifier prefixes |
|--------|---------------------|
| Architecture | `CTX-`, `ADR-`, `STK-`, `SEC-` |
| Design | `DAT-`, `API-`, `ENB-`, `ENB-STUB-`, `TST-`, `OBS-` |
| Implementation | `IMP-` |
| Quality | `DFT-`, `REL-`, `DEBT-` |
| Brownfield | `TECH-ASIS-`, `GAP-`, `MGR-` |
