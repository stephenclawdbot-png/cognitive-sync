# v1.0.00 "wizdung" — Complete Asset Specification

> **Purpose:** Every visual and audio asset needed, with specifications, naming, and priority.
> **Usage:** Hand this to artists / generate assets via PixelLab API.
> **Companion docs:** SPRITE_MANIFEST.md (existing sprites), START_HERE.md

---

## 1. ASSET NAMING CONVENTIONS

```
sprites/
├── characters/{class_name}/{direction}.png        # e.g., dex-wizard/south.png
├── enemies/{enemy_name}.png                        # e.g., skeleton-warrior.png
├── items/{item_name}.png                           # e.g., health-potion.png
├── equipment/{equipment_name}.png                   # e.g., iron-sword.png
├── npcs/{npc_name}.png                             # e.g., mysterious-wizard.png
├── tiles/{tileset_name}/{tile_type}.png            # e.g., stone-dungeon/floor.png
├── vfx/{effect_name}.png                           # e.g., fire-hit.png
├── ui/{element_name}.png                           # e.g., health-bar-bg.png

audio/
├── sfx/{action}_{target}.wav                       # e.g., sword_hit.wav
├── music/{track_name}_intro.wav                    # e.g., dungeon_intro.wav
├── music/{track_name}_loop.wav                     # e.g., dungeon_loop.wav
```

---

## 2. CHARACTER SPRITES

### 2.1 Playable Characters (8-directional)

| Class | Size (px) | Canvas (px) | Directions | Frames/Dir | Status |
|-------|-----------|-------------|------------|------------|--------|
| Dex Wizard | 48×48 | ~68×68 | 8 | 1 (static) | ✅ DONE |
| Int Wizard | 48×48 | ~68×68 | 8 | 1 (static) | ✅ DONE |
| Str Wizard | 48×48 | ~68×68 | 8 | 1 (static) | ✅ DONE |
| Ranger | 48×48 | ~68×68 | 8 | 1 (static) | ❌ NEEDED |
| Paladin | 48×48 | ~68×68 | 8 | 1 (static) | ❌ NEEDED |
| Necromancer | 48×48 | ~68×68 | 8 | 1 (static) | ❌ NEEDED |
| Berserker | 48×48 | ~68×68 | 8 | 1 (static) | ❌ NEEDED |
| Rogue | 48×48 | ~68×68 | 8 | 1 (static) | ❌ NEEDED |
| Battle Mage | 48×48 | ~68×68 | 8 | 1 (static) | ❌ NEEDED |

### 2.2 Animation Spritesheets (per character class)

Each character needs these animation states, each as an 8-direction spritesheet:

| Animation | Frame Count | Frame Size | Total Frames (8 dirs) | Priority |
|-----------|------------|-----------|----------------------|----------|
| Idle | 4 (loop) | 48×48 | 32 | P1 (Phase 1) |
| Walk | 8 (loop) | 48×48 | 64 | P1 (Phase 1) |
| Basic Attack | 6 | 48×48 | 48 | P1 (Phase 1) |
| Dash | 4 | 48×48 | 32 | P1 (Phase 1) |
| Special Attack | 8 | 48×48 | 64 | P2 (Phase 3) |
| Death | 10 | 48×48 | 80 | P2 (Phase 2) |
| Stunned | 2 (loop) | 48×48 | 16 | P3 (Phase 4) |

**Total per character:** 244 frames × 9 classes = 2,196 animation frames

### 2.3 Character Portraits

| Portrait | Size | Purpose | Status |
|----------|------|---------|--------|
| Dex Wizard Portrait | 64×64 | Dialog UI | ❌ NEEDED |
| Int Wizard Portrait | 64×64 | Dialog UI | ❌ NEEDED |
| Str Wizard Portrait | 64×64 | Dialog UI | ❌ NEEDED |
| Mysterious Wizard Portrait | 64×64 | Dialog UI | ❌ NEEDED |
| Trinket Witch Portrait | 64×64 | Dialog UI | ❌ NEEDED |

---

## 3. ENEMY SPRITES

### 3.1 Enemy Types

| Enemy | Size (px) | Animation Frames | Priority | Status |
|-------|-----------|-----------------|----------|--------|
| Skeleton Warrior | 48×48 | idle(4), walk(6), attack(4), death(6) | P1 | ✅ Static only |
| Skeleton Archer | 48×48 | idle(4), walk(6), attack(4), death(6) | P1 | ✅ Static only |
| Elite Skeleton Knight | 48×48 | idle(4), walk(6), attack(4), death(6) | P2 | ✅ Static only |
| Mimic | 48×48 | idle(4), attack(4), death(6) | P1 | ✅ Static only |
| Elite Mimic | 48×48 | idle(4), attack(4), death(6) | P2 | ✅ Static only |
| Dungeon Boss | 64×64 | idle(4), walk(6), attack(6), slam(6), summon(4), death(10) | P2 | ✅ Static only |

### 3.2 Additional Enemies Needed

| Enemy | Size (px) | Description | Priority |
|-------|-----------|-------------|----------|
| Skeleton Mage | 48×48 | Ranged frost caster | P2 |
| Ghost | 48×48 | Floating, phases through walls (visual only) | P3 |
| Slime | 32×32 | Small, swarming | P2 |
| Elite Skeleton Archer | 48×48 | Blue-tinted, higher stats | P3 |
| Cave Bat | 32×32 | Fast, swarming, flying | P3 |
| Stone Golem | 64×64 | Slow, tanky, heavy hitter | P3 |
| Lich (mini-boss) | 64×64 | Necromancer boss, summons skeletons | P3 |
| Dragon (endgame boss) | 96×96 | Final boss, fire breath | P3 |

---

## 4. ITEM & PICKUP SPRITES

### 4.1 Glob Pickups

| Item | Size (px) | Description | Status |
|------|-----------|-------------|-------|
| Health Potion | 32×32 | Red bottle, floating animation | ✅ DONE |
| Mana Potion | 32×32 | Blue bottle, floating animation | ✅ DONE |
| Gold Coins | 32×32 | Stack of coins, sparkle | ✅ DONE |
| Iron Key | 32×32 | Rusty key, slight rotation | ✅ DONE |
| Health Glob | 32×32 | Red orb (dropped by enemies) | ❌ NEEDED |
| Mana Glob | 32×32 | Blue orb (dropped by enemies) | ❌ NEEDED |
| XP Glob | 32×32 | Green/yellow orb | ❌ NEEDED |
| Money Glob | 32×32 | Gold orb | ❌ NEEDED |

### 4.2 Equipment Sprites

| Item | Size (px) | Description | Status |
|------|-----------|-------------|-------|
| Iron Sword | 32×32 | Basic weapon | ✅ DONE |
| Magic Staff | 32×32 | Magic weapon | ✅ DONE |
| Dagger | 32×32 | Dex weapon | ❌ NEEDED |
| Battle Axe | 32×32 | Str weapon | ❌ NEEDED |
| Wand | 32×32 | Int weapon | ❌ NEEDED |
| Bow | 32×32 | Ranger weapon | ❌ NEEDED |
| Shield | 32×32 | Paladin off-hand | ❌ NEEDED |
| Cloth Armor | 32×32 | Chest - Dex | ❌ NEEDED |
| Robe | 32×32 | Chest - Int | ❌ NEEDED |
| Plate Armor | 32×32 | Chest - Str | ❌ NEEDED |
| Leather Armor | 32×32 | Chest - Generic | ❌ NEEDED |
| Helmet (Iron) | 32×32 | Head | ❌ NEEDED |
| Wizard Hat | 32×32 | Head - Int | ❌ NEEDED |
| Hood | 32×32 | Head - Dex | ❌ NEEDED |
| War Helm | 32×32 | Head - Str | ❌ NEEDED |
| Boots (Leather) | 32×32 | Feet | ❌ NEEDED |
| Boots (Iron) | 32×32 | Feet | ❌ NEEDED |
| Ring (Gold) | 32×32 | Accessory | ❌ NEEDED |
| Ring (Emerald) | 32×32 | Accessory - Dex | ❌ NEEDED |
| Ring (Sapphire) | 32×32 | Accessory - Int | ❌ NEEDED |
| Ring (Ruby) | 32×32 | Accessory - Str | ❌ NEEDED |
| Necklace (Gold) | 32×32 | Accessory | ❌ NEEDED |
| Amulet | 32×32 | Accessory | ❌ NEEDED |

---

## 5. NPC SPRITES

| NPC | Size (px) | Description | Status |
|-----|-----------|-------------|-------|
| Mysterious Wizard | 48×48 | Identify/respec NPC | ✅ DONE |
| Trinket Witch | 48×48 | Enchant/sell NPC | ✅ DONE |
| Instruction Man | 48×48 | Tutorial NPC | ❌ NEEDED |
| NPC Dex Wizard | 48×48 | Class switch NPC | ✅ (uses char sprite) |
| NPC Int Wizard | 48×48 | Class switch NPC | ✅ (uses char sprite) |
| NPC Str Wizard | 48×48 | Class switch NPC | ✅ (uses char sprite) |

---

## 6. TILESET SPRITES

### 6.1 Required Tilesets (32×32 px each tile)

| Tileset | Tiles Needed | Description | Priority |
|---------|-------------|-------------|----------|
| Hub | 12 | Wood floor, stone floor, carpet, wall, doorway, portal pad | P1 |
| Tutorial Dungeon | 8 | Floor, wall, wall_top, corner, door, door_frame | P1 |
| Stone Dungeon | 16 | floor, cracked_floor, wall, wall_top, pillar, door, door_locked, stairs, rubble, torch_wall, chest_closed, chest_open, barrel, crate, bones, cobweb | P1 |
| Cave Dungeon | 14 | cave_floor, rock_wall, stalactite, moss, crystal, water_pool, door, door_locked, mushroom, rock_pile, cave_entrance, torch, chest, gem_vein | P2 |
| Overgrown Dungeon | 14 | mossy_floor, vine_wall, root, ancient_pillar, cracked_stone, vine_door, locked_vine_door, fern, flower, ancient_chest, broken_statue, tree_root, moss_patch, vine_overhang | P2 |
| Desert Dungeon | 12 | sand_floor, sandstone_wall, cracked_floor, sand_dune, cactus, pillar, sand_door, locked_sand_door, oasis_pool, skeleton_remains, treasure_chest, hieroglyph_wall | P3 |

### 6.2 Tile Variations

Each floor/wall tile should have 2-3 variations for visual interest:
- Floor: clean, cracked, decorated (with debris/bones)
- Wall: clean, damaged, decorated (with torch/banner)

---

## 7. VFX SPRITES

### 7.1 Combat VFX (each is a short animation, 4-8 frames)

| VFX | Size (px) | Frames | Description | Priority |
|-----|-----------|--------|-------------|----------|
| Hit Spark (physical) | 32×32 | 4 | White/yellow impact spark | P1 |
| Fire Hit | 32×32 | 6 | Orange/red flame burst | P1 |
| Frost Hit | 32×32 | 6 | Blue ice shard burst | P1 |
| Lightning Hit | 32×32 | 6 | Yellow/white electric arc | P1 |
| Blood Splash | 32×32 | 4 | Red particles (enemy hit) | P1 |
| Death Explosion | 48×48 | 8 | Enemy death particle burst | P1 |
| Dash Ghost Trail | 48×48 | 4 | Fading player silhouette | P1 |
| Crit Indicator | 32×32 | 4 | Star/crash effect on crit | P1 |
| Level Up Burst | 64×64 | 8 | Golden radial burst | P2 |
| Pick Up Sparkle | 16×16 | 4 | Small sparkle on item pickup | P1 |
| Health Glob VFX | 32×32 | 6 | Green healing effect | P2 |
| Mana Glob VFX | 32×32 | 6 | Blue mana effect | P2 |
| Gold Pickup VFX | 32×32 | 6 | Gold particle burst | P2 |
| XP Pickup VFX | 32×32 | 6 | Yellow/green particle | P2 |
| Shock Ground | 48×48 | 8 | Electric ground effect (Dex dash) | P2 |
| Frost Trail | 48×48 | 6 | Frosty ground trail (Int blink) | P2 |
| Explosion (kill) | 64×64 | 8 | Large explosion from ExplodeOnKill | P2 |
| Frost Nova | 64×64 | 8 | Expanding frost ring | P2 |
| Blizzard AOE | 96×96 | 16 | Large frost storm area | P3 |
| Whirlwind | 64×64 | 8 | Spinning slash effect | P3 |
| Ground Slam | 64×64 | 8 | Shockwave on ground | P3 |
| Berserk Aura | 48×48 | 8 (loop) | Red pulsing aura around player | P3 |
| Ethereal Shield | 48×48 | 6 (loop) | Blue shimmering shield | P3 |
| Summon Effect | 48×48 | 6 | Dark purple summon circle | P3 |
| Portal Entry | 64×64 | 8 (loop) | Swirling portal effect | P2 |
| Boss Slam Impact | 96×96 | 8 | Screen-wide slam effect | P3 |

### 7.2 UI VFX

| VFX | Size (px) | Frames | Description | Priority |
|-----|-----------|--------|-------------|----------|
| Damage Number (white) | Varies | 1 | Floating damage text | P1 |
| Damage Number (crit) | Varies | 1 | Larger, yellow, bold | P1 |
| Heal Number (green) | Varies | 1 | Floating heal text | P1 |
| Mana Number (blue) | Varies | 1 | Floating mana text | P1 |
| Gold Number (gold) | Varies | 1 | Floating gold text | P1 |
| XP Number (white) | Varies | 1 | Floating XP text | P1 |
| Screen Flash (hit) | Full | 1 | Red flash on player hit | P1 |
| Screen Flash (heal) | Full | 1 | Green flash on heal | P2 |

---

## 8. UI ELEMENTS

### 8.1 HUD Elements

| Element | Size (px) | Description | Priority |
|---------|-----------|-------------|----------|
| Health Bar BG | 200×20 | Dark panel with border | P1 |
| Health Bar Fill | 200×20 | Red gradient fill | P1 |
| Mana Bar BG | 200×16 | Dark panel with border | P1 |
| Mana Bar Fill | 200×16 | Blue gradient fill | P1 |
| Skill Icon (basic) | 32×32 | Basic attack icon | P1 |
| Skill Icon (special) | 32×32 | Special attack icon | P1 |
| Skill Icon (dash) | 32×32 | Dash icon | P1 |
| Skill Cooldown Overlay | 32×32 | Radial sweep overlay | P1 |
| Boss Health Bar BG | 400×30 | Large boss bar background | P2 |
| Boss Health Bar Fill | 400×30 | Red gradient, animated | P2 |
| Boss Name Plate | 200×30 | Name display | P2 |
| Room Info Display | 150×40 | Room level + enemies remaining | P2 |
| Minimap (optional) | 128×128 | Small room overview | P3 |
| Key Icon | 16×16 | Key indicator in HUD | P2 |
| Gold Counter | 100×20 | Gold amount display | P1 |
| Level Counter | 40×20 | Level display | P1 |
| XP Bar | 200×8 | Thin XP progress bar | P1 |

### 8.2 Menu Panels

| Panel | Size (px) | Description | Priority |
|-------|-----------|-------------|----------|
| Main Menu BG | 640×360 | Title screen background | P2 |
| Main Menu Title | 400×100 | Game logo/title | P2 |
| Character Select Panel | 300×400 | Class selection | P2 |
| Inventory Panel BG | 400×300 | Dark panel background | P1 |
| Inventory Slot | 40×40 | Individual item slot | P1 |
| Equipment Slot | 40×40 | Equipment slot (with icon) | P1 |
| Skill Tree Panel BG | 500×400 | Skill tree background | P2 |
| Skill Node (unallocated) | 24×24 | Gray circle | P2 |
| Skill Node (allocated) | 24×24 | Glowing circle | P2 |
| Skill Node (locked) | 24×24 | Dark with lock icon | P2 |
| Skill Connector Line | Variable | Line between nodes | P2 |
| Dialog Box BG | 500×120 | Dialog panel | P1 |
| Dialog Portrait Frame | 64×64 | Portrait border | P1 |
| Merchant Panel BG | 400×300 | Shop panel | P2 |
| Stash Panel BG | 400×300 | Stash panel | P2 |
| Settings Panel BG | 400×300 | Settings panel | P2 |
| Pause Menu BG | 300×200 | Pause overlay | P2 |
| Save Slot Panel | 300×80 | Save slot display | P2 |
| Button (normal) | 120×32 | Standard button | P1 |
| Button (hover) | 120×32 | Hover state | P1 |
| Button (pressed) | 120×32 | Pressed state | P1 |
| Tooltip BG | 200×100 | Item tooltip | P1 |
| Tooltip Rarity Frame | 200×4 | Colored rarity border | P1 |

### 8.3 Rarity Color References

| Rarity | Hex Color | RGB | Usage |
|--------|-----------|-----|-------|
| Common | #9a9a9a | (154, 154, 154) | Item frame, tooltip border |
| Magic | #5b8af7 | (91, 138, 247) | Item frame, tooltip border |
| Rare | #f7d050 | (247, 208, 80) | Item frame, tooltip border |
| Epic | #a855f7 | (168, 85, 247) | Item frame, tooltip border |
| Legendary | #f79025 | (247, 144, 37) | Item frame, tooltip border + glow |

---

## 9. AUDIO SPECIFICATION

### 9.1 SFX (Sound Effects)

| Sound | Duration | Format | Description | Priority |
|-------|----------|--------|-------------|----------|
| Dash | 0.3s | WAV | Quick whoosh | P1 |
| Sword Swing | 0.2s | WAV | Air cut sound | P1 |
| Sword Hit | 0.15s | WAV | Metal impact | P1 |
| Projectile Fire | 0.2s | WAV | Launch sound | P1 |
| Projectile Hit | 0.15s | WAV | Impact sound | P1 |
| Fire Hit | 0.3s | WAV | Flame burst | P1 |
| Frost Hit | 0.3s | WAV | Ice crystallize | P1 |
| Lightning Hit | 0.3s | WAV | Electric crackle | P1 |
| Enemy Death | 0.4s | WAV | Death sound | P1 |
| Boss Death | 1.0s | WAV | Large explosion | P2 |
| Player Hit | 0.2s | WAV | Pain grunt + impact | P1 |
| Player Death | 0.8s | WAV | Death sound | P1 |
| Level Up | 0.6s | WAV | Triumphant chime | P1 |
| Health Pickup | 0.2s | WAV | Healing chime | P1 |
| Mana Pickup | 0.2s | WAV | Magic shimmer | P1 |
| Money Pickup | 0.15s | WAV | Coin clink | P1 |
| XP Pickup | 0.15s | WAV | Soft chime | P1 |
| Key Pickup | 0.3s | WAV | Key jingle | P1 |
| Door Open | 0.4s | WAV | Door creak | P1 |
| Door Locked | 0.2s | WAV | Locked clunk | P1 |
| Portal Enter | 0.5s | WAV | Swirling sound | P2 |
| Inventory Open | 0.2s | WAV | Panel slide | P1 |
| Inventory Close | 0.2s | WAV | Panel close | P1 |
| Item Equip | 0.2s | WAV | Gear equip sound | P1 |
| Item Unequip | 0.2s | WAV | Gear remove sound | P1 |
| Skill Point Spend | 0.3s | WAV | Skill unlock chime | P2 |
| Skill Cooldown Ready | 0.1s | WAV | Ready ping | P1 |
| Stun Applied | 0.3s | WAV | Stun sound | P2 |
| Burn Applied | 0.4s | WAV | Fire ignition | P2 |
| Frostbite Applied | 0.3s | WAV | Ice crackle | P2 |
| Shock Applied | 0.3s | WAV | Electric zap | P2 |
| NPC Dialog Start | 0.2s | WAV | Dialog open | P1 |
| NPC Dialog End | 0.2s | WAV | Dialog close | P1 |
| Buy/Sell | 0.2s | WAV | Coin transaction | P2 |
| Enchant Success | 0.5s | WAV | Magic success | P2 |
| Identify Success | 0.4s | WAV | Reveal sound | P2 |
| Respec Confirm | 0.5s | WAV | Reset sound | P2 |
| Save Game | 0.3s | WAV | Save chime | P2 |
| Menu Navigate | 0.05s | WAV | UI blip | P1 |
| Menu Confirm | 0.1s | WAV | UI confirm | P1 |
| Menu Cancel | 0.1s | WAV | UI cancel | P1 |

**Total: ~42 SFX**

### 9.2 Music Tracks

| Track | Duration | Format | Loop? | Description | Priority |
|-------|----------|--------|-------|-------------|----------|
| Title Theme | 30s intro + 60s loop | WAV | Yes (loop) | Melodic, mysterious, chiptune | P2 |
| Hub Theme | 60s loop | WAV | Yes | Warm, ambient, relaxing | P2 |
| Dungeon Theme 1 | 15s intro + 90s loop | WAV | Yes (intro→loop) | Tense, driving, chiptune | P1 |
| Dungeon Theme 2 | 15s intro + 90s loop | WAV | Yes | Variant for tier 2 | P2 |
| Boss Theme | 10s intro + 60s loop | WAV | Yes | Intense, fast, dramatic | P1 |
| Victory Fanfare | 10s | WAV | No | Short victory jingle | P3 |

**Total: 6 music tracks (with intro+loop segments)**

### 9.3 Audio Technical Specs

- Format: WAV (uncompressed for low latency)
- Sample Rate: 44100 Hz
- Bit Depth: 16-bit
- Channels: Mono for SFX, Stereo for music
- Music has intro + loop segments (seamless transition)
- Beat count metadata for music synchronization (if needed for rhythm-based effects)

---

## 10. SHADER SPECIFICATIONS

### 10.1 CRT Post-Processing Shader

```
Type: Screen-space shader on ColorRect
Effects:
  - Scanlines (horizontal dark lines every 2px)
  - Slight curvature (barrel distortion)
  - Chromatic aberration (RGB shift at edges)
  - Vignette (darkened corners)
  
Parameters:
  - scanline_opacity: 0.15 (subtle)
  - curvature_amount: 0.02 (very slight)
  - chromatic_aberration: 0.001
  - vignette_intensity: 0.3
  
Toggle: settings menu → "CRT Filter" on/off
```

### 10.2 Hit Flash Shader

```
Type: Sprite shader
Effect: Brief white flash when entity takes damage
Parameters:
  - flash_intensity: 0→1→0 over 0.15s
  - flash_color: white (player), red (enemy)
```

### 10.3 Rarity Glow Shader

```
Type: Sprite shader (for item icons in inventory)
Effect: Pulsing colored glow around legendary items
Parameters:
  - glow_color: rarity color
  - pulse_speed: 2.0 (pulses per second)
  - glow_radius: 4px
```

---

## 11. FONT SPECIFICATION

| Use Case | Font | Size | Color | Notes |
|----------|------|------|-------|-------|
| UI Body | Pixel font (e.g., "Pixeloid") | 12px | White | Menus, tooltips, dialog |
| UI Header | Pixel font (bold) | 16px | Yellow | Section titles |
| Damage Numbers | Pixel font | 10-14px | White/Yellow/Red | Floating combat text |
| HUD Numbers | Pixel font | 10px | White | Health, mana, gold |
| Boss Name | Pixel font | 18px | Red | Boss health bar |
| Dialog Text | Pixel font | 12px | White | NPC dialog |
| Item Names | Pixel font | 10px | Rarity color | Tooltips |

**Font:** Use a free pixel font like "Pixeloid Sans" or "Press Start 2P" (for headers).

---

## 12. ASSET PRIORITY SUMMARY

### P1 — MVP (Phase 0-2, Days 1-12)
Everything needed for a playable vertical slice with combat + loot:

- ✅ 3 character classes (static sprites done)
- ✅ 6 enemies (static sprites done)
- ✅ 4 items (done)
- ✅ 2 equipment (done)
- ✅ 2 NPCs (done)
- ❌ Character animation spritesheets (idle, walk, attack, dash) — **CRITICAL**
- ❌ 4 Glob sprites (health, mana, money, XP)
- ❌ 3 Tilesets (hub, tutorial, stone dungeon) — 40 tiles total
- ❌ 8 Combat VFX (hit sparks for each element + death + dash + crit)
- ❌ 18 SFX (core combat sounds)
- ❌ 2 Music tracks (dungeon + boss)
- ❌ HUD elements (health bar, mana bar, skill icons, gold counter)
- ❌ Inventory/equipment UI panels
- ❌ CRT shader

### P2 — Full Game (Phase 3-4, Days 13-35)
Everything needed for the complete game:

- ❌ 6 additional character classes
- ❌ Character portraits (dialog)
- ❌ Additional enemies (skeleton mage, slime, golem)
- ❌ Cave + Overgrown tilesets — 28 tiles
- ❌ 18 more VFX (elemental effects, pickups, portal)
- ❌ 24 more SFX (status effects, UI, services)
- ❌ 4 more music tracks (title, hub, tier 2, victory)
- ❌ Skill tree UI elements
- ❌ Merchant/Stash/Settings panels
- ❌ Boss health bar
- ❌ Instruction Man NPC

### P3 — Polish & Expansion (Post-launch)
Content expansion and visual polish:

- ❌ Desert tileset
- ❌ Dragon endgame boss
- ❌ Lich mini-boss + more enemy types
- ❌ Advanced VFX (blizzard, berserk aura, ethereal shield)
- ❌ Minimap
- ❌ Additional music variants
- ❌ More equipment variety

---

## 13. TOTAL ASSET COUNT

| Category | Done | Needed (P1) | Needed (P2) | Needed (P3) | Total |
|----------|------|-------------|-------------|-------------|-------|
| Characters (static) | 3 | 0 | 6 | 0 | 9 |
| Character Animations | 0 | 244×3 | 244×6 | 0 | 2,196 |
| Character Portraits | 0 | 0 | 5 | 0 | 5 |
| Enemies (static) | 6 | 0 | 3 | 5 | 14 |
| Enemy Animations | 0 | 20×6 | 20×3 | 20×5 | 280 |
| Items/Pickups | 4 | 4 | 0 | 0 | 8 |
| Equipment | 2 | 4 | 16 | 0 | 22 |
| NPCs | 2 | 1 | 0 | 0 | 3 |
| Tilesets (tiles) | 0 | 40 | 28 | 12 | 80 |
| VFX Sprites | 0 | 8 | 18 | 8 | 34 |
| UI Elements | 0 | 20 | 25 | 5 | 50 |
| SFX | 0 | 18 | 24 | 0 | 42 |
| Music Tracks | 0 | 2 | 4 | 0 | 6 |
| Shaders | 0 | 1 | 2 | 0 | 3 |

**Grand Total: ~2,750 individual assets** (dominated by character animation frames)