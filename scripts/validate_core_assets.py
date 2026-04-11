#!/usr/bin/env python3
"""Validate canonical .apm/ layer — agents, skills, prompts, workflows, instructions exist."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
APM = ROOT / '.apm'

errors = []

# --- Required structure ---
required_dirs = [
    APM / 'agents',
    APM / 'skills',
    APM / 'prompts',
    APM / 'instructions',
    APM / 'contexts',
    APM / 'workflows',
    APM / 'templates',
]
for d in required_dirs:
    if not d.is_dir():
        errors.append(f'Missing directory: {d.relative_to(ROOT)}')

# --- apm.yml ---
if not (ROOT / 'apm.yml').exists():
    errors.append('Missing apm.yml manifest')

# --- At least one agent ---
agents = list((APM / 'agents').glob('*.md')) if (APM / 'agents').is_dir() else []
if not agents:
    errors.append('No agents found in .apm/agents/')

# --- At least one skill with SKILL.md ---
skills_dir = APM / 'skills'
if skills_dir.is_dir():
    skills = [d for d in skills_dir.iterdir() if d.is_dir() and (d / 'SKILL.md').exists()]
    if not skills:
        errors.append('No skills with SKILL.md found in .apm/skills/')
else:
    skills = []

# --- At least one workflow ---
workflows_dir = APM / 'workflows'
if workflows_dir.is_dir():
    workflows = list(workflows_dir.glob('*.yml'))
    if not workflows:
        errors.append('No workflow .yml files found in .apm/workflows/')
    if not (workflows_dir / '_schema.md').exists():
        errors.append('Missing .apm/workflows/_schema.md')
else:
    workflows = []

# --- At least one prompt ---
prompts = list((APM / 'prompts').glob('*.md')) if (APM / 'prompts').is_dir() else []
if not prompts:
    errors.append('No prompts found in .apm/prompts/')

# --- Knowledge base ---
knowledge = ROOT / '.apm' / 'knowledge'
for subdir in ['constitution', 'governance', 'playbooks']:
    kb_dir = knowledge / subdir
    if not kb_dir.is_dir():
        errors.append(f'Missing knowledge directory: .apm/knowledge/{subdir}/')
    elif not list(kb_dir.glob('*.md')):
        errors.append(f'Empty knowledge directory: .apm/knowledge/{subdir}/')

# --- Report ---
if errors:
    print(f'Core assets validation FAILED ({len(errors)} issues):')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)

print(f'Core assets validation PASSED')
print(f'  Agents: {len(agents)}')
print(f'  Skills: {len(skills)}')
print(f'  Workflows: {len(workflows)}')
print(f'  Prompts: {len(prompts)}')
