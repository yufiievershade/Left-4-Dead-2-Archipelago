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

- **Current State**: 181 lines of repetitive dictionary definitions
- **Issues**:
  - Hardcoded IDs with manual arithmetic (`base_id + 1`, `base_id + 2`, etc.)
  - Manual list appends for quantities (`["Dead Center"] * 1`, `["First Aid Kit"] * 5`)
  - No data-driven structure
- **Suggestion**: Similar to Locations refactor, use:
  - Data structures with item data (name, base quantity, classification)
  - Generator functions to build dictionaries and item pools
  - Estimated reduction: ~70% fewer lines

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

- **Issue**: Uses `MultiWorld.get_entrance()` and `MultiWorld.get_location()` instead of `world.multiworld`
- **Problem**: Accessing through class name rather than instance
- **Suggestion**: Use `multiworld.get_entrance()` through proper instance access

## Incomplete Features

### Option Groups Not Connected

- **Issue**: `l4d2_option_groups` defined in `Options.py` but never assigned to WebWorld
- **Doc Reference**: [world api.md#webworld-class] - option_groups for better organization on webhost
- **Current**: Groups exist in Options.py but not referenced in **init**.py
- **Fix**: Add `option_groups = l4d2_option_groups` to L4D2Web class

### Item Name Groups Empty

- **Issue**: `item_groups = {}` defined but never populated
- **Doc Reference**: [world api.md#world-class-skeleton] - "Items can be grouped using their names"
- **Suggestion**: Group items logically:
  - Weapons, Medical Items, Campaigns, Traps, etc.
- **Benefit**: Enables `!hint` group syntax and better organization

### Bug Report Page Missing

- **Issue**: No `bug_report_page` in WebWorld
- **Doc Reference**: [world api.md#webworld-class]
- **Suggestion**: Add link to GitHub issues or Discord

### Missing get_filler_item_name

- **Issue**: No implementation of `get_filler_item_name()` method
- **Doc Reference**: [adding games.md#encouraged-features]
- **Current**: Will pick any random item from item_name_to_id
- **Suggestion**: Implement to limit to true filler items only

## Style Guide Violations

### String Quotes

- **Issue**: Some strings use single quotes instead of double
- **Doc Reference**: [style.md#python-code] - "Strings in core code will be 'strings'... Strings in worlds should use double quotes as well"
- **Location**: `Items.py`, `__init__.py`, various files

### Type Annotations

- **Issue**: Old-style imports (`typing.Dict`, `typing.List`, `typing.Any`)
- **Doc Reference**: [style.md#python-code] - "Prefer new style type annotations"
- **Locations**:
  - `Options.py`: `from typing import List, Dict, Any`
  - `__init__.py`: `from typing import Dict, Any, List`
- **Suggestion**: Use `dict[str, ...]`, `list[...]` instead

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

- **Issue**: Campaign names hardcoded in multiple places:
  - `Items.py` progression_items dict
  - `__init__.py` win_condition property
  - `__init__.py` create_regions method
  - `Rules.py` campaign_names list
- **Suggestion**: Define once in `Types.py` or `Locations.py` as source of truth
- **Benefit**: Single point of maintenance, prevents drift

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
4. Fix option_groups connection to WebWorld
5. ✅ ~~Refactor massive match statement in **init**.py~~ (COMPLETED)

### Medium Priority (Code quality)

1. Refactor Items.py to be data-driven
2. Add item_name_groups
3. Add item/location descriptions
4. Implement get_filler_item_name()
5. Fix type annotations (old-style imports)

### Low Priority (Nice to have)

1. Add bug_report_page
2. Add options_presets
3. Add Settings support
4. Standardize string quotes
5. Add proper docstrings
6. Extract campaign list to single source

## Next Steps

Based on current progress, recommend:

1. **Immediate**: Create missing documentation files
2. **Short-term**: Add unit tests (start with basic generation test)
3. **Medium-term**: Refactor Items.py and **init**.py match statement
4. **Long-term**: Full test coverage + documentation descriptions
