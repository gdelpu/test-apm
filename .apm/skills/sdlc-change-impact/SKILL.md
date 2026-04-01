---
name: sdlc-change-impact
description: 'Analyze the impact of a change request across all SDLC deliverables and produce an ordered amendment sequence that surgically updates affected documents.'
---

# Skill: sdlc-change-impact

## Goal

Analyze the impact of a change request across all SDLC deliverables and produce an ordered amendment sequence that surgically updates affected documents while preserving untouched sections.

## When to use

- When a change request or Confluence review comment arrives
- On-demand via `/impact` command
- Activates the pre-amendment-mode hook for surgical delta application

## Procedure

### Impact analysis
1. Receive the change description (from user, Confluence comments, or Jira)
2. Trace affected deliverables using the traceability chain:
   - BA: EXF → EP → FT → US → BR → SCE
   - Tech: DOM → DAT, US → API, ADR → ENB, ACT → Auth
   - Steer: PLAN → STA, RDP → PLAN, RSK → COP
3. For each affected deliverable, classify the impact: structural change vs content update
4. Produce an ordered amendment sequence respecting dependencies
5. Write impact report with identifier `[IMPACT-xxx]`

### Amendment execution (via pre-amendment-mode hook)
1. For each deliverable in the amendment sequence:
   - Load the deliverable
   - Apply surgical delta: modify only affected sections
   - Preserve untouched sections exactly as-is
   - Update YAML front matter (status → draft, revision incremented)
2. Verify post-amendment consistency with coherence check

## Output

- Impact analysis report with `[IMPACT-xxx]` identifier
- Amended deliverables (in-place updates)

## Rules

- Impact analysis is read-only; amendments require explicit user approval
- Amendments are surgical: only modify affected sections
- Revision history must be maintained in YAML front matter
- Post-amendment coherence check is mandatory

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/sk-change-impact.md` | Impact analysis procedure |
