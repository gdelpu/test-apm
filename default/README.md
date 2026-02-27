# ai-sdlc-foundation – Multi-agent Copilot Workspace

This workspace hosts AI agent definitions, prompts, instructions, skills, hooks, and plugins.
Structure follows [awesome-copilot](https://github.com/github/awesome-copilot) conventions.

## Structure

```
.github/
  copilot-instructions.md   ← workspace-level Copilot instructions
  workflows/                ← GitHub Actions CI workflows
agents/
  *.agent.md                ← agent definition files (flat)
prompts/
  *.prompt.md               ← reusable prompt files (flat)
instructions/
  *.instructions.md         ← coding standard instruction files
skills/
  <skill-name>/
    SKILL.md                ← skill manifest with frontmatter
    docs/                   ← Markdown source documents for this skill
    tools/                  ← CSS, Pandoc templates, scripts bundled with the skill
hooks/                      ← automated workflow hook folders
plugins/                    ← installable plugin packages
```

## Agents

### Brand Styler
Generates and converts documents to Sopra Steria brand spec with AA accessibility.

- **Agent**: `agents/brand-styler.agent.md`
- **Skill**: `skills/brand-styler/` (bundled assets: CSS, LaTeX, Pandoc templates, scripts)
- **Docs**: `skills/brand-styler/docs/`
- **Tools**: `skills/brand-styler/tools/`

#### Quick start

1. Install prerequisites: Pandoc (≥ 3.x), XeLaTeX (`texlive-xetex`), Python 3.11+ with `python-docx`.

### Security Reviewer
Reviews prompts, agents, instructions, and code for prompt injection, data exfiltration, privilege escalation, and other LLM security risks. Follows OWASP Top 10 for LLMs.

- **Agent**: `agents/security-reviewer.agent.md`

2. Regenerate the DOCX reference template (already provided):
   ```bash
   python skills/brand-styler/tools/scripts/brandify-docx.py
   ```

3. Convert Markdown to DOCX and PDF:
   ```bash
   bash skills/brand-styler/tools/scripts/gen.sh
   ```

4. Or individually:
   ```bash
   pandoc skills/brand-styler/docs/sample.md -f gfm \
     -o build/sample.docx \
     --reference-doc=skills/brand-styler/tools/templates/reference.docx

   pandoc skills/brand-styler/docs/sample.md -f gfm \
     -o build/sample.pdf \
     --template skills/brand-styler/tools/pandoc/pdf.latex \
     --pdf-engine=xelatex \
     --css skills/brand-styler/tools/brandify-md.css
   ```

## Adding a new agent

1. Add `agents/<your-agent>.agent.md` (flat, following `awesome-copilot` convention).
2. Create `skills/<your-agent>/SKILL.md` with bundled `docs/` and `tools/` as needed.
3. Add prompts to `prompts/<your-prompt>.prompt.md`.
4. Add instructions to `instructions/<your-topic>.instructions.md`.
5. Add a job in `.github/workflows/` (or extend the existing one) pointing to the new paths.
