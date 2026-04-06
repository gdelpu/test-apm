# Amendment Mode — BA Base Rules

## Activation

If no `[IMPACT-xxx]` is provided as input, **skip amendment mode entirely** — proceed in creation mode.

## Constraints

You receive an existing deliverable and a list of targeted modifications (delta items from the IMPACT file). You operate as a **precise editor, not a generator**.

### Rules

1. **Apply ONLY the delta items listed** in the amendment scope — nothing else
2. **Do not reformulate, reorganize, or improve** content outside the amendment scope — even if it seems incomplete
3. **Addition**: insert at the correct location, assign the next sequential identifier
4. **Suppression**: remove the element AND clean all cross-references to it in the deliverable
5. **Quasi-code** (SQL, OpenAPI, k6, Mermaid): edit only the targeted lines within code blocks
6. **YAML front matter**: set `status: draft`, add `amended_by: IMPACT-xxx` and `amendment_date: YYYY-MM-DD`
7. **Amendment log**: append a `## Amendment log` section at the end of the deliverable:

```markdown
## Amendment log

| Date | IMPACT | Element | Type | Summary |
|------|--------|---------|------|---------|
| YYYY-MM-DD | IMPACT-xxx | US-012 CA-003 | modification | Delay updated 15min → 30min |
```

Quality control is handled by the `post/quality-control` hook and by the coherence check — do not self-check beyond these 7 rules.
