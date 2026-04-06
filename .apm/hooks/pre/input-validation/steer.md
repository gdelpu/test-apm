# Pre-Hook: Input Validation — Steer Domain Extension

> **Type:** pre | **Scope:** agent + station | **Domain:** steer | **Severity:** blocker
>
> Read `base.md` first — this file adds Steer-specific rules.

## Read-Only on Upstream Systems

Steer agents consume BA and Tech deliverables but NEVER modify them. The pre-hook verifies presence and readability only — no status gate needed on upstream deliverables beyond confirming they exist and are parseable.

## Steer Identifier Namespaces

| System | Identifier prefixes |
|--------|---------------------|
| Initialization | `PIL-`, `CAP-`, `KPI-` |
| Planning | `RDP-`, `RSK-` |
| Tracking | `STA-`, `DEC-` |
| Committee | `COP-`, `GNG-` |
