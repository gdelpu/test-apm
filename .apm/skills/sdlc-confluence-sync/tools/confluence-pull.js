#!/usr/bin/env node
/**
 * Confluence Pull — SDLC Agentic Harness
 * Syncs status labels from Confluence into local MD front matter,
 * and extracts page comments as plain text for /impact.
 *
 * Usage:
 *   All files:      node tools/confluence-pull.js
 *   One directory:  node tools/confluence-pull.js docs/1-prd/1-scoping/
 *   One file:       node tools/confluence-pull.js docs/1-prd/1-scoping/glo-001-glossary.md
 *   Since date:     node tools/confluence-pull.js --since 2026-03-15
 *   Output to file: node tools/confluence-pull.js --out feedback.txt
 *
 * Prerequisites:
 *   - .env at project root with CONFLUENCE_USER_EMAIL, CONFLUENCE_API_TOKEN,
 *     CONFLUENCE_INSTANCE_URL
 *   - Files must have `confluence_id` in their YAML front matter (set by confluence-publish.js)
 *
 * What it does:
 *   1. Discover target files (file, directory, or all docs/) with a confluence_id
 *   2. Status sync: fetch labels from Confluence, promote local status if behind
 *      (draft→review→validated). Never downgrades.
 *   3. Comment extraction: fetch page + inline comments, convert HTML to plain text
 *   4. Output comments to stdout (or --out file) for use with /impact
 *   5. Does NOT modify deliverable content — only updates front matter status
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const url = require('url');

// ── Config ────────────────────────────────────────────────────────────────────

const ENV_PATH = path.join(__dirname, '..', '.env');

function loadEnv(filePath) {
  if (!fs.existsSync(filePath)) return;
  const lines = fs.readFileSync(filePath, 'utf8').split('\n');
  for (const line of lines) {
    const m = line.match(/^([A-Z_]+)=(.+)/);
    if (m) process.env[m[1]] = m[2].trim();
  }
}
loadEnv(ENV_PATH);

const BASE_URL  = process.env.CONFLUENCE_INSTANCE_URL;
const EMAIL     = process.env.CONFLUENCE_USER_EMAIL;
const TOKEN     = process.env.CONFLUENCE_API_TOKEN;
const AUTH      = Buffer.from(`${EMAIL}:${TOKEN}`).toString('base64');

if (!BASE_URL || !EMAIL || !TOKEN) {
  console.error('ERROR: Missing CONFLUENCE_INSTANCE_URL, CONFLUENCE_USER_EMAIL, or CONFLUENCE_API_TOKEN.');
  console.error('Set them in .env or as environment variables.');
  process.exit(1);
}

// ── Args parsing ──────────────────────────────────────────────────────────────

let targetPath = null;
let sinceDate = null;
let outputFile = null;

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--since' && args[i + 1]) {
    sinceDate = new Date(args[++i]);
  } else if (args[i] === '--out' && args[i + 1]) {
    outputFile = args[++i];
  } else if (!args[i].startsWith('--')) {
    targetPath = args[i];
  }
}

// ── HTTP helper ───────────────────────────────────────────────────────────────

function apiGet(apiPath) {
  return new Promise((resolve, reject) => {
    const parsed = new url.URL(BASE_URL + apiPath);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: 'GET',
      headers: {
        'Authorization': `Basic ${AUTH}`,
        'Accept': 'application/json',
      },
    };
    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(data) }); }
        catch (e) { resolve({ status: res.statusCode, body: data }); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

// ── Markdown helpers ──────────────────────────────────────────────────────────

function parseFrontMatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return {};
  const meta = {};
  for (const line of match[1].split('\n')) {
    const m = line.match(/^(\w+):\s*"?([^"]*)"?/);
    if (m) meta[m[1]] = m[2].trim();
  }
  return meta;
}

function writeFrontMatterField(filePath, field, value) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const fmMatch = raw.match(/^(---\r?\n)([\s\S]*?)(\r?\n---\r?\n)([\s\S]*)$/);
  if (!fmMatch) return;

  const fmLines = fmMatch[2].split('\n');
  const fieldRegex = new RegExp(`^${field}:`);
  const existingIdx = fmLines.findIndex(l => fieldRegex.test(l));
  const newLine = `${field}: ${value}`;

  if (existingIdx >= 0) {
    fmLines[existingIdx] = newLine;
  } else {
    fmLines.push(newLine);
  }

  const updated = fmMatch[1] + fmLines.join('\n') + fmMatch[3] + fmMatch[4];
  fs.writeFileSync(filePath, updated, 'utf8');
}

function discoverFiles(target) {
  if (!target) target = 'docs';
  const resolved = path.resolve(target);

  if (!fs.existsSync(resolved)) {
    console.error(`ERROR: Path not found: ${resolved}`);
    process.exit(1);
  }

  const stat = fs.statSync(resolved);
  if (stat.isFile()) return [resolved];

  const results = [];
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.name.endsWith('.md')) results.push(full);
    }
  }
  walk(resolved);
  return results;
}

// ── HTML to plain text ────────────────────────────────────────────────────────

function htmlToText(html) {
  return html
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n')
    .replace(/<\/li>/gi, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

// ── Status detection (labels + comment commands) ────────────────────────────

const STATUS_RANK = { draft: 0, review: 1, validated: 2 };

// All known aliases for "review" and "validated" across supported languages.
// Stored without accents — input is also stripped before matching.
const STATUS_ALIASES = {
  review: [
    'review', 'revision', 'revue',                         // en, fr
    'prufung', 'uberprufung',                               // de
    'revisione',                                            // it
    'revisao',                                              // pt
    'revision',                                             // es
    'przeglad',                                             // pl
    'gjennomgang',                                          // no
    'gevalideerd',                                          // nl (review has no native, they use "review")
  ],
  validated: [
    'validated', 'valide', 'validee',                       // en, fr
    'validiert',                                            // de
    'validato',                                             // it
    'validado',                                             // pt, es
    'zatwierdzony', 'zatwierdzone',                         // pl
    'validert',                                             // no
    'gevalideerd',                                          // nl
  ],
};

/**
 * Strip accents/diacritics and lowercase for fuzzy matching.
 * "révision" → "revision", "Prüfung" → "prufung", "przegląd" → "przeglad"
 */
function normalize(str) {
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
}

/**
 * Levenshtein distance — allows typo tolerance (max 2 edits).
 */
function levenshtein(a, b) {
  const m = a.length, n = b.length;
  if (Math.abs(m - n) > 2) return 3; // fast reject
  const d = Array.from({ length: m + 1 }, (_, i) => [i]);
  for (let j = 1; j <= n; j++) d[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      d[i][j] = Math.min(
        d[i - 1][j] + 1,
        d[i][j - 1] + 1,
        d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)
      );
    }
  }
  return d[m][n];
}

/**
 * Try to match a word against known aliases with typo tolerance.
 * Returns 'review', 'validated', or null.
 */
function matchStatusCommand(word) {
  const norm = normalize(word);
  if (norm.length < 3) return null;
  for (const [status, aliases] of Object.entries(STATUS_ALIASES)) {
    for (const alias of aliases) {
      // Exact match after normalization
      if (norm === alias) return status;
      // Typo tolerance: max 2 edits for words >= 5 chars, max 1 for shorter
      const maxDist = alias.length >= 5 ? 2 : 1;
      if (levenshtein(norm, alias) <= maxDist) return status;
    }
  }
  return null;
}

/**
 * Scan comment text for a /command pattern.
 * Accepts: "/review", "/révision", "/ validé", "/revison" (typo), etc.
 */
function extractStatusFromComment(text) {
  // Match lines starting with / followed by a word (tolerant of spaces after /)
  const match = text.match(/\/\s*(\S+)/);
  if (!match) return null;
  return matchStatusCommand(match[1]);
}

async function fetchStatusLabel(confluenceId) {
  const r = await apiGet(`/rest/api/content/${confluenceId}/label`);
  if (r.status !== 200) return null;
  for (const label of (r.body.results || [])) {
    if (label.name.startsWith('status-')) {
      return label.name.replace('status-', '');
    }
  }
  return null;
}

// ── Fetch comments for a page ────────────────────────────────────────────────

async function fetchComments(confluenceId) {
  const comments = [];
  let startAt = 0;
  const limit = 50;

  while (true) {
    const r = await apiGet(
      `/rest/api/content/${confluenceId}/child/comment`
      + `?expand=body.storage,version,extensions.inlineProperties`
      + `&limit=${limit}&start=${startAt}`
    );

    if (r.status !== 200) {
      console.error(`  WARN: could not fetch comments for page ${confluenceId} (HTTP ${r.status})`);
      break;
    }

    const results = r.body.results || [];
    for (const c of results) {
      const created = new Date(c.version?.when || c.history?.createdDate || '');
      if (sinceDate && created < sinceDate) continue;

      const author = c.version?.by?.displayName
        || c.history?.createdBy?.displayName
        || 'Unknown';
      const bodyHtml = c.body?.storage?.value || '';
      const bodyText = htmlToText(bodyHtml);
      const inlineCtx = c.extensions?.inlineProperties?.originalSelection || null;

      comments.push({ author, date: created.toISOString().split('T')[0], text: bodyText, inlineContext: inlineCtx });
    }

    if (results.length < limit) break;
    startAt += limit;
  }

  return comments;
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const files = discoverFiles(targetPath);

  // Filter to files with confluence_id
  const candidates = [];
  for (const f of files) {
    const content = fs.readFileSync(f, 'utf8');
    const meta = parseFrontMatter(content);
    if (meta.confluence_id) {
      candidates.push({
        path: f,
        id: meta.id || path.basename(f, '.md'),
        confluenceId: meta.confluence_id,
        localStatus: meta.status || 'draft',
      });
    }
  }

  if (candidates.length === 0) {
    console.error('No files with confluence_id found in the target scope.');
    process.exit(0);
  }

  console.error(`Pulling from ${candidates.length} page(s)...\n`);

  // ── Part 1: Status sync (labels + comment commands) ────────────────────
  let statusChanges = 0;
  for (const file of candidates) {
    // Source A: Confluence labels (legacy mechanism)
    const labelStatus = await fetchStatusLabel(file.confluenceId);

    // Source B: Comment commands (e.g. "/review", "/validé", "/revision")
    const comments = await fetchComments(file.confluenceId);
    let commentStatus = null;
    // Take the LATEST matching comment (most recent wins)
    for (const c of comments) {
      const detected = extractStatusFromComment(c.text);
      if (detected) {
        commentStatus = detected;
        console.error(`  ${file.id}: found /${c.text.match(/\/\s*(\S+)/)?.[1] || '?'} in comment by ${c.author} (${c.date}) → ${detected}`);
      }
    }

    // Resolve: take the highest-ranked status from both sources
    const bestRemote = [labelStatus, commentStatus]
      .filter(Boolean)
      .sort((a, b) => (STATUS_RANK[b] ?? 0) - (STATUS_RANK[a] ?? 0))[0];

    if (!bestRemote) continue;

    const localRank = STATUS_RANK[file.localStatus] ?? 0;
    const remoteRank = STATUS_RANK[bestRemote] ?? 0;

    // Only promote (draft→review→validated), never downgrade
    if (remoteRank > localRank) {
      writeFrontMatterField(file.path, 'status', bestRemote);
      console.error(`  ${file.id}: status ${file.localStatus} \u2192 ${bestRemote}`);
      statusChanges++;
    }
  }

  if (statusChanges > 0) {
    console.error(`\n${statusChanges} status update(s) applied.\n`);
  } else {
    console.error('No status changes.\n');
  }

  // ── Part 2: Comment extraction ───────────────────────────────────────────
  const output = [];
  let totalComments = 0;

  for (const file of candidates) {
    const comments = await fetchComments(file.confluenceId);
    if (comments.length === 0) continue;

    totalComments += comments.length;
    output.push(`--- ${file.id} (${path.relative('.', file.path)}) ---`);
    output.push('');

    for (const c of comments) {
      const ctx = c.inlineContext ? ` [on: "${c.inlineContext.substring(0, 80)}"]` : '';
      output.push(`[${c.author} — ${c.date}]${ctx}`);
      output.push(c.text);
      output.push('');
    }
  }

  if (totalComments === 0) {
    console.error('No comments found' + (sinceDate ? ` since ${sinceDate.toISOString().split('T')[0]}` : '') + '.');
    return;
  }

  const result = output.join('\n');

  if (outputFile) {
    fs.writeFileSync(outputFile, result, 'utf8');
    console.error(`${totalComments} comment(s) written to ${outputFile}`);
    console.error(`\nTo analyze impact, run:\n  /impact ${outputFile}`);
  } else {
    console.log(result);
    console.error(`\n${totalComments} comment(s) extracted. Paste the output above into /impact to analyze.`);
  }
}

main().catch(e => { console.error('\nFATAL:', e.message); process.exit(1); });
