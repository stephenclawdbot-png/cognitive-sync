# Catapult Chaos 🏰💥

**Status:** SAVED - Angry Birds meets Knockout
**Theme:** Medieval siege warfare
**Style:** Turn-based aiming + Physics destruction

---

## 🎮 Core Concept

Players stand on castle walls. Take turns launching BOULDERS at each other. Aim direction + set power (like Knockout!). Knock players off or destroy their walls. Walls crumble over time. Last one standing wins.

**The Twist:** Knockout mechanics + destructible environment + medieval theme.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                      CATAPULT CHAOS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → All players spawn on CASTLE WALLS                        │
│      → Each player has own wall section                         │
│      → Castle surrounds central void                            │
│      → Everyone has a CATAPULT                                  │
│                                                                 │
│   2. AIM PHASE (5 seconds per player)                           │
│      → Turn-based: one player aims at a time                    │
│      → OR simultaneous: everyone aims together                  │
│      → Set DIRECTION (where to shoot)                           │
│      → Set POWER (how hard to launch)                           │
│      → Can target PLAYERS or WALLS                              │
│                                                                 │
│   3. FIRE PHASE                                                 │
│      → "FIRE!"                                                  │
│      → All boulders launch                                      │
│      → Physics simulation                                       │
│      → Boulders fly, arc, land                                  │
│                                                                 │
│   4. DESTRUCTION PHASE                                          │
│      → Boulder hits PLAYER = knockback                          │
│      → Enough knockback = fall off = eliminated                 │
│      → Boulder hits WALL = wall takes damage                    │
│      → Wall destroyed = player loses footing                    │
│                                                                 │
│   5. CRUMBLE PHASE (Every 3 rounds)                             │
│      → Outer walls crumble automatically                        │
│      → Less safe space each time                                │
│      → Forces players toward center                             │
│                                                                 │
│   6. VICTORY                                                    │
│      → Last player with wall intact = WINNER                    │
│      → Or last player not fallen                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏰 Castle Layout

### Arena Design
```
              ┌─────────────┐
         ┌────┤   WALL 1    ├────┐
         │    │  [Player]   │    │
    ┌────┤    └─────────────┘    ├────┐
    │    │                       │    │
    │  W │                       │ W  │
    │  A │                       │ A  │
    │  L │       V O I D         │ L  │
    │  L │      (center)         │ L  │
    │    │                       │    │
    │  2 │                       │ 3  │
    │    │                       │    │
    └────┤    ┌─────────────┐    ├────┘
         │    │   WALL 4    │    │
         └────┤  [Player]   ├────┘
              └─────────────┘

- 4-8 players, each on wall section
- Central void (fall = death)
- Walls face inward
- Can shoot across
```

### Wall Structure
```
WALL HEALTH: 100 HP

SECTIONS:
┌─────────────────────┐
│ BATTLEMENTS (25 HP) │ ← Player stands here
├─────────────────────┤
│ UPPER WALL (35 HP)  │
├─────────────────────┤
│ LOWER WALL (40 HP)  │
└─────────────────────┘

DESTRUCTION:
- Battlements gone = no cover
- Upper wall gone = unstable footing
- Lower wall gone = COLLAPSE (player falls)
```

---

## 🎯 Aiming System

### Aim Controls
```
DIRECTION:
- Rotate catapult left/right
- Full 180° arc
- Aim at any other player/wall

POWER:
- 1-10 scale
- Higher = farther, faster
- Lower = shorter, precise

TRAJECTORY:
- Dotted line shows arc (limited preview)
- Wind affects flight (optional)
```

### Power vs Distance
| Power | Distance | Speed | Knockback |
|-------|----------|-------|-----------|
| 1-3 | Short | Slow | Light |
| 4-6 | Medium | Medium | Medium |
| 7-9 | Long | Fast | Heavy |
| 10 | Max | Very Fast | MASSIVE |

---

## 💥 Projectile Types

### Standard Boulder
| Property | Value |
|----------|-------|
| Damage to Wall | 20 HP |
| Knockback | Medium |
| Splash | Small area |

### Unlockable Ammo (Earned/Shop)
| Ammo | Effect | Cost |
|------|--------|------|
| Fire Boulder | Burns, damage over time | $200 |
| Scatter Shot | 3 smaller boulders | $150 |
| Heavy Stone | 2x damage, slower | $250 |
| Bouncy Ball | Bounces once | $100 |
| Bomb | Explosion, big splash | $300 |

---

## 🧱 Wall Mechanics

### Wall Damage
```
BOULDER HIT:
- Direct hit = 20 damage
- Splash damage = 10 nearby

FIRE DAMAGE:
- 5 damage per second
- Burns for 3 seconds
- Spreads to adjacent sections

STRUCTURAL DAMAGE:
- Lower section destroyed = upper unstable
- Upper unstable + hit = collapse
- Collapse = player falls
```

### Wall Repair (Optional Mode)
- Between rounds, can repair
- Costs resources (earned from hits)
- Partial repair only (10 HP max)

---

## ⏱️ Turn System Options

### Option A: Turn-Based (Like Worms)
```
SEQUENCE:
- Player 1 aims + fires
- See result
- Player 2 aims + fires
- See result
- Repeat in order

PROS:
- Strategic, calculated
- Watch each shot
- Mind games

CONS:
- Slower pace
- Waiting time
```

### Option B: Simultaneous (Like Knockout!)
```
SEQUENCE:
- Everyone aims at same time (5 sec)
- Everyone fires together
- All boulders fly at once
- Chaos ensues

PROS:
- Fast paced
- Less waiting
- More chaotic

CONS:
- Less strategic
- Harder to track
```

### Recommended: SIMULTANEOUS
- Matches Roblox attention spans
- Faster rounds
- More exciting

---

## 📉 Crumble System

### Automatic Crumbling
| Round | Effect |
|-------|--------|
| 1-3 | Full walls |
| 4-6 | Outer 20% crumbles |
| 7-9 | Another 20% crumbles |
| 10+ | Only center platforms remain |

### Crumble Visual
```
BEFORE CRUMBLE:
- Warning rumble
- Cracks appear
- "WALLS CRUMBLING!"

DURING CRUMBLE:
- Outer sections fall
- Dramatic animation
- Players must move inward

AFTER:
- Less space
- Easier to hit
- More intense
```

---

## 🎮 Game Modes

### Classic (Above)
- 4-8 players
- Simultaneous firing
- Crumbling walls

### 1v1 Duel
- Two players
- Opposite walls
- Turn-based (more strategic)

### Team Siege
- 2 teams
- Shared wall per team
- Destroy enemy team's fortress

### Boss Battle
- 1 player = BOSS (giant castle, more HP)
- Others = Attackers
- Boss has multiple catapults

### No Crumble
- Walls don't auto-crumble
- Pure destruction based
- Longer games

---

## 🎨 Visual Design

### Medieval Theme
- Stone castle walls
- Wooden catapults
- Knights/archers as characters
- Banners and flags

### Alternative Themes
**"Pirate Ships"**
- Ships instead of walls
- Cannons instead of catapults
- Ocean instead of void

**"Space Stations"**
- Sci-fi platforms
- Laser catapults
- Space void

**"Brainrot Castle"**
- Italian brainrot characters
- Meatball projectiles
- Pasta walls

---

## 💰 Monetization Ideas

- Character skins (knights, archers)
- Catapult skins
- Projectile effects
- Wall themes
- Victory animations
- Destruction effects

---

## 🎯 Why This Could Work

1. ✅ **Proven mechanic** (Aim + Power like Knockout)
2. ✅ **Destructible environment** (satisfying)
3. ✅ **Medieval theme** (popular with kids)
4. ✅ **Strategic depth** (target player or wall?)
5. ✅ **Escalating tension** (crumbling walls)
6. ✅ **Fast rounds** (simultaneous fire)
7. ✅ **Visual spectacle** (flying boulders, destruction)
8. ✅ **Easy to understand** (knock them off)
