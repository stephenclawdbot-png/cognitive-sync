# Chain Reaction ⛓️💥

**Status:** SAVED - Unique cascade mechanic
**Theme:** Explosive dominoes with players
**Style:** Real-time survival with chain mechanics

---

## 🎮 Core Concept

Getting hit turns you into a BOMB. Bombs explode after 3 seconds. Explosion pushes nearby players, potentially turning THEM into bombs. Chain reactions cascade through the crowd. Last player not bombed wins.

**The Twist:** One trigger creates cascading chaos. Simple cause, complex effect.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                      CHAIN REACTION                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → All players spawn in arena                               │
│      → Everyone is SAFE (normal state)                          │
│      → One random player becomes BOMB                           │
│      → Bomb player glows, ticking sound                         │
│                                                                 │
│   2. BOMB TIMER (3 seconds)                                     │
│      → Bomb player has 3 sec until explosion                    │
│      → Can move freely during countdown                         │
│      → Other players RUN AWAY                                   │
│      → Bomb player CHASES (wants to chain others)               │
│                                                                 │
│   3. EXPLOSION                                                  │
│      → BOOM! Bomb player explodes                               │
│      → Knockback radius around explosion                        │
│      → Anyone HIT by knockback = becomes BOMB                   │
│      → Original bomb player = eliminated                        │
│                                                                 │
│   4. CHAIN REACTION                                             │
│      → New bombs have 3 sec timers                              │
│      → Multiple bombs can exist                                 │
│      → They explode → create more bombs                         │
│      → Cascade continues until no new bombs                     │
│                                                                 │
│   5. SURVIVAL                                                   │
│      → Chain ends when no one in explosion radius               │
│      → Survivors continue                                       │
│      → New bomb selected from survivors                         │
│      → Repeat until 1 player left                               │
│                                                                 │
│   6. VICTORY                                                    │
│      → Last player standing = WINNER                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💣 Bomb Mechanics

### Bomb State
```
WHEN YOU BECOME BOMB:
- 3 second timer starts
- Body glows red/orange
- Ticking sound plays
- Can see countdown above head
- Full movement control

EXPLOSION:
- Timer hits 0
- BOOM effect
- Knockback pulse outward
- You are ELIMINATED
```

### Explosion Radius
```
        ┌─────────────┐
        │             │
        │   INSTANT   │
        │    BOMB     │  ← Anyone here = BOMB
        │   RADIUS    │
        │             │
    ┌───┼─────────────┼───┐
    │   │             │   │
    │   │   KNOCKBACK │   │  ← Pushed but not bombed
    │   │    ONLY     │   │
    │   │             │   │
    └───┼─────────────┼───┘
        │             │
        └─────────────┘

INNER RADIUS (close): Instant bomb
OUTER RADIUS (far): Knockback only
```

### Explosion Stats
| Property | Value |
|----------|-------|
| Inner Radius | 5 meters |
| Outer Radius | 10 meters |
| Knockback Force | Strong |
| Visual | Fire/explosion |

---

## ⛓️ Chain Mechanics

### How Chains Work
```
SCENARIO:
Player A is bomb → explodes → hits B and C
B and C become bombs (3 sec timer each)
B explodes → hits D
C explodes → hits E and F
D, E, F become bombs...

CHAIN LENGTH:
- Can go infinitely
- Depends on player positioning
- Tight groups = massive chains
- Spread out = short chains
```

### Chain Scoring
| Chain Length | Bonus |
|--------------|-------|
| 1 (no chain) | 0 |
| 2-3 | +50 points |
| 4-5 | +100 points |
| 6-7 | +200 points |
| 8+ | +500 points (MEGA CHAIN) |

---

## 🏃 Movement & Strategy

### Safe Player Movement
| Action | Use |
|--------|-----|
| Run | Get away from bombs |
| Sprint | Emergency escape |
| Jump | Might dodge explosion? (minimal) |
| Dive | Slight distance gain |

### Bomb Player Movement
```
AS BOMB YOU WANT TO:
- Chase other players
- Get close before exploding
- Corner groups
- Maximize chain reaction
- Don't waste your explosion

SACRIFICE PLAY:
- You're dying anyway
- Take as many as possible
- Create biggest chain
- Glory in death
```

### Survivor Strategy
```
SPACING:
- Don't group up!
- Chains devastate clusters
- Keep distance from everyone
- But don't corner yourself

PREDICTION:
- Watch bomb player movement
- Predict explosion timing
- Position away from their path
- Use obstacles as shields
```

---

## 🗺️ Map Design

### Key Features
- Open spaces (chain potential)
- Obstacles (block explosions)
- No hiding spots (must stay mobile)
- Medium size (not too spread)

### Map Ideas

**"Warehouse"**
- Crates as obstacles
- Open floor sections
- Explosive barrels (bonus damage!)
- Industrial theme

**"Playground"**
- Open grass areas
- Playground equipment
- Sandboxes slow movement
- Kid-friendly

**"Space Station"**
- Circular rooms
- Airlocks (void zones)
- Sci-fi containers
- Futuristic

---

## 📊 Round Progression

### Typical Chain Event
```
TIMELINE:
0:00 - Random bomb selected
0:03 - First explosion (hits 2 players)
0:06 - Two explosions (hits 3 more)
0:09 - Three explosions (hits 1)
0:12 - Chain ends
0:15 - New bomb selected from 2 survivors
...
```

### Round Length
- Average chain: 10-15 seconds
- Multiple chains per round
- Full round: 60-90 seconds
- Fast-paced eliminations

---

## 🎮 Game Modes

### Classic (Above)
- 8-12 players
- Single arena
- Last standing wins

### Team Chains
- 2 teams
- Only enemy explosions bomb you
- Teammates don't chain each other
- Team with last member wins

### Mega Chain
- 20+ players
- Massive arena
- Epic chain potential
- One bomb starts it all

### Timed Survival
- Constant bomb spawning
- Survive 2 minutes
- Multiple bombs at once
- Pure chaos

### No Chase
- Bombs can't move
- Just explosion timing
- Positional game only
- More strategic

---

## 🎁 Power-Ups

| Power-Up | Effect | Duration |
|----------|--------|----------|
| Blast Shield | Immune to next explosion | 1 hit |
| Speed Boost | Faster escape | 10 sec |
| Explosion Shrink | Smaller explosion radius | 1 bomb |
| Timer Extend | +2 seconds as bomb | Next bomb |
| Ghost | Pass through players | 5 sec |

---

## 🎨 Visual Design

### Bomb State
- Body glows red/orange
- Pulsing effect (faster as timer drops)
- Ticking sound
- Timer visible above head
- Particle effects (sparks)

### Explosion
- Fiery burst
- Shockwave ring
- Screen shake
- Dramatic sound
- Slow-mo on big chains

### Chain Visual
- Each explosion numbered
- Chain counter on screen
- Combo announcer ("DOUBLE!", "TRIPLE!")
- Celebration for mega chains

---

## 🧠 Psychological Depth

### The Bomb's Dilemma
```
"I'm dying anyway..."
"Who can I take with me?"
"Should I chase or corner?"
"Can I reach that group?"
```

### The Survivor's Panic
```
"Stay away from everyone!"
"But don't get cornered..."
"Where's the bomb going?"
"Oh no, now there's THREE bombs!"
```

### Group Dynamics
```
CLUSTERING = DEATH
- Friends group up naturally
- Chains devastate groups
- Must fight instinct
- Every person is a risk

EVERY MAN FOR THEMSELVES
- Can't trust proximity
- Alliances are dangerous
- Isolation is survival
```

---

## 💰 Monetization Ideas

- Character skins
- Explosion effects
- Death animations
- Chain trail effects
- Bomb skins
- Victory celebrations

---

## 🎯 Why This Could Work

1. ✅ **Unique mechanic** (chain explosions)
2. ✅ **Simple trigger** (one bomb starts all)
3. ✅ **Complex results** (cascading chaos)
4. ✅ **Fast rounds** (chains resolve quickly)
5. ✅ **Spectacle** (massive chains are exciting)
6. ✅ **Strategic depth** (positioning matters)
7. ✅ **Clip moments** (mega chains go viral)
8. ✅ **Easy to understand** (don't get bombed)
