# Left 4 Dead 2 Archipelago World

An Archipelago world implementation for Left 4 Dead 2, enabling multiworld randomization support. Receive items from other players while fighting through zombie campaigns!

## Getting Started

- **New to L4D2 Archipelago?** The [Quick Start Guide](QUICKSTART.md) provides a step-by-step walkthrough to get you playing in under five minutes.
- **Already familiar?** The companion app lives in `l4d2_companion/` - see the [companion README](l4d2_companion/README.md) for detailed reference.
- **Want to contribute?** See [DEV_GUIDE.md](DEV_GUIDE.md) for development setup, Git workflows, and code architecture.

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

The companion app in `l4d2_companion/` is a modern Python application that:

- Connects to Archipelago servers via WebSocket
- Monitors game events and communicates through mod files
- Provides both GUI and CLI interfaces
- Works cross-platform with explicit configuration
- Built with Click, Pydantic, and asyncio

For setup instructions, see [QUICKSTART.md](QUICKSTART.md).

## Documentation

| Document                                             | Description                                    |
|------------------------------------------------------|------------------------------------------------|
| [QUICKSTART.md](QUICKSTART.md)                       | Step-by-step guide to get playing in 5 minutes |
| [l4d2_companion/README.md](l4d2_companion/README.md) | Detailed companion app documentation           |
| [DEV_GUIDE.md](DEV_GUIDE.md)                         | Development guide for contributors             |

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
├── Options.py            # Player-configurable options
├── Regions.py            # Region connections and campaign access
├── Rules.py              # Logic rules (campaign requirements, victory)
├── Types.py              # Type definitions (CAMPAIGNS, L4D1_CAMPAIGNS, etc.)
├── QUICKSTART.md         # Quick start guide for new users
├── DEV_GUIDE.md          # Development guide
├── README.md             # This file
├── l4d2_companion/       # Modern Python companion app
│   ├── README.md         # Detailed companion documentation
│   ├── main.py           # Entry point
│   └── ...
├── scripts/              # Utility scripts
│   ├── debug_location_check.py
│   ├── location_checker.py
│   └── location_mapping.py
└── ThirdPartyProgramStuff/
    └── mod_data/         # Runtime data folder
```

## Troubleshooting

### "I need help getting started"

→ See [QUICKSTART.md](QUICKSTART.md) for detailed setup steps

### Companion App Issues

→ See [l4d2_companion/README.md#troubleshooting](l4d2_companion/README.md#troubleshooting)

### Connection Problems

- Ensure the server address includes the port (e.g., `archipelago.gg:12345`)
- Check that your slot name exactly matches the one in the generated game
- See companion README for detailed troubleshooting
