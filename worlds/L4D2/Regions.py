from BaseClasses import Region, Entrance, MultiWorld
from .Types import L4D2Location
from .Locations import location_table
from typing import TYPE_CHECKING, Dict
from .Options import L4D2Options

if TYPE_CHECKING:
    from . import L4D2World
from .Locations import location_table

def create_regions(world: MultiWorld, options: L4D2Options, player: int) -> None:
    """
    This function defines all regions, locations, and entrances for the L4D2 world.
    It creates the logical map of the game.
    """
    
    # 1. Create all regions
    regions = {}
    
    # Starting region: Menu
    regions["Menu"] = Region("Menu", player, world)
    
    # One region per campaign
    regions["Dead Center"] = Region("Dead Center", player, world)
    regions["The Passing"] = Region("The Passing", player, world)
    regions["Dark Carnival"] = Region("Dark Carnival", player, world)
    regions["Swamp Fever"] = Region("Swamp Fever", player, world)
    regions["Hard Rain"] = Region("Hard Rain", player, world)
    regions["The Parish"] = Region("The Parish", player, world)
    regions["Cold Stream"] = Region("Cold Stream", player, world)
    regions["The Sacrifice"] = Region("The Sacrifice", player, world)
    regions["No Mercy"] = Region("No Mercy", player, world)
    regions["Crash Course"] = Region("Crash Course", player, world)
    regions["Death Toll"] = Region("Death Toll", player, world)
    regions["Dead Air"] = Region("Dead Air", player, world)
    regions["Blood Harvest"] = Region("Blood Harvest", player, world)
    regions["The Last Stand"] = Region("The Last Stand", player, world)
    
    # Add all created regions to the multiworld
    for region in regions.values():
        world.regions.append(region)
        
    # 2. Populate regions with locations
    for location_name, location_data in location_table.items():
        region_name = get_region_for_location(location_name)
        if region_name and region_name in regions:
            region = regions[region_name]
            location = L4D2Location(player, location_name, location_data.code, region)
            region.locations.append(location)
        else:
            # Handle locations that don't match a campaign region
            menu_region = regions["Menu"]
            location = L4D2Location(player, location_name, location_data.code, menu_region)
            menu_region.locations.append(location)
            
    # 3. Connect regions with entrances
    for campaign_name in ["Dead Center", "The Passing", "Dark Carnival", "Swamp Fever", "Hard Rain",
                          "The Parish", "Cold Stream", "The Sacrifice", "No Mercy", "Crash Course", "Death Toll",
                          "Dead Air", "Blood Harvest", "The Last Stand"]:
        menu_to_campaign = Entrance(player, f"Menu to {campaign_name}", regions["Menu"])
        menu_to_campaign.connect(regions[campaign_name])
        menu_to_campaign.access_rule = lambda state, c=campaign_name: state.has(f"Campaign: {c}", player)
        regions["Menu"].exits.append(menu_to_campaign)
        
        # Add an entrance for returning to the menu from the campaign
        campaign_to_menu = Entrance(player, f"{campaign_name} to Menu", regions[campaign_name])
        campaign_to_menu.connect(regions["Menu"])
        regions[campaign_name].exits.append(campaign_to_menu)

def get_region_for_location(location_name: str) -> str:
    """Helper function to determine the region from a location name."""
   # if location_name.startswith("Dead Center"):
      #  return "Dead Center"
   # elif location_name.startswith("Dark Carnival"):
      #  return "Dark Carnival"
   # elif location_name.startswith("The Passing"):
      #  return "The Passing"
   # elif location_name.startswith("Swamp Fever"):
     #   return "Swamp Fever"
   # elif location_name.startswith("Hard Rain"):
      #  return "Hard Rain"
   # elif location_name.startswith("The Parish"):
      #  return "The Parish"
   # elif location_name.startswith("Cold Stream"):
      #  return "Cold Stream"
   # elif location_name.startswith("The Sacrifice"):
      #  return "The Sacrifice"
   # elif location_name.startswith("No Mercy"):
      #  return "No Mercy"
   # elif location_name.startswith("Crash Course"):
      #  return "Crash Course"
   # elif location_name.startswith("Death Toll"):
      #  return "Death Toll"
   # elif location_name.startswith("Dead Air"):
      #  return "Dead Air"
   # elif location_name.startswith("Blood Harvest"):
      #  return "Blood Harvest"
   # elif location_name.startswith("The Last Stand"):
      #  return "The Last Stand"
    return None