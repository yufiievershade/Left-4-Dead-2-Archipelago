"""Pydantic data models for L4D2 Archipelago Companion.

This module contains all Pydantic BaseModels used throughout the application
for type-safe data validation and serialization.
"""

from l4d2_companion.definitions import (
    CAMPAIGNS,
    CHARACTERS_L4D1,
    CHARACTERS_L4D2,
    ITEM_SPAWN_COMMANDS,
    STARTER_ITEM_POOLS,
    TrapType,
)
from pydantic import BaseModel


class Campaign(BaseModel):
    """A L4D2 campaign definition."""

    name: str
    num_safe_rooms: int
    finale_map: str
    is_l4d1: bool = False

    @property
    def has_finale(self) -> bool:
        """Check if this campaign has a finale location."""
        return self.num_safe_rooms > 0

    def get_location_names(
        self, characters: list[str] | None = None
    ) -> list[str]:
        """Generate location names for this campaign.

        Args:
            characters: List of character names (uses L4D1 or L4D2 characters based on is_l4d1)

        Returns:
            List of location names
        """
        if characters is None:
            characters = CHARACTERS_L4D1 if self.is_l4d1 else CHARACTERS_L4D2

        locations: list[str] = []
        # Generate safe room locations
        for safe_room in range(1, self.num_safe_rooms + 1):
            for character in characters:
                locations.append(
                    f"Campaign: {self.name} Safe Room {safe_room}: {character}"
                )
        # Add finale if exists
        if self.has_finale:
            for character in characters:
                locations.append(
                    f"Campaign: {self.name} Finale: {character}"
                )
        return locations


class ItemDefinition(BaseModel):
    """Definition of a game item with spawn command."""

    name: str
    command: str


class StarterItemPool(BaseModel):
    """Configuration for starter items based on campaign count."""

    max_campaigns: int
    items: list[str]

    def is_applicable(self, num_campaigns: int) -> bool:
        """Check if this pool applies to a given campaign count."""
        return num_campaigns <= self.max_campaigns


class TrapSpawn(BaseModel):
    """Trap (special infected) spawn configuration."""

    trap_type: TrapType
    command: str


class Location(BaseModel):
    """A game location definition."""

    name: str
    location_type: str = "Safe Room"
    id: int | None = None
    campaign: str | None = None


# Convert tuple-based data to Pydantic models
CAMPAIGN_MODELS: list[Campaign] = [
    Campaign(name=name, num_safe_rooms=num_safe, finale_map=finale, is_l4d1=is_l4d1)
    for name, num_safe, finale, is_l4d1 in CAMPAIGNS
]


# Build item definition models from ITEM_SPAWN_COMMANDS
ITEM_MODELS: dict[str, ItemDefinition] = {
    name: ItemDefinition(name=name, command=cmd)
    for name, cmd in ITEM_SPAWN_COMMANDS.items()
}


# Build starter item pool models
STARTER_POOL_MODELS: list[StarterItemPool] = [
    StarterItemPool(max_campaigns=max_c, items=pool)
    for max_c, pool in STARTER_ITEM_POOLS
]


# Build trap spawn models
TRAP_MODELS: dict[str, TrapSpawn] = {
    trap_type.value: TrapSpawn(trap_type=trap_type, command=cmd)
    for trap_type, cmd in [
        (TrapType.BOOMER, "z_spawn boomer"),
        (TrapType.HUNTER, "z_spawn hunter"),
        (TrapType.SMOKER, "z_spawn smoker"),
        (TrapType.TANK, "z_spawn tank"),
        (TrapType.WITCH, "z_spawn witch"),
        (TrapType.CHARGER, "z_spawn charger"),
        (TrapType.JOCKEY, "z_spawn jockey"),
        (TrapType.SPITTER, "z_spawn spitter"),
    ]
}
