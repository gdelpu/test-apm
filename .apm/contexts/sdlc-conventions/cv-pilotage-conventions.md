# Convention: Pilotage Conventions

## Objective

Defines formatting and identifier conventions for Steer (pilotage) deliverables. Extends the base Markdown conventions.

## Identifier prefixes

| Prefix | Type | Producer |
|--------|------|---------|
| `PIL` | Project sheet | agent-p0.1 |
| `CAP` | Team capacity snapshot | agent-p0.1 |
| `KPI` | KPI and budget baseline | agent-p0.2 |
| `RDP` | Project roadmap | agent-p1.1 |
| `RSK` | Risk card | agent-p1.2, agent-p2.3 |
| `STA` | Sprint status report | agent-p2.1, agent-p2.2 |
| `DEC` | Steering decision | agent-p2.3 |
| `COP` | COPIL deck | agent-p3.1 |
| `GNG` | Release Go/No-Go | agent-p3.2 |

## Dual register rule

Every steering deliverable MUST contain:
1. A **technical section** (sprint velocity, burndown, debt, test coverage, token consumption)
2. A **sponsor section** (functional progress in business language, budget, Go/No-Go status)

## Read-only principle

Steer agents NEVER modify BA or Tech deliverables. They only read and aggregate.
