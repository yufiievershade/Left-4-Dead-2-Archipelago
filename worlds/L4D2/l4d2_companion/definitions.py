"""Definitions and constants for L4D2 Archipelago Companion.

This module contains all enums, constants, and data definitions used throughout
the application. This is the single source of truth for all constant values
to avoid circular import issues.
"""

from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================

class LocationType(str, Enum):
    """Types of locations in the game."""

    SAFE_ROOM = "Safe Room"
    FINALE = "Finale"
    EVENT = "Event"
    COLLECTIBLE = "Collectible"
    BOSS = "Boss"


class ItemType(str, Enum):
    """Types of items that can be received."""

    WEAPON = "weapon"
    MEDICAL = "medical"
    THROWABLE = "throwable"
    MELEE = "melee"
    SCAVENGE = "scavenge"
    TRAP = "trap"
    JUNK = "junk"
    CAMPAIGN = "campaign"


class TrapType(str, Enum):
    """Types of traps (special infected)."""

    BOOMER = "Boomer"
    HUNTER = "Hunter"
    SMOKER = "Smoker"
    TANK = "Tank"
    WITCH = "Witch"
    CHARGER = "Charger"
    JOCKEY = "Jockey"
    SPITTER = "Spitter"


# ============================================================================
# GAME DATA CONSTANTS
# ============================================================================

# Campaign definitions: (name, num_safe_rooms, finale_map, is_l4d1)
CAMPAIGNS: list[tuple[str, int, str, bool]] = [
    ("Dead Center", 3, "c1m4_atrium", False),
    ("The Passing", 2, "c6m3_port", False),
    ("Dark Carnival", 4, "c2m5_concert", False),
    ("Swamp Fever", 3, "c3m4_plantation", False),
    ("Hard Rain", 4, "c4m5_milltown_escape", False),
    ("The Parish", 4, "c5m5_bridge", False),
    ("Cold Stream", 3, "c13m4_cutthroatcreek", False),
    ("The Sacrifice", 3, "c7m3_port", True),
    ("No Mercy", 4, "c8m5_rooftop", True),
    ("Crash Course", 1, "c9m2_alleys", True),
    ("Death Toll", 4, "c10m5_houseboat", True),
    ("Dead Air", 4, "c11m5_runway", True),
    ("Blood Harvest", 4, "c12m5_cornfield", True),
    ("The Last Stand", 2, "c14m2_lighthouse", True),
]

# Campaign names for quick reference
CAMPAIGN_NAMES: list[str] = [name for name, _, _, _ in CAMPAIGNS]

# Character sets for location generation
CHARACTERS_L4D1: list[str] = ["Bill", "Zoey", "Louis", "Francis"]
CHARACTERS_L4D2: list[str] = ["Coach", "Rochelle", "Ellis", "Nick"]


# ============================================================================
# ITEM CONSTANTS
# ============================================================================

# Item spawn command mappings
ITEM_SPAWN_COMMANDS: dict[str, str] = {
    # Weapons - Primary
    "Pump Shotgun": "give pumpshotgun",
    "Chrome Shotgun": "give shotgun_chrome",
    "Submachine Gun": "give smg",
    "Silenced Submachine Gun": "give smg_silenced",
    "MP5": "give smg_mp5",
    "Tactical Shotgun": "give autoshotgun",
    "Combat Shotgun": "give shotgun_spas",
    "Hunting Rifle": "give hunting_rifle",
    "Sniper Rifle": "give sniper_military",
    "M-16": "give rifle",
    "Scar-H": "give rifle_desert",
    "AK-47": "give rifle_ak47",
    "SG 552": "give rifle_sg552",
    "Grenade Launcher": "give weapon_grenade_launcher",
    "M60": "give weapon_rifle_m60",
    # Weapons - Secondary
    "P220 Pistol": "give pistol",
    "Magnum": "give pistol_magnum",
    "Glock": "give pistol_magnum",  # Map Glock to magnum (it's a junk item)
    # Medical
    "First Aid Kit": "give first_aid_kit",
    "Defib": "give defibrillator",
    "Pills": "give pain_pills",
    "Adrenaline": "give adrenaline",
    # Throwables
    "Molotov": "give molotov",
    "Pipe Bomb": "give pipe_bomb",
    "Bile Bomb": "give vomitjar",
    # Upgrades
    "Laser Sight": "give upgrade_laser_sight",
    "Incendiary": "give upgradepack_incendiary",
    "Explosive Ammo": "give upgradepack_explosive",
    # Melee weapons
    "Fireaxe": "give fireaxe",
    "Baseball Bat": "give baseball_bat",
    "Cricket Bat": "give cricket_bat",
    "Crowbar": "give crowbar",
    "Frying Pan": "give frying_pan",
    "Golf Club": "give golfclub",
    "Guitar": "give electric_guitar",
    "Katana": "give katana",
    "Machete": "give machete",
    "Nightstick": "give tonfa",
    "Pitchfork": "give pitchfork",
    "Shovel": "give shovel",
    "Knife": "give knife",
    "Chainsaw": "give chainsaw",
    "Riot Shield": "give riotshield",
    # Scavenge items
    "Gas Can": "give gascan",
    "Oxygen Tank": "give oxygentank",
    "Propane Tank": "give propanetank",
    "Fireworks": "give fireworkcrate",
    # Special
    "Gnome Chompski": "give gnome",
    "Scout": "give sniper_scout",
    "AWP": "give sniper_awp",
}

# Trap (special infected) spawn commands
TRAP_SPAWN_COMMANDS: dict[str, str] = {
    TrapType.BOOMER.value: "z_spawn boomer",
    TrapType.HUNTER.value: "z_spawn hunter",
    TrapType.SMOKER.value: "z_spawn smoker",
    TrapType.TANK.value: "z_spawn tank",
    TrapType.WITCH.value: "z_spawn witch",
    TrapType.CHARGER.value: "z_spawn charger",
    TrapType.JOCKEY.value: "z_spawn jockey",
    TrapType.SPITTER.value: "z_spawn spitter",
}


# ============================================================================
# STARTER ITEM CONSTANTS
# ============================================================================

# Starting item pools by campaign count
STARTER_ITEMS_MINIMAL: list[str] = [
    "First Aid Kit",
    "First Aid Kit",
    "Pills",
    "Pills",
    "Adrenaline",
    "Molotov",
    "Pipe Bomb",
    "Bile Bomb",
    "Pump Shotgun",
    "Submachine Gun",
    "Chrome Shotgun",
    "P220 Pistol",
    "P220 Pistol",
]

STARTER_ITEMS_STANDARD: list[str] = [
    "First Aid Kit",
    "First Aid Kit",
    "First Aid Kit",
    "Pills",
    "Pills",
    "Pills",
    "Adrenaline",
    "Adrenaline",
    "Molotov",
    "Pipe Bomb",
    "Pipe Bomb",
    "Bile Bomb",
    "Pump Shotgun",
    "Submachine Gun",
    "Submachine Gun",
    "Chrome Shotgun",
    "Tactical Shotgun",
    "M-16",
    "AK-47",
    "Hunting Rifle",
    "P220 Pistol",
    "P220 Pistol",
    "Magnum",
]

STARTER_ITEMS_FULL: list[str] = [
    "First Aid Kit",
    "First Aid Kit",
    "First Aid Kit",
    "First Aid Kit",
    "Defib",
    "Pills",
    "Pills",
    "Pills",
    "Pills",
    "Adrenaline",
    "Adrenaline",
    "Molotov",
    "Molotov",
    "Pipe Bomb",
    "Pipe Bomb",
    "Pipe Bomb",
    "Bile Bomb",
    "Bile Bomb",
    "Pump Shotgun",
    "Chrome Shotgun",
    "Tactical Shotgun",
    "Combat Shotgun",
    "Submachine Gun",
    "Silenced Submachine Gun",
    "MP5",
    "M-16",
    "AK-47",
    "Scar-H",
    "SG 552",
    "Hunting Rifle",
    "Sniper Rifle",
    "Grenade Launcher",
    "M60",
    "P220 Pistol",
    "P220 Pistol",
    "Magnum",
    "Magnum",
    "Fireaxe",
    "Katana",
    "Machete",
    "Crowbar",
    "Laser Sight",
    "Incendiary",
    "Explosive Ammo",
    "Gnome Chompski",
]

# Starter items configuration: (max_campaigns, item_pool)
STARTER_ITEM_POOLS: list[tuple[int, list[str]]] = [
    (3, STARTER_ITEMS_MINIMAL),
    (7, STARTER_ITEMS_STANDARD),
    (14, STARTER_ITEMS_FULL),
]
