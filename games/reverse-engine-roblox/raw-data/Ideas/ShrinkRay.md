# Shrink Ray 🔬🐁

**Status:** SAVED - High potential
**Theme:** Size-changing combat
**Style:** Real-time shooter with unique size mechanic

---

## 🎮 Core Concept

Shrink rays spawn around the map. Shoot someone = they SHRINK. Smaller = weaker but faster and sneakier. Tiny players can be STEPPED ON. Grow pads restore size. Manage your size strategically.

**The Twist:** Being small isn't just bad — it's DIFFERENT. Size = tradeoffs.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                       SHRINK RAY LOOP                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → All players spawn NORMAL SIZE                            │
│      → Shrink rays scattered around map                         │
│      → Grow pads in specific locations                          │
│      → Everyone scrambles for weapons                           │
│                                                                 │
│   2. SHRINK COMBAT                                              │
│      → Find shrink ray, pick it up                              │
│      → Shoot other players with ray                             │
│      → HIT = target SHRINKS one level                           │
│      → Can shrink same target multiple times                    │
│      → Shrink ray has limited ammo (recharges)                  │
│                                                                 │
│   3. SIZE LEVELS                                                │
│      → GIANT (rare power-up)                                    │
│      → NORMAL (starting size)                                   │
│      → SMALL (1 shrink)                                         │
│      → TINY (2 shrinks)                                         │
│      → MICRO (3 shrinks) - can be stepped on!                   │
│                                                                 │
│   4. SIZE DYNAMICS                                              │
│      → Bigger players can STOMP smaller ones                    │
│      → Smaller players can HIDE in small spaces                 │
│      → Grow pads restore one size level                         │
│      → Strategic: sometimes small is better!                    │
│                                                                 │
│   5. ELIMINATION                                                │
│      → Get stomped = eliminated                                 │
│      → Fall off map = eliminated                                │
│      → Last player standing = WINS                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📏 Size Levels Detail

| Size | Scale | Speed | Jump | Health | Can Stomp | Can Be Stomped | Special |
|------|-------|-------|------|--------|-----------|----------------|---------|
| GIANT | 150% | Slow | Low | 5 HP | All sizes | Nobody | Rare power-up |
| NORMAL | 100% | Normal | Normal | 3 HP | Small+ | Giant | Starting size |
| SMALL | 70% | Fast | Higher | 2 HP | Tiny+ | Normal+ | Fit in small doors |
| TINY | 40% | Very Fast | Very High | 1 HP | Micro | Small+ | Hide in vents |
| MICRO | 20% | Ultra Fast | Ultra High | 1 HP | Nobody | Everyone | Almost invisible |

---

## 🔫 Shrink Ray Mechanics

### Shrink Ray Stats
| Property | Value |
|----------|-------|
| Ammo | 5 shots |
| Recharge | 1 shot per 3 sec |
| Range | Medium-long |
| Travel Speed | Medium (can dodge) |
| Effect | Shrink target 1 level |

### Shooting Dynamics
```
HIT NORMAL PLAYER → They become SMALL
HIT SMALL PLAYER → They become TINY
HIT TINY PLAYER → They become MICRO
HIT MICRO PLAYER → Nothing (already smallest)

HIT GIANT → They become NORMAL (skip sizes)
```

### Shrink Ray Locations
- Spawn at round start (3-5 rays)
- Respawn every 30 seconds
- Visible glow, sound cue
- Anyone can pick up

---

## 👟 Stomp Mechanics

### How Stomping Works
```
STOMP RULES:
- Jump on a smaller player's HEAD
- They must be 2+ sizes smaller
- Direct head hit required
- Successful stomp = ELIMINATION

STOMP PROTECTION:
- Same size = bounce off
- 1 size smaller = knockback only
- Indoors/covered = can't be stomped

COUNTER-STOMP:
- See someone jumping at you
- Dodge or find cover
- Shrink THEM mid-air to reverse
```

### Stomp Scenarios
| You | Target | Result |
|-----|--------|--------|
| Giant | Anyone | Stomp kill |
| Normal | Small | Knockback |
| Normal | Tiny | Stomp kill |
| Normal | Micro | Stomp kill |
| Small | Tiny | Knockback |
| Small | Micro | Stomp kill |
| Tiny | Micro | Stomp kill |

---

## 🟢 Grow Pad Mechanics

### Grow Pads
- Fixed locations on map
- Step on = grow ONE size level
- 10 second cooldown after use
- Glow when ready
- Multiple players can race for it

### Grow Strategy
```
WHEN TO GROW:
- You're Micro (survival!)
- Enemy is smaller than you (stomp them)
- Need more health for fight

WHEN TO STAY SMALL:
- Hiding/escaping
- Accessing small passages
- Being sneaky
- Enemies have shrink rays aimed at you (waste their ammo)
```

---

## 🗺️ Map Design

### Key Features
```
OPEN AREAS:
- Stomp danger zones
- Shrink ray fights
- Giant players dominate

SMALL PASSAGES:
- Only Small and below can enter
- Safe from stomps
- Escape routes for tiny players
- Vents, mouse holes, pipes

GROW PAD LOCATIONS:
- Open areas (risky to reach)
- Strategic positioning
- Contested zones

HEIGHT VARIATION:
- High ground = stomp advantage
- Low hiding spots
- Platforming elements
```

### Map Ideas

**"Science Lab"**
- Giant beakers, tubes
- Small passages through equipment
- Grow pads on lab tables
- Sci-fi aesthetic

**"House Interior"**
- Human-sized house
- Players feel small
- Hide under furniture
- Kitchen, living room, bedroom

**"Toy Store"**
- Giant toys
- Small passages through toy boxes
- Colorful, playful
- Stuffed animals as obstacles

---

## 🎁 Power-Ups

| Power-Up | Effect | Duration/Use |
|----------|--------|--------------|
| Growth Serum | Become GIANT | 15 seconds |
| Insta-Shrink | Shrink to MICRO (escape!) | Instant |
| Shield | Can't be shrunk | 10 seconds |
| Mega Ray | Shrink ray shrinks 2 levels | 3 shots |
| Stomp Boots | Stomp players 1 size smaller | 20 seconds |

---

## 🎮 Game Modes

### Classic (Above)
- Free for all
- Last standing wins
- All sizes in play

### Giants vs Micros
- Half start Giant, half start Micro
- Giants hunt, Micros survive
- Timer: Micros win if any survive

### Team Shrink
- 2 teams
- Shrink enemies, protect teammates
- Team with last member standing wins

### Size Freeze
- Size locked (everyone same)
- Pure combat, no shrinking
- Rotate sizes each round

### Grow Only
- Everyone starts Micro
- Only grow pads (no shrinking)
- Race to become Giant
- Giants hunt remaining Micros

---

## 🧠 Strategic Depth

### Size Strategies
```
GIANT HUNTER:
- Get giant power-up
- Stomp everyone
- Risk: slow, big target for rays

NORMAL BALANCED:
- Stay normal, use rays
- Not too slow, not too weak
- Middle ground

INTENTIONAL SMALL:
- Stay Small/Tiny on purpose
- Fast, sneaky
- Use small passages
- Avoid open areas

MICRO SURVIVALIST:
- Get shrunk, stay Micro
- Hide until others fight
- Nearly invisible
- High risk: one stomp = dead
```

### Counter-Play
```
If enemy is Giant:
→ Shrink them! They become Normal
→ Stay in small passages
→ Don't fight directly

If enemy is Micro:
→ Hard to hit with ray
→ Try to stomp
→ Guard grow pads

If enemy has shrink ray:
→ Keep distance
→ Dodge shots
→ Find your own ray
```

---

## 🎨 Visual Design

### Size Visuals
- Smooth scaling animations
- Shrink = cartoony squeeze effect
- Grow = stretch and pop
- Giant footsteps shake screen

### Shrink Ray
- Sci-fi gun design
- Blue/purple beam
- Target shrinks with spiral effect
- Satisfying sound

### Stomping
- Squish effect on kill
- Dust cloud
- Comedic sound
- Screen shake for stomper

---

## 💰 Monetization Ideas

- Character skins
- Shrink ray skins
- Stomp effects
- Shrink/grow animations
- Death effects
- Victory poses

---

## 🎯 Why This Could Work

1. ✅ **Unique mechanic** (size as gameplay element)
2. ✅ **Visual comedy** (big vs tiny)
3. ✅ **Strategic depth** (size tradeoffs)
4. ✅ **Multiple strategies** (big, small, balanced)
5. ✅ **Fast-paced** (constant size changes)
6. ✅ **Satisfying feedback** (stomp kills!)
7. ✅ **Kid-friendly** (sci-fi shrinking is fun)
8. ✅ **Clip-worthy** (giant stomping micros)
