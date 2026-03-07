import logging
from BaseClasses import MultiWorld, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, CollectionState, WebWorld
from typing import Dict, Any, List
from .Items import (
    base_id,
    full_item_list,
    unique_item_dict,
    useful_items,
    junk_items,
    progression_items,
    trap_items,
    item_groups,
)
from .Locations import get_location_names, get_total_locations
from .Options import L4D2Options, L4D2Goal
from .Regions import create_regions
from .Types import ItemData, APSkeletonItem


# This is where you setup the page on the site!
# Typically is the name of your game with web
# Whatever you named the folder you are holding all of this in
class L4D2Web(WebWorld):
    # Theres a few different themes so have fun with it
    theme = "Party"

    # You shouldnt have to change much here except the name at the bottom!
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up (the game you are randomizing) for Archipelago. "
            "This guide covers single-player, multiworld, and related software.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Yufii"],
        )
    ]


# This class is the real meat and potatoes
# Same as the first class its normally named whatever you named your folder with World at the end
class L4D2World(World):
    """
    Left 4 Dead 2 is a cooperative fps game where you kill a fuck ton of zombies and also kill the survivors too as the special infected
    """

    # You want to put the full name of the game here. If you shortened the name for the folder and class names, dont do that here
    game = "Left 4 Dead 2"
    # The item_table will be setup in  your Items.py. This line gets all the items you put into item_table and puts it in a way that AP can understand it
    item_name_to_id = unique_item_dict
    # get_location_names() will come from your Locations.py
    location_name_to_id = get_location_names()
    # And these 2 are the name of your Options.py class.
    options_dataclass = L4D2Options
    options = L4D2Options
    # The name of the class above
    web = L4D2Web()
    # print("🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀")

    # There are other built in variables for AP. You can look at other worlds to see your options
    # Like PLEASE look at the various worlds. Its so helpful. Find one you like and you can duplicate a bunch of it

    # This is where you put stuff that need to be done RIGHT away. Typically you can just leave it alone but it can be useful to pop some things here as needed
    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    @property
    def win_condition(self):
        # A list of the items that count towards campaign completion.
        campaign_items = (
            "Dead Center",
            "The Passing",
            "Dark Carnival",
            "Swamp Fever",
            "Hard Rain",
            "The Parish",
            "Cold Stream",
            "The Sacrifice",
            "No Mercy",
            "Crash Course",
            "Death Toll",
            "Dead Air",
            "Blood Harvest",
            "The Last Stand",
        )

        # Win condition for collecting the specified number of campaigns
        required_campaigns = self.options.goal.value
        if required_campaigns >= len(campaign_items):
            # If goal is 14 or more, require all campaigns
            return lambda state: state.has_all(campaign_items, self.player)
        else:
            # Otherwise, require the specified number of any campaigns
            return lambda state: state.has_any(
                campaign_items, self.player, required_campaigns
            )

    # Regions are the different locations in your world. So like Undead Burgh in dark souls or Pacifilog Town in pokemon
    # They dont have to match your game, they can be whatever you need them to be for organization
    def create_regions(self) -> None:
        create_regions(self.multiworld, self.options, self.player)

        # Solo play: guarantee one progression per campaign
        self.preplaced_prog = []
        if self.multiworld.players == 1:
            campaign_names = [
                "Dead Center",
                "The Passing",
                "Dark Carnival",
                "Swamp Fever",
                "Hard Rain",
                "The Parish",
                "Cold Stream",
                "The Sacrifice",
                "No Mercy",
                "Crash Course",
                "Death Toll",
                "Dead Air",
                "Blood Harvest",
                "The Last Stand",
            ]
            prog_items = list(progression_items.keys())
            self.multiworld.random.shuffle(prog_items)
            l4d1_campaigns = [
                "No Mercy",
                "Crash Course",
                "Death Toll",
                "Dead Air",
                "Blood Harvest",
                "The Sacrifice",
                "The Last Stand",
            ]
            for i, campaign in enumerate(campaign_names):
                character = "Bill" if campaign in l4d1_campaigns else "Coach"
                location_name = f"{campaign} - Safe Room 1({character})"
                location = self.multiworld.get_location(location_name, self.player)
                prog_name = prog_items[i]
                item = self.create_item(prog_name)
                location.place_locked_item(item)
                self.preplaced_prog.append(prog_name)

        # You can also use this space to do other location creation activities
        # Like if an option is enabled to add extra locations
        # Or the opposite, whatever it is. Just be careful that you arent duplicating locations

    # This is just a helper function for turning names into Items. You could do some other stuff here as well
    # ahit does similar if you want another look and bomb rush cyberfunk does it in a slightly different way by turning it into a specific item for that game
    # Again hopefully I do a better job of explaining the Items.py file
    def create_item(self, name: str) -> "APSkeletonItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id

        match name:
            case "Pump Shotgun":
                classification = ItemClassification.useful
            case "Chrome Shotgun":
                classification = ItemClassification.useful
            case "Submachine Gun":
                classification = ItemClassification.useful
            case "Silenced Submachine Gun":
                classification = ItemClassification.useful
            case "MP5":
                classification = ItemClassification.useful
            case "Tactical Shotgun":
                classification = ItemClassification.useful
            case "Combat Shotgun":
                classification = ItemClassification.useful
            case "Hunting Rifle":
                classification = ItemClassification.useful
            case "Sniper Rifle":
                classification = ItemClassification.useful
            case "M-16":
                classification = ItemClassification.useful
            case "Scar-H":
                classification = ItemClassification.useful
            case "AK-47":
                classification = ItemClassification.useful
            case "SG 552":
                classification = ItemClassification.useful
            case "Scout":
                classification = ItemClassification.filler
            case "AWP":
                classification = ItemClassification.filler
            case "The Passing":
                classification = ItemClassification.progression
            case "Dark Carnival":
                classification = ItemClassification.progression
            case "Swamp Fever":
                classification = ItemClassification.progression
            case "Hard Rain":
                classification = ItemClassification.progression
            case "The Parish":
                classification = ItemClassification.progression
            case "Cold Stream":
                classification = ItemClassification.progression
            case "No Mercy":
                classification = ItemClassification.progression
            case "Crash Course":
                classification = ItemClassification.progression
            case "Death Toll":
                classification = ItemClassification.progression
            case "Dead Air":
                classification = ItemClassification.progression
            case "Blood Harvest":
                classification = ItemClassification.progression
            case "The Sacrifice":
                classification = ItemClassification.progression
            case "The Last Stand":
                classification = ItemClassification.progression
            case "First Aid Kit":
                classification = ItemClassification.useful
            case "Defib":
                classification = ItemClassification.useful
            case "Pills":
                classification = ItemClassification.useful
            case "Adrenaline":
                classification = ItemClassification.useful
            case "Laser Sight":
                classification = ItemClassification.useful
            case "Incendiary":
                classification = ItemClassification.useful
            case "Explosive Ammo":
                classification = ItemClassification.useful
            case "Grenade Launcher":
                classification = ItemClassification.useful
            case "M60":
                classification = ItemClassification.useful
            case "Molotov":
                classification = ItemClassification.useful
            case "Pipe Bomb":
                classification = ItemClassification.useful
            case "Bile Bomb":
                classification = ItemClassification.useful
            case "Fireaxe":
                classification = ItemClassification.useful
            case "Baseball Bat":
                classification = ItemClassification.useful
            case "Cricket Bat":
                classification = ItemClassification.useful
            case "Crowbar":
                classification = ItemClassification.useful
            case "Frying Pan":
                classification = ItemClassification.useful
            case "Golf Club":
                classification = ItemClassification.useful
            case "Guitar":
                classification = ItemClassification.useful
            case "Katana":
                classification = ItemClassification.useful
            case "Machete":
                classification = ItemClassification.useful
            case "Nightstick":
                classification = ItemClassification.useful
            case "Pitchfork":
                classification = ItemClassification.useful
            case "Shovel":
                classification = ItemClassification.useful
            case "Knife":
                classification = ItemClassification.useful
            case "Chainsaw":
                classification = ItemClassification.useful
            case "Riot Shield":
                classification = ItemClassification.useful
            case "Gas Can":
                classification = ItemClassification.useful
            case "Oxygen Tank":
                classification = ItemClassification.useful
            case "Propane Tank":
                classification = ItemClassification.useful
            case "Fireworks":
                classification = ItemClassification.useful
            case "P220 Pistol":
                classification = ItemClassification.useful
            case "Glock":
                classification = ItemClassification.filler
            case "Gutted Medkit":
                classification = ItemClassification.filler
            case "Empty Gas Can":
                classification = ItemClassification.filler
            case "Expired Pills":
                classification = ItemClassification.filler
            case "Dud Pipe Bomb":
                classification = ItemClassification.filler
            case "Bent Laser Sight":
                classification = ItemClassification.filler
            case "Punctured Oxygen Tank":
                classification = ItemClassification.filler
            case "Magnum":
                classification = ItemClassification.useful
            case "Gnome Chompski":
                classification = ItemClassification.useful
            case "Trap: Boomer":
                classification = ItemClassification.trap
            case "Trap: Hunter":
                classification = ItemClassification.trap
            case "Trap: Smoker":
                classification = ItemClassification.trap
            case "Trap: Tank":
                classification = ItemClassification.trap
            case "Trap: Witch":
                classification = ItemClassification.trap
            case "Trap: Charger":
                classification = ItemClassification.trap
            case "Trap: Jockey":
                classification = ItemClassification.trap
            case "Trap: Spitter":
                classification = ItemClassification.trap
            case "Dead Center":
                classification = ItemClassification.progression
            case _:  # Should not occur
                raise Exception(
                    'Unexpected case met: classification cannot be set for unknown item "'
                    + name
                    + '"'
                )

        return APSkeletonItem(name, classification, item_id, self.player)

    # The slot data is what youre sending to the AP server kinda. You dont have to add all your options. Really you want the ones you think a pop tracker would use
    # Seed, Slot, and TotalLocations are all super important for AP though, you need those
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {
            "options": {
                "L4D2DeathLink": self.options.death_link.value,
                "StartWithCampaign": self.options.starting_campaign.value,
                "AllCampaignsStart": self.options.all_campaigns_start.value,
                "L4D2Goal": self.options.goal.value,
            },
            "Seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "Slot": self.multiworld.player_name[self.player],  # to connect to server
            "TotalLocations": get_total_locations(
                self
            ),  # get_total_locations(self) comes from Locations.py
        }
        slot_data["item_name_to_id"] = self.item_name_to_id
        slot_data["location_name_to_id"] = self.location_name_to_id

        return slot_data

    # These are used by AP to add and remove items from the player. You can probably just leave them alone
    def create_items(self) -> None:
        all_items = []
        # Add progression items
        for name in progression_items.keys():
            all_items.append(name)
        # Add useful items in tiers
        high_priority = [
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
        for name in high_priority:
            all_items += [name] * 5
        medium_priority = [
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
        for name in medium_priority:
            all_items += [name] * 4
        low_priority = [
            name
            for name in useful_items.keys()
            if name not in high_priority and name not in medium_priority
        ]
        for name in low_priority:
            all_items += [name] * 3
        # Add base traps
        for name in trap_items.keys():
            all_items.append(name)
        # Add extra traps based on option
        trap_count = self.options.trap_count.value
        extra_needed = max(0, trap_count - 8)
        trap_names = list(trap_items.keys())
        total_locations = get_total_locations(self)
        max_extra = total_locations - len(all_items)
        extra_to_add = min(extra_needed, max_extra)
        for _ in range(extra_to_add):
            all_items.append(self.multiworld.random.choice(trap_names))
        # Fill remainder with junk
        junk_names = list(junk_items.keys())
        while len(all_items) < total_locations:
            all_items.append(self.multiworld.random.choice(junk_names))
        # Remove pre-placed progression items
        if hasattr(self, "preplaced_prog"):
            for name in self.preplaced_prog:
                all_items.remove(name)
        # Create items and add to pool
        self.multiworld.itempool += [
            self.create_item(item_name) for item_name in all_items
        ]

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)
