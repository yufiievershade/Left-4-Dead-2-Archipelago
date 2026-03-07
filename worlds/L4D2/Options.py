from typing import Any
from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions


class L4D2DeathLink(Toggle):
    """
    If enabled, when a player in the multiworld dies, everyone else dies.
    A Left 4 Dead 2-style team wipe.
    """

    display_name = "DeathLink"
    default = False


class StartWithCampaign(Choice):
    """
    Determines which campaign is unlocked from the start.
    This does not change the starting map, but which campaign is logically available.
    """

    display_name = "Start with Campaign"
    option_dead_center = 1
    option_the_passing = 2
    option_dark_carnival = 3
    option_swamp_fever = 4
    option_hard_rain = 5
    option_the_parish = 6
    option_the_sacrifice = 7
    option_no_mercy = 8
    option_crash_course = 9
    option_death_toll = 10
    option_dead_air = 11
    option_blood_harvest = 12
    option_the_last_stand = 13
    option_cold_stream = 14
    default = option_dead_center


class AllCampaignsStart(Toggle):
    """
    Start with all campaigns unlocked. Overrides 'Start with Campaign'.
    """

    display_name = "All Campaigns Unlocked at Start"
    default = False


class L4D2Goal(Range):
    """
    Number of campaigns required to complete the game.
    """

    display_name = "Campaigns to Complete"
    range_start = 1
    range_end = 14
    default = 3


class TrapItemCount(Range):
    """
    Number of trap items to add to the item pool.
    """

    display_name = "Trap Items in Pool"
    range_start = 0
    range_end = 20
    default = 5


@dataclass
class L4D2Options(PerGameCommonOptions):
    death_link: L4D2DeathLink
    starting_campaign: StartWithCampaign
    all_campaigns_start: AllCampaignsStart
    goal: L4D2Goal
    trap_count: TrapItemCount


# Organize your options into groups
l4d2_option_groups: dict[str, list[Any]] = {
    "General": [StartWithCampaign, AllCampaignsStart, L4D2DeathLink],
    "Goal": [L4D2Goal],
    "Traps": [TrapItemCount],
}
