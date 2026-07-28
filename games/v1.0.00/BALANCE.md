# v1.0.00 "wizdung" — Balance & Progression Document

> **Purpose:** All balance formulas, damage calculations, loot probability tables, XP curves, and progression pacing.
> **Audience:** Game designer, balance designer, QA.
> **Companion docs:** GAME_MECHANICS.md, DATA_MODELS.md, ARCHITECTURE.md

---

## 1. DAMAGE CALCULATION

### 1.1 Full Damage Formula

```
INCOMING DAMAGE TO TARGET:

raw_damage = (attacker_base_damage + attacker_elemental_damage) × attacker_damage_multiplier

CRIT CHECK:
  if random() < attacker_crit_chance:
    raw_damage ×= attacker_crit_multiplier

DEFENSE:
  mitigated = raw_damage - target_toughness_reduction
  elemental_mitigated = raw_damage × (1 - target_elemental_resistance_clamped)
  
  DIMINISHING RETURNS:
    effective_resistance = resistance / (resistance + 50)
    # 50% resistance → 50/(50+50) = 50% actual mitigation
    # 75% resistance → 75/(75+50) = 60% actual mitigation
    # 100% resistance → 100/(100+50) = 66.7% actual mitigation
  
DODGE CHECK:
  if random() < target_dodge_chance:
    final_damage = 0  # fully dodged
  else:
    final_damage = max(1, mitigated - target_toughness)

ETHREAL ARMOR (Int Wizard shield):
  if target has ethereal_armor > 0:
    absorbed = min(ethereal_armor, final_damage)
    ethereal_armor -= absorbed
    final_damage -= absorbed
```

### 1.2 Example Calculation

```
Dex Wizard attacks Skeleton Warrior (Level 5):

Attacker:
  base_damage = 12 (weapon)
  lightning_damage = 8 (from skill tree)
  damage_multiplier = 1.0 (no buffs)
  crit_chance = 12%
  crit_multiplier = 1.5x

Target:
  toughness = 5 + (5-1) * 1.0 = 9 (level 5, base 5, per_level 1)
  lightning_resistance = 0
  dodge = 5 + (5-1) * 0.2 = 5.8%

RAW: (12 + 8) × 1.0 = 20
CRIT: random() < 0.12 → YES → 20 × 1.5 = 30
TOUGHNESS: 30 - 9 = 21
RESISTANCE: 21 × (1 - 0) = 21
DODGE: random() < 0.058 → NO
FINAL: max(1, 21) = 21 damage

Skeleton has 50 + (5-1) * 50 * 0.15^4... 
  life = 50 × 1.15^4 = 50 × 1.749 = 87.5
  Takes 21 damage → 66.5 HP remaining
```

### 1.3 DPS Reference Values

| Player Level | Expected DPS | vs Normal Enemy | vs Elite | vs Boss |
|-------------|-------------|-----------------|----------|---------|
| 1 | 15 | Kill in 3-4 hits | N/A | N/A |
| 5 | 30 | Kill in 3 hits | 4-5 hits | N/A |
| 10 | 55 | Kill in 1-2 hits | 3-4 hits | 10-12 hits |
| 15 | 85 | One-shot | 2-3 hits | 6-8 hits |
| 20 | 120 | One-shot | 1-2 hits | 4-5 hits |

---

## 2. XP & LEVELING CURVE

### 2.1 XP Required Per Level

| Level | XP Needed | Cumulative | Kill Count (normal enemy) |
|-------|-----------|-----------|--------------------------|
| 1→2 | 100 | 100 | 7 |
| 2→3 | 150 | 250 | 8 |
| 3→4 | 225 | 475 | 9 |
| 4→5 | 338 | 813 | 11 |
| 5→6 | 506 | 1,319 | 13 |
| 6→7 | 759 | 2,078 | 15 |
| 7→8 | 1,139 | 3,217 | 16 |
| 8→9 | 1,709 | 4,926 | 18 |
| 9→10 | 2,563 | 7,489 | 21 |
| 10→11 | 3,844 | 11,333 | 25 |
| 11→12 | 5,767 | 17,100 | 31 |
| 12→13 | 8,650 | 25,750 | 37 |
| 13→14 | 12,975 | 38,725 | 46 |
| 14→15 | 19,462 | 58,187 | 54 |
| 15→16 | 29,193 | 87,380 | 67 |
| 20→21 | 98,842 | ~330k | 165 |
| 25→26 | 334,475 | ~1.1M | 418 |

**Formula:** `xp_needed = floor(100 × 1.5^(level - 1))`

### 2.2 XP Sources

| Source | XP Amount | Formula |
|--------|----------|---------|
| Normal enemy kill | 15 | `15 × enemy_level` |
| Elite enemy kill | 50 | `50 × enemy_level` |
| Boss kill | 300 | `300 × dungeon_level` |
| XP glob pickup | 15% of kill XP | `enemy_xp × 0.3` (glob is 30% of kill XP, split between glob + direct) |
| Room clear bonus | 50 | `50 × room_level` |

### 2.3 Skill Points

- 1 skill point per level
- Max 36 skill points (all nodes in one class tree)
- Respec cost: 100 gold × skill points spent
- Respec refunds all points, resets tree

---

## 3. LOOT PROBABILITY TABLES

### 3.1 Drop Chance Per Enemy

| Enemy Rank | Base Drop Chance | Modifier |
|-----------|-----------------|----------|
| Normal | 45% | +0.4% per loot_chance_increase stat |
| Elite | 65% | +0.4% per loot_chance_increase stat |
| Boss | 100% | Always drops (guaranteed) |

### 3.2 Drop Category Weights

| Category | Weight | Probability (base) | Notes |
|----------|--------|-------------------|-------|
| Gear (weapon/armor/etc) | 35 | 35% | Random type, random rarity |
| Health glob | 20 | 20% | Heal 15% max life |
| Mana glob | 15 | 15% | Restore 15% max mana |
| Money glob | 15 | 15% | Gold based on money_curve |
| XP glob | 10 | 10% | 30% of kill XP |
| Key | 3 | 3% | Only if room has locked doors |
| Nothing | 2 | 2% | No drop |

### 3.3 Rarity Distribution

| Rarity | Base Weight | At Level 1 | At Level 10 | At Level 20 |
|--------|------------|------------|-------------|-------------|
| Common | 60 → 58 → 56 | 58.0% | 56.0% | 54.0% |
| Magic | 25 | 25.0% | 25.0% | 25.0% |
| Rare | 10 → 11 → 12 | 11.0% | 12.0% | 13.0% |
| Epic | 4 → 4.5 → 5 | 4.5% | 5.0% | 5.5% |
| Legendary | 1 → 1.5 → 2 | 1.5% | 2.0% | 2.5% |

**Adjustment:** Common weight decreases by 2 per 10 levels, redistributed to Rare/Epic/Legendary.

### 3.4 Item Stat Roll Ranges

| Rarity | Modifiers | Roll Range (% of max) |
|--------|-----------|----------------------|
| Common | 1 | 50-80% |
| Magic | 2 | 60-90% |
| Rare | 3 | 70-100% |
| Epic | 4 | 80-110% |
| Legendary | 5 | 90-120% |

**Example:** A "physical_damage_percent" modifier has max=80%.
- Common roll: 40% to 64%
- Legendary roll: 72% to 96%

---

## 4. ECONOMY BALANCE

### 4.1 Gold Flow

**Sources (per dungeon level cleared):**

| Source | Gold | Notes |
|--------|------|-------|
| Money glob drops | 20-40 | From 3-5 enemies per room |
| Item sales | 10-100 | Sell to Trinket Witch (10-25% of item value) |
| Boss kill | 150-300 | `150 × dungeon_level` |

**Sinks:**

| Sink | Cost | Notes |
|------|------|-------|
| Identify item | 50 × item_level | Per unidentified item |
| Enchant item | 200 × item_level | Add one modifier |
| Reroll modifier | 150 × item_level | Reroll one modifier |
| Respec skill tree | 100 × points_spent | Full tree reset |
| Buy item from shop | 100-1000 | Rotating shop inventory |

### 4.2 Expected Gold Per Run

| Dungeon Level | Enemies/Room | Rooms/Run | Gold/Run | Time/Run |
|--------------|-------------|-----------|----------|---------|
| 1-3 | 3-4 | 3 | 60-120 | 3-5 min |
| 4-6 | 4-5 | 4 | 150-250 | 5-8 min |
| 7-10 | 5-6 | 5 | 300-500 | 8-12 min |
| 11-15 | 6-8 | 5 | 600-1000 | 10-15 min |
| 16-20 | 8-10 | 6 | 1200-2000 | 15-20 min |

### 4.3 Service Cost Balance

| Service | Cost at Lvl 5 | Cost at Lvl 10 | Cost at Lvl 20 |
|---------|--------------|---------------|---------------|
| Identify | 250 | 500 | 1000 |
| Enchant | 1000 | 2000 | 4000 |
| Respec (full tree) | 3600 | 3600 | 3600 |
| Reroll | 750 | 1500 | 3000 |

**Target:** A player should be able to identify all gear from one run (3-5 items) without going broke. Enchanting is a luxury for endgame.

---

## 5. ENEMY SCALING

### 5.1 Enemy Stat Scaling Per Level

| Stat | Base (Lvl 1) | Growth | At Lvl 5 | At Lvl 10 | At Lvl 20 |
|------|-------------|--------|----------|-----------|-----------|
| **Skeleton Warrior** | | | | | |
| Health | 50 | ×1.15/level | 87 | 202 | 818 |
| Damage | 8 | ×1.10/level | 12 | 21 | 54 |
| Toughness | 3 | ×1.08/level | 4 | 6 | 14 |
| **Elite Skeleton Knight** | | | | | |
| Health | 120 | ×1.20/level | 249 | 745 | 5,715 |
| Damage | 15 | ×1.15/level | 26 | 61 | 242 |
| Toughness | 8 | ×1.12/level | 14 | 25 | 77 |
| **Dungeon Boss** | | | | | |
| Health | 500 | ×1.25/level | 1,220 | 4,657 | 67,910 |
| Damage | 30 | ×1.20/level | 62 | 186 | 1,668 |
| Toughness | 15 | ×1.15/level | 26 | 61 | 242 |

### 5.2 Player Stat Scaling Per Level

| Stat | Base (Lvl 1) | Per Level | At Lvl 5 | At Lvl 10 | At Lvl 20 |
|------|-------------|-----------|----------|-----------|-----------|
| Max Life | 100 | +10 | 150 | 200 | 300 |
| Max Mana | 50 | +5 | 75 | 100 | 150 |
| Power | 10 | +2 | 18 | 28 | 48 |
| Dexterity | 10 | +2 | 18 | 28 | 48 |
| Wisdom | 10 | +2 | 18 | 28 | 48 |
| Toughness | 5 | +1 | 9 | 14 | 24 |
| Dodge | 5% | +0.2% | 5.8% | 7% | 9% |
| Accuracy | 50 | +2 | 58 | 70 | 90 |

### 5.3 Player vs Enemy Balance Target

| Level | Enemy HP | Player DPS | Time to Kill | Player HP | Enemy DPS | Time to Kill Player |
|-------|---------|-----------|-------------|-----------|-----------|-------------------|
| 1 | 50 | 15 | 3.3s | 100 | 8 | 12.5s |
| 5 | 87 | 30 | 2.9s | 150 | 12 | 12.5s |
| 10 | 202 | 55 | 3.7s | 200 | 21 | 9.5s |
| 15 | 468 | 85 | 5.5s | 250 | 36 | 6.9s |
| 20 | 818 | 120 | 6.8s | 300 | 54 | 5.6s |

**Target:** Player should kill normal enemies in 3-7 hits (2-5 seconds). Player should survive 5-12 seconds against a single enemy without dodging. Dodging extends survival significantly.

---

## 6. DUNGEON PROGRESSION

### 6.1 Difficulty Curve

| Dungeon Level | Tier | Enemy Types | Pack Size | Elite Chance | Boss Every N Rooms |
|--------------|------|-------------|-----------|-------------|-------------------|
| 1-3 | Tutorial | Skeleton only | 3 | 0% | No boss |
| 4-7 | Tier 1 | Skeleton + Archer | 4 | 10% | Every 5 rooms |
| 8-12 | Tier 2 | + Mimic + Elite Knight | 5 | 15% | Every 4 rooms |
| 13+ | Endgame | + Elite Mimic | 6 | 20% | Every 3 rooms |

### 6.2 Pack Size Formula

```
pack_size = floor(3 + (dungeon_level × 0.5))
```

| Dungeon Level | Pack Size |
|--------------|-----------|
| 1 | 3 |
| 5 | 5 |
| 10 | 8 |
| 15 | 10 |
| 20 | 13 |

### 6.3 Room Clear Time Target

| Enemy Count | Target Clear Time | Notes |
|------------|------------------|-------|
| 3 enemies | 10-15 seconds | Fast room |
| 5 enemies | 15-25 seconds | Standard room |
| 8 enemies | 25-40 seconds | Hard room |
| Boss room | 30-60 seconds | Boss + 2-3 minions |

---

## 7. CLASS BALANCE

### 7.1 Class Identity Matrix

| Aspect | Dex Wizard | Int Wizard | Str Wizard |
|--------|-----------|-----------|-----------|
| Primary Stat | Dexterity | Wisdom | Power |
| Damage Type | Lightning + Physical | Frost | Physical |
| Health | Low (100 base) | Medium (120 base) | High (150 base) |
| Mana | Medium (50 base) | High (80 base) | Low (30 base) |
| Mobility | High (dash + projectiles) | Medium (blink + frost) | Low (charge) |
| Range | Long (projectiles) | Long (frost bolts) | Short (melee) |
| Defense | Dodge-based | Ethereal Armor | Toughness-based |
| Playstyle | Hit-and-run | Area control | Face-tank |
| Difficulty | Medium | Hard | Easy |

### 7.2 Damage Type Balance

| Element | Effect | DPS Multiplier | Utility |
|---------|--------|---------------|---------|
| Physical | Stun chance | 1.0x (baseline) | Stun interrupts |
| Fire | Burn DoT | 0.9x initial + DoT | Sustained damage |
| Frost | Frostbite (slow) | 0.85x + slow | Crowd control |
| Lightning | Shock (chain) | 0.95x + chain | Multi-target |

**Design intent:** Physical = reliable, Fire = ramp damage, Frost = control, Lightning = AoE clear.

### 7.3 Skill Tree Node Value Comparison

Each node should provide approximately 8-12% power increase:

| Node Type | Value Range | Example |
|-----------|------------|---------|
| Damage % | +15-25% | "Lightning Damage +20%" |
| Defensive | +10-20% | "Dodge +8%" |
| Behavior change | Variable | "Projectile" (melee → ranged) |
| Utility | Special | "Intangible" (i-frames on dash) |

---

## 8. STATUS EFFECT BALANCE

### 8.1 Effect Magnitudes

| Effect | Chance Source | Duration | Tick Damage/Effect | Resistance |
|--------|--------------|----------|-------------------|-----------|
| Burn | burn_chance % | 3s | 20% of hit damage per second | burn_resistance % |
| Frostbite | frostbite_chance % | 3s | 40% movement speed slow | frostbite_resistance % |
| Shock | shock_chance % | 1.5s | 10% of hit damage + chains to nearby | shock_resistance % |
| Stun | stun_chance % | 1s | Target cannot act | stun_resistance % |
| Freeze | Special (skill) | 2s | Target cannot move or act | frost_resistance % |

### 8.2 Status Effect Stacking Rules

- **Burn:** Stacks up to 3 times (refreshes duration, adds damage)
- **Frostbite:** Stacks up to 2 times (increases slow to 70%)
- **Shock:** Does NOT stack (refreshes duration, chains again)
- **Stun:** Does NOT stack (immune for 2s after stun ends)
- **Freeze:** Does NOT stack (immune for 5s after freeze ends)

---

## 9. DEATH & PENALTY

### 9.1 Death Rules

| Event | Consequence |
|-------|------------|
| Die in dungeon | Lose non-permanent room level progress |
| Die in dungeon | Keep all gear, XP, gold |
| Die in dungeon | Return to hub |
| Die to boss | Boss resets (must fight again) |
| Die in hub | Cannot die in hub (safe zone) |

### 9.2 "Non-Permanent Room Level Progress"

This means: the dungeon level you reached resets to your last checkpoint level.
- Enter dungeon at level 5 → clear rooms 5, 6, 7, 8 → die on room 9
- You keep all gear, XP, gold earned
- Your "highest cleared level" is still 8
- But you restart the dungeon at level 5 (or the level you entered at)

This creates tension without frustration — you never lose meaningful progress.

---

## 10. BALANCE TESTING CHECKLIST

### 10.1 Combat Feel Tests

- [ ] Level 1 Dex Wizard kills Skeleton Warrior in 3-4 hits (2-3 seconds)
- [ ] Level 1 Str Wizard kills Skeleton Warrior in 2-3 hits (2-3 seconds)
- [ ] Level 1 Int Wizard kills Skeleton Warrior in 3-4 hits (3-4 seconds, slower but more CC)
- [ ] Player survives 5+ seconds against 1 enemy without dodging
- [ ] Player survives 10+ seconds with active dodging
- [ ] Crit feels impactful (visible number, screen shake, audio sting)
- [ ] Dash i-frames are ~0.3s (enough to dodge one attack, not two)

### 10.2 Economy Tests

- [ ] After 1 dungeon run (5 rooms, level 5), player has 150-250 gold
- [ ] Identifying 3 items costs 750 (level 5) — affordable after 1 run
- [ ] Enchanting costs 1000 (level 5) — requires 2-3 runs to afford
- [ ] Respec (full tree, 10 points) costs 1000 — affordable after 2-3 runs

### 10.3 Progression Tests

- [ ] Level 1→5 takes ~15 minutes (first dungeon run)
- [ ] Level 5→10 takes ~30 minutes
- [ ] Level 10→15 takes ~1 hour
- [ ] Level 15→20 takes ~2 hours
- [ ] Each class feels distinctly different within 5 minutes of play
- [ ] First legendary drop creates excitement (orange frame, 5 modifiers)

### 10.4 Difficulty Tests

- [ ] Tutorial (levels 1-3) is always winnable, no frustration
- [ ] Tier 1 (levels 4-7) requires some dodging, some gear
- [ ] Tier 2 (levels 8-12) requires good gear + some skill tree investment
- [ ] Endgame (levels 13+) requires optimized build + good play
- [ ] Boss fights last 30-60 seconds (not too long, not too short)