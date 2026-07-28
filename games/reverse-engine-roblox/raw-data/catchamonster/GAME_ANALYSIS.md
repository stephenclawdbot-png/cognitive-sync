# 🎮 CATCH A MONSTER — Complete Game Analysis

**Game:** [🏕️] Catch a Monster  
**Developer:** LDS II  
**Rating:** 96% 👍  
**Players:** ~10.6K  
**Genre:** Monster Collector / Pokémon-style RPG  
**Analyzed:** 2026-01-26

---

## 📊 OVERVIEW

A Pokémon-inspired monster catching and battling game on Roblox. Players explore different islands, catch monsters, level them up, and compete on weekly leaderboards.

---

## 💰 ECONOMY

| Currency | Icon | Purpose |
|----------|------|---------|
| **Cash** | $ | Basic currency for purchases |
| **Robux** | ⓡ | Premium purchases (likely) |
| **Event tokens?** | ? | Rift Ball Event rewards |

**Starting cash:** ~$86 observed at Level 3

---

## 👤 PLAYER PROGRESSION

| Element | Details |
|---------|---------|
| **Player Level** | XP-based (160/590 for Lv.3→4) |
| **Level unlocks** | Pet slots (Lv.7 unlocks slot 2) |
| **Friend Luck** | Social multiplier (+0% base, invite friends) |

---

## 🐾 MONSTER SYSTEM

### Monster Stats
- **Name** — Unique creature name
- **Level** — Starts low, gains XP
- **Type** — Elemental/category (Nature, Ice, etc.)
- **Health bar** — Color-coded by type?

### Observed Monsters
| Name | Level | Notes |
|------|-------|-------|
| Dummee | Lv.6 | Yellow bar, likely starter |
| Leafet | Lv.6 | Green/nature type |
| Ice Dragons | Lv.32+ | Wild, high-level zone |

### Party System
- **Active slots** — Multiple monsters out at once
- **Slot unlocks** — Level-gated (Lv.7 for slot 2)
- **??? slot** — Mystery unlock (Lv.? or achievement?)

---

## 🗺️ WORLD SYSTEM

### Zones
- **Starting zone** — Ice/Snow themed
- **World Portal** — "Travel to any island"
- **Multiple biomes** — Implied by portal system

### Zone Features
- Wild monster spawns (zone-specific)
- Gift boxes in central areas
- Leaderboard displays
- Other players visible

---

## 🎛️ UI LAYOUT

```
[≡][💬][🎮]                                    [⚙️][🎁][📤]

[Event Timer]                              [leiven (respawn)]
[Rift Ball Event]
[Ends in: 5D]

[Party Display]                              [World Portal]
[Monster 1: Dummee Lv.6]                    Travel to any island
[Monster 2: Leafet Lv.6]
                                              [Shop]
                                              [Return]
                                              [Inventory]
                    PLAYER                    [Pet] ⚠️
                    Lv.3                      [Index]
                                              [Mount]
                                              [Achieve]
                                              [Task] ⚠️

[Friend Luck +0%] [Invite]  [$86]    [🔒Lv.7] [???]

              [====== Level 3 (160/590) ======]
```

---

## 🔘 MENU BUTTONS

| Button | Function | Notes |
|--------|----------|-------|
| **Shop** | In-game store | Purchases |
| **Return** | Teleport home/spawn | Quick travel |
| **Inventory** | Backpack/items | Storage |
| **Pet** | Monster management | Has notification (!) |
| **Index** | Pokédex/collection log | Track all monsters |
| **Mount** | Rideable creatures | Speed boost |
| **Achieve** | Achievements | Rewards |
| **Task** | Daily/weekly quests | Has notification (!) |

---

## 🏆 COMPETITIVE FEATURES

### Weekly Leaderboards
1. **Weekly Hatch** — Most eggs hatched
2. **Weekly Collection Points** — Catching score
3. **Weekly Capture** — Total catches

### Social
- Friend Luck bonus system
- Invite button for recruitment
- Multiplayer world (see other players)

---

## 🎪 EVENTS

| Event | Duration | Type |
|-------|----------|------|
| **Rift Ball Event** | 5 days remaining | Limited-time content |
| **Upcoming** | Jan 30 9PM | Mystery event (???) |

---

## 🔄 CORE GAMEPLAY LOOPS

### 1. CATCH LOOP
```
Explore Zone → Find Wild Monster → Battle/Weaken → Capture → Add to Collection
```

### 2. LEVEL LOOP
```
Use Monster → Gain XP → Level Up → Stronger Stats → Unlock Abilities/Evolution?
```

### 3. COLLECT LOOP
```
Catch New Species → Fill Index → Hatch Eggs → Complete Collection
```

### 4. COMPETE LOOP
```
Catch/Hatch → Earn Points → Weekly Leaderboard → Rewards?
```

### 5. EXPLORE LOOP
```
Level Up → Unlock New Islands → Find Rarer Monsters → Repeat
```

---

## 💎 MONETIZATION (Predicted)

| Type | Items |
|------|-------|
| **Gamepasses** | Extra pet slots, auto-catch, luck boost |
| **Robux Shop** | Premium monsters, eggs, cosmetics |
| **Event passes** | Rift Ball rewards |

---

## 📋 CLONE SPECIFICATION

### Data Structures

```lua
-- Monster Template
Monster = {
    id = "leafet_001",
    name = "Leafet",
    type = "Nature",
    rarity = "Common",
    level = 1,
    xp = 0,
    xpToNext = 100,
    stats = {
        hp = 50,
        attack = 10,
        defense = 8,
        speed = 12
    },
    moves = {"Tackle", "Leaf Whip"},
    evolves_to = "Leafeon",
    evolves_at = 16
}

-- Player Data
Player = {
    level = 1,
    xp = 0,
    cash = 0,
    party = {}, -- Active monsters (max 2-3)
    storage = {}, -- All caught monsters
    index = {}, -- Discovered species
    mounts = {},
    achievements = {},
    tasks = {}
}
```

### Core Systems Needed

1. **Monster Database**
   - Species definitions
   - Stats, types, rarities
   - Evolution chains

2. **Catching System**
   - Encounter triggers
   - Catch success calculation
   - Ball/tool types?

3. **Battle System**
   - Turn-based or real-time?
   - Type advantages
   - Move system

4. **Party Management**
   - Slot limits (level-gated)
   - Switch active monsters
   - Heal/restore

5. **Index/Pokédex**
   - Track seen vs caught
   - Rarity display
   - Completion rewards

6. **World/Zone System**
   - Multiple islands
   - Portal travel
   - Zone-specific spawns

7. **Egg/Hatching System**
   - Obtain eggs
   - Hatch timer or steps
   - Random monster result

8. **Mount System**
   - Rideable creatures
   - Speed multipliers
   - Unlock requirements

9. **Event System**
   - Timed events
   - Special rewards
   - Exclusive monsters

10. **Leaderboard System**
    - Weekly resets
    - Multiple categories
    - Rank rewards

---

## ❓ UNKNOWN (Need More Gameplay)

- [ ] Battle mechanics details
- [ ] Catch minigame specifics
- [ ] Shop contents/prices
- [ ] Evolution triggers
- [ ] Mount unlock requirements
- [ ] Full monster roster
- [ ] Type effectiveness chart
- [ ] Egg sources and costs

---

## 🎯 KEY TAKEAWAYS FOR PETWIN

Relevant mechanics to consider:

1. **Level-gated slots** — Incentivizes player progression
2. **Weekly leaderboards** — Drives engagement & competition
3. **Friend Luck system** — Viral growth mechanic
4. **Index completion** — Collection motivation
5. **Multi-zone exploration** — Content depth
6. **Event rotation** — Keeps game fresh
7. **Mount system** — Aspirational unlocks

---

*Analysis by Max ⚡ | 2026-01-26*
