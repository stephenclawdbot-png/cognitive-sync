# Legendum — Game Mechanics Document

**Engine:** Godot 4.6.2  
**Version:** v0.14.1 (demo)  
**Genre:** Top-down RPG / Life Simulation Roguelite  
**PCK Status:** Encrypted (flags=2), analyzed via string extraction  
**Extraction Date:** 2026-01-2x  

---

## 1. Overview

Legendum is a **life-simulation RPG with roguelite progression**. The player lives through a character's entire life — from youth to old age to death — making narrative choices, training skills, fighting in auto-battler style combat, and building permanent meta-progression across multiple lives ("runs").

The core concept: **each life is a run**. When your character dies, you carry over meta-progression (Legacy Points, Soul Perks, Heirlooms) but lose character-level progress. The goal is to build increasingly powerful lives through wise choices about what to train, who to befriend, and how to spend your limited time.

### Core Loop
1. **Choose an Origin** (prisoner, farmhand, scholar, hunter, etc.)
2. **Live your life** — perform jobs/tasks to earn XP, gold, and skill points
3. **Fight in encounters** — auto-battler combat with abilities, weapons, and perks
4. **Make narrative choices** — story web nodes that unlock locations, contacts, items
5. **Age and die** — character progresses through life stages (young → veteran → elder → decrepit)
6. **Earn Legacy Points** — spend on Soul Perks for the next life
7. **Reincarnate** — start a new life with meta-progression bonuses

---

## 2. Character System

### 2.1 Attributes (Stats)
Six primary attributes, each with a level (1-80+ observed):

| Stat | Code | Description |
|------|------|-------------|
| Strength | STAT_STRENGTH | Physical power, melee damage |
| Dexterity | STAT_DEXTERITY | Speed, agility, ranged combat |
| Vigor | STAT_VIGOR | Health, endurance, survivability |
| Perception | STAT_PERCEPTION | Awareness, critical chance |
| Intellect | STAT_INTELLECT | Magic, learning speed |
| Wisdom | STAT_WISDOM | Spirit, piety, knowledge |

**Stat Quality Tiers:** AVERAGE → GOOD → GREAT → EXCELLENT  
Each origin starts with different stat distributions (e.g., Prisoner starts AVERAGE across the board, Farmhand has GOOD Strength).

**Attribute Training:** During combat, the player can "focus" on training a specific attribute, gaining XP in that stat while fighting. This is unlocked via the "Attribute Training" story node.

### 2.2 Skills
Skills are separate from attributes and leveled through related activities:

| Skill | Code | Trained By |
|-------|------|------------|
| Blades | SKILL_BLADES | Melee combat with swords |
| Archery | (primary_skill ARCHERY) | Ranged combat with bows |
| Farming | SKILL_FARMING | Farm work tasks |
| Foraging | SKILL_FORAGING | Gathering herbs/food |
| Hunting | SKILL_HUNTING | Hunting tasks |
| Mining | SKILL_MINING | Mining tasks |
| Piety | SKILL_PIETY | Religious activities |
| Roguery | SKILL_ROGUERY | Rogue/thief activities |
| Scholar | (primary_skill SCHOLAR) | Academic study |
| Delving | SKILL_DELVING | Dungeon exploration |
| Social | (primary_skill SOCIAL) | Social interactions |

Skills have their own XP and levels. Some perks require minimum skill levels as prerequisites.

### 2.3 Life Stages
Characters age through life stages, each with stat modifiers:

| Stage | File | Description |
|-------|------|-------------|
| Young | stage1_young | Full vigor, peak physical stats |
| Veteran | stage3_veteran | Experience compensates for declining youth |
| Elder | stage4_elder | "The fire dims but does not die" — wisdom over might |
| Decrepit | stage5_decrepit | Final stage before death |

Each stage has narrative text describing the character's condition. Stats decline with age, but wisdom and intellect may increase.

### 2.4 Origins (Character Backgrounds)
Observed origins:
- **Prisoner** — Starts in prison, must escape (origin_prisoner_nodes.scn, origin_prisoner_open.res)
- **Farmhand** — Works on a farm (t1_farmhand.res, farmhand_3.res)
- **Academy Scholar** — Studies in ancient archives (origin_academy.scn, origin_library.scn)
- **Hunter's Child** — Grows up in the wild (origin_hunters_child.scn)
- **Library** — Academic origin (origin_library.scn)

Each origin provides:
- Starting stats and stat quality tiers
- Starting items (weapons, armor, tools)
- Starting status effects (e.g., "early_years")
- Unique narrative web (story nodes)
- Starting location/region access
- Default combat style

---

## 3. Combat System

### 3.1 Combat Style
Combat is **auto-battler style** — the player character automatically fights enemies while the player manages abilities, perks, and equipment.

**Combat Styles** (determine how the character fights):
| Style | File | Description |
|-------|------|-------------|
| Power | power.tres | Raw damage melee |
| Sword Style | sword_style.tres | Technical swordplay |
| Vigor | vigor.tres | Tanky, endurance-based |
| Precision | precision.tres | Critical hit focused |
| Speed | speed.tres | Fast attacks |
| Bow Dex Per | bow_dex_per.tres | Dexterity-based archery |

### 3.2 Weapons
Three weapon types, each with different behaviors:

| Type | Class | Description |
|------|-------|-------------|
| Melee | WeaponMelee | Swords, daggers — close range slash |
| Ranged | WeaponRanged | Bows — projectile attacks |
| Magic | WeaponMagic | Staves — magical orbs/spells |

**Weapon Tiers (observed):**
- Training Sword/Bow/Staff → Old Sword/Shortbow/Staff → Sturdy Sword/Shortbow/Staff → Mighty Sword/Shortbow → Sword 2/3/4, Shortbow 2/3/4, Staff 3/4
- Greatsword/Greatbow — high-tier weapons ("Giant's Sword", "Giant's Bow")
- Special: Duality Blade, Duality Bow, Magic Bow, Shatteraxe, Magic Dagger

**Weapon Stats:**
- damage_min / damage_max (e.g., 4-5, 5-6, 6-7, 7-8, 8-9, 10-11, 11-12, 13-14, 15-16, 16-18)
- scaling_damage (0.8 to 1.3 — multiplier based on stat scaling)
- Attack speed (modified by weapon speed effects)

### 3.3 Abilities
Abilities are special attacks/passives unlocked through perks and items:

| Ability | Type | Description | Stats |
|---------|------|-------------|-------|
| Analyze | Active | Study a foe to reveal weaknesses, +1.3x damage for 15s | SPD 3.5s |
| Assassinate | Active | Leap to weakest target, deadly strike | DMG 8-12, SPD 6s, CRIT 10% |
| Beartrap | Active | Throw a trap that snares enemies + damage | DMG 15-20, SPD 4s |
| Bowl of Fire | Active | Emit a fireball | DMG 7-9 (AoE), SPD 4.5s, CRIT 5% |
| Chain Lightning | Active | Lightning strike hitting multiple enemies | DMG 10-14 (AoE), SPD 10s, CRIT 5% |
| Giant Orb | Active | Staff attack hitting up to 3 targets | DMG 6-8 (AoE), SPD 4.2s, CRIT 5% |
| Guardian Spirit | Passive | Restore 40% HP when below 30% HP | SPD 60s |
| Magic Dagger | Passive | Orbiting daggers dealing damage | DMG 2-3, SPD 3s, CRIT 5% |
| Pickaxe Throw | Active | Hurl pickaxe piercing enemies in a line | DMG 9-10, SPD 2.1s |
| Piercing Strike | Active | Bow attack piercing up to 3 targets | SPD 4.2s |
| Rejuvenation | Passive | Heal over time | SPD 5.5s |
| Sweeping Slash | Active | Wide slash, 1.1x damage in a cone | SPD 6s |
| Throwing Knives | Active | Throw knives at distant enemies | DMG 10-14, SPD 10s, CRIT 10% |
| Wrath | Active | AoE damage burst | DMG 8-12, SPD 10s, CRIT 10% |

**Ability Types:** PASSIVE, ACTIVE  
**Ability Slot System:** Abilities are equipped into slots (ui_ability_slot.scn). Some abilities are AUTO-triggered.

### 3.4 Enemies (Mobs)
| Enemy | File | Notes |
|-------|------|-------|
| Slime | mob.slime | Basic enemy, blue/green/red variants |
| Slime Big | mob.slime_big, mob.slime_green_big | Larger, tougher variant |
| Bat | mob.bat | Flying enemy |
| Wolf | mob.wolf2, wolf2.scn, wolf3.scn | Brown/gray/danger variants |
| Spider | (referenced in assets) | |
| Snake | (referenced in assets) | |
| Rat | (referenced in assets) | |
| Ooze | (referenced in assets) | |
| Leech | (referenced in assets) | |
| Beholder | (referenced in assets) | |
| Mimic | (referenced in assets) | |
| Goblin | mob.goblin_spear, goblin.scn | Spear-wielding |
| Goblin Archer | kobold_archer.scn | Ranged goblin |
| Goblin Mage | kobold_mage.scn | Magic goblin |
| Kobold | kobold.scn | Small humanoid |
| Skeleton Knight | mob.skeleton_knight, skeleton_knight.scn | Heavy melee |
| Skeleton Archer | mob.skeleton_archer, skeleton_archer.scn | Ranged skeleton |
| Skeleton Mage | mob.skeleton_mage, skeleton_mage.scn | Magic skeleton |
| Golem | mob.golem | Large boss-type enemy |
| Ent/Entling | mob.fauna_ent, mob.fauna_entling | Plant creatures |
| Spirit | mob.spirit | Ghostly enemy |
| Dummy | mob.dummy | Training dummy |
| Sparrer | mob.sparrer, sparrer.scn | Sparring partner |
| Ancient Stone Guardian | ancient_stone_guardian.res | Boss |

**Enemy Projectiles:**
- enemy_arrow.scn — Skeleton archer arrows
- enemy_shaman_orb.scn — Shaman/mage orbs
- enemy_skeleton_orb.scn — Skeleton mage orbs

### 3.5 Combat Scaling
Encounters have scaling profiles:
- **scaling_damage**: 0.8, 0.9, 1.0, 1.1, 1.15, 1.2, 1.3 (multiplier on enemy damage)
- **scaling_health**: 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 3.0, 3.5 (multiplier on enemy health)
- Higher scaling = harder encounters, better rewards

### 3.6 Wave System
Combat encounters use a wave system:
- `swarm_spawn_interval_base`: 1.4 to 10.0 seconds between spawns
- `swarm_spawn_interval_decrease_per_minute`: 0.2 to 2.0 (spawns get faster over time)
- `swarm_spawn_interval_min`: 0.1 to 3.0 seconds (floor on spawn rate)
- `spawn_cap`: 3-4 (max concurrent enemies)
- `grid_spawn`: true/false (whether enemies spawn in grid pattern)
- `no_overlap_spawn`: true (enemies don't overlap)
- Boss enemies have `info: "Boss"`

### 3.7 Status Effects
Status effects can be applied to the character:
- `early_years` — Starting buff for young characters
- `injured` — Negative effect from combat
- Various temporary buffs from items/food (e.g., "A Warden's feast" — massive temporary buff to Physical stats)
- Status effects can be removed as quest rewards (reward_remove_status_effect)

---

## 4. Perk System

Perks are permanent character upgrades unlocked through gameplay. They form a **perk web** (tree) with prerequisites.

### 4.1 Perk Categories
Perks are organized into categories:
- **Combat Perks** — Blademaster, Bowmaster, damage bonuses
- **Skill Perks** — Forager, Miner, Piety bonuses (+20% SP gain)
- **Utility Perks** — Shop Discount (10% off), Pickpocket, Dense (loot chance)
- **Lifestyle Perks** — Early Riser (Morning slot), Night Owl (Evening slot)
- **Special Perks** — Dreamer, Voidmaw, Rejuvenation, Devotion

### 4.2 Observed Perks
| Perk | Effect |
|------|--------|
| blademaster_i | Unlocks Sweeping Slash ability |
| blades_slash | Melee slash ability |
| bowmaster_i | Unlocks Piercing Strike |
| bows_piercing | Bow piercing attack |
| staff_chain_orb | Staff chain orb ability |
| lightning_strike | Chain Lightning ability |
| lightning_strike_blitz_1/2 | Lightning upgrade nodes |
| analyze_dmg | Analyze damage bonus |
| holy_shrapnel | Holy damage perk |
| faith / devotion | Piety-related perks |
| forager | +20% Foraging SP gain |
| (mining perk) | +20% Mining SP gain |
| (piety perk) | +20% Piety SP gain |
| (roguery perk) | +20% Roguery SP gain |
| shop_discount | Shop prices reduced by 10% |
| pickpocket | Steal bonus coin |
| dense | +25% Loot Chance (Wilds) |
| perceptive | Perception bonus |
| dreamer | XP trickle in multiple stats |
| enduring | Endurance bonus |
| defense | Damage resistance |
| flame_enthusiast | Fire damage bonus |
| rejuvenation | Health regen |
| strong_miner | Mining strength bonus |
| gem_finder | Gem finding bonus |
| cave_delver | Delving bonus |
| prowler | Stealth perk |
| scoundrel | Rogue perk |
| voidmaw | Consume any item ability |
| smooth_brain_strong_muscle | Stronk book perk |
| nap_old | Rest perk |
| hunting_lodge | Hunting perk |

### 4.3 Perk Web
Perks are organized in a web with prerequisites:
- Some perks require other perks (e.g., lightning_strike_blitz_2 requires lightning_strike_blitz_1)
- Some perks require skill levels (req_skill_level)
- Some perks require attribute levels (req_attribute)
- Some perks require other perks (req_has_perk)
- The perk web is visualized in a dedicated UI (ui_perk_web_state, Camera2DPerkWeb)

### 4.4 Soul Perks (Meta-Progression)
Soul Perks are **permanent across lives**, purchased with Legacy Points:
- Early Bird — Start all lives with Morning slot
- Night Owl — Start all lives with Evening slot
- Various other meta bonuses

---

## 5. Item & Equipment System

### 5.1 Item Types
| Type | Description |
|------|-------------|
| WEAPON | Swords, bows, staves |
| ARMOR | Body armor (Cloth, Leather, Iron) |
| HELMET | Head protection |
| SHIELD | Defensive shields |
| ACCESSORY | Amulets, rings, capes |
| GENERIC | Consumables, tools, misc |

### 5.2 Equipment Slots
- Weapon
- Armor (body)
- Helmet
- Shield
- Accessory (amulet/ring)
- Boots
- Gloves

### 5.3 Item List (Observed)

**Weapons:**
- Training Sword, Old Sword, Sturdy Sword, Mighty Sword, Sword 2/3/4
- Training Bow, Old Shortbow, Sturdy Shortbow, Mighty Shortbow, Shortbow 2/3/4
- Training Staff, Sturdy Staff, Staff IV
- Greatsword 3, Giant's Sword, Duality Blade
- Greatbow 3, Giant's Bow, Duality Bow, Magic Bow
- Dagger, Magic Dagger, Shatteraxe
- Sturdy Pickaxe, Pickaxe (Iron/Bronze/Steel variants)

**Armor:**
- Leather Body, Iron Body, Cloth (implied)
- Leather Helm, Iron Helm, Miner's Helmet

**Shields:**
- Hide Shield, Heavy Shield
- Buckler (Metal/Wood), Heater (Metal/Wood) — from asset references

**Accessories:**
- Amulet of Dexterity, Amulet of Precision, Amulet of Siphoning, Amulet of Swiftness
- Blessed Ring, Ring of Life
- Hunter's Cape, Leather Cape
- Silk Fingerwraps

** consumables/Tools:**
- Berries, Herbs, Holy Water, Magic Ooze, Cloud Puff, Dirty Socks, Sorry Stone
- Holy Text: Dawn, Holy Text: Saint Morin, Guide to Prayer, Holy Scriptures
- Book of Stronk, Book of Megastronk, Book of Ultrastronk
- Scribe's Candle, Old Looking Glass, Spectacles
- Old Map (Woods), Faded Star Chart, Long Rope, Tent
- Mysterious Relic, Crescent Moon Key, Saint's Tooth
- Fine Clothing, Respectable Clothing, Farmer's Hat
- Sturdy Work Boots, Sturdy Work Gloves, Work Gloves
- Hide Quiver, Knife Pouch

### 5.4 Item Effects System
Items have effects defined by type:

| Effect Type | Description |
|-------------|-------------|
| effect_armor | Adds armor rating |
| effect_att_speed_for_weapon | Attack speed for specific weapon |
| effect_blocks_perk | Blocks a perk slot |
| effect_damage_resistance | Reduces incoming damage |
| effect_enable_ability | Enables an ability |
| effect_health_regen | HP regeneration |
| effect_mod_attribute | Modifies an attribute |
| effect_mod_skill | Modifies a skill |
| effect_specific_ability_custom | Custom ability effect |
| effect_specific_ability_dmg | Ability damage bonus |
| effect_specific_ability_speed | Ability speed bonus |
| effect_weapon_dmg | Weapon damage bonus |
| effect_ability_aoe | AoE ability bonus |
| effect_ability_dmg | General ability damage |
| effect_ability_speed | Ability speed bonus |
| effect_ability_recharge | Ability recharge speed |
| eff_spirit_spawn | Summon spirit |
| eff_typed_damage | Typed damage bonus |
| eff_blocks_perk | Block perk |
| eff_boost_sp_gain | Skill point gain boost |
| eff_boost_sp_gain_group | Group SP gain boost |
| eff_boost_xp_gain | XP gain boost |
| eff_boost_feat_lp | Feature LP boost |
| eff_crit_chance | Critical chance bonus |
| eff_day_duration | Day length modifier |
| eff_max_hp_percent | Max HP percentage |
| eff_scaled_by_domain | Scales by domain |
| eff_scaled_by_skill | Scales by skill level |
| eff_scaled_by_stat | Scales by stat |
| gain_armor | Gain armor |
| gain_att_speed_for_weapon | Attack speed for weapon |
| gain_attack_speed_boost | General attack speed |
| gain_block_chance | Block chance |
| gain_block_rating | Block rating |
| gain_crit_chance_boost | Crit chance boost |
| gain_crit_chance | Crit chance |
| gain_healing_boost | Healing boost |
| gain_health_regen | HP regen |
| gain_lifesteal | Lifesteal |
| gain_max_hp | Max HP |
| mod_attribute_effective_lvl | Modify effective attribute level |
| mod_global_xp_gain | Global XP gain |
| mod_max_energy | Max energy |
| mod_max_hp_factor | Max HP factor |
| mod_movement_speed | Movement speed |
| mod_task_energy | Task energy cost |
| mod_task_money | Task money reward |
| boost_job_xp_output | Job XP output boost |
| boost_job_xp_output_simple | Simple job XP boost |
| boost_stat_lvl | Boost stat level |
| boost_task_lvl | Boost task level |
| boost_task_speed | Task speed boost |
| boost_task_speed_time_of_day | Time-of-day task speed |
| boost_xp_output | XP output boost |
| add_movement_speed | Movement speed |

### 5.5 Item Rarity Tiers
Rarity borders observed in assets:
- **Unawoken** — Special/locked tier
- **Gray** — Common
- **Green** — Uncommon
- **Blue** — Rare
- **Red** — Epic
- **Gold** — Legendary
- **White** — Mythic
- **Destiny** — Special tier

---

## 6. Job & Task System

### 6.1 Jobs
Jobs are activities the character performs to earn XP, gold, and skill points:

| Job | File | Primary Skill | Description |
|-----|------|---------------|-------------|
| Farmhand | t1_farmhand.res | FARMING | Work on a farm |
| Forager | job_forager.res | FORAGING | Gather herbs and food |
| Herb Gatherer | job_herb_gatherer.res | FORAGING | Collect herbs |
| Quarry Worker | job_quarry_worker.res | MINING | Work in quarry |
| Quarry Hauler | job_quarry_hauler.res | MINING | Haul ore |
| Ore Hauler | job_ore_hauler.res | MINING | Transport ore |
| Hard Laborer | job_hard_laborer.res | (general) | Physical labor |
| Peasant Chapel Keeper | job_peasant_chapel_keeper.res | PIETY | Maintain chapel |
| Novice Hunter | novice_hunter.res | HUNTING | Basic hunting |
| Novice Miner | novice_miner.res | MINING | Basic mining |
| Expert Farmhand | (expert_farmhand) | FARMING | Advanced farming |
| Expert Archivist | (expert_archivist) | SCHOLAR | Advanced research |
| Monster Slayer | (monster_slayer) | COMBAT | Combat work |

### 6.2 Tasks
Tasks are specific activities within jobs:
- `task_rest` — Resting (recovers energy)
- `task.explore_cabin` — Explore a cabin
- `task.explore_roads` — Explore roads
- `task.old_map` — Use old map
- `quest_scour` — Scour/explore quest
- `patrol_woodlands_1/2` — Patrol the woodlands
- `mining_1`, `mining_1a` — Mining tasks
- `pushups` — Physical training
- `study_sacred_texts` — Religious study
- `beat_goblins` — Combat task
- `beat_training_grounds` — Combat training

**Task Modifiers:**
- Task energy cost (mod_task_energy)
- Task money reward (mod_task_money)
- Task speed (boost_task_speed, boost_task_speed_time_of_day)
- Task XP output (boost_job_xp_output, boost_xp_output)
- Task level (boost_task_lvl)

### 6.3 Time-of-Day System
Tasks and abilities are affected by time of day:
- Morning slot (Early Bird perk)
- Evening slot (Night Owl perk)
- Day duration modifier (eff_day_duration)
- Task speed varies by time of day (boost_task_speed_time_of_day)

---

## 7. Narrative System

### 7.1 Story Web
The narrative is structured as a **web of story nodes**:
- Each node has a description, optional prerequisites, and choices
- Nodes can unlock: new locations, items, contacts, quests, perks, abilities, regions, combat styles, world state changes
- Nodes are connected through a web UI (ui_story_web_state, base_story_web_nodes.scn)
- Some nodes have **selectors** (branching choices)
- Some nodes have **encounters** (combat or exploration)

### 7.2 Story Node Types
| Type | Description |
|------|-------------|
| node.* | Standard story node |
| selector.* | Choice/branch node |
| encounter.* | Combat/exploration encounter |
| quest_* | Quest trigger node |
| hc_* | High-cost story node |

### 7.3 Narrative Speakers
| Speaker | File | Role |
|---------|------|------|
| Narrator | narrator.res | Main narration |
| Father Alric | npc_father_alric.res | Church/priest NPC |
| Grey Wizard | npc_grey_wizard.res | Wizard mentor |
| Helga | npc_helga.res | Combat trainer |
| Lunorak | npc_lunorak.res | Scholar NPC |
| Prison Guard | npc_prison_guard.tres | Prison origin NPC |
| Goblin | goblin.res | Goblin trader (Mizgrub) |

### 7.4 Key Story Arcs (Observed)
1. **Prison Escape** — Start as prisoner, loosen bar, escape
2. **Caravan Investigation** — Investigate missing caravans, find goblin raiders
3. **Lost Temple** — Explore ancient temple, find coffer
4. **Archive Depths** — Scholar origin, explore ancient archives
5. **Training Grounds** — Upgrade training grounds in Ashvale
6. **Wolf Trouble** — Save farm from wolves
7. **Catacombs** — Explore catacombs under the town
8. **Goblin Conclusion** — Deal with captured goblin (spare/execute)
9. **Moonberries** — Special quest involving moonberries
10. **Sacred Pilgrimage** — Religious quest

### 7.5 Deeds
Deeds are permanent records of player choices:
- `deed.av_caravans` — Saved the caravans
- `deed.av_caravans_trader` — Trader quest deed
- `deed.av_upgrade_training_grounds` — Upgraded training grounds
- `deed.av_mizgrub_spared` — Spared Mizgrub the goblin
- `deed.av_mizgrub_executed` — Executed Mizgrub
- `deed.chapel_donation` — Donated to chapel
- `deed.uncover_lost_temple` — Discovered lost temple
- `deed.mg_queen_shield` — Special deed

### 7.6 Journal System
The journal tracks:
- Quests (journal_category_quests)
- Events (journal_category_events)
- Side quests (JournalSideQuest)
- Thread objectives and segments

---

## 8. World & Exploration

### 8.1 World Regions
| Region | File | Description |
|--------|------|-------------|
| Ashvale | ashvale.res | Starting town/village |
| Woodlands | woodlands.tres | Forest region with enemies |
| Woodlands 2 | woodlands2.scn | Deeper forest |
| Dead Woodlands | dead_woodlands.tscn | Dangerous forest area |
| Depths | depths2.tscn | Underground area |
| Valenthar | (referenced) | Elven region (NOT AVAILABLE IN DEMO) |

### 8.2 Locations
- Village Center (village_center.res)
- Church/Chapel (hub_church.scn)
- Rogue Guild (hub_rogue_guild.scn)
- Inn (node.inn)
- Mine (node.mine)
- Hunting Lodge (hunting_lodge.res)
- Training Grounds (training_grounds.res)
- Catacombs (trouble_in_the_catacombs.res)
- Caves in the Hills (caves_in_the_hills.res)
| Ancient Mines (encounter.ancient_mines_2.res)
- Rock Caverns (rock_caverns.res)
- Lost Temple (the_lost_temple.res)
- Archive Depths (archive_depths.res)
- Sewer (encounter.sewer.res)
- Slums (node.slums_sewer, node.slums_leave)

### 8.3 Encounter Types
- **Combat Encounters** — Fight waves of enemies
- **Exploration Encounters** — Explore areas for loot/story
- **Treasure Encounters** — Find chests (treasure_chest.scn)
- **Special Encounters** — Unique events (e.g., special_farm_wolf_trouble)

### 8.4 Exploration Points
Goods system uses exploration points by region:
- EXPLORATION_POINTS_PRISON
- EXPLORATION_POINTS_ROADS
- EXPLORATION_POINTS_TOWN
- EXPLORATION_POINTS_WOODLANDS

### 8.5 Loot System
- LootTable with LootTableEntry
- Guaranteed items vs random items
- Discoveries (loot.lost_temple, loot.woodlands1, loot.woodlands2)
- Fixed items and extra items

---

## 9. Shop & Trading System

### 9.1 Shops
| Shop | File | Description |
|------|------|-------------|
| Mizgrub | shop.mizgrub | Goblin trader |
| Father Alric | shop.father_alric | Church shop |
| Village Trader | shop.village_trader | General store |
| Goods Peddler | shop.goods_peddler | Traveling merchant |
| Ilaf | shop.ilaf | NPC shop |

### 9.2 Shop Mechanics
- **ShopStock** — Items available in shop, with stock instances
- **ShopItem** — Individual item listing
- **ShopItemPool** — Pool of possible items
- **ShopItemWeighted** — Weighted random items
- **ShopTier** — Tiered shop quality (common, uncommon, rare, etc.)
- **Shop Discounts** — Perk can reduce prices by 10%
- **Shop Shortages** — Dynamic stock events (shop_shortages.res)
- **Shop Upgrades** — Improve trader stock through quests

### 9.3 Goods System
"Goods" are a secondary currency/resource type:
- Exploration points by region
- Can be earned as quest rewards (reward_goods)
- Used for unlocking areas or trading

---

## 10. Progression Systems

### 10.1 Level System
- **Character Level** — Overall character level
- **Attribute Levels** — Individual stat levels (1-80+)
- **Skill Levels** — Individual skill levels
- **Legend Rank** — Meta-progression rank (legend_rank.gd)

**Level Curves:**
- lvl_curve, lvl_data, smart_lvl_curve — Multiple leveling curve implementations
- XP requirements scale with level

### 10.2 Currency
| Currency | Source | Use |
|----------|--------|-----|
| Gold | Quests, jobs, combat | Buy items, shop |
| Goods (exploration points) | Exploration | Unlock areas |
| XP | Combat, jobs, tasks | Level up stats/skills |
| Legend Points (LP) | Quests, deeds | Meta-progression |
| Resolve Points (RP) | Special quests | Character resolve |
| Skill Points (SP) | Skill activities | Unlock perks |

### 10.3 Reward Types
Quests and encounters can give:
- reward_xp — Experience points
- reward_gold — Gold
- reward_goods — Goods/exploration points
- reward_lp — Legend Points
- reward_rp — Resolve Points
- reward_sp — Skill Points
- reward_item — Items
- reward_heirloom — Heirloom (permanent item)
- reward_ability — New ability
- reward_talent — New talent
- reward_deed — Record a deed
- reward_contact — Unlock NPC contact
- reward_location — Unlock map location
- reward_region — Unlock world region
- reward_journal_entry — Journal entry
- reward_flag — Set a flag
- reward_world_state — Change world state
- reward_remove_status_effect — Remove debuff
- reward_unlock_perks — Unlock perk category
- reward_unlock_profession — Unlock profession
- reward_unlock_tab — Unlock UI tab
- reward_unlock_web — Unlock story web
- reward_upgrade_encounter — Upgrade an encounter
- reward_combat_styles — Unlock combat styles
- reward_close_web — Close a story web
- reward_show_task — Show a new task
- reward_title — Unlock a title

### 10.4 Requirements
Quests/perks can have requirements:
- req_attribute — Minimum attribute level
- req_skill_level — Minimum skill level
- req_has_perk — Must have a specific perk
- req_talent_lvl — Minimum talent level
- req_world_state — World state must match

---

## 11. Save System

- **shelve-it** addon — Save/load system
- Save data includes: calendar_state, campaign_state, character_state, inventory_state, journal_state, loot_state, meta_state, narrative_state, perk_selection_state, run_state, shop_data, task_state, web_state, world_state
- Save/Load UI with import/export functionality
- Persistent instances: ability_instance, item_instance, shop_stock_instance, status_effect

---

## 12. Calendar & Time System

- **CalendarState** — Tracks in-game time
- Seasons: Greenrise, Highsun, Amberfall (icon_season_*)
- Turn of the Year event (turn_of_the_year.res)
- Day/night cycle affects task speed and available slots
- Time elapsed indicator UI (ui_time_elapsed_indicator.scn)

---

## 13. Contact/Community System

- **Contacts** — NPCs you build relationships with
- Contact yield UI (ui_contact_yield.scn) — Shows relationship benefits
- Contacts can provide: shop access, quest opportunities, bonuses
- Panel contact UI (panel_contact.res)
- Contacts are unlocked as quest rewards (reward_contact)

---

## 14. Addons & Technical

### 14.1 Addons Used
| Addon | Purpose |
|-------|---------|
| better-terrain | Tilemap/terrain system |
| define-it | JSON database with hot reload |
| shelve-it | Save/load system |
| console | Debug console |
| tooltip | Tooltip system |
| damage_text | Floating combat text |
| FPS counter | Performance monitoring |

### 14.2 Key Scripts (GDScript)
- character.gd, character_modifiers.gd — Character data
- enums.gd — Game enumerations
- goods.gd — Goods/currency system
- save_service.gd — Save management
- combat_viewport.gd — Combat rendering
- player_unit.gd/2/3 — Player entity (multiple versions)
- ability_script.gd — Ability system
- weapon_script.gd — Weapon base
- reactive.gd, reactive_computed.gd — Reactive state management
- 610 total GDScript files
- 599 scenes (.tscn/.scn)
- 1458 resources (.tres/.res)

### 14.3 Reactive System
The game uses a custom reactive state system (similar to Vue/MobX):
- `Reactive` class — Observable values
- `ComputedReactive` — Computed/derived values
- Used for UI updates and game state propagation

---

## 15. UI System

### 15.1 Main UI Tabs
- Character (stats, skills, attributes)
- Inventory (items, equipment)
- Perks (perk web)
- Quests/Journal
- Shop/Trade
- Map/Region
- Abilities (ability slots)
- Tasks/Jobs
- Story Web
- Settings

### 15.2 Key UI Scenes
- ui_title.scn — Title screen
- ui_play_scenario.scn — Play setup
- ui_character_items.scn — Character items
- ui_inventory.scn — Inventory
- ui_perks_new.scn — Perk web
- ui_quests.scn — Quest list
- ui_shop_trader.scn — Shop
- ui_region.scn — Region map
- ui_ability.scn — Ability management
- ui_status_effects.scn — Status effects
- ui_settings_panels.scn — Settings
- ui_save_panel.scn — Save/load
- ui_quiet_years.scn — Quiet years (life review)
- ui_life_review_deed.scn — Life review
- ui_player_age.scn — Age display
- ui_player_lvl.scn — Level display
- ui_chronicle_legend_rank.scn — Legend rank

---

## 16. Life Review & Quiet Years

The game features a **"Quiet Years"** system — periods of life that pass in summary:
- Timeline entries (ui_quiet_years_timeline_entry.scn)
- Life review at death (ui_life_review_deed.scn)
- Deeds are reviewed at end of life
- Life cards show what was accomplished (ui_life_card.scn)
- The "life option" system lets you make high-level life choices

---

## 17. Heirlooms

Heirlooms are **permanent items passed between lives**:
- temple_relic_coffer — Ancient coffer from temple
- Gold ring from garden (narrative item)
- Stored in meta-state
- Earned through special quests

---

## 18. Meta-Progression

### 18.1 Soul Perks
Purchased with Legend Points, permanent across all lives:
- Early Bird / Night Owl — Time slot perks
- Various stat/skill bonuses

### 18.2 Legend Rank
- Chronical system tracking player's overall progress
- Legend rank UI (ui_chronicle_legend_rank.scn)
- Increases with Legend Points earned per life

---

## Clone Checklist

To rebuild Legendum, you need:

### Core Systems
- [ ] Life simulation loop (birth → aging → death → reincarnation)
- [ ] Life stage system with stat decay
- [ ] Origin selection with unique starting conditions
- [ ] Attribute system (6 stats, trainable via combat focus)
- [ ] Skill system (10+ skills, trained by jobs/tasks)
- [ ] Level curves for attributes, skills, and character level
- [ ] Reactive state management system
- [ ] Calendar/time system with seasons
- [ ] Save/load system with multiple state objects

### Combat
- [ ] Auto-battler combat (player auto-attacks)
- [ ] Combat styles (6 styles: power, sword, vigor, precision, speed, bow)
- [ ] Weapon types (melee, ranged, magic) with unique behaviors
- [ ] Ability system (14+ abilities, active/passive, cooldowns)
- [ ] Ability slot system
- [ ] Enemy types (20+ enemies with sprites)
- [ ] Wave spawning system with scaling
- [ ] Damage text floating UI
- [ ] Status effects (buffs/debuffs)
- [ ] Combat scaling profiles

### Progression
- [ ] Perk web with prerequisites
- [ ] Soul perks (meta-progression)
- [ ] Legend Points and Legend Rank
- [ ] Resolve Points
- [ ] Heirloom system
- [ ] Item rarity tiers (8 tiers)
- [ ] Item effect system (30+ effect types)
- [ ] Equipment slots (weapon, armor, helmet, shield, accessory, boots, gloves)

### World
- [ ] World region system
- [ ] Location unlocking
- [ ] Encounter system (combat, exploration, treasure)
- [ ] Loot table system
- [ ] Shop system with tiers, pools, and stock
- [ ] Goods/exploration points system
- [ ] Contact/relationship system

### Narrative
- [ ] Story web node system
- [ ] Narrative speakers (7+ NPCs)
- [ ] Quest system with requirements and rewards
- [ ] Journal system
- [ ] Deed system (permanent choice records)
- [ ] Quiet years / life review
- [ ] 10+ story arcs

### Jobs & Tasks
- [ ] Job system (12+ jobs)
- [ ] Task system with energy, money, XP, speed modifiers
- [ ] Time-of-day task modifiers
- [ ] Profession unlocking

### UI
- [ ] Title screen
- [ ] Character sheet (stats, skills, attributes)
- [ ] Inventory and equipment
- [ ] Perk web visualization
- [ ] Quest/journal
- [ ] Shop/trade interface
- [ ] Region map
- [ ] Ability management
- [ ] Status effects display
- [ ] Settings
- [ ] Save/load with import/export
- [ ] Quiet years timeline
- [ ] Life review screen
- [ ] Age and level displays