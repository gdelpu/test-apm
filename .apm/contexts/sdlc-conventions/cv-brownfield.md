# Convention: Brownfield Conventions

## Objective

This convention defines conventions specific to brownfield projects (evolution of existing applications). It is loaded by agents from System 0 and by agents from Systems 1/2/3 when a `[DELTA-001]` deliverable is present in the inputs.

---

## Brownfield identifier prefixes

### System 0 prefixes (audit and delta)

| Prefix | Usage | Example |
|--------|-------|---------|
| `ASIS-GLO-` | As-is glossary term | `[ASIS-GLO-001]` |
| `ASIS-ACT-` | As-is actor | `[ASIS-ACT-001]` |
| `ASIS-ROL-` | As-is role | `[ASIS-ROL-001]` |
| `ASIS-FT-` | As-is feature | `[ASIS-FT-001]` |
| `ASIS-BR-` | As-is business rule | `[ASIS-BR-001]` |
| `ASIS-JRN-` | As-is user journey | `[ASIS-JRN-001]` |
| `ASIS-SCR-` | As-is screen | `[ASIS-SCR-001]` |
| `ASIS-INT-` | As-is external integration | `[ASIS-INT-001]` |
| `DELTA-ENT-` | Entity in the delta (NEW or MODIFIED) | `[DELTA-ENT-001]` |
| `DELTA-FT-` | Feature in the delta | `[DELTA-FT-001]` |
| `DELTA-BR-` | Rule in the delta | `[DELTA-BR-001]` |
| `DELTA-ACT-` | Actor in the delta | `[DELTA-ACT-001]` |
| `DELTA-ROL-` | Role in the delta | `[DELTA-ROL-001]` |
| `DELTA-INT-` | Integration in the delta | `[DELTA-INT-001]` |

### System T0 prefixes (audit and technical gap)

| Prefix | Usage | Example |
|--------|-------|---------|
| `TECH-ASIS-STK-` | As-is tech stack | `[TECH-ASIS-STK-001]` |
| `TECH-ASIS-DAT-` | As-is data schema | `[TECH-ASIS-DAT-001]` |
| `TECH-ASIS-API-` | As-is API contract | `[TECH-ASIS-API-001]` |
| `TECH-ASIS-ARCH-` | As-is architecture | `[TECH-ASIS-ARCH-001]` |
| `TECH-ASIS-INT-` | As-is technical integration | `[TECH-ASIS-INT-001]` |
| `TECH-ASIS-INFRA-` | As-is infrastructure | `[TECH-ASIS-INFRA-001]` |
| `TECH-ASIS-TEST-` | Existing tests | `[TECH-ASIS-TEST-001]` |
| `GAP-DAT-` | Data schema gap | `[GAP-DAT-001]` |
| `GAP-API-` | API gap | `[GAP-API-001]` |
| `GAP-ARCH-` | Architecture gap | `[GAP-ARCH-001]` |
| `GAP-REM-` | Technical remediation | `[GAP-REM-001]` |
| `MGR-` | Migration plan step | `[MGR-001]` |

---

## Delta statuses

Every element in `[DELTA-001]` and `[GAP-001]` must have an explicit delta status:

| Status | Meaning | Behaviour in the pipeline |
|--------|---------|--------------------------|
| `NOUVEAU` | Did not exist in the as-is | Full specification in Systems 1/2/3 |
| `MODIFIE` | Exists and must evolve | Differential specification: only the delta is re-specified |
| `PRESERVE` | Exists and does not change | Inherited from `[ASIS-001]` — not re-specified |
| `DEPRECIE` | Exists and must be removed | Specification of the deprecation and its handling |

---

## Certainty level marking

Any element documented in an as-is deliverable whose value is assumed rather than confirmed must be marked:

| Marker | Usage |
|--------|-------|
| *(certain)* | Element confirmed by an explicit and reliable source |
| *(probable)* | Element deduced from indirect or partial sources |
| To validate | Assumed element — must be confirmed before using it in the delta |

---

## Brownfield-specific writing rules

### In [ASIS-xxx] and [TECH-ASIS-xxx] deliverables

1. **Capture, do not rephrase**: terms and concepts must be documented as they are used in the existing system
2. **Do not evaluate** functional or technical quality — limit yourself to factual description
3. **Indicate the source** of each element (document, interface, interview)
4. **Flag gaps** rather than filling them in by assumption

### In the [DELTA-001] deliverable

1. **Distinguish explicit from implicit**: an element not mentioned in the evolution requests is `PRESERVE` by default, not `MODIFIE`
2. **Document the "delta", not the full specification**: for a `MODIFIE` element, describe only what changes (before vs after)
3. **Always justify `DEPRECIE`**: requires explicit mention in requests or documented workshop agreement

### In System 1/2/3 deliverables in brownfield mode

1. **`PRESERVE` elements are not re-specified** — referenced by their `[ASIS-xxx]` identifier if needed
2. **`MODIFIE` elements are subject to a differential specification**: describe the target state (not history)
3. **Constraints from the existing system are valid inputs**: technical or functional limitations may be mentioned

---

## Brownfield checklist (to be executed by System 0 agents)

### For [ASIS-001] and [TECH-ASIS-001] deliverables
- [ ] All identifiers use the `ASIS-` prefix (BA) or `TECH-ASIS-` (Tech)
- [ ] Each assumed element is marked "To validate"
- [ ] The source is indicated for each element
- [ ] The Documentary Quality section is filled in with the gap areas
- [ ] Blockers for delta analysis are explicitly flagged

### For the [DELTA-001] deliverable
- [ ] All elements from `[ASIS-001]` have a delta status in the matrix
- [ ] `MODIFIE` elements have a precise description of the change (before vs after)
- [ ] Presumed `PRESERVE` statuses are flagged in Attention Points
- [ ] `DELTA-xxx` identifiers are correctly prefixed and sequential
- [ ] The impact zone map is complete

### For the [GAP-001] deliverable
- [ ] Each alteration `GAP-DAT-xxx` has an explicit migration strategy
- [ ] Breaking API changes are identified and distinguished from non-breaking changes
- [ ] `BLOCKING` remediations are separated from `OPTIONAL` ones
- [ ] Each gap traces back to a `[DELTA-xxx]` identifier
