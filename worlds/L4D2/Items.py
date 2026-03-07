from BaseClasses import Item

base_id = 69420000

progression_items = {
"Dead Center": base_id + 1,
"The Passing": base_id + 2,
"Dark Carnival": base_id + 3,
"Swamp Fever": base_id + 4,
"Hard Rain": base_id + 5,
"The Parish": base_id + 6,
"Cold Stream": base_id + 7,
"No Mercy": base_id + 8,
"Crash Course": base_id + 9,
"Death Toll": base_id + 10,
"Dead Air": base_id + 11,
"Blood Harvest": base_id + 12,
"The Sacrifice": base_id + 13,
"The Last Stand": base_id + 14,
}

trap_items = {
"Trap: Boomer": base_id + 650,
"Trap: Hunter": base_id + 651,
"Trap: Smoker": base_id + 652,
"Trap: Tank": base_id + 653,
"Trap: Witch": base_id + 654,
"Trap: Charger": base_id + 655,
"Trap: Jockey": base_id + 656,
"Trap: Spitter": base_id + 657
}



junk_items = {
"Glock": base_id + 15,
"AWP": base_id + 16,
"Scout": base_id + 17,
"Gutted Medkit": base_id + 658,
"Empty Gas Can": base_id + 659,
"Expired Pills": base_id + 660,
"Dud Pipe Bomb": base_id + 661,
"Bent Laser Sight": base_id + 662,
"Punctured Oxygen Tank": base_id + 663
}

useful_items = {
"First Aid Kit": base_id + 18,
"Defib": base_id + 19,
"Pills": base_id + 20,
"Adrenaline": base_id + 21,
"Laser Sight": base_id + 22,
"Incendiary": base_id + 23,
"Explosive Ammo": base_id + 24,
"Pump Shotgun": base_id + 25,
"Chrome Shotgun": base_id + 26,
"Submachine Gun": base_id + 27,
"Silenced Submachine Gun": base_id + 28,
"MP5": base_id + 29,
"Tactical Shotgun": base_id + 30,
"Combat Shotgun": base_id + 31,
"Hunting Rifle": base_id + 32,
"Sniper Rifle": base_id + 33,
"M-16": base_id + 34,
"Scar-H": base_id + 35,
"AK-47": base_id + 36,
"SG 552": base_id + 37,
"Grenade Launcher": base_id + 38,
"M60": base_id + 39,
"Molotov": base_id + 40,
"Pipe Bomb": base_id + 41,
"Bile Bomb": base_id + 42,
"Fireaxe": base_id + 43,
"Baseball Bat": base_id + 44,
"Cricket Bat": base_id + 45,
"Crowbar": base_id + 46,
"Frying Pan": base_id + 47,
"Golf Club": base_id + 48,
"Guitar": base_id + 49,
"Katana": base_id + 50,
"Machete": base_id + 51,
"Nightstick": base_id + 52,
"Pitchfork": base_id + 53,
"Shovel": base_id + 54,
"Knife": base_id + 55,
"Chainsaw": base_id + 56,
"Riot Shield": base_id + 57,
"Gas Can": base_id + 58,
"Oxygen Tank": base_id + 59,
"Propane Tank": base_id + 60,
"Fireworks": base_id + 61,
"P220 Pistol": base_id + 62,
"Magnum": base_id + 63,
"Gnome Chompski": base_id + 64
}

item_groups = {}

# All items except the duplications (no item amount)
# Note: There is no dedicated victory item; completion is handled by rules/companion logic.
unique_item_dict = {**useful_items, **junk_items, **progression_items, **trap_items}

# All items to add to the item pool
full_item_list = []
full_item_list += ["Dead Center"] * 1 
full_item_list += ["The Passing"] * 1
full_item_list += ["Dark Carnival"] * 1
full_item_list += ["Swamp Fever"] * 1
full_item_list += ["Hard Rain"] * 1
full_item_list += ["The Parish"] * 1
full_item_list += ["Cold Stream"] * 1
full_item_list += ["No Mercy"] * 1
full_item_list += ["Crash Course"] * 1
full_item_list += ["Death Toll"] * 1
full_item_list += ["Dead Air"] * 1
full_item_list += ["Blood Harvest"] * 1
full_item_list += ["The Sacrifice"] * 1
full_item_list += ["The Last Stand"] * 1
full_item_list += ["First Aid Kit"] * 5
full_item_list += ["Defib"] * 5
full_item_list += ["Pills"] * 5
full_item_list += ["Adrenaline"] * 5
full_item_list += ["Laser Sight"] * 5
full_item_list += ["Incendiary"] * 5
full_item_list += ["Explosive Ammo"] * 5
full_item_list += ["Pump Shotgun"] * 4
full_item_list += ["Chrome Shotgun"] * 5
full_item_list += ["Submachine Gun"] * 5
full_item_list += ["Silenced Submachine Gun"] * 5
full_item_list += ["MP5"] * 5
full_item_list += ["Tactical Shotgun"] * 5
full_item_list += ["Combat Shotgun"] * 5
full_item_list += ["Hunting Rifle"] * 5
full_item_list += ["Sniper Rifle"] * 3
full_item_list += ["M-16"] * 5
full_item_list += ["Scar-H"] * 5
full_item_list += ["AK-47"] * 5
full_item_list += ["SG 552"] * 5
full_item_list += ["Scout"] * 4
full_item_list += ["AWP"] * 5
full_item_list += ["Grenade Launcher"] * 5
full_item_list += ["M60"] * 5
full_item_list += ["Molotov"] * 5
full_item_list += ["Pipe Bomb"] * 6
full_item_list += ["Bile Bomb"] * 4
full_item_list += ["Fireaxe"] * 4
full_item_list += ["Baseball Bat"] * 5
full_item_list += ["Cricket Bat"] * 5
full_item_list += ["Crowbar"] * 5
full_item_list += ["Frying Pan"] * 4
full_item_list += ["Golf Club"] * 4
full_item_list += ["Guitar"] * 5
full_item_list += ["Katana"] * 4
full_item_list += ["Machete"] * 4
full_item_list += ["Nightstick"] * 5
full_item_list += ["Pitchfork"] * 4
full_item_list += ["Shovel"] * 5
full_item_list += ["Knife"] * 4
full_item_list += ["Chainsaw"] * 5
full_item_list += ["Riot Shield"] * 4
full_item_list += ["Gas Can"] * 7
full_item_list += ["Oxygen Tank"] * 4
full_item_list += ["Propane Tank"] * 5
full_item_list += ["Fireworks"] * 5
full_item_list += ["P220 Pistol"] * 4
full_item_list += ["Glock"] * 4
full_item_list += ["Magnum"] * 4
full_item_list += ["Gutted Medkit"] * 20
full_item_list += ["Empty Gas Can"] * 20
full_item_list += ["Expired Pills"] * 20
full_item_list += ["Dud Pipe Bomb"] * 20
full_item_list += ["Bent Laser Sight"] * 20
full_item_list += ["Punctured Oxygen Tank"] * 20
# Add trap placeholders - actual traps added dynamically based on trap_count option
full_item_list += ["Trap: Boomer", "Trap: Hunter", "Trap: Smoker", "Trap: Tank", "Trap: Witch", "Trap: Charger", "Trap: Jockey", "Trap: Spitter"]





