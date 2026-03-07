# L4D2 Archipelago Quick Start Guide

**New to L4D2 Archipelago? Start here!** This guide will get you up and running in under 5 minutes.

## What You Need

1. **Left 4 Dead 2** installed via Steam
2. **Python 3.11+** and the `uv` package manager
3. An Archipelago YAML file (or access to an Archipelago server)

## Step 1: Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Step 2: Get Your L4D2 Path

Find your L4D2 installation folder:

- Open Steam → Library → Right-click L4D2 → Properties → Installed Files
- Click "Browse" to open the installation folder
- Copy the full path

**Windows example:** `C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2`
**Linux example:** `~/.steam/steam/steamapps/common/Left 4 Dead 2`

## Step 3: Generate Your Game

If you haven't already, generate a game with L4D2:

```bash
# From the Archipelago root directory
py Launcher.py
# Select "Generate Template Options" and create a YAML
# Then generate the game
py Generate.py
```

## Step 4: Launch the Companion App

```bash
# Navigate to the companion directory
cd worlds/L4D2/l4d2_companion

# Install dependencies
uv sync

# Set your L4D2 path (replace with your actual path)
# Windows PowerShell:
$env:L4D2_INSTALLATION_PATH="C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2"
# Or Linux/macOS:
export L4D2_INSTALLATION_PATH="/path/to/Left 4 Dead 2"

# Launch the GUI
uv run l4d2-companion
```

## Step 5: Connect and Play

1. Enter your **slot name** (from the generated game)
2. Enter the **server address** (e.g., `archipelago.gg:12345`)
3. Click **Connect**
4. Start Left 4 Dead 2
5. Play! You'll receive items from other players at safe rooms.

## CLI Alternative

Prefer command line? Use the `--cli` flag:

```bash
uv run l4d2-companion --cli --slot "YourSlotName" --host "archipelago.gg:12345"
```

## Troubleshooting

**"L4D2 installation path not configured"**
→ Make sure you set the `L4D2_INSTALLATION_PATH` environment variable

**Can't connect to server**
→ Check that your slot name exactly matches the YAML

**Items not appearing in game**
→ Ensure L4D2 is running (not just Steam) and the companion shows "Connected"

For more detailed help, see [l4d2_companion/README.md](l4d2_companion/README.md).
