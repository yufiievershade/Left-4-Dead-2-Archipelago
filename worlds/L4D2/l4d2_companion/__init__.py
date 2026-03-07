"""L4D2 Archipelago Companion Application.

A Pythonic client application that bridges Left 4 Dead 2 with Archipelago multiworld servers.
"""

# Package metadata
__version__ = "1.0.0"
__author__ = "Yufii"

# ============================================================================
# MODULE IMPORTS
# ============================================================================

# Definitions module exports (enums and constants - single source of truth)
# Client module exports
from l4d2_companion.client import (
    ArchipelagoPacket,
    ConnectionState,
    ConnectPacket,
    L4D2ArchipelagoClient,
    LocationCheckPacket,
    ReceivedItem,
    ServerConnectedPacket,
    ServerReceivedItemsPacket,
)

# Config module exports (settings classes)
from l4d2_companion.config import (
    APConfig,
    GameConfig,
    ap_config,
    game_config,
)
from l4d2_companion.definitions import (
    CAMPAIGN_NAMES,
    CAMPAIGNS,
    CHARACTERS_L4D1,
    CHARACTERS_L4D2,
    ITEM_SPAWN_COMMANDS,
    STARTER_ITEM_POOLS,
    TRAP_SPAWN_COMMANDS,
    ItemType,
    LocationType,
    TrapType,
)

# GUI module exports
from l4d2_companion.gui import (
    ConnectionInfo,
    L4D2CompanionGUI,
    ThemeConfiguration,
    WindowConfiguration,
)

# Models module exports (Pydantic BaseModels)
from l4d2_companion.models import (
    CAMPAIGN_MODELS,
    ITEM_MODELS,
    STARTER_POOL_MODELS,
    TRAP_MODELS,
    Campaign,
    ItemDefinition,
    Location,
    StarterItemPool,
    TrapSpawn,
)

# Files module exports
from l4d2_companion.files import FileOperationResult

# Paths module exports
from l4d2_companion.paths import get_resource_path

__all__ = [
    # Package metadata
    "__version__",
    "__author__",
    # Data constants (from definitions)
    "CAMPAIGNS",
    "CAMPAIGN_NAMES",
    "CHARACTERS_L4D1",
    "CHARACTERS_L4D2",
    "ITEM_SPAWN_COMMANDS",
    "TRAP_SPAWN_COMMANDS",
    "STARTER_ITEM_POOLS",
    # Enums (from definitions)
    "LocationType",
    "ItemType",
    "TrapType",
    # Configuration classes (protocol settings via ap_config)
    "GameConfig",
    "APConfig",
    "game_config",
    "ap_config",
    # Pydantic models
    "Campaign",
    "ItemDefinition",
    "StarterItemPool",
    "TrapSpawn",
    "Location",
    "CAMPAIGN_MODELS",
    "ITEM_MODELS",
    "STARTER_POOL_MODELS",
    "TRAP_MODELS",
    # Client
    "L4D2ArchipelagoClient",
    "ConnectionState",
    "ArchipelagoPacket",
    "ConnectPacket",
    "LocationCheckPacket",
    "ReceivedItem",
    "ServerConnectedPacket",
    "ServerReceivedItemsPacket",
    # GUI
    "L4D2CompanionGUI",
    "ThemeConfiguration",
    "WindowConfiguration",
    "ConnectionInfo",
    # Files
    "FileOperationResult",
    # Paths
    "get_resource_path",
]
