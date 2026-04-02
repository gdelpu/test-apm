# /sdlc-validate

Run the **deliverable validation** tool on a specific file.

$ARGUMENTS = path to the deliverable file (e.g., "docs/1-prd/1-scoping/glo-001-glossary.md")

## Steps

1. Read `.apm/contexts/sdlc-agent-registry.yaml`.
2. **Route by domain:**
   - If path starts with `docs/2-tech/` → load Tech validation from `.apm/skills/sdlc-deliverable-validation/docs/`.
   - Otherwise → load BA validation from `.apm/skills/sdlc-deliverable-validation/docs/`.
3. Load conventions from `.apm/contexts/sdlc-conventions/`.
4. Load the corresponding template (infer from deliverable type in YAML front matter).
5. Execute: structural analysis, semantic analysis, production confidence check.
6. Display verdict: PASS / WARN / BLOCK with detailed findings.
7. Write the validation report next to the deliverable.
