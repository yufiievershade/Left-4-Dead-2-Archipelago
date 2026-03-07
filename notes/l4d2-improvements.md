---
updated: 2026-03-06
---

# L4D2 World Improvement Suggestions

Comparison of L4D2 world implementation against Archipelago documentation guidelines.

## Critical Issues

### Missing Required Documentation

- **Issue**: No game info doc (`en_Left 4 Dead 2.md`) in `docs/` directory
- **Issue**: Setup guide referenced in `__init__.py` as `setup_en.md` with URL `setup/en` doesn't exist
- **Doc Reference**: [adding games.md#hard-requirements] - "game folder has at least one game_info doc" and "at least one setup doc"
- **Impact**: Web host won't display proper documentation

### Missing Unit Tests

- **Issue**: No `/test` directory in L4D2 world
- **Doc Reference**: [world api.md#tests] - "Each world is expected to include unit tests that cover its logic"
- **Impact**: Logic bugs can regress without detection
- **Suggestion**: Create `worlds/L4D2/test/` package with test cases

## Code Quality Issues

### Items.py - Major Refactoring Opportunity

- **Status**: ✅ COMPLETED - Refactored to data-driven structure
- **Current State**: 181 lines → 205 lines, but now includes populated `item_groups`
- **Issues Resolved**:
  - ✅ Hardcoded IDs → Auto-generated sequential IDs via `ITEM_DEFINITIONS`
  - ✅ Manual list appends → Generator function `_generate_full_item_list()`
  - ✅ No data structure → `ITEM_DEFINITIONS` list with (name, category, quantity)
- **Bonus**: Populated `item_groups` with logical categories (weapons, medical, campaigns, traps, etc.)
- **Result**: More maintainable, easier to add/modify items

**New Structure**:
```python
ITEM_DEFINITIONS = [
    ("Dead Center", "progression", 1),
    ("First Aid Kit", "useful", 5),
    # ... auto-generates dictionaries and item pool
]
```

### **init**.py - Massive Match Statement

- **Status**: ✅ COMPLETED - Refactored from 162 lines to 11 lines using dictionary mapping
- **Issue**: Lines 155-317 contained huge `match` statement for item classification
- **Problems**:
  - 162 lines of repetitive case statements
  - Hard to maintain (every new item needs a new case)
  - Not data-driven
- **Solution**: Created `ITEM_CLASSIFICATIONS` dictionary mapping at top of file
- **Result**: ~64 lines saved (15% reduction in file size)

**Before**:

```python
match name:
    case "Pump Shotgun":
        classification = ItemClassification.useful
    # ... 160 more lines ...
```

**After**:

```python
classification = ITEM_CLASSIFICATIONS[name]
```

### Rules.py - API Usage

- **Status**: ✅ COMPLETED - Fixed to use proper instance access
- **Issue**: Used `MultiWorld.get_entrance()` and `MultiWorld.get_location()` through class
- **Solution**: Now uses `world.multiworld.get_entrance()` and `world.multiworld.get_location()`
- **Also Fixed**: `multiworld.completion_condition[player]` instead of `MultiWorld.completion_condition[player]`

## Incomplete Features

### Option Groups Not Connected

- **Status**: ✅ COMPLETED - Connected to WebWorld
- **Before**: `l4d2_option_groups` defined in Options.py but never assigned
- **Fix**: Added `option_groups = l4d2_option_groups` to L4D2Web class in __init__.py
- **Result**: Options now organized into groups on webhost:
  - General: StartWithCampaign, AllCampaignsStart, L4D2DeathLink
  - Goal: L4D2Goal
  - Traps: TrapItemCount

### Item Name Groups Empty

- **Status**: ✅ COMPLETED - Populated during Items.py refactor
- **Before**: `item_groups = {}` (empty dict)
- **After**: Populated with logical groups:
  - `weapons`: All firearms and pistols
  - `melee_weapons`: All melee weapons
  - `medical`: Medkits, pills, defibs, etc.
  - `throwables`: Molotov, pipe bombs, bile bombs
  - `campaigns`: All 14 campaign items
  - `traps`: All 8 special infected traps
  - `junk`: Broken/useless items
  - `scavenge`: Gas cans, propane tanks, etc.
- **Benefit**: Enables `!hint` group syntax and better organization

### Bug Report Page Missing

- **Issue**: No `bug_report_page` in WebWorld
- **Doc Reference**: [world api.md#webworld-class]
- **Suggestion**: Add link to GitHub issues or Discord

### Missing get_filler_item_name

- **Status**: ✅ COMPLETED - Implemented in L4D2World class
- **Implementation**: Returns random item from `junk_items` (broken weapons, useless items)
- **Benefit**: Archipelago now uses proper filler items instead of any random item

## Style Guide Violations

### String Quotes

- **Issue**: Some strings use single quotes instead of double
- **Doc Reference**: [style.md#python-code] - "Strings in core code will be 'strings'... Strings in worlds should use double quotes as well"
- **Location**: `Items.py`, `__init__.py`, various files

### Type Annotations

- **Status**: ✅ COMPLETED - Converted old-style typing imports to new style
- **Changes Made**:
  - `Options.py`: `Dict[str, List[Any]]` → `dict[str, list[Any]]`
  - `Locations.py`: `Dict[str, LocData]` → `dict[str, LocData]`, `Dict[str, int]` → `dict[str, int]`
  - `__init__.py`: `Dict[str, object]` → `dict[str, object]`
- **Result**: Uses Python 3.9+ built-in generic types as recommended by Archipelago style guide

### Line Length

- **Potential Issue**: Some lines may exceed 120 characters
- **Doc Reference**: [style.md#generic] - "120 character per line for all source files"
- **Needs Review**: Long strings in `__init__.py`, `Locations.py`

### Docstrings

- **Issue**: Missing reST-style docstrings on some methods
- **Doc Reference**: [style.md#python-code] - "New classes, attributes, and methods in core code should have docstrings"
- **Doc Reference**: [world api.md#docstrings] - "They are assigned by writing a string without any assignment right below a definition"
- **Locations**:
  - `create_item()` method
  - `create_items()` method
  - `fill_slot_data()` method
  - Most helper functions in `Items.py`, `Locations.py`

## Missing Features

### Item/Location Descriptions

- **Issue**: No `item_descriptions` or `location_descriptions` in WebWorld
- **Doc Reference**: [world api.md#webworld-class]
- **Benefit**: Human-friendly descriptions on webhost
- **Suggestion**: Add descriptions dicts with helpful info

### Options Presets

- **Issue**: No `options_presets` defined in WebWorld
- **Doc Reference**: [world api.md#webworld-class]
- **Benefit**: Pre-configured option sets for players
- **Suggestion**: Add presets like "Beginner", "Hardcore", "Chaos Mode"

### Settings Support

- **Issue**: No `settings` dataclass for world
- **Doc Reference**: [world api.md#world-settings] - "Settings are set by the user outside the generation process"
- **Doc Reference**: [settings api.md]
- **Potential Use**: ROM path, mod file paths, etc.

## Architectural Suggestions

### Duplicate Campaign Lists

- **Status**: ✅ COMPLETED - Extracted to single source of truth in `Types.py`
- **Issue**: Campaign names hardcoded in 4 different places:
  - `Items.py` - ITEM_DEFINITIONS (now uses `CAMPAIGNS`)
  - `__init__.py` win_condition (now uses `CAMPAIGNS`)
  - `__init__.py` create_regions (now uses `CAMPAIGNS` and `L4D1_CAMPAIGNS`)
  - `Rules.py` campaign_names list (now uses `CAMPAIGNS`)
- **Solution**: Created `CAMPAIGNS` and `L4D1_CAMPAIGNS` tuples in `Types.py`
- **Benefit**: Single point of maintenance - change one place, updates everywhere

### Location Naming Inconsistency

- **Issue**: Some locations use different character naming patterns
- **Observation**: L4D1 vs L4D2 character selection logic
- **Suggestion**: Ensure consistent naming pattern documented

## Style/Quality Improvements

### Remove Debug Comments

- **Issue**: Debug print statements left in code (line 60 in **init**.py)
- **Suggestion**: Remove or move to proper logging

### Companion App Location

- **Issue**: `ThirdPartyProgramStuff/` directory has unusual name
- **Consideration**: Could be renamed to `client/` for clarity
- **Note**: Contains companion Python script and build artifacts

## Documentation Improvements

### README.md Too Informal

- **Issue**: README is a development guide, not player-facing documentation
- **Tone**: Very casual/colloquial language
- **Suggestion**: Separate into:
  - `docs/en_Left 4 Dead 2.md` - Player-facing game info
  - `README.md` - Keep as dev guide but move to repo root or docs/

## Priority Rankings

### High Priority (Blocks PR to main repo)

1. Create game info doc (`en_Left 4 Dead 2.md`)
2. Create setup guide (`setup_en.md`)
3. Add unit tests
4. ✅ ~~Fix option_groups connection to WebWorld~~ (COMPLETED)
5. ✅ ~~Refactor massive match statement in __init__.py~~ (COMPLETED)

### Medium Priority (Code quality)

1. ✅ ~~Refactor Items.py to be data-driven~~ (COMPLETED)
2. ✅ ~~Add item_name_groups~~ (COMPLETED - done during Items.py refactor)
3. Add item/location descriptions
4. ✅ ~~Implement get_filler_item_name()~~ (COMPLETED)
5. ✅ ~~Fix type annotations (old-style imports)~~ (COMPLETED)

### Low Priority (Nice to have)

1. Add bug_report_page
2. Add options_presets
3. Add Settings support
4. Standardize string quotes
5. Add proper docstrings
6. ✅ ~~Extract campaign list to single source~~ (COMPLETED)

## Next Steps

Based on current progress, recommend:

1. **Immediate**: Create missing documentation files
2. **Short-term**: Add unit tests (start with basic generation test)
3. **Medium-term**: Refactor Items.py and **init**.py match statement
4. **Long-term**: Full test coverage + documentation descriptions
