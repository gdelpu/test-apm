#!/usr/bin/env python3
"""Validate Claude Code provider adapter matches canonical .apm/ layer."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
APM = ROOT / '.apm'
CLAUDE = ROOT / 'providers' / 'claude-code'

errors = []
warnings = []

# --- Required Claude structure ---
if not (CLAUDE / 'CLAUDE.md').exists():
    errors.append('Missing providers/claude-code/CLAUDE.md')

if not (CLAUDE / 'commands').is_dir():
    errors.append('Missing directory: providers/claude-code/commands/')

# --- Workflow command check: at least one command per workflow is expected ---
if (APM / 'workflows').is_dir() and (CLAUDE / 'commands').is_dir():
    workflows = [p.stem for p in (APM / 'workflows').glob('*.yml')]
    commands = [p.stem for p in (CLAUDE / 'commands').glob('workflow-*.md')]
    if workflows and not commands:
        warnings.append('No Claude workflow commands found')

# --- Report ---
if errors:
    print(f'Claude validation FAILED ({len(errors)} errors, {len(warnings)} warnings):')
    for e in errors:
        print(f'  ERROR: {e}')
    for w in warnings:
        print(f'  WARN:  {w}')
    sys.exit(1)

print(f'Claude validation PASSED ({len(warnings)} warnings)')
for w in warnings:
    print(f'  WARN: {w}')
