# Legendum — Economy Document

**Engine:** Godot 4.6.2  
**Version:** v0.14.1 (demo)  

---

## 1. Currency System

### 1.1 Primary Currencies

| Currency | Code | Source | Sink | Persistence |
|----------|------|--------|------|-------------|
| Gold | reward_gold | Quests, jobs, combat, trading | Shops, item purchases | Per-life (lost on death) |
| Goods (Exploration Points) | reward_goods | Exploration, quests | Unlocking areas, trading | Per-life |
| XP | reward_xp | Combat, jobs, tasks | Consumed by leveling | Per-life |
| Legend Points (LP) | reward_lp | Quests, deeds, encounters | Soul Perks | **Permanent (meta)** |
| Resolve Points (RP) | reward_rp | Special quests | Character resolve abilities | Per-life |
| Skill Points (SP) | reward_sp | Skill activities | Perk unlocks | Per-life |

### 1.2 Goods Sub-Types
Goods are region-specific exploration points:
- EXPLORATION_POINTS_PRISON — Earned in prison origin
- EXPLORATION_POINTS_ROADS — Earned on roads
- EXPLORATION_POINTS_TOWN — Earned in town
- EXPLORATION_POINTS_WOODLANDS — Earned in woodlands

---

## 2. Gold Economy

### 2.1 Gold Sources
| Source | Method | Notes |
|--------|--------|-------|
| Quests | reward_gold | Primary source, varies by quest |
| Jobs | Job payment | Roguery jobs give "extra coin on the side" |
| Combat | Enemy drops | Not explicitly confirmed but implied |
| Trading | Sell items to shops | Shop trader UI |
| Tasks | mod_task_money | Tasks can give money |

### 2.2 Gold Sinks
| Sink | Method | Notes |
|------|--------|-------|
| Item purchases | Shop system | Buy weapons, armor, consumables |
| Shop upgrades | Improve trader stock | Quest-gated |
| Inn | buy_rounds | Buy rounds at inn |
| Chapel donations | chapel_donation | Piety-related gold sink |
| Slums leave | Save up to leave slums | Gold-gated progression |

### 2.3 Gold Modifiers
- **mod_task_money** — Items can modify task money output
- **Shop Discount perk** — 10% off all shop prices
- **Pickpocket perk** — Extra coin from roguery activities
- **Traveling Merchant** — Dynamic pricing/stock

---

## 3. XP Economy

### 3.1 XP Types
| XP Type | Source | Use |
|---------|--------|-----|
| Character XP | Combat, quests | Character level |
| Attribute XP | Combat (focused training) | Attribute levels (STR, DEX, VIG, PER, INT, WIS) |
| Skill XP | Jobs, tasks | Skill levels (Blades, Archery, Mining, etc.) |
| Job XP | Job performance | Job rank/tier |

### 3.2 XP Modifiers
| Modifier | Effect | Source |
|----------|--------|--------|
| boost_xp_output | +XP from tasks | Items |
| boost_job_xp_output | +Job XP | Items |
| mod_global_xp_gain | +All XP | Items |
| eff_boost_xp_gain | +XP gain | Items |
| Perk: Dreamer | Trickle XP in STR/DEX/PER/INT/WIS | Scales with character level |
| Perk: (skill) +20% SP | +20% SP gain for specific skill | Perks |
| Time-of-day | Task speed varies by time | Morning/Evening slots |

### 3.3 Leveling Curves
- **lvl_curve** — Standard XP curve
- **lvl_data** — XP data table
- **smart_lvl_curve** — Adaptive leveling curve
- Attribute levels observed up to 80+
- Higher levels require exponentially more XP

---

## 4. Legend Points (LP) Economy

### 4.1 LP Sources
| Source | Amount | Notes |
|------|--------|-------|
| Quest completion | Varies | Main story quests |
| Deeds | Varies | Permanent choice records |
| Encounter completion | Varies | Special encounters |
| Training Grounds upgrade | +40 LP | Specific quest |
| Merchant improvement | 1 Legacy | Specific quest |

### 4.2 LP Sinks
| Sink | Cost | Notes |
|------|------|-------|
| Soul Perks | Varies | Permanent meta-progression |
| Legend Rank advancement | Accumulative | Rank up system |

### 4.3 LP Persistence
- **Permanent across all lives** — the core meta-progression currency
- Earned during life, spent between lives
- Encourages replayability and meaningful choices

---

## 5. Shop Economy

### 5.1 Shop Structure
Each shop has:
- **ShopStock** — Current available items
- **ShopItemPool** — Pool of possible items
- **ShopItemWeighted** — Weighted random selection
- **ShopTier** — Quality tier of shop
- **ShopItem** — Individual item listing with price

### 5.2 Shop Types
| Shop | NPC | Specialization |
|------|-----|----------------|
| Mizgrub | Goblin trader | General goods, quirky items |
| Father Alric | Church priest | Religious items, holy texts |
| Village Trader | Town merchant | General store |
| Goods Peddler | Traveling merchant | Random/limited stock |
| Ilaf | NPC | Specialized shop |

### 5.3 Shop Dynamics
- **Shop Shortages** — Random events affecting stock (shop_shortages.res)
- **Shop Upgrades** — Quests can improve shop stock permanently
- **Shop Discounts** — Perk gives 10% off
- **Dynamic Pricing** — Peddler and traveling merchant have variable prices
- **Mizgrub's Trading** — "Good trades! Fair prices! ...Mostly fair." — Slightly unpredictable

### 5.4 Item Pricing
Item prices scale with:
- Item tier/rarity
- Item type (weapon > armor > consumable)
- Shop tier
- Whether item is guaranteed vs weighted random

---

## 6. Item Economy

### 6.1 Item Value Chain
```
Loot Drops → Inventory → Equipment / Sell to Shop / Consume
                                    ↓
                              Gold / Stats
```

### 6.2 Item Tiers (by damage progression)
**Weapons (Sword example):**
| Tier | Name | Damage |
|------|------|--------|
| T1 | Training Sword | 4-5 |
| T2 | Old Sword | 5-6 |
| T3 | Sturdy Sword | 6-7 |
| T4 | Mighty Sword | 7-8 |
| T5 | Sword 2 | 8-9 |
| T6 | Sword 3 | 10-11 |
| T7 | Sword 4 | 11-12 |
| T8 | Greatsword 3 | 13-14 |
| T9 | Giant's Sword | 15-16 |
| T10 | Duality Blade | 16-18 |

### 6.3 Rarity System
| Rarity | Border Color | Drop Rate |
|--------|---------------|-----------|
| Unawoken | Special | N/A (locked) |
| Gray | Gray | Common |
| Green | Green | Uncommon |
| Blue | Blue | Rare |
| Red | Red | Epic |
| Gold | Gold | Legendary |
| White | White | Mythic |
| Destiny | Special | Destiny-tier |

### 6.4 Loot System
- **LootTable** — Defines possible drops
- **LootTableEntry** — Individual drop entry
- **guaranteed_items** — Always drop
- **fixed_items** — Fixed set of items
- **extra_items** — Random additional items
- **discoveries** — Special loot from exploration (loot.lost_temple, loot.woodlands1, loot.woodlands2)
- **Loot modifiers**: Dense perk (+25% loot chance in Wilds)

---

## 7. Energy & Task Economy

### 7.1 Energy System
- Tasks cost energy (mod_task_energy)
- Resting recovers energy (task_rest)
- Max energy can be modified (mod_max_energy)
- Energy management is a core resource allocation decision

### 7.2 Task Economics
Each task has:
- **Energy cost** — How much energy it uses
- **Time cost** — How long it takes (affected by speed modifiers)
- **XP reward** — Skill/attribute XP gained
- **Money reward** — Gold earned
- **Item rewards** — Possible item drops
- **Time-of-day modifier** — Some tasks are faster at certain times

### 7.3 Task Modifiers
| Modifier | Effect |
|----------|--------|
| boost_task_speed | Faster task completion |
| boost_task_speed_time_of_day | Faster at specific times |
| boost_task_lvl | Higher task level |
| boost_job_xp_output | More XP from job |
| mod_task_energy | Less energy per task |
| mod_task_money | More money per task |

---

## 8. Time Economy

### 8.1 Time as a Resource
- **Calendar system** — Days, seasons, years
- **Life stages** — Character ages through stages, stats decline
- **Limited time per life** — Can't do everything in one life
- **Time-of-day slots** — Morning, Day, Evening (some unlocked by perks)
- **Day duration** — Can be modified by items (eff_day_duration)

### 8.2 Seasons
| Season | Icon | Notes |
|--------|------|-------|
| Greenrise | icon_season_greenrise | Spring/early |
| Highsun | icon_season_highsun | Summer |
| Amberfall | icon_season_amberfall | Autumn |

### 8.3 Turn of the Year
- Annual event (turn_of_the_year.res)
- Likely resets or refreshes certain systems

---

## 9. Progression Economy

### 9.1 Per-Life Progression (Reset on Death)
- Character level
- Attribute levels
- Skill levels
- Gold
- Items (except heirlooms)
- Perks
- Abilities
- Story progress
- World state
- Contacts
- Quest progress

### 9.2 Permanent Progression (Kept Across Lives)
- Legend Points (LP)
- Legend Rank
- Soul Perks
- Heirlooms
- Meta state

### 9.3 Deed Economy
Deeds are permanent records that:
- Track player's moral choices (spare/execute Mizgrub)
- Record achievements (saved caravans, upgraded training grounds)
- May affect future lives (narrative references)
- Are reviewed at end of life (ui_life_review_deed.scn)

---

## 10. Contact Economy

### 10.1 Contact System
- Contacts are NPCs with relationships
- Each contact provides "yield" (ui_contact_yield.scn)
- Contacts can be unlocked via quests (reward_contact)
- Contacts provide: shop access, quest opportunities, bonuses, story

### 10.2 Known Contacts
- Ashvale Merchant (contact.ashvale_merchant)
- Mizgrub the Goblin trader
- Father Alric (church)
- Helga (combat trainer)
- Grey Wizard (mentor)
- Lunorak (scholar)

---

## 11. Heirloom Economy

### 11.1 Heirloom System
- Heirlooms are **permanent items** kept across lives
- Earned through special quests (reward_heirloom)
- Stored in meta-state
- Examples: temple_relic_coffer, gold ring from garden

### 11.2 Heirloom Impact
- Provides starting bonuses in new lives
- Can be equipped from the start
- Encourages completing specific questlines

---

## 12. Overall Economic Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     SINGLE LIFE CYCLE                        │
│                                                              │
│  Origin → Jobs/Tasks → XP/Gold/SP → Stats/Skills/Perks      │
│            ↓                    ↓                             │
│         Combat → Items → Equipment → Better Combat           │
│            ↓                    ↓                             │
│         Quests → Deeds → LP/RP → Soul Perks                  │
│            ↓                                                │
│         Aging → Death → Life Review                          │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    META-PROGRESSION                          │
│                                                              │
│  Legend Points → Soul Perks → Better Next Life               │
│  Heirlooms → Starting Items → Early Advantage               │
│  Legend Rank → Unlock Content → More Options                 │
│  Deeds → Narrative Consequences → Story Variations          │
└─────────────────────────────────────────────────────────────┘
```

---

## 13. Economy Balance Observations

### 13.1 Sinks vs Sources
- **Gold**: Multiple sinks (shops, inn, donations) and sources (quests, jobs, combat)
- **XP**: Primary sink is leveling; sources are diverse (combat, tasks, quests)
- **LP**: Limited sources (specific quests/deeds), spent on permanent upgrades
- **Energy**: Daily resource, recovered by resting, spent on tasks
- **Time**: Ultimate limited resource — can't max everything in one life

### 13.2 Progression Pace
- Early game: Gold-starved, focus on basic jobs and training
- Mid game: Equipment upgrades, perk web expansion, region unlocking
- Late game: LP farming, heirloom collection, deed completion
- Meta game: Soul perk optimization, legend rank climbing

### 13.3 Monetization Potential
The game is currently single-player with no microtransactions. Potential monetization:
- Cosmetic heirlooms
- Additional origins
- Bonus soul perk slots
- Extra life stage content
- New regions (Valenthar is locked behind "NOT AVAILABLE IN DEMO")

---

## 14. Key Economic Formulas (Inferred)

### 14.1 Damage Formula
```
damage = random(damage_min, damage_max) * scaling_damage * weapon_damage_modifier
```

### 14.2 XP Gain
```
xp_gained = base_xp * (1 + global_xp_modifier) * (1 + task_xp_modifier) * time_of_day_modifier
```

### 14.3 Task Completion
```
time_to_complete = base_time / (1 + task_speed_modifier) * time_of_day_modifier
energy_cost = base_energy * (1 - energy_reduction_modifier)
```

### 14.4 Shop Price
```
price = base_price * (1 - shop_discount) * shop_tier_multiplier
```

### 14.5 Loot Chance
```
drop_chance = base_drop_rate * (1 + loot_chance_modifier) * region_modifier
```

### 14.6 Level Requirement
```
xp_for_level(n) = base_xp * growth_rate^n (using lvl_curve / smart_lvl_curve)
```

---

## Summary

Legendum's economy is built on the tension between **limited time (one life)** and **permanent progression (across lives)**. The player must make meaningful choices about what to prioritize each life — combat vs. skills vs. narrative vs. gold — knowing that only Legend Points, Soul Perks, Heirlooms, and Deeds carry forward. This creates a compelling roguelite loop where each life feels both meaningful and transient.