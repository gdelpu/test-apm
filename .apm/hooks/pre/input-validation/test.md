# Pre-Hook: Input Validation — Test Domain Extension

> **Type:** pre | **Scope:** agent + station | **Domain:** test | **Severity:** blocker
>
> Read `base.md` first — this file adds Test-specific rules.

## Strict Dependency Enforcement

Test agents NEVER bypass entry criteria. Unlike BA/Tech/Steer agents that allow WARN mode on some inputs, Test agents operate in **strict BLOCK mode**:

- If a prerequisite is not met (drift report not clean, environment not ready, seeds not loaded), the agent MUST BLOCK.
- There is no WARN fallback for execution agents.
- Phase 0c in `base.md` is modified: any input at WARN level is escalated to STOP for Test agents.

## Test Identifier Namespaces

| System | Identifier prefixes |
|--------|---------------------|
| Campaign | `CAM-E2E-`, `CAMP-RPT-`, `QUAL-GNG-` |
| Performance | `PERF-EXEC-`, `PERF-RPT-` |
| DAST | `DAST-RPT-`, `DAST-VUL-` |
| Upstream (read-only) | `E2E-PLAN-`, `E2E-FLX-`, `E2E-TST-`, `E2E-SCRIPTS-`, `DAT-TEST-`, `NFR-TEST-` |
