# 🎮 YOUR ZOO! — Complete Game Analysis

**Game:** Your Zoo! 🦆  
**Rating:** 97% 👍  
**Players:** ~5.2K  
**Genre:** Zoo Tycoon / Animal Collector / Gacha  
**Tags:** EARNS OFFLINE  
**Analyzed:** 2026-01-26

---

## 📊 OVERVIEW

A zoo-themed collection game where players buy crates to get animals, build their zoo, and earn money. Features a gacha crate system with guaranteed rare drops on timers, rebirth prestige, and offline earnings.

---

## 💰 ECONOMY

| Currency | Icon | Purpose |
|----------|------|---------|
| **Cash** | $ | Main currency ($500 observed) |
| **Robux** | ⓡ | Premium purchases |

### Income
- **Money Boost** — 0% base (upgradeable with +)
- **Offline earnings** — "EARNS OFFLINE" feature

---

## 🎰 CRATE/GACHA SYSTEM

### Crate Types
| Crate | Cost | Luck | Notes |
|-------|------|------|-------|
| **Basic Crate** | $100 | 1x | Standard |
| **Golden Crate** | ? | Higher | Guaranteed timer |
| **Rainbow Crate** | ? | Higher | Guaranteed timer |
| **Secret Crate** | ? | Highest | Guaranteed timer |

### Guaranteed Drop Timers (Pity System)
| Tier | Timer |
|------|-------|
| GOLDEN | 47 seconds |
| RAINBOW | 4m 47s |
| SECRET | 14m 47s |

This is a **pity system** — keeps players opening crates knowing a rare is coming!

---

## 🔄 REBIRTH SYSTEM

- **Rebirth button** visible (red cap icon)
- **"Rebirthing will NOT reset animals!"** — Key selling point
- Players keep collection, reset cash for multipliers

---

## 🗺️ NAVIGATION

| Tab | Function |
|-----|----------|
| **Shrines** | Boost/upgrade area? |
| **Home** | Main zoo/hub |
| **Sell** | Sell animals for cash |

---

## 🎛️ UI LAYOUT

```
[≡][💬][🎮]                [Shrines][Home][Sell]           [DAILY!][🎁][⚙️]

                         [REBIRTH SIGN]
                    "Rebirthing will NOT reset animals!"
                    
[🛒 Shop]              [Guaranteed GOLDEN in 47s!]           [🎨 Skins]
                       [Guaranteed RAINBOW in 4m 47s!]
[🔄 Rebirth]           [Guaranteed SECRET in 14m 47s!]       [Starter Pack]
                                                              Ⓡ6 | 9m 47s
[📖 Index]                  [Buy a Box!]                     
                          Basic Crate                        [New!] Ⓡ129
[🧲 Collect All]           1x Luck                          
                            $100                             [2x Cash] Ⓡ189

[$500]                                              
[🐻 0%] [+]
Money Boost                    [🎒]
                            Pet Slot
```

---

## 🔘 MENU BUTTONS

| Button | Icon | Function |
|--------|------|----------|
| **Shop** | 🛒 | Store for purchases |
| **Rebirth** | 🔄 | Prestige reset |
| **Index** | 📖 | Animal collection tracker |
| **Collect All** | 🧲 | Auto-collect from zoo |
| **Skins** | 🎨 | Cosmetics |
| **Daily** | 📅 | Daily rewards |

---

## 💎 MONETIZATION

| Item | Price | Type |
|------|-------|------|
| **Starter Pack** | 6 Robux | Limited time (9m 47s) |
| **New! Item** | 129 Robux | Special offer |
| **2x Cash** | 189 Robux | Permanent multiplier |

---

## 🔄 CORE GAMEPLAY LOOPS

### 1. CRATE LOOP
```
Earn Cash → Buy Crates → Open → Get Animals → Place in Zoo
```

### 2. COLLECT LOOP
```
Animals in Zoo → Generate Cash → Collect All → Buy More Crates
```

### 3. REBIRTH LOOP
```
Reach Threshold → Rebirth → Keep Animals → Cash Multiplier → Faster Progress
```

### 4. PITY LOOP
```
Open Crates → Timer Counts Down → Guaranteed Rare → Excitement → Open More
```

### 5. INDEX LOOP
```
Get New Animals → Fill Index → Chase Rare Variants → Complete Collection
```

---

## 🎯 UNIQUE MECHANICS

### 1. Guaranteed Pity Timers
Instead of pure RNG, players know EXACTLY when they'll get a rare:
- Creates anticipation
- Reduces frustration
- Encourages "just one more" behavior

### 2. Rebirth Keeps Animals
- Removes fear of losing collection
- Makes rebirth feel rewarding, not punishing
- Smart retention design

### 3. Offline Earnings
- "EARNS OFFLINE" in thumbnail
- Respects player time
- Encourages daily returns

### 4. Collect All Button
- Quality of life feature
- One-click harvesting
- Reduces tedium

---

## 📋 CLONE SPECIFICATION

### Data Structures

```lua
-- Player Data
Player = {
    cash = 0,
    rebirths = 0,
    rebirthMultiplier = 1,
    moneyBoost = 0,  -- percentage
    
    animals = {},     -- owned animals
    zoo = {},         -- placed animals (generating income)
    index = {},       -- discovered species
    
    -- Pity timers (crates opened since last guaranteed)
    pityCounters = {
        golden = 0,
        rainbow = 0,
        secret = 0
    },
    
    -- Guaranteed thresholds
    pityThresholds = {
        golden = 10,    -- ~47 seconds worth
        rainbow = 60,   -- ~4m 47s worth  
        secret = 180    -- ~14m 47s worth
    },
    
    offlineTime = 0,
    lastLogin = timestamp
}

-- Animal Template
Animal = {
    id = "lion_001",
    name = "Lion",
    rarity = "Rare",        -- Common, Rare, Epic, Legendary, Secret
    variant = nil,          -- Golden, Rainbow, etc.
    incomePerSecond = 10,
    placed = false,
    zooSlot = nil
}

-- Crate Template
Crate = {
    id = "basic_crate",
    name = "Basic Crate",
    cost = 100,
    luck = 1,
    lootTable = {
        {rarity = "Common", chance = 70},
        {rarity = "Rare", chance = 20},
        {rarity = "Epic", chance = 8},
        {rarity = "Legendary", chance = 2}
    }
}
```

### Core Systems Needed

1. **Crate/Gacha System**
   - Purchase crates
   - Roll loot table
   - Pity timer tracking
   - Guaranteed drops

2. **Pity Timer System**
   - Track opens per tier
   - Display countdown
   - Force drop at threshold
   - Reset after guaranteed

3. **Zoo Placement**
   - Grid or slot-based
   - Place animals
   - Visual display
   - Income generation

4. **Income System**
   - Per-animal earnings
   - Passive generation
   - Money boost multiplier
   - Collect All function

5. **Offline Earnings**
   - Track time away
   - Calculate earnings (capped?)
   - Welcome back popup
   - Claim rewards

6. **Rebirth System**
   - Threshold requirement
   - Reset cash only
   - Keep animals
   - Increment multiplier

7. **Index/Collection**
   - Track all species
   - Show owned vs total
   - Rarity breakdown
   - Completion rewards?

8. **Sell System**
   - Sell unwanted animals
   - Convert to cash
   - Clear duplicates

9. **Shrine System**
   - Boost mechanic
   - Upgrade area
   - (Need more exploration)

---

## 🎯 KEY TAKEAWAYS FOR PETWIN

Excellent mechanics to consider:

1. **Pity Timer Display** — Shows exact countdown to guaranteed rare
   - Reduces gacha frustration
   - Creates anticipation
   - "I'm only 47s away from a Golden!"

2. **Rebirth Preserves Collection** — Huge QoL
   - Players never lose progress on what matters (animals)
   - Only reset soft currency
   - Makes rebirth feel good, not punishing

3. **Offline Earnings** — Respects player time
   - Come back to rewards
   - Daily login motivation
   - Doesn't require 24/7 grinding

4. **Collect All** — One-click convenience
   - Reduces tedium
   - Quality of life feature
   - Players appreciate this

5. **Visible Timers on Purchases** — Urgency
   - "Starter Pack 9m 47s" creates FOMO
   - Limited-time offers convert better

---

## 📈 TYPICAL PROGRESSION

```
New Player:
  Get $100 → Buy Basic Crate → Get first animal → Place in zoo
  
Early Game:
  Collect income → Buy more crates → Fill zoo → Watch pity timers
  
Mid Game:
  Golden guaranteed! → Better animals → More income → First rebirth
  
Late Game:
  Stack rebirths → Rainbow/Secret hunting → Complete Index
  
End Game:
  Max collection → All variants → Flex zoo → Help newbies
```

---

*Analysis by Max ⚡ | 2026-01-26*
