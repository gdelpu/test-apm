# Sopra Steria Copilot Development Instructions

## 🏛️ Project Constitution (PRIMARY AUTHORITY)

**CRITICAL**: The project constitution in `.specify/memory/constitution.md` is the supreme authority for all development decisions. All code, architecture, and workflow decisions MUST comply with the constitutional principles.

The Sopra Steria constitution defines four non-negotiable pillars:

1. **Code Quality Standards** — self-documenting code, single responsibility, max cyclomatic complexity of 10, linting and formatting must pass before commit
2. **Testing Standards** — test-first (Red-Green-Refactor), ≥ 80 % unit test coverage, 100 % on critical paths; all tests automated in CI/CD
3. **User Experience Consistency** — WCAG 2.1 AA accessibility, consistent design system, no color-as-sole signal
4. **Performance Requirements** — response time benchmarks, continuous monitoring, proactive optimisation

> Before proposing any solution, verify it does not violate any constitutional principle. If a trade-off is unavoidable, flag the conflict explicitly and seek approval.

---

## 🎨 Brand Styler Skill

The **Brand Styler** skill (`skills/brand-styler/`) provides all assets needed to produce Sopra Steria–compliant documents. Use it whenever creating or converting Markdown to DOCX or PDF.

### Fonts
- **Headings**: Hurme Geometric Sans 4 (fallback: Tahoma, Segoe UI, Arial, sans-serif)
- **Body**: Hurme Geometric Sans 3 where licensed; otherwise Tahoma → Segoe UI → Arial → sans-serif

### Colours (hex)
`#4D1D82` `#8B1D82` `#CF022B` `#EF7D00` `#1D1D1B` `#A8A8A7` `#EDEDED` `#FFFFFF`

### Icons
Outline style in `#4D1D82`; optional 20 %-tone colour patch smaller than the icon, placed centre or top-right.

### Accessibility
Maintain contrast ≥ 4.5:1 for normal text and ≥ 3:1 for large text; avoid colour-as-the-only signal; ensure link text is descriptive.

### Document generation
- **DOCX**: Use `skills/brand-styler/tools/templates/reference.docx` as the Pandoc reference doc; prefer Title/Heading styles, avoid direct formatting.
- **PDF/HTML**: Load `skills/brand-styler/tools/brandify-md.css`; keep compositions light with generous whitespace. Prioritise primary palette; use secondary colours sparingly.
- **Batch build**: `bash skills/brand-styler/tools/scripts/gen.sh`

---

## 🧠 Learning from Corrections

When a user corrects your behaviour during a conversation — for example, pointing out a wrong step, a misapplied convention, an incorrect tool invocation, or a factual error — you **must** capture the lesson so the same mistake is not repeated.

### How it works

1. **Detect** — recognise when the user explicitly or implicitly corrects you (e.g. "no, you should …", "that's wrong because …", "use X instead of Y").
2. **Extract** — distil the correction into a concise, actionable rule. Generalise beyond the specific instance so the lesson applies to future similar situations.
3. **Append** — add a new `## <title>` section to `instructions/corrections.instructions.md` following the format below. If the file does not yet exist, create it with the required frontmatter first.
4. **Confirm** — briefly tell the user you have captured the correction and show the rule you added.
5. **De-duplicate** — before appending, read the existing file and skip the update if an equivalent rule already exists.

### Rule format

Each entry is a level-2 heading with a short descriptive title, followed by a one-to-three sentence actionable instruction. Include a code or command example when relevant.

```markdown
## Use runCommands instead of terminal in agent tool lists

When defining agent `.agent.md` files, the correct tool name for terminal
access is `runCommands` (or `terminalCommand`), not `terminal`.
```

### What NOT to capture

- Personal preferences that contradict the project constitution.
- Speculative suggestions the user is merely exploring.
- One-off context that has no future reuse value.

---