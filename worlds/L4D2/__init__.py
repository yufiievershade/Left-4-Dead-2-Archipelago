from BaseClasses import MultiWorld, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, CollectionState, WebWorld
from .Items import (
    unique_item_dict,
    useful_items,
    junk_items,
    progression_items,
    trap_items,
)
from .Locations import get_location_names, get_total_locations
from .Options import L4D2Options, l4d2_option_groups
from .Regions import create_regions
from .Types import APSkeletonItem, CAMPAIGNS, L4D1_CAMPAIGNS


# Item classifications for create_item method
ITEM_CLASSIFICATIONS: dict[str, ItemClassification] = {
    # Campaigns (progression)
    "Dead Center": ItemClassification.progression,
    "The Passing": ItemClassification.progression,
    "Dark Carnival": ItemClassification.progression,
    "Swamp Fever": ItemClassification.progression,
    "Hard Rain": ItemClassification.progression,
    "The Parish": ItemClassification.progression,
    "Cold Stream": ItemClassification.progression,
    "No Mercy": ItemClassification.progression,
    "Crash Course": ItemClassification.progression,
    "Death Toll": ItemClassification.progression,
    "Dead Air": ItemClassification.progression,
    "Blood Harvest": ItemClassification.progression,
    "The Sacrifice": ItemClassification.progression,
    "The Last Stand": ItemClassification.progression,
    # Weapons (useful)
    "Pump Shotgun": ItemClassification.useful,
    "Chrome Shotgun": ItemClassification.useful,
    "Submachine Gun": ItemClassification.useful,
    "Silenced Submachine Gun": ItemClassification.useful,
    "MP5": ItemClassification.useful,
    "Tactical Shotgun": ItemClassification.useful,
    "Combat Shotgun": ItemClassification.useful,
    "Hunting Rifle": ItemClassification.useful,
    "Sniper Rifle": ItemClassification.useful,
    "M-16": ItemClassification.useful,
    "Scar-H": ItemClassification.useful,
    "AK-47": ItemClassification.useful,
    "SG 552": ItemClassification.useful,
    # Medical supplies (useful)
    "First Aid Kit": ItemClassification.useful,
    "Defib": ItemClassification.useful,
    "Pills": ItemClassification.useful,
    "Adrenaline": ItemClassification.useful,
    "Laser Sight": ItemClassification.useful,
    "Incendiary": ItemClassification.useful,
    "Explosive Ammo": ItemClassification.useful,
    # Throwables and special weapons (useful)
    "Grenade Launcher": ItemClassification.useful,
    "M60": ItemClassification.useful,
    "Molotov": ItemClassification.useful,
    "Pipe Bomb": ItemClassification.useful,
    "Bile Bomb": ItemClassification.useful,
    # Melee weapons (useful)
    "Fireaxe": ItemClassification.useful,
    "Baseball Bat": ItemClassification.useful,
    "Cricket Bat": ItemClassification.useful,
    "Crowbar": ItemClassification.useful,
    "Frying Pan": ItemClassification.useful,
    "Golf Club": ItemClassification.useful,
    "Guitar": ItemClassification.useful,
    "Katana": ItemClassification.useful,
    "Machete": ItemClassification.useful,
    "Nightstick": ItemClassification.useful,
    "Pitchfork": ItemClassification.useful,
    "Shovel": ItemClassification.useful,
    "Knife": ItemClassification.useful,
    "Chainsaw": ItemClassification.useful,
    "Riot Shield": ItemClassification.useful,
    # Items and scavenge (useful)
    "Gas Can": ItemClassification.useful,
    "Oxygen Tank": ItemClassification.useful,
    "Propane Tank": ItemClassification.useful,
    "Fireworks": ItemClassification.useful,
    # Pistols and collectibles (useful)
    "P220 Pistol": ItemClassification.useful,
    "Magnum": ItemClassification.useful,
    "Gnome Chompski": ItemClassification.useful,
    # Junk weapons (filler)
    "Scout": ItemClassification.filler,
    "AWP": ItemClassification.filler,
    "Glock": ItemClassification.filler,
    # Junk items (filler)
    "Gutted Medkit": ItemClassification.filler,
    "Empty Gas Can": ItemClassification.filler,
    "Expired Pills": ItemClassification.filler,
    "Dud Pipe Bomb": ItemClassification.filler,
    "Bent Laser Sight": ItemClassification.filler,
    "Punctured Oxygen Tank": ItemClassification.filler,
    # Infected traps (trap)
    "Trap: Boomer": ItemClassification.trap,
    "Trap: Hunter": ItemClassification.trap,
    "Trap: Smoker": ItemClassification.trap,
    "Trap: Tank": ItemClassification.trap,
    "Trap: Witch": ItemClassification.trap,
    "Trap: Charger": ItemClassification.trap,
    "Trap: Jockey": ItemClassification.trap,
    "Trap: Spitter": ItemClassification.trap,
}


# Item priority tiers for create_items
HIGH_PRIORITY_ITEMS = [
    "First Aid Kit",
    "Defib",
    "Pills",
    "Adrenaline",
    "Laser Sight",
    "Incendiary",
    "Explosive Ammo",
    "Molotov",
    "Pipe Bomb",
    "Bile Bomb",
    "Grenade Launcher",
    "M60",
]

MEDIUM_PRIORITY_ITEMS = [
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
    "P220 Pistol",
    "Magnum",
    "Gnome Chompski",
]


class L4D2Web(WebWorld):
    """WebWorld configuration for Left 4 Dead 2."""

    theme = "Party"
    option_groups = l4d2_option_groups

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Left 4 Dead 2 for Archipelago. "
            "This guide covers single-player, multiworld, and related software.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Yufii"],
        )
    ]


class L4D2World(World):
    """Left 4 Dead 2 Archipelago world implementation.

    A cooperative FPS where players fight through zombie campaigns.
    """

    game = "Left 4 Dead 2"
    item_name_to_id = unique_item_dict
    location_name_to_id = get_location_names()
    options_dataclass = L4D2Options
    options = L4D2Options
    web = L4D2Web()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    @property
    def win_condition(self):
        """Determine the win condition based on the goal option."""
        # Win condition for collecting the specified number of campaigns
        required_campaigns = self.options.goal.value

        if required_campaigns >= len(CAMPAIGNS):
            # If goal is 14 or more, require all campaigns
            return lambda state: state.has_all(CAMPAIGNS, self.player)
        else:
            # Otherwise, require the specified number of any campaigns
            return lambda state: state.has_any(
                CAMPAIGNS, self.player, required_campaigns
            )

    def create_regions(self) -> None:
        """Create all regions and place pre-placed items for solo play."""
        # Create base regions from Regions.py
        create_regions(self.multiworld, self.options, self.player)

        # Solo play: guarantee one progression per campaign
        self.preplaced_prog = []

        if self.multiworld.players == 1:
            prog_items = list(progression_items.keys())
            self.multiworld.random.shuffle(prog_items)

            for i, campaign in enumerate(CAMPAIGNS):
                # Determine which character to use based on campaign
                character = "Bill" if campaign in L4D1_CAMPAIGNS else "Coach"

                # Build location name and get the location object
                location_name = f"{campaign} - Safe Room 1({character})"
                location = self.multiworld.get_location(location_name, self.player)

                # Get the progression item for this campaign and create it
                prog_name = prog_items[i]
                item = self.create_item(prog_name)

                # Place the item and track it
                location.place_locked_item(item)
                self.preplaced_prog.append(prog_name)

    # This is just a helper function for turning names into Items. You could do some other stuff here as well
    # ahit does similar if you want another look and bomb rush cyberfunk does it in a slightly different way by turning it into a specific item for that game
    # Again hopefully I do a better job of explaining the Items.py file
    def create_item(self, name: str) -> "APSkeletonItem":
        """Create an item with the appropriate classification."""
        item_id: int = self.item_name_to_id[name]

        # Get classification from mapping, raise error if not found
        if name not in ITEM_CLASSIFICATIONS:
            raise Exception(f'Classification cannot be set for unknown item "{name}"')

        return APSkeletonItem(name, ITEM_CLASSIFICATIONS[name], item_id, self.player)

    def fill_slot_data(self) -> dict[str, object]:
        """Fill slot data for the client to receive on connection."""
        slot_data: dict[str, object] = {
            "options": {
                "L4D2DeathLink": self.options.death_link.value,
                "StartWithCampaign": self.options.starting_campaign.value,
                "AllCampaignsStart": self.options.all_campaigns_start.value,
                "L4D2Goal": self.options.goal.value,
            },
            "Seed": self.multiworld.seed_name,
            "Slot": self.multiworld.player_name[self.player],
            "TotalLocations": get_total_locations(self),
            "item_name_to_id": self.item_name_to_id,
            "location_name_to_id": self.location_name_to_id,
        }

        return slot_data

    def create_items(self) -> None:
        """Create all items for the item pool based on player options."""
        # Build item pool
        all_items: list[str] = []

        # Add one of each progression item (campaign unlocks)
        all_items.extend(progression_items.keys())

        # Add useful items by priority (higher priority = more copies)
        all_items.extend(item for item in HIGH_PRIORITY_ITEMS for _ in range(5))
        all_items.extend(item for item in MEDIUM_PRIORITY_ITEMS for _ in range(4))

        # Add remaining useful items (low priority, 3 copies each)
        prioritized = set(HIGH_PRIORITY_ITEMS) | set(MEDIUM_PRIORITY_ITEMS)
        low_priority = [item for item in useful_items.keys() if item not in prioritized]
        all_items.extend(item for item in low_priority for _ in range(3))

        # Add base traps (8 special infected types)
        all_items.extend(trap_items.keys())

        # Add extra traps based on player option (capped by available slots)
        total_locations = get_total_locations(self)
        available_slots = total_locations - len(all_items)
        trap_names = list(trap_items.keys())

        # Can't be less than 0
        extra_traps = max(0, self.options.trap_count.value - 8)

        # Loop N times to add N randomly chosen traps (may be different each iteration)
        for _ in range(min(extra_traps, available_slots)):
            all_items.append(self.multiworld.random.choice(trap_names))

        # Fill remaining slots with junk items
        junk_pool = list(junk_items.keys())
        while len(all_items) < total_locations:
            all_items.append(self.multiworld.random.choice(junk_pool))

        # Remove pre-placed progression items (using set for O(1) lookup)
        preplaced = set(getattr(self, "preplaced_prog", []))
        all_items = [item for item in all_items if item not in preplaced]

        # Create items and add to pool
        self.multiworld.itempool.extend(self.create_item(name) for name in all_items)

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        """Collect an item and update the collection state."""
        return super().collect(state, item)

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        """Remove an item and update the collection state."""
        return super().remove(state, item)

    def get_filler_item_name(self) -> str:
        """Return the name of a filler item for padding the item pool.

        Returns a random junk item (broken/useless items or bad weapons).
        """
        return self.random.choice(list(junk_items.keys()))
