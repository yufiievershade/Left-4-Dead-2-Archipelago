from typing import TYPE_CHECKING

# You need to import the BaseClasses.py from Archipelago's core
from .Types import LocData

if TYPE_CHECKING:
    from . import L4D2World

base_id = 69420000

# Campaign definitions: (campaign_name, num_safe_rooms, finale_name, is_l4d1)
CAMPAIGNS = [
    ("Dead Center", 3, "Atrium", False),
    ("The Passing", 2, "Port", False),
    ("Dark Carnival", 4, "Concert", False),
    ("Swamp Fever", 3, "Plantation", False),
    ("Hard Rain", 4, "Town Escape", False),
    ("The Parish", 4, "Bridge", False),
    ("The Sacrifice", 2, "Port", True),
    ("No Mercy", 4, "Rooftop", True),
    ("Crash Course", 1, "Truck Depot", True),
    ("Death Toll", 4, "Boathouse", True),
    ("Dead Air", 4, "Runway", True),
    ("Blood Harvest", 4, "Farmhouse", True),
    ("Cold Stream", 3, "Cut Throat Creek", False),
    ("The Last Stand", 1, "Lighthouse", True),
]

# Character sets
L4D2_SURVIVORS = ["Ellis", "Rochelle", "Coach", "Nick"]
L4D1_SURVIVORS = ["Francis", "Bill", "Zoey", "Louis"]

# Special single locations
SPECIAL_LOCATIONS = [
    ("Dead Center - Cola Bottle Spot", "Progression"),
]

# Extra optional locations
EXTRA_LOCATIONS = [
    ("Moustachio Strength", "Progression"),
    ("Moustachio Whack A Mole", "Progression"),
    ("Gnome Chompski", "Progression"),
]


def generate_location_table() -> dict[str, LocData]:
    """Generate the complete location table from campaign definitions."""
    table = {}
    location_id = 0

    for campaign_name, num_safe_rooms, finale_name, is_l4d1 in CAMPAIGNS:
        survivors = L4D1_SURVIVORS if is_l4d1 else L4D2_SURVIVORS

        # Generate safe room locations
        for room_num in range(1, num_safe_rooms + 1):
            for survivor in survivors:
                loc_name = f"{campaign_name} - Safe Room {room_num}({survivor})"
                table[loc_name] = LocData(
                    base_id + location_id, loc_name, "Progression"
                )
                location_id += 1

        # Generate finale locations
        for survivor in survivors:
            loc_name = f"{campaign_name} - {finale_name} Finale({survivor})"
            table[loc_name] = LocData(base_id + location_id, loc_name, "Progression")
            location_id += 1

    # Add special single locations
    for loc_name, loc_type in SPECIAL_LOCATIONS:
        table[loc_name] = LocData(base_id + location_id, loc_name, loc_type)
        location_id += 1

    # Add extra locations
    for loc_name, loc_type in EXTRA_LOCATIONS:
        table[loc_name] = LocData(base_id + location_id, loc_name, loc_type)
        location_id += 1

    return table


# Generate the location table
location_table = generate_location_table()

# List of extra location names for filtering
extra_location_names = [name for name, _ in EXTRA_LOCATIONS]


def did_include_extra_locations(world: "L4D2World") -> bool:
    # Assuming an option exists to toggle extra locations
    # return bool(world.options.ExtraLocations)
    return True  # Placeholder for now


def get_total_locations(world: "L4D2World") -> int:
    total = len(location_table)
    if not did_include_extra_locations(world):
        total -= len(extra_location_names)
    return total


def get_location_names() -> dict[str, int]:
    return {name: loc_data.code for name, loc_data in location_table.items()}
