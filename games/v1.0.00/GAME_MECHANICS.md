# v1.0.00 — Game Mechanics Document

**Engine:** Godot 4.6.1  
**Genre:** Action RPG / Dungeon Crawler (top-down, 8-directional)  
**Code Status:** PCK encrypted (flags=2), GDScript compiled to bytecode — analysis via string extraction  
**Total Assets:** 152 scripts, 106 scenes, 401 resources, 353 sprites, 27 audio files, 4 shaders, 1 font  

---

## 1. Character Classes

### 1.1 Playable Classes (3)

The game features three wizard classes, each with a unique skill tree. Players can switch between classes in the hub by talking to NPC versions of the other classes.

#### Dex Wizard (Agility)
- **Sprite:** `character_dex_wizard_spritesheet.png` (8-directional)
- **Scene:** `Agility_Wizard.tscn`
- **Primary Damage:** Lightning + Physical
- **Starting Items:** Agility Weapon, Wisdom Weapon, Cloth Armor, Worn Boots, Rusty Key
- **Playstyle:** Fast, mobile, projectile-based with shuriken attacks and dash-based movement

#### Int Wizard (Wisdom)
- **Sprite:** `character_int_wizard_spritesheet.png` (8-directional)
- **Primary Damage:** Frost
- **Abilities:** Ethereal Shield, Icey Shards, Teleport (Blink)
- **Playstyle:** Area control with frost effects, crowd control via frostbite, teleport-based mobility

#### Str Wizard (Power)
- **Sprite:** `character_str_wizard_spritesheet.png` (8-directional)
- **Primary Damage:** Physical
- **Playstyle:** Tanky, high health, melee-oriented (skill tree data not fully extracted — likely incomplete in this build)

### 1.2 Character Switch System
- Talk to NPC versions of other classes in the hub area
- NPC_Dex_Wizard: "Can you take over?" / "You look tired. Would you like me to take over?"
- NPC_Int_Wizard: Similar swap dialog
- NPC_Str_Wizard: "Puny Wizard begon, I'm busy right now." (initially dismissive)
- Dialog response type: `Character_Change_Response`
- Character portraits: `Character_Portrait_Dex_Wizard_Square.png`, `Character_portrait_int_wizard_square.png`, `Character_Portraite_Str_Wizard_Square.png`

### 1.3 Character State Machine
All characters use a state machine with these states:
- `State_Idle` — Default non-combat state
- `State_Walk` — Movement state
- `State_Attack` — Attacking (includes 8-directional: DashAttack_Down/Right/Up/Left/DownLeft/DownRight/UpRight/UpLeft)
- `State_Death` — Death animation/state
- `State_Stunned` — Stunned by enemy attacks

---

## 2. Stats System

### 2.1 Core Attributes

| Stat | Effect | Notes |
|------|--------|-------|
| **Power** | Increases health total | Primary attribute for Str Wizard |
| **Swiftness** | Increases Toughness and Max Life | Defensive scaling |
| **Wisdom** | Increases Max Mana and Ethereal Shield | Primary attribute for Int Wizard |
| **Toughness** | Reduces incoming physical damage | Damage mitigation |
| **Dexterity** | Increases Dodge and Accuracy | Primary attribute for Dex Wizard |
| **Accuracy** | Chance to hit, contested against dodge | Offensive utility |

### 2.2 Offensive Stats

| Stat | Description |
|------|-------------|
| Physical Damage | Base physical damage |
| Fire Damage | Fire elemental damage |
| Frost Damage | Frost elemental damage |
| Lightning Damage | Lightning elemental damage |
| Critical Strike Chance | Chance to land critical hit |
| Critical Strike Multiplier | Multiplier applied on critical hit |
| Attack Speed | Melee attack speed |
| Cast Speed | Spell casting speed |
| Multiple Projectiles | Number of projectiles fired |
| Piercing | Number of times projectiles pierce enemies |
| Fire Penetration | Bypasses fire resistance |
| Frost Penetration | Bypasses frost resistance |
| Lightning Penetration | Bypasses lightning resistance |

### 2.3 Defensive Stats

| Stat | Description |
|------|-------------|
| Max Life | Maximum health |
| Current Life | Current available life |
| Max Mana | Maximum mana |
| Current Mana | Current available mana |
| Life Regen | Life regeneration rate |
| Mana Regen | Mana regeneration rate |
| Mana Cost Reduction | Reduces mana cost of skills |
| Ethereal Armor | Magic shield (separate from health) |
| Current Ethereal Armor | Active ethereal armor value |
| Dodge | Chance for incoming damage to miss |
| Fire Resistance | Reduces fire damage received |
| Frost Resistance | Reduces frost damage received |
| Lightning Resistance | Reduces lightning damage received |
| Dash Distance | Increases dash distance |
| Movement Speed | Movement speed |

### 2.4 Status-Related Stats

| Element | Effect Chance | Effect Duration | Resistance |
|---------|---------------|-----------------|------------|
| Fire | Burn Chance | Burn Duration | Burn Resistance |
| Frost | Frostbite Chance | Frostbite Duration | Frostbite Resistance |
| Lightning | Shock Chance | — | Shock Resistance |
| Physical | Stun Chance | Stun Duration | Stun Resistance |

### 2.5 Room Modifier Stats

| Stat | Effect |
|------|--------|
| Monster Rarity | Increases chance for magic and rare monsters to spawn |
| Pack Size | Increases monster pack size |
| Portal Spawn Chance | Increases NPC spawn chance in rooms |
| Increased Boss Spawns | Increases number of bosses in boss rooms |

### 2.6 Stat Scaling Curves
- `Health_Per_Level_Curve` — Health scaling per level
- `Mana_Per_Level_Curve` — Mana scaling per level
- `Power_Curve` — Power stat scaling
- `Wisdom_Curve` — Wisdom stat scaling
- `Swiftness_Curve` — Swiftness stat scaling
- `Accuracy_Per_Level_Curve` — Accuracy scaling per level
- `Diminishing_Return_Curve` — Diminishing returns formula
- `XP_Curve` — XP required per level
- `Level_Up_Curve` — Level-up progression curve
- `curve_ability_point_distribution` — Ability point distribution curve
- `curve_xp` — XP curve (character resources)

---

## 3. Skill System

### 3.1 Skill Tree Architecture

Each class has 4 skill sub-trees, each with 9 nodes (36 nodes per class total):

**Sub-trees per class:**
1. **Basic Attack** — Modifies the primary attack
2. **Movement** — Modifies dash/movement skill
3. **Passive Tree** — Passive bonuses
4. **Special Attack** — Modifies the special attack skill

### 3.2 Agility (Dex Wizard) Skill Tree

#### Basic Attack (QuickStrike)
| Node # | Name | Effect |
|--------|------|--------|
| 001 | Projectile | Basic attack becomes projectile-based |
| 002 | ProjectileSpeed | Increased projectile speed |
| 003 | Piercing | Projectiles pierce enemies |
| 004 | DoubleStrike | Attack hits twice |
| 005 | SpeedOfTheWind | Attack speed bonus |
| 006 | ShreddingWinds | Shredding wind effect |
| 007 | ThunderousCrackling | Lightning crackling effect |
| 008 | CullingThunder | Culling strike (execute) |
| 009 | ExplodeOnKill | Enemies explode on death |

**Behaviors:**
- QuickAttack base behavior
- ChanceToShock — Adds shock chance to attacks
- ChanceTriggerTwice — Chance to trigger attack twice
- DextoPhys — Converts Dexterity to Physical damage
- Frenzy_AttackSpeed — Frenzy attack speed buff
- Frenzy_MovementSpeed — Frenzy movement speed buff
- PhysicalDamageMult — Physical damage multiplier
- PhysicalToLightning — Converts physical to lightning damage

**Skill Modifiers:**
- CullingThunder, ExplosiveThundershock, PiercingStrike, ShreddingWinds, SonicStrike, StikingSpeed, TempestSpeed, ThunderousCrackling

#### Movement (Dash)
| Node # | Name | Effect |
|--------|------|--------|
| 001 | DashDistance | Increased dash distance |
| 002 | DashSpeed | Increased dash speed |
| 003 | Intangible | I-frames during dash |
| 004 | CracklingReflexes | Shock effect on dash |
| 005 | Momentum | Momentum bonus |
| 006 | MomentumDamage | Damage increases with momentum |
| 007 | IncreasedDamage | General damage increase |
| 008 | ShockingPath | Leaves shocking ground |
| 009 | BonusShockChanceAfterDash | Bonus shock chance post-dash |

#### Passive Tree
| Node # | Name | Effect |
|--------|------|--------|
| 001 | LightningDamage | Increased lightning damage |
| 002 | ShockChance | Increased shock chance |
| 003 | ShockTwice | Shock triggers twice |
| 004 | PhysicalDamage | Increased physical damage |
| 005 | StunChance | Increased stun chance |
| 006 | ToughnessReduction | Reduces enemy toughness |
| 007 | DodgeChance | Increased dodge chance |
| 008 | IncreasedDexterity | +Dexterity |
| 009 | CritChanceOnDodge | Crit chance after dodging |

#### Special Attack (Shuriken)
| Node # | Name | Effect |
|--------|------|--------|
| 001 | MultipleProjectiles | Additional shuriken projectiles |
| 002 | Piercing | Shurikens pierce |
| 003 | ForkingShuriken | Shurikens fork on hit |
| 004 | SwirlingWinds | Swirling shuriken pattern |
| 005 | ForceOfAHurricane | Hurricane force attack |
| 006 | GiantShurikens | Larger shurikens |
| 007 | LeechingLightning | Life/mana leech on lightning |
| 008 | StormShurikens | Storm-infused shurikens |
| 009 | ShockingShurikens | Shock-infused shurikens |

**Special Attack Behaviors:**
- BaseProjectile, ForkingShurikens, MultipleProjectiles (1 & 2), Orbital, ShockingShurikens
- Orbital behavior: shurikens orbit the player

### 3.3 Wisdom (Int Wizard) Skill Tree

#### Basic Attack
| Node # | Name | Effect |
|--------|------|--------|
| 001 | KnockBack | Basic attack knocks back enemies |
| 002 | CastingSpeed | Increased cast speed |
| 003 | IncreasedChannelDuration | Longer channel duration |
| 004 | IncreasedSize | Larger attack hitbox |
| 005 | CircleOfCold | 360-degree cold attack |
| 006 | ExplodeDeath | Enemies explode on death |
| 007 | FrostbiteChance | Chance to apply frostbite |
| 008 | FrostbiteDuration | Longer frostbite duration |
| 009 | IceyTouch | Icey touch effect |

**Behaviors:**
- Wisdom_BasicAttack_Behavior (base)
- Wisdom_BasicAttack_360_Behavior (360-degree variant)
- 360ConeOfCold projectile

#### Movement (Blink/Teleport)
| Node # | Name | Effect |
|--------|------|--------|
| 001 | DashDistance | Blink distance |
| 002 | MovementSpeed | Movement speed |
| 003 | ManaRegen | Mana regeneration |
| 004 | FrostDamage | Frost damage bonus |
| 005 | FrostedGround | Leaves frosted ground |
| 006 | IncreasedFrostDamage | More frost damage |
| 007 | ExplodeOnTeleport | Explosion at departure |
| 008 | IncreasedArea | Larger area |
| 009 | ExplodeOnTeleportLand | Explosion at arrival |

#### Passive Tree
| Node # | Name | Effect |
|--------|------|--------|
| 001-009 | Wisdom_Passive_001 through 009 | Passive frost/wisdom bonuses |

#### Special Attack (Icey Shards / Cone of Cold)
| Node # | Name | Effect |
|--------|------|--------|
| 001 | GreaterArea | Larger area of effect |
| 002 | InsightOnHit | Insight buff on hit |
| 003 | InsightDamage | Damage from insight |
| 004 | IncreasedDuration | Longer duration |
| 005 | IceyShardExplosion | Shards explode |
| 006 | ChanneledIce | Channeled ice attack |
| 007 | IncreasedShards | More shards |
| 008 | IncreasedShards | Even more shards |
| 009 | IceOnDeath | Ice effect on enemy death |

### 3.4 Skill Behaviors (Shared)

All skills use a modular behavior system:

| Behavior | Description |
|----------|-------------|
| AOE_HitBehavior | Area-of-effect hit detection |
| Aoe_At_Location_Behavior | AOE at target location |
| Chance_Behavior | Probability-based effect |
| Channel_Behavior | Channeled ability |
| Channel_Modifier_Over_Time_Behavior | Channel with stacking modifier |
| Conditional_Check_Behavior | Conditional trigger |
| Conversion_Damage_Behavior | Damage type conversion |
| Culling_Strike_Behavior | Execute low-HP enemies |
| Damage_Mult_ConditionalStatus_Behavior | Damage multiplier vs status'd enemies |
| Damage_Scalar_Behavior | Scaled damage |
| Dash_Behavior | Dash movement |
| Duration_Behavior | Timed effect |
| During_Damage_Behavior | On-damage trigger |
| I-Frame_Behavior | Invincibility frames |
| KnockBack_OnHit_Behavior | Knockback on hit |
| Leech_Behavior | Life/mana leech |
| Melee_Hitbox_Behavior | Melee hitbox |
| Momentum_DamageIncrease_Behavior | Damage scales with momentum |
| Multiply_Damage_Behavior | Damage multiplication |
| Projectile_Behavior | Projectile firing |
| Projectile_OnHit_Behavior | Projectile on-hit effect |
| Remove_Effect_Behavior | Remove status effect |
| Shock_Behavior | Shock status application |
| Spawn_Portal_Behavior | Spawn portal |
| Status_Effect_Behavior | Apply status effect |
| Trigger_Twice_Behavior | Trigger skill twice |

### 3.5 Skill Modifiers (Shared)

| Modifier | Scope |
|----------|-------|
| Stat_All_Behavior | All skills |
| Stat_BasicAttack_Behavior | Basic attack only |
| Stat_Movement_Behavior | Movement skill only |
| Stat_Passive_Behavior | Passive only |
| Stat_SpecialAttack_Behavior | Special attack only |
| Stat_Global_Projectile_Count | All projectiles |
| Stat_Global_Projectile_Speed | All projectiles |
| Stat_Global_Projectile_Size | All projectiles |
| Stat_Global_Piercing | All projectiles |
| Stat_BasicAttack_Projectile_Count | Basic attack projectiles |
| Stat_BasicAttack_Projectile_Speed | Basic attack projectile speed |
| Stat_BasicAttack_Projectile_Size | Basic attack projectile size |
| Stat_BasicAttack_Piercing | Basic attack piercing |
| Stat_SpecialAttack_Projectile_Count | Special projectiles |
| Stat_SpecialAttack_Projectile_Speed | Special projectile speed |
| Stat_SpecialAttack_Projectile_Size | Special projectile size |
| Stat_SpecialAttack_Piercing | Special piercing |
| Stat_SpecialAttack_Duration | Special duration |
| Stat_All_DodgeSkill | Dodge skill modifier |
| Stat_Life_Leech_Stat | Life leech |
| Stat_Mana_Leech_Stat | Mana leech |

### 3.6 Damage Types
- **Physical** — Can stun, reduced by Toughness
- **Fire** — Can burn (DoT), has penetration
- **Frost** — Can frostbite (slow/freeze), has penetration
- **Lightning** — Can shock (AoE chain), has penetration
- **Damage Conversion** — Physical→Lightning, Dexterity→Physical

### 3.7 Status Effects
| Status | Source | Effect |
|--------|--------|--------|
| Burn | Fire damage | Damage over time |
| Frostbite | Frost damage | Slow/freeze |
| Shock | Lightning damage | AoE spread damage |
| Stun | Physical damage | Disables enemy |
| Freeze | Frost (special) | Complete immobilization |
| Ethereal Armor | Wisdom skill | Absorbs damage before health |

---

## 4. Item System

### 4.1 Item Types

| Slot | Variants |
|------|----------|
| Weapon | Agility Weapon, Power Weapon, Wisdom Weapon |
| Chest | Cloth Robe, Leather Chest, Plate Chest |
| Helmet | Cloth Hat, Leather Hood, Plate Helmet |
| Boots | Cloth Boots, Leather Boots, Plate Boots |
| Ring | Emerald Ring (Agility), Ruby Ring (Power), Sapphire Ring (Wisdom) |
| Necklace | Emerald Necklace (Agility), Ruby Necklace (Power), Sapphire Necklace (Wisdom) |
| Key | Rusty Key, Room Key, Rune Keys 001-004 |

### 4.2 Item Rarity Tiers

| Rarity | Frame Color |
|--------|-------------|
| Common | Grey |
| Magic | Blue |
| Rare | Yellow |
| Epic | Purple |
| Legendary | Orange/Legendary |
| Unidentified | Special icon (requires identification) |

### 4.3 Item Stat Modifier Sets

**T1 Modifier Categories:**
| Set | Stats | Range |
|-----|-------|-------|
| Core_Attribute | Power, Swiftness, Wisdom | 1-5 |
| Core_LifeAndMana | Life and Mana | 1-15 |
| Defensive_Core | Toughness, Dodge, Ethereal Armor | 1-10 |
| Defensive_Resistances | Elemental resistances | — |
| Offensive_Crit | Critical chance | 1-5 |
| Offensive_Damage | Damage | 1-10 |
| Offensive_DebuffChance | Status effect chances | — |
| Offensive_Pen | Elemental penetration | — |
| Offensive_Speed | Attack/Cast speed | — |
| Offensive_Misc | Miscellaneous offensive | — |
| Utility_Movement | Movement speed | — |

**Simplified Sets:**
- Core_Attributes, Core_Ability_Modifiers
- Defensive_Core, Defensive_Elemental, Defensive_Life
- Offensive_Core, Offensive_Misc
- Utility_Mana, Utility_Movement, Utility_Room_BonusDamage

### 4.4 Item Curves
- `item_base_stat_scalar` — Base stat scaling
- `item_core_stat_scalar` — Core stat scaling
- `item_regeneration_curve` — Regen stat scaling
- `item_room_curve` — Room-based item scaling
- `modifier_curve` — General modifier scaling

### 4.5 Starting Items (Agility Class)
- Starting Agility Weapon
- Starting Wisdom Weapon
- Starting Armor (Cloth)
- Starting Boots (Worn Boots)
- Starting Key (Rusty Key)

### 4.6 Equipment System
- **Equipment Manager** — Manages equipped items
- **Inventory Manager** — Manages inventory slots
- 6 equipment slots: Weapon, Chest, Helmet, Boots, Ring, Necklace
- UI shows empty slot icons for each type
- Tooltip comparison system (shows current vs. new item stats)
- "Your Inventory is Full" message when inventory is full

---

## 5. Enemy System

### 5.1 Enemy Types

#### Melee Skeleton
- **Sprite:** `character_skeleton_enemy-Sheet.png`
- **Attack:** `Skill_Enemy_Skeleton_BasicAttack`
- **Sound:** `Skeleton_Charge.wav`
- **AI:** Melee chase + attack
- **Scalable stats:** Damage, Life, Toughness, Dodge, Elite variants

#### Wizard Mimic
- **Sprite:** `character_wizard_mimic_enemy-Sheet.png`
- **Attack:** `Skill_Enemy_MimicWizard_ArcaneBolt`
- **Projectile:** `ability_wizard_mimic_projectile-Sheet.png`
- **Sound:** `Mimic_Charge.wav`
- **Special:** Has ethereal armor
- **AI:** Ranged spellcaster

#### Dungeon Boss
- **Sprite:** `character_boss_dungeon_floor-Sheet.png`
- **Attack:** `Skill_Enemy_DungeonBoss_BasicAttack`
- **UI:** Boss health bar (separate from regular enemy health bar)
- **Boss rooms:** Level_Boss_A, Level_Boss_B

### 5.2 Enemy AI System
- **AI Controller** (`ai_controller.gd`) — Central AI management
- **Enemy Movement** (`EnemyMovement.gd`) — Pathfinding/movement
- **Aggro Radius** (`Aggro_Radius.gd`) — Detection range
- **Group Aggro Radius** (`Group_aggro_radius.gd`) — Group-based detection
- **State Machine:** Idle → Walk → Attack → Stunned → Death
- **Enemy Rank** — Normal/Elite/Boss classification
- **Boss Enemy flag** — Special boss behavior

### 5.3 Enemy Scaling System
Enemy stats scale with room level and difficulty:

| Scalar | Effect |
|--------|--------|
| EnemyScalar_Life | Enemy health |
| EnemyScalar_Damage | Enemy damage |
| EnemyScalar_Toughness | Enemy damage reduction |
| EnemyScalar_Dodge | Enemy dodge chance |
| EnemyScalar_Elite_Life | Elite enemy health bonus |
| EnemyScalar_Elite_Damage | Elite enemy damage bonus |
| EnemyScalar_EtherialArmor | Enemy ethereal armor |

### 5.4 Spawn System
- Multiple EnemySpawn nodes per room (EnemySpawn through EnemySpawn61+)
- `pack_size_spawn_chance` — Curve controlling pack size probability
- `rarity_spawn_chance` — Curve controlling monster rarity probability
- `Pack_Size_Level_Curve` — Pack size scales with level
- `min_rarity` / `max_rarity` — Rarity bounds per room
- `portal_spawn_chance_override` — Override NPC spawn chance

---

## 6. Dungeon / Level System

### 6.1 Level Structure

| Level | Type |
|-------|------|
| Level_Tutorial_01, 02 | Tutorial |
| Level_0_A | Starting level |
| Level_1_A through Level_4_A | Main progression |
| Level_B_1, Level_B_2 | Alternate path |
| Level_Boss_A, Level_Boss_B | Boss encounters |
| Test_Cave_Scene | Test/debug |

### 6.2 Room Sets

| Room Set | Use |
|----------|-----|
| Tutorial_01_RoomSet | Tutorial rooms |
| T1_RoomSet | Tier 1 rooms |
| T2_RoomSet | Tier 2 rooms |
| Endgame_RoomSet | Endgame rooms |
| Hub_Roomset | Hub area rooms |

Each Room Set contains:
- `possible_rooms` — List of room templates
- `possible_boss_rooms` — List of boss room templates
- `TileMap_Template` (1-25) — Room layout templates

### 6.3 Tilesets

| Tileset | Style |
|---------|-------|
| Base_Dungeon_Tileset | Standard dungeon |
| Base_Dungeon_Tileset_New | Updated dungeon |
| Dungeon_Tileset | Alternative dungeon |
| Alternate_Dungeon_Tileset | Alternate visual style |
| Base_Dungeon_Floor_Tileset | Floor tiles |
| Dungeon-Cave | Cave variant |
| Dungeon-Overgrown | Overgrown variant |
| Desert_Dungeon_Tileset_Animations | Desert theme |

**Floor Types:**
- Base_Floor
- Floor_Grunge (01-13) — Various floor variations

### 6.4 Room Features
- **Room Level** — "Determines the Level of Enemies in the Room"
- **Doors** — `Door_Interactable` with `door_transitions`, some require keys (`needs_key`)
- **Portal** — `Home_Portal` for returning to hub
- **Projectile_Blockers** — Walls that block projectiles
- **Floor_Lighting** — Ambient lighting
- **Door_Light** — Light around doors
- **UnderFloor** — Below-floor layer
- **Offering** — Room offering system (sacrifice for bonuses?)

### 6.5 Hub Area
- Central safe zone with NPCs
- Home Portal to return to hub from dungeons
- Confirmation: "Are you sure you want to return to the hub area?"
- Warning: "Abandon run and return to the hub? Non-permanent room level progress will be lost"
- Stash (Treasure Chest) for item storage
- NPC interactions for services

---

## 7. NPC System

### 7.1 Mysterious Wizard (Djorbgripper)
- **Sprite:** `character_djorbgripper-Sheet.png`
- **Portrait:** `Character_Portrait_Wizard.png`
- **Location:** Hub area
- **Dialog:**
  - "Ive grown too old to fight the monsters that dwell beyond the doorway."
  - "I've been here a long time, so if you need anything"
  - "Going through portals like the one that brough you here seems to do the trick to settle it just fine."
  - "I would wish you luck, but i expect to see you back here again soon."
  - "My eyes arent as keen as they used to be, but I can still identify what others overlook."
- **Services:**
  - **Identify Items** — Reveals unidentified items
  - **Respec** — Reset skill tree (refund skill points)

### 7.2 Trinket Witch (Merchant)
- **Sprite:** `character_witchmerchent-Sheet.png`
- **Portrait:** `Character_Portrait_Witch.png`
- **Location:** Hub area
- **Dialog:**
  - "oho, hello there!"
  - "you know what a new face means kitty, new profits!"
  - "what trinkets have you dragged up today? Or shall I work my magic on one of your goodies?"
- **Services:**
  - **Enchant Items** — Add modifiers to items
  - **Sell Items** — Sell unwanted gear

### 7.3 Character Select NPCs
- NPC_Dex_Wizard, NPC_Int_Wizard, NPC_Str_Wizard
- Located in hub area
- Talk to switch playable character
- Dialog conditions: `dialog_condition_talked_to_merchant`, `dialog_condition_talked_to_wizard`

### 7.4 Instruction Man
- Tutorial NPC
- Scene: `instruction_man.tscn`
- Provides tutorial guidance

### 7.5 Dialog System
- `dialog_profile` — NPC dialog configuration
- `dialog_set` — Set of dialog options
- `dialog_text` — Individual dialog lines
- `dialog_condition` — Conditions for dialog availability
- **Response Types:**
  - `Character_Change_Response` — Switch character
  - `Enchantment_UI_Response` — Open enchantment UI
  - `Identify_Items_Response` — Identify items
  - `Respec_Response` — Respec skill tree
  - `Spoke_to_Merchant_Response` — Track merchant interaction
  - `Spoke_to_Wizard_Response` — Track wizard interaction

---

## 8. Loot System

### 8.1 Loot Table Structure
```
Loot_Table:
  chance_to_drop_gear: float
  key_list: [Key definitions]
  chance_to_drop_key: float
  chance_to_drop_glob: float
  money_glob: Resource
```

### 8.2 Loot Curves
- `Money_Curve` — Money drop scaling
- `XP_Curve` — XP drop scaling
- `Number_Of_Drops_Math` — Drop count calculation
- `loot_chance_increase` — Bonus loot chance

### 8.3 Glob Pickups
| Glob | Effect | VFX |
|------|--------|-----|
| Health_Glob | Restores life | VFX_HealthGlob |
| Mana_Glob | Restores mana | VFX_ManaGlob |
| Currency_glob | Gives money | VFX_MunnyGlob |
| XP_glob | Gives experience | VFX_XPGlob |

Each glob has pickup FX sprites and sounds.

### 8.4 Loot Interaction
- Loot drops as interactable objects on the ground
- `loot_Interactable.gd` handles pickup
- "Your Inventory is Full" message when can't pick up
- Loot sprite visible on ground

---

## 9. Progression System

### 9.1 Experience & Leveling
- XP gained from kills (XP orbs) and XP globs
- `XP_Curve` and `Level_Up_Curve` determine progression
- `curve_xp` and `curve_ability_point_distribution` for character resources
- Level up triggers sound effect and VFX

### 9.2 Skill Points
- Earned through leveling
- Spent on skill tree nodes
- Can be refunded via respec (talk to Mysterious Wizard)

### 9.3 Item Identification
- Some items drop unidentified (Unidentified_Item.png icon)
- Talk to Mysterious Wizard in hub to identify
- Identification reveals item stats and rarity

### 9.4 Enchanting
- Talk to Trinket Witch to enchant items
- Reroll system with yes/no sound feedback
- Adds modifiers to existing items

---

## 10. Combat System

### 10.1 Attack Types
- **Basic Attack** — Primary attack (class-specific, mana-cost or free)
- **Special Attack** — Powerful attack with mana cost
- **Movement/Dash** — Defensive movement with i-frames
- **Passive** — Always-active bonuses

### 10.2 Damage Calculation
```
base_damage = skill_base_damage × stat_multiplier
final_damage = base_damage × (1 + crit_chance × crit_multiplier) × damage_conversion
mitigated_damage = final_damage × (1 - resistance) × (1 - toughness_reduction)
```

### 10.3 Damage Conversion
- Physical → Lightning (Agility skill)
- Dexterity → Physical (Agility skill)
- Supports multi-step conversion chains

### 10.4 Combat Feedback
- `UI_Combat_Crit` — Critical hit indicator
- `VFX_Crit_Buff` — Critical buff visual
- `VFX_Ghost_Trail` — Movement ghost trail
- Damage numbers (implied by VFX system)
- Hit sound effect
- Death sound effect

### 10.5 Aiming System
- `Aiming_Reticle` — Visual aiming reticle
- 8-directional attack system
- `DashAttack` with 8 directional variants
- Projectile direction based on facing

---

## 11. UI System

### 11.1 Main Menu
- `main_menu.tscn` — Main menu
- `start_menu.tscn` — Start menu
- Character selection
- Settings (keyboard + controller)

### 11.2 In-Game UI
| UI Element | Scene |
|------------|-------|
| Player HUD | `Player_Hud.tscn` |
| Boss Health Bar | `Boss_HealthBar.tscn` |
| Enemy Health Bar | `Enemy_Health_Bar.png` |
| Inventory | `UI_Inventory.tscn` |
| Equipment Slots | `ui_equipment_slot.tscn` |
| Tooltip | `UI_Tooltip.tscn` |
| Tooltip Compare | `UI_Tooltip_Compare.tscn` |
| Skill Tree | `UI_Skill_Tree.tscn` |
| Skill Tree Page | `UI_Skill_Tree_Page.tscn` |
| Character Sheet | `character_sheet.tscn` |
| Settings | `UI_Settings.tscn` |
| Pause Menu | `pause_menu.tscn` |
| Save Screen | `Save_Screen.tscn` |
| Dialog Box | `dialog_box.tscn` |
| Room Info | `room_information.tscn` |
| Key UI | `Key_UI.tscn` / `New_Key_UI.tscn` |
| Merchant Screen | `merchant_screen.tscn` |
| Stash UI | `Stash_UI.tscn` |
| Are You Sure | `are_you_sure.tscn` |
| Skill Icon | `skill_icon.tscn` / `ability_icon.tscn` |
| Stat Label | `stat_label.tscn` |
| Pickup Sprite | `Pickup_Sprite.tscn` |

### 11.3 Visual Effects
- **CRT Shader** — Retro CRT screen effect overlay
- **Custom Cursor** — Custom game cursor
- **Pixel Font** — `PixelFont1.ttf` for pixel-art aesthetic

### 11.4 Control Schemes
- **Keyboard** — Keyboard + mouse controls
- **Controller** — Gamepad support with `controller_controls_container`
- UI shows different control hints based on active input method
- `Keyboard_asset` and `controller_asset` UI elements

---

## 12. VFX System

| VFX | Purpose |
|-----|---------|
| VFX_Crit_Buff | Critical hit buff visual |
| VFX_Defense_Resistance | Defense/resistance visual |
| VFX_Explosion | Generic explosion |
| VFX_Freeze | Freeze status effect |
| VFX_Frost_Damage | Frost damage hit |
| VFX_Ghost_Trail | Movement ghost trail |
| VFX_HealthGlob | Health glob pickup |
| VFX_IceExplosion | Ice explosion |
| VFX_Iceicle | Ice shard projectile |
| VFX_Lightning | Lightning effect |
| VFX_Lightning_Damage | Lightning damage hit |
| VFX_ManaGlob | Mana glob pickup |
| VFX_ManaRegen | Mana regeneration |
| VFX_MovementSpeed | Movement speed buff |
| VFX_MovementandAttackSpeed | Combined speed buff |
| VFX_MunnyGlob | Money pickup |
| VFX_Shocking_Ground | Shock ground effect |
| VFX_StaticCharge | Static charge buildup |
| VFX_Stun | Stun status effect |
| VFX_XPGlob | XP pickup |

---

## 13. Audio System

### 13.1 Sound Effects (SFX)
| Sound | File |
|-------|------|
| Button Hover | `button.wav` |
| Button Press | `button_press.wav` |
| Dash | `Dash.wav` |
| Death | `Death.wav` |
| Dialog 1-3 | `Dialog_1.wav`, `Dialog_2.wav` |
| Hit | `hit.wav` |
| Item Identified | `Identified.wav` |
| Level Up | `Power Up 1.wav` |
| Mana Glob | `Mana_Glob.wav` |
| Mimic Charge | `Mimic_Charge.wav` |
| Money Pickup | `Money_Pickup.wav` |
| Reroll No | `reroll_no.wav` |
| Reroll Yes | `reroll_yes.wav` |
| Rolling | `Rolling.wav` |
| Shock/Explosion | `explosion.wav` |
| Skeleton Charge | `Skeleton_Charge.wav` |
| Sword | `Sword.wav` |
| XP Pickup | `XP_Pickup.wav` |

### 13.2 Music
| Track | File |
|-------|------|
| Game Music 1 | `wizdung_level_w_intro(1).wav` |
| Game Music 2 (Loop) | `wizdung level_loop.wav` |
| Main Menu | `wizdung_title.wav` |

### 13.3 Audio Manager
- `Audio_Manager.gd` — Central audio management
- `Audio_Def.gd` — Audio definition system
- `2D_Audio_Player.gd` — 2D positional audio
- Audio resources (.tres) for each sound with metadata (beat_count, bar_beats, loop_offset)

---

## 14. Save System

- `Save_Screen.tscn` — Save game UI
- `Save_Button.gd` — Save button handler
- `save_screen.gd` — Save screen logic
- `settings_manager.gd` — Settings persistence
- Save likely stored locally (no cloud save evidence)

---

## 15. File Structure Summary

```
res://
├── Abilities/
│   ├── Sprites/ (ability_wizard_mimic_projectile)
│   ├── icons/ (Icon_Agility_Basic_Attack, Icon_DashingBlades)
│   └── scripts/ (Damage_Structure.gd)
├── Audio/
│   ├── SFX/ (18 sound effects)
│   ├── music/ (3 music tracks)
│   ├── Audio_Resources/ (27 .tres audio definitions)
│   ├── scripts/ (Audio_Manager, Audio_Def, 2D_Audio_Player)
│   └── Scenes/ (Scene_Audio_Manager)
├── Character/
│   ├── Scripts/ (CharacterScripts, EnemyAI, StateMachine)
│   ├── Stats/ (Stat_Definitions, Stat_Curves, scripts)
│   ├── Sprite/ (character spritesheets, drop shadows, VFX sheets)
│   ├── Experience/ (XP curves, level up curves, math functions)
│   ├── enemy_resources/ (EnemyScalar definitions)
│   ├── Player_Characters/ (Agility_Wizard, aiming_reticle)
│   ├── Animation_State_Machine/ (Base_Charactera_Anim_Tree)
│   └── Enemies/ (Mimic_Wizard)
├── Dialog/
│   ├── scripts/ (dialog_profile, dialog_set, dialog_text, dialog_condition)
│   └── Response_Types/ (6 response type scripts)
├── General/ (settings_manager)
├── Interactables/
│   ├── Globs/ (Health, Mana, Currency, XP)
│   ├── Home Portal/ (portal_interactable, home_portal_tutorial)
│   ├── Loot/ (Loot_Table, loot_Interactable)
│   ├── Stash/ (Stash, UI_Stash)
│   ├── Character_Select_NPCs/ (NPC_Dex/Int/Str_Wizard, dialog_interactable)
│   ├── Door_Shrine/
│   └── NPC_Merchant_Witch.tscn
├── Inventory/
│   ├── Icons/ (rarity frames, empty slot icons)
│   ├── scripts/ (ui_equipment_slot)
│   └── (UI_Inventory, UI_Tooltip, UI_Tooltip_Compare)
├── Items/
│   ├── data/
│   │   ├── item_defs/ (Boots, Helmet, Necklace, Ring, weapon, key)
│   │   ├── item_instance/ (Starting items, T1 items, keys)
│   │   ├── item_curves/ (5 scaling curves)
│   │   └── item_stat_mod_sets/ (T1 sets, simplified sets)
│   ├── icons/ (AS_ prefixed item icons)
│   └── scripts/ (item_Definition, item_instance, item_stat_mod)
├── Levels/
│   ├── scenes/ (Level_0A through Level_4A, Boss levels, Tutorial levels)
│   ├── scripts/ (level_base, enemy_spawn, camera, collision, transition)
│   ├── Resources/ (RoomSets, Scalars)
│   ├── Tilesets/ (Dungeon, Cave, Overgrown, Desert)
│   └── SpawnRarity_Curves/ (pack_size, rarity)
├── Skill Tree/
│   ├── Scripts/ (Skill_Node, Skill_Node_Set)
│   └── Resources/
│       ├── Agility_Skill_Behaviors/ (Basic Attack, Movement, Passive, Special Attack)
│       ├── Wisdom_Skill_Behaviors/ (Basic Attack, Movement, Passive, Special Attack)
│       ├── Skill_Node_Sets/ (8 skill tree sets)
│       └── Skill_Nodes/ (Agility + Wisdom, 9 nodes each)
├── Skills/
│   ├── Scripts/ (Core_Functionality, Base_Behaviors)
│   ├── Skill_Definitions/ (13 skill definitions)
│   ├── Skill_Modifier_Definitions/ (Shared + class-specific)
│   ├── Resources/ (Behaviors, Status_Effects)
│   └── Base Skill/ (Projectile, Hitbox, Skill scenes)
├── UI/
│   ├── main_menu/ (main_menu, character_sheet, UI_Skill_Tree, UI_Settings)
│   ├── Boss_HealthBar/
│   ├── CRT Shader/ (CRT effect)
│   ├── Cursor/ (custom cursor)
│   ├── Door_Interaction/ (Door_UI, Key_UI)
│   ├── Merchant_Screen/
│   ├── PauseMenu/
│   ├── Save_Menu/
│   ├── combat_feedback/ (UI_Combat_Crit)
│   ├── UI_Assets/ (portraits, money icon, button themes)
│   └── Generic Themes/ (Base_Theme, fonts, scroll bars, buttons)
├── VFX/
│   ├── Scripts/ (Vfx_Cleanup, vfx_ghost_trail)
│   └── (20 VFX scenes)
└── Visual_Scripts/ (visual_snapper)
```

---

## 16. Clone Checklist

To rebuild this game, you need:

### Core Engine
- [ ] Godot 4.6.1 project setup
- [ ] 8-directional character movement system
- [ ] State machine (Idle, Walk, Attack, Death, Stunned)
- [ ] Aiming reticle system
- [ ] CRT shader post-processing
- [ ] Custom cursor
- [ ] Pixel font

### Character System
- [ ] 3 playable classes (Dex/Int/Str Wizard) with unique spritesheets
- [ ] Character switch system via NPC dialog
- [ ] 6 core attributes (Power, Swiftness, Wisdom, Toughness, Dexterity, Accuracy)
- [ ] 30+ combat stats (offensive, defensive, status-related)
- [ ] Stat scaling curves per level
- [ ] Ethereal Armor shield system

### Skill System
- [ ] Skill tree with 4 sub-trees per class (36 nodes per class)
- [ ] 26+ skill behavior scripts (modular)
- [ ] 20+ skill modifier definitions
- [ ] 4 damage types (Physical, Fire, Frost, Lightning)
- [ ] 5 status effects (Burn, Frostbite, Shock, Stun, Freeze)
- [ ] Damage conversion system
- [ ] Projectile system with count/speed/size/piercing modifiers
- [ ] Skill point system with respec

### Item System
- [ ] 6 equipment slots (Weapon, Chest, Helmet, Boots, Ring, Necklace)
- [ ] 3 armor types (Cloth, Leather, Plate)
- [ ] 3 class-specific weapon types
- [ ] 3 ring/necklace variants per class
- [ ] 5 rarity tiers + Unidentified
- [ ] 12+ stat modifier sets
- [ ] 5 item scaling curves
- [ ] Item identification system
- [ ] Enchanting/rerolling system
- [ ] Tooltip with comparison

### Enemy System
- [ ] 3 enemy types (Skeleton, Wizard Mimic, Boss)
- [ ] AI controller with aggro radius
- [ ] Enemy state machine
- [ ] 7 enemy scalar types (normal + elite variants)
- [ ] Enemy rank system (Normal/Elite/Boss)
- [ ] Boss health bar UI

### Dungeon System
- [ ] Room set system with room templates
- [ ] 5+ room sets (Tutorial, T1, T2, Endgame, Hub)
- [ ] 4+ tileset themes (Dungeon, Cave, Overgrown, Desert)
- [ ] Door system with key requirements
- [ ] Room level scaling
- [ ] Spawn system with rarity curves
- [ ] Pack size scaling
- [ ] Portal system (hub return)
- [ ] Stash storage

### NPC System
- [ ] Mysterious Wizard (identify + respec)
- [ ] Trinket Witch (enchant + sell)
- [ ] 3 Character Select NPCs
- [ ] Instruction Man (tutorial)
- [ ] Dialog system with conditions and response types

### Loot System
- [ ] Loot table with gear/key/glob chances
- [ ] 4 glob types (Health, Mana, Currency, XP)
- [ ] Loot scaling curves
- [ ] Ground loot interaction

### Progression
- [ ] XP and leveling system
- [ ] Skill point earning and spending
- [ ] Item identification
- [ ] Enchanting
- [ ] Respec system

### UI
- [ ] Main menu with character selection
- [ ] Player HUD
- [ ] Boss/enemy health bars
- [ ] Inventory with equipment slots
- [ ] Skill tree UI
- [ ] Character sheet
- [ ] Dialog box system
- [ ] Merchant screen
- [ ] Stash UI
- [ ] Pause menu
- [ ] Save screen
- [ ] Settings (keyboard + controller)
- [ ] Room info display
- [ ] Key UI for doors
- [ ] Combat feedback (crit indicator)

### VFX & Audio
- [ ] 20 VFX scenes
- [ ] 18 SFX
- [ ] 3 music tracks
- [ ] Audio manager system
- [ ] Ghost trail effect

### Save System
- [ ] Save/load functionality
- [ ] Settings persistence