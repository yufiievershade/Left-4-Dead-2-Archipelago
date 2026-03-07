"""Path utilities for L4D2 Archipelago Companion.
"""
import sys
from pathlib import Path

from l4d2_companion.config import game_config


def get_resource_path(relative_path: str) -> Path:
    """Get absolute path to resource, works for dev and for PyInstaller.

    In PyInstaller builds, resources are stored in sys._MEIPASS.
    In development, resources are relative to the current directory.

    Args:
        relative_path: Path relative to the application root

    Returns:
        Absolute Path object
    """
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path.cwd()

    return base_path / relative_path


def ensure_mod_data_directory() -> Path:
    """Ensure the mod_data directory exists.

    Returns:
        Path to the mod_data directory from game configuration
    """
    mod_data_path = game_config.mod_data_path
    mod_data_path.mkdir(parents=True, exist_ok=True)
    return mod_data_path
