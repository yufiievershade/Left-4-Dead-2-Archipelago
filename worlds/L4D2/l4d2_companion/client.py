"""Archipelago WebSocket client for L4D2 Companion.

Handles connection, message parsing, and game logic.
"""

import asyncio
import json
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import websockets
from l4d2_companion.config import ap_config
from l4d2_companion.definitions import (
    ITEM_SPAWN_COMMANDS,
    TRAP_SPAWN_COMMANDS,
)
from l4d2_companion.models import (
    CAMPAIGN_MODELS,
    STARTER_POOL_MODELS,
)
from l4d2_companion.files import (
    clear_events_file,
    read_events_file,
    write_status_file,
)
from pydantic import BaseModel, Field


class ConnectionState(BaseModel):
    """Tracks the state of the Archipelago connection."""

    connected: bool = False
    authenticated: bool = False
    slot: int = Field(default=-1, description="Player slot number")
    player_name: str = Field(default="", description="Player name/slot name")
    team: int = Field(default=0, description="Team number")
    seed_name: str = Field(default="", description="Multiworld seed name")
    checked_locations: set[int] = Field(default_factory=set)
    items_received: list[dict[str, Any]] = Field(default_factory=list)
    campaigns_unlocked: set[str] = Field(default_factory=set)

    class Config:
        arbitrary_types_allowed = True


class ArchipelagoPacket(BaseModel):
    """Base model for Archipelago protocol packets."""

    cmd: str


class ConnectPacket(ArchipelagoPacket):
    """Connect packet to authenticate with server."""

    cmd: str = "Connect"
    password: str | None = None
    game: str = "Left 4 Dead 2"
    name: str
    uuid: str = ""
    version: dict[str, Any] = Field(
        default_factory=lambda: {
            "major": ap_config.version_major,
            "minor": ap_config.version_minor,
            "build": ap_config.version_build,
            "class": "Version",
        }
    )
    items_handling: int = ap_config.items_handling
    tags: list[str] = Field(default_factory=lambda: [ap_config.tag])


class LocationCheckPacket(ArchipelagoPacket):
    """Send location checks to server."""

    cmd: str = "LocationChecks"
    locations: list[int]


class ReceivedItem(BaseModel):
    """An item received from the server."""

    item: str
    location: int = -1
    player: int = -1


class ServerConnectedPacket(ArchipelagoPacket):
    """Response from server after successful connection."""

    cmd: str = "Connected"
    slot: int
    team: int = 0


class ServerReceivedItemsPacket(ArchipelagoPacket):
    """Packet containing items received from server."""

    cmd: str = "ReceivedItems"
    items: list[ReceivedItem] = Field(default_factory=list)


class L4D2ArchipelagoClient:
    """WebSocket client for connecting to Archipelago server."""

    def __init__(
        self,
        mod_data_path: Path,
        on_item_received: Callable[[str], None] | None = None,
        on_location_checked: Callable[[str, int], None] | None = None,
        on_campaign_unlocked: Callable[[str], None] | None = None,
    ):
        self.mod_data_path = mod_data_path
        self.state = ConnectionState()
        self.on_item_received = on_item_received
        self.on_location_checked = on_location_checked
        self.on_campaign_unlocked = on_campaign_unlocked
        self.websocket: websockets.WebSocketClientProtocol | None = None

    async def connect(
        self,
        server_address: str,
        player_name: str,
        password: str | None = None,
    ) -> bool:
        """Connect to Archipelago server.

        Args:
            server_address: Server host:port (e.g., "archipelago.gg:12345")
            player_name: Slot name for this player
            password: Optional server password

        Returns:
            True if connected successfully, False otherwise
        """
        # Determine WebSocket protocol
        if "archipelago.gg" in server_address:
            uri = f"{ap_config.ws_protocol}{server_address}"
        else:
            uri = f"{ap_config.ws_fallback}{server_address}"

        try:
            self.websocket = await websockets.connect(uri)
            print(f"Connected to {server_address}")

            # Send connection packet using Pydantic model
            connect_packet = ConnectPacket(
                password=password or None,
                name=player_name,
            )
            packet_list = [connect_packet.model_dump(exclude_none=True)]

            await self.send_packet(packet_list)
            self.state.player_name = player_name
            self.state.connected = True

            return True

        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    async def send_packet(self, packet: list[dict[str, Any]]) -> None:
        """Send a packet to the server.

        Args:
            packet: List of command dictionaries
        """
        if self.websocket:
            await self.websocket.send(json.dumps(packet))

    async def receive_messages(self) -> None:
        """Main message loop."""
        try:
            async for message in self.websocket:
                try:
                    packets = json.loads(message)
                    for packet in packets:
                        await self.handle_packet(packet)
                except json.JSONDecodeError:
                    print(f"Failed to parse message: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            self.state.connected = False

    async def handle_packet(self, packet: dict[str, Any]) -> None:
        """Handle a single packet from the server.

        Args:
            packet: Command dictionary from server
        """
        cmd = packet.get("cmd")

        if cmd == "Connected":
            await self.handle_connected(packet)
        elif cmd == "ReceivedItems":
            await self.handle_received_items(packet)
        elif cmd == "RoomInfo":
            await self.handle_room_info(packet)
        elif cmd == "PrintJSON":
            await self.handle_print_json(packet)

    async def handle_connected(self, packet: dict[str, Any]) -> None:
        """Handle successful connection using Pydantic validation."""
        try:
            validated = ServerConnectedPacket.model_validate(packet)
            self.state.authenticated = True
            self.state.slot = validated.slot
            self.state.team = validated.team
        except Exception as e:
            print(f"Warning: Could not validate Connected packet: {e}")
            self.state.authenticated = True
            self.state.slot = packet.get("slot", -1)
            self.state.team = packet.get("team", 0)

        print(f"Authenticated as slot {self.state.slot}")
        write_status_file(self.mod_data_path, self.state.player_name, True)

        # Write starting items based on campaign count
        await self.write_starting_items()

    async def handle_received_items(self, packet: dict[str, Any]) -> None:
        """Handle received items from server using Pydantic validation."""
        try:
            validated = ServerReceivedItemsPacket.model_validate(packet)
            for item in validated.items:
                item_name = item.item
                if item_name:
                    self.state.items_received.append(item.model_dump())
                    if self.on_item_received:
                        self.on_item_received(item_name)
                    await self.process_item(item_name)
        except Exception as e:
            print(f"Error validating received items: {e}")
            # Fallback to direct parsing
            items = packet.get("items", [])
            for item in items:
                item_name = item.get("item", "")
                if item_name:
                    self.state.items_received.append(item)
                    if self.on_item_received:
                        self.on_item_received(item_name)
                    await self.process_item(item_name)

    async def handle_room_info(self, packet: dict[str, Any]) -> None:
        """Handle room information."""
        self.state.seed_name = packet.get("seed_name", "")
        print(f"Seed: {self.state.seed_name}")

    async def handle_print_json(self, packet: dict[str, Any]) -> None:
        """Handle print JSON messages (chat, notifications)."""
        message_data = packet.get("data", [])
        text = self.parse_print_json_message(message_data)
        print(f"[AP] {text}")

    def parse_print_json_message(self, data: list[dict[str, Any]]) -> str:
        """Parse PrintJSON message data into readable text."""
        parts = []
        for part in data:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                text = part.get("text", "")
                if text:
                    parts.append(text)
        return "".join(parts)

    async def process_item(self, item_name: str) -> None:
        """Process a received item.

        Args:
            item_name: Name of the received item
        """
        # Check if it's a campaign unlock
        if item_name in self.get_campaign_names():
            self.state.campaigns_unlocked.add(item_name)
            if self.on_campaign_unlocked:
                self.on_campaign_unlocked(item_name)
            return

        # Check if it's a trap
        if self.is_trap_item(item_name):
            await self.spawn_trap(item_name)
            return

        # Regular item spawn
        await self.spawn_item(item_name)

    async def spawn_item(self, item_name: str) -> None:
        """Write item spawn command to game."""
        command = ITEM_SPAWN_COMMANDS.get(item_name)
        if command:
            await self.write_to_game(command)

    async def spawn_trap(self, item_name: str) -> None:
        """Spawn a trap (special infected)."""
        trap_type = self.get_trap_type_from_name(item_name)
        if trap_type:
            command = TRAP_SPAWN_COMMANDS.get(trap_type)
            if command:
                await self.write_to_game(command)

    def is_trap_item(self, item_name: str) -> bool:
        """Check if an item is a trap."""
        return item_name.startswith("Trap: ")

    def get_trap_type_from_name(self, trap_name: str) -> str | None:
        """Extract trap type from item name."""
        match = re.match(r"Trap:\s*(\w+)", trap_name)
        return match.group(1) if match else None

    def get_campaign_names(self) -> list[str]:
        """Get list of campaign names from Pydantic models."""
        return [c.name for c in CAMPAIGN_MODELS]

    async def write_starting_items(self) -> None:
        """Write starting items based on campaign count using Pydantic models."""
        # STARTER_POOL_MODELS already imported at top of file

        # Determine appropriate item pool based on number of campaigns
        num_campaigns = len(self.get_campaign_names())

        for pool_model in STARTER_POOL_MODELS:
            if pool_model.is_applicable(num_campaigns):
                for item in pool_model.items:
                    await self.spawn_item(item)
                break

    async def write_to_game(self, command: str) -> None:
        """Write a command to the game via outgoing log file."""
        outgoing_file = self.mod_data_path / "outgoing.log"
        try:
            with open(outgoing_file, "a", encoding="utf-8") as f:
                f.write(f"{command}\n")
        except OSError as e:
            print(f"Failed to write command: {e}")

    async def check_locations(self) -> None:
        """Check for location checks from the game."""
        events_text = read_events_file(self.mod_data_path)
        if not events_text:
            return

        # Parse each line as a location check
        for line in events_text.strip().split("\n"):
            if line.startswith("CHECK:"):
                location_id_str = line.replace("CHECK:", "").strip()
                try:
                    location_id = int(location_id_str)
                    if location_id not in self.state.checked_locations:
                        self.state.checked_locations.add(location_id)

                        # Send to server
                        await self.send_location_check(location_id)

                        # Callback
                        if self.on_location_checked:
                            location_name = self.get_location_name_from_id(location_id)
                            self.on_location_checked(location_name, location_id)
                except ValueError:
                    print(f"Invalid location ID: {location_id_str}")

        # Clear events file
        clear_events_file(self.mod_data_path)

    async def send_location_check(self, location_id: int) -> None:
        """Send a location check to the server using Pydantic model."""
        packet = LocationCheckPacket(locations=[location_id])
        await self.send_packet([packet.model_dump()])

    def get_location_name_from_id(self, location_id: int) -> str:
        """Get human-readable name from location ID."""
        # This would need to be implemented based on the actual location table
        return f"Location {location_id}"

    async def run(self, server_address: str, player_name: str, password: str | None = None) -> None:
        """Main client run loop."""
        if not await self.connect(server_address, player_name, password):
            return

        # Start message receiving task
        receive_task = asyncio.create_task(self.receive_messages())

        # Start location checking loop
        check_task = asyncio.create_task(self.location_check_loop())

        # Wait for either task to complete
        done, pending = await asyncio.wait(
            [receive_task, check_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        # Cancel remaining tasks
        for task in pending:
            task.cancel()

    async def location_check_loop(self) -> None:
        """Continuously check for location updates from the game."""
        while self.state.connected:
            await self.check_locations()
            await asyncio.sleep(0.5)


async def connect_to_archipelago(
    server: str,
    slot_name: str,
    password: str | None = None,
    mod_data_path: Path | None = None,
) -> None:
    """Convenience function to connect and run the client.

    Args:
        server: Server address (host:port)
        slot_name: Player slot name
        password: Optional password
        mod_data_path: Path to mod_data directory
    """
    if mod_data_path is None:
        mod_data_path = Path.cwd() / "mod_data"

    client = L4D2ArchipelagoClient(mod_data_path)
    await client.run(server, slot_name, password)
