"""Configuration management for the Project Booster CLI."""

import json
import os
from pathlib import Path
from dataclasses import dataclass, field

CONFIG_FILENAME = ".project-booster.json"

DEFAULT_BASE_URL = "https://project-booster.dep.soprasteria.com"


@dataclass
class BoosterConfig:
    """Holds the Project Booster connection configuration."""

    base_url: str
    token: str
    ssl_verify: bool = True

    @property
    def api_url(self) -> str:
        return self.base_url.rstrip("/") + "/api"

    def __post_init__(self) -> None:
        if not self.token:
            raise ValueError("Token must not be empty")
        if not self.base_url:
            raise ValueError("Base URL must not be empty")


def _find_config_file() -> Path | None:
    """Walk upward from CWD looking for .project-booster.json."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        candidate = parent / CONFIG_FILENAME
        if candidate.is_file():
            return candidate
    # Also check user home
    home = Path.home() / CONFIG_FILENAME
    if home.is_file():
        return home
    return None


def load_config(config_path: str | None = None) -> BoosterConfig:
    """Load config from file, falling back to env vars.

    Resolution order:
      1. Explicit --config path
      2. .project-booster.json in CWD or parents
      3. ~/.project-booster.json
      4. Environment variables PROJECT_BOOSTER_URL / PROJECT_BOOSTER_TOKEN
    """
    if config_path:
        path = Path(config_path)
    else:
        path = _find_config_file()

    if path and path.is_file():
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return BoosterConfig(
            base_url=data.get("base_url", DEFAULT_BASE_URL),
            token=data["token"],
            ssl_verify=data.get("ssl_verify", True),
        )

    # Fallback to env vars
    token = os.environ.get("PROJECT_BOOSTER_TOKEN", "")
    if not token:
        raise SystemExit(
            f"No config file ({CONFIG_FILENAME}) found and PROJECT_BOOSTER_TOKEN "
            "environment variable is not set.\n"
            f"Run: project-booster init\n"
            f"  or create {CONFIG_FILENAME} with:\n"
            '  {"base_url": "https://...", "token": "glpat-..."}'
        )
    return BoosterConfig(
        base_url=os.environ.get("PROJECT_BOOSTER_URL", DEFAULT_BASE_URL),
        token=token,
        ssl_verify=os.environ.get("PROJECT_BOOSTER_SSL_VERIFY", "true").lower()
        == "true",
    )


def init_config(base_url: str, token: str, ssl_verify: bool = True) -> Path:
    """Write a new .project-booster.json in the current directory."""
    path = Path.cwd() / CONFIG_FILENAME
    data = {"base_url": base_url, "token": token, "ssl_verify": ssl_verify}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    # Restrict file permissions (owner-only read/write) on Unix
    try:
        path.chmod(0o600)
    except OSError:
        pass  # Windows doesn't support Unix permissions
    return path
