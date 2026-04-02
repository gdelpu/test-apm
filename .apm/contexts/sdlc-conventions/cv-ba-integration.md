# Convention: Integration with BA Deliverables

## Objective

This convention imposes strict traceability from Tech deliverables back to BA deliverables. It applies to ALL Tech agents.

---

## Rules

### 1. Mandatory BA deliverable consumption

Tech agents MUST consume the following BA deliverables when available:
- `[VIS-001]` Vision & Scope — system boundaries
- `[GLO-001]` Glossary — terminology for naming (tables, columns, endpoints, classes)
- `[ACT-001]` Actors & Roles — security model input
- `[DOM-001]` Domain Model — entity-to-table mapping
- `[EXF-001]` Functional Requirements — NFR source
- `[BRL-001]` Business Rules — constraint-to-code mapping
- `[EP-xxx]` / `[FT-xxx]` Epics & Features — scope
- `[US-xxx]` User Stories — endpoint-to-story mapping

### 2. Glossary consistency

Technical naming MUST reflect BA glossary terms:
- Table names derive from entity names
- API endpoint paths derive from entity/action names
- Class names derive from entity names
- No rephrasing or translation of business terms

### 3. Traceability sections

Each Tech deliverable MUST include a traceability section mapping:
- Entity [ENT-xxx] to table/schema
- Story [US-xxx] to API endpoint
- Business rule [BR-xxx] to technical constraint (validation, trigger, check)
- Actor [ACT-xxx] to security role/permission

### 4. Signaling divergences

When a technical decision diverges from a BA assumption:
- Document it in the "Attention Points" section
- Reference the BA identifier that is affected
- Propose a resolution (ADR or BA update)
