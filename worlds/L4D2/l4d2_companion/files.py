"""File I/O operations for L4D2 Archipelago Companion.
"""
from pathlib import Path

from l4d2_companion.config import game_config
from pydantic import BaseModel


class FileOperationResult(BaseModel):
    """Result of a file operation."""

    success: bool
    path: Path | None = None
    content: str | None = None
    error: str | None = None


def write_status_file(player_name: str, connected: bool) -> FileOperationResult:
    """Write current connection status to status file.

    Args:
        player_name: Player's slot name
        connected: Whether currently connected to server

    Returns:
        FileOperationResult with success status
    """
    status_file = game_config.mod_data_path / game_config.status_file
    try:
        content = f"connected:{connected}\nplayer:{player_name}\n"
        status_file.write_text(content, encoding="utf-8")
        return FileOperationResult(success=True, path=status_file, content=content)
    except OSError as e:
        error_msg = f"Failed to write status file: {e}"
        print(error_msg)
        return FileOperationResult(success=False, path=status_file, error=error_msg)


def read_events_file() -> FileOperationResult:
    """Read contents of the events file.

    Returns:
        FileOperationResult with content or error
    """
    events_file = game_config.mod_data_path / game_config.events_file
    try:
        content = events_file.read_text(encoding="utf-8")
        return FileOperationResult(success=True, path=events_file, content=content)
    except FileNotFoundError:
        return FileOperationResult(success=True, path=events_file, content="")
    except OSError as e:
        error_msg = f"Failed to read events file: {e}"
        print(error_msg)
        return FileOperationResult(success=False, path=events_file, error=error_msg)


def clear_events_file() -> FileOperationResult:
    """Clear the events file by truncating it.

    Returns:
        FileOperationResult with success status
    """
    events_file = game_config.mod_data_path / game_config.events_file
    try:
        events_file.write_text("", encoding="utf-8")
        return FileOperationResult(success=True, path=events_file, content="")
    except OSError as e:
        error_msg = f"Failed to clear events file: {e}"
        print(error_msg)
        return FileOperationResult(success=False, path=events_file, error=error_msg)
