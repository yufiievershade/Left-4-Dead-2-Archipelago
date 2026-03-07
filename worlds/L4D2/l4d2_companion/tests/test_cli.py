"""Tests for Click CLI interface.

Run with: uv run pytest tests/test_cli.py -v
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner
from l4d2_companion.main import main


@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_l4d2_paths(tmp_path):
    """Create a mock L4D2 installation path."""
    install_path = tmp_path / "Left 4 Dead 2"
    install_path.mkdir()
    return [MagicMock(path=install_path, source="test", is_valid=True)]


class TestClickCLI:
    """Test Click-based CLI interface."""

    def test_help_shows_usage(self, runner):
        """Test that --help shows proper usage information."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "L4D2 Archipelago Companion Client" in result.output
        assert "--host" in result.output
        assert "--slot" in result.output
        assert "--password" in result.output
        assert "--cli" in result.output

    def test_version_shows_version(self, runner):
        """Test that --version shows version."""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_default_host_is_set(self, runner):
        """Test that default host is set."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "archipelago.gg:38281" in result.output

    @patch("l4d2_companion.main.find_l4d2_installations")
    @patch("l4d2_companion.main.run_gui")
    def test_no_args_launches_gui(self, mock_run_gui, mock_find, runner, mock_l4d2_paths):
        """Test that running without arguments launches GUI."""
        mock_find.return_value = mock_l4d2_paths

        result = runner.invoke(main, [])

        assert result.exit_code == 0
        mock_run_gui.assert_called_once()

    @patch("l4d2_companion.main.find_l4d2_installations")
    @patch("l4d2_companion.main.run_cli")
    def test_cli_flag_runs_cli_mode(self, mock_run_cli, mock_find, runner, mock_l4d2_paths):
        """Test that --cli flag runs CLI mode."""
        mock_find.return_value = mock_l4d2_paths

        result = runner.invoke(main, ["--cli", "--slot", "Player1"])

        assert result.exit_code == 0
        mock_run_cli.assert_called_once()
        # Check the arguments passed to run_cli
        call_args = mock_run_cli.call_args
        assert call_args[0][0] == "Player1"  # slot
        assert call_args[0][1] == "archipelago.gg:38281"  # host (default)
        assert call_args[0][2] is None  # password

    @patch("l4d2_companion.main.find_l4d2_installations")
    @patch("l4d2_companion.main.run_cli")
    def test_slot_arg_alone_runs_cli_mode(self, mock_run_cli, mock_find, runner, mock_l4d2_paths):
        """Test that providing --slot runs CLI mode even without --cli flag."""
        mock_find.return_value = mock_l4d2_paths

        result = runner.invoke(main, ["--slot", "Player1", "--host", "custom.server:12345"])

        assert result.exit_code == 0
        mock_run_cli.assert_called_once()
        call_args = mock_run_cli.call_args
        assert call_args[0][0] == "Player1"
        assert call_args[0][1] == "custom.server:12345"

    @patch("l4d2_companion.main.find_l4d2_installations")
    @patch("l4d2_companion.main.run_cli")
    def test_cli_with_all_options(self, mock_run_cli, mock_find, runner, mock_l4d2_paths):
        """Test CLI mode with all options."""
        mock_find.return_value = mock_l4d2_paths

        result = runner.invoke(
            main,
            [
                "--cli",
                "--host", "myserver.com:55555",
                "--slot", "MyPlayer",
                "--password", "secret123",
            ],
        )

        assert result.exit_code == 0
        mock_run_cli.assert_called_once()
        call_args = mock_run_cli.call_args
        assert call_args[0][0] == "MyPlayer"
        assert call_args[0][1] == "myserver.com:55555"
        assert call_args[0][2] == "secret123"

    @patch("l4d2_companion.main.find_l4d2_installations")
    @patch("l4d2_companion.main.run_cli")
    def test_cli_prompts_for_missing_slot(self, mock_run_cli, mock_find, runner, mock_l4d2_paths):
        """Test that CLI mode prompts for slot if not provided."""
        mock_find.return_value = mock_l4d2_paths

        result = runner.invoke(main, ["--cli"], input="TestPlayer\n")

        assert result.exit_code == 0
        mock_run_cli.assert_called_once()
        call_args = mock_run_cli.call_args
        assert call_args[0][0] == "TestPlayer"

    @patch("l4d2_companion.main.find_l4d2_installations")
    def test_exits_when_no_l4d2_found(self, mock_find, runner):
        """Test that application exits when L4D2 is not found."""
        mock_find.return_value = []

        result = runner.invoke(main, [])

        assert result.exit_code == 1
        assert "Could not find L4D2 installation" in result.output

    @patch("l4d2_companion.main.find_l4d2_installations")
    @patch("l4d2_companion.main.run_gui")
    def test_gui_flag_explicit(self, mock_run_gui, mock_find, runner, mock_l4d2_paths):
        """Test that --gui flag launches GUI even with slot provided."""
        mock_find.return_value = mock_l4d2_paths

        result = runner.invoke(main, ["--gui", "--slot", "Player1"])

        assert result.exit_code == 0
        mock_run_gui.assert_called_once()


class TestCLIArguments:
    """Test CLI argument parsing and validation."""

    def test_short_options_work(self, runner):
        """Test that short options -h, -s, -p work."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "-h, --host" in result.output
        assert "-s, --slot" in result.output
        assert "-p, --password" in result.output

    def test_host_option_accepts_custom_value(self, runner):
        """Test that --host accepts custom values."""
        with (
            patch("l4d2_companion.main.find_l4d2_installations") as mock_find,
            patch("l4d2_companion.main.run_cli") as mock_run_cli,
        ):
            mock_find.return_value = [MagicMock(path=Path("/fake/l4d2"), source="test")]

            result = runner.invoke(main, ["--cli", "--slot", "Test", "--host", "192.168.1.1:38281"])

            assert result.exit_code == 0
            call_args = mock_run_cli.call_args
            assert call_args[0][1] == "192.168.1.1:38281"
