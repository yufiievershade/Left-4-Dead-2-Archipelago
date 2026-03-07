# This file is technically not required whatsoever
# I like to do this for organization and a few other worlds do similar
# Its helpful for grouping variables, making them easy to access, and consistent

from enum import IntEnum
from typing import NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification


# Campaign names in canonical order
# This is the single source of truth for all campaign-related logic
CAMPAIGNS = (
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

# L4D1 campaigns (for character selection logic)
L4D1_CAMPAIGNS = (
    "No Mercy",
    "Crash Course",
    "Death Toll",
    "Dead Air",
    "Blood Harvest",
    "The Sacrifice",
    "The Last Stand",
)


# These 2 make it so that the generic Location and Item types are more specific for your game
class L4D2Location(Location):
    game = "Left 4 Dead 2"


class APSkeletonItem(Item):
    game = "Left 4 Dead 2"


# I use these next 2 to convert the number you get from the options into a name
# Mainly used in Items.py for starting chapter
# Not important for a lot of games
class ChapterType(IntEnum):
    DeadCenter = 1
    ThePassing = 2
    DarkCarnival = 3
    SwampFever = 4
    HardRain = 5
    TheParish = 6
    TheSacrifice = 7
    NoMercy = 8
    CrashCourse = 9
    DeathToll = 10
    DeadAir = 11
    BloodHarvest = 12
    ColdStream = 13
    TheLastStand = 14


chapter_type_to_name = {
    ChapterType.DeadCenter: "Campaign: Dead Center",
    ChapterType.ThePassing: "Campaign: The Passing",
    ChapterType.DarkCarnival: "Campaign: Dark Carnival",
    ChapterType.SwampFever: "Campaign: Swamp Fever",
    ChapterType.HardRain: "Campaign: Hard Rain",
    ChapterType.TheParish: "Campaign: The Parish",
    ChapterType.TheSacrifice: "Campaign: The Sacrifice",
    ChapterType.NoMercy: "Campaign: No Mercy",
    ChapterType.CrashCourse: "Campaign: Crash Course",
    ChapterType.DeathToll: "Campaign: Death Toll",
    ChapterType.DeadAir: "Campaign: Dead Air",
    ChapterType.BloodHarvest: "Campaign: Blood Harvest",
    ChapterType.ColdStream: "Campaign: Cold Stream",
    ChapterType.TheLastStand: "Campaign: The Last Stand",
}


# Here is where all the stuff from the Items.py comes from
# You can add or take away anything you want but ap_code and classification are pretty important
# Adding Optional[] makes it so you dont have to include it when you create an ItemData
# Adding = x at the end adds a default to it so if you dont include it, it'll default to whatever you put after it
class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 63


# Again where all the Location.py things come from
# You can add whatever you want here as well but ap_code and region are pretty important
class LocData(NamedTuple):
    code: int
    name: str
    type: str
