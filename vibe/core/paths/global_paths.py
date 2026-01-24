from __future__ import annotations

from collections.abc import Callable
import os
from pathlib import Path

from vibe import VIBE_ROOT


class GlobalPath:
    def __init__(self, resolver: Callable[[], Path]) -> None:
        self._resolver = resolver

    @property
    def path(self) -> Path:
        return self._resolver()


_DEFAULT_GLAUDE_HOME = Path.home() / ".glaude"


def _get_glaude_home() -> Path:
    if glaude_home := os.getenv("GLAUDE_HOME"):
        return Path(glaude_home).expanduser().resolve()
    if vibe_home := os.getenv("VIBE_HOME"):
        return Path(vibe_home).expanduser().resolve()
    return _DEFAULT_GLAUDE_HOME


GLAUDE_HOME = GlobalPath(_get_glaude_home)


VIBE_HOME = GlobalPath(_get_glaude_home)
GLOBAL_CONFIG_FILE = GlobalPath(lambda: GLAUDE_HOME.path / "config.toml")
GLOBAL_ENV_FILE = GlobalPath(lambda: GLAUDE_HOME.path / ".env")
GLOBAL_TOOLS_DIR = GlobalPath(lambda: GLAUDE_HOME.path / "tools")
GLOBAL_SKILLS_DIR = GlobalPath(lambda: GLAUDE_HOME.path / "skills")
SESSION_LOG_DIR = GlobalPath(lambda: GLAUDE_HOME.path / "logs" / "session")
TRUSTED_FOLDERS_FILE = GlobalPath(lambda: GLAUDE_HOME.path / "trusted_folders.toml")
LOG_DIR = GlobalPath(lambda: GLAUDE_HOME.path / "logs")
LOG_FILE = GlobalPath(lambda: GLAUDE_HOME.path / "glaude.log")

DEFAULT_TOOL_DIR = GlobalPath(lambda: VIBE_ROOT / "core" / "tools" / "builtins")
