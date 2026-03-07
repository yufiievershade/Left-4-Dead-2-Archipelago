"""Configuration and data for L4D2 Archipelago Companion.

This module contains BaseSettings classes for configuration.
All constants are defined in definitions.py to avoid circular imports.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# ============================================================================
# PYDANTIC SETTINGS CLASSES
# ============================================================================

class GameConfig(BaseSettings):
    """Game-related configuration constants with environment variable support.

    Environment variables:
        L4D2_MOD_DATA_DIR: Directory for mod data files (default: mod_data)
        L4D2_STATUS_FILE: Status file name (default: ap_status.txt)
        L4D2_EVENTS_FILE: Events file name (default: ap_events.txt)
        L4D2_OUTGOING_FILE: Outgoing commands file (default: outgoing.log)
        L4D2_ERROR_LOG: Error log file name (default: error.log)
        L4D2_INSTALLATION_PATH: Path to L4D2 installation (REQUIRED)
    """

    model_config = SettingsConfigDict(
        env_prefix="L4D2_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # File paths with inline defaults (can be overridden via environment variables)
    mod_data_dir: str = Field(default="mod_data", description="Directory for mod data files")
    status_file: str = Field(default="ap_status.txt", description="Connection status file")
    events_file: str = Field(default="ap_events.txt", description="Game events file")
    outgoing_file: str = Field(default="outgoing.log", description="Outgoing commands log")
    error_log: str = Field(default="error.log", description="Error log file")

    # L4D2 installation path (REQUIRED - no auto-detection)
    installation_path: Path = Field(
        description="Path to Left 4 Dead 2 installation (e.g., C:\\Program Files (x86)\\Steam\\steamapps\\common\\Left 4 Dead 2)"
    )

    @property
    def mod_data_path(self) -> Path:
        """Get the full path to the mod_data directory."""
        return self.installation_path / self.mod_data_dir


class APConfig(BaseSettings):
    """Archipelago protocol configuration with environment variable support.
    """

    model_config = SettingsConfigDict(
        env_prefix="AP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Server configuration from environment (default can be overridden via AP_HOST)
    host: str = Field(default="archipelago.gg:38281", description="Default server address")
    debug: bool = Field(default=False, description="Enable debug logging")

    # Protocol version (used for WebSocket handshake)
    version_major: int = Field(default=0, description="Protocol version major")
    version_minor: int = Field(default=6, description="Protocol version minor")
    version_build: int = Field(default=3, description="Protocol version build")

    # WebSocket protocol configuration
    ws_protocol: str = Field(default="wss://", description="Primary WebSocket protocol")
    ws_fallback: str = Field(default="ws://", description="Fallback WebSocket protocol")

    # Connection constants
    tag: str = Field(default="AP", description="Connection tag for packets")
    items_handling: int = Field(default=0b111, description="Items handling flags (0b111 = all)")


# Create singleton instances for easy import
game_config = GameConfig()
ap_config = APConfig()
