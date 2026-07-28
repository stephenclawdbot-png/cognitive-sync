# Legendum — Complete Asset Specification

> **Visual style:** 16-bit SNES-era pixel art (Stardew Valley × Chrono Trigger)
> **Engine:** Godot 4.6.2 · **Pixel density:** 16px base tile, sprites at native pixel scale, SubViewport upscale to display
> **Audience:** Artists, animators, audio engineers, VFX designers, build engineer.
> **Total estimated asset count:** ~620 files (sprites + audio + UI + VFX + fonts).
> All paths below are `res://`-relative under `assets/`.

---

## 1. Style Guide

### 1.1 Visual Palette

| Use              | Palette                                                           | Hex examples                                            |
|------------------|-------------------------------------------------------------------|---------------------------------------------------------|
| Town warm tones  | Earthy browns, cream, moss green, soft gold                      | `#5C3A21 #A37C45 #C9B27C #6B7F3E #E8D9B0`               |
| Combat cool tones| Slate, deep blue, blood red, ember orange                         | `#2E3438 #4A6FA5 #B0383A #D67A2C`                       |
| UI parchment     | Aged paper, ink brown, gold accent, subtle teal for highlights    | `#F3E6C8 #4A3825 #DAA520 #6FA0A0`                       |
| Character skin   | Warm tan base, two shadow steps, one highlight                    | `#E8B57E #C99264 #A06A40 #F3D2A0`                       |
| Effects          | Pure white core, color-tinted auras, additive blend for sparks    | `#FFFFFF #FFD56B #FF6B6B #6BB6FF`                       |

**Palette discipline:** every sprite must restrict itself to the global palette plus up to 4 unique per-asset hues. No true black except outlines; use `#1B1410` for the deepest shadow.

### 1.2 Pixel Density & Outline

- **Base unit:** 16×16 px tiles in world; 32×32 to 48×48 px for character sprites; 64×64 to 96×96 px for portraits.
- **Player sprite canvas:** 48×48 px (the visible character occupies ~32×32, leaving room for animations and weapons to extend).
- **Enemy sprite canvas:** 32×32 to 96×96 depending on class (slimes 32, golems 96).
- **Outline style:** single-color black outline (`#1B1410`) for characters, enemies, items; selective outline for environment tiles (edges only, no internal lines); lineless for VFX/particles.
- **Shading:** basic-to-medium shading (2 shadow steps + 1 highlight). Flat shading is reserved for UI parchment.
- **Anti-aliasing:** none. Hard pixel edges everywhere. Sprites snap to integer pixels.
- **Animation frame count:** see §5 per-asset table.

### 1.3 Rendering Setup

- All gameplay renders to a `SubViewport` at native pixel resolution (base 320×180 or 480×270 depending on area).
- Upscaled ×5–6 to display via a `TextureRect` with `texture_filter = NEAREST`.
- Optional CRT shader (scanlines + slight bloom) toggled in Settings.
- Camera snaps to integer pixels (`Camera2D.position_smoothing_enabled = false`, manual integer snapping).

---

## 2. Naming Conventions

### 2.1 General Rules

- `snake_case` everywhere. No spaces, no camelCase in file names.
- Prefix sprites with category: `char_`, `mob_`, `item_`, `tile_`, `ui_`, `vfx_`, `port_`, `bg_`.
- Animation frames are numbered zero-padded: `char_player_walk_s_00.png`, `char_player_walk_s_01.png`, …
- Direction suffix for directional sprites: `_n` (north), `_s` (south), `_e` (east), `_w` (west). Diagonal variants use `_nw`, `_ne`, `_sw`, `_se` if used (default game is 4-directional).
- Aseprite source files use `.aseprite`; exported PNGs live next to them with the same base name.
- Audio files: `bgm_<area>`, `sfx_<action>`, `amb_<area>`.
- All icons are 16×16 or 32×32 PNG; UI panels are 9-sliced `.png` + a `.tres` `StyleBoxTexture`.

### 2.2 Aseprite → PNG Export

Each animated sprite ships as:
1. A single `.aseprite` source file.
2. An horizontal-strip PNG spritesheet (`<name>.png`) with frame tags matching animation names.
3. A `<name>.import` file (Godot auto-generates) with `filter = false`.
4. (Optional) A `<name>.tres` `SpriteFrames` resource for AnimatedSprite2D use.

The build script (`tools/export_aseprite.gd`) walks `assets/` and re-exports any `.aseprite` whose mtime is newer than its `.png`.

---

## 3. Folder Structure

```
assets/
├── sprites/
│   ├── characters/
│   │   ├── player/
│   │   │   ├── young/
│   │   │   ├── veteran/
│   │   │   ├── elder/
│   │   │   └── decrepit/
│   │   ├── enemies/
│   │   │   ├── slimes/
│   │   │   ├── wolves/
│   │   │   ├── skeletons/
│   │   │   ├── goblins/
│   │   │   ├── undead/
│   │   │   ├── beasts/
│   │   │   └── bosses/
│   │   └── npcs/
│   ├── portraits/
│   │   ├── narrators/
│   │   └── npcs/
│   ├── tiles/
│   │   ├── town/
│   │   ├── woodlands/
│   │   ├── dead_woodlands/
│   │   ├── depths/
│   │   └── valenthar/
│   ├── items/
│   │   ├── weapons/
│   │   ├── armor/
│   │   ├── helmets/
│   │   ├── shields/
│   │   ├── accessories/
│   │   ├── consumables/
│   │   └── tools/
│   ├── icons/
│   │   ├── abilities/
│   │   ├── perks/
│   │   ├── soul_perks/
│   │   ├── stats/
│   │   ├── skills/
│   │   ├── ui/
│   │   └── seasons/
│   ├── ui/
│   │   ├── panels/
│   │   ├── buttons/
│   │   ├── frames/
│   │   ├── cursors/
│   │   └── tabs/
│   ├── vfx/
│   │   ├── hits/
│   │   ├── auras/
│   │   ├── projectiles/
│   │   └── ambient/
│   └── scenes/
│       ├── backgrounds/
│       └── title/
├── audio/
│   ├── bgm/
│   ├── sfx/
│   ├── amb/
│   └── stingers/
├── fonts/
│   ├── pixel/
│   └── ui/
└── shaders/
    ├── crt.gdshader
    ├── outline.gdshader
    └── tint.gdshader
```

---

## 4. Animation Requirements

### 4.1 Universal Animation Set

Every **walkable** character (player + NPCs) needs:

| Animation | Frames | Direction variants | Notes                              |
|-----------|--------|--------------------|------------------------------------|
| idle      | 4      | 4 (n/s/e/w)        | Subtle breathing, ~6 fps            |
| walk      | 6–8    | 4                  | ~10 fps                            |
| action    | 6      | 4                  | Interact / pickup                   |
| hurt      | 2      | 1 (face player)    | Flicker + recoil                    |
| death     | 6      | 1                  | Fall, then dissolve                 |

Every **combat-capable** character (player + combat NPCs + enemies) adds:

| Animation | Frames | Direction variants | Notes                              |
|-----------|--------|--------------------|------------------------------------|
| attack    | 6      | 4                  | Per weapon class (slash/draw/cast)  |
| cast      | 6      | 1                  | For magic users, raised arms        |
| block     | 2      | 1                  | Shield up                           |
| ability_* | 4–8    | 1                  | One per slotted ability             |

### 4.2 Player by Life Stage

The player sprite is **per life stage** — the same person visually ages. All four stages use the same skeleton pose so animations transfer.

| Stage     | Canvas | Idle | Walk | Attack | Hurt | Death |
|-----------|--------|------|------|--------|------|-------|
| Young     | 48×48  | 4    | 6    | 6      | 2    | 6     |
| Veteran   | 48×48  | 4    | 6    | 6      | 2    | 6     |
| Elder     | 48×48  | 4    | 6    | 6      | 2    | 6     |
| Decrepit  | 48×48  | 4    | 6    | 6      | 2    | 6     |

Total per stage: idle(4×4) + walk(6×4) + attack(6×4) + hurt(2) + death(6) = **68 frames** per stage × 4 stages = **272 player frames**. Add weapon overlays (separate sprite layer for weapon visuals): 6 frames × 4 directions × 3 weapon classes = 72 frames.

### 4.3 Enemy Animation Sets

| Class           | Canvas | Idle | Walk | Attack | Hurt | Death | Special |
|-----------------|--------|------|------|--------|------|-------|---------|
| Slime           | 32×32  | 4    | —    | 4      | 2    | 4     | —       |
| Bat             | 32×32  | 4    | 4 (fly) | 4   | 2    | 4     | —       |
| Wolf            | 48×48  | 4    | 6    | 6      | 2    | 6     | —       |
| Spider          | 32×32  | 4    | 6    | 6      | 2    | 6     | web (4) |
| Snake           | 32×32  | 4    | 6    | 4      | 2    | 4     | —       |
| Rat             | 16×16  | 4    | 4    | 4      | 2    | 4     | —       |
| Ooze            | 32×32  | 4    | 4    | 4      | 2    | 4     | —       |
| Leech           | 16×16  | 4    | 4    | 4      | 2    | 4     | —       |
| Goblin (spear)  | 32×32  | 4    | 6    | 6      | 2    | 6     | —       |
| Goblin (archer) | 32×32  | 4    | 6    | 6      | 2    | 6     | —       |
| Goblin (mage)   | 32×32  | 4    | 6    | 6      | 2    | 6     | cast(6) |
| Kobold          | 32×32  | 4    | 6    | 6      | 2    | 6     | —       |
| Skeleton knight | 48×48  | 4    | 6    | 6      | 2    | 6     | block(2)|
| Skeleton archer | 32×32  | 4    | 6    | 6      | 2    | 6     | —       |
| Skeleton mage   | 32×32  | 4    | 6    | 6      | 2    | 6     | cast(6) |
| Golem           | 96×96  | 4    | 6    | 8      | 2    | 8     | slam(8) |
| Ent             | 64×64  | 4    | 4    | 6      | 2    | 6     | —       |
| Entling         | 32×32  | 4    | 6    | 4      | 2    | 4     | —       |
| Spirit          | 32×32  | 4    | 4 (float) | 4 | 2    | 4     | —       |
| Dummy (training)| 32×32  | 1    | —    | —      | 2    | —     | —       |
| Sparrer         | 48×48  | 4    | 6    | 6      | 2    | —     | —       |
| Ancient Stone Guardian (boss) | 96×96 | 6 | 6 | 8 | 4 | 10 | slam(10), special(8) |

### 4.4 Animation FPS

- idle: 6 fps
- walk: 10 fps
- attack: 12 fps
- ability: 10 fps
- hurt: 12 fps (single-frame pop + 2-frame flicker)
- death: 8 fps

Looping animations (idle, walk, cast-loop) must end on a frame that loops seamlessly to frame 0. Use Aseprite's "loop" tag.

---

## 5. Full Asset List

### 5.1 Characters — Player (272 frames + 72 weapon frames = 344 PNGs)

| Asset ID                     | Description                          | Frames | Dirs | Format | Priority |
|------------------------------|--------------------------------------|--------|------|--------|----------|
| char_player_young_idle_*     | Young player idle, 4 dirs            | 4×4=16 | 4    | PNG    | P0       |
| char_player_young_walk_*      | Young player walk, 4 dirs            | 6×4=24 | 4    | PNG    | P0       |
| char_player_young_attack_*    | Young player attack, 4 dirs          | 6×4=24 | 4    | PNG    | P1       |
| char_player_young_hurt        | Young player hurt                    | 2      | 1    | PNG    | P1       |
| char_player_young_death       | Young player death                   | 6      | 1    | PNG    | P1       |
| char_player_veteran_*         | (same set as young)                  | 68     | —    | PNG    | P1       |
| char_player_elder_*           | (same set as young)                 | 68     | —    | PNG    | P2       |
| char_player_decrepit_*        | (same set as young)                  | 68     | —    | PNG    | P2       |
| char_player_weapon_melee_*    | Sword overlay, 6 frames × 4 dirs     | 24     | 4    | PNG    | P1       |
| char_player_weapon_ranged_*   | Bow overlay, 6 frames × 4 dirs       | 24     | 4    | PNG    | P1       |
| char_player_weapon_magic_*    | Staff overlay, 6 frames × 4 dirs     | 24     | 4    | PNG    | P2       |

### 5.2 Characters — NPCs (portraits + overworld sprites)

| Asset ID                  | Description                          | Frames | Format  | Priority |
|---------------------------|--------------------------------------|--------|---------|----------|
| npc_ashvale_merchant      | Overworld sprite, 4 dirs            | 24 (idle+walk) | PNG | P1 |
| port_npc_ashvale_merchant | Portrait bust, 96×96                 | 3 (neutral/talk/happy) | PNG | P1 |
| npc_father_alric          | Overworld sprite                     | 24     | PNG     | P1       |
| port_npc_father_alric     | Portrait bust                        | 3      | PNG     | P1       |
| npc_grey_wizard           | Overworld sprite                     | 24     | PNG     | P1       |
| port_npc_grey_wizard      | Portrait bust                        | 3      | PNG     | P1       |
| npc_helga                 | Overworld sprite                     | 24     | PNG     | P1       |
| port_npc_helga            | Portrait bust                        | 3      | PNG     | P1       |
| npc_lunorak                | Overworld sprite                     | 24     | PNG     | P2       |
| port_npc_lunorak          | Portrait bust                        | 3      | PNG     | P2       |
| npc_mizgrub               | Overworld sprite                     | 24     | PNG     | P1       |
| port_npc_mizgrub          | Portrait bust                        | 3      | PNG     | P1       |
| npc_prison_guard          | Overworld sprite                     | 24     | PNG     | P0       |
| port_npc_prison_guard     | Portrait bust                        | 3      | PNG     | P0       |
| npc_goods_peddler         | Overworld sprite                     | 24     | PNG     | P2       |
| port_npc_goods_peddler    | Portrait bust                        | 3      | PNG     | P2       |
| npc_ilaf                  | Overworld sprite                     | 24     | PNG     | P3       |
| port_npc_ilaf             | Portrait bust                        | 3      | PNG     | P3       |

**NPC total:** 8 NPCs × (24 overworld + 3 portrait) = **216 PNGs** at P1+; P0 NPCs (prison guard) ship first.

### 5.3 Characters — Enemies (per §4.3)

| Asset ID                       | Description                | Frames | Canvas | Priority |
|--------------------------------|----------------------------|--------|--------|----------|
| mob_slime_blue                 | Blue slime                | 14     | 32×32  | P0       |
| mob_slime_green                | Green slime               | 14     | 32×32  | P0       |
| mob_slime_red                  | Red slime                 | 14     | 32×32  | P1       |
| mob_slime_big                  | Big slime                 | 14     | 64×64  | P1       |
| mob_slime_green_big            | Big green slime           | 14     | 64×64  | P2       |
| mob_bat                        | Bat                       | 18     | 32×32  | P0       |
| mob_wolf2                      | Brown wolf                | 24     | 48×48  | P0       |
| mob_wolf_gray                  | Gray wolf                 | 24     | 48×48  | P1       |
| mob_wolf3                      | Danger wolf              | 24     | 48×48  | P1       |
| mob_spider                     | Spider                    | 22     | 32×32  | P2       |
| mob_snake                      | Snake                     | 20     | 32×32  | P2       |
| mob_rat                        | Rat                       | 18     | 16×16  | P2       |
| mob_ooze                       | Ooze                      | 18     | 32×32  | P2       |
| mob_leech                      | Leech                     | 18     | 16×16  | P3       |
| mob_beholder                   | Beholder                  | 22     | 48×48  | P3       |
| mob_mimic                      | Mimic (chest disguise)    | 16     | 32×32  | P3       |
| mob_goblin_spear               | Goblin spearman           | 24     | 32×32  | P1       |
| mob_goblin_archer              | Goblin archer             | 24     | 32×32  | P1       |
| mob_goblin_mage                | Goblin mage               | 30     | 32×32  | P2       |
| mob_kobold                     | Kobold                    | 24     | 32×32  | P2       |
| mob_skeleton_knight            | Skeleton knight           | 26     | 48×48  | P2       |
| mob_skeleton_archer            | Skeleton archer           | 24     | 32×32  | P2       |
| mob_skeleton_mage              | Skeleton mage             | 30     | 32×32  | P2       |
| mob_golem                      | Stone golem               | 32     | 96×96  | P3       |
| mob_fauna_ent                  | Ent                       | 22     | 64×64  | P3       |
| mob_fauna_entling              | Entling                   | 20     | 32×32  | P3       |
| mob_spirit                     | Spirit                    | 18     | 32×32  | P3       |
| mob_dummy                      | Training dummy            | 3      | 32×32  | P0       |
| mob_sparrer                    | Sparring partner          | 24     | 48×48  | P1       |
| mob_ancient_stone_guardian     | Boss — Ancient Stone Guardian | 52 | 96×96  | P3       |

**Enemy total:** ~30 enemies × ~22 frames avg ≈ **660 PNGs**.

### 5.4 Environment — Tilesets

Each tileset is a set of tile PNGs at 16×16 (some 16×24 for tall walls), with associated terrain rules (better-terrain addon format). One tileset per region:

| Asset ID                  | Description                          | Tile count | Tile size | Priority |
|---------------------------|--------------------------------------|------------|-----------|----------|
| tile_town_ground          | Town grass, path, dirt, cobble       | 24         | 16×16     | P0       |
| tile_town_walls           | Town building walls, doors, windows  | 36         | 16×16     | P0       |
| tile_town_props           | Town props (barrels, crates, flowers)| 32         | 16×16     | P1       |
| tile_town_interior        | Interior floors, walls, furniture    | 48         | 16×16     | P1       |
| tile_woodlands_ground     | Woodlands grass, dirt, leaves       | 24         | 16×16     | P0       |
| tile_woodlands_trees      | Tree trunks, foliage, dead trees    | 28         | 16×32     | P0       |
| tile_woodlands_props      | Bushes, rocks, logs, mushrooms       | 32         | 16×16     | P1       |
| tile_dead_woodlands_*     | Dead woodlands set (darker)         | 60         | mixed     | P2       |
| tile_depths_ground        | Cave floor, walls, ore veins        | 32         | 16×16     | P2       |
| tile_depths_props         | Stalactites, crystals, bones         | 28         | 16×16     | P2       |
| tile_valenthar_*          | Valenthar elven region (demo-locked) | 80         | mixed     | P3       |
| tile_dungeon_catacombs    | Catacomb walls, floors, sarcophagi   | 40         | 16×16     | P2       |
| tile_dungeon_mines        | Mine tracks, supports, lanterns      | 36         | 16×16     | P2       |
| tile_dungeon_temple       | Lost temple ornate tiles            | 44         | 16×16     | P2       |

**Tileset total:** ~540 tiles across all sets = **~540 PNGs** (many tiles reused via rotations/flips).

### 5.5 Items — Icons

Item icons are 32×32 PNGs, one per item plus a rarity border overlay (8 borders, tinted at runtime).

| Category   | Count | Description                                       | Format | Priority |
|------------|-------|---------------------------------------------------|--------|----------|
| Weapons    | 30    | Swords (10 tiers), bows (10), staves (5), greats (5) | 32×32 PNG | P0 (swords 1–4 first) |
| Armor      | 8     | Cloth, Leather, Iron body + variants              | 32×32 PNG | P1       |
| Helmets    | 6     | Leather, Iron, Miner's, plus 3 variants          | 32×32 PNG | P1       |
| Shields    | 8     | Hide, Heavy, Buckler ×2, Heater ×2, plus variants | 32×32 PNG | P1       |
| Accessories| 12    | Amulets (4), Rings (2), Capes (3), Fingerwraps     | 32×32 PNG | P2       |
| Consumables| 16    | Berries, Herbs, Holy Water, Ooze, Cloud Puff, etc | 32×32 PNG | P0 (healing first) |
| Books/Texts| 8     | Holy Texts, Book of Stronk ×3, Scriptures         | 32×32 PNG | P2       |
| Tools      | 8     | Pickaxes (4), Candle, Spectacles, Map, Rope       | 32×32 PNG | P1       |
| Misc/Keys  | 10    | Mysterious Relic, Crescent Key, Saint's Tooth     | 32×32 PNG | P3       |
| Clothing   | 8     | Fine/Respectable Clothing, Farmer's Hat, Work Boots/Gloves | 32×32 PNG | P2       |
| Quivers/Pouches | 4 | Hide Quiver, Knife Pouch, etc.                  | 32×32 PNG | P2       |

**Item icon total:** ~110 PNGs + 8 rarity borders = **118 PNGs**.

### 5.6 Ability & Perk Icons

| Asset ID prefix     | Count | Description                          | Format | Priority |
|----------------------|-------|--------------------------------------|--------|----------|
| icon_ability_*       | 14    | One per ability (Analyze, Assassinate, Beartrap, Bowl of Fire, Chain Lightning, Giant Orb, Guardian Spirit, Magic Dagger, Pickaxe Throw, Piercing Strike, Rejuvenation, Sweeping Slash, Throwing Knives, Wrath) | 32×32 PNG | P1 |
| icon_perk_*          | 32    | One per per-life perk (Blademaster, Forager, Shop Discount, Pickpocket, Dense, etc.) | 32×32 PNG | P1 |
| icon_soul_perk_*     | 12    | One per Soul Perk (Early Bird, Night Owl, Dreamer's Echo, etc.) | 32×32 PNG | P2 |
| icon_stat_*          | 6     | STR/DEX/VIG/PER/INT/WIS              | 16×16 PNG | P0 |
| icon_skill_*         | 11    | One per skill (Blades, Archery, Farming, etc.) | 16×16 PNG | P0 |
| icon_season_*        | 3     | Greenrise, Highsun, Amberfall        | 16×16 PNG | P1 |
| icon_resource_*      | 8     | Gold, LP, RP, SP, Goods (4 region variants), Energy, HP, XP | 16×16 PNG | P0 |

**Icon total:** ~86 PNGs.

### 5.7 UI Assets

| Asset ID                  | Description                                       | Format                | Priority |
|---------------------------|---------------------------------------------------|-----------------------|----------|
| ui_panel_parchment         | 9-slice parchment panel (corner + edge + center)  | PNG + StyleBoxTexture | P0 |
| ui_panel_dark             | Dark variant for combat HUD                       | PNG + StyleBoxTexture | P1 |
| ui_panel_inset             | Inset panel (gray border, for lists)             | PNG + StyleBoxTexture | P1 |
| ui_button_default          | Default button (rest/hover/pressed)               | 3× PNG + StyleBox     | P0 |
| ui_button_gold             | Gold-accented confirm button                      | 3× PNG + StyleBox     | P1 |
| ui_button_icon             | Square icon button                                | 3× PNG + StyleBox     | P1 |
| ui_button_tab_active       | Active tab                                        | PNG + StyleBox        | P0 |
| ui_button_tab_inactive     | Inactive tab                                      | PNG + StyleBox        | P0 |
| ui_button_close            | Close (×) button                                  | 3× PNG                | P0 |
| ui_scrollbar_v            | Vertical scrollbar (track + thumb + arrows)       | 4× PNG                | P0 |
| ui_scrollbar_h            | Horizontal scrollbar                              | 4× PNG                | P1 |
| ui_frame_hp_bar            | HP bar frame + fill (red gradient)                | 2× PNG                | P0 |
| ui_frame_energy_bar        | Energy bar frame + fill (yellow)                  | 2× PNG                | P0 |
| ui_frame_xp_bar            | XP bar frame + fill (blue)                        | 2× PNG                | P1 |
| ui_frame_lp_bar_segment    | Legend Points timeline segment (8 variants)       | 8× PNG                | P2 |
| ui_frame_perk_node          | Perk web node (locked/unlocked/selected/blocked)  | 4× PNG                | P1 |
| ui_frame_perk_socket        | Web connector line (4 orientations)              | 4× PNG                 | P1 |
| ui_frame_ability_slot      | Ability slot (active/passive/empty)               | 3× PNG                 | P1 |
| ui_frame_item_slot          | Inventory item slot (with rarity border set)      | 9× PNG (rarity tiers) | P0 |
| ui_frame_equip_slot         | Equipment slot (weapon/armor/helmet/...)          | 7× PNG (per slot type)| P1 |
| ui_cursor_default           | Default cursor                                    | PNG                    | P0 |
| ui_cursor_pointer          | Pointer cursor (for interactive objects)          | PNG                    | P0 |
| ui_cursor_text              | Text cursor                                        | PNG                    | P2 |
| ui_dialog_box               | Dialog box parchment                              | PNG + StyleBox        | P0 |
| ui_dialog_nameplate         | Speaker nameplate                                  | PNG                    | P0 |
| ui_dialog_arrow             | "Continue" arrow (animated, 4 frames)              | 4× PNG                 | P0 |
| ui_choice_arrow             | Choice indicator                                   | PNG                    | P0 |
| ui_death_screen_bg          | Death screen background                             | 320×180 PNG            | P1 |
| ui_life_review_card         | Life review card frame                              | PNG + StyleBox        | P2 |
| ui_life_review_deed         | Deed card frame                                    | PNG + StyleBox        | P2 |
| ui_quiet_years_timeline_node| Timeline node marker (3 states)                     | 3× PNG                 | P2 |
| ui_title_logo               | Title screen logo                                   | PNG (large)            | P1 |
| ui_title_bg                 | Title background art                                | 480×270 PNG            | P1 |
| ui_title_btn_new            | "New Life" button                                   | 3× PNG                 | P1 |
| ui_title_btn_continue       | "Continue" button                                   | 3× PNG                 | P1 |
| ui_title_btn_settings        | "Settings" button                                   | 3× PNG                 | P1 |
| ui_origin_portrait_*        | Origin portraits (5 origins × 1 portrait each)      | 5× 96×96 PNG           | P0 |
| ui_backstory_fighter         | Backstory scene art (fighter)                      | 320×180 PNG            | P1 |
| ui_backstory_nomad           | Backstory scene art (nomad)                        | 320×180 PNG            | P2 |
| ui_region_map_ashvale        | Ashvale region map                                  | 480×270 PNG            | P1 |
| ui_region_map_woodlands      | Woodlands region map                                | 480×270 PNG            | P2 |
| ui_poi_symbol_*             | Point-of-interest symbols (town/mine/inn/church)   | 8× 16×16 PNG           | P1 |
| ui_tooltip_frame             | Tooltip frame (9-slice)                             | PNG + StyleBox         | P1 |
| ui_tooltip_separator        | Tooltip horizontal separator                        | PNG                    | P2 |
| ui_settings_slider          | Settings slider (track + thumb)                     | 2× PNG                 | P2 |
| ui_settings_checkbox        | Checkbox (unchecked/checked)                       | 2× PNG                 | P2 |
| ui_settings_dropdown         | Dropdown arrow                                      | PNG                    | P2 |

**UI total:** ~120 PNGs + ~14 StyleBoxTexture `.tres` resources.

### 5.8 VFX Sprites & Animations

VFX are short (4–12 frame) PNG strips, played once via `AnimatedSprite2D` and pooled.

| Asset ID                     | Description                          | Frames | Canvas | Priority |
|------------------------------|--------------------------------------|--------|--------|----------|
| vfx_hit_slash_basic           | Sword slash spark                    | 6      | 32×32  | P0       |
| vfx_hit_slash_sparks          | Wide slash sparks                    | 6      | 48×32  | P1       |
| vfx_hit_arrow_impact          | Arrow impact                         | 4      | 16×16  | P0       |
| vfx_hit_orb_impact            | Magic orb impact                     | 4      | 24×24  | P0       |
| vfx_hit_blood                 | Blood splatter (enemy hit)           | 4      | 24×24  | P0       |
| vfx_hit_block                 | Block spark (shield up)              | 4      | 32×32  | P1       |
| vfx_crit_burst                | Critical hit burst (gold star)        | 8      | 32×32  | P1       |
| vfx_death_poof                | Enemy death poof                     | 6      | 32×32  | P0       |
| vfx_death_dissolve            | Player death dissolve                | 12     | 48×48  | P1       |
| vfx_levelup_burst             | Level-up burst (radiating rings)     | 12     | 64×64  | P1       |
| vfx_perk_unlock               | Perk unlock flash                    | 10     | 48×48  | P2       |
| vfx_lp_grant                  | Legend Point grant (floating coin)   | 6      | 16×16  | P2       |
| vfx_item_drop                 | Item drop bounce                     | 4      | 16×16  | P1       |
| vfx_item_pickup               | Item pickup sparkle                  | 4      | 16×16  | P0       |
| vfx_gold_drop                 | Gold coin drop (rotating)            | 6      | 16×16  | P0       |
| vfx_gold_pickup               | Gold pickup sparkle                  | 4      | 16×16  | P0       |
| vfx_ability_analyze           | Analyze lock-on reticle              | 6      | 32×32  | P1       |
| vfx_ability_assassinate       | Assassinate dash trail               | 6      | 64×32  | P1       |
| vfx_ability_beartrap           | Beartrap throw + arm                  | 8      | 32×32  | P2       |
| vfx_ability_bowl_of_fire       | Fireball trail                        | 6      | 32×32  | P1       |
| vfx_ability_chain_lightning    | Chain lightning arcs                  | 8      | 64×64  | P2       |
| vfx_ability_giant_orb          | Giant staff orb                       | 8      | 32×32  | P2       |
| vfx_ability_guardian_spirit     | Guardian spirit aura                  | 12     | 64×64  | P2       |
| vfx_ability_magic_dagger       | Orbiting dagger                       | 6      | 16×16  | P2       |
| vfx_ability_pickaxe_throw      | Pickaxe projectile                    | 6      | 24×24  | P2       |
| vfx_ability_piercing_strike     | Piercing arrow line                   | 6      | 48×16  | P1       |
| vfx_ability_rejuvenation        | Heal glow                              | 8      | 48×48  | P2       |
| vfx_ability_sweeping_slash      | Wide slash cone                       | 6      | 48×32  | P1       |
| vfx_ability_throwing_knives     | Throwing knife projectile             | 4      | 16×16  | P2       |
| vfx_ability_wrath              | AoE shockwave                         | 8      | 64×64  | P2       |
| vfx_aura_buff                  | Generic buff aura (golden)            | 8      | 48×48  | P2       |
| vfx_aura_debuff                | Generic debuff aura (red)             | 8      | 48×48  | P2       |
| vfx_status_burn                | Burn DoT flame                        | 6      | 24×24  | P2       |
| vfx_status_poison              | Poison bubbles                       | 6      | 24×24  | P2       |
| vfx_status_stun                | Stun stars                           | 6      | 24×24  | P2       |
| vfx_ambient_dust               | Ambient dust motes (town)            | 8      | 16×16  | P3       |
| vfx_ambient_embers             | Ambient embers (combat areas)        | 8      | 16×16  | P3       |
| vfx_ambient_leaves             | Falling leaves (woodlands, Amberfall)| 8      | 16×16  | P3       |
| vfx_ambient_snow               | Snow particles (winter seasonal)     | 8      | 16×16  | P3       |
| vfx_screen_flash_lowhp         | Low HP red vignette pulse             | 4      | full-screen | P1 |
| vfx_screen_flash_death         | Death screen flash                    | 4      | full-screen | P1 |

**VFX total:** ~40 effects × ~6 frames avg ≈ **240 PNGs**.

### 5.9 Projectiles (separate from VFX — these are pooled Node2D sprites)

| Asset ID                     | Description                          | Frames | Canvas | Priority |
|------------------------------|--------------------------------------|--------|--------|----------|
| proj_arrow                    | Player arrow                          | 1 (rotated at runtime) | 16×4 | P0 |
| proj_greatarrow               | Great arrow                           | 1      | 24×6   | P2       |
| proj_arcane_orb               | Arcane orb                            | 4 (pulse) | 16×16 | P0 |
| proj_arcane_orb_big            | Giant orb                             | 4      | 24×24  | P2       |
| proj_fireball                 | Fireball                              | 4 (flicker) | 16×16 | P1 |
| proj_chain_lightning          | Lightning bolt                        | 4      | 32×32  | P2       |
| proj_light_shard              | Light shard                           | 4      | 16×16  | P3       |
| proj_laser_orb                | Laser orb                             | 4      | 16×16  | P3       |
| proj_laser                    | Laser beam                            | 1      | 32×4   | P3       |
| proj_magic_dagger             | Magic dagger                          | 4 (spin) | 16×16 | P2 |
| proj_pickaxe                  | Pickaxe throw                          | 4 (spin) | 24×24 | P2 |
| proj_throwing_knife           | Throwing knife                        | 1 (rotated) | 12×4 | P2 |
| proj_enemy_arrow              | Enemy arrow                           | 1      | 16×4   | P0       |
| proj_enemy_shaman_orb          | Shaman orb                            | 4      | 16×16  | P1       |
| proj_enemy_skeleton_orb       | Skeleton mage orb                     | 4      | 16×16  | P1       |
| proj_trail_fire               | Fire trail                            | 4      | 16×16  | P2       |
| proj_trail_magic              | Magic trail                           | 4      | 16×16  | P2       |

**Projectile total:** ~17 projectiles × ~3 frames avg ≈ **40 PNGs**.

### 5.10 Backgrounds & Full-Screen Art

| Asset ID                  | Description                          | Dimensions | Format | Priority |
|---------------------------|--------------------------------------|------------|--------|----------|
| bg_title                  | Title screen background              | 480×270    | PNG    | P1       |
| bg_origin_prison          | Prison origin backstory scene        | 320×180    | PNG    | P0       |
| bg_origin_farmhand        | Farmhand origin backstory            | 320×180    | PNG    | P1       |
| bg_origin_academy         | Academy scholar origin               | 320×180    | PNG    | P2       |
| bg_origin_hunters_child   | Hunter's child origin                | 320×180    | PNG    | P2       |
| bg_origin_library         | Library origin                       | 320×180    | PNG    | P2       |
| bg_death                  | Death screen background              | 480×270    | PNG    | P1       |
| bg_life_review            | Life review montage backdrop         | 480×270    | PNG    | P2       |
| bg_soul_perk_selection    | Soul perk selection backdrop         | 480×270    | PNG    | P2       |
| bg_reincarnation          | Reincarnation transition             | 480×270    | PNG    | P2       |
| bg_combat_arena_woods      | Combat arena backdrop — woods        | 320×180    | PNG    | P0       |
| bg_combat_arena_depths    | Combat arena backdrop — depths       | 320×180    | PNG    | P2       |
| bg_combat_arena_temple    | Combat arena backdrop — temple       | 320×180    | PNG    | P2       |
| bg_combat_arena_catacombs | Combat arena backdrop — catacombs    | 320×180    | PNG    | P2       |
| bg_combat_arena_mines     | Combat arena backdrop — mines        | 320×180    | PNG    | P2       |
| bg_combat_arena_boss      | Combat arena backdrop — boss         | 320×180    | PNG    | P3       |

**Background total:** 16 PNGs.

---

## 6. Audio List

### 6.1 Music (BGM)

All BGM is streamed Ogg Vorbis, 44.1 kHz, mono or stereo, looped. Files in `assets/audio/bgm/`.

| Asset ID                  | Description                          | Duration | Loop? | Loop points             | Format | Priority |
|---------------------------|--------------------------------------|----------|-------|-------------------------|--------|----------|
| bgm_title                 | Title screen — soft acoustic        | 1:30     | yes   | 0:08 → 1:28             | OGG    | P1       |
| bgm_town_ashvale          | Ashvale town — lo-fi ambient         | 2:40     | yes   | 0:12 → 2:38             | OGG    | P0       |
| bgm_town_alt              | Alternate town theme (night)         | 2:20     | yes   | 0:10 → 2:18             | OGG    | P2       |
| bgm_combat_woods          | Woodlands combat — chiptune          | 1:50     | yes   | 0:05 → 1:48             | OGG    | P0       |
| bgm_combat_depths         | Depths combat — darker chiptune     | 1:50     | yes   | 0:06 → 1:48             | OGG    | P2       |
| bgm_combat_temple         | Temple combat — ethereal             | 1:55     | yes   | 0:08 → 1:52             | OGG    | P2       |
| bgm_combat_catacombs     | Catacombs combat — haunting          | 1:55     | yes   | 0:05 → 1:52             | OGG    | P2       |
| bgm_combat_boss           | Boss combat — intense chiptune      | 2:10     | yes   | 0:10 → 2:08             | OGG    | P3       |
| bgm_quiet_years           | Quiet years — reflective piano       | 1:20     | yes   | 0:05 → 1:18             | OGG    | P2       |
| bgm_life_review           | Life review — bittersweet            | 1:40     | yes   | 0:08 → 1:38             | OGG    | P2       |
| bgm_soul_perk_selection  | Soul perk selection — hopeful        | 1:30     | yes   | 0:05 → 1:28             | OGG    | P2       |
| bgm_reincarnation        | Reincarnation transition             | 0:30     | no    | —                       | OGG    | P2       |
| bgm_season_greenrise     | Spring ambient stinger               | 0:25     | no    | —                       | OGG    | P3       |
| bgm_season_highsun       | Summer ambient stinger               | 0:25     | no    | —                       | OGG    | P3       |
| bgm_season_amberfall     | Autumn ambient stinger               | 0:25     | no    | —                       | OGG    | P3       |
| bgm_turn_of_the_year     | Turn-of-the-year fanfare             | 0:35     | no    | —                       | OGG    | P3       |

**BGM total:** 16 tracks. Loop points are sample-accurate; the audio loader (`audio_bgm.gd`) sets `loop_begin` / `loop_end` from a sidecar `.loop.txt` file (one per BGM, format: `begin_sec end_sec`).

### 6.2 SFX

All SFX are WAV (uncompressed for low latency) or OGG (short, < 3 sec). Files in `assets/audio/sfx/`.

| Asset ID                  | Description                          | Duration | Format | Priority |
|---------------------------|--------------------------------------|----------|--------|----------|
| sfx_attack_sword_slash    | Sword swing                           | 0.20     | WAV    | P0       |
| sfx_attack_sword_hit      | Sword hit                             | 0.18     | WAV    | P0       |
| sfx_attack_bow_draw       | Bow draw                               | 0.25     | WAV    | P0       |
| sfx_attack_bow_release    | Bow release                            | 0.10     | WAV    | P0       |
| sfx_attack_bow_hit        | Arrow hit                              | 0.15     | WAV    | P0       |
| sfx_attack_staff_cast     | Staff cast                             | 0.30     | WAV    | P1       |
| sfx_attack_staff_hit      | Staff orb hit                          | 0.18     | WAV    | P1       |
| sfx_attack_dagger_slash   | Dagger slash                           | 0.15     | WAV    | P2       |
| sfx_hit_player            | Player takes damage                    | 0.25     | WAV    | P0       |
| sfx_hit_enemy             | Enemy takes damage                     | 0.18     | WAV    | P0       |
| sfx_hit_crit              | Critical hit sting                     | 0.30     | WAV    | P1       |
| sfx_hit_block             | Block clang                            | 0.20     | WAV    | P1       |
| sfx_hit_dodge             | Dodge whoosh                           | 0.15     | WAV    | P2       |
| sfx_death_enemy           | Enemy death poof                       | 0.40     | WAV    | P0       |
| sfx_death_player          | Player death                           | 0.80     | WAV    | P1       |
| sfx_levelup               | Level-up chime                         | 0.60     | WAV    | P1       |
| sfx_perk_unlock           | Perk unlock sting                      | 0.50     | WAV    | P1       |
| sfx_lp_grant              | Legend Point gained                    | 0.30     | WAV    | P2       |
| sfx_item_pickup           | Item pickup                            | 0.20     | WAV    | P0       |
| sfx_item_equip            | Item equip clink                       | 0.18     | WAV    | P1       |
| sfx_item_drop             | Item drop                              | 0.20     | WAV    | P1       |
| sfx_gold_pickup           | Gold coin pickup                       | 0.18     | WAV    | P0       |
| sfx_ui_hover              | UI hover blip                          | 0.05     | WAV    | P1       |
| sfx_ui_click               | UI click                               | 0.06     | WAV    | P1       |
| sfx_ui_confirm            | UI confirm                             | 0.10     | WAV    | P1       |
| sfx_ui_back               | UI back                                | 0.08     | WAV    | P1       |
| sfx_ui_error              | UI error buzz                          | 0.15     | WAV    | P2       |
| sfx_ui_tab_open           | Tab open slide                         | 0.20     | WAV    | P1       |
| sfx_ui_tab_close          | Tab close slide                        | 0.20     | WAV    | P1       |
| sfx_dialogue_advance     | Dialogue page advance                   | 0.10     | WAV    | P0       |
| sfx_dialogue_open         | Dialogue box open                      | 0.15     | WAV    | P0       |
| sfx_shop_open             | Shop open                               | 0.20     | WAV    | P1       |
| sfx_shop_buy              | Shop buy (coin clink)                  | 0.18     | WAV    | P1       |
| sfx_shop_sell             | Shop sell                              | 0.18     | WAV    | P1       |
| sfx_shop_error            | Shop cannot afford                     | 0.20     | WAV    | P2       |
| sfx_quest_accept          | Quest accept                           | 0.30     | WAV    | P1       |
| sfx_quest_complete        | Quest complete fanfare                 | 0.80     | WAV    | P1       |
| sfx_door_open             | Door open creak                        | 0.40     | WAV    | P1       |
| sfx_door_close            | Door close                             | 0.30     | WAV    | P1       |
| sfx_footstep_grass        | Footstep on grass                      | 0.08     | WAV    | P2       |
| sfx_footstep_stone        | Footstep on stone                      | 0.08     | WAV    | P2       |
| sfx_footstep_wood         | Footstep on wood                       | 0.08     | WAV    | P2       |
| sfx_ability_analyze       | Analyze lock-on                         | 0.40     | WAV    | P1       |
| sfx_ability_assassinate   | Assassinate dash                        | 0.30     | WAV    | P1       |
| sfx_ability_beartrap      | Beartrap throw + arm                    | 0.40     | WAV    | P2       |
| sfx_ability_bowl_of_fire  | Fireball cast                           | 0.30     | WAV    | P1       |
| sfx_ability_chain_lightning| Chain lightning zap                    | 0.50     | WAV    | P2       |
| sfx_ability_giant_orb     | Giant orb cast                         | 0.35     | WAV    | P2       |
| sfx_ability_guardian_spirit| Guardian spirit activation             | 0.60     | WAV    | P2       |
| sfx_ability_magic_dagger  | Magic dagger orbit                      | 0.20     | WAV    | P2       |
| sfx_ability_pickaxe_throw | Pickaxe throw                           | 0.30     | WAV    | P2       |
| sfx_ability_piercing_strike| Piercing strike                         | 0.25     | WAV    | P1       |
| sfx_ability_rejuvenation  | Rejuvenation heal                       | 0.40     | WAV    | P2       |
| sfx_ability_sweeping_slash | Sweeping slash                          | 0.30     | WAV    | P1       |
| sfx_ability_throwing_knives| Throwing knives                        | 0.30     | WAV    | P2       |
| sfx_ability_wrath         | Wrath AoE burst                         | 0.50     | WAV    | P2       |
| sfx_status_burn           | Burn tick                               | 0.15     | WAV    | P2       |
| sfx_status_poison         | Poison tick                             | 0.15     | WAV    | P2       |
| sfx_status_stun           | Stun impact                             | 0.20     | WAV    | P2       |
| sfx_save_write            | Save write beep                         | 0.20     | WAV    | P2       |
| sfx_save_load             | Save load                               | 0.20     | WAV    | P2       |
| sfx_quiet_years_advance  | Quiet years year tick                   | 0.15     | WAV    | P2       |
| sfx_reincarnation_begin   | Reincarnation begin                     | 0.80     | WAV    | P2       |
| sfx_reincarnation_complete| Reincarnation complete                  | 0.60     | WAV    | P2       |

**SFX total:** ~58 files. Many share a single source recording with variations; aim for 6–8 distinct source sounds at P0 and reuse variants.

### 6.3 Ambient

Looping ambient beds, lower priority than BGM, ducked under BGM at -12 dB.

| Asset ID              | Description                          | Duration | Loop? | Format | Priority |
|-----------------------|--------------------------------------|----------|-------|--------|----------|
| amb_town_market       | Town market chatter                  | 2:00     | yes   | OGG    | P2       |
| amb_town_night        | Town night crickets                  | 2:00     | yes   | OGG    | P3       |
| amb_woods_day         | Woodlands birdsong                   | 2:30     | yes   | OGG    | P2       |
| amb_woods_night       | Woodlands night owls                 | 2:30     | yes   | OGG    | P3       |
| amb_depths_cave       | Cave echo drips                      | 2:00     | yes   | OGG    | P2       |
| amb_temple_hum        | Temple resonant hum                   | 2:00     | yes   | OGG    | P3       |
| amb_wind_open         | Open-area wind                        | 1:30     | yes   | OGG    | P3       |
| amb_rain              | Rain (seasonal)                       | 2:00     | yes   | OGG    | P3       |

**Ambient total:** 8 tracks.

### 6.4 Stingers (one-shot musical accents)

| Asset ID                | Description                          | Duration | Format | Priority |
|-------------------------|--------------------------------------|----------|--------|----------|
| stinger_perk_unlock     | Perk unlock flourish                 | 0.80     | OGG    | P2       |
| stinger_life_review     | Life review begin                    | 1.20     | OGG    | P2       |
| stinger_reincarnation  | Reincarnation flourish               | 1.00     | OGG    | P2       |
| stinger_boss_intro      | Boss intro danger                    | 0.80     | OGG    | P3       |
| stinger_season_change   | Season change                        | 0.60     | OGG    | P3       |
| stinger_turn_of_year   | Turn-of-the-year                     | 1.00     | OGG    | P3       |

**Stinger total:** 6 tracks.

---

## 7. Fonts

Godot uses `.ttf`/`.otf` fonts imported with `filter = false` and a `FixedSize` for pixel-perfect rendering.

| Asset ID                | Description                          | Size(s)        | Format | Priority |
|-------------------------|--------------------------------------|----------------|--------|----------|
| font_pixel_body         | Body text (parchment)                | 8, 12, 16 px   | TTF    | P0       |
| font_pixel_header       | Headers, titles                      | 16, 24, 32 px  | TTF    | P0       |
| font_pixel_dialogue     | Dialogue                             | 12 px          | TTF    | P0       |
| font_pixel_mono         | Monospace for stats / numbers        | 8, 12 px       | TTF    | P1       |
| font_pixel_small_caps   | Small caps for UI labels             | 10 px          | TTF    | P1       |
| font_pixel_title        | Title logo display font              | 48, 64 px      | TTF    | P1       |

**Font total:** 6 TTF files. All must be open-source or licensed for game use (e.g. Press Start 2P, VT323, Pixelated MS Sans Serif). The pixel body font should support full Latin-1 + common accented chars for future localization.

---

## 8. Shaders

| Asset ID            | Description                                       | Priority |
|---------------------|---------------------------------------------------|----------|
| shader_crt          | CRT scanline + bloom (toggleable)                 | P2       |
| shader_outline      | Sprite outline (used for selection highlights)   | P1       |
| shader_tint         | Tint shader (status effect auras)                 | P1       |
| shader_pixelation    | Pixelation post-effect for death dissolve         | P2       |
| shader_vignette     | Vignette for low HP warning                        | P1       |
| shader_dissolve     | Dissolve transition (death, scene fades)          | P1       |
| shader_water         | Water surface animation (tilemap shader)          | P3       |

**Shader total:** 7 `.gdshader` files.

---

## 9. Total Asset Count Estimate

| Category            | Files | Notes                                   |
|---------------------|-------|-----------------------------------------|
| Player sprites      | 344   | 4 stages × 68 + 72 weapon overlays     |
| NPC sprites + portraits | 216 | 8 NPCs × (24 + 3)                       |
| Enemy sprites       | ~660  | 30 enemies × ~22 frames                 |
| Tilesets            | ~540  | ~14 sets, reused via flips              |
| Item icons          | 118   | 110 items + 8 rarity borders            |
| Ability/perk icons  | 86    | 14 ability + 32 perk + 12 soul + 18 misc|
| UI assets           | ~120  | Panels, buttons, bars, frames, cursors  |
| VFX                 | ~240  | ~40 effects × ~6 frames                 |
| Projectiles         | ~40   | 17 projectiles × ~3 frames              |
| Backgrounds         | 16    | Full-screen art                         |
| BGM                 | 16    | Looped + stingers                        |
| SFX                 | 58    | WAV for low latency                      |
| Ambient             | 8     | Looped beds                              |
| Stingers            | 6     | Musical accents                          |
| Fonts               | 6     | TTF                                      |
| Shaders             | 7     | `.gdshader`                              |
| **TOTAL**           | **~2,481** | Files (some are `.tres` StyleBox resources) |

The demo vertical slice (Phase 0–1) needs only **P0 + critical P1** assets — roughly **~450 files**. Full game needs the entire count above.

---

## 10. Priority Tiers

Priority gates which assets to build first. P0 ships in the demo, P1 by Phase 2, P2 by Phase 3, P3 by Phase 4 (full release).

### P0 — Foundation (Phase 0–1, demo)
- Player sprite (Young stage only, idle + walk + attack + hurt + death)
- Prison guard NPC (overworld + portrait)
- 4 enemies (slime blue, bat, brown wolf, training dummy)
- Town tileset (ground + walls)
- Woodlands tileset (ground + trees)
- 10 weapon icons (sword tiers 1–4, bow tier 1, staff tier 1)
- 6 consumable icons (berries, herbs, holy water, etc.)
- 6 stat icons + 8 resource icons
- HUD (HP bar, energy bar, parchment panel, default button, dialog box, cursors)
- Origin portrait for prison + prison backstory background
- 1 BGM town + 1 BGM combat (woods)
- 12 SFX (sword swing/hit, bow draw/release/hit, player hit, enemy death, level-up, item pickup, gold pickup, dialogue advance, UI click)
- 2 fonts (body + header)
- 1 shader (outline)

**P0 count: ~450 files.** This is the minimum to ship the 5-minute test.

### P1 — Core Loop (Phase 2, vertical slice complete)
- Player Veteran stage
- 5 key NPCs (Ashvale merchant, Father Alric, Grey Wizard, Helga, Mizgrub) — overworld + portraits
- 8 more enemies (slime green/red, danger wolf, goblin spear/archer, skeleton knight/archer, sparrer)
- Town interior tileset + woodlands props
- Remaining weapon/armor/shield icons
- 14 ability icons
- 32 perk icons
- Full UI kit (tabs, scrollbars, frames, ability slots, item slots, perk nodes, region map, POI symbols, tooltips)
- Title screen art + logo + buttons
- 4 more BGM (combat depths/temple/catacombs + boss)
- Quiet years BGM + life review BGM
- ~30 more SFX (all abilities + UI interactions + shop + quest)
- Rejuvenation ability SFX + footstep variants
- 4 more fonts + 4 more shaders

**P1 count: ~700 additional files.**

### P2 — Content Depth (Phase 3)
- Player Elder + Decrepit stages
- 5 more NPCs (Lunorak, goods peddler, ilaf, others)
- 8 more enemies (spider, snake, rat, goblin mage, skeleton mage, ent, entling, kobold)
- Dead woodlands, depths, dungeon tilesets (catacombs, mines, temple)
- All remaining item icons (accessories, books, tools, keys, clothing, quivers)
- 12 soul perk icons
- 3 season icons
- Death screen, life review, quiet years, soul perk selection UI
- 5 more BGM (alt town, boss combat, quiet years, life review, soul perk selection, reincarnation)
- All remaining ability SFX
- All ambient beds
- All stingers
- 4 more backgrounds (death, life review, reincarnation, soul perk)

**P2 count: ~900 additional files.**

### P3 — Polish & Full Release (Phase 4)
- Player magic weapon overlay (full set)
- 6 more enemies (ooze, leech, beholder, mimic, golem, spirit)
- Ancient Stone Guardian boss
- Valenthar region tileset (demo-locked but ship-ready)
- All remaining misc icons (keys, relics)
- Boss intro stinger, season stingers, turn-of-the-year
- Rain ambient, night ambients
- CRT shader, water shader
- Title backdrop variations
- Optional cosmetic heirlooms

**P3 count: ~430 additional files.**

### Priority Build Order (Top 25)

If the team can only build 25 assets first, in order:

1. `char_player_young_idle_*` (16 PNGs)
2. `char_player_young_walk_*` (24 PNGs)
3. `tile_town_ground` (24 tiles)
4. `tile_town_walls` (36 tiles)
5. `mob_slime_blue` (14 PNGs)
6. `mob_bat` (18 PNGs)
7. `mob_wolf2` (24 PNGs)
8. `mob_dummy` (3 PNGs)
9. `icon_stat_*` (6 PNGs)
10. `icon_resource_gold`, `icon_resource_hp`, `icon_resource_energy` (3 PNGs)
11. `ui_panel_parchment` (StyleBox)
12. `ui_button_default` (3 states)
13. `ui_dialog_box` (StyleBox)
14. `ui_frame_hp_bar` (2 PNGs)
15. `ui_frame_energy_bar` (2 PNGs)
16. `icon_item_sword_1`–`icon_item_sword_4` (4 PNGs)
17. `icon_item_holy_water` (1 PNG)
18. `port_npc_prison_guard` (3 PNGs)
19. `bg_origin_prison` (1 PNG)
20. `bgm_town_ashvale` (1 OGG)
21. `bgm_combat_woods` (1 OGG)
22. `sfx_attack_sword_slash` + `sfx_attack_sword_hit` (2 WAV)
23. `sfx_hit_player` + `sfx_death_enemy` (2 WAV)
24. `sfx_levelup` (1 WAV)
25. `font_pixel_body` + `font_pixel_header` (2 TTF)

This unblocks the entire Phase 0 milestone.

---

## 11. Asset Delivery & Import

### 11.1 Per-File Requirements

- Every PNG: 32-bit RGBA, no extraneous metadata, optimized with `pngcrush` or `oxipng` to <2 KB per 16×16 tile, <8 KB per 48×48 sprite frame.
- Every `.aseprite`: layered, with frame tags matching animation names (`idle`, `walk_n`, `walk_s`, `walk_e`, `walk_w`, `attack_n`, …). No unused layers.
- Every OGG: 44.1 kHz, q=5 Vorbis, mono for SFX, stereo for BGM. Loop files include a sidecar `<name>.loop.txt` with `begin_sec end_sec`.
- Every WAV: 44.1 kHz, 16-bit, mono.
- Every TTF: subsetted to Latin-1 + accented chars; no kerning issues at small sizes.
- Every StyleBoxTexture `.tres`: 9-slice margins set explicitly (no auto-detect).
- Every `SpriteFrames` `.tres`: animation names match the Aseprite frame tags exactly; loop mode = LOOP for idle/walk, ONCE for attack/hurt/death/vfx.

### 11.2 Godot Import Settings

- All sprites: `texture filter = NEAREST`, `compression = lossless`, `mipmaps = false`.
- All audio: BGM `loop = true`; SFX `loop = false`.
- All fonts: `filter = false`, `subpixel = none`, `hinting = none`.
- All shaders: `mode = canvas_item` (2D).

### 11.3 Build Pipeline

```
Aseprite sources (assets/sprites/**/*.aseprite)
        │  tools/export_aseprite.gd (Godot headless --script)
        ▼
Exported PNG sheets (assets/sprites/**/*.png)
        │  tools/slice_spritesheet.gd (slices into per-frame PNGs)
        ▼
Per-frame PNGs + SpriteFrames .tres
        │  Godot import (auto on project open)
        ▼
.tres resources registered in scripts/_generated/resource_index.gd
```

CI runs `tools/export_aseprite.gd` on every commit; if any `.aseprite` is newer than its `.png`, the build fails until the artist re-exports. This prevents "the .aseprite has an animation the .png doesn't" drift bugs.

### 11.4 Validation Checklist (per asset)

- [ ] File follows the naming convention (§2)
- [ ] File is in the correct folder (§3)
- [ ] PNG dimensions match the spec (§5)
- [ ] PNG uses the palette (§1) — no out-of-palette colors
- [ ] Aseprite has frame tags matching animation names
- [ ] Animation loops seamlessly (for looping animations)
- [ ] No anti-aliasing; hard pixel edges
- [ ] Outline color is `#1B1410` (not pure black) where outlined
- [ ] Audio loop points are set (for BGM)
- [ ] StyleBoxTexture has correct 9-slice margins
- [ ] SpriteFrames `.tres` animation names match Aseprite tags

---

## 12. Accessibility Notes

- **Color-blind safety:** never encode rarity by color alone — always pair color with a symbol (e.g. gray = square, green = triangle, blue = diamond, red = star, gold = crown). The 8 rarity borders already ship as distinct shapes, not just colors.
- **Text legibility:** body font minimum 12 px on screen (after upscale); never below 10 px equivalent. Dialogue text 12 px minimum.
- **Reduce motion:** a Settings toggle disables VFX particles and screen shake; only the gameplay-critical VFX (hit spark, level-up) remain.
- **Audio cues:** every gameplay event has both a visual and an audio cue — no information conveyed by sound alone.

---

## 13. Out-of-Scope (Not in v1.0)

- Voice acting (text-only dialogue).
- 3D models or pre-rendered backgrounds.
- Animated cutscenes beyond the in-engine story web pages.
- User-generated content tools (modding opens via define-it but no UI is shipped).
- Mobile / touch-specific assets (the UI is keyboard/mouse first; touch is best-effort).
- Multiplayer-specific assets.

---

End of `ASSET_SPEC.md`. For systems layout, see `ARCHITECTURE.md`. For data shapes, see `DATA_MODELS.md`.