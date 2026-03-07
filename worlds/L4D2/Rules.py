from worlds.generic.Rules import add_rule
from typing import TYPE_CHECKING
from BaseClasses import MultiWorld

if TYPE_CHECKING:
    from . import L4D2World


# This is the last big thing to do (at least for me)
# This is where you add item
# These are omega simplified rules
# There are a ton of different ways you can add rules from amount of items you need to optional items
# Theres also difficulty options and a bunch others
# Id suggest going through a bunch of different ap worlds and seeing how they do the rules
# Even better if its a game you know a lot about and can tell what you need to get to certain locations
def set_rules(world: "L4D2World"):
    player = world.player
    options = world.options

    # 1. Access rules for campaign entrances
    # These rules gate access to campaigns from the main menu.
    campaign_names = [
        "Dead Center",
        "The Passing",
        "Dark Carnival",
        "Swamp Fever",
        "Hard Rain",
        "The Parish",
        "The Sacrifice",
        "No Mercy",
        "Crash Course",
        "Death Toll",
        "Dead Air",
        "Blood Harvest",
        "The Last Stand",
    ]

    for campaign in campaign_names:
        entrance_name = f"Menu to {campaign}"
        # It adds a lambda function that checks for the corresponding campaign item.
        # The `c=campaign` is a closure to capture the correct campaign name in each iteration.
        add_rule(
            MultiWorld.get_entrance(entrance_name, player),
            lambda state, c=campaign: state.has(f"Campaign: {c}", player),
        )

    # 3. Rule for the final Victory location
    # This rule dictates when the Victory location itself can be "checked".
    # Use the goal option to determine how many campaigns are required
    required_campaigns = options.goal.value
    if required_campaigns >= len(campaign_names):
        # If goal is 14 or more, require all campaigns
        add_rule(
            MultiWorld.get_location("Beat Campaigns", player),
            lambda state: all(
                state.has(f"Campaign: {c}", player) for c in campaign_names
            ),
        )
    else:
        # Otherwise, require the specified number of any campaigns
        add_rule(
            MultiWorld.get_location("Beat Campaigns", player),
            lambda state: sum(
                1 for c in campaign_names if state.has(f"Campaign: {c}", player)
            )
            >= required_campaigns,
        )

    # 4. Final Victory condition for the world
    # Consider the world complete when the player owns goal number of campaign unlock items.
    # Finale-based tracking is handled client-side; this ensures AP marks the slot finished cleanly.
    def has_required_campaigns(state):
        owned_campaigns = sum(
            1 for c in campaign_names if state.has(f"Campaign: {c}", player)
        )
        return owned_campaigns >= required_campaigns

    MultiWorld.completion_condition[player] = has_required_campaigns
