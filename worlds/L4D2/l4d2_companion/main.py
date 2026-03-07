"""L4D2 Archipelago Companion - Main Entry Point.

A standalone application that bridges Left 4 Dead 2 with Archipelago multiworld servers.
"""

import asyncio
import sys
import traceback

import click
from l4d2_companion.client import L4D2ArchipelagoClient
from l4d2_companion.config import ap_config, game_config
from l4d2_companion.files import write_status_file
from l4d2_companion.gui import L4D2CompanionGUI
from l4d2_companion.paths import ensure_mod_data_directory


def run_cli(
    player_name: str,
    server_address: str,
    password: str | None,
) -> None:
    """Run in CLI mode without GUI.

    Args:
        player_name: Slot name for this player
        server_address: Server address (host:port)
        password: Server password (optional)
    """
    # Setup mod data directory
    mod_data_path = ensure_mod_data_directory()

    # Write initial status
    write_status_file(player_name, False)

    click.echo(f"Using L4D2 installation: {game_config.installation_path}")
    click.echo(f"Connecting as: {player_name} to {server_address}")

    # Create and run client
    client = L4D2ArchipelagoClient(mod_data_path)

    try:
        asyncio.run(client.run(server_address, player_name, password))
    except Exception as e:
        click.echo(f"Script crashed: {e}", err=True)
        traceback.print_exc()
    finally:
        write_status_file(player_name, False)
        input("Press Enter to exit...")


def run_gui() -> None:
    """Run with GUI."""
    # Setup mod data directory
    mod_data_path = ensure_mod_data_directory()

    # Create GUI
    gui = L4D2CompanionGUI([game_config.installation_path])

    # Track client instance
    client: L4D2ArchipelagoClient | None = None
    client_task: asyncio.Task | None = None

    def on_connect(host: str, slot: str, password: str) -> None:
        """Handle connect button."""
        nonlocal client, client_task

        client = L4D2ArchipelagoClient(
            mod_data_path=mod_data_path,
            on_item_received=lambda item: gui.log_message(f"Received: {item}", "item"),
            on_location_checked=lambda name, loc_id: gui.log_message(f"Checked: {name}", "success"),
            on_campaign_unlocked=lambda campaign: gui.update_campaign_status(campaign, True),
        )

        # Start client in background
        async def run_client():
            try:
                connected = await client.connect(host, slot, password)
                if connected:
                    gui.log_message("Connected successfully!", "success")
                    await client.receive_messages()
                else:
                    gui.log_message("Failed to connect", "error")
            except Exception as e:
                gui.log_message(f"Error: {e}", "error")
                traceback.print_exc()
            finally:
                gui.log_message("Disconnected", "info")
                write_status_file(slot, False)

        client_task = asyncio.create_task(run_client())
        write_status_file(slot, True)
        gui.log_message(f"Connecting to {host} as {slot}...", "info")

    def on_disconnect() -> None:
        """Handle disconnect button."""
        nonlocal client, client_task

        if client:
            client.state.connected = False
            client = None

        if client_task:
            client_task.cancel()
            client_task = None

        gui.log_message("Disconnected", "info")

    # Set callbacks
    gui.set_connect_callback(on_connect)
    gui.set_disconnect_callback(on_disconnect)

    # Log initial info
    gui.log_message(f"Using L4D2 installation: {game_config.installation_path}", "info")
    gui.log_message("Ready to connect. Enter server details and click Connect.", "info")

    # Run GUI
    gui.mainloop()


@click.command()
@click.option(
    "--host",
    "-h",
    default=None,
    help="Archipelago server address (host:port, default: archipelago.gg:38281)",
)
@click.option(
    "--slot",
    "-s",
    default=None,
    help="Player slot name (required in CLI mode)",
)
@click.option(
    "--password",
    "-p",
    default=None,
    help="Server password (optional)",
)
@click.option(
    "--cli/--gui",
    "use_cli",
    default=None,
    help="Force CLI mode (default: auto-detect based on arguments)",
)
@click.version_option(version="1.0.0")
def main(host: str, slot: str | None, password: str | None, use_cli: bool | None) -> None:
    """L4D2 Archipelago Companion Client.

    Connects Left 4 Dead 2 to Archipelago multiworld servers.

    When run without arguments, starts in GUI mode.
    When run with --slot, starts in CLI mode.
    """
    # Validate L4D2 installation path is configured
    if not game_config.installation_path:
        click.echo("ERROR: L4D2 installation path not configured.", err=True)
        click.echo(
            "Please set L4D2_INSTALLATION_PATH environment variable or add to .env file.",
            err=True,
        )
        click.echo(
            "Example: L4D2_INSTALLATION_PATH=C:\\Program Files (x86)\\Steam\\steamapps\\common\\Left 4 Dead 2",
            err=True,
        )
        input("Press Enter to exit...")
        sys.exit(1)

    # Determine mode: CLI if --cli flag or if slot is provided
    is_cli_mode = use_cli is True or (use_cli is not False and slot is not None)

    # Use config default if host not provided
    effective_host = host if host is not None else ap_config.host

    if is_cli_mode:
        # CLI mode - prompt for slot if not provided
        cli_slot = slot
        if not cli_slot:
            cli_slot = click.prompt("Enter your slot name")

        # Run in CLI mode
        run_cli(cli_slot, effective_host, password)
    else:
        # GUI mode
        run_gui()


if __name__ == "__main__":
    main()
