#!/usr/bin/env python3
"""Run all validation scripts and produce a summary report."""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

validators = [
    ('Core Assets', SCRIPTS_DIR / 'validate_core_assets.py'),
    ('Copilot Projection', SCRIPTS_DIR / 'validate_copilot_assets.py'),
    ('Claude Adapter', SCRIPTS_DIR / 'validate_claude_assets.py'),
]

results = []

for name, script in validators:
    print(f'\n--- {name} ---')
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=False,
    )
    results.append((name, result.returncode == 0))

print('\n=== Summary ===')
all_passed = True
for name, passed in results:
    status = 'PASS' if passed else 'FAIL'
    print(f'  [{status}] {name}')
    if not passed:
        all_passed = False

sys.exit(0 if all_passed else 1)
