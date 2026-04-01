#!/usr/bin/env python3
"""Validate GitHub Copilot two-layer architecture:
  Layer 1: .apm/ (canonical definitions — agents, skills, prompts, templates, workflows)
  Layer 2: providers/github-copilot/ (adapter docs: conventions.md, sync-map.md)
  Layer 3: .github/ (runtime projection: agents, prompts, instructions)
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
APM = ROOT / '.apm'
ADAPTER = ROOT / 'providers' / 'github-copilot'
RUNTIME = ROOT / '.github'

errors = []
warnings = []

# --- Canonical layer: must have agents, prompts, skills, templates ---
for subdir in ['agents', 'skills', 'prompts', 'templates']:
    d = APM / subdir
    if not d.is_dir() or not any(d.iterdir()):
        errors.append(f'Missing or empty canonical directory: .apm/{subdir}/')

# --- Canonical agents must be projected to .github/agents/ ---
if (APM / 'agents').is_dir() and (RUNTIME / 'agents').is_dir():
    canonical_agents = {p.stem for p in (APM / 'agents').glob('*.md')}
    runtime_agents = {p.stem.replace('.agent', '') for p in (RUNTIME / 'agents').glob('*.agent.md')}
    missing = canonical_agents - runtime_agents
    for a in missing:
        warnings.append(f'Canonical agent without runtime projection: {a}')

# --- Canonical prompts must be projected to .github/prompts/ ---
if (APM / 'prompts').is_dir() and (RUNTIME / 'prompts').is_dir():
    canonical_prompts = {p.stem for p in (APM / 'prompts').glob('*.md')}
    runtime_prompts = {p.stem.replace('.prompt', '') for p in (RUNTIME / 'prompts').glob('*.prompt.md')}
    missing = canonical_prompts - runtime_prompts
    for p in missing:
        warnings.append(f'Prompt not projected to .github/: {p}')

# --- Runtime agents must have a canonical counterpart ---
if (APM / 'agents').is_dir() and (RUNTIME / 'agents').is_dir():
    canonical_agents = {p.stem for p in (APM / 'agents').glob('*.md')}
    runtime_agents = {p.stem.replace('.agent', '') for p in (RUNTIME / 'agents').glob('*.agent.md')}
    orphaned = runtime_agents - canonical_agents
    for a in orphaned:
        errors.append(f'Runtime agent without canonical definition: {a}')

# --- Layer 2: Adapter must have conventions.md + sync-map.md ---
for doc in ['conventions.md', 'sync-map.md']:
    if not (ADAPTER / doc).exists():
        errors.append(f'Missing adapter doc: providers/github-copilot/{doc}')

# --- Layer 2: Adapter must NOT contain runtime files ---
for bad_dir in ['agents', 'prompts', 'instructions']:
    bad_path = ADAPTER / bad_dir
    if bad_path.is_dir() and any(bad_path.iterdir()):
        errors.append(f'Runtime files in adapter layer: providers/github-copilot/{bad_dir}/ (move to .github/{bad_dir}/)')
if (ADAPTER / 'copilot-instructions.md').exists():
    errors.append('Runtime file in adapter layer: providers/github-copilot/copilot-instructions.md (move to .github/)')

# --- Layer 3: Required runtime structure ---
required_dirs = [
    RUNTIME / 'agents',
    RUNTIME / 'prompts',
    RUNTIME / 'instructions',
]
for d in required_dirs:
    if not d.is_dir():
        errors.append(f'Missing runtime directory: {d.relative_to(ROOT)}')

# --- Layer 3: copilot-instructions.md ---
if not (RUNTIME / 'copilot-instructions.md').exists():
    errors.append('Missing .github/copilot-instructions.md')

# --- Sync check: canonical workflows → runtime workflow prompts ---
if (APM / 'workflows').is_dir() and (RUNTIME / 'prompts').is_dir():
    canonical_workflows = {p.stem for p in (APM / 'workflows').glob('*.yml')}
    workflow_prompts = {p.stem.replace('workflow-', '').replace('.prompt', '')
                       for p in (RUNTIME / 'prompts').glob('workflow-*.prompt.md')}

    for wf in canonical_workflows:
        # Check if a workflow prompt exists (exact or fuzzy match)
        if not any(wf in wp or wp in wf for wp in workflow_prompts):
            warnings.append(f'Workflow without runtime prompt: {wf}')

# --- Instruction files must have applyTo frontmatter ---
if (RUNTIME / 'instructions').is_dir():
    for instr in (RUNTIME / 'instructions').glob('*.instructions.md'):
        content = instr.read_text(encoding='utf-8')
        if 'applyTo:' not in content:
            errors.append(f'Instruction missing applyTo frontmatter: {instr.name}')

# --- Report ---
if errors:
    print(f'Copilot validation FAILED ({len(errors)} errors, {len(warnings)} warnings):')
    for e in errors:
        print(f'  ERROR: {e}')
    for w in warnings:
        print(f'  WARN:  {w}')
    sys.exit(1)

print(f'Copilot validation PASSED ({len(warnings)} warnings)')
for w in warnings:
    print(f'  WARN: {w}')
