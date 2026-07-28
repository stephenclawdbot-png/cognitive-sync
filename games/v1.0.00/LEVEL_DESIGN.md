# v1.0.00 "wizdung" — Level Design Document

> **Purpose:** Room templates, dungeon generation rules, difficulty pacing, and spatial design guidelines.
> **Audience:** Level designer, gameplay programmer building the dungeon system.
> **Companion docs:** ARCHITECTURE.md, DATA_MODELS.md, BALANCE.md

---

## 1. DUNGEON STRUCTURE

### 1.1 Dungeon Flow

```
Hub (safe zone)
  │
  ▼
Portal → Dungeon Entrance
  │
  ▼
Room 1 (dungeon_level = player_level)
  ├── Fight enemies
  ├── Pick up loot
  ├── Find key (if locked door)
  └── Choose door → Room 2
      │
      ▼
Room 2 (dungeon_level + 1)
  ├── Harder enemies
  ├── Better loot
  └── Choose door → Room 3
      │
      ▼
Room 3 (dungeon_level + 2)
  ├── ...
  └── Boss Room (every N rooms)
      │
      ▼
Boss Room
  ├── Boss fight
  ├── Big loot
  └── Portal appears → Return to Hub
```

### 1.2 Room Composition

Each room contains:
- **Floor:** Walkable tilemap (collision-free)
- **Walls:** Collision tilemap (impassable)
- **Decorations:** Non-collision visual tiles
- **Enemy spawn points:** Pre-placed positions (3-8 per room)
- **Loot spawn points:** Chests or ground drops
- **Doors:** 1-3 exits to other rooms (some locked)
- **Key items:** Dropped by specific enemies (if locked doors exist)
- **Exit portal:** Appears when room is cleared

---

## 2. ROOM TEMPLATE SPECIFICATIONS

### 2.1 Room Sizes

| Room Type | Size (tiles) | Size (px at 32px tiles) | Purpose |
|-----------|-------------|------------------------|---------|
| Small | 15×11 | 480×352 | Tutorial, quick encounters |
| Medium | 20×15 | 640×480 | Standard dungeon rooms |
| Large | 25×18 | 800×576 | Boss rooms, elite rooms |
| Arena | 30×20 | 960×640 | Multi-boss endgame |

### 2.2 Room Layout Patterns

```
PATTERN A — Open Arena (combat focus)
┌──────────────────────────┐
│  E                        │
│      [open space]          │
│  P        E        E       │
│      [open space]          │
│              E             │
└────D──────────────────────┘
P = player spawn, E = enemy spawn, D = door

PATTERN B — Corridor (chokepoint combat)
┌─────┐    ┌─────┐    ┌─────┐
│  E  │    │  E  │    │  E  │
│  E  │ D  │  E  │ D  │  E  │
│     │    │     │    │     │
│  P  │    │  E  │    │  E  │
└─────┘    └─────┘    └─────┘
Three connected chambers

PATTERN C — Crossroads (choice room)
┌─────┐    ┌─────┐
│  E  │ D  │     │
│     │    │  E  │
│  P  │    │     │
│     │ D  │     │
│  E  │    │  E  │
└─────┘    └─────┘
      │ D
      │
┌─────┐    ┌─────┐
│     │ D  │  E  │
│  E  │    │     │
│     │    │ Key │
└─────┘    └─────┘
Player chooses path — one has key, other has enemies

PATTERN D — Boss Arena
┌───────────────────────────┐
│                           │
│         BOSS              │
│                           │
│       P                    │
│                           │
│  [exit portal appears]    │
│  [after boss defeated]    │
└───────────────────────────┘
```

### 2.3 Room Template Detail — t1_room_01

```
Size: 20×15 tiles (640×480px at 32px tiles)

Tile Legend:
  # = Wall (collision)
  . = Floor (walkable)
  D = Door
  P = Player spawn
  E = Enemy spawn point
  L = Loot spawn point
  C = Chest

Map:
####################
#..................#
#..E....E....E.....#
#..................#
#..E....P....E.....#
#..................#
#.........D........#
#..................#
#..E....L....E.....#
#..................#
#..E....C....E.....#
#..................#
#......D....D......#
#..................#
####################

Spawn points: 8 enemies
Loot: 1 chest + 1 ground drop
Doors: 3 (left, right, bottom)
Key: No (all doors unlocked)
Tileset: stone_dungeon
```

### 2.4 Room Template Detail — t1_room_02 (Key Room)

```
Size: 20×15 tiles

Map:
####################
#..................#
#..E...........E...#
#..................#
#........D.........#
#..................#
#..E....K....E....#
#..................#
#........D.........#
#..................#
#..E...........E...#
#..................#
#..C....D....C....#
#..................#
####################

K = Key enemy (drops key when killed)
Doors: 4 (top, 2 middle, bottom)
Key: YES — top door locked until key enemy is killed
Chests: 2
Enemies: 6 (one carries the key)
```

---

## 3. DUNGEON GENERATION RULES

### 3.1 Generation Algorithm

```
1. Determine dungeon tier based on player level
   - Level 1-3 → tutorial
   - Level 4-7 → tier1
   - Level 8-12 → tier2
   - Level 13+ → endgame

2. Set dungeon_level = player_level (or highest unlocked, whichever is lower)

3. Generate room sequence:
   rooms_to_generate = 5 + floor(dungeon_level / 5)  # 5 rooms at level 1, up to 13 at level 40
   
   for each room (i = 0 to rooms_to_generate):
     a. Pick room template from tier's room_set (random)
     b. Set room_level = dungeon_level + i (escalating)
     c. Determine enemy count: pack_size = floor(3 + room_level * 0.5)
     d. Roll elite chance: if random() < elite_chance → spawn elite
     e. If i % boss_every_n == 0 and i > 0 → boss room
     f. Place enemies at spawn points (random selection)
     g. Roll loot: place chests and ground drops
     h. Determine doors: pick 1-3 doors, some may be locked
     i. If locked door exists → designate one enemy as key carrier
   
4. Last room is always boss room (or portal room for tutorial)
5. Boss room cleared → portal appears → return to hub
```

### 3.2 Enemy Placement Rules

```
For each room:
  1. Count available spawn points in room template
  2. Determine pack_size for this room level
  3. If pack_size > spawn_points → fill all, add overflow in center
  4. Enemy type selection:
     - Random from tier's enemy_types list
     - Weight: normal enemies 70%, ranged 20%, special 10%
  5. Elite roll:
     - if random() < elite_chance → upgrade one enemy to elite
     - Elite uses elite variant (higher stats, color tint)
  6. Boss room:
     - Always 1 boss + floor(pack_size / 3) minions
     - Boss at center, minions at perimeter spawn points
```

### 3.3 Loot Placement Rules

```
For each room:
  1. Place chests at designated chest positions (1-2 per room)
  2. Chest loot: always drops gear (never globs)
     - Rarity roll uses room_level for adjustment
  3. Enemy drops: rolled per-enemy on death (not pre-placed)
  4. Boss drops: guaranteed 1 epic+ item + 2-3 random items
```

---

## 4. TILESET SPECIFICATIONS

### 4.1 Required Tilesets

| Tileset | Use Case | Tile Size | Tiles Needed |
|---------|----------|-----------|-------------|
| tutorial_dungeon | Tutorial levels | 32×32 | floor, wall, wall_top, corner, door, door_frame |
| stone_dungeon | Tier 1 | 32×32 | floor, cracked_floor, wall, wall_top, pillar, door, door_locked, stairs |
| cave_dungeon | Tier 2 | 32×32 | cave_floor, rock_wall, stalactite, moss_floor, crystal, door, door_locked |
| overgrown_dungeon | Endgame | 32×32 | mossy_floor, vine_wall, root_floor, ancient_pillar, door, door_locked |
| hub | Hub area | 32×32 | wood_floor, stone_floor, carpet, wall, doorway, portal_pad |

### 4.2 Tile Properties

Each tile in the tileset must have:
- **Collision:** Wall tiles have collision, floor tiles do not
- **Navigation:** Floor tiles are walkable for enemy pathfinding
- **Visual layer:** Floor tiles on layer 0, walls on layer 1, decorations on layer 2

### 4.3 Autotiling Rules

```
Wall tiles should autotile based on neighbors:
  - If surrounded by walls on all 4 sides → interior wall
  - If exposed on top → wall top (visible face)
  - If exposed on left/right → wall side
  - Corner tiles → diagonal texture
  
Floor tiles:
  - If surrounded by floor → standard floor
  - If adjacent to wall → transition tile (slightly darker near wall)
  - If at room edge → edge tile
```

---

## 5. HUB AREA DESIGN

### 5.1 Hub Layout

```
Size: 30×22 tiles (960×704px at 32px tiles)

┌───────────────────────────────────┐
│                                   │
│  [Stash]              [Portal]    │
│                                   │
│         [Mysterious Wizard]       │
│                                   │
│  [Instruction Man]    [Trinket    │
│                        Witch]    │
│                                   │
│  [NPC_Dex]  [NPC_Int]  [NPC_Str]  │
│                                   │
│         [Player Spawn]             │
│                                   │
└───────────────────────────────────┘

Layout principles:
- Player spawns in center
- NPCs arranged in semicircle around spawn
- Stash on left, Portal on right (clear flow: store → shop → enter dungeon)
- No enemies, no hazards
- Warm lighting, safe atmosphere
- Music: ambient town theme
```

### 5.2 Hub Interactables

| Object | Position | Action |
|--------|----------|--------|
| Stash | Left side | Open stash inventory (shared between classes) |
| Portal | Right side | Enter dungeon (opens dungeon select) |
| Mysterious Wizard | Top center | Identify items, respec |
| Trinket Witch | Center right | Enchant, sell, buy |
| NPC Dex Wizard | Bottom left | Switch to Dex class |
| NPC Int Wizard | Bottom center | Switch to Int class |
| NPC Str Wizard | Bottom right | Switch to Str class |
| Instruction Man | Center left | Tutorial dialog |

---

## 6. DIFFICULTY PACING

### 6.1 Per-Room Difficulty Curve

```
Room 1: 3 enemies, level = dungeon_level (warmup)
Room 2: 4 enemies, level = dungeon_level + 1
Room 3: 5 enemies, level = dungeon_level + 2
Room 4: 5 enemies + 1 elite, level = dungeon_level + 3
Room 5: BOSS + 3 minions, level = dungeon_level + 4
Room 6: 5 enemies, level = dungeon_level + 5 (slight breather)
Room 7: 6 enemies, level = dungeon_level + 6
...
```

### 6.2 Tension Graph

```
Tension
  ↑
  │     ╱╲      ╱╲      ╱╲
  │    ╱  ╲    ╱  ╲    ╱  ╲
  │   ╱    ╲  ╱    ╲  ╱    ╲
  │  ╱      ╲╱      ╲╱      ╲___
  │ ╱
  │╱_______________________________→ Rooms
     R1  R2  R3  R4  R5(BOSS)  R6  R7  R8  R9  R10(BOSS)

Each boss room is a tension peak. After boss, brief drop then ramp up again.
Player should feel: "I barely survived that boss, but I got amazing loot."
```

### 6.3 Loot Quality Pacing

| Room Position | Loot Quality | Notes |
|--------------|-------------|-------|
| Room 1-2 | Common/Magic | Warmup, basic drops |
| Room 3-4 | Magic/Rare | Building excitement |
| Boss room | Rare/Epic guaranteed | Big reward for boss kill |
| Post-boss rooms | Epic/Legendary chance | Escalating rewards |
| Final boss | Epic guaranteed + Legendary chance | Climax of run |

---

## 7. ENVIRONMENTAL DESIGN GUIDELINES

### 7.1 Visual Clarity Rules

1. **Floor must contrast with walls** — Player should never be confused about where they can walk
2. **Enemy sprites must contrast with floor** — No camouflaged enemies
3. **Loot must be visible** — Gold sparkles, floating animation, clear silhouette
4. **Doors must be obvious** — Different color from walls, arrow indicator
5. **Locked doors must be readable** — Chain/lock visual, red indicator

### 7.2 Camera Rules

- Camera follows player with smoothing (speed 8.0)
- Camera clamped to room bounds (player can't see outside room)
- Slight zoom out in boss rooms (1.0 → 0.85x) to show boss and arena
- Screen shake on: crit hit, boss slam, explosion, player hit
- Screen shake magnitude: 2px (small), 5px (medium), 10px (large)

### 7.3 Spatial Flow Rules

- **No dead ends** — Every room should have clear flow (enter → fight → exit)
- **No maze rooms** — Rooms are combat arenas, not navigation puzzles
- **Sightlines** — Player should see all enemies when entering a room
- **Escape routes** — Player should always be able to dodge around enemies (room is wide enough)

---

## 8. ROOM BUILD CHECKLIST

For each room template, verify:

- [ ] Room has clear entrance and exit points
- [ ] Enemy spawn points are spread out (not clustered)
- [ ] No spawn point is within 100px of player spawn
- [ ] Chests are accessible after clearing room
- [ ] Doors are visually distinct from walls
- [ ] Locked doors have clear "locked" visual
- [ ] Room has at least 2 walkable paths to each door
- [ ] No tight corridors where player gets stuck
- [ ] Room is symmetrical or balanced (no advantage to one side)
- [ ] Lighting/VFX highlights interactables (chests glow, doors have indicator)
- [ ] Room can be cleared in 10-40 seconds (not too long)
- [ ] Boss room has enough space for dodging (at least 8 tiles of open space around boss)