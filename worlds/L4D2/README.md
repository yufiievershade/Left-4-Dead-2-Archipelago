# Left 4 Dead 2 Archipelago World

An Archipelago world implementation for Left 4 Dead 2, enabling multiworld randomization support. Receive items from other players while fighting through zombie campaigns!

## Overview

This world randomizes items and locations across Left 4 Dead 2's 14 campaigns, allowing players to:

- **Receive items** from other Archipelago players while playing through safe rooms
- **Send items** to other players by reaching safe rooms and completing finales
- **Cooperate** with other L4D2 players in the same multiworld
- **Experience** a fresh take on the classic cooperative zombie shooter

## How It Works

The Left 4 Dead 2 Archipelago integration works through a companion application that bridges the game with the Archipelago server:

1. **Safe Rooms = Locations**: Each safe room in every campaign is a checkable location
2. **Campaign Unlocks = Progression Items**: Receiving a campaign item unlocks that campaign's entrance
3. **Weapons & Supplies = Useful Items**: Medical items, weapons, throwables sent from other worlds
4. **Traps = Special Infected**: Other players can send you surprise infected attacks!

### The Companion App

The companion app in `l4d2_companion/` is a standalone Python application that:

- Connects to the Archipelago server via WebSocket
- Monitors the Left 4 Dead 2 installation for game events
- Communicates with the game through mod files (in `mod_data/` folder)
- Provides a GUI for easy connection (or can run headless with CLI args)

**Note**: The companion app currently only supports Windows due to Windows Registry lookups for Steam paths.

## Quick Start

### Prerequisites

1. **Left 4 Dead 2** installed via Steam
2. **Python 3.11+** with required packages:

   ```bash
   pip install websockets
   ```

3. **Archipelago Generator** or access to an Archipelago server

### Setup Steps

1. **Generate a Game**:
   - Use the Archipelago Launcher (`py Launcher.py`) to create a YAML template
   - Or use `py Generate.py` directly with your YAML file
   - Make sure your YAML includes Left 4 Dead 2 as one of the games

2. **Launch the Companion App**:

   ```bash
   cd worlds/L4D2/l4d2_companion
   python main.py
   ```

3. **Connect to Server**:
   - Enter your slot name (from the generated game)
   - Enter the server address (e.g., `archipelago.gg:12345` or `localhost:38281`)
   - Enter password if required
   - Click "Connect"

4. **Start Left 4 Dead 2**:
   - Launch the game normally through Steam
   - The companion app will automatically detect the game running

5. **Play!**:
   - Progress through safe rooms to send items to other players
   - Receive items from other players at safe rooms
   - Complete the required number of campaigns to win!

## Configuration Options

When creating your YAML file, you can customize:

- **Start with Campaign**: Choose which campaign is unlocked at the start
- **All Campaigns Unlocked at Start**: Start with all campaigns available
- **Death Link**: When enabled, dying sends a death signal to other Death Link-enabled players
- **Goal**: Number of campaigns required to win (1-14)
- **Trap Item Count**: How many trap items (special infected spawns) to include

## File Structure

```
worlds/L4D2/
├── __init__.py           # Main world implementation
├── Items.py              # Item definitions and item groups
├── Locations.py          # Location definitions (safe rooms, finales)
├── location_mapping.py   # Map location names to in-game map names
├── Options.py            # Player-configurable options
├── Regions.py            # Region connections and campaign access
├── Rules.py              # Logic rules (campaign requirements, victory)
├── Types.py              # Type definitions (CAMPAIGNS, L4D1_CAMPAIGNS, etc.)
├── DEV_GUIDE.md          # Development guide
├── README.md             # This file
├── ThirdPartyProgramStuff/
│   ├── ap_companion_clean.py  # Companion app (Windows only)
│   └── mod_data/              # Runtime data folder
└── .gitignore
```

## Troubleshooting

### Companion App Can't Find L4D2

The companion app auto-detects common Steam installation paths. If it can't find your installation:

1. Check that L4D2 is installed via Steam
2. Try running the companion app as administrator
3. Common paths are checked: `C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2`

### Connection Issues

- Ensure the server address includes the port (e.g., `archipelago.gg:12345`)
- For archipelago.gg, use the full address with slot number
- Check that your slot name exactly matches the one in the generated game

### Items Not Appearing In-Game

1. Make sure the companion app shows as "Connected"
2. Verify L4D2 is actually running (not just Steam launched)
3. Check the companion app logs for errors
4. Try restarting the companion app after L4D2 is already running

### Generation Errors

If you get errors during `Generate.py`:

- Check that your YAML file syntax is valid
- Verify the world is properly installed in `worlds/L4D2/`
- Look for specific error messages in the terminal output

## For Developers

See [DEV_GUIDE.md](DEV_GUIDE.md) for a comprehensive development guide covering:

- Getting started with AP world development
- Git/GitHub basics
- Command line usage
- Troubleshooting and debugging
- Code structure and architecture
