---
name: sdlc-deliverable-validation
description: 'Audit any SDLC deliverable for quality: template conformance, completeness, placeholder removal, traceability integrity, and production confidence scoring.'
triggers: ['deliverable validation', 'quality audit', 'template conformance', 'traceability check']
---

# Skill: sdlc-deliverable-validation

## Goal

Audit any SDLC deliverable for quality: template conformance, completeness, placeholder removal, traceability integrity, and production confidence scoring.

## When to use

- After any agent produces a deliverable (invoked via post-quality-control hook)
- On-demand via `/validate` command
- As cross-deliverable consistency checks via `/coherence` command

## Procedure

### Validation audit
1. Load the deliverable file
2. Check template conformance: required sections present, YAML front matter valid
3. Check completeness: no placeholder text remaining (e.g., `TODO`, `TBD`, `{{...}}`)
4. Check minimum counts: tables have rows, lists have items
5. Check traceability: bracketed identifiers reference existing upstream deliverables
6. Run the "next-reader test": can a human understand this without the agent?
7. Add a "Production Confidence" section with score (0-100) and findings
8. Return verdict: **PASS** / **WARN** / **BLOCK**

### Coherence check
1. Load multiple related deliverables across domains
2. Verify cross-references are valid (no broken links)
3. Check for contradictions between related deliverables
4. Verify identifier uniqueness across the project
5. Check traceability chains: EXF→EP→FT→US→BR→SCE (BA), DOM→DAT, US→API (Tech)

## Output

- Validation report (inline in deliverable or separate file)
- Coherence report (separate file)

## Rules

- Never modify the deliverable content during validation — report only
- BLOCK verdict halts the pipeline; WARN logs and continues
- Coherence check must cover BA-Tech traceability (not just within-domain)

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/sk-validate.md` | Detailed validation procedure |
| `docs/sk-coherence-check.md` | Cross-deliverable consistency check procedure |
