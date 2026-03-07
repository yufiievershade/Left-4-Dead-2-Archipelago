---
updated: 2026-03-06
---

# Fork Differences from Upstream Archipelago

## Overview

This fork (`yufiievershade/Left-4-Dead-2-Archipelago`) is based on `ArchipelagoMW/Archipelago` and primarily adds **Left 4 Dead 2 (L4D2)** support while removing several upstream features.

## Main Additions

### New Game World: Left 4 Dead 2

- **Location**: `worlds/L4D2/`
- **Purpose**: Adds Archipelago randomizer support for the cooperative first-person shooter
- **Key Files**:
  - `__init__.py`, `Items.py`, `Locations.py`, `Options.py`, `Regions.py`, `Rules.py`, `Types.py`
  - `ThirdPartyProgramStuff/` - Companion application and mod integration
  - Helper scripts: `location_checker.py`, `location_mapping.py`, `debug_location_check.py`
  - `README.md` - Development documentation

## Major Removals from Upstream

### 1. Rule Builder Module

- **Removed**: `rule_builder/` directory entirely
- **Files**: `cached_world.py`, `options.py`, `rules.py`, `__init__.py`
- **Docs**: `docs/rule builder.md`
- **Tests**: `test/general/test_rule_builder.py`

### 2. Complete Game Worlds Removed

- `worlds/apquest/` - APQuest mini-game
- `worlds/earthbound/` - EarthBound (SNES) support
- `worlds/satisfactory/` - Satisfactory support

### 3. CI/Development Tools

- `ci-requirements.txt`
- `mypy.ini`
- `ruff.toml`
- `.run/Build APWorlds.run.xml` (PyCharm run configuration)

### 4. archipelago.json Files

Many worlds lost their `archipelago.json` files (metadata/configuration), including:

- celeste64, dkc3, ladx, landstalker, messenger, mlss, oot, paint, sa2b
- sc2, smw, soe, timespinner, wargroove, witness, yachtdice, yoshisisland
- stardew_valley, tloz

## Core vs Game-Specific Changes

### Core Archipelago Files (minor changes)

- `BaseClasses.py` - Minor formatting
- `MultiServer.py`, `NetUtils.py`, `Options.py`, `Utils.py` - Mostly whitespace
- `worlds/__init__.py`, `worlds/AutoWorld.py` - Structural adjustments

### Build/Workflow Changes

- `.github/workflows/build.yml` - Reverted to older AppImage sources
- `.github/workflows/release.yml` - Removed PopTracker fork references
- `.github/workflows/docker.yml` - Branch filter changed to `*`

### Game-Specific Changes

- `worlds/ladx/LinksAwakeningClient.py` → Moved to root
- `worlds/kh2/ClientStuff/WorldLocations.py` → Moved location
- `worlds/celeste64/LICENSE` → Moved to `worlds/L4D2/LICENSE`
- Various Stardew Valley file reorganizations

## Summary

This fork is a **specialized L4D2 development fork** that:

1. ✅ Adds complete L4D2 Archipelago support with companion tools
2. ❌ Removes the rule_builder module system
3. ❌ Removes 3 complete game worlds (APQuest, EarthBound, Satisfactory)
4. ❌ Removes various CI tooling and world metadata files

The fork appears to be based on an older upstream version and has diverged significantly, making it unsuitable for general Archipelago use but specialized for L4D2 development.

---

*Generated: 2026-03-06*
*Comparing: `upstream/main` → `origin/main`*
