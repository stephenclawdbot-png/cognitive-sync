# Gravity Gauntlet 🌍⬆️⬇️

**Status:** SAVED - Unique mechanic
**Theme:** Gravity-flipping obstacle course
**Style:** Racing + Adaptation + Chaos

---

## 🎮 Core Concept

Obstacle course race where GRAVITY FLIPS mid-race. Ceiling becomes floor. Must adapt instantly or fall into void. Platforms and obstacles change meaning with each flip.

**The Twist:** The course you learned is INVERTED constantly. Adaptability = survival.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                      GRAVITY GAUNTLET                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. RACE START                                                 │
│      → All players at starting line                             │
│      → Obstacle course ahead                                    │
│      → Gravity: NORMAL (down)                                   │
│      → Timer starts                                             │
│                                                                 │
│   2. RUNNING PHASE                                              │
│      → Race through obstacles                                   │
│      → Jump over gaps                                           │
│      → Avoid hazards                                            │
│      → Standard platforming                                     │
│                                                                 │
│   3. GRAVITY WARNING                                            │
│      → "GRAVITY FLIP IN 3... 2... 1..."                         │
│      → Screen effect (purple flash)                             │
│      → Warning sound                                            │
│      → Players prepare                                          │
│                                                                 │
│   4. GRAVITY FLIPS                                              │
│      → UP becomes DOWN                                          │
│      → Players FALL to ceiling                                  │
│      → Ceiling is now floor                                     │
│      → Course layout INVERTS                                    │
│      → Void is now above (was below)                            │
│                                                                 │
│   5. ADAPTATION                                                 │
│      → Continue racing on "ceiling"                             │
│      → New obstacles from this angle                            │
│      → Gaps and hazards repositioned                            │
│      → Same goal: reach finish                                  │
│                                                                 │
│   6. REPEAT FLIPS                                               │
│      → Gravity flips every 10-15 seconds                        │
│      → Keep adapting                                            │
│      → Flips happen at worst moments                            │
│                                                                 │
│   7. FINISH                                                     │
│      → First to finish = WINNER                                 │
│      → Or last players eliminated (too slow)                    │
│      → Fall into void = eliminated                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Gravity Mechanics

### Flip Physics
```
WHEN GRAVITY FLIPS:
- All players fall "up"
- Momentum preserved
- Land on ceiling
- Takes ~1 second to land

PLAYER STATE:
- Brief uncontrollable fall
- Can air-steer slightly
- Land animation
- Resume control
```

### Flip Timing
| Stage | Flip Frequency | Warning |
|-------|---------------|---------|
| Early | Every 15 sec | 3 sec warning |
| Mid | Every 12 sec | 2 sec warning |
| Late | Every 10 sec | 1 sec warning |
| Chaos | Every 7 sec | 0.5 sec warning |

---

## 🏃 Movement Mechanics

### Standard Movement
| Action | Use |
|--------|-----|
| Run | Standard speed |
| Sprint | Faster, limited |
| Jump | Cross gaps |
| Slide | Under obstacles |
| Wall-run | Special sections |

### During Flip
```
FALLING PHASE:
- Limited air control
- Can steer left/right slightly
- Can't change fall speed
- Choose landing spot

LANDING:
- Smooth landing = keep momentum
- Bad landing = stumble (slow)
- Miss platform = FALL INTO VOID
```

---

## 🎢 Obstacle Types

### Standard Obstacles
| Obstacle | Normal Gravity | Flipped Gravity |
|----------|---------------|-----------------|
| Gap | Jump over | Jump over (reversed) |
| Wall | Go around | Go around |
| Pit | Don't fall in | Was ceiling, now floor |
| Spikes | Avoid on floor | Now on ceiling! |

### Gravity-Specific Obstacles
| Obstacle | Effect |
|----------|--------|
| Sticky Pad | Hold onto during flip |
| Bounce Pad | Launch in current gravity |
| Gravity Zone | Local flip (just you) |
| Anti-Grav Tunnel | Float through |

### Moving Obstacles
- Swinging pendulums
- Rotating platforms
- Moving walls
- Appear different after flip

---

## 🗺️ Course Design

### Section Types
```
SECTION 1: TUTORIAL
- Simple gaps
- Clear platforms
- Learn the flip
- Generous timing

SECTION 2: COMPLEXITY
- Moving platforms
- Multiple paths
- Tighter gaps
- Faster flips

SECTION 3: CHAOS
- Everything moving
- Rapid flips
- Tiny platforms
- One mistake = death
```

### Course Layout (Side View)
```
NORMAL GRAVITY:

     START                                    FINISH
       │                                         │
       ▼                                         ▼
   ════════    ═══    ═══════    ══    ════════════
              ╱   ╲        ╲   ╱
             ╱     ╲        ╲ ╱
   ─────────────────────────────────────────────────
                    V O I D

FLIPPED GRAVITY:

   ─────────────────────────────────────────────────
                    V O I D (now above!)
             ╲     ╱        ╱ ╲
              ╲   ╱        ╱   ╲
   ════════    ═══    ═══════    ══    ════════════
       │                                         │
       ▼                                         ▼
     START                                    FINISH
```

---

## 💀 Elimination

### Ways to Die
| Death | Cause |
|-------|-------|
| Void Fall | Miss platform after flip |
| Spike Hit | Land on spikes |
| Crush | Caught between flip |
| Timeout | Too slow, course closes |

### Respawn Options
**Elimination Mode:**
- One life
- Die = out
- Last standing wins

**Checkpoint Mode:**
- Respawn at checkpoints
- Time penalty
- First to finish wins

---

## 🎮 Game Modes

### Race (Above)
- First to finish wins
- Multiple flips
- One life or checkpoints

### Survival
- Course loops infinitely
- Faster and faster flips
- Last alive wins
- No finish line

### Team Race
- 2 teams
- First team to get 3 players across
- Help teammates (kinda)

### Flip Frenzy
- Random flip timing
- No warnings
- Pure chaos

### Practice
- Single player
- Learn course
- No elimination

---

## 🎨 Visual Design

### Aesthetic Options
**"Space Station"**
- Sci-fi corridors
- Metal platforms
- Earth visible outside
- Airlocks as hazards

**"Candy World"**
- Colorful platforms
- Chocolate rivers (void)
- Gummy obstacles
- Kid-friendly

**"Neon Arcade"**
- Glowing platforms
- Dark void
- Synth aesthetic
- Tron-like

### Flip Effects
- Screen tint (purple flash)
- World rotates smoothly
- Hair/clothes physics
- Disorientation effect

---

## 🎁 Power-Ups

| Power-Up | Effect | Duration |
|----------|--------|----------|
| Sticky Feet | Don't fall during flip | 10 sec |
| Hover | Float briefly after flip | 5 sec |
| Speed Boost | Run faster | 8 sec |
| Ghost | Pass through obstacles | 5 sec |
| Flip Cancel | Immune to next flip | 1 flip |

---

## 🧠 Skill Expression

### Beginner
- Follow the path
- React to flips
- Survive somehow

### Intermediate
- Predict flip timing
- Position for flips
- Use sticky pads

### Advanced
- Speedrun routes
- Air control mastery
- Skip sections with momentum
- Use flips as shortcuts

### Pro
- Flip timing abuse
- Intentional risky positions
- Sub-optimal paths that flip makes optimal

---

## 💰 Monetization Ideas

- Character skins
- Trail effects
- Death animations
- Gravity effects
- Course themes
- Victory poses

---

## 🎯 Why This Could Work

1. ✅ **Unique mechanic** (gravity flipping)
2. ✅ **Constant surprise** (flips keep it fresh)
3. ✅ **Skill-based** (adaptability matters)
4. ✅ **Visual spectacle** (world turning upside down)
5. ✅ **Easy to understand** (reach the end)
6. ✅ **Hard to master** (timing, positioning)
7. ✅ **Replayable** (random flip timing)
8. ✅ **Clip-worthy** (clutch flip survivals)
