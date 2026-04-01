#!/usr/bin/env python3
"""
Comprehensive local CI simulator for all deterministic station checks.

Covers:
  A1 - Policy validation (P-01 through P-05)
  A2 - Security static checks (S-03, S-04) — scoped to changed files
  A3 - Prompt injection / exfil hardening (PI-01 through PI-06)
  A5 - Sandbox simulation (basic constraint presence checks)

Scans ALL agent paths the pipeline inspects:
  - .apm/agents/*.md              (canonical)
  - .github/agents/*.agent.md      (Copilot projection)
  - providers/github-copilot/agents/*.agent.md  (provider source)

Important: A2 and A3 apply code-block exclusions per station definitions.
A3 PI-06 uses word-boundary matching to avoid false positives on
"directories"/"directives".
"""
import pathlib, re, sys, json, subprocess
from collections import defaultdict

root = pathlib.Path(__file__).resolve().parents[1]
findings = []  # list of dicts: {station, check, severity, file, message}

def add(station, check, severity, filepath, message):
    rel = str(filepath.relative_to(root)).replace('\\', '/')
    findings.append({
        'station': station, 'check': check, 'severity': severity,
        'file': rel, 'message': message,
    })

def extract_frontmatter(text):
    """Return frontmatter string (between --- delimiters) or empty string."""
    m = re.match(r'^---\n(.*?)\n---', text, re.S)
    return m.group(1) if m else ''

def extract_body(text):
    """Return body text after frontmatter."""
    m = re.match(r'^---\n.*?\n---\n?(.*)', text, re.S)
    return m.group(1) if m else text

def strip_code_blocks(text):
    """Remove fenced code blocks (may contain example attack patterns)."""
    return re.sub(r'```[^`]*?```', '', text, flags=re.S)

def is_in_code_block(text, match_start):
    """Check if a match position falls inside a fenced code block."""
    for block in re.finditer(r'```[^`]*?```', text, re.S):
        if block.start() <= match_start <= block.end():
            return True
    return False

def has_safety_comment_in_block(text, match_start):
    """Check if the code block containing the match has a safety comment."""
    safety_re = re.compile(r'#\s*(example|do not follow|do not interpret|detection patterns)', re.I)
    for block in re.finditer(r'```[^`]*?```', text, re.S):
        if block.start() <= match_start <= block.end():
            return bool(safety_re.search(block.group()))
    return False

def is_documentation_context(text, match_start, window=120):
    """Check if the match is in a documentation/example context (describing threats)."""
    start = max(0, match_start - window)
    end = min(len(text), match_start + window)
    surrounding = text[start:end].lower()
    doc_markers = [
        'example', 'e.g.', 'such as', 'look for', 'check for', 'scan for',
        'detect', 'pattern', 'known', 'trigger', 'the following',
        'direct injection', 'indirect injection', 'prompt injection',
    ]
    return any(marker in surrounding for marker in doc_markers)


# ══════════════════════════════════════════════════════════════
# Collect files
# ══════════════════════════════════════════════════════════════
canonical_agents = sorted(root.glob('.apm/agents/*.md'))
projected_agents = sorted(root.glob('.github/agents/*.agent.md'))
provider_agents = sorted(root.glob('providers/github-copilot/agents/*.agent.md'))
all_agents = canonical_agents + projected_agents + provider_agents

canonical_skills = sorted(root.glob('.apm/skills/*/SKILL.md'))

all_prompts = (
    sorted(root.glob('.apm/prompts/**/*.md'))
    + sorted(root.glob('.github/prompts/*.prompt.md'))
    + sorted(root.glob('providers/github-copilot/prompts/*.prompt.md'))
)

# Exclude ci-gates/stations/ from scanning (pipeline infra, not user agents)
def not_station(f):
    return 'ci-gates/stations' not in str(f).replace('\\', '/')

all_agents = [f for f in all_agents if not_station(f)]
all_prompts = [f for f in all_prompts if not_station(f)]

TOOL_ALLOWLIST = {
    'codebase', 'search', 'edit/editFiles', 'problems',
    'runCommands', 'github', 'terminal', 'fetch', 'vscode',
}

# Get changed files from git (the pipeline only scans changed files for A2)
def get_changed_files():
    """Get list of files changed vs main branch (or uncommitted)."""
    changed = set()
    try:
        # Staged + working tree changes
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD'],
            capture_output=True, text=True, cwd=root
        )
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                changed.add(root / line.strip())
        # Also include all uncommitted changes
        result2 = subprocess.run(
            ['git', 'diff', '--name-only', '--cached'],
            capture_output=True, text=True, cwd=root
        )
        for line in result2.stdout.strip().split('\n'):
            if line.strip():
                changed.add(root / line.strip())
    except Exception:
        pass
    return changed


# ══════════════════════════════════════════════════════════════
# A1 — Policy Validation
# ══════════════════════════════════════════════════════════════
def check_a1():
    # Agents: P-01, P-02, P-03, P-04, P-05
    for f in all_agents:
        content = f.read_text(encoding='utf-8')
        fm = extract_frontmatter(content)
        if not fm:
            add('A1', 'P-01', 'critical', f, 'No YAML frontmatter')
            continue
        if not re.search(r'^name:', fm, re.M):
            add('A1', 'P-01', 'critical', f, 'Missing name in frontmatter')
        if not re.search(r'^description:', fm, re.M):
            add('A1', 'P-01', 'critical', f, 'Missing description in frontmatter')
        if not re.search(r'^tools:', fm, re.M):
            add('A1', 'P-01', 'critical', f, 'Missing tools in frontmatter')

        # P-02: tool allowlist
        m = re.search(r"tools:\s*\[([^\]]*)\]", fm)
        if m:
            tools = [t.strip().strip("'\"") for t in m.group(1).split(',') if t.strip()]
            for t in tools:
                if t not in TOOL_ALLOWLIST:
                    add('A1', 'P-02', 'critical', f, f'Unknown tool: "{t}"')

        # P-03: runCommands + commandAllowlist
        if 'runCommands' in fm and not re.search(r'^commandAllowlist:', fm, re.M):
            add('A1', 'P-03', 'critical', f, 'runCommands without commandAllowlist')

        # P-04: fetch + allowedNetworkDomains
        if "'fetch'" in fm or '"fetch"' in fm:
            if not re.search(r'^allowedNetworkDomains:', fm, re.M):
                add('A1', 'P-04', 'high', f, 'fetch without allowedNetworkDomains')

        # P-05: description quality
        dm = re.search(r"description:\s*['\"]([^'\"]*)['\"]", fm)
        if dm and len(dm.group(1)) < 20:
            add('A1', 'P-05', 'low', f, f'Description too short ({len(dm.group(1))} chars)')

    # Skills: P-01
    for f in canonical_skills:
        content = f.read_text(encoding='utf-8')
        fm = extract_frontmatter(content)
        if not fm:
            add('A1', 'P-01', 'critical', f, 'No YAML frontmatter')
            continue
        if not re.search(r'^name:', fm, re.M):
            add('A1', 'P-01', 'critical', f, 'Missing name in frontmatter')
        if not re.search(r'^description:', fm, re.M):
            add('A1', 'P-01', 'critical', f, 'Missing description in frontmatter')
        if not re.search(r'^triggers:', fm, re.M):
            add('A1', 'P-01', 'critical', f, 'Missing triggers in frontmatter')


# ══════════════════════════════════════════════════════════════
# A2 — Security Static Checks (deterministic patterns only)
# ══════════════════════════════════════════════════════════════
#
# Per the A2 station definition:
# - Only scan files in the git diff (changed files)
# - Files under **/fixtures/**, **/test*/**, or ci-gates/stations/**
#   are downgraded to info severity
# - Code blocks with safety comments are excluded
# - S-03-F specifically checks for /** in allowedFilePaths context
#
DANGEROUS_PATTERNS_A2 = [
    ('S-03-A', r'curl\s+[^\|]+\|\s*(bash|sh)\b', 'Piping curl to shell', 'critical'),
    ('S-03-B', r'wget\s+[^\|]+\|\s*(bash|sh)\b', 'Piping wget to shell', 'critical'),
    ('S-03-C', r'\beval\s*\(', 'Use of eval()', 'high'),
    ('S-03-D', r'subprocess\.call\([^)]*shell\s*=\s*True', 'Python shell=True subprocess', 'high'),
    ('S-03-E', r'os\.system\s*\(', 'os.system() call', 'high'),
    # S-03-F is handled separately (needs line-scoped matching for allowedFilePaths)
    ('S-03-G', r'\brm\s+-rf\s+/', 'Recursive delete from root', 'critical'),
    ('S-03-H', r'chmod\s+777\b', 'World-writable permissions', 'medium'),
]

SENSITIVE_PATHS = [
    '/etc/passwd', '/etc/shadow', '~/.ssh/', '~/.aws/credentials', '~/.config/',
]

def is_fixture_or_test(f):
    rel = str(f.relative_to(root)).replace('\\', '/')
    return any(seg in rel for seg in ['fixtures/', '/test', 'ci-gates/stations/'])

def check_a2():
    # The real pipeline scans only changed files. We scan all agent/skill files
    # (since they're the ones that matter) plus scripts.
    scan_files = set()
    for f in all_agents:
        scan_files.add(f)
    for f in canonical_skills:
        scan_files.add(f)
    # Also scan script files
    for f in root.glob('scripts/**/*.py'):
        scan_files.add(f)
    for f in root.glob('ci-gates/scripts/**'):
        if f.is_file():
            scan_files.add(f)

    for f in sorted(scan_files):
        if not f.is_file():
            continue
        try:
            content = f.read_text(encoding='utf-8')
        except (UnicodeDecodeError, PermissionError):
            continue

        is_fixture = is_fixture_or_test(f)
        # Also treat skill SKILL.md files that document detection patterns as info
        is_detection_skill = any(name in str(f) for name in [
            'secret-scan', 'injection-detection', 'soprasteria-agent-policy-guard',
            'red-team-simulation',
        ])
        # Scripts that ARE the scanner should not flag themselves
        is_self = 'simulate_ci.py' in f.name or 'check_policy.py' in f.name

        if is_self:
            continue

        for rule_id, pattern_re, desc, severity in DANGEROUS_PATTERNS_A2:
            for m in re.finditer(pattern_re, content):
                if is_in_code_block(content, m.start()):
                    if has_safety_comment_in_block(content, m.start()):
                        continue
                    if is_detection_skill:
                        continue
                # Skip eval() in inline code (backtick-wrapped documentation)
                if rule_id == 'S-03-C':
                    start = max(0, m.start() - 2)
                    end = min(len(content), m.end() + 2)
                    if '`' in content[start:m.start()] and '`' in content[m.end():end]:
                        continue
                    # Skip in documentation/threat-model context
                    if is_documentation_context(content, m.start()):
                        continue
                if is_fixture or is_detection_skill:
                    continue
                add('A2', rule_id, severity, f, desc)

        # S-03-F: Wildcard /** in allowedFilePaths — check per-line in frontmatter
        fm = extract_frontmatter(content)
        if fm:
            for line in fm.split('\n'):
                if 'allowedFilePaths' in line and ('/**' in line or "**" in line):
                    if is_fixture or is_detection_skill:
                        continue
                    add('A2', 'S-03-F', 'high', f, f'Wildcard in allowedFilePaths: {line.strip()}')

        # S-04: sensitive path access (only flag if not in defensive/exclusion context)
        for sp in SENSITIVE_PATHS:
            idx = content.find(sp)
            if idx >= 0:
                if is_in_code_block(content, idx):
                    continue
                if is_fixture or is_detection_skill or is_self:
                    continue
                # Skip if it's in a defensive / exclusion context
                surrounding = content[max(0,idx-150):idx+100].lower()
                if any(kw in surrounding for kw in [
                    'do not read', 'do not open', 'do not access', 'do not',
                    'skip', 'exclusion', 'exclude', 'never read', 'never include',
                    'refuse', 'sensitive file', 'credential', 'must not',
                    'sensitive path', 'matching these patterns',
                ]):
                    continue
                add('A2', 'S-04', 'high', f, f'Reference to sensitive path: {sp}')


# ══════════════════════════════════════════════════════════════
# A3 — Prompt Injection & Exfil Hardening
# ══════════════════════════════════════════════════════════════
JAILBREAK_PATTERNS = [
    (r'ignore\s+(all|previous|above|prior)\s+instructions?', 'Instruction override', 'critical'),
    (r'disregard\s+(your|all)\s+(previous|prior)', 'Instruction override variant', 'critical'),
    (r'you\s+(are|were)\s+now\s+(a|an)', 'Role reassignment', 'high'),
    (r'pretend\s+(you are|to be)', 'Persona hijack', 'high'),
    (r'\bdo anything now\b', 'DAN jailbreak', 'high'),
    (r'your\s+(new|real|true)\s+instructions', 'System prompt override', 'high'),
    (r'\bdeveloper mode\b', 'Developer-mode jailbreak', 'high'),
    (r'\[SYSTEM\]|\[INST\]', 'Injected system-role delimiter', 'critical'),
]

PI02_ANCHORS = [
    # "must not" / "will not" / "never" + action verb
    r'(?:must\s+not|will\s+not|MUST\s+NOT|never)\s+\w*\s*(?:delete|modify|send|exfiltrate|bypass)',
    # "refuse" + trigger
    r'refuse\s+\w*\s*(?:request|instruction|attempt)',
    # explicit "out of scope" section
    r'out\s+of\s+scope',
]

# PI-06: Use word boundaries to avoid matching "directories"/"directives"
INDIRECT_INJECTION = (
    r'(read|process|execute|follow).{0,40}'
    r'(file|document|webpage|url).{0,40}'
    r'(instructions?\b|steps?\b|directives?\b)'
)

def check_a3():
    # Per station def: scan agent, skill, and prompt files (excluding ci-gates/stations/)
    target_files = all_agents + list(canonical_skills) + all_prompts

    for f in target_files:
        try:
            content = f.read_text(encoding='utf-8')
        except (UnicodeDecodeError, PermissionError):
            continue

        body = extract_body(content)
        body_no_code = strip_code_blocks(body)

        # Is this a detection/security skill that documents patterns?
        is_detection_skill = any(name in str(f) for name in [
            'secret-scan', 'injection-detection', 'soprasteria-agent-policy-guard',
            'red-team-simulation',
        ])

        # PI-01: Jailbreak patterns
        for pattern_re, desc, severity in JAILBREAK_PATTERNS:
            for m in re.finditer(pattern_re, body, re.I):
                # Skip matches inside code blocks with safety comments
                if is_in_code_block(body, m.start()):
                    continue
                # Skip matches in documentation context (describing threats)
                if is_documentation_context(body, m.start()):
                    continue
                # Skip in detection skills
                if is_detection_skill:
                    continue
                add('A3', 'PI-01', severity, f, f'Jailbreak pattern: {desc} — "{m.group()}"')

        # PI-02: Non-negotiable refusal constraints (agent files only)
        is_agent = (
            f.name.endswith('.agent.md')
            or (f.parent.name == 'agents' and f.name.endswith('.md'))
        )
        if is_agent:
            has_anchor = False
            for anchor in PI02_ANCHORS:
                if re.search(anchor, body, re.I):
                    has_anchor = True
                    break
            if not has_anchor:
                add('A3', 'PI-02', 'high', f,
                    'Agent body contains no non-negotiable refusal constraints '
                    '(missing "must not"/"will not"/"never" + action, "refuse" + trigger, or "out of scope")')

        # PI-05: Exfiltration via URL construction
        url_patterns = [
            (r'\$\{[^}]*\}', 'Template variable in URL context'),
            (r'\{\{[^}]*\}\}', 'Handlebars variable in URL context'),
        ]
        for pat, desc in url_patterns:
            for m in re.finditer(pat, body_no_code):
                surrounding = body_no_code[max(0,m.start()-50):m.end()+50]
                if re.search(r'https?://', surrounding, re.I):
                    add('A3', 'PI-05', 'high', f, f'{desc}: {m.group()}')

        # PI-06: Indirect injection vectors
        if not is_detection_skill:
            for m in re.finditer(INDIRECT_INJECTION, body_no_code, re.I):
                # Skip if in defensive context ("do not", "refuse", "reject", "ignore")
                start = max(0, m.start() - 80)
                surrounding = body_no_code[start:m.end()+40].lower()
                if any(kw in surrounding for kw in [
                    'do not', 'must not', 'never', 'refuse', 'reject', 'ignore',
                    'discard', 'treat all', 'inert data',
                ]):
                    continue
                add('A3', 'PI-06', 'critical', f, f'Indirect injection vector: "{m.group()}"')

    # PI-04: Unconstrained tool scope (duplicate of A1 P-03/P-04)
    for f in all_agents:
        content = f.read_text(encoding='utf-8')
        fm = extract_frontmatter(content)
        m = re.search(r"tools:\s*\[([^\]]*)\]", fm)
        if m:
            tools_str = m.group(1)
            if "'*'" in tools_str or '"*"' in tools_str or "'all'" in tools_str or '"all"' in tools_str:
                add('A3', 'PI-04', 'critical', f, 'tools: ["*"] or ["all"] — unconstrained tool scope')
            if 'runCommands' in fm and not re.search(r'^commandAllowlist:', fm, re.M):
                add('A3', 'PI-04', 'high', f, 'runCommands without commandAllowlist (prompt-sec layer)')
            if ("'fetch'" in fm or '"fetch"' in fm) and not re.search(r'^allowedNetworkDomains:', fm, re.M):
                add('A3', 'PI-04', 'high', f, 'fetch without allowedNetworkDomains (prompt-sec layer)')


# ══════════════════════════════════════════════════════════════
# A5 — Sandbox Simulation (basic deterministic assessment)
# ══════════════════════════════════════════════════════════════
def check_a5_basic():
    """Check that agent definitions contain basic defensive constraints."""
    for f in projected_agents + provider_agents:
        try:
            content = f.read_text(encoding='utf-8')
        except (UnicodeDecodeError, PermissionError):
            continue

        body = extract_body(content)
        fm = extract_frontmatter(content)
        body_lower = body.lower()

        # 4-A: Does agent forbid contacting arbitrary external addresses?
        has_fetch = "'fetch'" in fm or '"fetch"' in fm
        if has_fetch:
            if not re.search(r'allowedNetworkDomains:', fm, re.I):
                add('A5', '4-A', 'high', f, 'Agent has fetch but no allowedNetworkDomains — exfiltration risk')

        # 4-D: Does agent explicitly refuse to read credential files?
        has_cred_refusal = any(kw in body_lower for kw in [
            '.env', 'credential', 'secret', '.pem', '.key', '.aws', '.ssh'
        ])
        if not has_cred_refusal:
            if 'codebase' in fm or 'edit/editFiles' in fm:
                add('A5', '4-D', 'medium', f,
                    'Agent has file access tools but no explicit mention of credential file restrictions')


# ══════════════════════════════════════════════════════════════
# Run all checks
# ══════════════════════════════════════════════════════════════
check_a1()
check_a2()
check_a3()
check_a5_basic()


# ══════════════════════════════════════════════════════════════
# Report
# ══════════════════════════════════════════════════════════════
blocking = [f for f in findings if f['severity'] in ('critical', 'high')]
warnings = [f for f in findings if f['severity'] in ('medium', 'low')]

# Group by station
by_station = defaultdict(list)
for f in findings:
    by_station[f['station']].append(f)

stations = ['A1', 'A2', 'A3', 'A5']
print('=' * 60)
print('  LOCAL CI SIMULATION RESULTS')
print('=' * 60)

for s in stations:
    sf = by_station.get(s, [])
    s_blocking = [f for f in sf if f['severity'] in ('critical', 'high')]
    status = 'FAIL' if s_blocking else 'PASS'
    icon = '❌' if s_blocking else '✅'
    print(f'\n{icon} {s}: {status}')
    if sf:
        for f in sf:
            sev_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵'}.get(f['severity'], '⚪')
            print(f'   {sev_icon} [{f["check"]}] {f["severity"]:8s} {f["file"]}')
            print(f'     {f["message"]}')

# A6 gate simulation
print(f'\n{"=" * 60}')
has_critical = any(f['severity'] == 'critical' for f in findings)
has_high = any(f['severity'] == 'high' for f in findings)
if has_critical or has_high:
    print('🚫 A6 GATE DECISION: BLOCK')
    print(f'   {len(blocking)} blocking finding(s)')
elif warnings:
    print('⚠️  A6 GATE DECISION: APPROVE (with warnings)')
    print(f'   {len(warnings)} warning(s)')
else:
    print('✅ A6 GATE DECISION: APPROVE')

print(f'\nTotal: {len(findings)} findings '
      f'({sum(1 for f in findings if f["severity"]=="critical")} critical, '
      f'{sum(1 for f in findings if f["severity"]=="high")} high, '
      f'{sum(1 for f in findings if f["severity"]=="medium")} medium, '
      f'{sum(1 for f in findings if f["severity"]=="low")} low)')

# Write JSON report
report_path = root / 'reports' / 'local-ci-simulation.json'
report_path.parent.mkdir(exist_ok=True)
report = {
    'stations': {},
    'gate_decision': 'BLOCK' if blocking else 'APPROVE',
    'total_findings': len(findings),
    'blocking_findings': len(blocking),
}
for s in stations:
    sf = by_station.get(s, [])
    s_blocking = [f for f in sf if f['severity'] in ('critical', 'high')]
    report['stations'][s] = {
        'status': 'fail' if s_blocking else 'pass',
        'findings': sf,
    }
report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(f'\nReport written to: {report_path.relative_to(root)}')

sys.exit(1 if blocking else 0)
