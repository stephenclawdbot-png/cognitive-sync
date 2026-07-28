# Legendum — Technical System Architecture

> **Engine:** Godot 4.6.2 · **Language:** GDScript · **Target:** 60 FPS @ 1080p, 45–90 min per life
> **Audience:** Lead programmers, systems engineers, tools devs. Hand-off ready.
> **Source basis:** Reverse-engineered from v0.14.1 demo PCK (610 GDScript files, 599 scenes, 1458 resources).

---

## 1. System Architecture Diagram

```
                          ┌─────────────────────────────────────────────┐
                          │                 APPLICATION LAYER             │
                          │      Main Scene Tree / Scene Manager          │
                          │   (Title → OriginSelect → Town → Combat →    │
                          │    QuietYears → LifeReview → Reincarnate)    │
                          └───────────────────────┬─────────────────────┘
                                                  │ owns
                          ┌───────────────────────▼─────────────────────┐
                          │               GAME MANAGER (autoload)         │
                          │  orchestrates sub-systems, owns the run,     │
                          │  routes EventBus signals, drives lifecycle   │
                          └───┬───────┬───────┬───────┬───────┬─────────┘
                              │       │       │       │       │
        ┌─────────────────────┘       │       │       │       └──────────────────────┐
        ▼                             ▼       │       ▼                              ▼
┌───────────────┐         ┌────────────────┐  │  ┌───────────────┐         ┌──────────────────┐
│  SAVE SYSTEM   │         │   EVENT BUS    │  │  │  INPUT MGR    │         │   SCENE MANAGER   │
│  shelve-it     │◀───────▶│  (global sigs) │  │  │  (actions +   │         │  (transitions,    │
│  SaveService    │         │  on_day_passed │  │  │   remap, DPAD)│         │   fades, stacks)  │
│  SaveGame       │         │  on_combat_end │  │  └───────────────┘         └──────────────────┘
│  SaveLoadData   │         │  on_death ...  │  │
└───────┬───────┘         └────────┬───────┘  │
        │ serializes                │ broadcast│
        ▼                            ▼         │
┌──────────────────────────────────────────────┴─────────────────────────────┐
│                          PERSISTENT STATE LAYER                            │
│   (JSON-serializable RefCounted objects — one file per save slot)           │
│                                                                             │
│   CharacterState  CalendarState  CampaignState  InventoriesState            │
│   JournalState   LootState       MetaState       NarrativeState             │
│   PerkSelectionState  RunState   ShopData       TasksState                  │
│   WebState        WorldState     Metrics        Milestone                   │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │ mutated by
                ┌───────────────┴────────────────────────────────┐
                ▼                                                ▼
┌───────────────────────────────┐                 ┌──────────────────────────────┐
│        SIMULATION LAYER        │                 │        CONTENT LAYER          │
│  (stateless logic operating    │                 │  (static .tres resources,     │
│   on Persistent State)        │                 │   loaded via define-it DB)    │
│                               │                 │                               │
│  AgingLogic      Calendar      │◀────── reads ──│  items.json  abilities.json  │
│  CombatHelpers  EncounterLogic│                 │  perks.json  enemies.json    │
│  Jobs            ProfessionsLogic                │  skills.json jobs.json       │
│  AbilitiesLogic TaskManager   │                 │  narratives.json shops.json  │
│  TitlesLogic     XPUtils       │                 │  + .tres perk/ability/etc.   │
└───────────────┬───────────────┘                 └──────────────────────────────┘
                │ emits events
                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                               │
│   Reactive<T> / ComputedReactive<T> — observable values bound to UI controls  │
│   UI scenes subscribe; on mutation they tween / refresh automatically          │
│                                                                               │
│   HUD  Inventory  PerkWeb  Quests  Shop  Region  Abilities  Status  Settings  │
│   StoryWeb  QuietYears  LifeReview  Dialogue  Contacts  Journal  SavePanel   │
└──────────────────────────────────────────────────────────────────────────────┘
```

The cardinal rule: **simulation logic never touches nodes, presentation never mutates state directly.** All cross-cutting communication goes through the EventBus; all state lives in the Persistent State Layer and is serialized by the SaveSystem.

---

## 2. Core Engine Systems

### 2.1 GameManager (autoload singleton)

The conductor. Owns the current `RunState`, holds references to every other singleton, and drives the high-level state machine of a life.

```
GameManager (Node, autoload "GameManager")
├── run_state: RunState                     # the live run (null between lives)
├── meta_state: MetaState                   # permanent across lives
├── calendar: CalendarState                 # owned here for time-wide queries
├── current_origin: LifeOrigin              # chosen at character draft
├── current_backstory: LifeBackstory         # chosen at draft
├── life_stage_idx: int                      # 0..3 (young/veteran/elder/decrepit)
├── pending_reincarnation: bool
└── funcs:
    begin_life(origin, backstory, soul_perks[])
    advance_day()                            # delegates to Calendar, fires on_day_passed
    enter_combat(encounter_def)             # pushes CombatScene via SceneManager
    end_combat(result)                      # applies rewards, fires on_combat_end
    begin_quiet_years(span)                 # narrated time jump
    end_life()                              # → LifeReview → grant LP → reincarnate
    reincarnate(soul_perk_selection)
    save(slot_id) / load(slot_id)
```

**Lifecycle state machine** (see §10 for full diagram): `BOOT → TITLE → DRAFT → YOUTH → LIFE(ADVENTURE|TOWN|COMBAT) → QUIET_YEARS → LIFE_REVIEW → REINCARNATE → YOUTH …`.

### 2.2 SceneManager

Wraps Godot's `SceneTree.change_scene_to_packed()` with a transition bus. Maintains a small stack for "enter building" return-trips so the player can pop back to the town map without re-instantiating it.

```
SceneManager (Node, autoload)
├── push(scene_packed, params: Dictionary, transition="fade")
├── pop(transition="fade")
├── replace(scene_packed, params)
├── get_param(key) -> Variant                # params passed to the new scene's _ready
└── current_mode: Mode { EXPLORE, COMBAT, UI_MODAL, NARRATIVE, LIFE_REVIEW }
```

Transitions are 0.25s Tween fades over a black ColorRect; never block input mid-fade (queue the input). All scene entry points read params via `SceneManager.get_param()` so the caller does not need a direct reference.

### 2.3 SaveSystem (shelve-it addon wrapper)

Versioned JSON serialization. Every save slot is a single JSON document with a top-level `save_version` and a per-subsystem object. The system is **migration-aware**: a `Migrators` table maps old versions forward on load, never on save.

```
SaveService (autoload)
├── save(slot_id: int) -> void                # serialize all *State objects → JSON → user://save_<id>.json
├── load(slot_id: int) -> bool                # read JSON → migrate → hydrate State singletons
├── export_to_text(slot_id) -> String         # for the "download save" UI button
├── import_from_text(json_text) -> bool       # for the "import save" UI button
├── list_slots() -> Array[SaveSlotInfo]
├── delete_slot(slot_id)
└── autosave_enabled: bool                    # fires on day_passed and on scene transition
```

**State objects persisted** (each is a `RefCounted` GDScript class under `scripts/data/persistent/`):

| State Object        | Purpose                                              | Reset on Death? |
|---------------------|------------------------------------------------------|-----------------|
| CalendarState       | Day, season, year, time-of-day slot                  | Yes             |
| CampaignState       | Story flags, web progress, region unlocks            | Yes             |
| CharacterState     | Attributes, skills, level, HP, age, life stage       | Yes             |
| InventoriesState    | Player inventory + equipment + heirloom bag         | Partial (heirlooms persist) |
| JournalState        | Quest log, threads, side quests, events              | Yes             |
| LootState           | Pending loot tables, discovery state                 | Yes             |
| MetaState           | Legend Points, Legend Rank, Soul Perks, Heirlooms    | **No (permanent)** |
| NarrativeState      | Active web, current node, dialogue history           | Yes             |
| PerkSelectionState  | Per-life perk web selections                         | Yes             |
| RunState            | Run id, origin, backstory, lifetime stats            | Yes             |
| ShopData            | All shop stocks + shortages + tiers                  | Yes             |
| TasksState          | Active jobs, task slots, cooldowns                    | Yes             |
| WebState            | Per-web node completion, sockets, selectors           | Yes             |
| WorldState          | Region flags, location states, NPC states             | Yes             |
| Metrics / Milestone | Lifetime telemetry and achievement milestones         | Partial         |

### 2.4 EventBus (signal bus singleton)

A plain `Node` autoload exposing typed GDScript signals. Systems connect to the signals they care about; emitters call `EventBus.signal_name.emit(args)`. This decouples combat from UI, aging from save, etc.

```gdscript
# EventBus.gd  (autoload "EventBus")
extends Node

# --- Time ---
signal day_passed(day: int, season: StringName)
signal season_changed(new_season: StringName)
signal turn_of_the_year(year: int)
signal time_slot_changed(slot: TimeSlot)        # MORNING / DAY / EVENING

# --- Character ---
signal attribute_leveled(stat: StringName, new_lvl: int)
signal skill_leveled(skill: StringName, new_lvl: int)
signal character_leveled(new_lvl: int)
signal hp_changed(current: int, maximum: int)
signal status_effect_applied(def_id: StringName)
signal status_effect_removed(def_id: StringName)
signal life_stage_changed(stage_idx: int)

# --- Combat ---
signal combat_started(encounter_id: StringName)
signal combat_wave_started(wave_idx: int)
signal enemy_spawned(enemy: Enemy)
signal enemy_damaged(enemy: Enemy, amount: int, is_crit: bool)
signal enemy_killed(enemy: Enemy)
signal player_damaged(amount: int, is_crit: bool)
signal ability_fired(ability_id: StringName)
signal combat_ended(result: CombatResult)

# --- Economy ---
signal gold_changed(new_total: int)
signal goods_changed(region: StringName, new_total: int)
signal lp_changed(new_total: int)
signal item_acquired(item_instance: ItemInstance)
signal item_equipped(slot: EquipSlot, item_instance: ItemInstance)
signal shop_stock_changed(shop_id: StringName)

# --- Narrative ---
signal story_node_entered(node_id: StringName)
signal story_choice_made(node_id: StringName, option_idx: int)
signal deed_recorded(deed_id: StringName)
signal web_completed(web_id: StringName)

# --- Meta ---
signal perk_unlocked(perk_id: StringName)
signal soul_perk_purchased(perk_id: StringName)
signal heirloom_awarded(heirloom_id: StringName)
signal legacy_points_granted(amount: int)

# --- Lifecycle ---
signal life_started(origin_id: StringName)
signal quiet_years_began(span_years: int)
signal death(trigger: DeathCause)
signal life_review_complete(summary: LifeSummary)
signal reincarnation_complete(new_origin_id: StringName)
```

**Rules:**
1. Signals carry **value types only** (StringName, int, Dictionary). Never pass Node references — use ids and let the receiver look the node up.
2. Emitters must not assume listeners; signals are best-effort broadcasts.
3. UI listeners must be connected in `_ready()` and disconnected in `_exit_tree()` to avoid dangling connections across scene transitions.
4. The EventBus never holds state — it is a pure dispatcher.

### 2.5 InputManager

Wraps Godot `InputMap` actions with a remappable binding table and a context stack so the same physical input can mean different things in town vs. combat vs. menu.

```
InputManager (autoload)
├── contexts: Array[InputContext]  # stack, top is active
│     EXPLORE → move, interact, open_tabs, cancel
│     COMBAT  → focus_attribute, swap_ability, retreat
│     MENU    → navigate, confirm, back
│     DIALOGUE→ advance, option_1..4
├── push_context(ctx) / pop_context()
├── remap(action: StringName, event: InputEvent)
├── is_action_pressed(action) -> bool   # respects active context
└── action_just_pressed(action) -> bool
```

Default bindings are loaded from `res://settings/default_input.tres`; user remaps persist into `MetaState.key_bindings`. Combat uses auto-targeting so the player only manages ability fires and attribute focus — no twin-stick aiming.

### 2.6 ObjectPool

A generic pool for short-lived nodes that spawn/despawn rapidly in combat: projectiles, damage text, hit particles, enemy corpses, loot drops. Avoids `queue_free()`/`instantiate()` churn that would otherwise tank combat FPS.

```gdscript
# ObjectPool.gd  (autoload "ObjectPool")
extends Node
var _pools: Dictionary = {}   # scene_path -> Array[Node]

func acquire(scene: PackedScene, parent: Node) -> Node:
    var key := scene.resource_path
    var pool: Array = _pools.get(key, [])
    if pool.is_empty():
        var n := scene.instantiate()
        parent.add_child(n)
        return n
    var n: Node = pool.pop_back()
    n.process_mode = Node.PROCESS_MODE_INHERIT
    n.set_visible(true)
    parent.add_child(n)
    n._on_pool_acquire()        # nodes implement this to reset state
    return n

func release(node: Node):
    var key := node.scene_file_path
    node._on_pool_release()       # nodes implement this to clear state
    node.get_parent().remove_child(node)
    node.set_visible(false)
    node.process_mode = Node.PROCESS_MODE_DISABLED
    (_pools[key] as Array).push_back(node)
```

Pooled node classes (`Arrow`, `ArcaneOrb`, `Fireball`, `DamageText`, `HitSpark`, `LootDrop`) implement `_on_pool_acquire()` and `_on_pool_release()`. Pool size caps per type are tuned in `CombatSettings` (default: arrows 64, orbs 32, damage text 128, sparks 64).

---

## 3. Life Simulation System

### 3.1 Age Progression

`AgingLogic` runs once per `day_passed`. Each day advances `CalendarState.day`; every N days (configurable per origin, default 30) the character gains one **age year**. Age years map to life stages via a curve:

| Age Years | Life Stage    | Stage idx | Stat Modifiers                                  |
|-----------|---------------|-----------|--------------------------------------------------|
| 0–14      | Young         | 0         | STR/DEX/VIG ×1.10, INT/WIS ×0.95, PER ×1.00       |
| 15–34     | Veteran       | 1         | STR/DEX/VIG ×1.00, INT/WIS ×1.05, PER ×1.00       |
| 35–54     | Elder         | 2         | STR/DEX/VIG ×0.90, INT/WIS ×1.15, PER ×1.05       |
| 55+       | Decrepit      | 3         | STR/DEX/VIG ×0.75, INT/WIS ×1.20, PER ×1.10, HP cap −20% |

The aging curve is data-driven: `scripts/resources/life_stage.gd` defines a `LifeStage` resource with `{id, name, min_age, max_age, stat_mods: Dictionary[StringName, float], narrative_blurb}`. The four observed stages (`stage1_young`, `stage3_veteran`, `stage4_elder`, `stage5_decrepit`) ship as `.tres` files in `resources/life_stages/`.

`AgingLogic.advance_year()`:
1. Increments `CharacterState.age`.
2. Looks up the stage whose `[min_age, max_age]` contains the new age; if the stage changed, fires `life_stage_changed` and applies the new `stat_mods` as a recompute trigger (not a stacked buff — the modifiers replace the previous stage's modifiers in the derived-stat pipeline).
3. If age exceeds the origin's `max_age` (default 70, modified by Soul Perks up to +20), fires `death(NATURAL)`.

### 3.2 Life Stages & Content Gating

Each life stage gates content — not by hard locks, but by **story web availability** and **task tier caps**. Example: T3 jobs (`t3_hunter.tres`, `expert_archivist`) require Veteran stage; the catacombs web opens at Veteran; the "mentor" quiet-years path opens at Elder. This is enforced by `Condition.has_origin_tag` and `ReqDomainRank` requirements on web nodes.

### 3.3 Quiet Years

The signature pacing device. After certain narrative milestones (or when the player chooses "fast-forward" from the menu), `GameManager.begin_quiet_years(span_years)` enters the QuietYears view:

```
QuietYears
├── span_years: int                       # how many years to skip
├── timeline: Array[QYTimelineEvent]      # one entry per year, generated procedurally
├── paths: Array[QuietYearPath]           # "mentor" / "travel" / "hermit" / "soldier"
├── impacts: Array[QuietYearImpact]       # stat/skill/gold deltas per year
└── on_complete(): applies all impacts, advances calendar by span_years, fires quiet_years_began + per-year sub-events
```

Each timeline entry (`ui_quiet_years_timeline_entry.scn`) shows a year blurb, an optional choice (`qy_timeline_event_choice.gd`), and the resulting impacts. The player gets to **steer** the montage rather than watch passively — preserving agency even during time skips.

### 3.4 Life Event System

Life events are **story web nodes** plus **quiet year events** plus **random life events**. The random layer fires off `day_passed`:

| Trigger              | Handler                           | Effect                                            |
|----------------------|-----------------------------------|---------------------------------------------------|
| day_passed           | `RandomLifeEventTable.roll(state)`| Small flavor events: find coin, meet traveler     |
| season_changed       | `SeasonalEventTable.roll()`       | Season-locked encounters & shop shortages         |
| turn_of_the_year     | `TurnOfTheYear.apply()`           | Refresh shop pools, reset seasonal counters       |
| life_stage_changed   | `StageTransitionEvents.fire()`    | Stage-specific narrative page, stat tutorial      |
| death                | `LifeReview.compose(summary)`     | Builds the review montage, grants LP              |

Random event tables are weighted JSON (loaded via define-it) so designers can tune without touching code.

---

## 4. Combat System (Auto-Battler)

### 4.1 Topology

Combat is **auto-battler**: the player character auto-attacks the nearest enemy with its equipped weapon, while the player manages ability fires, perk triggers, and which attribute to "focus" for XP. There is no manual movement during combat.

```
CombatScene (Node2D)
├── CombatViewport (SubViewport)             # low-res render, upscaled for pixel-perfect
│   ├── PlayerUnit (CharacterBody2D)
│   │    ├── StatsComponent (derived stats from CharacterState + equipment)
│   │    ├── WeaponScript (sword / bow / staff child)
│   │    ├── AbilitiesComponent (equipped AbilitySlots)
│   │    └── StatusEffectsComponent
│   ├── WaveSpawner (Node2D)
│   │    └── enemies: Array[Enemy]           # pooled, capped by spawn_cap
│   ├── ProjectileLayer (Node2D)             # pooled arrows / orbs / daggers
│   ├── DamageTextLayer (CanvasLayer)       # pooled damage_text bundle
│   └── HitSparkLayer (Node2D)              # pooled particles
├── CombatHUD (CanvasLayer)
│   ├── HPBar, EnergyBar, AbilityBar (cooldown wedges)
│   ├── AttributeFocusSelector (6 buttons, one per stat)
│   └── WaveIndicator, EnemyCounter
└── CombatSettings (Resource)               # scaling_profile, spawn params, caps
```

### 4.2 Turn / Tick Model

Although "turn-based" in feel, the engine uses a **fixed tick** at 60 Hz with cooldown-gated actions. Each weapon has `attack_speed` (attacks/sec); each ability has `cooldown` (sec). The "turn" abstraction is the ability cooldown cycle — the player watches cooldowns and fires abilities when ready.

`PlayerUnit._physics_process(dt)`:
1. Acquire target via `TargetFocus.acquire(nearest, weakest, strongest — per combat_style)`.
2. If weapon cooldown elapsed → fire `WeaponScript.attack(target)` → spawn projectile (pooled) → reset cooldown.
3. For each equipped ability, if `ability.is_auto` and cooldown elapsed → fire.
4. Status effects tick (burn DoT, regen, stun check).

### 4.3 Damage Formula

Implemented in `CombatHelpers.compute_damage(attacker, defender, weapon, ability_mod)`:

```
base_roll      = randf_range(weapon.damage_min, weapon.damage_max)
weapon_scaling = weapon.scaling_damage              # 0.8..1.3
stat_factor    = attacker.derived(weapon.scaling_stat) / 10.0
crit_roll      = randf() < attacker.crit_chance
crit_mult      = crit_roll ? attacker.crit_mult : 1.0
ability_mod    = ability ? ability.dmg_mult : 1.0
typed_mult     = TypeChart.effective(weapon.damage_type, defender.armor_type)
resist_mult    = 1.0 - clamp(defender.damage_resistance, 0.0, 0.85)
final = round(base_roll * weapon_scaling * stat_factor * crit_mult * ability_mod * typed_mult * resist_mult)
```

Crits emit `enemy_damaged(amount, is_crit=true)` which the DamageText bundle renders in gold with a 1.15× scale pop. Non-crits render in white. Heals render in green.

### 4.4 Combat Styles

Six `CombatStyle` resources (`power.tres`, `sword_style.tres`, `vigor.tres`, `precision.tres`, `speed.tres`, `bow_dex_per.tres`) define:

| Field            | Type     | Effect                                            |
|------------------|----------|---------------------------------------------------|
| target_strategy  | enum     | NEAREST / WEAKEST / STRONGEST                     |
| base_attack_mult | float    | Multiplier on weapon attack speed                 |
| crit_chance_bonus| float    | Added to crit chance                              |
| hp_mult          | float    | Multiplier on derived max HP                      |
| dodge_chance     | float    | Chance to avoid an incoming hit                   |
| block_rating     | float    | Reduces incoming damage when blocking             |
| auto_abilities   | Array    | Ability ids fired automatically on cooldown       |

Styles are unlocked via `reward_combat_styles` and chosen in the loadout tab. Per-life only one style is active; changing it requires returning to town.

### 4.5 Wave System

`Wave.gd` + `WaveSpawner` reads `CombatSettings.scaling_profile`:

```
swarm_spawn_interval_base:           1.4..10.0 sec
swarm_spawn_interval_decrease_per_minute: 0.2..2.0
swarm_spawn_interval_min:            0.1..3.0 sec
spawn_cap:                           3..4
grid_spawn:                          bool
no_overlap_spawn:                    true
scaling_damage:                      0.8..1.3   (enemy dmg mult)
scaling_health:                      0.8..3.5   (enemy hp mult)
```

Each encounter defines a wave list (`Array[Wave]`); on wave clear, `combat_wave_started` fires with the next index. On final wave clear, `combat_ended` fires with `result = VICTORY` and rewards are applied via `Reward.apply_all()`.

### 4.6 Enemies & AI

Enemy classes inherit from `base_mob.gd`:

| Class            | Behaviour                                                 |
|------------------|-----------------------------------------------------------|
| `Mob` (base)     | Move toward player, melee on contact                      |
| `ArcherMob`      | Keep distance, fire `enemy_arrow.scn` (pooled)            |
| `CasterMob`      | Channel `enemy_shaman_orb.scn` / `enemy_skeleton_orb.scn` |
| `DummyMob`       | No movement; training target                              |

Each `MobDef` (resource) carries: `id`, `sprite_scene`, `hp`, `damage`, `speed`, `attack_interval`, `tags[]` (used by `req_kill_mob_matching_tag` requirements), `loot_table`, `info` (e.g. "Boss"). Bosses get `scaling_health = 3.0+` and a unique nameplate.

---

## 5. Reincarnation System

### 5.1 Death Flow

```
death(trigger)
   │
   ▼
LifeReview.compose(run_state, meta_state, deeds)
   │ reads deeds, metrics, milestones, journal
   │ computes legacy_points = base + deeds_bonus + milestone_bonus
   ▼
life_review_complete(summary)
   │ UI shows montage: life cards, deed cards, stat recap
   ▼
grant_legacy_points(summary.legacy_points)   # adds to MetaState.legend_points
   ▼
SoulPerkSelectionScene  (player spends LP on Soul Perks)
   │
   ▼
reincarnation_complete(new_origin_id)
   │ resets all per-life State objects (CharacterState, RunState, etc.)
   │ keeps MetaState (LP, SoulPerks, Heirlooms, Deeds)
   │ applies SoulPerk effects as starting modifiers
   ▼
YOUTH scene  (new life begins)
```

### 5.2 Soul Perks

`SoulPerkDef` (resource, `scripts/resources/meta/soul_perk.gd`):

| Field            | Type     | Description                                              |
|------------------|----------|---------------------------------------------------------|
| id               | StringName | unique key                                             |
| display_name     | String   | UI label                                                |
| description      | String   | Rich-text effect summary                                |
| cost             | int      | Legend Point cost                                       |
| category         | enum     | TIME / STAT / SKILL / NARRATIVE / MISC                  |
| effects          | Array[MetaEffect] | Applied to every new life at draft time        |
| requires         | Array[Requirement] | e.g. Legend Rank ≥ 3                          |
| max_stacks       | int      | 1 by default; some perks stack (e.g. +5% XP)           |

Observed Soul Perks:
- **Early Bird** — "Start all lives with the Early Bird perk, unlocking the Morning slot."
- **Night Owl** — "Start all lives with the Night Owl perk, unlocking the Evening slot."

Stacking rules: `max_stacks` controls how many times a perk can be purchased. `MetaEffect`s are applied in purchase order; additive effects sum, multiplicative effects multiply (additive first, then multiplicative, then flat).

### 5.3 Legacy Points

LP is the meta-currency. Earned during a life from:
- `reward_lp` from quests (`LegendPointsReward` resource)
- Deed bonuses (each `deed.*` grants a fixed LP on first recording)
- Milestone bonuses (lifetime metrics crossing thresholds)
- Special quest rewards (e.g. "Training Grounds upgrade: +40 LP")

LP is **never lost** — only spent on Soul Perks. Unspent LP carries across deaths. The Legend Rank (`scripts/data/legend_rank.gd`) is a derived value from total LP earned (not current LP) and gates certain Soul Perks and content.

### 5.4 Carryover

| Carryover Item      | Lives in            | Notes                                                |
|---------------------|---------------------|------------------------------------------------------|
| Legend Points       | MetaState           | Spent on Soul Perks                                  |
| Legend Rank         | MetaState           | Derived from lifetime LP earned                      |
| Soul Perks          | MetaState           | Permanent until manually refunded (no UI for that) |
| Heirlooms           | MetaState.heirlooms | Items passed via `reward_heirloom`                  |
| Deeds               | MetaState.deeds     | Permanent record; some affect narrative (`condition_has_prior_life_deed`) |
| Key bindings        | MetaState           | User settings                                        |
| Lifetime metrics    | MetaState.metrics   | Telemetry for milestones                             |

Everything else (character level, attributes, skills, gold, items, perks, abilities, story progress, world state, contacts, quests) is **reset on death**.

---

## 6. Data Flow Diagrams

### 6.1 Day Advance

```
InputManager (player presses "Sleep" / time elapses)
        │
        ▼
GameManager.advance_day()
        │
        ├── CalendarState.advance_day()  →  emits day_changed
        ├── AgingLogic.tick(day)
        │       ├── may increment age  →  may change life stage
        │       └── may fire death(NATURAL)
        ├── TaskState.refresh_slots(time_of_day)
        ├── ShopData.refresh_shortages(day)
        ├── RandomLifeEventTable.roll(state)
        │
        ▼
EventBus.day_passed.emit(day, season)
        │
        ├── HUD updates day/season indicator (Reactive binding)
        ├── SaveService.autosave() if enabled
        ├── JournalState.append_day_entry()
        └── Quest deadline check (some quests expire in N days)
```

### 6.2 Combat Resolution

```
Player enters encounter (from map or quest)
        │
        ▼
SceneManager.push(CombatScene, {encounter_id})
        │
        ▼
CombatScene._ready()
   ├── loads EncounterDef via define-it
   ├── builds PlayerUnit from CharacterState + equipment + perks
   ├── instantiates WaveSpawner with CombatSettings
   └── EventBus.combat_started.emit(encounter_id)
        │
        ▼  (gameplay loop — auto-battler)
   PlayerUnit auto-attacks; abilities fire; waves spawn
        │
        ▼
Final wave cleared  →  combat_ended(VICTORY)
        │
        ▼
Reward.apply_all(encounter.rewards, run_state)
   ├── XpReward    → CharacterState.gain_xp
   ├── GoldReward  → InventoriesState.gold += amount
   ├── GoodsReward → WorldState.goods[region] += amount
   ├── LegendPointsReward → MetaState.legend_points += amount (rare in combat)
   ├── GiveItem    → InventoriesState.add_item(item_instance)
   └── RewardDeed → MetaState.deeds.add(deed_id)
        │
        ▼
SceneManager.pop() → returns to map/town
```

### 6.3 Story Web Choice

```
Player taps story node in UiStoryWebState
        │
        ▼
WebState.enter_node(node_id)
   ├── validates node.requirements against current state
   ├── displays NarrativePage(s) via UiNarrativeState
   └── shows options (NarrativeOption[])
        │
        ▼
Player picks option
        │
        ▼
NarrativeState.apply_option(option)
   ├── for each NarrativeOptionEffect:
   │     ├── Reward (gold, item, perk, location, contact, region…)
   │     ├── WorldStateChange
   │     └── set_campaign_flag
   ├── WebState.complete_node(node_id)
   └── EventBus.story_choice_made.emit(node_id, option_idx)
        │
        ▼
UI refreshes web view; newly unlocked nodes appear
        │
        ▼
If option closed a web → EventBus.web_completed.emit(web_id)
```

### 6.4 Save / Load

```
SaveService.save(slot_id):
   for each State singleton:
       payload[state_id] = state.to_dict()       # _to_dict() per State class
   payload["save_version"] = CURRENT_SAVE_VERSION
   payload["meta"] = { origin, backstory, played_at, playtime_sec }
   JSON.print(payload) → user://save_<slot_id>.json
   (atomic: write to .tmp then rename)

SaveService.load(slot_id):
   read JSON → parse → migrate(payload, payload.save_version → CURRENT)
   for each State singleton:
       state.from_dict(payload[state_id])
   GameManager.hydrate_from_states()
   SceneManager.replace(TownScene)  # or last scene stored in RunState
```

Migration is forward-only. `Migrators` is a `Dictionary[int, Callable]`; each migrator transforms a v-n payload to v-(n+1). Saves from unsupported (too old) versions are rejected with a UI message; saves from newer versions than the running build are also rejected.

---

## 7. Module Dependency Graph

Arrows mean "depends on". Singletons are at the top; stateless utilities at the bottom.

```
                  GameManager ──── SceneManager ── CombatScene/TownScene
                  │   │   │          │
                  │   │   │          ▼
                  │   │   │      InputManager
                  │   │   │
        ┌─────────┘   │   └───────────┐
        ▼             ▼               ▼
    SaveService   EventBus       ObjectPool
        │             ▲               ▲
        │             │               │
        ▼             │               │
   State singletons ──┴─ emit on ──────┘
   (Character, Calendar, Inventories, Journal, Meta, Narrative, …)
        │
        │ read / mutate
        ▼
   Simulation logic (stateless)
   ├── AgingLogic, Calendar, TaskManager, Jobs, ProfessionsLogic
   ├── CombatHelpers, EncounterLogic, AbilitiesLogic, Wave
   ├── TitlesLogic, XPUtils, LegendRank
   └── Requirement evaluator, Reward applier
        │
        │ read static data from
        ▼
   define-it JSON DB (items.json, abilities.json, perks.json,
                      enemies.json, skills.json, jobs.json,
                      narratives.json, shops.json) + .tres resources
        │
        │ referenced by
        ▼
   Reactive<T> / ComputedReactive<T>   ←── UI scenes bind here
```

**Layering rules:**
1. UI may only read Reactive values and emit user intent via signals; it never mutates State directly.
2. Simulation logic may mutate State and emit EventBus signals; it never touches Nodes or UI.
3. Singletons may hold State and subscribe to EventBus; they never instantiate gameplay nodes directly (SceneManager does that).
4. define-it DB is read-only at runtime; hot-reload only happens in editor.

---

## 8. Scene Tree Structure

```
Main (Window)
└── Root (Node)
    ├── GameManager (autoload Node)               # process_mode = ALWAYS
    ├── EventBus (autoload Node)                  # process_mode = ALWAYS
    ├── SaveService (autoload Node)              # process_mode = ALWAYS
    ├── SceneManager (autoload Node)
    ├── InputManager (autoload Node)
    ├── ObjectPool (autoload Node)
    ├── AudioBGM (AudioStreamPlayer, autoload)   # music
    ├── SFX (Node with pooled AudioStreamPlayer children, autoload)
    ├── TooltipManager (CanvasLayer, autoload)
    ├── DamageTextManager (CanvasLayer, autoload)
    └── CurrentScene (Node)                      # swapped by SceneManager
        ├── TownScene
        │   ├── TileMap (better-terrain)
        │   ├── YSort (Node2D)
        │   │   ├── Player (CharacterBody2D)
        │   │   └── NPCs (Node2D)
        │   │       └── NPC instances (schedule-driven position)
        │   ├── Camera2D (follows player, bounds per area)
        │   └── HUD (CanvasLayer)
        │       ├── TopBar (HP, Energy, Gold, Day/Season, Age, Level)
        │       ├── TabBar (Character, Inventory, Perks, Quests, Shop, Region, Abilities, Story, Settings)
        │       └── BottomRow (LP timeline, calendar indicator, URL button)
        ├── CombatScene  (SubViewport-based, see §4.1)
        ├── NarrativeScene  (story web / dialogue)
        ├── QuietYearsScene
        ├── LifeReviewScene
        ├── SoulPerkSelectionScene
        ├── CharacterDraftScene  (origin + backstory + soul perks review)
        └── TitleScene
```

---

## 9. Singleton / Autoload Organization

`project.godot` `[autoload]` section (order matters — later ones can depend on earlier):

| Order | Name            | Path                                           | Type           |
|-------|-----------------|------------------------------------------------|----------------|
| 1     | EventBus        | `res://scripts/core/event_bus.gd`              | Node           |
| 2     | SaveService     | `res://scripts/data/save_service.gd`           | Node           |
| 3     | InputManager    | `res://scripts/core/input_manager.gd`          | Node           |
| 4     | ObjectPool      | `res://scripts/core/object_pool.gd`            | Node           |
| 5     | SceneManager    | `res://scripts/core/scene_manager.gd`          | Node           |
| 6     | GameManager     | `res://scripts/game/core.gd`                   | Node           |
| 7     | AudioBGM        | `res://scripts/game/audio_bgm.gd`              | AudioStreamPlayer |
| 8     | SFX             | `res://scripts/game/sfx.gd`                    | Node           |
| 9     | TooltipManager  | `res://bundles/tooltip/tooltip_manager.gd`     | CanvasLayer    |
| 10    | DamageTextManager | `res://bundles/damage_text/damage_text.gd`   | CanvasLayer    |

State singletons (Character, Calendar, etc.) are **not** autoloads — they are owned by GameManager and serialized by SaveService. They expose themselves via `GameManager.<state_name>`.

---

## 10. Signal Bus Design Pattern

The EventBus is the **only** sanctioned channel for cross-system communication. The pattern is:
- **Producer** = any code that mutates state. After mutating, it emits the corresponding signal.
- **Consumer** = UI or other systems that need to react. They `connect()` in `_ready()` and `disconnect()` in `_exit_tree()`.
- **No back-channels**: systems do not hold references to each other except through GameManager (for state) and EventBus (for events).

Why this pattern:
1. Decouples combat from UI — UI can be rebuilt without touching combat code.
2. Decouples save from gameplay — SaveService listens to `day_passed` for autosave; gameplay does not know.
3. Makes debugging tractable — every cross-system event is named and grep-able.
4. Enables the editor hot-reload — define-it can re-emit `data_reloaded` and UI refreshes without restarting.

**Anti-patterns to reject in review:**
- Direct method calls between systems (`ShopData.refresh()` from combat code). Route through EventBus (`combat_ended` → `ShopData._on_combat_ended`).
- Passing Node references through signals. Pass ids; let receivers look up.
- Subscribing in `_init()`. Always `_ready()`/`_exit_tree()` so scene lifetime is respected.

---

## 11. State Machine Patterns

### 11.1 Run Lifecycle (top-level FSM)

```
        ┌──────┐
        │ BOOT │
        └──┬───┘
           ▼
        ┌──────┐    new game      ┌────────┐
        │ TITLE │───────────────▶│ DRAFT  │  (origin + backstory + soul perks)
        └──┬───┘                  └────┬───┘
           │ load                      │
           ▼                           ▼
        ┌──────────────────────────────────────┐
        │              LIFE (YOUTH)              │
        └────┬───────────┬───────────┬───────────┘
             │           │           │
             ▼           ▼           ▼
        ┌────────┐  ┌────────┐  ┌────────┐
        │ TOWN   │  │ADVENTURE│  │ COMBAT │   ◀── nested FSMs (see below)
        └────┬───┘  └────┬───┘  └────┬───┘
             │           │           │
             └──────────┬┴───────────┘
                        │ age/stage triggers
                        ▼
                  ┌──────────────┐
                  │ QUIET_YEARS  │
                  └──────┬───────┘
                         ▼
                  ┌──────────────┐
                  │ LIFE_REVIEW  │
                  └──────┬───────┘
                         ▼
                  ┌──────────────┐
                  │ REINCARNATE  │ (spend LP → new Soul Perks)
                  └──────┬───────┘
                         ▼
                    back to YOUTH
                         │
                         ▼  (eventually player quits)
                       TITLE
```

### 11.2 Town FSM

```
TOWN: IDLE → WALKING → INTERACTING(NPC/SHOP/BUILDING) → TAB_OPEN(Character/Inventory/Perks/Quests/Shop/Map) → IDLE
```

### 11.3 Combat FSM

```
COMBAT: INTRO → SPAWNING → ACTIVE → WAVE_CLEAR_BANNER → (SPAWNING|VICTORY|DEFEAT)
        DEFEAT → death(COMBAT) → life review flow
        VICTORY → reward apply → exit to map
```

### 11.4 Narrative FSM

```
NARRATIVE: NODE_ENTERED → PAGE_ADVANCING → OPTIONS_SHOWN → OPTION_CHOSEN → EFFECTS_APPLIED → NEXT_NODE
```

State machines are implemented as `StringName` enum + `match` in `_physics_process` rather than a generic FSM library — keeps the code flat and debuggable. The only generic FSM is the top-level GameManager one, which uses a `current_mode` field guarded by `_transition_to(mode)`.

---

## 12. Performance Considerations

### 12.1 Rendering
- **Pixel-perfect**: All gameplay renders to a `SubViewport` at native pixel resolution (320×180 base, scaled 5×–6× to display). Camera snaps to integer pixels; `viewport_snap_to_pixel = true`. No sub-pixel jitter.
- **CRT shader** (optional in Settings): a `ShaderMaterial` on the upscaled ColorRect that adds scanlines + slight bloom; toggleable for accessibility.
- **YSort** for player + NPCs + enemies in town; only one YSort root per area to keep the sort O(n log n).
- **TileMap**: better-terrain addon; collision shapes baked at scene load, not per-frame.

### 12.2 Object Pooling
All short-lived combat nodes go through `ObjectPool`. Caps (combat only):
- Projectiles: 128 total across all types
- DamageText: 64 on screen, overflow drops oldest
- Hit sparks: 64

### 12.3 Reactive System
`Reactive<T>` is a thin wrapper around a value + a `changed` signal. `ComputedReactive<T>` recomputes when its source Reactives change. **Rules:**
- Never create a Reactive inside `_process`. They are owned by State singletons.
- UI binds in `_ready()` and unbinds in `_exit_tree()`. Dangling bindings leak.
- ComputedReactives must be pure — no side effects, no reads of other systems.
- For expensive computations (e.g. derived stats from 6 attributes + 7 equipment slots + 20 perks), wrap in a `ComputedReactive` and let it cache until a source changes.

### 12.4 Save Frequency
- Autosave on `day_passed` and on scene transition (not per-frame).
- Save is synchronous (JSON is small, <100KB typical). If save time exceeds 16ms once, switch to threaded `Thread.start()` with a `Mutex` on State mutation during the write — measure first.

### 12.5 Data Loading
define-it loads JSON at boot and caches as `Dictionary`. Lookups by `def_id` are O(1) hash. Hot-reload in editor only; never at runtime. All gameplay code references content via `def!item.sword_4` syntax (a `DefRef` that resolves at boot).

### 12.6 Memory Budget (target: <512MB)
| Area              | Budget     |
|-------------------|------------|
| Tilesets + sprites| ~180 MB    |
| Audio (streamed)  | ~40 MB resident |
| UI scenes         | ~30 MB     |
| State singletons  | <5 MB      |
| Combat pool       | <8 MB      |
| Misc / headroom   | remainder  |

Audio streams use `AudioStreamOggVorbis` with `loop = true` for BGM and `loop = false` for SFX; BGM is streamed from disk, SFX are loaded fully (short).

### 12.7 Frame Budget (16.6ms @ 60Hz)
| Slice                | Budget   |
|----------------------|----------|
| Combat logic         | 2 ms     |
| Projectile physics   | 1.5 ms   |
| Reactive recomputes  | 1 ms     |
| UI layout            | 2 ms     |
| Render               | 6 ms     |
| Misc / GC            | 1 ms     |
| Headroom             | 3 ms     |

If combat FPS drops below 55, first lever: reduce `spawn_cap`. Second lever: cull damage text earlier. Third lever: skip particle frames.

---

## 13. Save Data Schema (top-level)

The save file is a single JSON document. See `DATA_MODELS.md` for full per-object schemas. Top-level shape:

```jsonc
{
  "save_version": 3,
  "meta": {
    "origin_id": "origin_prisoner",
    "backstory_id": "backstory_fighter",
    "played_at": "2026-07-29T05:34:13+08:00",
    "playtime_sec": 4123,
    "lifetime_id": "01J...",
    "lives_lived": 4
  },
  "calendar_state":      { /* DATA_MODELS.md §CalendarState */ },
  "campaign_state":      { /* flags, region unlocks */ },
  "character_state":     { /* attributes, skills, level, hp, age */ },
  "inventories_state":   { /* inventory, equipment, gold */ },
  "journal_state":       { /* quests, threads, side_quests */ },
  "loot_state":          { /* pending loot tables */ },
  "meta_state":          { /* LP, legend_rank, soul_perks, heirlooms, deeds, key_bindings */ },
  "narrative_state":     { /* active web, current node */ },
  "perk_selection_state":{ /* per-life perk web picks */ },
  "run_state":           { /* run id, origin, backstory */ },
  "shop_data":           { /* per-shop stock + shortages + tiers */ },
  "tasks_state":         { /* active jobs, slots, cooldowns */ },
  "web_state":           { /* per-web node completion */ },
  "world_state":         { /* region flags, location states, npc states */ },
  "metrics":             { /* lifetime telemetry */ },
  "milestones":          { /* achievement checkmarks */ }
}
```

`save_version` is bumped on any breaking schema change. Migrators are forward-only. The current version (v3) corresponds to the v0.14.1 demo.

---

## 14. Addons

| Addon         | Path                                | Purpose                                              |
|---------------|-------------------------------------|------------------------------------------------------|
| better-terrain| `addons/better-terrain`            | TileMap terrain painting + auto-tile transitions    |
| define-it     | `addons/define-it`                  | JSON database with `def!id` references, hot-reload  |
| shelve-it     | `addons/shelve-it`                  | Save/load framework (`SaveGame`, `SaveLoadData`)    |
| console       | `addons/console`                    | In-game debug console (dev builds only)             |
| tooltip       | `addons/tooltip`                    | Hover tooltips for items, perks, abilities          |
| damage_text   | `addons/damage_text`                | Floating combat text                                 |
| FPS counter   | `addons/fps_counter`                | Debug overlay                                         |

---

## 15. Coding Conventions

- **GDScript 2.0** syntax (typed arrays, `@export`, `await`).
- File names: `snake_case.gd`; class names: `PascalCase`.
- One class per file. No implicit classes.
- `StringName` for all identifier strings (perk ids, stat ids, def ids). Plain `String` only for display text.
- `signal` declarations at the top of the file, before member vars.
- `_ready()` connects signals; `_exit_tree()` disconnects.
- `@onready` for child node references; never `get_node()` in `_process`.
- All public API on State classes goes through methods, not direct field writes.
- All combat math uses `CombatHelpers` statics — no `randf()` outside it (deterministic seeds for replays).
- Comments only for non-obvious intent. No restating code in English.
- All new systems must have an EventBus signal for every observable state change.

---

## 16. Testing & Validation

- Unit tests (GUT addon, optional): `CombatHelpers.compute_damage`, `XPUtils.xp_for_level`, `Migrators` table.
- Smoke test scene (`scenes/dev/dev_skip.scn`) — `dev_skip.gd` jumps to mid-life with preset stats for fast iteration.
- 5-minute playtest gate per START_HERE §11.
- Save migration tests: every migrator gets a fixture payload from the previous version.
- Balance validation: a `scripts/data/scaling_helpers.gd` table-driven test ensures damage grows ~10% per weapon tier.

---

## 17. Open Architectural Decisions

| Decision            | Options                                  | Current Lean |
|---------------------|------------------------------------------|--------------|
| Combat tick rate    | 30 Hz logic / 60 Hz render vs 60/60      | 60/60 (auto-battler is light) |
| Save format         | JSON vs ConfigFile vs .tres              | JSON (debuggable, migratable) |
| Narrative scripting | Custom web vs Dialogic                   | Custom web (story web needs branching) |
| Multiplayer         | None planned                            | — |
| Modding             | define-it JSON is mod-friendly by design | Open, no official support yet |
| Localization        | Godot CSV translation tables             | Plan for v1.0; English-only for demo |

---

End of `ARCHITECTURE.md`. For data shapes, see `DATA_MODELS.md`. For asset pipeline, see `ASSET_SPEC.md`.