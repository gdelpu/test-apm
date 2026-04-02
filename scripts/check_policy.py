#!/usr/bin/env python3
"""Quick A1 policy pre-check for agents and skills."""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parents[1]
fails = []

# Agents: P-01, P-03, P-04, P-05
for f in sorted(root.glob('.apm/agents/*.md')):
    c = f.read_text(encoding='utf-8')
    if not c.startswith('---'):
        fails.append(f'P-01 {f.name}: NO FRONTMATTER')
        continue
    if not re.search(r'^name:', c, re.M):
        fails.append(f'P-01 {f.name}: missing name')
    if not re.search(r'^description:', c, re.M):
        fails.append(f'P-01 {f.name}: missing description')
    if not re.search(r'^tools:', c, re.M):
        fails.append(f'P-01 {f.name}: missing tools')
    # Extract frontmatter only for tool checks
    fm_match = re.match(r'^---\n(.*?)\n---', c, re.S)
    fm = fm_match.group(1) if fm_match else ''
    if 'runCommands' in fm and not re.search(r'^commandAllowlist:', fm, re.M):
        fails.append(f'P-03 {f.name}: runCommands without commandAllowlist')
    if "'fetch'" in fm and not re.search(r'^allowedNetworkDomains:', fm, re.M):
        fails.append(f'P-04 {f.name}: fetch without allowedNetworkDomains')
    m = re.search(r"description:\s*'([^']*)'", c)
    if m and len(m.group(1)) < 20:
        fails.append(f'P-05 {f.name}: description too short ({len(m.group(1))} chars)')

# Skills: P-01
for f in sorted(root.glob('.apm/skills/*/SKILL.md')):
    c = f.read_text(encoding='utf-8')
    if not c.startswith('---'):
        fails.append(f'P-01 {f.parent.name}/SKILL.md: NO FRONTMATTER')
        continue
    if not re.search(r'^name:', c, re.M):
        fails.append(f'P-01 {f.parent.name}/SKILL.md: missing name')
    if not re.search(r'^description:', c, re.M):
        fails.append(f'P-01 {f.parent.name}/SKILL.md: missing description')
    if not re.search(r'^triggers:', c, re.M):
        fails.append(f'P-01 {f.parent.name}/SKILL.md: missing triggers')

# Tool allowlist check (P-02)
allowed = {'codebase','search','edit/editFiles','problems','runCommands','github','terminal','fetch','vscode'}
for f in sorted(root.glob('.apm/agents/*.md')):
    c = f.read_text(encoding='utf-8')
    m = re.search(r"tools:\s*\[([^\]]*)\]", c)
    if m:
        tools = [t.strip().strip("'\"") for t in m.group(1).split(',') if t.strip()]
        for t in tools:
            if t not in allowed:
                fails.append(f'P-02 {f.name}: unknown tool "{t}"')

if fails:
    print(f'FAILURES: {len(fails)}')
    for x in fails:
        print(f'  {x}')
    sys.exit(1)
else:
    agents = len(list(root.glob('.apm/agents/*.md')))
    skills = len(list(root.glob('.apm/skills/*/SKILL.md')))
    print(f'ALL PASS: {agents} agents, {skills} skills checked')
    sys.exit(0)
