# 🎮 v1.0.00 "wizdung" — START HERE: Build Guide

> **Role:** You are the Game Architect + Creative Director for a new action RPG dungeon crawler.
> **Goal:** Build a game inspired by wizdung from scratch, bottom-up.

---

## 1. ELEVATOR PITCH

**"Hades meets Diablo, but pixel-art, top-down, and every dungeon run lets you swap between three wizards with completely different skill trees."**

A top-down, 8-directional action RPG where you delve into procedurally-arranged dungeon rooms, fight enemies with elemental combat, collect loot across 5 rarity tiers, and build your character through a deep skill tree. Return to the hub to identify gear, enchant items, respec your tree, and switch between three distinct wizard classes.

---

## 2. DESIGN PEG

### Visual Style
- **Reference:** Retro pixel-art ARPG (think Realm of the Mad God × Diablo II × Stardew Valley dungeon sections)
- **Palette:** Dark dungeon backgrounds, vibrant elemental effects (orange fire, blue frost, purple lightning)
- **Characters:** 8-directional spritesheets with DashAttack animations per direction
- **UI:** Dark fantasy panels with colored rarity frames (grey/blue/yellow/purple/orange)
- **Shader:** CRT scanline overlay for retro feel

### Game Feel
- **Pacing:** Fast-paced combat — dash, attack, dash, attack. Rooms take 10-30 seconds.
- **Juice:** Screen shake on crit, hit pause on boss death, ghost trail on dash, exploding enemies on kill, particle bursts on every pickup
- **Audio:** Chiptune music with intro + loop, satisfying "crunch" on hits, weighty explosion sounds

### Tone
- **Emotional arc:** Tension (enter room) → Action (fight) → Relief (clear room) → Greed (see loot) → Decision (hub: identify or sell?)
- **Themes:** Power through gear, build variety, risk-reward dungeon diving
- **Vibe:** "One more room, one more item, one more level"

### Design North Star
> **Every room should feel like a micro-arena: fight, loot, decide.**

If a room doesn't have combat, loot, and a decision — cut it.

---

## 3. CORE LOOP

```
┌──────────────────────────────────────────────────────┐
│                  DUNGEON RUN                           │
│                                                       │
│  Hub → Enter Portal → Room 1 → Fight → Loot          │
│    ↓                                                  │
│  Room 2 → Fight → Loot → Key? → Open Door             │
│    ↓                                                  │
│  Room 3 → Harder Enemies → Better Loot               │
│    ↓                                                  │
│  Boss Room → Fight Boss → Big Loot                    │
│    ↓                                                  │
│  Return to Hub → Identify → Equip/Sell/Enchant        │
│    ↓                                                  │
│  Stash → Switch Character → Enter Portal (stronger)  │
└──────────────────────────────────────────────────────┘
```

**10-second loop:** Enter room → Kill enemies → Pick up globs
**30-second loop:** Clear room → Pick up loot → Open door → Next room
**5-minute loop:** Complete a dungeon section → Fight boss → Return to hub
**30-minute loop:** Identify all gear → Enchant best items → Respec skill tree → Switch class → Next run

---

## 4. BOTTOM-UP ARCHITECTURE

### Layer 0: Engine Foundation
```
Godot 4.x Project
├── Core/
│   ├── GameManager (singleton, game state)
│   ├── SceneManager (room transitions, hub/dungeon)
│   ├── SaveSystem (player progress, stash, settings)
│   ├── InputManager (keyboard + controller, 8-directional)
│   ├── EventBus (decoupled signals: on_hit, on_kill, on_pickup)
│   └── ObjectPool (projectiles, globs, VFX, enemies)
├── Data/
│   ├── stats.json (40+ stat definitions)
│   ├── items.json (all item definitions per slot/type)
│   ├── skills.json (skill tree nodes, behaviors)
│   ├── enemies.json (enemy types, scalars, AI)
│   ├── levels.json (room sets, tilemaps, spawn points)
│   └── curves.json (XP, money, enemy scaling, item scaling)
└── AutoLoad/ (Godot autoload singletons)
```

**Build first:**
- [ ] Godot 4.x project with pixel-art settings (snap to pixel, no texture filtering)
- [ ] 8-directional movement (input vector → velocity → move_and_slide)
- [ ] Camera follows player, clamped to room bounds
- [ ] Scene transition system (hub ↔ dungeon rooms)
- [ ] Object pool for projectiles
- [ ] Save system (JSON: player stats, inventory, stash, skill tree)

### Layer 1: Character + Combat
```
Character/
├── PlayerCharacter (CharacterBody, 8-dir movement)
├── StateMachine (Idle, Walk, Attack, Death, Stunned)
├── StatsComponent (40+ stats, derived calculations)
├── EquipmentManager (6 slots: weapon, chest, helmet, boots, ring, necklace)
├── SkillManager (equipped skills, cooldowns, mana costs)
├── InventoryManager (inventory slots, pickup, drop)
├── AimingReticle (mouse/gamepad direction)
└── AnimationPlayer (8-dir spritesheet playback)

Combat/
├── HitboxSystem (melee + projectile hit detection)
├── DamageCalculator (type, crit, resistance, penetration)
├── StatusEffectSystem (burn, frostbite, shock, stun, freeze)
├── ProjectileSystem (spawn, move, pierce, on-hit behaviors)
├── BehaviorSystem (modular skill behaviors)
└── CombatFeedback (damage numbers, crit indicator, screen shake)
```

**Build second:**
- [ ] Player can move in 8 directions with keyboard + controller
- [ ] Basic attack (melee hitbox or projectile) in facing direction
- [ ] Dash with i-frames (brief invincibility)
- [ ] 1 enemy that chases and attacks
- [ ] Health system (take damage, die)
- [ ] Mana system (skills cost mana)
- [ ] Damage calculation (physical damage vs. toughness)
- [ ] Status effects: apply burn on fire hit, shock on lightning hit

### Layer 2: Stats + Items + Skills
```
Stats/
├── StatDefinitions (40+ stats with descriptions)
├── StatCurves (per-level scaling: health, mana, power, etc.)
├── DerivedStats (dodge from dexterity, health from power, etc.)
├── StatModifiers (temporary buffs/debuffs from skills/items)
└── StatUI (character sheet, tooltips, compare)

Items/
├── ItemDefinitions (per slot, per type, per class)
├── ItemInstances (id, rarity, stats, modifiers, identified flag)
├── ItemStatMods (12+ modifier sets with value ranges)
├── ItemCurves (base_stat, core_stat, regen, room scaling)
├── RaritySystem (Common → Magic → Rare → Epic → Legendary)
├── LootTable (drop chances: gear, key, glob, money)
├── LootCurves (money_curve, xp_curve, number_of_drops)
└── GlobPickups (health, mana, currency, XP — with VFX)

Skills/
├── SkillTree (4 sub-trees per class, 9 nodes each = 36 nodes)
├── SkillBehaviors (26+ modular behaviors: projectile, AOE, dash, etc.)
├── SkillModifiers (global + per-skill-type modifiers)
├── SkillDefinitions (13 skills: basic attacks, specials, movement)
├── SkillPoints (earn on level, spend on nodes, refund on respec)
└── SkillTreeUI (node tree visualization, tooltips, point spending)
```

**Build third:**
- [ ] Full stat system (all 40+ stats, derived calculations)
- [ ] Items drop from enemies (loot table with chances)
- [ ] Items can be picked up, equipped, unequipped
- [ ] Equipment changes stats (weapon adds damage, armor adds defense)
- [ ] 5 rarity tiers with colored frames
- [ ] Unidentified items (need NPC to identify)
- [ ] Skill tree UI with nodes (start with 9 nodes, expand to 36)
- [ ] Skill points spent on nodes, modifying skill behavior
- [ ] Glob pickups (health, mana, money, XP) with VFX

### Layer 3: Enemies + Dungeon + Progression
```
Enemies/
├── EnemyBase (AI controller, state machine, aggro radius)
├── EnemyTypes (Melee Skeleton, Wizard Mimic, Boss)
├── EnemyScalars (7 scalars: life, damage, toughness, dodge, elite variants)
├── EnemyRank (normal, elite, boss)
├── EnemySkills (skeleton basic, mimic arcane bolt, boss basic)
└── EnemySpawner (spawn points, pack size, rarity chance)

Dungeon/
├── RoomSetSystem (room templates per tier: tutorial, T1, T2, endgame)
├── RoomGenerator (pick room from set, populate enemies, loot, doors)
├── TilemapSystem (multiple tilesets: base, cave, overgrown, desert)
├── DoorSystem (locked doors, key requirements, transitions)
├── PortalSystem (enter dungeon, return to hub)
├── RoomLevelScaling (enemy level = room level)
├── SpawnCurves (pack_size, rarity chance per room level)
└── BossRoom (boss encounter, boss health bar)

Progression/
├── XPSytem (XP from kills, level up, skill points)
├── XPCurves (xp required per level, level-up curve)
├── StashSystem (store items in hub, share between classes)
├── CharacterSwitch (talk to NPC to swap class)
└── SaveSystem (save stash, skill tree, character level)
```

**Build fourth:**
- [ ] 3 enemy types (skeleton melee, mimic ranged, boss)
- [ ] Enemy AI (chase, attack, aggro radius, group aggro)
- [ ] Enemy scaling (stats scale with room level)
- [ ] Elite enemy variants (higher stats, different color)
- [ ] Room generation (pick from room set, populate)
- [ ] 2+ tilesets (base dungeon, alternate)
- [ ] Door system (some require keys)
- [ ] Key drops from enemies
- [ ] Portal to hub
- [ ] Boss room with boss health bar
- [ ] XP and leveling
- [ ] Stash in hub
- [ ] Character switch (talk to NPC)

### Layer 4: NPC + UI + Polish
```
NPC/
├── MysteriousWizard (identify items, respec — costs gold)
├── TrinketWitch (enchant items, sell items)
├── CharacterNPCs (Dex/Int/Str wizard — switch class)
├── InstructionMan (tutorial NPC)
├── DialogSystem (profiles, sets, conditions, responses)
└── ServicesUI (identify screen, enchant screen, respec screen)

UI/
├── MainMenu (start, character select, settings)
├── PlayerHUD (health, mana, skills, minimap?)
├── BossHealthBar (boss name + health)
├── EnemyHealthBar (floating, above enemy)
├── InventoryUI (grid, equipment slots, tooltips, compare)
├── SkillTreeUI (per-class tree, node interaction)
├── CharacterSheet (stats display)
├── DialogBox (NPC dialog, response choices)
├── MerchantScreen (buy/sell/enchant UI)
├── StashUI (stash storage)
├── PauseMenu (resume, settings, save, quit)
├── SaveScreen (save slots)
├── RoomInfo (current room level, enemies remaining)
├── KeyUI (key icons for doors)
├── CombatFeedback (crit indicator, damage numbers)
├── CRTShader (retro post-processing)
└── SettingsMenu (keyboard + controller config)

VFX/
├── 20+ VFX scenes (explosion, freeze, lightning, ghost trail, etc.)
├── VFXManager (spawn, pool, cleanup)
└── ParticleSystem (hit sparks, pickup effects)

Audio/
├── AudioManager (play SFX, music, 2D positional)
├── 18 SFX (dash, hit, death, pickup, level up, etc.)
├── 3 music tracks (title, level intro, level loop)
└── AudioResources (metadata: beat count, loop points)
```

**Build last:**
- [ ] Mysterious Wizard NPC (identify + respec services)
- [ ] Trinket Witch NPC (enchant + sell services)
- [ ] Character switch NPCs in hub
- [ ] Full dialog system with conditions
- [ ] All UI panels (main menu, HUD, inventory, skill tree, etc.)
- [ ] 20+ VFX scenes
- [ ] 18 SFX + 3 music tracks
- [ ] CRT shader
- [ ] Controller support
- [ ] Tutorial NPC

---

## 5. BUILD ORDER (Priority Sequence)

| Priority | What | Why | Time |
|----------|------|-----|------|
| 1 | Godot project + 8-dir movement | Foundation | 1 day |
| 2 | Dash with i-frames | Game feel | 1 day |
| 3 | Basic attack (projectile or melee) | Combat prototype | 1 day |
| 4 | 1 enemy with AI | Combat partner | 2 days |
| 5 | Health + mana + death | Survival mechanics | 1 day |
| 6 | Stats system (10 core stats) | RPG foundation | 2 days |
| 7 | Item drops + pickup | Rewards | 1 day |
| 8 | Equipment + inventory | Character progression | 2 days |
| 9 | Rarity tiers + item modifiers | Loot excitement | 2 days |
| 10 | Skill tree (9 nodes, 1 sub-tree) | Build variety | 3 days |
| 11 | Room generation + doors | Dungeon structure | 2 days |
| 12 | Enemy scaling + room level | Difficulty curve | 1 day |
| 13 | Glob pickups (HP/mana/money/XP) | Combat sustain | 1 day |
| 14 | Hub area + portal | Safe zone | 1 day |
| 15 | NPC: identify + enchant + respec | Service economy | 2 days |
| 16 | 3 classes + character switch | Replay variety | 3 days |
| 17 | Full skill tree (36 nodes/class) | Deep builds | 5 days |
| 18 | Boss enemy + boss health bar | Climax | 2 days |
| 19 | Stash system | Persistence | 1 day |
| 20 | VFX + audio + polish | Ship quality | 5 days |

**Total: ~35 days for a full vertical slice with all systems.**

---

## 6. PHASE BREAKDOWN

### Phase 0: Foundation (Days 1-2)
**Milestone:** Character moves in 8 directions, can dash, camera follows.

- [ ] Godot 4.x project (pixel-perfect, snap-to-pixel, no texture filtering)
- [ ] CharacterBody2D with 8-directional movement
- [ ] Input: WASD + gamepad left stick (normalized vector)
- [ ] Dash ability (speed burst + i-frames for 0.3s)
- [ ] Camera2D follows player, clamped to room
- [ ] Simple tilemap room with walls (collision)
- [ ] Ghost trail VFX on dash
- [ ] Aiming reticle (mouse or right stick)

**Playtest:** Does movement feel good? Is dashing satisfying? Can you aim?

### Phase 1: Core Combat (Days 3-6)
**Milestone:** Fight an enemy, deal damage, take damage, die, respawn.

- [ ] Basic attack (projectile for Dex Wizard, hitbox for Str Wizard)
- [ ] Attack in facing direction (8 directions)
- [ ] 1 enemy (Melee Skeleton) with simple AI (chase + attack)
- [ ] Enemy state machine (Idle → Walk → Attack → Death)
- [ ] Health system (player + enemy have health)
- [ ] Damage calculation (base damage - toughness reduction)
- [ ] Death + respawn (or return to hub)
- [ ] Hit VFX (spark on hit)
- [ ] Hit SFX (sword/hit sound)
- [ ] Mana system (attack costs mana, mana regenerates)
- [ ] Crit system (random crit, multiplier, visual feedback)

**Playtest:** Is combat fun? Do hits feel weighty? Is there risk-reward?

### Phase 2: Stats + Loot + Items (Days 7-12)
**Milestone:** Kill enemies → get loot → equip items → get stronger.

- [ ] Full stat system (start with 15 core stats, expand later)
- [ ] Derived stats (Power → Max Health, Wisdom → Max Mana + Ethereal Shield)
- [ ] Loot table (chance to drop gear, key, glob, money)
- [ ] Item drops (interactable on ground, pickup with prompt)
- [ ] Inventory system (grid, slots, stack limits)
- [ ] Equipment system (6 slots: weapon, chest, helmet, boots, ring, necklace)
- [ ] Item stat modifiers (random modifiers within rarity-based ranges)
- [ ] 5 rarity tiers (Common grey → Magic blue → Rare yellow → Epic purple → Legendary orange)
- [ ] Item tooltips (show all stats, compare with equipped)
- [ ] Glob pickups: health glob, mana glob, money glob, XP glob (with VFX + sound)
- [ ] XP system (gain XP from kills, level up, earn skill points)
- [ ] "Your Inventory is Full" message

**Playtest:** Do you want to kill more enemies for loot? Is equipping items satisfying?

### Phase 3: Skill Tree + Dungeon (Days 13-20)
**Milestone:** Spend skill points on a tree, navigate rooms, fight varied enemies.

- [ ] Skill tree UI (node-based, per class)
- [ ] Start with 9 nodes in 1 sub-tree (e.g., Agility BasicAttack)
- [ ] Skill points: earn on level, spend on nodes
- [ ] Skill behaviors modify attacks (e.g., "Projectile" makes melee ranged)
- [ ] Room set system (list of room templates per tier)
- [ ] Room generation (pick room, populate with enemies + loot + doors)
- [ ] Door system (open door → transition to next room)
- [ ] Key system (some doors need keys, keys drop from enemies)
- [ ] 3 enemy types (skeleton melee, mimic ranged, boss)
- [ ] Enemy scaling (enemy stats scale with room level)
- [ ] Elite enemies (higher stats, visual indicator)
- [ ] Boss room (boss has boss health bar UI)
- [ ] 2+ tilesets (base dungeon + alternate)
- [ ] Portal system (enter dungeon from hub, return to hub)

**Playtest:** Does the skill tree feel meaningful? Are rooms varied? Is the boss exciting?

### Phase 4: Hub + NPCs + Polish (Days 21-35)
**Milestone:** Full game loop — hub services, 3 classes, all VFX/audio, ship quality.

- [ ] Hub area (safe zone, NPCs, stash, portals)
- [ ] Mysterious Wizard NPC (identify items, respec)
- [ ] Trinket Witch NPC (enchant items, sell items)
- [ ] Dialog system (profiles, sets, conditions, response types)
- [ ] Character switch NPCs (talk to swap class)
- [ ] Stash system (store items, share between classes)
- [ ] 3 playable classes (Dex/Int/Str Wizard) with unique skill trees
- [ ] Full skill trees (36 nodes per class, 4 sub-trees × 9 nodes)
- [ ] 26+ skill behaviors (projectile, AOE, dash, channel, etc.)
- [ ] Status effects: burn (fire), frostbite (frost), shock (lightning), stun (physical), freeze
- [ ] 4 damage types: physical, fire, frost, lightning
- [ ] Damage conversion (physical → lightning, dexterity → physical)
- [ ] 20+ VFX scenes
- [ ] 18 SFX + 3 music tracks
- [ ] CRT shader post-processing
- [ ] Controller support (full button mapping)
- [ ] Main menu + character select
- [ ] Pause menu + settings + save screen
- [ ] All UI panels (HUD, inventory, skill tree, character sheet, dialog, merchant, stash)
- [ | Tutorial NPC (instruction man)
- [ ] Room info display (room level, enemies)

**Playtest:** Can a stranger play it in 5 minutes? Would they play for 30? Does each class feel different?

---

## 7. DESIGN PEG BOARD

```
┌─────────────────────────────────────────────────────┐
│               WIZDUNG DESIGN PEG                      │
│                                                      │
│  PITCH: Hades meets Diablo, but pixel-art and you    │
│         can swap between three wizards mid-run.      │
│                                                      │
│  FEEL:  Fast, punchy, greedy                          │
│         Every room is a micro-arena. Every hit has    │
│         weight. Every drop makes you want more.      │
│                                                      │
│  LOOK:  Dark dungeons, bright elemental effects      │
│         8-directional pixel sprites, CRT scanlines    │
│         Rarity colors: grey/blue/yellow/purple/orange│
│                                                      │
│  SOUND: Chiptune music, crunchy hit SFX              │
│         Dash whoosh, explosion boom, coin pickup     │
│                                                      │
│  LOOP:  Hub → Portal → Room → Fight → Loot → Hub     │
│                                                      │
│  HOOK:  "I found a LEGENDARY item and my build        │
│         completely changed."                         │
│                                                      │
│  CUT IF: It doesn't serve combat, loot, or builds.   │
│          If a room doesn't have fighting and rewards,│
│          cut it.                                     │
└─────────────────────────────────────────────────────┘
```

---

## 8. CRITICAL DESIGN DECISIONS

### Decision 1: Combat Perspective
**Question:** Top-down 8-directional or isometric?
- **8-directional:** Simpler, more responsive, easier to build, matches source
- **Isometric:** More cinematic, harder to build, harder to read

**Recommendation:** 8-directional. It's what the source game uses and it feels great for fast combat.

### Decision 2: Skill Tree Scope
**Question:** How many nodes per class?
- **9 nodes (1 sub-tree):** Prototype, test the system
- **36 nodes (4 sub-trees):** Full game, meaningful builds
- **72+ nodes (8 sub-trees):** Very deep, hard to balance

**Recommendation:** Start with 9 (Phase 3), expand to 36 (Phase 4). Don't build all 36 at once.

### Decision 3: Character Switch Depth
**Question:** When can you switch classes?
- **Hub only:** Strategic, deliberate. You commit to a class per run.
- **Mid-dungeon:** Tactical, flexible. You adapt to situations.
- **NPC offer only:** Narrative-driven. NPCs "take over" when you're tired.

**Recommendation:** Hub only for first build. Add NPC mid-dungeon switch later (matches source game's dialog: "Can you take over?").

### Decision 4: Loot Identification
**Question:** Should items be unidentified when they drop?
- **No:** All items show stats immediately. Simpler, less friction.
- **Yes:** Items show rarity but not stats. Must visit NPC. Adds hub purpose.

**Recommendation:** Yes. It gives the hub meaning and creates an economy sink. But make identification cheap or free early game.

### Decision 5: Death Penalty
**Question:** What happens when you die in the dungeon?
- **Lose everything:** Hardcore, high stakes, can frustrate
- **Lose current run progress, keep gear:** Moderate, standard ARPG
- **Lose nothing, just return to hub:** Too forgiving, no tension

**Recommendation:** Lose current room level progress (as source says: "Non-permanent room level progress will be lost"), but keep all gear and XP. This creates tension without punishment.

---

## 9. THE THREE CLASSES — BUILD SHEETS

### Dex Wizard (Agility) — "The Speed Demon"

```
ARCHETYPE: Fast, mobile, projectile-based
PRIMARY DAMAGE: Lightning + Physical
MOBILITY: Dash-based (dash leaves shocking ground)
PLAYSTYLE: Hit-and-run, kite enemies, shock-chain groups

SKILL TREE FOCUS:
├── BasicAttack: Projectile + DoubleStrike + CullingThunder + ExplodeOnKill
├── Movement: DashDistance + Intangible + ShockingPath + MomentumDamage
├── Passive: LightningDamage + ShockChance + ShockTwice + DodgeChance
└── SpecialAttack: MultipleProjectiles + ForkingShuriken + StormShurikens

KEY STATS: Dexterity, Lightning Damage, Dodge, Attack Speed, Crit Chance
WEAPON TYPE: Agility Weapon (fast, low damage, multi-hit)
ARMOR TYPE: Cloth (low defense, high dodge/mana)
ACCESSORY: Emerald (Dexterity bonuses)

BUILD VARIANTS:
- "Gatling Gun": Max projectiles + attack speed + pierce
- "Dash Master": Max dash distance + shocking path + momentum damage
- "Crit Fisher": Max dodge + crit on dodge + culling thunder
```

### Int Wizard (Wisdom) — "The Area Controller"

```
ARCHETYPE: Control, area denial, burst damage
PRIMARY DAMAGE: Frost
MOBILITY: Teleport/Blink (explode at departure + arrival)
PLAYSTYLE: Control crowds with frostbite, burst with icey shards, teleport to safety

SKILL TREE FOCUS:
├── BasicAttack: CircleOfCold + FrostbiteChance + FrostbiteDuration + ExplodeDeath
├── Movement: ExplodeOnTeleport + ExplodeOnTeleportLand + IncreasedArea + ManaRegen
├── Passive: FrostDamage + IncreasedFrostDamage + InsightDamage
└── SpecialAttack: IncreasedShards + IceyShardExplosion + IceOnDeath + ChanneledIce

KEY STATS: Wisdom, Frost Damage, Max Mana, Ethereal Shield, Cast Speed
WEAPON TYPE: Wisdom Weapon (slow, high damage, AoE)
ARMOR TYPE: Cloth (low defense, high mana/ethereal shield)
ACCESSORY: Sapphire (Wisdom bonuses)

SPECIAL MECHANIC: Ethereal Shield (mana-based damage absorption)

BUILD VARIANTS:
- "Bomb Wizard": Max teleport explosion + area + ice on death
- "Ice Mage": Max frostbite duration + frost damage + channeled ice
- "Battle Mage": Max insight + basic attack scaling + circle of cold
```

### Str Wizard (Power) — "The Tank"

```
ARCHETYPE: Slow, tanky, high melee damage
PRIMARY DAMAGE: Physical
MOBILITY: Walk (no dash, high movement speed)
PLAYSTYLE: Face-tank enemies, high health, stun on hit, melee combat

SKILL TREE FOCUS:
├── (Skill tree data incomplete in source — design your own!)
├── BasicAttack: Heavy strike, stun chance, knockback
├── Movement: Movement speed, charge attack
├── Passive: Max health, toughness, stun duration
└── SpecialAttack: Ground slam, AOE stun, damage multiplier

KEY STATS: Power, Max Health, Toughness, Physical Damage, Stun Chance
WEAPON TYPE: Power Weapon (slow, very high damage, melee)
ARMOR TYPE: Plate (high defense, low mobility)
ACCESSORY: Ruby (Power bonuses)

BUILD VARIANTS:
- "Juggernaut": Max health + toughness + stun resistance
- "Earthquake": Max AOE + stun + physical damage
- "Berserker": Max damage + attack speed + life leech

NOTE: The source game's Str Wizard skill tree was incomplete in extracted data.
This is your opportunity to design it yourself. Use the same 4-sub-tree × 9-node structure.
```

---

## 10. TECH STACK

| Component | Tool |
|-----------|------|
| Engine | Godot 4.x |
| Language | GDScript |
| Data format | JSON for content data, .tres for Godot resources |
| Tilemap | Godot TileMapLayer (4.x) |
| Animation | AnimationPlayer + AnimationTree for state machine |
| UI | Godot Control nodes + custom Theme |
| Shaders | Godot Shader (canvas_item for CRT, post-process) |
| Audio | AudioStreamPlayer (2D for SFX, bus for music) |
| Input | InputMap (keyboard + gamepad) |
| Save | JSON file or Godot ConfigFile |
| Version control | Git |
| Pixel art | Aseprite (or PixelLab for AI-generated) |

---

## 11. ASSET CHECKLIST

### Minimum Viable Assets (Phase 0-1)
- [ ] Player spritesheet (8-dir walk, idle, attack, dash, death) — 1 class
- [ ] 1 enemy spritesheet (walk, attack, death)
- [ ] 1 tileset (dungeon walls + floor)
- [ ] 1 projectile sprite
- [ ] Health/mana bar UI
- [ ] 1 VFX (hit spark)
- [ ] 3 SFX (attack, hit, dash)
- [ ] 1 music track

### Phase 2 Assets
- [ ] 10+ item icons (weapon, 3 armor types, ring, necklace, key)
- [ ] 5 rarity frames (grey, blue, yellow, purple, orange)
- [ ] Unidentified item icon
- [ ] 4 glob sprites (health, mana, money, XP)
- [ ] 4 glob VFX (pickup effects)
- [ ] Inventory + equipment UI
- [ ] Item tooltip UI
- [ ] Level-up VFX + SFX

### Full Game Assets (Phase 3-4)
- [ ] 3 class spritesheets (Dex/Int/Str Wizard, 8-dir each)
- [ ] 3+ enemy spritesheets (skeleton, mimic, boss)
- [ ] 4+ tilesets (base, cave, overgrown, desert)
- [ ] 50+ item icons
- [ ] 5 rarity frames + unidentified
- [ ] Skill tree UI + 36 skill icons per class
- [ ] 20+ VFX sprites/animations
- [ ] 18 SFX + 3 music tracks
- [ ] NPC sprites + portraits (Mysterious Wizard, Trinket Witch, 3 class NPCs)
- [ ] Hub area tileset
- [ ] Door + portal sprites
- [ ] Key sprites (rusty, room, rune keys)
- [ ] Boss health bar UI
- [ | CRT shader
- [ ] Custom cursor
- [ ] Main menu art
- [ ] All UI panels (inventory, skill tree, character sheet, dialog, merchant, stash, pause, save, settings)

---

## 12. THE 5-MINUTE TEST

```
Minute 0-1: Title → New Game → Choose class (Dex/Int/Str Wizard)
Minute 1-2: Spawn in hub → Tutorial NPC explains controls → Enter portal
Minute 2-3: First room → Kill 2 enemies → Pick up health glob → Open door
Minute 3-4: Second room → Kill enemies → Get item drop → Equip it → Feel stronger
Minute 4-5: Level up → Skill point → Open skill tree → Spend point → "I want more"
```

If the first 5 minutes aren't fun, nothing else matters. **Playtest the 5-minute test with 5 strangers.**

---

## 13. COMMON PITFALLS

| Pitfall | Fix |
|---------|-----|
| Movement feels bad | Add coyote time, dash i-frames, ghost trail, screen shake |
| Combat feels floaty | Add hit pause (0.05s freeze on hit), screen shake, knockback |
| Loot is boring | Make rarity visible (color frames), add unidentified mystery |
| Skill tree is overwhelming | Start with 9 nodes, unlock more as player levels |
| Stats are too complex | Show derived stats in UI, hide the math |
| Rooms feel empty | Add varied enemy spawns, loot, door/key choices |
| Boss is a damage sponge | Add phases, telegraphed attacks, boss health bar |
| Inventory fills too fast | Auto-pickup globs, manual-pickup gear, "inventory full" message |
| Death feels unfair | Show what killed you, allow hub return, keep gear |
| respec feels wasteful | Make respec cheap, show before/after preview |

---

## 14. FILE STRUCTURE TEMPLATE

```
project/
├── scenes/
│   ├── Core/          (GameManager, SceneManager, SaveManager)
│   ├── Player/       (PlayerCharacter, StateMachine, AimingReticle)
│   ├── Enemies/      (Skeleton, Mimic, Boss, AIController)
│   ├── Dungeon/      (RoomGenerator, Door, Portal, Tilemaps)
│   ├── Hub/          (Hub map, NPCs, Stash, Portals)
│   ├── UI/           (HUD, Inventory, SkillTree, Dialog, Menus)
│   ├── VFX/          (20+ VFX scenes)
│   └── Items/        (ItemPickup, GlobPickups)
├── scripts/
│   ├── Core/         (GameManager, InputManager, ObjectPool, EventBus)
│   ├── Character/    (Stats, Equipment, Inventory, Skills, StateMachine)
│   ├── Combat/       (DamageCalc, Hitbox, Projectile, StatusEffects, Behaviors)
│   ├── Dungeon/      (RoomSet, RoomGenerator, DoorSystem, SpawnSystem)
│   ├── NPC/          (DialogSystem, Services, CharacterSwitch)
│   └── UI/           (HUDController, InventoryUI, SkillTreeUI, etc.)
├── data/
│   ├── stats.json
│   ├── items.json
│   ├── skills.json
│   ├── enemies.json
│   ├── levels.json
│   └── curves.json
├── assets/
│   ├── sprites/
│   ├── audio/
│   ├── shaders/
│   ├── ui/
│   └── fonts/
├── shaders/
│   ├── crt_shader.gdshader
│   └── enemy_outline_shader.gdshader
└── project.godot
```

---

## 15. KEY FORMULAS REFERENCE

```
# Damage Calculation
base_damage = skill_base × stat_multiplier
crit_damage = base_damage × crit_multiplier (if crit hits)
mitigated = crit_damage × (1 - resistance) × (1 - toughness_reduction)
final_damage = max(1, mitigated - ethereal_armor)

# Enemy Scaling
enemy_life = base_life × EnemyScalar_Life(room_level) × (is_elite ? elite_life_mult : 1)
enemy_damage = base_damage × EnemyScalar_Damage(room_level) × (is_elite ? elite_damage_mult : 1)

# Loot Drop
if random() < chance_to_drop_gear: drop_gear()
if random() < chance_to_drop_key: drop_key_from(key_list)
if random() < chance_to_drop_glob: drop_glob(money_glob)

# XP
xp_required = XP_Curve(level) × Level_Up_Curve(level)
skill_points = curve_ability_point_distribution(level)

# Item Stats
item_stat = base_value × item_base_stat_scalar(item_level) × rarity_multiplier

# Pet/Equipment Multiplier (for reference)
total_multiplier = sum(equipped_multipliers)  # or product for multiplicative
```

---

## 16. QUICK START CHECKLIST

```
□ Read GAME_MECHANICS.md (full 16-section spec)
□ Read ECONOMY.md (11-section economy doc)
□ Set up Godot 4.x project (pixel-perfect)
□ 8-directional movement + dash + i-frames
□ Basic attack (projectile or hitbox)
□ 1 enemy with AI (chase + attack)
□ Health + mana + death + respawn
□ Damage calculation (damage vs. resistance)
□ Item drops + pickup + equipment
□ 5 rarity tiers with colored frames
□ Skill tree (start with 9 nodes)
□ Room generation + doors + keys
□ Enemy scaling per room level
□ Glob pickups (HP/mana/money/XP)
□ Hub area + portal system
□ NPC: identify + enchant + respec
□ 3 classes + character switch
□ Full skill tree (36 nodes/class)
□ Boss enemy + boss health bar
□ Stash system
□ 20+ VFX + 18 SFX + 3 music tracks
□ CRT shader + controller support
□ Playtest 5-minute test with 5 strangers
□ Ship a demo
```

**Start with Layer 0. Make the character move and dash. Everything else stacks on top.**