from worlds.generic.Rules import add_rule
from typing import TYPE_CHECKING
from .Types import CAMPAIGNS

if TYPE_CHECKING:
    from . import L4D2World


def set_rules(world: "L4D2World"):
    player = world.player
    options = world.options
    multiworld = world.multiworld

    # Access rules for campaign entrances
    # These rules gate access to campaigns from the main menu.
    for campaign in CAMPAIGNS:
        entrance_name = f"Menu to {campaign}"
        # Add rule requiring the corresponding campaign item
        add_rule(
            multiworld.get_entrance(entrance_name, player),
            lambda state, c=campaign: state.has(f"Campaign: {c}", player),
        )

    # This rule dictates when the Victory location itself can be "checked".
    # Use the goal option to determine how many campaigns are required
    required_campaigns = options.goal.value
    if required_campaigns >= len(CAMPAIGNS):
        # If goal is 14 or more, require all campaigns
        add_rule(
            multiworld.get_location("Beat Campaigns", player),
            lambda state: all(state.has(f"Campaign: {c}", player) for c in CAMPAIGNS),
        )
    else:
        # Otherwise, require the specified number of any campaigns
        add_rule(
            multiworld.get_location("Beat Campaigns", player),
            lambda state: sum(
                1 for c in CAMPAIGNS if state.has(f"Campaign: {c}", player)
            )
            >= required_campaigns,
        )

    # Final Victory condition for the world
    # Consider the world complete when the player owns goal number of campaign unlock items.
    def has_required_campaigns(state):
        owned_campaigns = sum(
            1 for c in CAMPAIGNS if state.has(f"Campaign: {c}", player)
        )
        return owned_campaigns >= required_campaigns

    multiworld.completion_condition[player] = has_required_campaigns
