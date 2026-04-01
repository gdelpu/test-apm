# Convention: Tech Markdown Conventions

## Objective

This convention extends the BA Markdown conventions for technical deliverables. Tech deliverables follow the same YAML front matter and heading structure, with tech-specific identifier prefixes.

See `BA-Agents/refs/conventions/cv-markdown.md` for the base conventions.

## Tech-specific rules

### Identifier prefixes
| Prefix | Type |
|--------|------|
| `CTX` | System Context |
| `ADR` | Architecture Decision Record |
| `STK` | Stack & Conventions |
| `SEC` | Security Architecture |
| `DAT` | Data Model |
| `API` | API Contract |
| `ENB` | Technical Enabler |
| `ENB-STUB` | External System Stub |
| `TST` | Test Strategy |
| `OBS` | Observability Strategy |
| `IMP` | Implementation Plan |
| `DFT` | Drift Report |
| `REL` | Release Plan |
| `DEBT` | Tech Debt |

### Quasi-code deliverables
Unlike BA deliverables (pure Markdown), Tech deliverables may include:
- SQL DDL snippets (data model)
- OpenAPI YAML fragments (API contracts)
- Configuration examples (stack conventions)
- Mermaid C4 diagrams (system context)

### ADR structure
Each ADR follows the pattern: Context > Decision > Alternatives Evaluated > Consequences.
The `status` field adds `superseded` for replaced decisions.

### Deliverable statuses
| Status | Meaning |
|--------|---------|
| `draft` | Produced by agent, not yet reviewed |
| `review` | Under architect / lead dev review |
| `validated` | Validated, ready for next phase |
| `superseded` | Replaced by newer version (ADRs only) |
