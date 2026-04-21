#!/usr/bin/env python3
"""Install APM git hooks into the local .git/hooks directory.

Usage:
    python scripts/hooks/setup-hooks.py

Copies hook scripts from scripts/hooks/ into .git/hooks/, preserving any
existing hooks by appending rather than overwriting. Safe to run repeatedly.
"""

import os
import shutil
import stat
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
HOOKS_SRC = REPO_ROOT / "scripts" / "hooks"
GIT_HOOKS = REPO_ROOT / ".git" / "hooks"

# Hooks we manage (filename must match the git hook name)
MANAGED_HOOKS = ["pre-commit"]

MARKER = "# --- APM managed hook ---"


def install_hook(hook_name: str) -> None:
    src = HOOKS_SRC / hook_name
    dest = GIT_HOOKS / hook_name

    if not src.is_file():
        print(f"  skip {hook_name} (source not found)")
        return

    src_content = src.read_text(encoding="utf-8")

    if dest.is_file():
        existing = dest.read_text(encoding="utf-8")
        if MARKER in existing:
            # Replace the managed block
            before = existing.split(MARKER)[0]
            dest.write_text(
                before.rstrip() + "\n\n" + MARKER + "\n" + src_content + "\n",
                encoding="utf-8",
            )
            print(f"  updated {hook_name}")
        else:
            # Append to existing hook
            dest.write_text(
                existing.rstrip() + "\n\n" + MARKER + "\n" + src_content + "\n",
                encoding="utf-8",
            )
            print(f"  appended to existing {hook_name}")
    else:
        dest.write_text(
            "#!/usr/bin/env bash\n" + MARKER + "\n" + src_content + "\n",
            encoding="utf-8",
        )
        print(f"  created {hook_name}")

    # Make executable (Unix)
    if os.name != "nt":
        dest.chmod(dest.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def main() -> int:
    if not GIT_HOOKS.parent.is_dir():
        print("Error: .git directory not found. Run from the repo root.", file=sys.stderr)
        return 1

    GIT_HOOKS.mkdir(exist_ok=True)
    print("Installing APM git hooks...")

    for hook_name in MANAGED_HOOKS:
        install_hook(hook_name)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
