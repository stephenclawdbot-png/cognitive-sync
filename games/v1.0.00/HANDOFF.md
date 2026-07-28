# v1.0.00 "wizdung" — Developer Handoff Document

> **Purpose:** Everything a developer needs to start building immediately. No ambiguity. No guessing.
> **Read this first:** START_HERE.md → ARCHITECTURE.md → this file → DATA_MODELS.md → BALANCE.md
> **Last updated:** 2026-07-29

---

## 0. QUICK START (5 MINUTES)

```bash
# 1. Install Godot 4.x (https://godotengine.org)
# 2. Create new project at games/v1.0.00/codebase/
# 3. Configure project settings (see Section 1 below)
# 4. Copy data/ JSON files from DATA_MODELS.md
# 5. Start building Layer 0 (see START_HERE.md Phase 0)
```

**First milestone:** Character moves in 8 directions with WASD, camera follows, simple tilemap room with walls. This should take 1-2 hours.

---

## 1. GODOT PROJECT SETTINGS

### 1.1 project.godot Configuration

```ini
[application]
config/name="wizdung"
config/description="Top-down ARPG dungeon crawler"
run/main_scene="res://scenes/MainMenu.tscn"
config/features=PackedStringArray("4.3")

[rendering]
renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
textures/canvas_textures/default_texture_filter=0

[display]
window/size/viewport_width=640
window/size/viewport_height=360
window/stretch/mode="viewport"
window/stretch/aspect="keep"
window/size/window_width_override=1280
window/size/window_height_override=720

[input]
move_up={...}  # See ARCHITECTURE.md Section 12.2

[autoload]
DataManager="*res://core/DataManager.gd"
EventBus="*res://core/EventBus.gd"
SaveSystem="*res://core/SaveSystem.gd"
GameManager="*res://core/GameManager.gd"
InputManager="*res://core/InputManager.gd"
SceneManager="*res://core/SceneManager.gd"
ObjectPool="*res://core/ObjectPool.gd"
AudioManager="*res://core/AudioManager.gd"

[physics]
common/physics_ticks_per_second=60
2d/default_gravity=0
```

### 1.2 Pixel-Perfect Checklist

- [ ] Texture filter set to NEAREST (not LINEAR)
- [ ] Renderer set to gl_compatibility (for pixel art + CRT shader)
- [ ] Viewport set to 640×360 (internal resolution)
- [ ] Window stretch mode "viewport" with "keep" aspect
- [ ] Window override: 1280×720 (2x internal resolution)
- [ ] 2D physics gravity set to 0 (top-down, no gravity)
- [ ] Snap 2D transforms to pixels enabled

---

## 2. FOLDER STRUCTURE

```
codebase/
├── project.godot
├── core/                        # Autoload singletons
│   ├── GameManager.gd
│   ├── SceneManager.gd
│   ├── SaveSystem.gd
│   ├── EventBus.gd
│   ├── InputManager.gd
│   ├── ObjectPool.gd
│   ├── AudioManager.gd
│   └── DataManager.gd
├── character/                   # Player character system
│   ├── PlayerCharacter.gd
│   ├── DexWizard.gd
│   ├── IntWizard.gd
│   ├── StrWizard.gd
│   ├── state_machine/
│   │   ├── StateMachine.gd
│   │   ├── State.gd
│   │   ├── StateIdle.gd
│   │   ├── StateWalk.gd
│   │   ├── StateAttack.gd
│   │   ├── StateDash.gd
│   │   ├── StateDeath.gd
│   │   └── StateStunned.gd
│   ├── StatsComponent.gd
│   ├── EquipmentManager.gd
│   ├── SkillManager.gd
│   ├── InventoryManager.gd
│   ├── HealthComponent.gd
│   ├── ManaComponent.gd
│   ├── StatusEffectManager.gd
│   └── AimingReticle.gd
├── combat/                      # Combat system
│   ├── Hitbox2D.gd
│   ├── Hurtbox2D.gd
│   ├── DamageCalculator.gd
│   ├── Projectile.gd
│   ├── ProjectilePool.gd
│   └── StatusEffect.gd
├── skills/                      # Skill system
│   ├── SkillTree.gd
│   ├── SkillNode.gd
│   ├── SkillBehavior.gd
│   └── behaviors/
│       ├── ProjectileBehavior.gd
│       ├── PiercingBehavior.gd
│       ├── DoubleStrikeBehavior.gd
│       ├── DashBehavior.gd
│       ├── AOEBehavior.gd
│       ├── ForkBehavior.gd
│       ├── ExplodeOnKillBehavior.gd
│       ├── ShockChanceBehavior.gd
│       ├── FrostbiteBehavior.gd
│       ├── BurnBehavior.gd
│       ├── StunBehavior.gd
│       └── CleaveBehavior.gd
├── items/                       # Item system
│   ├── ItemDefinition.gd
│   ├── ItemInstance.gd
│   ├── LootTable.gd
│   ├── RaritySystem.gd
│   └── ItemPickup.gd
├── enemies/                     # Enemy system
│   ├── EnemyBase.gd
│   ├── EnemySpawner.gd
│   ├── EnemyAI.gd
│   ├── MeleeChaseAI.gd
│   ├── RangedKiteAI.gd
│   ├── StationaryRangedAI.gd
│   └── BossAI.gd
├── dungeon/                     # Dungeon system
│   ├── DungeonGenerator.gd
│   ├── RoomSet.gd
│   ├── RoomInstance.gd
│   ├── DoorSystem.gd
│   ├── PortalSystem.gd
│   └── TilemapManager.gd
├── npc/                         # NPC system
│   ├── NPCBase.gd
│   ├── DialogSystem.gd
│   ├── DialogProfile.gd
│   └── MysteriousWizard.gd
├── ui/                          # UI system
│   ├── MainMenu.gd
│   ├── PlayerHUD.gd
│   ├── BossHealthBar.gd
│   ├── InventoryUI.gd
│   ├── EquipmentUI.gd
│   ├── SkillTreeUI.gd
│   ├── CharacterSheetUI.gd
│   ├── DialogBox.gd
│   ├── MerchantUI.gd
│   ├── StashUI.gd
│   ├── IdentifyUI.gd
│   ├── EnchantUI.gd
│   ├── PauseMenu.gd
│   ├── SettingsMenu.gd
│   ├── SaveScreen.gd
│   ├── RoomInfoUI.gd
│   ├── CombatFeedback.gd
│   ├── DamageNumber.gd
│   └── CRTShader.gd
├── scenes/                      # Scene files (.tscn)
│   ├── MainMenu.tscn
│   ├── Hub.tscn
│   ├── Dungeon.tscn
│   ├── BossRoom.tscn
│   ├── PlayerCharacter.tscn
│   ├── Enemy.tscn
│   └── rooms/                   # Room templates
│       ├── tutorial_room_01.tscn
│       ├── t1_room_01.tscn
│       └── ...
├── data/                        # JSON data files (from DATA_MODELS.md)
│   ├── stats.json
│   ├── items.json
│   ├── skills.json
│   ├── enemies.json
│   ├── levels.json
│   ├── curves.json
│   ├── npcs.json
│   └── equipment_slots.json
├── shaders/                     # Shader files
│   ├── crt.gdshader
│   ├── hit_flash.gdshader
│   └── rarity_glow.gdshader
└── sprites/                     # Sprite assets (symlink or copy from ../sprites/)
    ├── characters/
    ├── enemies/
    ├── items/
    ├── equipment/
    ├── npcs/
    ├── tiles/
    ├── vfx/
    └── ui/
```

---

## 3. IMPLEMENTATION ORDER

### Sprint 1: Foundation (Days 1-2)

| Task | File(s) | Est. Time | Done? |
|------|---------|-----------|-------|
| Create Godot project + settings | project.godot | 30 min | [ ] |
| Implement EventBus (all signals) | core/EventBus.gd | 1 hour | [ ] |
| Implement DataManager (JSON loader) | core/DataManager.gd | 2 hours | [ ] |
| Create data JSON files | data/*.json | 2 hours | [ ] |
| Implement InputManager | core/InputManager.gd | 1 hour | [ ] |
| 8-directional movement | character/PlayerCharacter.gd | 2 hours | [ ] |
| Camera follows player | scenes/Dungeon.tscn | 30 min | [ ] |
| Simple tilemap room | scenes/rooms/tutorial_room_01.tscn | 1 hour | [ ] |
| Dash ability | character/state_machine/StateDash.gd | 1 hour | [ ] |

### Sprint 2: Core Combat (Days 3-6)

| Task | File(s) | Est. Time | Done? |
|------|---------|-----------|-------|
| State machine framework | character/state_machine/*.gd | 3 hours | [ ] |
| Basic attack (projectile) | combat/Projectile.gd, ProjectilePool.gd | 3 hours | [ ] |
| Hitbox + Hurtbox system | combat/Hitbox2D.gd, Hurtbox2D.gd | 2 hours | [ ] |
| Damage calculator | combat/DamageCalculator.gd | 2 hours | [ ] |
| Health + Mana components | character/HealthComponent.gd, ManaComponent.gd | 2 hours | [ ] |
| 1 enemy with AI | enemies/EnemyBase.gd, MeleeChaseAI.gd | 4 hours | [ ] |
| Death + respawn | character/state_machine/StateDeath.gd | 1 hour | [ ] |
| Status effects (burn, shock) | combat/StatusEffect.gd | 3 hours | [ ] |
| VFX (hit spark, death) | ui/CombatFeedback.gd | 2 hours | [ ] |
| SFX integration | core/AudioManager.gd | 1 hour | [ ] |

### Sprint 3: Stats + Loot (Days 7-12)

| Task | File(s) | Est. Time | Done? |
|------|---------|-----------|-------|
| Stats component (40+ stats) | character/StatsComponent.gd | 4 hours | [ ] |
| Derived stat calculations | character/StatsComponent.gd | 2 hours | [ ] |
| Item definitions + instances | items/ItemDefinition.gd, ItemInstance.gd | 3 hours | [ ] |
| Loot table + rarity | items/LootTable.gd, RaritySystem.gd | 3 hours | [ ] |
| Item pickups | items/ItemPickup.gd | 2 hours | [ ] |
| Inventory system | character/InventoryManager.gd | 4 hours | [ ] |
| Equipment manager | character/EquipmentManager.gd | 3 hours | [ ] |
| Inventory UI | ui/InventoryUI.gd, EquipmentUI.gd | 4 hours | [ ] |
| Item tooltips + rarity frames | ui/InventoryUI.gd | 2 hours | [ ] |
| Glob pickups (HP/mana/money/XP) | items/ItemPickup.gd | 2 hours | [ ] |
| XP + leveling system | character/StatsComponent.gd | 2 hours | [ ] |

### Sprint 4: Skills + Dungeon (Days 13-20)

| Task | File(s) | Est. Time | Done? |
|------|---------|-----------|-------|
| Skill tree data structure | skills/SkillTree.gd, SkillNode.gd | 3 hours | [ ] |
| Skill behavior system | skills/SkillBehavior.gd | 2 hours | [ ] |
| 5 core behaviors | skills/behaviors/*.gd | 5 hours | [ ] |
| Skill tree UI | ui/SkillTreeUI.gd | 4 hours | [ ] |
| Room set system | dungeon/RoomSet.gd | 2 hours | [ ] |
| Room generator | dungeon/DungeonGenerator.gd | 3 hours | [ ] |
| Door system | dungeon/DoorSystem.gd | 2 hours | [ ] |
| Enemy spawner | enemies/EnemySpawner.gd | 2 hours | [ ] |
| Enemy scaling (per room level) | enemies/EnemyBase.gd | 1 hour | [ ] |
| Elite enemy variants | enemies/EnemyBase.gd | 2 hours | [ ] |
| Boss + boss health bar | enemies/BossAI.gd, ui/BossHealthBar.gd | 4 hours | [ ] |
| Portal system | dungeon/PortalSystem.gd | 1 hour | [ ] |
| Scene transitions (hub↔dungeon) | core/SceneManager.gd | 2 hours | [ ] |

### Sprint 5: Hub + NPCs + Polish (Days 21-35)

| Task | File(s) | Est. Time | Done? |
|------|---------|-----------|-------|
| Hub scene | scenes/Hub.tscn | 2 hours | [ ] |
| NPC base + dialog system | npc/NPCBase.gd, DialogSystem.gd | 4 hours | [ ] |
| Mysterious Wizard (identify) | npc/MysteriousWizard.gd, ui/IdentifyUI.gd | 3 hours | [ ] |
| Trinket Witch (enchant/sell) | ui/MerchantUI.gd, EnchantUI.gd | 4 hours | [ ] |
| Respec system | npc/MysteriousWizard.gd | 2 hours | [ ] |
| Character switch NPCs | npc/NPCBase.gd | 2 hours | [ ] |
| Stash system | ui/StashUI.gd | 2 hours | [ ] |
| Save system (JSON) | core/SaveSystem.gd | 3 hours | [ ] |
| Main menu + character select | ui/MainMenu.gd | 3 hours | [ ] |
| Pause menu + settings | ui/PauseMenu.gd, SettingsMenu.gd | 2 hours | [ ] |
| CRT shader | shaders/crt.gdshader | 1 hour | [ ] |
| Controller support | core/InputManager.gd | 2 hours | [ ] |
| 3 class skill trees (36 nodes each) | data/skills.json | 4 hours | [ ] |
| Remaining VFX + audio | scenes/*.tscn | 4 hours | [ ] |
| Playtesting + bug fixing | — | 8 hours | [ ] |

---

## 4. KEY ALGORITHMS (PSEUDOCODE)

### 4.1 8-Directional Movement

```gdscript
func _physics_process(delta):
    var input_vector = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    input_vector = input_vector.normalized()
    
    if input_vector != Vector2.ZERO:
        velocity = input_vector * movement_speed
        # Update facing direction for animations
        facing_direction = input_vector
        state_machine.change_state("walk")
    else:
        velocity = Vector2.ZERO
        state_machine.change_state("idle")
    
    move_and_slide()
```

### 4.2 Dash with I-Frames

```gdscript
func start_dash():
    is_dashing = true
    invincible = true
    dash_timer = dash_duration  # 0.3 seconds
    
    # Save dash direction (can't change mid-dash)
    dash_direction = facing_direction.normalized()
    
    # Spawn ghost trail VFX
    EventBus.spawn_vfx("dash_trail", global_position)
    
    # After dash_duration, end i-frames
    # After dash_total_time, end dash state
```

### 4.3 Damage Calculation

```gdscript
func calculate_damage(attacker_stats: Dictionary, target_stats: Dictionary) -> Dictionary:
    var base = attacker_stats.get("physical_damage", 0)
    var elemental = attacker_stats.get("fire_damage", 0) + attacker_stats.get("frost_damage", 0) + attacker_stats.get("lightning_damage", 0)
    var raw = (base + elemental) * attacker_stats.get("damage_multiplier", 1.0)
    
    # Crit check
    var is_crit = randf() < (attacker_stats.get("crit_chance", 5.0) / 100.0)
    if is_crit:
        raw *= attacker_stats.get("crit_multiplier", 1.5)
    
    # Dodge check
    if randf() < (target_stats.get("dodge", 5.0) / 100.0):
        return {"damage": 0, "dodged": true, "crit": false}
    
    # Toughness reduction
    var mitigated = max(1, raw - target_stats.get("toughness", 0))
    
    # Elemental resistance (diminishing returns)
    var avg_res = 0
    if elemental > 0:
        avg_res = (target_stats.get("fire_resistance", 0) + target_stats.get("frost_resistance", 0) + target_stats.get("lightning_resistance", 0)) / 3.0
    var effective_res = avg_res / (avg_res + 50.0)  # diminishing returns
    mitigated = mitigated * (1.0 - effective_res)
    
    # Ethereal armor
    var eth_armor = target_stats.get("ethereal_armor", 0)
    var absorbed = min(eth_armor, mitigated)
    mitigated -= absorbed
    
    return {"damage": max(1, int(mitigated)), "dodged": false, "crit": is_crit, "absorbed": absorbed}
```

### 4.4 Loot Roll

```gdscript
func roll_loot(enemy_level: int, loot_chance_mod: float, has_locked_doors: bool) -> Array:
    var drops = []
    var base_chance = 0.45 + loot_chance_mod * 0.01
    
    if randf() > base_chance:
        return drops  # No drop
    
    # Roll category
    var weights = {
        "gear": 35, "health_glob": 20, "mana_glob": 15, 
        "money_glob": 15, "xp_glob": 10, "nothing": 2
    }
    if has_locked_doors:
        weights["key"] = 3
    
    var category = weighted_random(weights)
    
    if category == "gear":
        var item = generate_item(enemy_level)
        drops.append({"type": "item", "data": item})
    elif category == "key":
        drops.append({"type": "key"})
    elif category != "nothing":
        drops.append({"type": "glob", "glob_type": category})
    
    return drops

func generate_item(level: int) -> Dictionary:
    # Pick type
    var types = ["weapon", "chest", "helmet", "boots", "ring", "necklace"]
    var item_type = types[randi() % types.size()]
    
    # Roll rarity
    var rarity = roll_rarity(level)
    
    # Generate modifiers
    var mod_count = rarities[rarity]["modifier_count"]
    var modifiers = []
    var available_mods = get_modifiers_for_type(item_type)
    
    for i in mod_count:
        var mod = available_mods[randi() % available_mods.size()]
        var range = item_modifiers[mod]
        var value = lerp(range["min"], range["max"], randf() * rarities[rarity]["roll_multiplier"])
        modifiers.append({"stat": mod, "value": value})
    
    return {
        "id": generate_uuid(),
        "type": item_type,
        "rarity": rarity,
        "identified": false,
        "modifiers": modifiers,
        "level": level
    }
```

### 4.5 Enemy AI (Melee Chase)

```gdscript
func ai_process(delta):
    match current_state:
        "idle":
            # Check aggro
            var dist = global_position.distance_to(player.global_position)
            if dist < aggro_radius:
                current_state = "chase"
        
        "chase":
            # Move toward player
            var dir = (player.global_position - global_position).normalized()
            velocity = dir * speed
            move_and_slide()
            
            # Check attack range
            var dist = global_position.distance_to(player.global_position)
            if dist < attack_range and attack_cooldown_timer <= 0:
                current_state = "attack"
            
            # Check aggro loss
            if dist > aggro_radius * 1.5:
                current_state = "idle"
        
        "attack":
            # Stop moving, play attack animation
            velocity = Vector2.ZERO
            # Spawn hitbox during attack frames
            # On attack complete → cooldown → chase
        
        "death":
            velocity = Vector2.ZERO
            # Play death animation, then queue_free
```

---

## 5. GUT TEST STUBS

```gdscript
# tests/test_damage_calculator.gd
extends GutTest

func test_basic_damage():
    var attacker = {"physical_damage": 20, "crit_chance": 0, "damage_multiplier": 1.0}
    var target = {"toughness": 5, "dodge": 0}
    var result = DamageCalculator.calculate(attacker, target)
    assert_eq(result.damage, 15)  # 20 - 5 = 15

func test_crit_doubles_damage():
    var attacker = {"physical_damage": 20, "crit_chance": 100, "crit_multiplier": 2.0, "damage_multiplier": 1.0}
    var target = {"toughness": 5, "dodge": 0}
    var result = DamageCalculator.calculate(attacker, target)
    assert_eq(result.crit, true)
    assert_eq(result.damage, 35)  # (20 * 2) - 5 = 35

func test_dodge_negates_damage():
    var attacker = {"physical_damage": 20, "crit_chance": 0, "damage_multiplier": 1.0}
    var target = {"toughness": 5, "dodge": 100}
    var result = DamageCalculator.calculate(attacker, target)
    assert_eq(result.dodged, true)
    assert_eq(result.damage, 0)

func test_minimum_damage():
    var attacker = {"physical_damage": 1, "crit_chance": 0, "damage_multiplier": 1.0}
    var target = {"toughness": 50, "dodge": 0}
    var result = DamageCalculator.calculate(attacker, target)
    assert_eq(result.damage, 1)  # max(1, 1-50) = max(1, -49) = 1
```

```gdscript
# tests/test_loot_table.gd
extends GutTest

func test_common_rarity_distribution():
    var counts = {"common": 0, "magic": 0, "rare": 0, "epic": 0, "legendary": 0}
    for i in 10000:
        var rarity = LootTable.roll_rarity(1)
        counts[rarity] += 1
    # Common should be ~58-62% at level 1
    assert_between(counts["common"], 5700, 6300)
    # Legendary should be ~1-2%
    assert_between(counts["legendary"], 50, 250)
```

---

## 6. COMMON PITFALLS & SOLUTIONS

### Pitfall 1: Projectiles causing frame drops
**Cause:** Instantiating Projectile.tscn at runtime
**Fix:** Use ProjectilePool — pre-warm 100 projectiles at startup, reuse inactive ones

### Pitfall 2: Enemy pathfinding through walls
**Cause:** Using raw `move_toward` without collision check
**Fix:** Use `NavigationAgent2D` or raycast before moving. For simple AI, raycast toward player — if blocked, try moving perpendicular

### Pitfall 3: Stats not updating after equipment change
**Cause:** Modifying base stats instead of using a modifier layer
**Fix:** StatsComponent should have: base_stats + equipment_modifiers + skill_modifiers + buff_modifiers. Recalculate total when any layer changes

### Pitfall 4: Save file corruption on crash during save
**Cause:** Writing directly to save file
**Fix:** Write to temp file first, then rename to actual save file (atomic operation)

### Pitfall 5: CRT shader tanking performance
**Cause:** Complex shader on full-screen ColorRect
**Fix:** Keep shader simple (scanlines only) for mobile. Only enable curvature + chromatic aberration on desktop. Shader should be <20 instructions

### Pitfall 6: Skill tree node dependencies not enforced
**Cause:** Player allocates node without prerequisites
**Fix:** Validate prerequisites in SkillTree.allocate_node() — check all prerequisite nodes are allocated before allowing allocation

### Pitfall 7: Inventory items lost on class switch
**Cause:** Clearing inventory on switch
**Fix:** Class switch only changes active class + equipped items. Inventory and stash persist. Store current class's equipment in save data per class

---

## 7. DEFINITION OF DONE

### Phase 0 Done When:
- [ ] Character moves in 8 directions with WASD
- [ ] Dash works with i-frames (0.3s)
- [ ] Camera follows player, clamped to room
- [ ] Tilemap room with wall collision
- [ ] Aiming reticle follows mouse

### Phase 1 Done When:
- [ ] Basic attack fires projectile in facing direction
- [ ] 1 enemy chases player and attacks on cooldown
- [ ] Player and enemy have health, can take damage, can die
- [ ] Damage numbers appear on hit
- [ ] Crit system works (random chance, multiplier, visual feedback)
- [ ] Mana system (attack costs mana, mana regenerates)
- [ ] Status effects apply (burn, shock) and tick damage
- [ ] Hit VFX and SFX play on hit
- [ ] Death animation + respawn/return to hub

### Phase 2 Done When:
- [ ] 40+ stats all functional with derived calculations
- [ ] Enemies drop loot (gear, globs, keys)
- [ ] Inventory opens, items can be moved/equipped
- [ ] Equipment changes stats (equip weapon → damage increases)
- [ ] 5 rarity tiers with colored frames in UI
- [ ] Unidentified items show "?" until identified
- [ ] Skill tree UI shows nodes, can spend points
- [ ] 9 skill nodes in one sub-tree work and modify attacks
- [ ] Glob pickups (health, mana, money, XP) with VFX + sound
- [ ] XP system: gain XP → level up → earn skill point

### Phase 3 Done When:
- [ ] Full skill tree (36 nodes per class, 4 sub-trees)
- [ ] 26+ skill behaviors functional
- [ ] 3 enemy types with distinct AI (melee, ranged, boss)
- [ ] Enemy scaling per room level works
- [ ] Elite enemies spawn with higher stats + color tint
- [ ] Room generation picks from room set, populates enemies
- [ ] Door system (locked doors need keys)
- [ ] Key drops from designated enemy
- [ ] Boss room with boss + boss health bar
- [ ] Portal system (enter dungeon from hub, return to hub)
- [ ] 2+ tilesets (base dungeon + alternate)

### Phase 4 Done When:
- [ ] Hub area with all NPCs placed
- [ ] Mysterious Wizard identifies items (pay gold → reveal stats)
- [ ] Trinket Witch enchants (pay gold → add modifier) and buys items
- [ ] Respec works (pay gold → reset tree → refund points)
- [ ] Character switch via NPC dialog
- [ ] Stash system stores items shared between classes
- [ ] 3 playable classes with unique skill trees
- [ ] Main menu + character select
- [ ] Pause menu + settings + save screen
- [ ] CRT shader toggle in settings
- [ ] Controller support (all actions mapped)
- [ ] Save/load works (all state persisted)
- [ ] Tutorial NPC explains controls
- [ ] Room info display (level, enemies remaining)
- [ ] 20+ VFX, 18+ SFX, 3+ music tracks
- [ ] No crash bugs in 30-minute play session

---

## 8. CONTACT & REFERENCES

| Resource | Location |
|----------|----------|
| Game mechanics | games/v1.0.00/GAME_MECHANICS.md |
| Economy | games/v1.0.00/ECONOMY.md |
| Build guide | games/v1.0.00/START_HERE.md |
| Architecture | games/v1.0.00/ARCHITECTURE.md |
| Data models | games/v1.0.00/DATA_MODELS.md |
| Balance | games/v1.0.00/BALANCE.md |
| Level design | games/v1.0.00/LEVEL_DESIGN.md |
| Asset spec | games/v1.0.00/ASSET_SPEC.md |
| Sprite manifest | games/v1.0.00/sprites/SPRITE_MANIFEST.md |
| Raw extracted data | games/v1.0.00/raw-data/ |
| Godot docs | https://docs.godotengine.org/en/stable/ |
| GUT (testing) | https://github.com/bitwes/Gut |

---

## 9. CHANGELOG

| Date | Change |
|------|--------|
| 2026-07-29 | Initial handoff document created |