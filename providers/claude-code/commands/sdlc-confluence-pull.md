# /sdlc-confluence-pull

Pull **status changes and comments** from Confluence pages linked to local deliverables.

$ARGUMENTS = optional scope + options:
- A file path: `outputs/docs/1-prd/1-scoping/glo-001-glossary.md`
- A directory: `outputs/docs/1-prd/1-scoping/`
- No argument: all files with a `confluence_id`
- `--since YYYY-MM-DD`: only comments after this date
- `--out feedback.txt`: write comments to file instead of stdout

## Steps

1. Read `.apm/skills/sdlc-confluence-sync/tools/confluence-config.yaml`.
2. Execute the pull script:
   ```bash
   node .apm/skills/sdlc-confluence-sync/tools/confluence-pull.js $ARGUMENTS
   ```
3. **Status sync**: promotes local `status` if Confluence label is ahead (draft→review→validated). Never downgrades.
4. **Comment extraction**: fetches all comments as plain text, ready to feed into `/sdlc-impact`.

After extracting comments, run `/sdlc-impact` with the output to trigger change analysis.
