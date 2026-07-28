# 1 Speed for Jetpack - Complete Analysis

**Game:** 1 Speed for Jetpack  
**Platform:** Roblox  
**Date Analyzed:** 2025-02-15  
**Analyst:** Max ⚡  
**Player Account:** admiralthefinest

---

## 🎯 Executive Summary

"1 Speed for Jetpack" is a **Step Simulator / Obby Hybrid** where players walk on treadmills to earn steps, level up to increase speed, unlock jetpacks, and navigate obby stages. Classic idle + skill hybrid with heavy monetization.

---

## 🔄 Core Gameplay Loop

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  TREADMILL → STEPS → LEVEL UP → SPEED ↑ → JETPACK UNLOCK    │
│       ↑                                                      │
│       └──────── OBBY (bonus steps, uses energy) ────────────┘
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

1. **Walk on treadmill** → Earn steps passively
2. **Accumulate steps** → Fill level bar
3. **Level up** → Speed increases (+2 per level observed)
4. **Higher speed** → Earn steps faster
5. **Reach level thresholds** → Unlock jetpacks
6. **Do obby** → Bonus steps (+1 to +10 per platform)

---

## 💰 Economy System

### Currencies

| Currency | Source | Use |
|----------|--------|-----|
| **Steps** | Treadmills, Obby pads | Level progression |
| **Trophies 🏆** | Leveling, Purchases | Step upgrades (+20, +40, +80 steps) |
| **Robux (R$)** | Real money | Multipliers, VIP, Step packs |

### Multiplier Pricing (Observed)

| Multiplier | Robux Cost |
|------------|------------|
| x2 | 3 R$ |
| x4 | 9 R$ |
| x8 | 25 R$ |
| x16 | 39 R$ |
| x32 | 79 R$ |
| x64 | 129 R$ |
| x128 | 199 R$ |

### VIP Tiers

| Tier | Cost | Benefits |
|------|------|----------|
| VIP | 79 R$ | x2 Steps treadmill access |
| VIP+ | 249 R$ | x4 Steps treadmill access |

### Step Upgrades (Trophy Cost)

| Upgrade | Trophy Cost |
|---------|-------------|
| +20 steps | 🏆 400 |
| +40 steps | 🏆 1,000 |
| +80 steps | 🏆 2,000+ |

---

## 📊 Progression Observed

### Level → Speed Correlation
| Level | Speed | Steps Needed |
|-------|-------|--------------|
| 1 | ~1 | 39 |
| 4 | ~10 | 222 |
| 6 | ~16 | 394 |
| 8 | ~22 | 636 |
| 10 | 28 | 950 |
| 11 | 30 | 1,100 |
| 12 | 32 | 1,300 |
| 13 | 34 | 1,500 |
| 14 | 36 | 1,700 |

**Pattern:** ~+2 speed per level, steps needed grows ~15% per level

### Energy System
- Starts at **10/10**
- Scales with level (reached **12/12** at level 12)
- Used for **obby jumping**
- Regenerates over time

---

## 🚀 Jetpack System

### Jetpacks Observed

| Jetpack | Est. Level Req | Trophy Price |
|---------|----------------|--------------|
| Jetpack 1 | 10 | FREE |
| Jetpack 2 | 25 | 35 |
| Jetpack 3 | 40 | ? |
| Jetpack 4 | 60 | 500 |
| Jetpack 5 | 80 | ? |
| Pulse Jetpack | 100+ | 7,300 |

Jetpacks are **cosmetic** + possible speed bonuses.

---

## 🎮 Treadmill System

### Treadmill Types

| Type | Color | Multiplier | Access |
|------|-------|------------|--------|
| Basic | Gray/Blue | x1 | Free |
| VIP | Yellow/Orange | x2 | VIP Required |
| VIP+ | Cyan | x4 | VIP+ Required |

### Mechanics
- Walk on treadmill to earn steps
- Steps/second = Speed × Treadmill Multiplier × Multiplier Gamepass
- Sign: "NO SPACE? MORE TREADMILLS UPSTAIRS!"

---

## 🗺️ Stage System

### Stages Discovered

| Stage | Theme | Bonus Pad Values |
|-------|-------|------------------|
| Stage 1 | Gray industrial | +1 yellow, +2 pink |
| Stage 2 | Lava/Tropical 🌋 | +5 yellow, +10 pink |
| Stage 3 | Purple | +5 yellow, +10 pink |
| Stage 4 | (glimpsed) | Higher? |

### Obby Mechanics
- Jump between platforms
- Each platform = +1 step (base)
- Colored pads give bonus steps
- **Energy cost** per jump
- Fall = respawn at checkpoint (penalty?)

---

## 🏁 Racing System

- **"A race is starting in X seconds. Join?"**
- **Requirement: Level 50**
- **1st Place Reward: +20 gems** 💎
- Endgame competitive content

---

## 🏆 Leaderboards

### Trophy Leaderboard (Top Players)
1. Brunitls2_0 - 4619.9t
2. M5_kosuke - 4160.4t
3. caloxx289 - 2000.3t
4. jammar01 - 420.5t
5. FUEGO5435JH - 403.9t

(Note: "t" = trillion - massive numbers!)

### Playtime Leaderboard
1. PigGOD1914 - **397 hours**
2. NoodlemanThomas - 300h
3. justlen101232 - 272h

Players grind HUNDREDS of hours!

---

## 🛒 Shop / Monetization

### Left Side UI
- **Rebirth** button (prestige system?)
- **Skins** button
- **Worlds** button

### Right Side UI
- **x2 Multiplier: ONLY 3 Robux!**
- **+25k** steps button
- **+150k** steps button
- **+2m** steps button

### Limited Items
- **"Ancient Loadpoint"** - Exclusive golden wings skin
- **4275/5000 left** (decreasing, FOMO!)
- Creates urgency to purchase

### Crates System
- Gacha/lootbox for skins
- Likely Robux or trophy cost

---

## 🎯 Badge System

- **9 badges** tracked at top of screen
- Progress through badges as achievements
- Observed completing badges 1-7 during session

---

## 💡 Monetization Hooks

| Hook | Implementation |
|------|----------------|
| **Time Skip** | Buy step packs (+25k, +150k, +2m) |
| **Multipliers** | x2 to x128 multipliers stack |
| **VIP Access** | Better treadmills (x2, x4 steps) |
| **Limited FOMO** | "4275/5000 left!" counter |
| **Leaderboards** | Competitive drive to spend |
| **Playtime Rewards** | Incentivize long sessions |
| **Crates** | Gacha cosmetics |

---

## 📝 Session Statistics

| Metric | Start | End | Time |
|--------|-------|-----|------|
| Level | 1 | 14 | ~10 min |
| Steps | 0 | ~1,700 | |
| Speed | 1 | 36 | |
| Energy Max | 10 | 12 | |
| Jetpacks | 0 | 1 | |

---

## 🔧 Technical Notes

### UI Layout
- **Top:** Badge progress (1-9)
- **Left:** Rebirth, Skins, Worlds, Party slots
- **Right:** Multiplier buttons, Leaderboards
- **Bottom:** Level bar, Energy bar, Multiplier indicators

### Controls
- **WASD** - Movement
- **Space** - Jump (obby)
- **E** - Interact (exit treadmill)

---

## 📁 Reverse Engineering Docs

Full implementation guides available in:
`I:\Reverse Engine Roblox\Games\ReverseEngineering\`

1. **01_JetpackSystem.md** - Level-gated unlock system
2. **02_MonsterSystem.md** - Stage 2 hazard AI
3. **03_BrainrotSpawnSystem.md** - Random collectible spawning

---

## 🎮 Clone Recommendations

### Must-Have
1. Treadmill step generation
2. Level → Speed progression
3. Jetpack unlock milestones
4. Multi-stage obby with bonus pads
5. Energy system for obby

### Nice-to-Have
1. VIP treadmills
2. Racing at level 50
3. Rebirth/prestige system
4. Skin crates
5. Playtime leaderboard

### Monetization
1. Multiplier gamepasses (x2 to x128)
2. VIP/VIP+ tiers
3. Step packs (instant boost)
4. Limited exclusive cosmetics
5. Crate keys

---

*Analysis complete. Ready for Phase 3: Build Clone.*
