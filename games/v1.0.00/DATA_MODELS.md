# v1.0.00 "wizdung" — Data Models & JSON Schemas

> **Purpose:** Complete data schema definitions for all game systems.
> **Usage:** Load these as JSON files in `res://data/`. DataManager autoload reads them at startup.
> **Format:** Each schema shown as TypeScript interface + JSON example.

---

## 1. STATS DEFINITIONS (`data/stats.json`)

```json
{
    "stats": [
        {"id": "power", "name": "Power", "category": "core", "description": "Increases max health. Primary for Str Wizard.", "base_value": 10, "per_level": 2.0},
        {"id": "swiftness", "name": "Swiftness", "category": "core", "description": "Increases toughness and max life. Defensive scaling.", "base_value": 10, "per_level": 1.5},
        {"id": "wisdom", "name": "Wisdom", "category": "core", "description": "Increases max mana and ethereal shield. Primary for Int Wizard.", "base_value": 10, "per_level": 2.0},
        {"id": "toughness", "name": "Toughness", "category": "core", "description": "Reduces incoming physical damage.", "base_value": 5, "per_level": 1.0},
        {"id": "dexterity", "name": "Dexterity", "category": "core", "description": "Increases dodge and accuracy. Primary for Dex Wizard.", "base_value": 10, "per_level": 2.0},
        {"id": "accuracy", "name": "Accuracy", "category": "core", "description": "Chance to hit, contested against dodge.", "base_value": 50, "per_level": 2.0},

        {"id": "physical_damage", "name": "Physical Damage", "category": "offensive", "base_value": 0, "per_level": 0},
        {"id": "fire_damage", "name": "Fire Damage", "category": "offensive", "base_value": 0, "per_level": 0},
        {"id": "frost_damage", "name": "Frost Damage", "category": "offensive", "base_value": 0, "per_level": 0},
        {"id": "lightning_damage", "name": "Lightning Damage", "category": "offensive", "base_value": 0, "per_level": 0},
        {"id": "crit_chance", "name": "Critical Chance", "category": "offensive", "base_value": 5.0, "per_level": 0.1, "unit": "%"},
        {"id": "crit_multiplier", "name": "Critical Multiplier", "category": "offensive", "base_value": 1.5, "per_level": 0},
        {"id": "attack_speed", "name": "Attack Speed", "category": "offensive", "base_value": 1.0, "per_level": 0},
        {"id": "cast_speed", "name": "Cast Speed", "category": "offensive", "base_value": 1.0, "per_level": 0},
        {"id": "multiple_projectiles", "name": "Additional Projectiles", "category": "offensive", "base_value": 0, "per_level": 0},
        {"id": "piercing", "name": "Piercing", "category": "offensive", "base_value": 0, "per_level": 0},
        {"id": "fire_penetration", "name": "Fire Penetration", "category": "offensive", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "frost_penetration", "name": "Frost Penetration", "category": "offensive", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "lightning_penetration", "name": "Lightning Penetration", "category": "offensive", "base_value": 0, "per_level": 0, "unit": "%"},

        {"id": "max_life", "name": "Max Life", "category": "defensive", "base_value": 100, "per_level": 10},
        {"id": "current_life", "name": "Current Life", "category": "defensive", "base_value": 100, "per_level": 0},
        {"id": "max_mana", "name": "Max Mana", "category": "defensive", "base_value": 50, "per_level": 5},
        {"id": "current_mana", "name": "Current Mana", "category": "defensive", "base_value": 50, "per_level": 0},
        {"id": "life_regen", "name": "Life Regen", "category": "defensive", "base_value": 0, "per_level": 0.1},
        {"id": "mana_regen", "name": "Mana Regen", "category": "defensive", "base_value": 2.0, "per_level": 0.1},
        {"id": "mana_cost_reduction", "name": "Mana Cost Reduction", "category": "defensive", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "ethereal_armor", "name": "Ethereal Armor", "category": "defensive", "base_value": 0, "per_level": 0},
        {"id": "dodge", "name": "Dodge", "category": "defensive", "base_value": 5.0, "per_level": 0.2, "unit": "%"},
        {"id": "fire_resistance", "name": "Fire Resistance", "category": "defensive", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "frost_resistance", "name": "Frost Resistance", "category": "defensive", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "lightning_resistance", "name": "Lightning Resistance", "category": "defensive", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "dash_distance", "name": "Dash Distance", "category": "defensive", "base_value": 120, "per_level": 0, "unit": "px"},
        {"id": "movement_speed", "name": "Movement Speed", "category": "defensive", "base_value": 120, "per_level": 0, "unit": "px/s"},

        {"id": "burn_chance", "name": "Burn Chance", "category": "status", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "burn_duration", "name": "Burn Duration", "category": "status", "base_value": 3.0, "per_level": 0, "unit": "s"},
        {"id": "burn_resistance", "name": "Burn Resistance", "category": "status", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "frostbite_chance", "name": "Frostbite Chance", "category": "status", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "frostbite_duration", "name": "Frostbite Duration", "category": "status", "base_value": 3.0, "per_level": 0, "unit": "s"},
        {"id": "frostbite_resistance", "name": "Frostbite Resistance", "category": "status", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "shock_chance", "name": "Shock Chance", "category": "status", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "shock_resistance", "name": "Shock Resistance", "category": "status", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "stun_chance", "name": "Stun Chance", "category": "status", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "stun_duration", "name": "Stun Duration", "category": "status", "base_value": 1.0, "per_level": 0, "unit": "s"},
        {"id": "stun_resistance", "name": "Stun Resistance", "category": "status", "base_value": 0, "per_level": 0, "unit": "%"},

        {"id": "monster_rarity", "name": "Monster Rarity", "category": "room_modifier", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "pack_size", "name": "Pack Size", "category": "room_modifier", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "portal_spawn_chance", "name": "Portal Spawn Chance", "category": "room_modifier", "base_value": 0, "per_level": 0, "unit": "%"},
        {"id": "increased_boss_spawns", "name": "Increased Boss Spawns", "category": "room_modifier", "base_value": 0, "per_level": 0, "unit": "%"}
    ],
    "derived_stats": [
        {"id": "max_life", "formula": "100 + (power * 10) + (swiftness * 5) + (level * 10)", "description": "Base 100 + Power×10 + Swiftness×5 + Level×10"},
        {"id": "max_mana", "formula": "50 + (wisdom * 8) + (level * 5)", "description": "Base 50 + Wisdom×8 + Level×5"},
        {"id": "ethereal_armor", "formula": "wisdom * 2", "description": "Wisdom×2 (Int Wizard shield)"},
        {"id": "dodge", "formula": "5.0 + (dexterity * 0.3)", "description": "Base 5% + Dex×0.3%"},
        {"id": "accuracy", "formula": "50 + (dexterity * 2) + (level * 2)", "description": "Base 50 + Dex×2 + Level×2"},
        {"id": "toughness", "formula": "5 + (swiftness * 1.5) + (level * 1)", "description": "Base 5 + Swiftness×1.5 + Level×1"}
    ]
}
```

---

## 2. ITEM DEFINITIONS (`data/items.json`)

```json
{
    "item_types": {
        "weapon": {
            "slots": ["weapon"],
            "stat_priority": ["physical_damage", "fire_damage", "frost_damage", "lightning_damage", "crit_chance", "attack_speed"],
            "base_stats": {"physical_damage": [5, 50]},
            "class_restrictions": {
                "dex": {"name": "Agility Weapon", "stat_bias": ["dexterity", "lightning_damage", "attack_speed"]},
                "int": {"name": "Wisdom Weapon", "stat_bias": ["wisdom", "frost_damage", "cast_speed"]},
                "str": {"name": "Power Weapon", "stat_bias": ["power", "physical_damage", "crit_multiplier"]},
                "any": {"name": "Generic Weapon", "stat_bias": ["physical_damage"]}
            }
        },
        "chest": {
            "slots": ["chest"],
            "stat_priority": ["max_life", "toughness", "fire_resistance", "frost_resistance", "lightning_resistance"],
            "base_stats": {"max_life": [10, 80]},
            "class_restrictions": {
                "dex": {"name": "Cloth Armor", "stat_bias": ["dodge", "movement_speed", "max_mana"]},
                "int": {"name": "Robe", "stat_bias": ["max_mana", "ethereal_armor", "mana_regen"]},
                "str": {"name": "Plate Armor", "stat_bias": ["max_life", "toughness", "stun_resistance"]},
                "any": {"name": "Leather Armor", "stat_bias": ["max_life", "dodge"]}
            }
        },
        "helmet": {
            "slots": ["helmet"],
            "stat_priority": ["max_life", "max_mana", "crit_chance", "dodge"],
            "base_stats": {"max_life": [5, 40]}
        },
        "boots": {
            "slots": ["boots"],
            "stat_priority": ["movement_speed", "dash_distance", "dodge"],
            "base_stats": {"movement_speed": [5, 30]}
        },
        "ring": {
            "slots": ["ring"],
            "stat_priority": ["crit_chance", "crit_multiplier", "mana_cost_reduction", "elemental_damage"],
            "base_stats": {"crit_chance": [1, 10]}
        },
        "necklace": {
            "slots": ["necklace"],
            "stat_priority": ["max_life", "max_mana", "life_regen", "mana_regen"],
            "base_stats": {"max_life": [5, 30]}
        }
    },

    "item_modifiers": {
        "physical_damage_percent": {"min": 10, "max": 80, "unit": "%"},
        "fire_damage_flat": {"min": 2, "max": 30},
        "frost_damage_flat": {"min": 2, "max": 30},
        "lightning_damage_flat": {"min": 2, "max": 30},
        "crit_chance_flat": {"min": 1, "max": 15, "unit": "%"},
        "crit_multiplier_flat": {"min": 0.1, "max": 0.8},
        "attack_speed_percent": {"min": 5, "max": 40, "unit": "%"},
        "cast_speed_percent": {"min": 5, "max": 40, "unit": "%"},
        "max_life_flat": {"min": 5, "max": 80},
        "max_mana_flat": {"min": 5, "max": 60},
        "life_regen_flat": {"min": 0.5, "max": 8.0},
        "mana_regen_flat": {"min": 0.5, "max": 6.0},
        "mana_cost_reduction_percent": {"min": 3, "max": 25, "unit": "%"},
        "dodge_flat": {"min": 1, "max": 12, "unit": "%"},
        "toughness_flat": {"min": 2, "max": 20},
        "ethereal_armor_flat": {"min": 5, "max": 50},
        "fire_resistance_percent": {"min": 5, "max": 40, "unit": "%"},
        "frost_resistance_percent": {"min": 5, "max": 40, "unit": "%"},
        "lightning_resistance_percent": {"min": 5, "max": 40, "unit": "%"},
        "movement_speed_percent": {"min": 3, "max": 20, "unit": "%"},
        "dash_distance_flat": {"min": 10, "max": 60, "unit": "px"},
        "dexterity_flat": {"min": 1, "max": 15},
        "wisdom_flat": {"min": 1, "max": 15},
        "power_flat": {"min": 1, "max": 15},
        "swiftness_flat": {"min": 1, "max": 15},
        "burn_chance_flat": {"min": 2, "max": 15, "unit": "%"},
        "frostbite_chance_flat": {"min": 2, "max": 15, "unit": "%"},
        "shock_chance_flat": {"min": 2, "max": 15, "unit": "%"},
        "stun_chance_flat": {"min": 2, "max": 15, "unit": "%"},
        "loot_chance_increase_flat": {"min": 2, "max": 20, "unit": "%"},
        "monster_rarity_flat": {"min": 2, "max": 20, "unit": "%"},
        "pack_size_flat": {"min": 2, "max": 15, "unit": "%"},
        "multiple_projectiles_flat": {"min": 1, "max": 3},
        "piercing_flat": {"min": 1, "max": 3}
    },

    "rarities": {
        "common": {"weight": 60, "modifier_count": 1, "roll_multiplier": 0.65, "color": "#9a9a9a"},
        "magic": {"weight": 25, "modifier_count": 2, "roll_multiplier": 0.75, "color": "#5b8af7"},
        "rare": {"weight": 10, "modifier_count": 3, "roll_multiplier": 0.85, "color": "#f7d050"},
        "epic": {"weight": 4, "modifier_count": 4, "roll_multiplier": 0.95, "color": "#a855f7"},
        "legendary": {"weight": 1, "modifier_count": 5, "roll_multiplier": 1.05, "color": "#f79025"}
    },

    "loot_table": {
        "base_drop_chance": 0.45,
        "drop_modifiers": {
            "loot_chance_increase": 0.01,
            "monster_rarity": 0.005
        },
        "drop_categories": {
            "gear": {"weight": 35, "types": ["weapon", "chest", "helmet", "boots", "ring", "necklace"]},
            "glob_health": {"weight": 20},
            "glob_mana": {"weight": 15},
            "glob_money": {"weight": 15},
            "glob_xp": {"weight": 10},
            "key": {"weight": 3, "condition": "some_doors_locked"},
            "nothing": {"weight": 2}
        }
    }
}
```

---

## 3. SKILL TREE (`data/skills.json`)

```json
{
    "skill_trees": {
        "dex": {
            "basic_attack": [
                {"id": "dex_ba_01", "name": "Projectile", "description": "Basic attack becomes a projectile.", "behaviors": ["projectile"], "prerequisites": [], "position": [0, 0]},
                {"id": "dex_ba_02", "name": "Projectile Speed", "description": "+30% projectile speed.", "modifiers": {"projectile_speed": 30}, "prerequisites": ["dex_ba_01"], "position": [1, 0]},
                {"id": "dex_ba_03", "name": "Piercing", "description": "Projectiles pierce 1 enemy.", "behaviors": ["piercing"], "modifiers": {"piercing": 1}, "prerequisites": ["dex_ba_02"], "position": [2, 0]},
                {"id": "dex_ba_04", "name": "Double Strike", "description": "Attack hits twice.", "behaviors": ["double_strike"], "prerequisites": ["dex_ba_01"], "position": [1, 1]},
                {"id": "dex_ba_05", "name": "Speed of the Wind", "description": "+20% attack speed.", "modifiers": {"attack_speed_percent": 20}, "prerequisites": ["dex_ba_04"], "position": [2, 1]},
                {"id": "dex_ba_06", "name": "Shredding Winds", "description": "Attacks shred enemy toughness.", "behaviors": ["shred_toughness"], "prerequisites": ["dex_ba_05"], "position": [3, 1]},
                {"id": "dex_ba_07", "name": "Thunderous Crackling", "description": "Adds lightning crackling to attacks.", "behaviors": ["lightning_crackle"], "prerequisites": ["dex_ba_03", "dex_ba_06"], "position": [3, 0]},
                {"id": "dex_ba_08", "name": "Culling Thunder", "description": "Execute enemies below 20% health.", "behaviors": ["culling_strike"], "prerequisites": ["dex_ba_07"], "position": [4, 0]},
                {"id": "dex_ba_09", "name": "Explode on Kill", "description": "Killed enemies explode, damaging nearby.", "behaviors": ["explode_on_kill"], "prerequisites": ["dex_ba_08"], "position": [5, 0]}
            ],
            "movement": [
                {"id": "dex_mv_01", "name": "Dash Distance", "description": "+20% dash distance.", "modifiers": {"dash_distance_percent": 20}, "prerequisites": [], "position": [0, 0]},
                {"id": "dex_mv_02", "name": "Dash Speed", "description": "+30% dash speed.", "modifiers": {"dash_speed_percent": 30}, "prerequisites": ["dex_mv_01"], "position": [1, 0]},
                {"id": "dex_mv_03", "name": "Intangible", "description": "Dash grants i-frames.", "behaviors": ["dash_iframes"], "prerequisites": ["dex_mv_02"], "position": [2, 0]},
                {"id": "dex_mv_04", "name": "Crackling Reflexes", "description": "Dash applies shock to nearby enemies.", "behaviors": ["dash_shock"], "prerequisites": ["dex_mv_03"], "position": [3, 0]},
                {"id": "dex_mv_05", "name": "Momentum", "description": "Gain momentum stacks while moving.", "behaviors": ["momentum_stacks"], "prerequisites": ["dex_mv_01"], "position": [1, 1]},
                {"id": "dex_mv_06", "name": "Momentum Damage", "description": "Damage scales with momentum stacks.", "behaviors": ["momentum_damage"], "prerequisites": ["dex_mv_05"], "position": [2, 1]},
                {"id": "dex_mv_07", "name": "Increased Damage", "description": "+15% overall damage.", "modifiers": {"damage_multiplier": 15}, "prerequisites": ["dex_mv_06"], "position": [3, 1]},
                {"id": "dex_mv_08", "name": "Shocking Path", "description": "Dash leaves shocking ground trail.", "behaviors": ["shocking_path"], "prerequisites": ["dex_mv_04", "dex_mv_07"], "position": [4, 0]},
                {"id": "dex_mv_09", "name": "Bonus Shock After Dash", "description": "+50% shock chance for 3s after dash.", "behaviors": ["dash_shock_bonus"], "prerequisites": ["dex_mv_08"], "position": [5, 0]}
            ],
            "passive": [
                {"id": "dex_ps_01", "name": "Lightning Damage", "description": "+20% lightning damage.", "modifiers": {"lightning_damage_percent": 20}, "prerequisites": [], "position": [0, 0]},
                {"id": "dex_ps_02", "name": "Shock Chance", "description": "+10% shock chance.", "modifiers": {"shock_chance_flat": 10}, "prerequisites": ["dex_ps_01"], "position": [1, 0]},
                {"id": "dex_ps_03", "name": "Shock Twice", "description": "Shock triggers twice.", "behaviors": ["shock_twice"], "prerequisites": ["dex_ps_02"], "position": [2, 0]},
                {"id": "dex_ps_04", "name": "Physical Damage", "description": "+15% physical damage.", "modifiers": {"physical_damage_percent": 15}, "prerequisites": ["dex_ps_01"], "position": [1, 1]},
                {"id": "dex_ps_05", "name": "Stun Chance", "description": "+8% stun chance on hit.", "modifiers": {"stun_chance_flat": 8}, "prerequisites": ["dex_ps_04"], "position": [2, 1]},
                {"id": "dex_ps_06", "name": "Toughness Reduction", "description": "Reduces enemy toughness by 10%.", "behaviors": ["reduce_toughness"], "prerequisites": ["dex_ps_05"], "position": [3, 1]},
                {"id": "dex_ps_07", "name": "Dodge Chance", "description": "+8% dodge.", "modifiers": {"dodge_flat": 8}, "prerequisites": ["dex_ps_03", "dex_ps_06"], "position": [3, 0]},
                {"id": "dex_ps_08", "name": "Increased Dexterity", "description": "+10 Dexterity.", "modifiers": {"dexterity_flat": 10}, "prerequisites": ["dex_ps_07"], "position": [4, 0]},
                {"id": "dex_ps_09", "name": "Crit on Dodge", "description": "Guaranteed crit after dodging.", "behaviors": ["crit_on_dodge"], "prerequisites": ["dex_ps_08"], "position": [5, 0]}
            ],
            "special_attack": [
                {"id": "dex_sa_01", "name": "Multiple Projectiles", "description": "Special fires 2 additional projectiles.", "behaviors": ["multi_projectile"], "modifiers": {"multiple_projectiles_flat": 2}, "prerequisites": [], "position": [0, 0]},
                {"id": "dex_sa_02", "name": "Forking Shuriken", "description": "Projectiles fork on hit.", "behaviors": ["fork"], "prerequisites": ["dex_sa_01"], "position": [1, 0]},
                {"id": "dex_sa_03", "name": "Storm Shurikens", "description": "Special attack summons a storm of shurikens.", "behaviors": ["storm_shuriken"], "prerequisites": ["dex_sa_02"], "position": [2, 0]}
            ]
        },

        "int": {
            "basic_attack": [
                {"id": "int_ba_01", "name": "Frost Bolt", "description": "Basic attack becomes a frost projectile.", "behaviors": ["projectile", "frost_damage"], "prerequisites": [], "position": [0, 0]},
                {"id": "int_ba_02", "name": "Frostbite on Hit", "description": "Attacks apply frostbite.", "behaviors": ["apply_frostbite"], "prerequisites": ["int_ba_01"], "position": [1, 0]},
                {"id": "int_ba_03", "name": "Ice Shards", "description": "Attack fires 3 shards in a spread.", "behaviors": ["spread_projectile"], "modifiers": {"multiple_projectiles_flat": 2}, "prerequisites": ["int_ba_02"], "position": [2, 0]},
                {"id": "int_ba_04", "name": "Piercing Cold", "description": "Projectiles pierce 2 enemies.", "behaviors": ["piercing"], "modifiers": {"piercing": 2}, "prerequisites": ["int_ba_03"], "position": [3, 0]},
                {"id": "int_ba_05", "name": "Frost Nova", "description": "Hits have a chance to trigger a frost nova.", "behaviors": ["frost_nova"], "prerequisites": ["int_ba_04"], "position": [4, 0]}
            ],
            "movement": [
                {"id": "int_mv_01", "name": "Blink", "description": "Dash becomes a teleport (blink).", "behaviors": ["blink"], "prerequisites": [], "position": [0, 0]},
                {"id": "int_mv_02", "name": "Blink Distance", "description": "+30% blink distance.", "modifiers": {"dash_distance_percent": 30}, "prerequisites": ["int_mv_01"], "position": [1, 0]},
                {"id": "int_mv_03", "name": "Ethereal Shield", "description": "Blink grants ethereal armor.", "behaviors": ["blink_shield"], "prerequisites": ["int_mv_02"], "position": [2, 0]},
                {"id": "int_mv_04", "name": "Frost Trail", "description": "Blink leaves a frost trail.", "behaviors": ["frost_trail"], "prerequisites": ["int_mv_03"], "position": [3, 0]}
            ],
            "passive": [
                {"id": "int_ps_01", "name": "Frost Damage", "description": "+25% frost damage.", "modifiers": {"frost_damage_percent": 25}, "prerequisites": [], "position": [0, 0]},
                {"id": "int_ps_02", "name": "Frostbite Chance", "description": "+15% frostbite chance.", "modifiers": {"frostbite_chance_flat": 15}, "prerequisites": ["int_ps_01"], "position": [1, 0]},
                {"id": "int_ps_03", "name": "Frostbite Duration", "description": "+50% frostbite duration.", "modifiers": {"frostbite_duration_percent": 50}, "prerequisites": ["int_ps_02"], "position": [2, 0]},
                {"id": "int_ps_04", "name": "Max Mana", "description": "+30 max mana.", "modifiers": {"max_mana_flat": 30}, "prerequisites": ["int_ps_01"], "position": [1, 1]},
                {"id": "int_ps_05", "name": "Mana Regen", "description": "+50% mana regen.", "modifiers": {"mana_regen_percent": 50}, "prerequisites": ["int_ps_04"], "position": [2, 1]},
                {"id": "int_ps_06", "name": "Mana Cost Reduction", "description": "-15% mana costs.", "modifiers": {"mana_cost_reduction_percent": 15}, "prerequisites": ["int_ps_05"], "position": [3, 1]},
                {"id": "int_ps_07", "name": "Ethereal Armor", "description": "+30 ethereal armor.", "modifiers": {"ethereal_armor_flat": 30}, "prerequisites": ["int_ps_03", "int_ps_06"], "position": [3, 0]},
                {"id": "int_ps_08", "name": "Increased Wisdom", "description": "+10 Wisdom.", "modifiers": {"wisdom_flat": 10}, "prerequisites": ["int_ps_07"], "position": [4, 0]},
                {"id": "int_ps_09", "name": "Freeze on Frostbite", "description": "Frostbite has a chance to freeze.", "behaviors": ["freeze_on_frostbite"], "prerequisites": ["int_ps_08"], "position": [5, 0]}
            ],
            "special_attack": [
                {"id": "int_sa_01", "name": "Icey Shards", "description": "Special launches a barrage of ice shards.", "behaviors": ["ice_shards"], "prerequisites": [], "position": [0, 0]},
                {"id": "int_sa_02", "name": "Blizzard", "description": "Special creates a blizzard AOE.", "behaviors": ["blizzard_aoe"], "prerequisites": ["int_sa_01"], "position": [1, 0]},
                {"id": "int_sa_03", "name": "Absolute Zero", "description": "Blizzard has a chance to freeze all enemies.", "behaviors": ["absolute_zero"], "prerequisites": ["int_sa_02"], "position": [2, 0]}
            ]
        },

        "str": {
            "basic_attack": [
                {"id": "str_ba_01", "name": "Heavy Strike", "description": "Basic attack deals +50% physical damage.", "modifiers": {"physical_damage_percent": 50}, "prerequisites": [], "position": [0, 0]},
                {"id": "str_ba_02", "name": "Cleave", "description": "Attacks hit enemies in an arc.", "behaviors": ["cleave"], "prerequisites": ["str_ba_01"], "position": [1, 0]},
                {"id": "str_ba_03", "name": "Stun Chance", "description": "+15% stun chance on hit.", "modifiers": {"stun_chance_flat": 15}, "prerequisites": ["str_ba_02"], "position": [2, 0]},
                {"id": "str_ba_04", "name": "Ground Slam", "description": "Attack becomes an AOE ground slam.", "behaviors": ["ground_slam"], "prerequisites": ["str_ba_03"], "position": [3, 0]},
                {"id": "str_ba_05", "name": "Earthshaker", "description": "Ground slam creates a shockwave.", "behaviors": ["shockwave"], "prerequisites": ["str_ba_04"], "position": [4, 0]}
            ],
            "movement": [
                {"id": "str_mv_01", "name": "Charge", "description": "Dash becomes a charge that knocks back enemies.", "behaviors": ["charge"], "prerequisites": [], "position": [0, 0]},
                {"id": "str_mv_02", "name": "Charge Distance", "description": "+30% charge distance.", "modifiers": {"dash_distance_percent": 30}, "prerequisites": ["str_mv_01"], "position": [1, 0]},
                {"id": "str_mv_03", "name": "Iron Skin", "description": "Charge grants damage reduction for 3s.", "behaviors": ["iron_skin"], "prerequisites": ["str_mv_02"], "position": [2, 0]},
                {"id": "str_mv_04", "name": "Impact Damage", "description": "Charge deals damage on impact.", "behaviors": ["charge_damage"], "prerequisites": ["str_mv_03"], "position": [3, 0]}
            ],
            "passive": [
                {"id": "str_ps_01", "name": "Physical Damage", "description": "+25% physical damage.", "modifiers": {"physical_damage_percent": 25}, "prerequisites": [], "position": [0, 0]},
                {"id": "str_ps_02", "name": "Max Life", "description": "+40 max life.", "modifiers": {"max_life_flat": 40}, "prerequisites": ["str_ps_01"], "position": [1, 0]},
                {"id": "str_ps_03", "name": "Toughness", "description": "+20 toughness.", "modifiers": {"toughness_flat": 20}, "prerequisites": ["str_ps_02"], "position": [2, 0]},
                {"id": "str_ps_04", "name": "Life Regen", "description": "+5 life regen.", "modifiers": {"life_regen_flat": 5}, "prerequisites": ["str_ps_02"], "position": [2, 1]},
                {"id": "str_ps_05", "name": "Crit Multiplier", "description": "+0.3 crit multiplier.", "modifiers": {"crit_multiplier_flat": 0.3}, "prerequisites": ["str_ps_03", "str_ps_04"], "position": [3, 0]},
                {"id": "str_ps_06", "name": "Stun Duration", "description": "+50% stun duration.", "modifiers": {"stun_duration_percent": 50}, "prerequisites": ["str_ps_05"], "position": [4, 0]},
                {"id": "str_ps_07", "name": "Increased Power", "description": "+10 Power.", "modifiers": {"power_flat": 10}, "prerequisites": ["str_ps_06"], "position": [5, 0]}
            ],
            "special_attack": [
                {"id": "str_sa_01", "name": "Whirlwind", "description": "Special becomes a whirlwind attack hitting all nearby.", "behaviors": ["whirlwind"], "prerequisites": [], "position": [0, 0]},
                {"id": "str_sa_02", "name": "Earthquake", "description": "Whirlwind ends with an earthquake AOE.", "behaviors": ["earthquake"], "prerequisites": ["str_sa_01"], "position": [1, 0]},
                {"id": "str_sa_03", "name": "Berserk", "description": "Special grants berserk mode: +50% damage, -30% damage taken for 5s.", "behaviors": ["berserk"], "prerequisites": ["str_sa_02"], "position": [2, 0]}
            ]
        }
    },

    "skill_definitions": {
        "basic_attack": {"mana_cost": 0, "cooldown": 0.0, "base_damage": 10, "damage_type": "physical"},
        "special_attack": {"mana_cost": 15, "cooldown": 4.0, "base_damage": 25, "damage_type": "physical"},
        "dash": {"mana_cost": 5, "cooldown": 1.5, "base_damage": 0, "damage_type": "physical"},
        "ethereal_shield": {"mana_cost": 10, "cooldown": 8.0, "base_damage": 0, "damage_type": "frost"},
        "teleport": {"mana_cost": 8, "cooldown": 3.0, "base_damage": 0, "damage_type": "frost"},
        "icey_shards": {"mana_cost": 15, "cooldown": 4.0, "base_damage": 20, "damage_type": "frost"},
        "shuriken_storm": {"mana_cost": 20, "cooldown": 5.0, "base_damage": 15, "damage_type": "lightning"}
    }
}
```

---

## 4. ENEMY DEFINITIONS (`data/enemies.json`)

```json
{
    "enemy_types": {
        "skeleton_warrior": {
            "name": "Skeleton Warrior",
            "sprite": "res://sprites/enemies/skeleton-warrior.png",
            "size": [48, 48],
            "base_stats": {"max_life": 50, "damage": 8, "toughness": 3, "dodge": 5, "accuracy": 70, "speed": 80},
            "scalars": {"life": 1.15, "damage": 1.10, "toughness": 1.08, "dodge": 1.02},
            "ai_type": "melee_chase",
            "aggro_radius": 200,
            "attack_range": 40,
            "attack_cooldown": 1.5,
            "xp_reward": 15,
            "money_reward": 5,
            "loot_chance": 0.40,
            "skills": ["skeleton_basic"],
            "rank": "normal",
            "color_tint": null
        },
        "skeleton_archer": {
            "name": "Skeleton Archer",
            "sprite": "res://sprites/enemies/skeleton-archer.png",
            "size": [48, 48],
            "base_stats": {"max_life": 35, "damage": 12, "toughness": 2, "dodge": 8, "accuracy": 85, "speed": 70},
            "scalars": {"life": 1.12, "damage": 1.12, "toughness": 1.05, "dodge": 1.03},
            "ai_type": "ranged_kite",
            "aggro_radius": 250,
            "attack_range": 200,
            "attack_cooldown": 2.0,
            "xp_reward": 18,
            "money_reward": 7,
            "loot_chance": 0.45,
            "skills": ["skeleton_archer_basic"],
            "rank": "normal",
            "color_tint": null
        },
        "elite_skeleton_knight": {
            "name": "Elite Skeleton Knight",
            "sprite": "res://sprites/enemies/elite-skeleton-knight.png",
            "size": [48, 48],
            "base_stats": {"max_life": 120, "damage": 15, "toughness": 8, "dodge": 5, "accuracy": 75, "speed": 90},
            "scalars": {"life": 1.20, "damage": 1.15, "toughness": 1.12, "dodge": 1.02},
            "ai_type": "melee_chase",
            "aggro_radius": 250,
            "attack_range": 45,
            "attack_cooldown": 1.2,
            "xp_reward": 50,
            "money_reward": 20,
            "loot_chance": 0.65,
            "skills": ["skeleton_basic", "skeleton_charge"],
            "rank": "elite",
            "color_tint": "#4488ff"
        },
        "mimic": {
            "name": "Mimic",
            "sprite": "res://sprites/enemies/mimic.png",
            "size": [48, 48],
            "base_stats": {"max_life": 80, "damage": 14, "toughness": 5, "dodge": 3, "accuracy": 70, "speed": 0},
            "scalars": {"life": 1.18, "damage": 1.13, "toughness": 1.10, "dodge": 1.01},
            "ai_type": "stationary_ranged",
            "aggro_radius": 180,
            "attack_range": 150,
            "attack_cooldown": 1.8,
            "xp_reward": 35,
            "money_reward": 15,
            "loot_chance": 0.55,
            "skills": ["arcane_bolt"],
            "rank": "normal",
            "color_tint": null
        },
        "elite_mimic": {
            "name": "Elite Mimic",
            "sprite": "res://sprites/enemies/elite-mimic.png",
            "size": [48, 48],
            "base_stats": {"max_life": 180, "damage": 22, "toughness": 10, "dodge": 5, "accuracy": 75, "speed": 0},
            "scalars": {"life": 1.22, "damage": 1.18, "toughness": 1.14, "dodge": 1.02},
            "ai_type": "stationary_ranged",
            "aggro_radius": 220,
            "attack_range": 180,
            "attack_cooldown": 1.5,
            "xp_reward": 80,
            "money_reward": 35,
            "loot_chance": 0.75,
            "skills": ["arcane_bolt", "mimic_curse"],
            "rank": "elite",
            "color_tint": "#aa44ff"
        },
        "dungeon_boss": {
            "name": "Dungeon Boss",
            "sprite": "res://sprites/enemies/dungeon-boss.png",
            "size": [64, 64],
            "base_stats": {"max_life": 500, "damage": 30, "toughness": 15, "dodge": 8, "accuracy": 80, "speed": 100},
            "scalars": {"life": 1.30, "damage": 1.20, "toughness": 1.15, "dodge": 1.02},
            "ai_type": "boss_chase",
            "aggro_radius": 400,
            "attack_range": 60,
            "attack_cooldown": 1.0,
            "xp_reward": 300,
            "money_reward": 150,
            "loot_chance": 1.0,
            "skills": ["boss_basic", "boss_slam", "boss_summon"],
            "rank": "boss",
            "color_tint": null
        }
    },

    "enemy_ai_types": {
        "melee_chase": "Move toward player until in attack range, then attack. Retreat slightly after attack.",
        "ranged_kite": "Maintain distance from player. Attack when in range. Retreat if player is close.",
        "stationary_ranged": "Do not move. Attack player when in range.",
        "boss_chase": "Chase player aggressively. Use multiple skills. Summon minions at 50% health."
    },

    "enemy_skills": {
        "skeleton_basic": {"damage_multiplier": 1.0, "type": "melee", "range": 40},
        "skeleton_archer_basic": {"damage_multiplier": 1.0, "type": "projectile", "speed": 200, "range": 200},
        "skeleton_charge": {"damage_multiplier": 1.5, "type": "dash", "range": 150, "cooldown": 5.0},
        "arcane_bolt": {"damage_multiplier": 1.0, "type": "projectile", "speed": 150, "range": 150, "element": "frost"},
        "mimic_curse": {"damage_multiplier": 0.5, "type": "debuff", "effect": "slow", "duration": 3.0},
        "boss_basic": {"damage_multiplier": 1.0, "type": "melee", "range": 60},
        "boss_slam": {"damage_multiplier": 2.0, "type": "aoe", "radius": 100, "cooldown": 4.0},
        "boss_summon": {"type": "summon", "enemy": "skeleton_warrior", "count": 2, "cooldown": 10.0}
    }
}
```

---

## 5. CURVES (`data/curves.json`)

```json
{
    "xp_curve": {
        "type": "exponential",
        "base": 100,
        "growth": 1.5,
        "formula": "xp_needed = floor(base * pow(growth, level - 1))",
        "values": [100, 150, 225, 338, 506, 759, 1139, 1709, 2563, 3844, 5767, 8650, 12975, 19462, 29193]
    },
    "level_up_curve": {
        "type": "linear",
        "formula": "stat_increase = base_increase + (level * per_level_scaling)"
    },
    "money_curve": {
        "type": "linear",
        "base": 5,
        "per_level": 2,
        "formula": "money_drop = base + (level * per_level)"
    },
    "enemy_stat_curve": {
        "type": "exponential",
        "formula": "stat = base_stat * pow(scalar, level - 1)",
        "scalars": {"life": 1.15, "damage": 1.10, "toughness": 1.08, "dodge": 1.02}
    },
    "item_stat_curve": {
        "type": "linear",
        "formula": "item_stat = base_stat_range * (1 + level * 0.05)",
        "base_stat_range": [5, 50]
    },
    "ability_point_curve": {
        "type": "fixed",
        "formula": "points_per_level = 1",
        "max_points": 36
    },
    "diminishing_returns_curve": {
        "type": "diminishing",
        "formula": "effective = stat / (stat + constant)",
        "constant": 50,
        "description": "Used for resistance stats to prevent 100% mitigation"
    },
    "pack_size_curve": {
        "type": "linear",
        "base": 3,
        "per_level": 0.5,
        "formula": "pack_size = floor(base + (dungeon_level * per_level))"
    },
    "rarity_chance_curve": {
        "type": "weighted",
        "base_weights": {"common": 60, "magic": 25, "rare": 10, "epic": 4, "legendary": 1},
        "per_level_adjustment": {"common": -2, "magic": 0, "rare": +1, "epic": +0.5, "legendary": +0.5}
    },
    "boss_health_curve": {
        "type": "exponential",
        "base": 500,
        "growth": 1.25,
        "formula": "boss_hp = base * pow(growth, dungeon_level - 1)"
    }
}
```

---

## 6. ROOM SETS (`data/levels.json`)

```json
{
    "dungeon_tiers": {
        "tutorial": {
            "name": "Tutorial Dungeon",
            "room_set": ["tutorial_room_01", "tutorial_room_02", "tutorial_room_03"],
            "enemy_types": ["skeleton_warrior"],
            "elite_enabled": false,
            "boss_enabled": false,
            "min_level": 1,
            "max_level": 3,
            "tileset": "tutorial_dungeon"
        },
        "tier1": {
            "name": "Dungeon Tier 1",
            "room_set": ["t1_room_01", "t1_room_02", "t1_room_03", "t1_room_04", "t1_room_05"],
            "enemy_types": ["skeleton_warrior", "skeleton_archer"],
            "elite_enabled": true,
            "elite_chance": 0.10,
            "boss_enabled": true,
            "boss_every_n_rooms": 5,
            "min_level": 3,
            "max_level": 7,
            "tileset": "stone_dungeon"
        },
        "tier2": {
            "name": "Dungeon Tier 2",
            "room_set": ["t2_room_01", "t2_room_02", "t2_room_03", "t2_room_04", "t2_room_05", "t2_room_06"],
            "enemy_types": ["skeleton_warrior", "skeleton_archer", "mimic", "elite_skeleton_knight"],
            "elite_enabled": true,
            "elite_chance": 0.15,
            "boss_enabled": true,
            "boss_every_n_rooms": 4,
            "min_level": 7,
            "max_level": 12,
            "tileset": "cave_dungeon"
        },
        "endgame": {
            "name": "Endgame Dungeon",
            "room_set": ["end_room_01", "end_room_02", "end_room_03", "end_room_04", "end_room_05", "end_room_06", "end_room_07"],
            "enemy_types": ["skeleton_archer", "mimic", "elite_skeleton_knight", "elite_mimic"],
            "elite_enabled": true,
            "elite_chance": 0.20,
            "boss_enabled": true,
            "boss_every_n_rooms": 3,
            "min_level": 12,
            "max_level": 99,
            "tileset": "overgrown_dungeon"
        }
    },

    "room_templates": {
        "tutorial_room_01": {
            "size": [15, 11],
            "tilemap": "res://rooms/tutorial_room_01.tscn",
            "spawn_points": [{"x": 3, "y": 3}, {"x": 11, "y": 3}, {"x": 7, "y": 8}],
            "door_count": 1,
            "has_key": false,
            "loot_chests": 1
        },
        "t1_room_01": {
            "size": [20, 15],
            "tilemap": "res://rooms/t1_room_01.tscn",
            "spawn_points": [{"x": 3, "y": 3}, {"x": 16, "y": 3}, {"x": 10, "y": 7}, {"x": 3, "y": 11}, {"x": 16, "y": 11}],
            "door_count": 2,
            "has_key": false,
            "loot_chests": 1
        },
        "t1_room_02": {
            "size": [20, 15],
            "tilemap": "res://rooms/t1_room_02.tscn",
            "spawn_points": [{"x": 5, "y": 5}, {"x": 15, "y": 5}, {"x": 10, "y": 10}],
            "door_count": 2,
            "has_key": true,
            "key_drop_from": "skeleton_warrior",
            "loot_chests": 2
        }
    }
}
```

---

## 7. NPC & DIALOG (`data/npcs.json`)

```json
{
    "npcs": {
        "mysterious_wizard": {
            "name": "Mysterious Wizard",
            "sprite": "res://sprites/npcs/mysterious-wizard.png",
            "services": ["identify", "respec"],
            "dialog_profile": "mysterious_wizard_profile",
            "location": "hub"
        },
        "trinket_witch": {
            "name": "Trinket Witch",
            "sprite": "res://sprites/npcs/trinket-witch.png",
            "services": ["enchant", "sell", "buy"],
            "dialog_profile": "trinket_witch_profile",
            "location": "hub"
        },
        "npc_dex_wizard": {
            "name": "Dex Wizard",
            "sprite": "res://sprites/characters/dex-wizard/south.png",
            "services": ["class_switch"],
            "dialog_profile": "dex_wizard_switch",
            "location": "hub"
        },
        "npc_int_wizard": {
            "name": "Int Wizard",
            "sprite": "res://sprites/characters/int-wizard/south.png",
            "services": ["class_switch"],
            "dialog_profile": "int_wizard_switch",
            "location": "hub"
        },
        "npc_str_wizard": {
            "name": "Str Wizard",
            "sprite": "res://sprites/characters/str-wizard/south.png",
            "services": ["class_switch"],
            "dialog_profile": "str_wizard_switch",
            "location": "hub"
        },
        "instruction_man": {
            "name": "Instruction Man",
            "sprite": "res://sprites/npcs/instruction-man.png",
            "services": ["tutorial"],
            "dialog_profile": "tutorial_profile",
            "location": "hub"
        }
    },

    "dialog_profiles": {
        "mysterious_wizard_profile": {
            "sets": [
                {
                    "id": "greeting",
                    "conditions": [],
                    "lines": ["Greetings, adventurer.", "I sense you carry unknown artifacts.", "Shall I reveal their secrets?"],
                    "responses": [
                        {"text": "Yes, identify my items.", "action": "open_identify"},
                        {"text": "I want to respec my skill tree.", "action": "open_respec"},
                        {"text": "Not now, thank you.", "action": "end_dialog"}
                    ]
                },
                {
                    "id": "identify_prompt",
                    "conditions": ["has_unidentified_items"],
                    "lines": ["I can identify these items for a small fee.", "Choose what you'd like me to reveal."],
                    "responses": [
                        {"text": "Identify all (50 gold each)", "action": "identify_all"},
                        {"text": "Let me choose.", "action": "open_identify_ui"},
                        {"text": "Never mind.", "action": "return_to_greeting"}
                    ]
                },
                {
                    "id": "respec_prompt",
                    "conditions": [],
                    "lines": ["A fresh start? Wise choice.", "This will reset your skill tree and refund all points.", "The cost is 100 gold per skill point spent."],
                    "responses": [
                        {"text": "Yes, respec my tree.", "action": "confirm_respec"},
                        {"text": "How much will it cost?", "action": "show_respec_cost"},
                        {"text": "Never mind.", "action": "return_to_greeting"}
                    ]
                }
            ]
        },
        "trinket_witch_profile": {
            "sets": [
                {
                    "id": "greeting",
                    "conditions": [],
                    "lines": ["Welcome to my shop!", "I can enchant your gear or buy your unwanted trinkets.", "What can I do for you?"],
                    "responses": [
                        {"text": "Show me your enchantments.", "action": "open_enchant"},
                        {"text": "I want to sell items.", "action": "open_sell"},
                        {"text": "I want to buy items.", "action": "open_buy"},
                        {"text": "Just browsing.", "action": "end_dialog"}
                    ]
                }
            ]
        },
        "dex_wizard_switch": {
            "sets": [
                {
                    "id": "greeting",
                    "conditions": [],
                    "lines": ["Can you take over?", "You look tired. Would you like me to take over?"],
                    "responses": [
                        {"text": "Yes, switch to Dex Wizard.", "action": "switch_class", "response_type": "Character_Change_Response", "class": "dex"},
                        {"text": "No, I'm fine.", "action": "end_dialog"}
                    ]
                }
            ]
        },
        "str_wizard_switch": {
            "sets": [
                {
                    "id": "greeting",
                    "conditions": [],
                    "lines": ["Puny Wizard begon, I'm busy right now."],
                    "responses": [
                        {"text": "Please, I need your strength.", "action": "switch_class", "response_type": "Character_Change_Response", "class": "str"},
                        {"text": "I'll come back later.", "action": "end_dialog"}
                    ]
                }
            ]
        }
    }
}
```

---

## 8. EQUIPMENT SLOTS

```json
{
    "equipment_slots": [
        {"id": "weapon", "name": "Weapon", "icon": "sword", "allowed_types": ["weapon"]},
        {"id": "chest", "name": "Chest", "icon": "chest", "allowed_types": ["chest"]},
        {"id": "helmet", "name": "Helmet", "icon": "helmet", "allowed_types": ["helmet"]},
        {"id": "boots", "name": "Boots", "icon": "boots", "allowed_types": ["boots"]},
        {"id": "ring", "name": "Ring", "icon": "ring", "allowed_types": ["ring"]},
        {"id": "necklace", "name": "Necklace", "icon": "necklace", "allowed_types": ["necklace"]}
    ]
}
```

---

## 9. GLOB PICKUPS

```json
{
    "glob_types": {
        "health_glob": {
            "sprite": "res://sprites/items/health-glob.png",
            "sound": "res://audio/sfx/health_pickup.wav",
            "effect": "heal",
            "amount_formula": "player_max_life * 0.15",
            "vfx": "res://vfx/health_pickup.tscn"
        },
        "mana_glob": {
            "sprite": "res://sprites/items/mana-glob.png",
            "sound": "res://audio/sfx/mana_pickup.wav",
            "effect": "restore_mana",
            "amount_formula": "player_max_mana * 0.15",
            "vfx": "res://vfx/mana_pickup.tscn"
        },
        "money_glob": {
            "sprite": "res://sprites/items/gold-coins.png",
            "sound": "res://audio/sfx/money_pickup.wav",
            "effect": "add_gold",
            "amount_formula": "money_curve(room_level)",
            "vfx": "res://vfx/money_pickup.tscn"
        },
        "xp_glob": {
            "sprite": "res://sprites/items/xp-glob.png",
            "sound": "res://audio/sfx/xp_pickup.wav",
            "effect": "add_xp",
            "amount_formula": "xp_curve(enemy_level) * 0.3",
            "vfx": "res://vfx/xp_pickup.tscn"
        }
    }
}
```