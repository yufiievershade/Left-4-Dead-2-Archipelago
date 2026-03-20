# L4D2 Archipelago Companion

A modern, Pythonic companion application that bridges Left 4 Dead 2 with Archipelago multiworld servers. Built with Click, Pydantic, and asyncio for a clean, maintainable codebase.

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Left 4 Dead 2 installed via Steam
- [uv](https://docs.astral.sh/uv/) for Python package management
- Your L4D2 installation path (e.g., `C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2`)

Install uv:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation

```bash
# Navigate to the companion directory
cd l4d2_companion

# Install dependencies (creates .venv automatically)
uv sync

# Configure your L4D2 installation path (required)
# Linux/macOS:
export L4D2_INSTALLATION_PATH="/path/to/Left 4 Dead 2"
# Windows PowerShell:
$env:L4D2_INSTALLATION_PATH="C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2"
# Or create a .env file in the l4d2_companion directory:
echo "L4D2_INSTALLATION_PATH=/path/to/Left 4 Dead 2" > .env
```

### Running the Application

#### GUI Mode (Default)

Launch the graphical interface - best for interactive use:

```bash
uv run l4d2-companion
```

The GUI provides:

- Visual connection status
- Campaign unlock tracker
- Colored log output
- Light/dark theme toggle

#### CLI Mode

Run headless from command line - ideal for automation:

```bash
# Basic connection
uv run l4d2-companion --cli --slot "Player1"

# With custom server
uv run l4d2-companion --cli --slot "Player1" --host "myserver.com:38281"

# With password
uv run l4d2-companion --cli --slot "Player1" --password "secret"

# Interactive mode (prompts for missing values)
uv run l4d2-companion --cli
```

### CLI Reference

```
Usage: l4d2-companion [OPTIONS]

  L4D2 Archipelago Companion Client.

  Connects Left 4 Dead 2 to Archipelago multiworld servers.

  When run without arguments, starts in GUI mode.
  When run with --cli or --slot, starts in CLI mode.

Options:
  -h, --host TEXT          Server address (host:port)  [default: archipelago.gg:38281]
  -s, --slot TEXT          Player slot name (required in CLI mode)
  -p, --password TEXT      Server password (optional)
  --cli / --gui            Force mode (default: auto-detect)
  --version                Show version and exit
  --help                   Show this message and exit
```

## Configuration

### Environment Variables

All configuration can be set via environment variables or `.env` files:

| Variable                 | Description                             | Default                |
|--------------------------|-----------------------------------------|------------------------|
| `L4D2_INSTALLATION_PATH` | **REQUIRED:** Path to L4D2 installation | (none - must be set)   |
| `L4D2_MOD_DATA_DIR`      | Directory for mod communication         | `mod_data`             |
| `L4D2_STATUS_FILE`       | Connection status file                  | `ap_status.txt`        |
| `L4D2_EVENTS_FILE`       | Game events file                        | `ap_events.txt`        |
| `L4D2_OUTGOING_FILE`     | Commands to game                        | `outgoing.log`         |
| `AP_HOST`                | Default server address                  | `archipelago.gg:38281` |
| `AP_DEBUG`               | Enable debug logging                    | `false`                |

Example `.env` file:

```bash
# Required - your L4D2 installation path
L4D2_INSTALLATION_PATH=C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2

# Optional overrides
AP_HOST=myserver.com:12345
AP_DEBUG=true
```

### Finding Your L4D2 Installation Path

The companion requires you to explicitly provide your L4D2 installation path. No auto-detection, no registry hacks.

**Windows:**

```bash
# Default Steam path (most common)
L4D2_INSTALLATION_PATH="C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2"

# Or if installed on a different drive
L4D2_INSTALLATION_PATH="D:\SteamLibrary\steamapps\common\Left 4 Dead 2"
```

**Linux (Proton):**

```bash
# Default Proton path
L4D2_INSTALLATION_PATH="~/.steam/steam/steamapps/common/Left 4 Dead 2"
```

**How to find your path:**

1. Open Steam → Library → Right-click L4D2 → Properties → Installed Files
2. Click "Browse" to open the installation folder
3. Copy the full path and set it as your `L4D2_INSTALLATION_PATH`

The companion will fail fast with a clear error if this is not set.

## Architecture

### How It Works

The companion bridges the game and Archipelago server through file-based IPC:

```
┌─────────────────┐      WebSocket      ┌──────────────────┐
│  L4D2 Companion │◄────────────────────►│ Archipelago      │
│                 │                     │ Server           │
└────────┬────────┘                     └──────────────────┘
         │
         │ File I/O
         ▼
┌─────────────────┐
│   mod_data/     │
│   ├── ap_events.txt  (location checks from game)
│   ├── outgoing.log   (commands to game)
│   └── ap_status.txt  (connection status)
└─────────────────┘
```

**Communication Flow:**

1. Game writes location checks to `ap_events.txt`
2. Companion reads checks and sends to Archipelago server
3. Server sends items from other players via WebSocket
4. Companion writes spawn commands to `outgoing.log`
5. Game reads and executes commands

### Project Structure

```
l4d2_companion/
├── __init__.py          # Package exports and public API
├── config.py            # BaseSettings configuration classes
│   ├── GameConfig       # File paths and L4D2 installation (BaseSettings)
│   └── APConfig         # Archipelago protocol config (BaseSettings)
├── definitions.py       # Game data constants (single source of truth)
│   ├── CAMPAIGNS        # Campaign data tuples
│   ├── ITEM_SPAWN_COMMANDS  # Item spawn mappings
│   ├── TRAP_SPAWN_COMMANDS  # Trap spawn mappings
│   ├── LocationType     # Location type enum
│   ├── ItemType         # Item type enum
│   └── TrapType         # Trap type enum
├── models.py            # Pydantic BaseModels
│   ├── Campaign         # Campaign data model
│   ├── ItemDefinition   # Item spawn definitions
│   ├── StarterItemPool  # Starter item configuration
│   ├── TrapSpawn        # Trap configuration
│   └── Location         # Location definition
├── client.py            # WebSocket client and game logic
│   ├── L4D2ArchipelagoClient  # Main client class
│   ├── ConnectionState        # Connection state model (BaseModel)
│   └── Packet models          # Pydantic packet validation
├── gui.py               # Tkinter GUI
│   ├── L4D2CompanionGUI       # Main GUI class
│   ├── ThemeConfiguration     # Light/dark themes (BaseModel)
│   └── WindowConfiguration    # Window settings (BaseModel)
├── files.py             # File I/O operations
├── paths.py             # Path utilities
├── main.py              # Click CLI entry point
├── tests/               # Unit tests
│   └── test_config.py   # Configuration tests
└── pyproject.toml       # Project configuration
```

## Development

### Setup Development Environment

```bash
# Install with dev dependencies
uv sync --extra dev

# Run all checks
uv run ruff check .
uv run ruff format . --check
uv run pytest
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=l4d2_companion
```

### Code Quality

```bash
# Lint code
uv run ruff check . --fix

# Format code
uv run ruff format .

# Check both
uv run ruff check . && uv run ruff format . --check
```

### Building Executable

Build a standalone Windows executable with PyInstaller (already included in dev dependencies):

```bash
# Build one-file executable (Windows GUI)
uv run pyinstaller --onefile --windowed --name l4d2-companion l4d2_companion/main.py

# Or build with console for debugging
uv run pyinstaller --onefile --name l4d2-companion l4d2_companion/main.py

# Output: dist/l4d2-companion.exe
```

## Troubleshooting

### Connection Issues

**"L4D2 installation path not configured"**

- You must set `L4D2_INSTALLATION_PATH` environment variable
- See [Configuration](#configuration) section above
- Example: `L4D2_INSTALLATION_PATH="C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2"`

**"Connection failed"**

- Verify server address and port
- Check firewall settings
- Ensure server is running and accepting connections

### Game Integration

**Items not spawning in game**

- Verify `mod_data/` directory exists in L4D2 installation
- Check that `outgoing.log` is being created
- Ensure VScript mod is properly installed

**Location checks not registering**

- Check `ap_events.txt` is being written by the game
- Verify file permissions in `mod_data/` directory
