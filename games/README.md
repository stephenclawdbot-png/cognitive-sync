# Games — Reverse Engineering Documentation

This folder contains detailed reverse-engineering documentation for 3 games, analyzed to the level of detail needed to rebuild them from scratch.

## Games

### 1. Legendum
**Engine:** Godot 4.6.2 | **Genre:** Life-simulation RPG roguelite

A life simulation RPG where each life is a "run" — your character ages from youth to death, earns Legacy Points for meta-progression, and reincarnates with Soul Perks. Features 6 attributes, 10+ skills, 6 combat styles, 14 abilities, 20+ enemy types, perk web, item effect system, 8 rarity tiers, shop system, job/task system, narrative story web, deed system, journal, contacts, heirlooms, calendar/seasons.

- 📄 [GAME_MECHANICS.md](./legendum/GAME_MECHANICS.md) — Full mechanics document (18 sections)
- 📄 [ECONOMY.md](./legendum/ECONOMY.md) — Economy document (14 sections)
- 📁 [raw-data/](./legendum/raw-data/) — Extracted PCK string data

### 2. Reverse Engine Roblox
**Type:** Roblox game analysis collection | **Games Analyzed:** 9

A collection of detailed analysis of 9 Roblox games, including full game mechanic breakdowns, economy patterns, design theory (Universal Game Thesis, Viral Formula), 60+ game idea documents, mobile game concepts, and tool infrastructure for automated game analysis.

- 📄 [GAME_MECHANICS.md](./reverse-engine-roblox/GAME_MECHANICS.md) — Analysis of all 9 games + design theory
- 📄 [ECONOMY.md](./reverse-engine-roblox/ECONOMY.md) — Economy patterns across all games
- 📁 [raw-data/](./reverse-engine-roblox/raw-data/) — Original analysis files, ideas, research

### 3. v1.0.00 (codename "wizdung")
**Engine:** Godot 4.6.1 | **Genre:** Action RPG / Dungeon Crawler

A top-down 8-directional action RPG dungeon crawler with 3 playable wizard classes (Dex/Int/Str), each with unique skill trees (36 nodes per class). Features 40+ stats, 4 damage types, 5 status effects, 5 item rarity tiers, 3 enemy types with elite variants, room-based dungeon generation, NPC services (identify/enchant/respec), loot system with glob pickups, and stash storage.

- 📄 [GAME_MECHANICS.md](./v1.0.00/GAME_MECHANICS.md) — Full mechanics document (16 sections)
- 📄 [ECONOMY.md](./v1.0.00/ECONOMY.md) — Economy document (11 sections)
- 📁 [raw-data/](./v1.0.00/raw-data/) — Extracted PCK string data

## Methodology

All 3 games were analyzed using:

1. **File extraction** — Zip files extracted to workspace
2. **Godot PCK string extraction** — Python regex extraction of readable ASCII strings from encrypted PCK files (flags=2, PACK_FILE_ENCRYPTED)
3. **Path analysis** — All `res://` paths catalogued to reconstruct file structure
4. **String analysis** — Game text, dialog, stat descriptions, item names, skill names extracted and categorized
5. **Resource analysis** — .tres resource paths reveal stat definitions, item definitions, skill definitions, enemy scalars, level room sets
6. **Scene analysis** — .tscn scene paths reveal level structure, UI panels, character scenes, VFX scenes
7. **Roblox analysis** — Markdown documents, screenshots, and game logs analyzed for game mechanics and economy patterns

## Disclaimer

These documents are reverse-engineering analysis for educational and game design reference purposes. The games are proprietary works of their respective creators. The documentation describes game mechanics and systems at a design level, sufficient to build similar games, but does not reproduce any original code, assets, or copyrighted material.