"""Tests for L4D2 Archipelago Companion.

Run with: uv run pytest
"""

from pathlib import Path

from l4d2_companion.config import APConfig, GameConfig, ap_config, game_config
from l4d2_companion.definitions import (
    CAMPAIGN_NAMES,
    CAMPAIGNS,
    ITEM_SPAWN_COMMANDS,
    TrapType,
)
from l4d2_companion.models import (
    CAMPAIGN_MODELS,
    ITEM_MODELS,
    Campaign,
    ItemDefinition,
    StarterItemPool,
    TrapSpawn,
)
from l4d2_companion.paths import get_resource_path


class TestConfig:
    """Test configuration constants."""

    def test_game_config_has_required_paths(self):
        """Test that GameConfig has required file paths."""
        config = GameConfig()
        assert config.mod_data_dir == "mod_data"
        assert config.status_file == "ap_status.txt"
        assert config.events_file == "ap_events.txt"

    def test_ap_config_has_protocol_settings(self):
        """Test that APConfig has protocol version settings."""
        config = APConfig()
        assert config.version_major == 0
        assert config.version_minor == 6
        assert config.version_build == 3
        assert config.ws_protocol == "wss://"
        assert config.tag == "AP"
        assert config.items_handling == 0b111

    def test_trap_type_enum_values(self):
        """Test TrapType enum has all special infected."""
        assert TrapType.BOOMER.value == "Boomer"
        assert TrapType.HUNTER.value == "Hunter"
        assert TrapType.TANK.value == "Tank"
        assert len(TrapType) == 8

    def test_campaigns_list_has_14_entries(self):
        """Test we have all 14 campaigns defined."""
        assert len(CAMPAIGNS) == 14
        assert len(CAMPAIGN_NAMES) == 14
        assert len(CAMPAIGN_MODELS) == 14

    def test_campaign_names_matches_campaigns(self):
        """Test campaign names match campaign definitions."""
        for i, (name, _, _, _) in enumerate(CAMPAIGNS):
            assert CAMPAIGN_NAMES[i] == name


class TestPydanticModels:
    """Test Pydantic BaseModels."""

    def test_campaign_model_creation(self):
        """Test Campaign Pydantic model."""
        campaign = Campaign(
            name="Test Campaign", num_safe_rooms=3, finale_map="test_finale"
        )
        assert campaign.name == "Test Campaign"
        assert campaign.num_safe_rooms == 3
        assert campaign.finale_map == "test_finale"
        assert not campaign.is_l4d1  # Default value
        assert campaign.has_finale

    def test_item_definition_model(self):
        """Test ItemDefinition Pydantic model."""
        item = ItemDefinition(name="Test Item", command="give test_item")
        assert item.name == "Test Item"
        assert item.command == "give test_item"

    def test_starter_item_pool_model(self):
        """Test StarterItemPool Pydantic model."""
        pool = StarterItemPool(max_campaigns=3, items=["Item1", "Item2"])
        assert pool.max_campaigns == 3
        assert len(pool.items) == 2
        assert pool.is_applicable(2)
        assert not pool.is_applicable(5)

    def test_trap_spawn_model(self):
        """Test TrapSpawn Pydantic model."""
        trap = TrapSpawn(trap_type=TrapType.BOOMER, command="z_spawn boomer")
        assert trap.trap_type == TrapType.BOOMER
        assert trap.command == "z_spawn boomer"

    def test_campaign_models_list(self):
        """Test that CAMPAIGN_MODELS are all valid Campaign instances."""
        for campaign in CAMPAIGN_MODELS:
            assert isinstance(campaign, Campaign)
            assert campaign.name in CAMPAIGN_NAMES
            assert campaign.num_safe_rooms >= 1

    def test_item_models_dict(self):
        """Test that ITEM_MODELS are all valid ItemDefinition instances."""
        for name, item in ITEM_MODELS.items():
            assert isinstance(item, ItemDefinition)
            assert item.name == name
            assert item.command.startswith("give")


class TestUtils:
    """Test utility functions."""

    def test_get_resource_path_returns_path(self):
        """Test get_resource_path returns a Path object."""
        path = get_resource_path("test.txt")
        assert isinstance(path, Path)
        assert path.name == "test.txt"

    def test_get_resource_path_handles_relative_paths(self):
        """Test get_resource_path handles relative paths correctly."""
        path = get_resource_path("mod_data/test.txt")
        assert "mod_data" in str(path)


class TestItemSpawnCommands:
    """Test item spawn command mappings."""

    def test_first_aid_kit_has_command(self):
        """Test First Aid Kit has spawn command."""
        assert "First Aid Kit" in ITEM_SPAWN_COMMANDS
        assert "give first_aid_kit" in ITEM_SPAWN_COMMANDS["First Aid Kit"]

    def test_all_primary_weapons_have_commands(self):
        """Test all primary weapons have spawn commands."""
        weapons = [
            "Pump Shotgun",
            "Submachine Gun",
            "M-16",
            "AK-47",
            "Hunting Rifle",
            "Sniper Rifle",
        ]
        for weapon in weapons:
            assert weapon in ITEM_SPAWN_COMMANDS, f"{weapon} missing command"


class TestPathOperations:
    """Test path operations."""

    def test_mod_data_path_computed_correctly(self):
        """Test that mod_data_path is computed from installation_path and mod_data_dir."""
        # The mod_data_path should be installation_path / mod_data_dir
        expected_path = game_config.installation_path / game_config.mod_data_dir
        assert game_config.mod_data_path == expected_path
