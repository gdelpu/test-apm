#!/usr/bin/env node
/**
 * Confluence Publisher — SDLC Agentic Harness
 * Publishes Markdown deliverables to Confluence using REST API v1.
 *
 * Usage:
 *   Scaffold:       node tools/confluence-publish.js --scaffold
 *   Single file:    node tools/confluence-publish.js --file <path-to-md>
 *   Directory mode: node tools/confluence-publish.js <source-dir> [parent-title] [phase-title] [phase-page-id] [root-page-id]
 *
 * Prerequisites:
 *   - .env at project root with CONFLUENCE_USER_EMAIL, CONFLUENCE_API_TOKEN,
 *     CONFLUENCE_INSTANCE_URL, CONFLUENCE_SPACE_KEY
 *   - Pandoc installed (see MEMORY.md for local path)
 *   - mmdc (mermaid-cli) for Mermaid diagram rendering
 *   - tools/confluence-config.yaml for root_page_id
 *   - tools/confluence-pages.yaml (page registry, auto-generated)
 *
 * What it does:
 *   1. Parse front matter (id, title, status, confluence_id, confluence_sync_hash)
 *   2. Skip if content hash unchanged
 *   3. Render Mermaid blocks to PNG via mmdc
 *   4. Convert Markdown to Confluence HTML via Pandoc
 *   5. Wrap with read-only cartouche + Page Properties macro (ID, status badge)
 *   6. Create or update page (parent hierarchy auto-created from file path)
 *   7. Upload Mermaid PNGs as attachments
 *   8. Set status label (status-draft / status-review / status-validated)
 *   9. Lock page editing to the publishing account
 *  10. Write back confluence_id and confluence_sync_hash to front matter
 *
 * Confluence page hierarchy mirrors the Git docs/ structure:
 *
 *   [Project Root Page]
 *   +-- PRD — Exigences Produit              <- docs/1-prd/
 *   |   +-- Audit de l'existant              <- 0-audit/
 *   |   +-- Scoping                          <- 1-scoping/
 *   |   +-- Spécification                    <- 2-specification/
 *   |   +-- Epics & Features                 <- 3-epics/  (ep-xxx > ft-xxx > us/uf/scr...)
 *   |   +-- Tests                            <- 4-tests/
 *   |   +-- Outils                           <- 5-tools/
 *   |   +-- Ateliers de revue                <- 6-workshops/
 *   +-- Tech — Architecture & Design         <- docs/2-tech/
 *   |   +-- Audit de l'existant              <- 0-audit/
 *   |   +-- Architecture                     <- 1-architecture/  (adr/)
 *   |   +-- Design Technique                 <- 2-design/  (api/, enablers/)
 *   |   +-- Implementation                  <- 3-implementation/
 *   |   +-- Qualité Continue                 <- 4-quality/
 *   |   +-- Ateliers Tech                    <- 5-workshops/
 *   +-- Steer — Pilotage Projet              <- docs/3-steer/
 *       +-- Rapports de Sprint               <- 0-sprint-reports/
 *       +-- Comités de Pilotage              <- 1-committees/
 *
 *   Display names are controlled by SECTION_TITLES below.
 *   Dynamic dirs (epics, features) are auto-formatted from their slug.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const { execFileSync } = require('child_process');
const crypto = require('crypto');
const url = require('url');

// ── Config ────────────────────────────────────────────────────────────────────

const ENV_PATH = path.join(__dirname, '..', '.env');
const PANDOC = process.env.PANDOC_PATH || 'pandoc';
const MMDC = process.env.MMDC_PATH || 'mmdc';

// Validate external tool paths — reject shell metacharacters (S-03-D)
const SAFE_PATH_RE = /^[a-zA-Z0-9_.\-\/\\:]+$/;
if (!SAFE_PATH_RE.test(PANDOC)) throw new Error(`Invalid PANDOC_PATH: ${PANDOC}`);
if (!SAFE_PATH_RE.test(MMDC))   throw new Error(`Invalid MMDC_PATH: ${MMDC}`);

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
const SPACE_KEY = process.env.CONFLUENCE_SPACE_KEY;
const AUTH      = Buffer.from(`${EMAIL}:${TOKEN}`).toString('base64');

// ── Page registry (confluence-pages.yaml) ─────────────────────────────────────
// Maps directory paths to Confluence page IDs for deterministic parent resolution.

const PAGES_REGISTRY_PATH = path.join(__dirname, '..', 'docs', 'confluence-pages.yaml');

// Load root_page_id from docs/confluence-pages.yaml (target section)
let ROOT_PAGE_ID_FROM_CONFIG = null;
const initTarget = loadTarget();
if (initTarget.root_page_id) ROOT_PAGE_ID_FROM_CONFIG = initTarget.root_page_id;

function loadTarget() {
  if (!fs.existsSync(PAGES_REGISTRY_PATH)) return {};
  const content = fs.readFileSync(PAGES_REGISTRY_PATH, 'utf8');
  const target = {};
  let inTarget = false;
  for (const line of content.split('\n')) {
    if (/^target:/.test(line)) { inTarget = true; continue; }
    if (inTarget && /^\s{2}\w/.test(line)) {
      const m = line.match(/^\s+(\w+):\s*"?([^"\n]+)"?/);
      if (m) target[m[1]] = m[2].trim().replace(/^"|"$/g, '');
    } else if (inTarget && !/^\s/.test(line) && line.trim() !== '') {
      inTarget = false;
    }
  }
  return target;
}

function loadPagesRegistry() {
  if (!fs.existsSync(PAGES_REGISTRY_PATH)) return {};
  const content = fs.readFileSync(PAGES_REGISTRY_PATH, 'utf8');
  const pages = {};
  for (const line of content.split('\n')) {
    const m = line.match(/^\s+"([^"]+)":\s*"(\d+)"/);
    if (m) pages[m[1]] = m[2];
  }
  return pages;
}

function savePagesRegistry(pages, target) {
  if (target === undefined) target = loadTarget();
  const lines = ['# Auto-generated by confluence-publish — do not edit manually'];
  if (target && Object.keys(target).length > 0) {
    lines.push('target:');
    for (const [key, val] of Object.entries(target)) {
      lines.push(`  ${key}: "${val}"`);
    }
  }
  lines.push('pages:');
  for (const [key, id] of Object.entries(pages)) {
    lines.push(`  "${key}": "${id}"`);
  }
  fs.writeFileSync(PAGES_REGISTRY_PATH, lines.join('\n') + '\n', 'utf8');
}

function registrySet(pages, key, id) {
  pages[key] = String(id);
}

// Load project language and name from docs/project.yml
let PROJECT_LANG = 'en';
let PROJECT_NAME = 'Project';
const PROJECT_YML_PATH = path.join(__dirname, '..', 'docs', 'project.yml');
if (fs.existsSync(PROJECT_YML_PATH)) {
  const projContent = fs.readFileSync(PROJECT_YML_PATH, 'utf8');
  const langMatch = projContent.match(/^lang:\s*(\w+)/m);
  if (langMatch) PROJECT_LANG = langMatch[1];
  const nameMatch = projContent.match(/^project_name:\s*(.+)/m);
  if (nameMatch) PROJECT_NAME = nameMatch[1].trim();
}

// ── i18n ─────────────────────────────────────────────────────────────────────
// Translations for Confluence UI elements (banner + section titles).
// Keyed by ISO 639-1 code from docs/project.yml `lang` field.
// To add a new language: add a new key to I18N with the same structure.
// Unsupported languages fall back to English.

const I18N = {
  en: {
    bannerTitle: 'Auto-generated page',
    bannerBody: 'This page is automatically produced and synchronised from the source repository. <strong>Please do not edit the content directly.</strong>',
    bannerContrib: 'To contribute, you can:',
    bannerComment: 'Add a <strong>comment</strong> on the page (inline or at the bottom)',
    bannerStatus: 'To move this document to <strong>review</strong> or <strong>validated</strong>, add a comment containing <code>/review</code> or <code>/validated</code>',
    sectionTitles: {
      '1-prd':            'PRD \u2014 Product Requirements',
      '2-tech':           'Tech \u2014 Architecture & Design',
      '3-steer':          'Steer \u2014 Project Governance',
      '0-audit':          'Existing System Audit',
      '1-scoping':        'Scoping',
      '2-specification':  'Specification',
      '3-epics':          'Epics & Features',
      '4-tests':          'Tests',
      '5-tools':          'Tools',
      '6-workshops':      'Review Workshops',
      '1-architecture':   'Architecture',
      '2-design':         'Technical Design',
      '3-implementation': 'Implementation',
      '4-quality':        'Continuous Quality',
      '5-workshops':      'Tech Workshops',
      '0-sprint-reports': 'Sprint Reports',
      '1-committees':     'Steering Committees',
      'adr':              'Architecture Decision Records',
      'api':              'API Contracts',
      'enablers':         'Technical Enablers',
    },
  },
  fr: {
    bannerTitle: 'Page g\u00e9n\u00e9r\u00e9e automatiquement',
    bannerBody: 'Cette page est produite et synchronis\u00e9e automatiquement depuis le r\u00e9f\u00e9rentiel source. <strong>Merci de ne pas modifier directement le contenu.</strong>',
    bannerContrib: 'Pour contribuer, vous pouvez\u00a0:',
    bannerComment: 'Ajouter un <strong>commentaire</strong> sur la page (en ligne ou en bas de page)',
    bannerStatus: 'Pour passer ce document en <strong>revue</strong> ou le <strong>valider</strong>, ajoutez un commentaire contenant <code>/r\u00e9vision</code> ou <code>/valid\u00e9</code>',
    sectionTitles: {
      '1-prd':            'PRD \u2014 Exigences Produit',
      '2-tech':           'Tech \u2014 Architecture & Design',
      '3-steer':          'Steer \u2014 Pilotage Projet',
      '0-audit':          'Audit de l\'existant',
      '1-scoping':        'Cadrage',
      '2-specification':  'Sp\u00e9cification',
      '3-epics':          'Epics & Features',
      '4-tests':          'Tests',
      '5-tools':          'Outils',
      '6-workshops':      'Ateliers de revue',
      '1-architecture':   'Architecture',
      '2-design':         'Design Technique',
      '3-implementation': 'Implementation',
      '4-quality':        'Qualit\u00e9 Continue',
      '5-workshops':      'Ateliers Tech',
      '0-sprint-reports': 'Rapports de Sprint',
      '1-committees':     'Comit\u00e9s de Pilotage',
      'adr':              'Architecture Decision Records',
      'api':              'Contrats API',
      'enablers':         'Enablers Techniques',
    },
  },
  es: {
    bannerTitle: 'P\u00e1gina generada autom\u00e1ticamente',
    bannerBody: 'Esta p\u00e1gina se produce y sincroniza autom\u00e1ticamente desde el repositorio fuente. <strong>Por favor, no edite el contenido directamente.</strong>',
    bannerContrib: 'Para contribuir, puede:',
    bannerComment: 'A\u00f1adir un <strong>comentario</strong> en la p\u00e1gina (en l\u00ednea o al final)',
    bannerStatus: 'Para pasar este documento a <strong>revisi\u00f3n</strong> o <strong>validado</strong>, a\u00f1ada un comentario con <code>/revisi\u00f3n</code> o <code>/validado</code>',
    sectionTitles: {
      '1-prd':            'PRD \u2014 Requisitos de Producto',
      '2-tech':           'Tech \u2014 Arquitectura y Dise\u00f1o',
      '3-steer':          'Steer \u2014 Gobernanza del Proyecto',
      '0-audit':          'Auditor\u00eda del Sistema Existente',
      '1-scoping':        'Alcance',
      '2-specification':  'Especificaci\u00f3n',
      '3-epics':          'Epics & Features',
      '4-tests':          'Pruebas',
      '5-tools':          'Herramientas',
      '6-workshops':      'Talleres de Revisi\u00f3n',
      '1-architecture':   'Arquitectura',
      '2-design':         'Dise\u00f1o T\u00e9cnico',
      '3-implementation': 'Implementation',
      '4-quality':        'Calidad Continua',
      '5-workshops':      'Talleres T\u00e9cnicos',
      '0-sprint-reports': 'Informes de Sprint',
      '1-committees':     'Comit\u00e9s de Direcci\u00f3n',
      'adr':              'Architecture Decision Records',
      'api':              'Contratos API',
      'enablers':         'Habilitadores T\u00e9cnicos',
    },
  },
  de: {
    bannerTitle: 'Automatisch generierte Seite',
    bannerBody: 'Diese Seite wird automatisch aus dem Quell-Repository erstellt und synchronisiert. <strong>Bitte bearbeiten Sie den Inhalt nicht direkt.</strong>',
    bannerContrib: 'Um beizutragen, k\u00f6nnen Sie:',
    bannerComment: 'Einen <strong>Kommentar</strong> auf der Seite hinzuf\u00fcgen (inline oder am Ende)',
    bannerStatus: 'Um dieses Dokument auf <strong>Pr\u00fcfung</strong> oder <strong>Validiert</strong> zu setzen, f\u00fcgen Sie einen Kommentar mit <code>/pr\u00fcfung</code> oder <code>/validiert</code> hinzu',
    sectionTitles: {
      '1-prd':            'PRD \u2014 Produktanforderungen',
      '2-tech':           'Tech \u2014 Architektur & Design',
      '3-steer':          'Steer \u2014 Projektsteuerung',
      '0-audit':          'Bestandsaufnahme',
      '1-scoping':        'Scoping',
      '2-specification':  'Spezifikation',
      '3-epics':          'Epics & Features',
      '4-tests':          'Tests',
      '5-tools':          'Werkzeuge',
      '6-workshops':      'Review-Workshops',
      '1-architecture':   'Architektur',
      '2-design':         'Technisches Design',
      '3-implementation': 'Implementation',
      '4-quality':        'Kontinuierliche Qualit\u00e4t',
      '5-workshops':      'Tech-Workshops',
      '0-sprint-reports': 'Sprint-Berichte',
      '1-committees':     'Lenkungsaussch\u00fcsse',
      'adr':              'Architecture Decision Records',
      'api':              'API-Vertr\u00e4ge',
      'enablers':         'Technische Enabler',
    },
  },
  it: {
    bannerTitle: 'Pagina generata automaticamente',
    bannerBody: 'Questa pagina \u00e8 prodotta e sincronizzata automaticamente dal repository sorgente. <strong>Si prega di non modificare direttamente il contenuto.</strong>',
    bannerContrib: 'Per contribuire, \u00e8 possibile:',
    bannerComment: 'Aggiungere un <strong>commento</strong> sulla pagina (in linea o in fondo)',
    bannerStatus: 'Per portare questo documento in <strong>revisione</strong> o <strong>validato</strong>, aggiungete un commento con <code>/revisione</code> o <code>/validato</code>',
    sectionTitles: {
      '1-prd':            'PRD \u2014 Requisiti di Prodotto',
      '2-tech':           'Tech \u2014 Architettura & Design',
      '3-steer':          'Steer \u2014 Governance del Progetto',
      '0-audit':          'Audit del Sistema Esistente',
      '1-scoping':        'Ambito',
      '2-specification':  'Specifica',
      '3-epics':          'Epics & Features',
      '4-tests':          'Test',
      '5-tools':          'Strumenti',
      '6-workshops':      'Workshop di Revisione',
      '1-architecture':   'Architettura',
      '2-design':         'Design Tecnico',
      '3-implementation': 'Implementation',
      '4-quality':        'Qualit\u00e0 Continua',
      '5-workshops':      'Workshop Tecnici',
      '0-sprint-reports': 'Report di Sprint',
      '1-committees':     'Comitati di Direzione',
      'adr':              'Architecture Decision Records',
      'api':              'Contratti API',
      'enablers':         'Enabler Tecnici',
    },
  },
  pt: {
    bannerTitle: 'P\u00e1gina gerada automaticamente',
    bannerBody: 'Esta p\u00e1gina \u00e9 produzida e sincronizada automaticamente a partir do reposit\u00f3rio fonte. <strong>Por favor, n\u00e3o edite o conte\u00fado diretamente.</strong>',
    bannerContrib: 'Para contribuir, pode:',
    bannerComment: 'Adicionar um <strong>coment\u00e1rio</strong> na p\u00e1gina (em linha ou no final)',
    bannerStatus: 'Para passar este documento para <strong>revis\u00e3o</strong> ou <strong>validado</strong>, adicione um coment\u00e1rio com <code>/revis\u00e3o</code> ou <code>/validado</code>',
    sectionTitles: {
      '1-prd':            'PRD \u2014 Requisitos de Produto',
      '2-tech':           'Tech \u2014 Arquitetura & Design',
      '3-steer':          'Steer \u2014 Governan\u00e7a do Projeto',
      '0-audit':          'Auditoria do Sistema Existente',
      '1-scoping':        'Escopo',
      '2-specification':  'Especifica\u00e7\u00e3o',
      '3-epics':          'Epics & Features',
      '4-tests':          'Testes',
      '5-tools':          'Ferramentas',
      '6-workshops':      'Workshops de Revis\u00e3o',
      '1-architecture':   'Arquitetura',
      '2-design':         'Design T\u00e9cnico',
      '3-implementation': 'Implementation',
      '4-quality':        'Qualidade Cont\u00ednua',
      '5-workshops':      'Workshops T\u00e9cnicos',
      '0-sprint-reports': 'Relat\u00f3rios de Sprint',
      '1-committees':     'Comit\u00eas de Dire\u00e7\u00e3o',
      'adr':              'Architecture Decision Records',
      'api':              'Contratos API',
      'enablers':         'Enablers T\u00e9cnicos',
    },
  },
  nl: {
    bannerTitle: 'Automatisch gegenereerde pagina',
    bannerBody: 'Deze pagina wordt automatisch geproduceerd en gesynchroniseerd vanuit de bronrepository. <strong>Bewerk de inhoud niet rechtstreeks.</strong>',
    bannerContrib: 'Om bij te dragen kunt u:',
    bannerComment: 'Een <strong>opmerking</strong> toevoegen op de pagina (inline of onderaan)',
    bannerStatus: 'Om dit document naar <strong>review</strong> of <strong>gevalideerd</strong> te zetten, voeg een opmerking toe met <code>/review</code> of <code>/gevalideerd</code>',
    sectionTitles: {
      '1-prd':            'PRD \u2014 Productvereisten',
      '2-tech':           'Tech \u2014 Architectuur & Design',
      '3-steer':          'Steer \u2014 Projectbestuur',
      '0-audit':          'Audit Bestaand Systeem',
      '1-scoping':        'Scoping',
      '2-specification':  'Specificatie',
      '3-epics':          'Epics & Features',
      '4-tests':          'Testen',
      '5-tools':          'Hulpmiddelen',
      '6-workshops':      'Review Workshops',
      '1-architecture':   'Architectuur',
      '2-design':         'Technisch Ontwerp',
      '3-implementation': 'Implementation',
      '4-quality':        'Continue Kwaliteit',
      '5-workshops':      'Tech Workshops',
      '0-sprint-reports': 'Sprintverslagen',
      '1-committees':     'Stuurgroepen',
      'adr':              'Architecture Decision Records',
      'api':              'API-contracten',
      'enablers':         'Technische Enablers',
    },
  },
  pl: {
    bannerTitle: 'Strona wygenerowana automatycznie',
    bannerBody: 'Ta strona jest tworzona i synchronizowana automatycznie z repozytorium \u017ar\u00f3d\u0142owego. <strong>Prosz\u0119 nie edytowa\u0107 tre\u015bci bezpo\u015brednio.</strong>',
    bannerContrib: 'Aby wnie\u015b\u0107 wk\u0142ad, mo\u017cesz:',
    bannerComment: 'Doda\u0107 <strong>komentarz</strong> na stronie (w tek\u015bcie lub na dole)',
    bannerStatus: 'Aby przenie\u015b\u0107 ten dokument do <strong>przegl\u0105du</strong> lub <strong>zatwierdzony</strong>, dodaj komentarz z <code>/przegl\u0105d</code> lub <code>/zatwierdzony</code>',
    sectionTitles: {
      '1-prd':            'PRD \u2014 Wymagania Produktowe',
      '2-tech':           'Tech \u2014 Architektura i Projekt',
      '3-steer':          'Steer \u2014 Zarz\u0105dzanie Projektem',
      '0-audit':          'Audyt Istniej\u0105cego Systemu',
      '1-scoping':        'Zakres',
      '2-specification':  'Specyfikacja',
      '3-epics':          'Epics & Features',
      '4-tests':          'Testy',
      '5-tools':          'Narz\u0119dzia',
      '6-workshops':      'Warsztaty Przegl\u0105dowe',
      '1-architecture':   'Architektura',
      '2-design':         'Projekt Techniczny',
      '3-implementation': 'Implementation',
      '4-quality':        'Ci\u0105g\u0142a Jako\u015b\u0107',
      '5-workshops':      'Warsztaty Techniczne',
      '0-sprint-reports': 'Raporty ze Sprintu',
      '1-committees':     'Komitety Steruj\u0105ce',
      'adr':              'Architecture Decision Records',
      'api':              'Kontrakty API',
      'enablers':         'Enablery Techniczne',
    },
  },
  no: {
    bannerTitle: 'Automatisk generert side',
    bannerBody: 'Denne siden produseres og synkroniseres automatisk fra kildelageret. <strong>Vennligst ikke rediger innholdet direkte.</strong>',
    bannerContrib: 'For \u00e5 bidra kan du:',
    bannerComment: 'Legge til en <strong>kommentar</strong> p\u00e5 siden (inline eller nederst)',
    bannerStatus: 'For \u00e5 flytte dette dokumentet til <strong>gjennomgang</strong> eller <strong>validert</strong>, legg til en kommentar med <code>/gjennomgang</code> eller <code>/validert</code>',
    sectionTitles: {
      '1-prd':            'PRD \u2014 Produktkrav',
      '2-tech':           'Tech \u2014 Arkitektur & Design',
      '3-steer':          'Steer \u2014 Prosjektstyring',
      '0-audit':          'Revisjon av Eksisterende System',
      '1-scoping':        'Omfang',
      '2-specification':  'Spesifikasjon',
      '3-epics':          'Epics & Features',
      '4-tests':          'Tester',
      '5-tools':          'Verkt\u00f8y',
      '6-workshops':      'Gjennomgangsworkshops',
      '1-architecture':   'Arkitektur',
      '2-design':         'Teknisk Design',
      '3-implementation': 'Implementation',
      '4-quality':        'Kontinuerlig Kvalitet',
      '5-workshops':      'Tekniske Workshops',
      '0-sprint-reports': 'Sprintrapporter',
      '1-committees':     'Styringskomiteer',
      'adr':              'Architecture Decision Records',
      'api':              'API-kontrakter',
      'enablers':         'Tekniske Enablere',
    },
  },
};

function i18n() {
  const lang = I18N[PROJECT_LANG];
  if (lang) return lang;
  console.log(`  WARN: no i18n for lang="${PROJECT_LANG}", falling back to English`);
  return I18N['en'];
}

// ── Mode detection ───────────────────────────────────────────────────────────

const SCAFFOLD_MODE = process.argv.includes('--scaffold');
const SINGLE_FILE_MODE = !SCAFFOLD_MODE && process.argv.includes('--file');
let SINGLE_FILE_PATH = null;

if (SINGLE_FILE_MODE) {
  const fileIdx = process.argv.indexOf('--file');
  SINGLE_FILE_PATH = process.argv[fileIdx + 1];
  if (!SINGLE_FILE_PATH || !fs.existsSync(SINGLE_FILE_PATH)) {
    console.error('ERROR: --file requires a valid path to a Markdown file.');
    process.exit(1);
  }
}

const SOURCE_DIR   = !SINGLE_FILE_MODE ? (process.argv[2] || 'docs/1-prd/scoping') : null;
const PARENT_TITLE = !SINGLE_FILE_MODE ? (process.argv[3] || 'HotelManagement') : null;
const PHASE_TITLE  = !SINGLE_FILE_MODE ? (process.argv[4] || 'Phase 1 – Scoping') : null;
const PHASE_PAGE_ID = !SINGLE_FILE_MODE ? (process.argv[5] || null) : null;
const ROOT_PAGE_ID  = !SINGLE_FILE_MODE ? (process.argv[6] || null) : null;

// ── HTTP helpers ──────────────────────────────────────────────────────────────

function apiRequest(method, apiPath, body) {
  return new Promise((resolve, reject) => {
    const parsed = new url.URL(BASE_URL + apiPath);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method,
      headers: {
        'Authorization': `Basic ${AUTH}`,
        'Content-Type': 'application/json',
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
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// Cache for the service account ID (resolved once at startup)
let _serviceAccountId = null;

async function getServiceAccountId() {
  if (_serviceAccountId) return _serviceAccountId;
  const r = await apiRequest('GET', '/rest/api/user/current');
  if (r.status === 200 && r.body.accountId) {
    _serviceAccountId = r.body.accountId;
    console.log(`  Service account: ${r.body.displayName} (${_serviceAccountId})`);
    return _serviceAccountId;
  }
  console.error('  WARN: could not resolve service account — edit restrictions will not be applied');
  return null;
}

async function lockPageEditing(pageId) {
  const accountId = await getServiceAccountId();
  if (!accountId) return;
  const payload = [{
    operation: 'update',
    restrictions: {
      user: [{ type: 'known', accountId }],
      group: []
    }
  }];
  const r = await apiRequest('PUT', `/rest/api/content/${pageId}/restriction`, payload);
  if (r.status === 200) {
    console.log(`    ~ LOCKED  edit restricted to service account`);
  } else {
    console.error(`    WARN: could not set edit restriction (HTTP ${r.status})`);
  }
}

async function findPage(title) {
  const encoded = encodeURIComponent(title);
  const r = await apiRequest('GET', `/rest/api/content?title=${encoded}&spaceKey=${SPACE_KEY}&expand=version`);
  if (r.body.size > 0) return r.body.results[0];
  return null;
}

async function findChildPage(parentId, title) {
  const encoded = encodeURIComponent(title);
  const r = await apiRequest('GET', `/rest/api/content/search?cql=ancestor=${parentId}+AND+title="${encoded}"+AND+space="${SPACE_KEY}"&expand=version`);
  if (r.body && r.body.results && r.body.results.length > 0) return r.body.results[0];
  return null;
}

async function createPage(title, parentId, htmlBody) {
  const payload = {
    type: 'page',
    title,
    space: { key: SPACE_KEY },
    body: { storage: { value: htmlBody, representation: 'storage' } },
  };
  if (parentId) payload.ancestors = [{ id: parentId }];
  const r = await apiRequest('POST', '/rest/api/content', payload);
  if (r.status !== 200) throw new Error(`Create failed (${r.status}): ${JSON.stringify(r.body)}`);
  return r.body;
}

async function updatePage(pageId, title, version, htmlBody) {
  const payload = {
    type: 'page',
    title,
    version: { number: version + 1 },
    body: { storage: { value: htmlBody, representation: 'storage' } },
  };
  const r = await apiRequest('PUT', `/rest/api/content/${pageId}`, payload);
  if (r.status !== 200) throw new Error(`Update failed (${r.status}): ${JSON.stringify(r.body)}`);
  return r.body;
}

async function getPageById(id) {
  const r = await apiRequest('GET', `/rest/api/content/${id}?expand=version`);
  if (r.status === 200) return r.body;
  return null;
}

async function findOrCreate(title, parentId, htmlBody, knownId) {
  if (knownId) {
    const existing = await getPageById(knownId);
    if (existing) {
      console.log(`  ~ EXISTS  "${title}" (id=${existing.id}) [by known ID]`);
      return existing;
    }
  }
  const existing = await findPage(title);
  if (existing) {
    console.log(`  ~ EXISTS  "${title}" (id=${existing.id})`);
    return existing;
  }
  const page = await createPage(title, parentId, htmlBody);
  console.log(`  + CREATED "${title}" (id=${page.id})`);
  return page;
}

async function setLabels(pageId, labels) {
  // Remove existing status-* labels, then add the new ones
  const r = await apiRequest('GET', `/rest/api/content/${pageId}/label`);
  if (r.status === 200 && r.body.results) {
    for (const label of r.body.results) {
      if (label.name.startsWith('status-')) {
        await apiRequest('DELETE', `/rest/api/content/${pageId}/label/${label.name}`);
      }
    }
  }
  for (const label of labels) {
    await apiRequest('POST', `/rest/api/content/${pageId}/label`, [{ prefix: 'global', name: label }]);
  }
}

// ── Mermaid helpers ───────────────────────────────────────────────────────────

function extractAndReplaceMermaid(mdContent) {
  const diagrams = [];
  let idx = 0;
  const processed = mdContent.replace(/```mermaid\r?\n([\s\S]*?)```/g, (_, content) => {
    const filename = `mermaid-${idx}.png`;
    diagrams.push({ idx, content, filename });
    idx++;
    return `<ac:image ac:align="center"><ri:attachment ri:filename="${filename}"/></ac:image>`;
  });
  return { processed, diagrams };
}

function renderMermaidToPng(mmdContent, idx) {
  const tmpDir = (process.env.TEMP || '/tmp').replace(/\\/g, '/');
  const mmdFile = `${tmpDir}/_mermaid_${idx}.mmd`;
  const pngFile = `${tmpDir}/_mermaid_${idx}.png`;
  fs.writeFileSync(mmdFile, mmdContent, 'utf8');
  execFileSync(MMDC, ['-i', mmdFile, '-o', pngFile, '--backgroundColor', 'white'], { stdio: 'pipe' });
  return pngFile;
}

async function uploadAttachment(pageId, filePath, filename) {
  const fileContent = fs.readFileSync(filePath);
  const boundary = '----FormBoundary' + Date.now();
  const body = Buffer.concat([
    Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${filename}"\r\nContent-Type: image/png\r\n\r\n`),
    fileContent,
    Buffer.from(`\r\n--${boundary}--\r\n`),
  ]);
  return new Promise((resolve, reject) => {
    const parsed = new url.URL(BASE_URL + `/rest/api/content/${pageId}/child/attachment`);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: 'POST',
      headers: {
        'Authorization': `Basic ${AUTH}`,
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length,
        'X-Atlassian-Token': 'no-check',
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
    req.write(body);
    req.end();
  });
}

// ── Markdown helpers ──────────────────────────────────────────────────────────

function parseFrontMatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) return { meta: {}, body: content, rawFrontMatter: '' };
  const meta = {};
  const rawFrontMatter = match[1];
  for (const line of rawFrontMatter.split('\n')) {
    const m = line.match(/^(\w+):\s*"?([^"]*)"?/);
    if (m) meta[m[1]] = m[2].trim();
  }
  return { meta, body: match[2], rawFrontMatter };
}

function contentHash(body) {
  return crypto.createHash('sha256').update(body).digest('hex').substring(0, 12);
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

function mdToHtml(mdContent) {
  const tmpIn  = path.join(process.env.TEMP || '/tmp', '_cf_input.md');
  const tmpOut = path.join(process.env.TEMP || '/tmp', '_cf_output.html');
  fs.writeFileSync(tmpIn, mdContent, 'utf8');
  execFileSync(PANDOC, ['-f', 'markdown', '-t', 'html', '--wrap=none', '-o', tmpOut, tmpIn]);
  return fs.readFileSync(tmpOut, 'utf8');
}

function statusBanner(status) {
  const colors = { draft: 'Yellow', review: 'Blue', validated: 'Green' };
  const color = colors[status] || 'Yellow';
  return `<ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">${color}</ac:parameter><ac:parameter ac:name="title">${status.toUpperCase()}</ac:parameter></ac:structured-macro>`;
}

// ── Core publish logic ───────────────────────────────────────────────────────

const mapping = [];

async function publishFile(filePath, parentId) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const { meta, body } = parseFrontMatter(raw);

  // No status filter — push any deliverable regardless of status.
  // If this is an update to a validated/review page, the hook resets status to draft.

  const status = meta.status || 'draft';
  const title = meta.title || meta.id || path.basename(filePath, '.md');
  console.log(`\n  Publishing: ${meta.id || path.basename(filePath)} — ${title.substring(0, 60)}`);

  // Check if content actually changed (skip if hash matches)
  const currentHash = contentHash(body);
  if (meta.confluence_sync_hash === currentHash && meta.confluence_id) {
    console.log(`    = UNCHANGED (hash=${currentHash}) — skipping`);
    return null;
  }

  const { processed: bodyWithMacros, diagrams } = extractAndReplaceMermaid(body);

  const pngFiles = [];
  for (const diag of diagrams) {
    try {
      const pngPath = renderMermaidToPng(diag.content, diag.idx);
      pngFiles.push({ pngPath, filename: diag.filename });
      console.log(`    ~ MERMAID  diagram ${diag.idx} → ${diag.filename}`);
    } catch (e) {
      console.error(`    WARN rendering mermaid ${diag.idx}: ${e.message}`);
    }
  }

  let html;
  try {
    html = mdToHtml(bodyWithMacros);
  } catch (e) {
    console.error(`    ERROR converting ${path.basename(filePath)}: ${e.message}`);
    return null;
  }

  const banner = statusBanner(status);
  // Read-only warning cartouche (language from docs/project.yml)
  const t = i18n();
  const readOnlyNotice = `<ac:structured-macro ac:name="info"><ac:parameter ac:name="icon">true</ac:parameter><ac:parameter ac:name="title">${t.bannerTitle}</ac:parameter><ac:rich-text-body>`
    + `<p>${t.bannerBody}</p>`
    + `<p>${t.bannerContrib}</p>`
    + `<ul><li>${t.bannerComment}</li>`
    + `<li>${t.bannerStatus}</li></ul>`
    + `</ac:rich-text-body></ac:structured-macro>`;
  // Page Properties macro for structured metadata
  const pageProps = `<ac:structured-macro ac:name="details"><ac:rich-text-body>`
    + `<table><tbody>`
    + `<tr><th>ID</th><td>${meta.id || '—'}</td></tr>`
    + `<tr><th>Status</th><td>${banner}</td></tr>`
    + `<tr><th>Version</th><td>${meta.version || '1.0'}</td></tr>`
    + `<tr><th>Last updated</th><td>${meta.last_updated || new Date().toISOString().split('T')[0]}</td></tr>`
    + `</tbody></table>`
    + `</ac:rich-text-body></ac:structured-macro>`;
  const fullHtml = readOnlyNotice + pageProps + html;

  let page;

  // Prefer ID-based lookup if confluence_id is known
  if (meta.confluence_id) {
    const existing = await getPageById(meta.confluence_id);
    if (existing) {
      page = await updatePage(existing.id, title, existing.version.number, fullHtml);
      console.log(`    ~ UPDATED (id=${page.id})`);
    } else {
      // ID was stale, create new
      page = await createPage(title, parentId, fullHtml);
      console.log(`    + CREATED (id=${page.id}) [stale confluence_id replaced]`);
    }
  } else {
    // No confluence_id — try title lookup, then create
    let existing = await findPage(title);
    if (!existing && meta.id && meta.id !== title) existing = await findPage(meta.id);
    if (existing) {
      page = await updatePage(existing.id, title, existing.version.number, fullHtml);
      console.log(`    ~ UPDATED (id=${page.id}) [found by title]`);
    } else {
      page = await createPage(title, parentId, fullHtml);
      console.log(`    + CREATED (id=${page.id})`);
    }
  }

  // Upload Mermaid PNGs as attachments
  for (const { pngPath, filename } of pngFiles) {
    try {
      const r = await uploadAttachment(page.id, pngPath, filename);
      if (r.status === 200) {
        console.log(`    ~ ATTACHED ${filename} (ok)`);
      } else {
        console.error(`    WARN attaching ${filename}: HTTP ${r.status}`);
      }
    } catch (e) {
      console.error(`    WARN attaching ${filename}: ${e.message}`);
    }
  }

  // Set status label on the page
  await setLabels(page.id, [`status-${status}`]);

  // Restrict page editing to the service account only (comments & labels remain open)
  await lockPageEditing(page.id);

  // Write back confluence_id and sync_hash to the MD front matter
  writeFrontMatterField(filePath, 'confluence_id', page.id);
  writeFrontMatterField(filePath, 'confluence_sync_hash', currentHash);
  console.log(`    ~ SYNCED  confluence_id=${page.id}, hash=${currentHash}`);

  const pageUrl = `${BASE_URL}/spaces/${SPACE_KEY}/pages/${page.id}`;
  mapping.push({ id: meta.id, title, url: pageUrl, status, date: new Date().toISOString().split('T')[0] });
  return page;
}

// ── Section title mapping ────────────────────────────────────────────────────
// Maps directory names to human-friendly Confluence page titles.
// Language-aware: reads from I18N[PROJECT_LANG].sectionTitles.
// Dynamic segments (epics, features, etc.) fall through to slug formatting.

function sectionTitle(dirName) {
  const titles = i18n().sectionTitles;
  if (titles[dirName]) return titles[dirName];
  // Fallback: strip leading number prefix, replace hyphens, title-case
  return dirName
    .replace(/^\d+-/, '')
    .replace(/-/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}

// ── Single-file mode: resolve parent from path ──────────────────────────────

async function resolveParentFromPath(filePath) {
  // Derive Confluence parent hierarchy from file path relative to docs/
  const docsRoot = path.resolve('docs');
  const relPath = path.relative(docsRoot, path.resolve(filePath));
  const segments = path.dirname(relPath).split(path.sep).filter(s => s && s !== '.');

  const pages = loadPagesRegistry();
  let registryChanged = false;

  // Start from root page (registry, config, or space root)
  let parentId = pages['/'] || ROOT_PAGE_ID_FROM_CONFIG || null;

  let registryKey = '';
  let prevSegment = '';
  for (const segment of segments) {
    registryKey = registryKey ? `${registryKey}/${segment}` : segment;
    // Suffix the project name so section pages are unique per project in a shared
    // Confluence space. Mirrors the behaviour of scaffoldConfluenceHierarchy which
    // already does this for top-level sections (1-prd, 2-tech, 3-steer).
    // Without the suffix, generic titles like "Scoping" would collide across projects.
    // Additionally, when a leaf section (user-stories, journeys, screens, etc.) is
    // nested inside a feature directory (ft-xxx), include the feature slug in the title
    // to prevent Confluence space-wide title collisions across features.
    const featureQualifier = prevSegment.startsWith('ft-') ? ` — ${prevSegment}` : '';
    const title = `${sectionTitle(segment)}${featureQualifier} — ${PROJECT_NAME}`;

    // Check registry first
    const knownId = pages[registryKey];
    if (knownId) {
      // Verify that the registered page exists AND is a direct child of the current
      // parent. Using expand=ancestors is title-independent, which matters because
      // top-level section pages are created with a project-name suffix by --scaffold
      // (e.g. "PRD — Product Requirements — Activity Tracking") while sectionTitle()
      // returns the short form ("PRD — Product Requirements"). A title-based check
      // would therefore always fail for those segments, causing false "stale" reports
      // and duplicate section pages.
      const r = await apiRequest('GET', `/rest/api/content/${knownId}?expand=ancestors`);
      if (r.status === 200) {
        const ancestors = r.body.ancestors || [];
        const directParent = ancestors[ancestors.length - 1];
        if (directParent && String(directParent.id) === String(parentId)) {
          // Correctly placed under the expected parent — registry entry is valid
          parentId = String(knownId);
          prevSegment = segment;
          continue;
        }
        // Page exists in Confluence but its direct parent does not match the expected
        // one — stale registry entry from a previous project (e.g. MyHotel).
        const actualParentId = directParent ? directParent.id : 'none';
        console.log(`  ~ REGISTRY STALE  "${registryKey}" id=${knownId} parent=${actualParentId} (expected ${parentId}) — will create under correct parent`);
      }
      // Page missing (404) or stale — fall through to findOrCreate
    }

    // Create on demand and register.
    // Use findChildPage (parent-scoped) rather than findOrCreate (space-wide) to
    // avoid picking up identically-named section pages from previous projects in
    // the same Confluence space (e.g. an old "Scoping" page from MyHotel).
    let parent = await findChildPage(parentId, title);
    if (parent) {
      console.log(`  ~ EXISTS  "${title}" (id=${parent.id}) [child of ${parentId}]`);
    } else {
      parent = await createPage(title, parentId, `<p>Section : ${title}</p>`);
      console.log(`  + CREATED "${title}" (id=${parent.id})`);
    }
    parentId = parent.id;
    registrySet(pages, registryKey, parent.id);
    registryChanged = true;
    prevSegment = segment;
  }

  if (registryChanged) {
    savePagesRegistry(pages);
  }

  return parentId;
}

// ── Directory mode ───────────────────────────────────────────────────────────

async function processDirectory(dirPath, parentId) {
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });
  const mdFiles = entries.filter(e => e.isFile() && e.name.endsWith('.md'));
  const subdirs = entries.filter(e => e.isDirectory());

  if (mdFiles.length === 1) {
    const mainPage = await publishFile(path.join(dirPath, mdFiles[0].name), parentId);
    const childParentId = mainPage ? mainPage.id : parentId;
    for (const d of subdirs) {
      await processDirectory(path.join(dirPath, d.name), childParentId);
    }
  } else {
    for (const f of mdFiles) {
      await publishFile(path.join(dirPath, f.name), parentId);
    }
    for (const d of subdirs) {
      await processDirectory(path.join(dirPath, d.name), parentId);
    }
  }
}

// ── Scaffold mode: create root + top-level section pages ─────────────────────

async function scaffoldConfluenceHierarchy() {
  const projYmlPath = path.join(__dirname, '..', 'docs', 'project.yml');
  if (!fs.existsSync(projYmlPath)) {
    console.error('ERROR: docs/project.yml not found. Run scaffold first.');
    process.exit(1);
  }
  const projContent = fs.readFileSync(projYmlPath, 'utf8');
  const nameMatch = projContent.match(/^project_name:\s*(.+)/m);
  const projectName = nameMatch ? nameMatch[1].trim() : 'Project';

  const t = i18n();
  const topSections = [
    { key: '1-prd',   title: `${t.sectionTitles['1-prd']} — ${projectName}` },
    { key: '2-tech',  title: `${t.sectionTitles['2-tech']} — ${projectName}` },
    { key: '3-steer', title: `${t.sectionTitles['3-steer']} — ${projectName}` },
  ];

  const pages = loadPagesRegistry();

  // 1. Root project page
  let rootId = pages['/'];
  if (rootId) {
    const existing = await getPageById(rootId);
    if (existing && existing.title === projectName) {
      console.log(`  ~ ROOT EXISTS  "${projectName}" (id=${rootId})`);
    } else {
      if (existing && existing.title !== projectName) {
        console.log(`  ~ ROOT ID MISMATCH  stored id=${rootId} belongs to "${existing.title}", not "${projectName}" — searching by name`);
      }
      rootId = null; // stale or wrong project, search/create by name
    }
  }
  if (!rootId) {
    const rootPage = await findOrCreate(
      projectName, null,
      `<p>Espace documentaire du projet <strong>${projectName}</strong>.</p>`,
      null
    );
    rootId = rootPage.id;
  }
  registrySet(pages, '/', rootId);

  // 2. Top-level section pages
  for (const section of topSections) {
    let sectionId = pages[section.key];
    if (sectionId) {
      const existing = await getPageById(sectionId);
      if (existing && existing.title === section.title) {
        // Also verify it is a child of the current root
        const child = await findChildPage(rootId, section.title);
        if (child && child.id === sectionId) {
          console.log(`  ~ SECTION EXISTS  "${section.title}" (id=${sectionId})`);
          continue;
        }
      }
      console.log(`  ~ SECTION ID STALE/MISMATCH  id=${sectionId} — searching under root ${rootId}`);
      sectionId = null;
    }
    // Search strictly under the project root, then create if absent
    const existingChild = await findChildPage(rootId, section.title);
    if (existingChild) {
      console.log(`  ~ SECTION EXISTS  "${section.title}" (id=${existingChild.id}) [found under root]`);
      registrySet(pages, section.key, existingChild.id);
      continue;
    }
    const sectionPage = await createPage(section.title, rootId, `<p>Section : ${section.title}</p>`);
    console.log(`  + SECTION CREATED  "${section.title}" (id=${sectionPage.id})`);
    registrySet(pages, section.key, sectionPage.id);
  }

  savePagesRegistry(pages, { space_key: SPACE_KEY, root_page_id: rootId });
  console.log(`  ~ TARGET  space_key=${SPACE_KEY}, root_page_id=${rootId} written to docs/confluence-pages.yaml`);
  console.log(`\nConfluence hierarchy ready. Registry: docs/confluence-pages.yaml`);
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  // Resolve service account early to validate credentials
  await getServiceAccountId();

  if (SCAFFOLD_MODE) {
    console.log(`\nConfluence Publisher (scaffold mode)`);
    console.log(`Space : ${SPACE_KEY}\n`);
    await scaffoldConfluenceHierarchy();
    return;
  }

  if (SINGLE_FILE_MODE) {
    // Single file mode: --file <path>
    console.log(`\nConfluence Publisher (single file)`);
    console.log(`Space : ${SPACE_KEY}`);
    console.log(`File  : ${SINGLE_FILE_PATH}\n`);

    const parentId = await resolveParentFromPath(SINGLE_FILE_PATH);
    const page = await publishFile(SINGLE_FILE_PATH, parentId);

    if (page) {
      const pageUrl = `${BASE_URL}/spaces/${SPACE_KEY}/pages/${page.id}`;
      console.log(`\nDone. Page published: ${pageUrl}`);
    } else {
      console.log('\nDone. No changes to publish.');
    }
  } else {
    // Directory mode (legacy)
    console.log(`\nConfluence Publisher (directory)`);
    console.log(`Space   : ${SPACE_KEY}`);
    console.log(`Source  : ${SOURCE_DIR}`);
    console.log(`Parent  : ${PARENT_TITLE} > ${PHASE_TITLE}\n`);

    const rootPage = await findOrCreate(
      PARENT_TITLE, null,
      '<p>Espace documentaire du projet.</p>',
      ROOT_PAGE_ID
    );

    const phasePage = await findOrCreate(
      PHASE_TITLE, rootPage.id,
      `<p>Livrables — ${PHASE_TITLE}.</p>`,
      PHASE_PAGE_ID
    );

    await processDirectory(SOURCE_DIR, phasePage.id);

    // Update mapping file
    const mappingPath = path.join(__dirname, 'confluence-mapping.md');
    const rows = mapping.map(m => `| ${m.id} | ${m.title.substring(0,50)} | ${m.url} | ${m.status} | ${m.date} |`).join('\n');
    const header = `## Confluence Pages Mapping\n\n| BA-ID | Title | Confluence URL | Status | Last sync |\n|-------|-------|----------------|--------|-----------|\n`;
    fs.writeFileSync(mappingPath, header + rows + '\n', 'utf8');

    console.log(`\nDone. ${mapping.length} page(s) published.`);
    console.log(`Mapping updated: tools/confluence-mapping.md\n`);
    for (const m of mapping) console.log(`  [${m.id}] ${m.url}`);
  }
}

main().catch(e => { console.error('\nFATAL:', e.message); process.exit(1); });
