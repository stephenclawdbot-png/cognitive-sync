# Conveyor Chaos 🏭📦

**Status:** SAVED - High potential
**Theme:** Factory conveyor battle
**Style:** Real-time survival with constant movement pressure

---

## 🎮 Core Concept

Everyone stands on moving CONVEYOR BELTS that lead to death (crusher, pit, fire). Must keep walking AGAINST the conveyor to survive. Push others toward death while staying alive yourself. Conveyors speed up over time.

**The Twist:** You're always moving toward death — survival requires CONSTANT effort.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                      CONVEYOR CHAOS LOOP                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → All players spawn on conveyor belt                       │
│      → Conveyor moving toward DEATH ZONE                        │
│      → Death zone: crusher, pit, fire, saw blades               │
│      → Must WALK/RUN against conveyor direction                 │
│                                                                 │
│   2. SURVIVAL BASICS                                            │
│      → Stand still = conveyor drags you to death                │
│      → Walk forward = stay in place                             │
│      → Run forward = move away from death                       │
│      → Stamina limits running                                   │
│                                                                 │
│   3. COMBAT                                                     │
│      → PUSH other players (toward death zone)                   │
│      → Pushed player loses ground                               │
│      → Can JUMP over push attempts                              │
│      → Can DODGE sideways                                       │
│                                                                 │
│   4. ESCALATION                                                 │
│      → Conveyor SPEEDS UP every 15 seconds                      │
│      → Walking no longer enough — must run                      │
│      → Eventually too fast to survive                           │
│      → Obstacles appear on belt                                 │
│                                                                 │
│   5. ELIMINATION                                                │
│      → Touch death zone = eliminated                            │
│      → Fall off sides = eliminated                              │
│      → Last player alive = WINS                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Conveyor Speed Progression

| Time | Speed | Survival Method | Difficulty |
|------|-------|-----------------|------------|
| 0:00 | Slow | Walk to stay still | Easy |
| 0:15 | Medium | Jog to stay still | Moderate |
| 0:30 | Fast | Run to stay still | Hard |
| 0:45 | Very Fast | Sprint constantly | Very Hard |
| 1:00 | Maximum | Sprint + never stop | Nearly impossible |

### Speed Mechanics
```
CONVEYOR SPEED vs PLAYER SPEED:

Slow conveyor:
- Walk speed > conveyor = move forward
- Stand still = drift back slowly

Fast conveyor:
- Walk speed < conveyor = drift back
- Run speed = stay in place
- Sprint = move forward slightly

Max conveyor:
- Run speed < conveyor = drift back!
- Sprint = barely stay in place
- Any mistake = death
```

---

## 🏃 Movement Mechanics

### Movement Options
| Action | Speed | Stamina Cost | Use |
|--------|-------|--------------|-----|
| Stand | 0 | None | Never (death) |
| Walk | Slow | None | Early game |
| Run | Medium | Low drain | Mid game |
| Sprint | Fast | High drain | Emergency/Late game |
| Jump | Pause movement | Medium | Dodge/Obstacle |

### Stamina System
```
STAMINA BAR: 100 max

DRAIN:
- Run = -5 per second
- Sprint = -15 per second
- Pushing = -10 per push

REGEN:
- Walking = +10 per second
- Standing = +20 per second (risky!)

STRATEGY:
- Manage stamina carefully
- Sprint burns out fast
- Walk to recover, but don't fall behind
```

---

## 🤜 Combat Mechanics

### Push Attack
| Property | Value |
|----------|-------|
| Range | Melee (close) |
| Knockback | 2 meters back |
| Cooldown | 1.5 seconds |
| Stamina Cost | 10 |

### Push Dynamics
```
PUSH FROM BEHIND:
- Target pushed toward death
- Most effective attack
- Must catch up to someone

PUSH FROM FRONT:
- You're closer to death
- Push them away (toward safe zone)
- Not useful usually

PUSH FROM SIDE:
- Knock them into obstacles
- Knock them off edge
- Situational
```

### Counter-Push
```
SEE PUSH COMING:
- Jump over attacker
- Dodge sideways
- Counter-push (both pushed back)
- Use obstacle as shield
```

---

## 🚧 Obstacles

### Obstacle Types
| Obstacle | Effect | Counter |
|----------|--------|---------|
| Box | Blocks path, climb over | Jump or go around |
| Oil Spill | Slippery, can't control | Jump over |
| Fence | Must jump | Time your jump |
| Spinning Blade | Instant death | Dodge carefully |
| Speed Pad | Boost forward | Use strategically |
| Slow Pad | Slows you down | Avoid |

### Obstacle Spawning
```
EARLY GAME:
- Few obstacles
- Easy to navigate
- Focus on pushing

MID GAME:
- More obstacles
- Must dodge AND fight
- Paths get complex

LATE GAME:
- Obstacle nightmare
- Combined with fast conveyor
- Pure chaos survival
```

---

## 🗺️ Map Layouts

### Single Belt
```
┌─────────────────────────────────────────┐
│                                         │
│    SAFE ◄◄◄◄ CONVEYOR ◄◄◄◄ DEATH       │
│    ZONE     [players]      ZONE         │
│                                         │
└─────────────────────────────────────────┘

- Simplest layout
- One direction of danger
- Pure pushing focus
```

### Multi-Lane
```
┌─────────────────────────────────────────┐
│    LANE 1  ◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄  DEATH      │
├─────────────────────────────────────────┤
│    LANE 2  ◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄  DEATH      │
├─────────────────────────────────────────┤
│    LANE 3  ◄◄◄◄◄◄◄◄◄◄◄◄◄◄◄  DEATH      │
└─────────────────────────────────────────┘

- 3 parallel lanes
- Can jump between lanes
- Different lanes = different speeds?
```

### Circle Belt
```
         ┌──────────┐
         │  DEATH   │
         │  (center)│
     ┌───┴──────────┴───┐
     │ ▼              ▼ │
     │   ◄ CONVEYOR ◄   │
     │ ▼              ▼ │
     └──────────────────┘
     
- Circular conveyor
- Death in center
- Pushed inward = death
- Must run outer edge
```

### Converging Belts
```
    ◄◄◄◄◄◄◄◄◄┐
              │
    ◄◄◄◄◄◄◄◄─┼──► DEATH
              │
    ◄◄◄◄◄◄◄◄◄┘

- Multiple belts converge
- All lead to same death
- Choose your path
- Cross-lane pushing
```

---

## 💀 Death Zone Varieties

| Death Zone | Visual | Effect |
|------------|--------|--------|
| Crusher | Giant press | Squish animation |
| Fire Pit | Flames | Burn animation |
| Saw Blades | Spinning saws | Slice effect |
| Void | Empty hole | Falling scream |
| Grinder | Industrial grinder | Dramatic |
| Acid | Green liquid | Dissolve effect |

---

## 🎁 Power-Ups

| Power-Up | Effect | Duration |
|----------|--------|----------|
| Speed Boost | Run faster | 10 sec |
| Infinite Stamina | No stamina drain | 15 sec |
| Super Push | 2x knockback | 5 sec |
| Shield | Can't be pushed | 5 sec |
| Slowdown Aura | Slow nearby enemies | 8 sec |
| Grapple | Pull enemy toward death | 1 use |

---

## 🎮 Game Modes

### Classic (Above)
- Single belt
- Speeding up
- Last standing wins

### Team Conveyor
- 2 teams, 2 belts
- Push enemies, help teammates
- Team with last survivor wins

### Infinite Run
- Solo survival
- How long can you last?
- Leaderboard for best times

### Obstacle Hell
- Max obstacles from start
- Normal conveyor speed
- Focus on dodging

### Reverse Conveyor
- Conveyor pushes AWAY from death
- Must push people BACKWARD
- Weird and funny

---

## 🎨 Visual Design

### Factory Theme
- Industrial setting
- Metal textures
- Warning signs
- Steam, sparks, grime

### Candy Factory (Kid-Friendly)
- Candy conveyor belts
- Chocolate waterfalls (death)
- Gummy obstacles
- Bright colors

### Space Station
- Sci-fi conveyor
- Airlocks (death)
- Zero-G sections?
- Futuristic

---

## 💰 Monetization Ideas

- Character skins
- Death animations
- Push effects
- Trail effects
- Conveyor skins
- Victory poses

---

## 🎯 Why This Could Work

1. ✅ **Constant pressure** (always moving toward death)
2. ✅ **Simple concept** (don't fall in death zone)
3. ✅ **Skill expression** (stamina management, pushing)
4. ✅ **Escalating difficulty** (conveyor speeds up)
5. ✅ **Visual drama** (dramatic death animations)
6. ✅ **Fast rounds** (~90 sec)
7. ✅ **Easy to understand** (walk or die)
8. ✅ **Chaotic fun** (pushing + obstacles)
