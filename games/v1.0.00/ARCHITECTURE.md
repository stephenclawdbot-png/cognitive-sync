# v1.0.00 "wizdung" — Technical Architecture Document

> **Purpose:** Complete system architecture for building wizdung from scratch in Godot 4.x.
> **Audience:** Lead programmer, systems engineers, gameplay programmers.
> **Companion docs:** GAME_MECHANICS.md, ECONOMY.md, DATA_MODELS.md, BALANCE.md, LEVEL_DESIGN.md

---

## 1. HIGH-LEVEL SYSTEM MAP

```
┌─────────────────────────────────────────────────────────────────────┐
│                        WIZDUNG SYSTEM MAP                            │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Input   │  │  Event   │  │  Save    │  │  Scene   │            │
│  │ Manager  │  │   Bus    │  │  System  │  │ Manager  │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│       │              │              │              │                  │
│       ▼              ▼              ▼              ▼                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    GAME MANAGER (Autoload)                    │   │
│  │          game_state | current_class | run_data               │   │
│  └───────────────────────┬─────────────────────────────────────┘   │
│                          │                                           │
│       ┌──────────────────┼──────────────────┐                        │
│       ▼                  ▼                  ▼                        │
│  ┌─────────┐    ┌──────────────┐   ┌────────────┐                   │
│  │ Character │   │  Dungeon     │   │    Hub     │                   │
│  │  System  │   │  System      │   │  System    │                   │
│  └────┬────┘   └──────┬───────┘   └──────┬─────┘                   │
│       │               │                   │                          │
│       ▼               ▼                   ▼                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    COMBAT SYSTEM                              │   │
│  │  Hitbox | Projectile | StatusEffect | DamageCalc | VFX       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    ITEM SYSTEM                                │   │
│  │  LootTable | Rarity | Modifiers | Inventory | Equipment      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    SKILL SYSTEM                                │   │
│  │  SkillTree | Behaviors | Modifiers | Cooldowns | ManaCost      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐        │
│  │  UI Layer   │  │  Audio Mgr  │  │  Object Pool         │        │
│  │  (Canvas)   │  │  (Busses)   │  │  (Projectiles/VFX)   │        │
│  └─────────────┘  └─────────────┘  └─────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. AUTOLOAD SINGLETONS

All core systems are Godot Autoloads (singletons) registered in `project.godot`:

| Singleton | Script Path | Purpose |
|-----------|-------------|---------|
| `GameManager` | `res://core/GameManager.gd` | Global game state, run data, class data |
| `SceneManager` | `res://core/SceneManager.gd` | Scene transitions, hub↔dungeon, room loading |
| `SaveSystem` | `res://core/SaveSystem.gd` | JSON save/load, stash persistence, settings |
| `EventBus` | `res://core/EventBus.gd` | Decoupled signal bus for cross-system communication |
| `InputManager` | `res://core/InputManager.gd` | Keyboard + controller input, deadzone, rebinding |
| `ObjectPool` | `res://core/ObjectPool.gd` | Pre-instantiated projectiles, VFX, globs |
| `AudioManager` | `res://core/AudioManager.gd` | SFX playback, music, 2D positional audio |
| `DataManager` | `res://core/DataManager.gd` | Loads all JSON data (stats, items, skills, enemies) |

### 2.1 Singleton Load Order

```
1. DataManager    (loads all JSON — must be first, others depend on it)
2. EventBus       (signal infrastructure — must exist before anything connects)
3. SaveSystem     (loads save file — needed before game state initializes)
4. GameManager    (initializes from save data)
5. InputManager   (input mapping — needed before player spawns)
6. SceneManager   (scene management — loads first scene)
7. ObjectPool     (pre-warm pools — needed before combat starts)
8. AudioManager   (audio bus setup — can be last)
```

---

## 3. EVENT BUS — SIGNAL ARCHITECTURE

The EventBus uses Godot signals for fully decoupled communication. No system references another system directly — all cross-system communication goes through EventBus.

### 3.1 Signal Catalog

```gdscript
# res://core/EventBus.gd
extends Node
signal player_hit(damage: float, source: Node)
signal player_died()
signal player_healed(amount: float)
signal player_mana_changed(current: float, max: float)
signal player_level_up(new_level: int)
signal player_xp_changed(current: float, needed: float)

signal enemy_hit(enemy: Node, damage: float, is_crit: bool)
signal enemy_killed(enemy: Node, xp: float, money: float)
signal enemy_spawned(enemy: Node)
signal boss_spawned(boss: Node)
signal boss_died(boss: Node)

signal item_dropped(item: Dictionary, position: Vector2)
signal item_picked_up(item: Dictionary)
signal item_equipped(slot: String, item: Dictionary)
signal item_identified(item: Dictionary)

signal skill_activated(skill_id: String)
signal skill_cooldown_started(skill_id: String, duration: float)
signal skill_cooldown_finished(skill_id: String)

signal room_entered(room_level: int, room_type: String)
signal room_cleared()
signal door_locked(door_id: String)
signal door_unlocked(door_id: String)
signal portal_entered(destination: String)

signal gold_changed(amount: int)
signal gold_picked_up(amount: int)

signal status_effect_applied(target: Node, effect: String, duration: float)
signal status_effect_expired(target: Node, effect: String)

signal inventory_opened()
signal inventory_closed()
signal skill_tree_opened()
signal skill_tree_closed()
signal dialog_started(npc_id: String)
signal dialog_ended()

signal save_started()
signal save_completed()
signal save_failed(error: String)

signal class_changed(new_class: String)
signal skill_point_spent(node_id: String)
signal skill_point_refunded()
```

### 3.2 Signal Flow Examples

```
PLAYER ATTACKS ENEMY:
  Player.Attack → HitboxSystem → EventBus.enemy_hit(enemy, damage, crit)
    → UIManager: show damage number
    → VFXManager: spawn hit spark
    → AudioManager: play hit sound
    → Enemy: reduce health, check death

ENEMY DIES:
  Enemy.Death → EventBus.enemy_killed(enemy, xp, money)
    → XPSystem: add XP, check level up
    → LootSystem: roll loot table, spawn drops
    → VFXManager: spawn death VFX
    → AudioManager: play death sound
    → UIManager: update kill counter

ITEM DROPS:
  LootSystem.roll_loot(enemy_level) → EventBus.item_dropped(item_dict, pos)
    → ObjectPool: spawn item pickup node
    → VFXManager: spawn drop sparkle
```

---

## 4. CHARACTER SYSTEM ARCHITECTURE

### 4.1 Class Hierarchy

```
CharacterBody2D (Godot built-in)
└── PlayerCharacter (base player class)
    ├── DexWizard (Agility class — projectile + dash specialist)
    ├── IntWizard (Wisdom class — frost + area control)
    └── StrWizard (Power class — melee + tank)
```

### 4.2 Component Composition

```
PlayerCharacter (CharacterBody2D)
├── StateMachine (Node)
│   ├── State_Idle
│   ├── State_Walk
│   ├── State_Attack (8 directional variants)
│   ├── State_Dash
│   ├── State_Death
│   └── State_Stunned
├── StatsComponent (Node)
│   ├── core_stats (dictionary: 40+ stats)
│   ├── derived_stats (computed from core)
│   ├── modifiers (temporary buffs/debuffs)
│   └── stat_curves (per-level scaling)
├── EquipmentManager (Node)
│   ├── slots: {weapon, chest, helmet, boots, ring, necklace}
│   └── equipment_changed signal → StatsComponent.recalc
├── SkillManager (Node)
│   ├── equipped_skills: [basic_attack, special_attack, dash_skill]
│   ├── cooldowns: Dictionary
│   ├── mana_costs: Dictionary
│   └── skill_tree: SkillTree (per-class)
├── InventoryManager (Node)
│   ├── slots: Array[Dictionary] (grid)
│   ├── max_slots: int
│   └── pickup/drop/stack logic
├── HealthComponent (Node)
│   ├── current_health: float
│   ├── max_health: float
│   ├── ethereal_armor: float
│   └── death signal
├── ManaComponent (Node)
│   ├── current_mana: float
│   ├── max_mana: float
│   ├── regen_rate: float
│   └── cost/drain logic
├── StatusEffectManager (Node)
│   ├── active_effects: Array[StatusEffect]
│   ├── apply_effect(type, duration, magnitude)
│   └── tick/update logic
├── Hitbox2D (Area2D)
│   ├── damage: float
│   ├── damage_type: String
│   └── active_frames: Vector2 (start, end)
├── Hurtbox2D (Area2D)
│   ├── receives_damage: bool
│   └── on_area_entered → EventBus.player_hit
├── AimingReticle (Node2D)
│   ├── direction: Vector2
│   └── update from mouse/gamepad
├── AnimationPlayer (AnimationPlayer)
│   ├── 8-directional spritesheet playback
│   ├── walk/idle/attack/dash/death/stunned
│   └── signal: animation_finished
└── Sprite2D (Sprite2D)
    └── texture: per-direction spritesheet
```

### 4.3 State Machine Pattern

```gdscript
# res://character/state_machine/State.gd
class_name State extends Node
var machine: StateMachine
var player: PlayerCharacter

func enter() -> void:
    pass

func exit() -> void:
    pass

func process(delta: float) -> void:
    pass

func physics_process(delta: float) -> void:
    pass

func handle_input(event: InputEvent) -> void:
    pass
```

```gdscript
# res://character/state_machine/StateMachine.gd
class_name StateMachine extends Node
@export var initial_state: State

var current_state: State
var states: Dictionary = {}

func _ready() -> void:
    for child in get_children():
        if child is State:
            states[child.name] = child
            child.machine = self
            child.player = get_parent()
    if initial_state:
        current_state = initial_state
        current_state.enter()

func change_state(new_state_name: String) -> void:
    if not states.has(new_state_name):
        return
    if current_state:
        current_state.exit()
    current_state = states[new_state_name]
    current_state.enter()

func _process(delta) -> void:
    if current_state:
        current_state.process(delta)

func _physics_process(delta) -> void:
    if current_state:
        current_state.physics_process(delta)

func _unhandled_input(event) -> void:
    if current_state:
        current_state.handle_input(event)
```

---

## 5. COMBAT SYSTEM ARCHITECTURE

### 5.1 Damage Pipeline

```
ATTACK INITIATED
    │
    ▼
┌──────────────┐
│ SkillManager │  ← Gets equipped skill behavior
│ .activate()  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Behavior    │  ← Executes behavior (projectile, melee, AOE, dash)
│  System      │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  Hitbox /    │────▶│  Damage      │
│  Projectile  │     │  Calculator  │
│  spawned      │     └──────┬──────┘
└──────────────┘            │
                            ▼
                   ┌────────────────┐
                   │ Calculate:     │
                   │ base_damage    │
                   │ + elemental    │
                   │ - resistance  │
                   │ - toughness   │
                   │ × crit_mult   │
                   │ × dmg_mult    │
                   └───────┬────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              ┌──────────┐ ┌──────────────┐
              │  Target  │ │ StatusEffect │
              │  takes   │ │  roll chance │
              │  damage  │ │  (burn/shock)│
              └────┬─────┘ └──────┬───────┘
                   │              │
                   ▼              ▼
              ┌──────────────────────────┐
              │    EventBus.enemy_hit     │
              │  → VFX, SFX, UI numbers  │
              └──────────────────────────┘
```

### 5.2 Damage Calculation Formula

```
final_damage = (
    (base_damage + elemental_damage)
    × damage_multiplier
    × crit_multiplier (if crit)
    - target_toughness_reduction
    × (1 - target_elemental_resistance)
)
MINIMUM: final_damage = max(1, final_damage)  # always at least 1 damage
```

### 5.3 Projectile Pool System

```gdscript
# Projectiles are pooled — never instantiate at runtime
# Pool size: 100 projectiles pre-warmed at game start
# Pool retrieves inactive projectile → sets properties → activates
# Projectile hits something → deactivates → returns to pool

class_name ProjectilePool extends Node2D

var pool: Array[Projectile] = []
var pool_size: int = 100

func _ready():
    for i in pool_size:
        var proj = preload("res://combat/Projectile.tscn").instantiate()
        proj.active = false
        add_child(proj)
        pool.append(proj)

func spawn(position: Vector2, direction: Vector2, data: Dictionary) -> Projectile:
    for proj in pool:
        if not proj.active:
            proj.configure(position, direction, data)
            proj.active = true
            return proj
    # Pool exhausted — expand or warn
    return null
```

---

## 6. ITEM SYSTEM ARCHITECTURE

### 6.1 Item Lifecycle

```
LOOT ROLL
  │
  ▼
LootTable.roll(enemy_level, loot_chance_modifiers)
  │
  ├─ No drop → nothing
  ├─ Gear drop → create ItemInstance (unidentified)
  ├─ Key drop → spawn key pickup
  └─ Glob drop → spawn health/mana/money/xp glob
       │
       ▼
  ItemInstance created:
    id: UUID
    base_type: "weapon" | "chest" | "helmet" | "boots" | "ring" | "necklace"
    class_restriction: "dex" | "int" | "str" | "any"
    rarity: "common" | "magic" | "rare" | "epic" | "legendary"
    identified: false
    modifiers: [random from rarity-based pool]
    base_stats: from curve × enemy_level
       │
       ▼
  Spawn Pickup on ground → Player picks up → enters inventory
       │
       ▼
  Player visits Mysterious Wizard → identify (cost gold)
    identified: true
    modifiers revealed
       │
       ▼
  Player equips → StatsComponent recalculates with item modifiers
  OR
  Player sells to Trinket Witch → gold
  OR
  Player enchants at Trinket Witch → add new modifier (cost gold)
  OR
  Player stores in Stash → shared between classes
```

### 6.2 Rarity System

| Rarity | Color | Drop Weight | Modifier Count | Modifier Roll Range |
|--------|-------|-------------|----------------|-------------------|
| Common | Grey | 60% | 1 | 50-80% of max |
| Magic | Blue | 25% | 2 | 60-90% of max |
| Rare | Yellow | 10% | 3 | 70-100% of max |
| Epic | Purple | 4% | 4 | 80-110% of max |
| Legendary | Orange | 1% | 5 | 90-120% of max |

---

## 7. SKILL SYSTEM ARCHITECTURE

### 7.1 Skill Tree Data Structure

```
SkillTree
├── class_id: String ("dex" | "int" | "str")
├── sub_trees: Dictionary
│   ├── "basic_attack": SkillSubTree
│   ├── "movement": SkillSubTree
│   ├── "passive": SkillSubTree
│   └── "special_attack": SkillSubTree
│
SkillSubTree
├── nodes: Array[SkillNode] (9 nodes per sub-tree)
├── allocated: Dictionary (node_id → bool)
├── dependencies: Dictionary (node_id → [prerequisite_node_ids])
│
SkillNode
├── id: String (e.g., "dex_basic_001")
├── name: String ("Projectile")
├── description: String
├── behaviors: Array[String] (behavior IDs to enable)
├── modifiers: Dictionary (stat modifications)
├── cost: int (skill points, usually 1)
├── prerequisites: Array[String] (node IDs that must be allocated first)
├── position: Vector2 (UI position in tree)
```

### 7.2 Skill Behavior System

Behaviors are modular components that modify how a skill works:

```
Behavior System
├── BaseBehavior (abstract)
│   ├── apply(skill_data: Dictionary) -> Dictionary  (modifies skill data)
│   └── get_modifiers() -> Dictionary
│
├── ProjectileBehavior: Makes melee attack ranged
├── PiercingBehavior: Projectile pierces N enemies
├── DoubleStrikeBehavior: Attack hits twice
├── AOEBehavior: Area damage on hit
├── DashBehavior: Dash to target
├── ForkBehavior: Projectile splits on hit
├── ExplodeOnKillBehavior: Enemy explodes on death
├── ShockChanceBehavior: Adds shock chance
├── StatusEffectBehavior: Applies status on hit
├── ... (26+ behaviors total)
```

### 7.3 Skill Activation Flow

```
Player presses attack button
    │
    ▼
SkillManager.activate("basic_attack")
    │
    ├── Check cooldown → if on cooldown, return
    ├── Check mana → if insufficient, return
    ├── Deduct mana
    ├── Start cooldown
    │
    ▼
Get skill definition from DataManager
    │
    ▼
Get all allocated nodes in the skill's sub-tree
    │
    ▼
For each allocated node → apply behaviors to skill_data
    │
    ▼
Execute skill with modified skill_data
    (spawn projectile, create hitbox, dash, AOE, etc.)
    │
    ▼
EventBus.skill_activated("basic_attack")
```

---

## 8. DUNGEON SYSTEM ARCHITECTURE

### 8.1 Room Generation Pipeline

```
Enter Portal → SceneManager loads dungeon scene
    │
    ▼
DungeonGenerator.generate(dungeon_level)
    │
    ├── Select room_set for current tier (tutorial/T1/T2/endgame)
    ├── Pick N rooms from room_set (random selection)
    │
    ▼
For each room:
    │
    ├── Load tilemap template (pre-built .tscn room scenes)
    ├── Place enemies at spawn points
    │   ├── Enemy count = base_pack_size × pack_size_modifier
    │   ├── Enemy level = dungeon_level
    │   ├── Elite chance = monster_rarity_stat
    │   └── Boss room: 1 boss + minions
    │
    ├── Place loot (chests, ground drops)
    ├── Place doors (some locked, need keys)
    ├── Place key items (drop from specific enemies)
    └── Place exit portal (appears when room cleared)
    │
    ▼
Room entered → EventBus.room_entered(level, type)
    Player must clear all enemies → room_cleared
    → Doors unlock → Player chooses next room
    → Or portal appears → return to hub
```

### 8.2 Scene Structure

```
MainScene (Node2D)
├── TileMapLayer (Floor)
├── TileMapLayer (Walls — collision)
├── TileMapLayer (Decorations)
├── Entities (Node2D)
│   ├── Player (PlayerCharacter)
│   ├── Enemies (Node2D)
│   │   └── [enemy instances]
│   ├── Items (Node2D)
│   │   └── [item pickup instances]
│   └── Doors (Node2D)
│       └── [door instances]
├── VFX (Node2D)
│   └── [pooled VFX instances]
├── Projectiles (Node2D)
│   └── [pooled projectile instances]
├── Camera2D
│   └── follow player, clamp to room bounds
├── UI (CanvasLayer)
│   ├── HUD (health, mana, skills)
│   ├── BossHealthBar
│   ├── RoomInfo
│   ├── InventoryUI (toggled)
│   ├── SkillTreeUI (toggled)
│   └── DialogBox (toggled)
└── CRTShader (ColorRect with shader)
```

---

## 9. SAVE SYSTEM ARCHITECTURE

### 9.1 Save File Structure

```json
{
    "version": "1.0.0",
    "timestamp": "2026-07-29T12:00:00",
    "playtime_seconds": 14400,
    "characters": {
        "dex": {
            "level": 15,
            "xp": 4500,
            "xp_next": 6000,
            "skill_points_available": 3,
            "skill_tree": {
                "basic_attack": [true, true, true, false, false, false, false, false, false],
                "movement": [true, true, false, false, false, false, false, false, false],
                "passive": [true, false, false, false, false, false, false, false, false],
                "special_attack": [false, false, false, false, false, false, false, false, false]
            },
            "equipped_skills": ["basic_attack", "dash", "special_attack"]
        },
        "int": { ... },
        "str": { ... }
    },
    "current_class": "dex",
    "gold": 12500,
    "inventory": [
        {"id": "uuid1", "type": "weapon", "rarity": "epic", "identified": true, "modifiers": [...]},
        {"id": "uuid2", "type": "helmet", "rarity": "rare", "identified": false, "modifiers": [...]}
    ],
    "equipment": {
        "dex": {"weapon": "uuid1", "chest": null, "helmet": "uuid2", "boots": null, "ring": null, "necklace": null},
        "int": { ... },
        "str": { ... }
    },
    "stash": [
        {"id": "uuid3", "type": "ring", "rarity": "legendary", "identified": true, "modifiers": [...]}
    ],
    "dungeon_progress": {
        "highest_level_reached": 7,
        "bosses_killed": 3
    },
    "settings": {
        "master_volume": 0.8,
        "sfx_volume": 0.9,
        "music_volume": 0.6,
        "crt_shader": true,
        "screen_shake": true,
        "controller_deadzone": 0.2,
        "keybinds": { ... }
    }
}
```

### 9.2 Save Triggers

- **Auto-save:** On room cleared, on boss kill, on level up, every 60 seconds
- **Manual save:** Pause menu → Save → select slot
- **No save:** During combat (prevents save-scumming)

---

## 10. HUB SYSTEM ARCHITECTURE

### 10.1 Hub Layout

```
Hub Scene (Node2D)
├── TileMap (Hub floor/walls — safe zone, no enemies)
├── NPCs (Node2D)
│   ├── MysteriousWizard (identify items, respec skill tree)
│   ├── TrinketWitch (enchant items, sell items)
│   ├── NPC_DexWizard (character switch → become Dex Wizard)
│   ├── NPC_IntWizard (character switch → become Int Wizard)
│   ├── NPC_StrWizard (character switch → become Str Wizard)
│   └── InstructionMan (tutorial NPC)
├── Stash (Interactable → opens StashUI)
├── Portal (Interactable → enter dungeon)
├── Player (PlayerCharacter)
├── Camera2D (follow player in hub)
└── UI (CanvasLayer)
    ├── HUD
    ├── StashUI (toggled)
    ├── DialogBox (toggled)
    ├── MerchantUI (toggled)
    └── IdentifyUI (toggled)
```

### 10.2 NPC Interaction Flow

```
Player approaches NPC → interact prompt appears
    │
    ▼
Player presses interact → DialogSystem starts
    │
    ├── Dialog profile loaded (NPC-specific dialog sets)
    ├── Dialog conditions checked (e.g., "has_unidentified_items?")
    ├── Dialog options shown (identify, respec, switch class, etc.)
    │
    ▼
Player selects option
    │
    ├── "Identify items" → Open IdentifyUI → select item → pay gold → reveal
    ├── "Respec" → Confirm dialog → reset skill tree → refund points → pay gold
    ├── "Enchant" → Open EnchantUI → select item → pay gold → add modifier
    ├── "Sell" → Open MerchantUI → select items → sell for gold
    ├── "Switch class" → Character_Change_Response → swap active class
    └── "Talk" → Continue dialog tree
```

---

## 11. PERFORMANCE BUDGET

| System | Budget | Notes |
|--------|--------|-------|
| Draw calls | <200 per frame | Use sprite atlases, batch rendering |
| Physics bodies | <100 active | Enemy limit per room: 20 max |
| Projectiles | Pool size: 100 | Pre-warmed, reused, never freed |
| VFX | Pool size: 50 | Pre-warmed, reused |
| Audio voices | 32 max | Godot default, adjust if needed |
| Tilemap layers | 3-4 max | Floor, walls, decorations, overhead |
| Script process | <2ms total | Profile critical paths |
| Memory | <256MB | Texture atlas + audio + data |
| Target FPS | 60 | Pixel art is lightweight |

### 11.1 Optimization Strategies

- **Sprite atlases:** Combine all character directions into one atlas per class
- **Object pooling:** All projectiles, VFX, and item pickups are pooled
- **Scene instancing:** Room templates are .tscn scenes, pre-loaded
- **Data caching:** All JSON data loaded once at startup by DataManager
- **Lazy loading:** Tileset textures loaded per-dungeon, freed on exit
- **Signal decoupling:** EventBus prevents unnecessary cross-references
- **Process mode:** Inactive entities set to `PROCESS_MODE_DISABLED`

---

## 12. INPUT MAPPING

### 12.1 Default Keybinds

| Action | Keyboard | Controller (Xbox) |
|--------|----------|-------------------|
| Move | WASD | Left Stick |
| Aim | Mouse | Right Stick |
| Basic Attack | Left Click / Space | RT |
| Special Attack | Right Click / Q | LT |
| Dash | Shift / E | RB |
| Interact | F | A |
| Inventory | Tab / I | Y |
| Skill Tree | K | D-Pad Right |
| Pause | Esc | Start |
| Use Item (Health) | 1 | D-Pad Up |
| Use Item (Mana) | 2 | D-Pad Down |

### 12.2 Input Action Definitions

```ini
# project.godot → [input]
move_up = [W, Up Arrow, JoyAxis2-]
move_down = [S, Down Arrow, JoyAxis2+]
move_left = [A, Left Arrow, JoyAxis0-]
move_right = [D, Right Arrow, JoyAxis0+]
aim = [MouseMotion, JoyAxis3]
basic_attack = [MouseLeft, Space, JoyButton7]
special_attack = [MouseRight, Q, JoyButton6]
dash = [Shift, E, JoyButton5]
interact = [F, JoyButton0]
inventory = [Tab, I, JoyButton3]
skill_tree = [K, JoyButton14]
pause = [Escape, JoyButton6]
use_health = [1, JoyButton12]
use_mana = [2, JoyButton13]
```

---

## 13. RENDERING PIPELINE

```
World rendering:
  TileMap layers → Sprite2D (characters/enemies) → Hitbox2D → VFX sprites
    ↓
  Y-sort enabled (characters sort by Y position for depth)
    ↓
  Camera2D (follows player, pixel-locked, clamp to room bounds)
    ↓
  CanvasLayer (UI):
    HUD, Inventory, SkillTree, Dialog, Menus
    ↓
  CRT Shader (post-processing):
    ColorRect with custom shader (scanlines, slight curvature, chromatic aberration)
    ↓
  Screen output
```

### 13.1 Pixel-Perfect Settings

```ini
# project.godot
[rendering]
textures/canvas_textures/default_texture_filter = NEAREST
renderer/rendering_method = "gl_compatibility"
```

```gdscript
# Camera2D settings
camera.position_smoothing_enabled = true
camera.position_smoothing_speed = 8.0
# Snap camera to pixel grid
camera.snap_offset = Vector2(0.5, 0.5)  # offset for odd sprite sizes
```

---

## 14. TESTING STRATEGY

### 14.1 Unit Tests

| Module | Test | Method |
|--------|------|--------|
| DamageCalculator | Damage formula correctness | GUT (Godot Unit Test) |
| StatsComponent | Derived stat calculations | GUT |
| LootTable | Drop rate distribution | Statistical sampling (1000 rolls) |
| SkillTree | Node dependency validation | GUT |
| SaveSystem | Save/load round-trip | GUT |
| Enemy AI | State transitions | Manual playtest |
| RoomGenerator | Room population | Manual playtest |

### 14.2 Integration Tests

| Flow | Test |
|------|------|
| Full combat loop | Spawn enemy → attack → kill → loot → equip |
| Full dungeon run | Enter → fight 3 rooms → boss → return to hub |
| Character switch | Hub → switch class → skill tree persisted → stats different |
| Save/load | Play 10 min → save → load → verify all state intact |
| Stash sharing | Store item as Dex → switch to Int → retrieve from stash |

### 14.3 Performance Tests

| Metric | Target | Test |
|--------|--------|------|
| FPS | 60 stable | 20 enemies on screen, 30 projectiles, 10 VFX |
| Frame time | <16.67ms | Same scenario, profiled |
| Memory | <256MB | After 30-min play session |
| Load time | <2s | Room transition |