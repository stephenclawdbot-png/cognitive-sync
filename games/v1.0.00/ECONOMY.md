# v1.0.00 — Economy Document

**Game:** v1.0.00 (codename "wizdung")  
**Engine:** Godot 4.6.1  
**Genre:** Action RPG / Dungeon Crawler  

---

## 1. Currency System

### 1.1 Primary Currency: Money (Gold)

**Sources:**
- `Currency_glob` (Money Orb) — Dropped by enemies, picked up from ground
- `Money_Pickup.wav` — Sound confirmation on pickup
- `Money_Curve` — Scaling formula for money drops based on room/level
- `loot_chance_increase` — Increases money drop rate
- Merchant sales — Sell unwanted gear to Trinket Witch

**Sinks:**
- **Enchant Items** — Pay Trinket Witch to add modifiers to items
- **Identify Items** — Pay Mysterious Wizard to reveal unidentified items (service cost implied)
- **Respec** — Pay Mysterious Wizard to reset skill tree (service cost implied)
- **Reroll** — Rerolling item modifiers (reroll_yes/no sounds suggest cost-based rerolling)

### 1.2 Experience (XP)

**Sources:**
- `XP_glob` (XP Orb) — Dropped by enemies
- `XP_Pickup.wav` — Sound confirmation
- `XP_Curve` — Scaling formula for XP drops

**Uses:**
- Character leveling (Level_Up_Curve)
- Earns skill points for skill tree progression
- `curve_ability_point_distribution` — How many skill points per level

### 1.3 Mana (Combat Resource)

**Sources:**
- `Mana_Glob` — Dropped by enemies, restores mana
- `Mana_Regen` — Passive mana regeneration
- `Mana_Cost_Reduction` stat — Reduces skill costs

**Sinks:**
- **Basic Attack** — May have small mana cost (class-dependent)
- **Special Attack** — Higher mana cost
- **Ethereal Shield** — Consumes mana for damage absorption
- **Teleport/Blink** — Movement skill mana cost

### 1.4 Ethereal Armor (Shield Resource)

**Sources:**
- Wisdom attribute increases Max Ethereal Armor
- `Increase Max Mana and Ethereal Shield` stat

**Mechanics:**
- Separate damage absorption layer before health
- `Current_Ethereal_Armor` depletes as it absorbs damage
- Likely regenerates over time or via mana glob pickups

---

## 2. Loot Economy

### 2.1 Drop System

```
Loot_Table:
  chance_to_drop_gear: float       # Probability of gear drop
  chance_to_drop_key: float        # Probability of key drop
  chance_to_drop_glob: float       # Probability of glob drop
  key_list: [Key definitions]      # Which keys can drop
  money_glob: Resource             # Money drop definition
```

### 2.2 Drop Calculations

| Formula | Purpose |
|---------|---------|
| `Number_Of_Drops_Math` | Calculates how many items drop per kill |
| `Money_Curve` | Scales money drops with room level |
| `XP_Curve` | Scales XP drops with room level |
| `loot_chance_increase` | Bonus to base drop chances |

### 2.3 Drop Types

| Drop | Source | Pickup VFX |
|------|--------|------------|
| Gear (armor/weapon/accessory) | Enemy kills | Interactable on ground |
| Keys (Room Key, Rune Keys) | Enemy kills | Interactable on ground |
| Health Glob | Enemy kills | VFX_HealthGlob |
| Mana Glob | Enemy kills | VFX_ManaGlob |
| Money (Currency) | Enemy kills | VFX_MunnyGlob |
| XP | Enemy kills | VFX_XPGlob |

### 2.4 Rarity Distribution

Item rarity follows tiered distribution:
1. **Common** (Grey) — Most frequent drop
2. **Magic** (Blue) — Uncommon, 1-2 modifiers
3. **Rare** (Yellow) — Rare, 2-3 modifiers
4. **Epic** (Purple) — Very rare, 3+ modifiers
5. **Legendary** (Orange) — Extremely rare, best modifiers

Unidentified items mask their rarity until identified by the Mysterious Wizard.

---

## 3. Item Economy

### 3.1 Item Value Chain

```
Kill Enemy → Loot Drop → [Unidentified Item] → Identify (NPC) → 
  Equip / Sell (Merchant) / Enchant (Merchant) / Stash
```

### 3.2 Item Stat Mod Value Ranges

| Modifier Set | Stats | Value Range |
|-------------|-------|-------------|
| Core Attributes | Power, Swiftness, Wisdom | 1-5 |
| Life and Mana | Max Life, Max Mana | 1-15 |
| Defensive Core | Toughness, Dodge, Ethereal Armor | 1-10 |
| Offensive Crit | Critical Strike Chance | 1-5 |
| Offensive Damage | Damage | 1-10 |
| Offensive Debuff | Status effect chances | (variable) |
| Offensive Pen | Elemental penetration | (variable) |
| Offensive Speed | Attack/Cast Speed | (variable) |
| Utility Movement | Movement Speed | (variable) |
| Utility Mana | Mana-related | (variable) |
| Utility Room Bonus | Room-specific damage bonus | (variable) |

### 3.3 Item Scaling

Items scale with:
- `item_base_stat_scalar` — Base stat values
- `item_core_stat_scalar` — Core attribute values
- `item_regeneration_curve` — Regen stat values
- `item_room_curve` — Room-level-based scaling

Higher room levels = better item stats and higher rarity chances.

### 3.4 Gear Progression

| Tier | Armor Type | Slots |
|------|-----------|-------|
| T1 Cloth | Robe, Hat, Boots | Chest, Helmet, Boots |
| T1 Leather | Chest, Hood, Boots | Chest, Helmet, Boots |
| T1 Plate | Chest, Helmet, Boots | Chest, Helmet, Boots |
| Accessories | Rings, Necklaces | Ring, Necklace |

**Class-specific gear:**
- Agility class: Emerald accessories, Agility weapons
- Power class: Ruby accessories, Power weapons
- Wisdom class: Sapphire accessories, Wisdom weapons

---

## 4. NPC Service Economy

### 4.1 Mysterious Wizard (Djorbgripper)

| Service | Cost | Effect |
|---------|------|--------|
| **Identify Items** | Implied gold cost | Reveals hidden item stats and rarity |
| **Respec** | Implied gold cost | Refunds all skill points for re-allocation |

**Dialog triggers:**
- "Identify Items" — Opens identification UI
- "Id Like to respec" — Opens respec UI

### 4.2 Trinket Witch (Merchant)

| Service | Cost | Effect |
|---------|------|--------|
| **Enchant Items** | Gold + possibly materials | Adds/modifies item modifiers |
| **Sell Items** | N/A (player receives gold) | Converts unwanted gear to currency |
| **Reroll** | Gold (reroll_yes/no feedback) | Rerolls item modifiers |

**Dialog triggers:**
- "Enchant and Sell Items" — Opens merchant UI
- "what trinkets have you dragged up today? Or shall I work my magic on one of your goodies?"

### 4.3 Service Economy Flow

```
Dungeon Run → Collect Unidentified Gear → Return to Hub →
  Identify (pay gold) → Equip OR Sell (receive gold) OR Enchant (pay gold)
```

The identify → sell/enchant loop creates a gold circulation system where players spend gold to reveal item value, then either use the item or sell it for more gold.

---

## 5. Dungeon Economy

### 5.1 Room Level Scaling

Each room has a `Room_Level` that determines:
- Enemy level and stats (via EnemyScalar curves)
- Loot drop quality and quantity
- Money and XP drop amounts (via Money_Curve, XP_Curve)
- Pack size and rarity chances

### 5.2 Risk vs. Reward

| Factor | Effect |
|--------|--------|
| `Monster_Rarity` stat | Higher rarity = better loot, harder enemies |
| `Pack_Size` stat | More enemies = more drops, more risk |
| `Increased_Boss_Spawns` stat | More bosses = better loot, higher danger |
| `Portal_Spawn_Chance` stat | More NPC spawns = more services available |

### 5.3 Room Modifiers as Economy

Room modifier stats create an emergent economy:
- Investing in `Monster_Rarity` increases loot quality but increases difficulty
- Investing in `Pack_Size` increases loot quantity but increases danger
- Investing in `Portal_Spawn_Chance` increases NPC service availability
- Investing in `Increased_Boss_Spawns` increases boss loot but increases risk

### 5.4 Key Economy

| Key Type | Use |
|----------|-----|
| Rusty Key | Starting key (given at character creation) |
| Room Key | Opens locked doors in dungeons |
| Rune Key 001-004 | Opens special/rune-locked doors |

Keys drop from enemies (`chance_to_drop_key`) and are required for door progression. This creates a gating system where players must farm keys to access deeper dungeon areas.

### 5.5 Stash Economy

- `Treasure_Chest` / `Stash_UI` in hub area
- Stores items between dungeon runs
- Enables loot hoarding and gear swapping between character classes
- Supports the character switch system (stash gear for alternate classes)

---

## 6. Skill Tree Economy

### 6.1 Skill Points

- Earned through leveling (curve_ability_point_distribution)
- Spent on skill tree nodes
- 36 nodes per class (4 sub-trees × 9 nodes each)
- Refundable via respec (gold cost)

### 6.2 Skill Investment Strategy

**Agility (Dex Wizard) Investment Paths:**
- **Projectile Build:** Projectile → ProjectileSpeed → Piercing → DoubleStrike → MultipleProjectiles
- **Dash Build:** DashDistance → DashSpeed → Intangible → ShockingPath → BonusShockChanceAfterDash
- **Crit Build:** DodgeChance → CritChanceOnDodge → CullingThunder → ThunderousCrackling
- **Shuriken Build:** MultipleProjectiles → ForkingShuriken → StormShurikens → GiantShurikens

**Wisdom (Int Wizard) Investment Paths:**
- **Frost Build:** FrostDamage → IncreasedFrostDamage → FrostbiteChance → FrostbiteDuration → IceyTouch
- **Teleport Build:** DashDistance → ExplodeOnTeleport → ExplodeOnTeleportLand → IncreasedArea
- **Shard Build:** IncreasedShards → IceyShardExplosion → ChanneledIce → IceOnDeath
- **Area Build:** IncreasedSize → GreaterArea → CircleOfCold → IncreasedChannelDuration

### 6.3 respec Economy

- respec refunds skill points
- Costs gold (service from Mysterious Wizard)
- Allows build experimentation without permanent commitment
- Creates gold sink for players who want to try different builds

---

## 7. Currency Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        DUNGEON RUN                          │
│                                                             │
│  Kill Enemy → [Gear] [Key] [Health Glob] [Mana Glob]       │
│              [Money Glob] [XP Glob]                         │
│                                                             │
│  Room Level → Scales enemy stats, loot quality, drop rates  │
│  Room Modifiers → Player invests stats for better rewards  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                        HUB AREA                             │
│                                                             │
│  ┌─────────────────┐  ┌──────────────────┐                  │
│  │ Mysterious Wizard│  │ Trinket Witch    │                 │
│  │                  │  │ (Merchant)       │                 │
│  │ • Identify (pay) │  │ • Sell (earn)    │                 │
│  │ • Respec (pay)   │  │ • Enchant (pay)  │                 │
│  └─────────────────┘  │ • Reroll (pay)    │                 │
│                        └──────────────────┘                 │
│                                                             │
│  ┌─────────────────┐  ┌──────────────────┐                  │
│  │ Stash            │  │ Character Switch │                 │
│  │ (store items)    │  │ (change class)   │                 │
│  └─────────────────┘  └──────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Economy Balance Observations

### 8.1 Positive Feedback Loops
- Better gear → Kill faster → More loot → Better gear
- Higher room level → Better drops → Better gear → Can do higher room level
- More gold → More enchanting/identifying → Better gear → More gold

### 8.2 Negative Feedback Loops
- Inventory full → Must return to hub → Must sell/stash → Breaks farming loop
- Death → Lose non-permanent room progress → Must restart room
- Mana depletion → Must find mana glob → Slows combat
- Key required → Must farm for key → Gates progression

### 8.3 Gold Circulation
```
Earn gold (kills) → Spend gold (identify) → 
  Sell identified item (earn gold) → Spend gold (enchant) → 
    Better item → Kill faster → Earn more gold
```

### 8.4 Time Economy
- Dungeon runs take time (room by room progression)
- Hub services take time (identify each item, enchant each item)
- Stash management takes time (organize gear for multiple classes)
- Room level progress is non-permanent (lost on returning to hub)

---

## 9. Key Economy Formulas

### 9.1 Drop Chance Formula
```
drop_roll = random()
if drop_roll < chance_to_drop_gear:
    drop_gear()
if drop_roll < chance_to_drop_key:
    drop_key_from(key_list)
if drop_roll < chance_to_drop_glob:
    drop_glob(money_glob)
```

### 9.2 Number of Drops
```
num_drops = Number_Of_Drops_Math(room_level, loot_chance_increase)
```

### 9.3 Money Scaling
```
money_amount = Money_Curve(room_level) × enemy_scalar
```

### 9.4 XP Scaling
```
xp_amount = XP_Curve(room_level) × enemy_scalar
```

### 9.5 Enemy Stat Scaling
```
enemy_life = base_life × EnemyScalar_Life(room_level) × (is_elite ? EnemyScalar_Elite_Life : 1)
enemy_damage = base_damage × EnemyScalar_Damage(room_level) × (is_elite ? EnemyScalar_Elite_Damage : 1)
```

### 9.6 Item Stat Scaling
```
item_stat_value = base_value × item_base_stat_scalar(item_level) × modifier_curve(rarity)
```

### 9.7 XP Per Level
```
xp_required = XP_Curve(level) × Level_Up_Curve(level)
skill_points_earned = curve_ability_point_distribution(level)
```

---

## 10. Monetization Implications

While the game appears to be a standalone title (no microtransaction evidence in extracted data), the economy design supports potential extensions:

- **Stash tabs** — Could be sold as expansions
- **Character slots** — If more classes were added
- **Cosmetic skins** — VFX variations, character skins
- **Convenience items** — Auto-identify, bulk enchant
- **Time-saving** — XP boosters, money boosters

The core loop (dungeon → loot → hub → upgrade → dungeon) is self-sustaining without monetization, but the systems are modular enough to support it.

---

## 11. Summary

The v1.0.00 economy is a **loot-driven ARPG economy** with these key characteristics:

1. **Dual currency** — Gold (economy) + XP (progression), both earned from kills
2. **Service-based gold sinks** — Identify, enchant, respec, reroll
3. **Loot rarity tiers** — 5 tiers + unidentified state
4. **Room-level scaling** — Higher rooms = better rewards, harder enemies
5. **Key-gated progression** — Must farm keys to advance
6. **Stash-based persistence** — Store gear between runs and for alternate classes
7. **Skill tree investment** — Permanent (until respec) character build choices
8. **Character switching** — Swap between 3 classes, share stash

The economy creates a satisfying loop: **fight → loot → return → identify → equip/sell/enchant → fight harder**. The room modifier system adds player agency in risk-reward tuning, while the key system gates progression to prevent skipping content.