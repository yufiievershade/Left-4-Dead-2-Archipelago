#!/usr/bin/env python3
"""
Location mapping for L4D2 Archipelago integration
Maps game events to Archipelago location IDs
"""

# Base ID from Locations.py
BASE_ID = 69420000

# Character sets
L4D2_SURVIVORS = ["ellis", "rochelle", "coach", "nick"]
L4D1_SURVIVORS = ["francis", "bill", "zoey", "louis"]

# Campaign map definitions: (campaign_prefix, map_names[], is_l4d1)
# Map names should be in order of safe room progression
CAMPAIGN_MAPS = [
    ("c1", ["m1_hotel", "m2_streets", "m3_mall", "m4_atrium"], False),  # Dead Center
    ("c6", ["m1_riverbank", "m2_bedlam", "m3_port"], False),  # The Passing
    ("c2", ["m1_highway", "m2_fairgrounds", "m3_coaster", "m4_barns", "m5_concert"], False),  # Dark Carnival
    ("c3", ["m1_plankcountry", "m2_swamp", "m3_shantytown", "m4_plantation"], False),  # Swamp Fever
    ("c4", ["m1_milltown_a", "m2_sugarmill_a", "m3_sugarmill_b", "m4_milltown_b", "m5_milltown_escape"], False),  # Hard Rain
    ("c5", ["m1_waterfront", "m2_park", "m3_cemetery", "m4_quarter", "m5_bridge"], False),  # The Parish
    ("c7", ["m1_docks", "m2_barge", "m3_port"], True),  # The Sacrifice
    ("c8", ["m1_apartment", "m2_subway", "m3_sewers", "m4_interior", "m5_rooftop"], True),  # No Mercy
    ("c9", ["m1_alleys", "m2_lots"], True),  # Crash Course
    ("c10", ["m1_caves", "m2_drainage", "m3_ranchhouse", "m4_mainstreet", "m5_houseboat"], True),  # Death Toll
    ("c11", ["m1_greenhouse", "m2_offices", "m3_garage", "m4_terminal", "m5_runway"], True),  # Dead Air
    ("c12", ["m1_hilltop", "m2_traintunnel", "m3_bridge", "m4_barn", "m5_cornfield"], True),  # Blood Harvest
    ("c13", ["m1_alpinecreek", "m2_southpinestream", "m3_memorialbridge", "m4_cutthroatcreek"], False),  # Cold Stream
    ("c14", ["m1_junkyard", "m2_lighthouse"], True),  # The Last Stand
]

# Special single locations: (map_name, key, offset)
SPECIAL_LOCATIONS = [
    ("c1m2_streets", "cola_bottles", 16),
]

# Extra minigame locations: (map_name, key, offset)
EXTRA_LOCATIONS = [
    ("c2m2_fairgrounds", "moustachio_strength", 229),
    ("c2m3_coaster", "moustachio_whack", 230),
    ("c2m1_highway", "gnome_chompski", 231),
]


def generate_location_map():
    """Generate the complete location mapping dictionary."""
    location_map = {}
    location_id = 0

    for campaign_prefix, maps, is_l4d1 in CAMPAIGN_MAPS:
        survivors = L4D1_SURVIVORS if is_l4d1 else L4D2_SURVIVORS

        for map_suffix in maps:
            map_name = f"{campaign_prefix}{map_suffix}"
            for survivor in survivors:
                key = (map_name, survivor)
                location_map[key] = BASE_ID + location_id
                location_id += 1

    # Add special locations
    for map_name, key, offset in SPECIAL_LOCATIONS:
        location_map[(map_name, key)] = BASE_ID + offset

    # Add extra locations
    for map_name, key, offset in EXTRA_LOCATIONS:
        location_map[(map_name, key)] = BASE_ID + offset

    return location_map


# Generate the location map
LOCATION_MAP = generate_location_map()


def get_location_id(map_name, character_name):
    """Get location ID for a map and character combination"""
    key = (map_name, character_name.lower())
    return LOCATION_MAP.get(key)


def get_all_location_ids():
    """Get all location IDs"""
    return list(LOCATION_MAP.values())
