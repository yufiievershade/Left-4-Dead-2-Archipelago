---
updated: 2026-03-06
---

# Documentation Guide

A guide to navigating the Archipelago documentation in `@docs/`.

## Quick Reference by Topic

### 🎮 Adding a New Game

Start here if you want to add Archipelago support for a new game:

1. **[adding games.md](/docs/adding%20games.md)** - Complete overview of requirements for both client and world
2. **[world api.md](/docs/world%20api.md)** - World class API reference (World, WebWorld, Regions, Items, Locations)
3. **[apworld_dev_faq.md](/docs/apworld_dev_faq.md)** - Solutions to common world development problems
4. **[world maintainer.md](/docs/world%20maintainer.md)** - Responsibilities when maintaining a world in the main repo

### 🌐 Client Development

1. **[network protocol.md](/docs/network%20protocol.md)** - WebSocket protocol, packet formats, connection handshake
2. **[adding games.md](/docs/adding%20games.md)** - Client requirements section (hard requirements, item/location handling)

### ⚙️ Core Development

1. **[contributing.md](/docs/contributing.md)** - How to contribute to core Archipelago
2. **[style.md](/docs/style.md)** - Code style guide (PEP8, 120 char lines, docstrings)
3. **[tests.md](/docs/tests.md)** - Writing and running tests

### 🔧 Configuration & APIs

| Document                                                         | Purpose                                               |
|------------------------------------------------------------------|-------------------------------------------------------|
| **[options api.md](/docs/options%20api.md)**                     | Creating player options (Toggle, Choice, Range, etc.) |
| **[settings api.md](/docs/settings%20api.md)**                   | Settings system for world configuration               |
| **[webhost api.md](/docs/webhost%20api.md)**                     | WebHost integration for worlds                        |
| **[apworld specification.md](/docs/apworld%20specification.md)** | Packaging worlds as `.apworld` files                  |

### 🏗️ Advanced Topics

| Document                                                           | Purpose                              |
|--------------------------------------------------------------------|--------------------------------------|
| **[entrance randomization.md](/docs/entrance%20randomization.md)** | Entrance shuffle implementation      |
| **[shared_cache.md](/docs/shared_cache.md)**                       | Shared data caching system           |
| **[network diagram/](/docs/network%20diagram/)**                   | Visual network architecture diagrams |

### 🚀 Deployment & Setup

| Document                                                                             | Purpose                         |
|--------------------------------------------------------------------------------------|---------------------------------|
| **[running from source.md](/docs/running%20from%20source.md)**                       | Install from source (dev setup) |
| **[deploy using containers.md](/docs/deploy%20using%20containers.md)**               | Docker/container deployment     |
| **[webhost configuration sample.yaml](/docs/webhost%20configuration%20sample.yaml)** | WebHost config template         |

### 📋 Project Governance

| Document                                                                 | Purpose                               |
|--------------------------------------------------------------------------|---------------------------------------|
| **[CODEOWNERS](/docs/CODEOWNERS)**                                       | Code ownership and review assignments |
| **[code_of_conduct.md](/docs/code_of_conduct.md)**                       | Community standards                   |
| **[triage role expectations.md](/docs/triage%20role%20expectations.md)** | Triage team responsibilities          |

## By Use Case

### "I want to add a new game to Archipelago"

**Reading order:**

1. [contributing.md](/docs/contributing.md) - Understand contribution requirements
2. [adding games.md](/docs/adding%20games.md) - Learn the two-part structure (client + world)
3. [world api.md](/docs/world%20api.md) - Reference for world implementation
4. [apworld_dev_faq.md](/docs/apworld_dev_faq.md) - When you hit common problems
5. [options api.md](/docs/options%20api.md) - If adding player-configurable options
6. [world maintainer.md](/docs/world%20maintainer.md) - Before submitting PR

### "I need to implement a game client"

**Key docs:**

1. [network protocol.md](/docs/network%20protocol.md) - Complete protocol specification
2. [adding games.md](/docs/adding%20games.md) - Client requirements section
3. Check existing similar games in `worlds/` for reference implementations

### "I'm fixing a bug in core Archipelago"

1. [contributing.md](/docs/contributing.md) - Contribution guidelines
2. [style.md](/docs/style.md) - Code style requirements
3. [tests.md](/docs/tests.md) - Adding/updating tests
4. Relevant API docs (options api, world api, etc.)

### "I'm setting up a local Archipelago server"

1. [running from source.md](/docs/running%20from%20source.md) - Source installation
2. [deploy using containers.md](/docs/deploy%20using%20containers.md) - Docker alternative
3. [webhost configuration sample.yaml](/docs/webhost%20configuration%20sample.yaml) - Configuration options

## Key Concepts Cross-Reference

| Concept             | Primary Doc                                                    | Secondary Docs                             |
|---------------------|----------------------------------------------------------------|--------------------------------------------|
| World class         | [world api.md](/docs/world%20api.md)                           | [adding games.md](/docs/adding%20games.md) |
| Options/Toggles     | [options api.md](/docs/options%20api.md)                       | [world api.md](/docs/world%20api.md)       |
| Network protocol    | [network protocol.md](/docs/network%20protocol.md)             | [adding games.md](/docs/adding%20games.md) |
| Indirect conditions | [apworld_dev_faq.md](/docs/apworld_dev_faq.md)                 | [world api.md](/docs/world%20api.md)       |
| Entrance shuffle    | [entrance randomization.md](/docs/entrance%20randomization.md) | [world api.md](/docs/world%20api.md)       |
| apworld packaging   | [apworld specification.md](/docs/apworld%20specification.md)   | -                                          |
| Testing             | [tests.md](/docs/tests.md)                                     | [contributing.md](/docs/contributing.md)   |

## Important Notes

- All worlds are Python packages in `worlds/` directory
- Clients can be in any language with WebSocket support
- Style guide: 120 char lines, PEP8-ish, double-quoted strings
- Tests are required for critical changes
- Python 3.11+ required for development
