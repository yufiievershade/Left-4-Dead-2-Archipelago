"""Item definitions for Left 4 Dead 2 Archipelago world.

This module defines all items, their IDs, and quantities for the item pool.
"""

from .Types import CAMPAIGNS

base_id = 69420000

# Item definitions: (name, category, quantity_in_pool)
# Categories: "progression", "useful", "junk", "trap"
ITEM_DEFINITIONS = [
    # Progression items (campaign unlocks) - 1 each
    *((campaign, "progression", 1) for campaign in CAMPAIGNS),
    # Medical supplies (high priority, quantity 5)
    ("First Aid Kit", "useful", 5),
    ("Defib", "useful", 5),
    ("Pills", "useful", 5),
    ("Adrenaline", "useful", 5),
    ("Laser Sight", "useful", 5),
    ("Incendiary", "useful", 5),
    ("Explosive Ammo", "useful", 5),
    # Primary weapons
    ("Pump Shotgun", "useful", 4),
    ("Chrome Shotgun", "useful", 5),
    ("Submachine Gun", "useful", 5),
    ("Silenced Submachine Gun", "useful", 5),
    ("MP5", "useful", 5),
    ("Tactical Shotgun", "useful", 5),
    ("Combat Shotgun", "useful", 5),
    ("Hunting Rifle", "useful", 5),
    ("Sniper Rifle", "useful", 3),
    ("M-16", "useful", 5),
    ("Scar-H", "useful", 5),
    ("AK-47", "useful", 5),
    ("SG 552", "useful", 5),
    # Secondary weapons
    ("Grenade Launcher", "useful", 5),
    ("M60", "useful", 5),
    ("Scout", "useful", 4),
    ("AWP", "useful", 5),
    # Junk weapons
    ("Glock", "junk", 4),
    # Throwables
    ("Molotov", "useful", 5),
    ("Pipe Bomb", "useful", 6),
    ("Bile Bomb", "useful", 4),
    # Melee weapons
    ("Fireaxe", "useful", 4),
    ("Baseball Bat", "useful", 5),
    ("Cricket Bat", "useful", 5),
    ("Crowbar", "useful", 5),
    ("Frying Pan", "useful", 4),
    ("Golf Club", "useful", 4),
    ("Guitar", "useful", 5),
    ("Katana", "useful", 4),
    ("Machete", "useful", 4),
    ("Nightstick", "useful", 5),
    ("Pitchfork", "useful", 4),
    ("Shovel", "useful", 5),
    ("Knife", "useful", 4),
    ("Chainsaw", "useful", 5),
    ("Riot Shield", "useful", 4),
    # Scavenge items
    ("Gas Can", "useful", 7),
    ("Oxygen Tank", "useful", 4),
    ("Propane Tank", "useful", 5),
    ("Fireworks", "useful", 5),
    # Pistols and special
    ("P220 Pistol", "useful", 4),
    ("Magnum", "useful", 4),
    ("Gnome Chompski", "useful", 1),
    # Junk items
    ("Gutted Medkit", "junk", 20),
    ("Empty Gas Can", "junk", 20),
    ("Expired Pills", "junk", 20),
    ("Dud Pipe Bomb", "junk", 20),
    ("Bent Laser Sight", "junk", 20),
    ("Punctured Oxygen Tank", "junk", 20),
    # Traps (8 special infected types) - added dynamically based on trap_count option
    ("Trap: Boomer", "trap", 1),
    ("Trap: Hunter", "trap", 1),
    ("Trap: Smoker", "trap", 1),
    ("Trap: Tank", "trap", 1),
    ("Trap: Witch", "trap", 1),
    ("Trap: Charger", "trap", 1),
    ("Trap: Jockey", "trap", 1),
    ("Trap: Spitter", "trap", 1),
]


def _generate_item_dicts():
    """Generate item dictionaries from ITEM_DEFINITIONS."""
    progression = {}
    useful = {}
    junk = {}
    trap = {}

    for idx, (name, category, _) in enumerate(ITEM_DEFINITIONS, start=1):
        item_id = base_id + idx
        if category == "progression":
            progression[name] = item_id
        elif category == "useful":
            useful[name] = item_id
        elif category == "junk":
            junk[name] = item_id
        elif category == "trap":
            trap[name] = item_id

    return progression, useful, junk, trap


def _generate_full_item_list():
    """Generate the full item pool list from ITEM_DEFINITIONS."""
    items = []
    for name, _, quantity in ITEM_DEFINITIONS:
        items.extend([name] * quantity)
    return items


# Generate the dictionaries
progression_items, useful_items, junk_items, trap_items = _generate_item_dicts()

# All items combined (unique, no duplicates)
unique_item_dict = {**useful_items, **junk_items, **progression_items, **trap_items}

# Full item pool with quantities
full_item_list = _generate_full_item_list()

# Item groups for organization and hinting
item_groups = {
    "weapons": [
        "Pump Shotgun",
        "Chrome Shotgun",
        "Submachine Gun",
        "Silenced Submachine Gun",
        "MP5",
        "Tactical Shotgun",
        "Combat Shotgun",
        "Hunting Rifle",
        "Sniper Rifle",
        "M-16",
        "Scar-H",
        "AK-47",
        "SG 552",
        "Scout",
        "AWP",
        "Grenade Launcher",
        "M60",
        "P220 Pistol",
        "Magnum",
        "Glock",
    ],
    "melee_weapons": [
        "Fireaxe",
        "Baseball Bat",
        "Cricket Bat",
        "Crowbar",
        "Frying Pan",
        "Golf Club",
        "Guitar",
        "Katana",
        "Machete",
        "Nightstick",
        "Pitchfork",
        "Shovel",
        "Knife",
        "Chainsaw",
        "Riot Shield",
    ],
    "medical": [
        "First Aid Kit",
        "Defib",
        "Pills",
        "Adrenaline",
        "Laser Sight",
        "Incendiary",
        "Explosive Ammo",
    ],
    "throwables": [
        "Molotov",
        "Pipe Bomb",
        "Bile Bomb",
    ],
    "campaigns": list(progression_items.keys()),
    "traps": list(trap_items.keys()),
    "junk": list(junk_items.keys()),
    "scavenge": [
        "Gas Can",
        "Oxygen Tank",
        "Propane Tank",
        "Fireworks",
    ],
}
