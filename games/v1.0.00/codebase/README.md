# v1.0.00 (wizdung) — Godot Codebase Scaffold

This folder contains the complete GDScript scaffold for a top-down ARPG dungeon crawler built in Godot 4.x (GL Compatibility renderer, 640×360 viewport, pixel-perfect).

## Project Setup

1. Copy this entire `codebase/` folder into a new Godot 4.x project
2. Open `project.godot` in Godot Editor
3. Create the following scene files (`.tscn`) — the scripts are ready, just need nodes:
   - `scenes/MainMenu.tscn` → Control + VBoxContainer with buttons (attach `MainMenu.gd`)
   - `scenes/Dungeon.tscn` → Node2D + DungeonGenerator + Player + TileMap + HUD (attach `Dungeon.gd`)
   - `scenes/Hub.tscn` → Node2D + Player + NPCBase instances + HUD (attach `Hub.gd`)
   - `combat/Projectile.tscn` → Area2D + Sprite2D + CollisionShape2D (attach `Projectile.gd`)
   - `combat/VFX.tscn` → Node2D + AnimatedSprite2D (VFX effect node)
   - `items/ItemPickup.tscn` → Area2D + Sprite2D + CollisionShape2D (attach `ItemPickup.gd`)
   - `ui/DamageNumber.tscn` → Label (attach `DamageNumber.gd`)
   - `ui/HUD.tscn` → CanvasLayer with ProgressBar×3, Label×2, HBoxContainer (attach `HUD.gd`)
   - `npc/NPCBase.tscn` → CharacterBody2D + Sprite2D + Area2D + Label (attach `NPCBase.gd`)
   - `enemies/EnemyBase.tscn` → CharacterBody2D + Sprite2D + ProgressBar + CollisionShape2D (attach `EnemyBase.gd`)
4. Create JSON data files in `data/` folder (see `DATA_MODELS.md` for full schemas)
5. Import sprites into `assets/sprites/` (see `ASSET_SPEC.md` for naming conventions)

## Architecture Overview

```
Autoloads (load order matters):
  DataManager  → loads all JSON data at startup
  EventBus     → central signal bus (all cross-system comms)
  SaveSystem   → JSON saves, auto-save on events
  GameManager  → run state, floor tracking, score
  InputManager → global input routing
  SceneManager → scene transitions with fade
  ObjectPool   → projectile/VFX/item pooling
  AudioManager → SFX pool + music crossfade
```

## Folder Structure

```
codebase/
├── project.godot              # Godot project config (autoloads, input map, renderer)
├── core/
│   ├── EventBus.gd            # Central signal bus (40+ signals)
│   ├── DataManager.gd         # JSON data loader + lookup API + XP/leveling
│   ├── GameManager.gd         # Run state machine, score tracking
│   ├── SaveSystem.gd          # JSON saves, auto-save triggers
│   ├── SceneManager.gd        # Scene transitions with fade
│   ├── InputManager.gd        # Global input routing
│   ├── ObjectPool.gd          # Projectile/VFX/item pooling
│   └── AudioManager.gd        # SFX pool + music crossfade
├── character/
│   ├── PlayerCharacter.gd     # Player node: stats, components, skill unlock
│   └── state_machine/
│       ├── State.gd           # Base state class
│       ├── StateMachine.gd    # State manager + transitions
│       ├── IdleState.gd       # Idle → walk/attack/dash/interact
│       ├── WalkState.gd       # 8-directional movement
│       ├── AttackState.gd     # Basic + special attack (fires projectile)
│       ├── DashState.gd       # Dash with i-frames
│       ├── StunnedState.gd   # Status effect stun
│       └── DeathState.gd      # Death animation → game over
├── combat/
│   ├── DamageCalculator.gd    # Full damage formula (crit, toughness, resistance)
│   └── Projectile.gd         # Pooled projectile, enemy hit detection
├── skills/
│   ├── SkillManager.gd        # Skill tree, unlock, activate, cooldowns
│   └── behaviors/
│       ├── SkillBehavior.gd   # Base skill behavior class
│       ├── MeleeStrike.gd     # Basic melee projectile
│       ├── Fireball.gd        # Fire elemental projectile
│       ├── IceNova.gd         # AoE ice damage + slow
│       └── ChainLightning.gd  # Multi-target lightning chain
├── items/
│   ├── LootTable.gd           # Rarity-weighted loot rolling with luck
│   └── ItemPickup.gd          # Ground item with magnet effect, pickup
├── enemies/
│   └── EnemyBase.gd           # Base enemy: AI states, scaling, loot drop, status
├── dungeon/
│   └── DungeonGenerator.gd   # Procedural floor layout, room types, spawn
├── npc/
│   └── NPCBase.gd             # Hub NPCs: dialog, shop, interaction
├── ui/
│   ├── HUD.gd                 # In-game HUD: health/mana/XP/gold/floor
│   └── DamageNumber.gd        # Floating damage numbers (pooled)
├── scenes/
│   ├── MainMenu.gd            # New game / continue / settings / quit
│   ├── Dungeon.gd             # Dungeon scene host
│   ├── Hub.gd                  # Hub area with NPCs
│   └── rooms/                 # Room template scenes go here
├── data/                      # JSON data files (items, skills, enemies, etc.)
└── shaders/
    └── crt.gdshader           # CRT post-processing shader
```

## Implementation Order

See `HANDOFF.md` for the full 5-sprint breakdown. Summary:

1. **Sprint 1** (Day 1-2): Core systems — DataManager, EventBus, GameManager, SaveSystem, ObjectPool
2. **Sprint 2** (Day 3-4): Character — StateMachine, PlayerCharacter, all states, movement
3. **Sprint 3** (Day 5-6): Combat — DamageCalculator, Projectile, EnemyBase, first enemy type
4. **Sprint 4** (Day 7-8): Content — DungeonGenerator, LootTable, ItemPickup, SkillManager + behaviors
5. **Sprint 5** (Day 9-10): Polish — HUD, NPC, MainMenu, CRT shader, audio, balance pass

## Key Patterns

- **EventBus**: All cross-system communication via signals — no direct references
- **State Machine**: Character states (Idle/Walk/Attack/Dash/Stunned/Death) with clean transitions
- **Object Pooling**: Projectiles, VFX, items, damage numbers — no runtime instantiation
- **Component Composition**: Player has Stats, Equipment, Skills, Inventory as child nodes
- **JSON Data**: All game content in `data/*.json` — no hardcoded items/skills/enemies
- **Scaling**: Enemy stats scale by level using `base × scalar^(level-1)`

## Notes

- All GDScript files use `extends` and Godot 4.x typed arrays
- `project.godot` has input actions pre-mapped (WASD + arrows, mouse/space for attack, Shift/E for dash, F interact, I inventory, K skill tree, Esc pause)
- Physics layers: 0=world, 1=hitbox, 2=hurtbox, 3=pickup
- Renderer: GL Compatibility, NEAREST filter, 640×360 viewport scaled 2×
- 8 autoloads with strict load order (DataManager first, AudioManager last)