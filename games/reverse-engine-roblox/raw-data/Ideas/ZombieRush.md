# 🧟 ZOMBIE RUSH

> **Formula:** K (Infection)
> **Core Mechanic:** One zombie chases, touch = infected, last human wins
> **Theme:** Cute zombie animals chasing survivors
> **Status:** ORIGINAL CONCEPT - Real-time chase

---

## 🎯 Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                        ZOMBIE RUSH                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   One player starts as ZOMBIE (visible, glowing)                │
│   Everyone else is HUMAN (survivors)                            │
│                                                                 │
│   REAL-TIME CHASE:                                              │
│   - Zombie chases humans                                        │
│   - Touch a human = they become zombie                          │
│   - Zombie horde GROWS                                          │
│                                                                 │
│   ESCALATION:                                                   │
│   - Zombies get FASTER over time                                │
│   - Arena SHRINKS over time                                     │
│                                                                 │
│   WIN CONDITION:                                                │
│   - Last human alive = WINNER                                   │
│   - OR: Survive until timer ends                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎮 Game Flow

```
START:
- 10 players
- Random player becomes ZOMBIE (3 sec warning)
- "ZOMBIE RUSH BEGINS IN 3... 2... 1..."
- Zombie spawns, chase begins!

EARLY GAME (0-30 sec):
- 1 zombie vs 9 humans
- Humans scatter
- Zombie is SLOW at first
- Relatively easy to escape

MID GAME (30-60 sec):
- 3-4 zombies now
- Zombies getting FASTER
- Arena starting to shrink
- Harder to escape

LATE GAME (60-90 sec):
- 7-8 zombies chasing 2-3 humans
- Zombies are FAST
- Arena is SMALL
- Intense survival

END:
- Last human = WINNER
- Or if timer runs out with humans alive = all survivors win
```

---

## 🧟 Zombie Mechanics

```
ZOMBIE STATS:
- Start: 80% of human speed
- +5% speed every 15 seconds
- By 60 sec: 100% speed
- By 90 sec: 110% speed (FASTER than humans!)

ZOMBIE ABILITIES:
- Basic: Just chase and touch
- Optional power-ups:
  - LUNGE: Short dash (cooldown)
  - ROAR: Slow nearby humans briefly
  - SENSE: See humans through walls briefly

INFECTION:
- Touch = instant infection
- New zombie has 2 sec "transformation" (can't move)
- Then joins the horde
```

---

## 🏃 Human Mechanics

```
HUMAN ABILITIES:
- Run (standard speed)
- Dash (short burst, cooldown)
- Jump (hop over obstacles)

OPTIONAL POWER-UPS (spawn on map):
- Speed boost (temporary)
- Shield (block one touch)
- Invisibility (5 sec)
- Freeze bomb (slow zombies in area)

STRATEGY:
- Stay away from zombie horde
- Use obstacles to block
- Don't get cornered!
- Watch for arena shrinking
```

---

## 🏟️ Arena Design

```
TOP-DOWN VIEW:

╔══════════════════════════════════════════╗
║                                          ║
║    🧟         🏃 🏃                      ║
║         ▓▓▓▓                             ║
║         ▓▓▓▓    🏃                       ║
║                        ▓▓▓▓             ║
║    🏃           ▓▓▓▓                    ║
║         ▓▓▓▓              🏃            ║
║                                    🏃    ║
║    🏃        🏃                         ║
║                                          ║
╚══════════════════════════════════════════╝

🧟 = Zombie
🏃 = Human survivors  
▓▓ = Obstacles (can't pass through)


SHRINKING:
╔══════════════════════╗
║   ░░░░░░░░░░░░░░░   ║
║   ░  DANGER ZONE  ░  ║
║   ░  ╔════════╗   ░  ║
║   ░  ║ SAFE   ║   ░  ║
║   ░  ║ ZONE   ║   ░  ║
║   ░  ╚════════╝   ░  ║
║   ░░░░░░░░░░░░░░░   ║
╚══════════════════════╝

Danger zone = instant elimination
```

---

## 🐾 Character Design

**Humans:**
- Cute animals running scared
- 🐰 Bunny, 🐱 Cat, 🐶 Dog, etc.
- Panic animations
- Sweat drops, scared eyes

**Zombies:**
- SAME animals but zombified!
- Green tint
- Torn clothes
- Silly zombie walk
- Groaning sounds
- NOT scary, CUTE-scary

---

## 📱 Mobile Controls

```
┌──────────────────────────────────────┐
│  Time: 45s    Humans: 4    Zone: 70% │
├──────────────────────────────────────┤
│                                      │
│         (Arena view)                 │
│                                      │
│    🧟 🧟      YOU 🐰                 │
│         🧟           🏃              │
│              🧟  🧟                  │
│                      🏃              │
│                                      │
├──────────────────────────────────────┤
│                                      │
│   [JOYSTICK]              [DASH]     │
│       ○                     💨       │
│                                      │
└──────────────────────────────────────┘

Simple: Joystick to move, Dash button
```

---

## 💰 Monetization

### Character Skins
- Different animals
- Human outfits (survivor gear)
- Zombie variants (different zombie styles)

### Effects
- Run trails
- Infection effect (green poof)
- Dash effects

### Arena Themes
- City streets
- Shopping mall
- School
- Haunted house
- Space station

---

## ✅ Checklist

- [x] Simple — Run from zombies. Touch = infected.
- [x] Dramatic — Horde growing, arena shrinking
- [x] Social — Watching friends get caught
- [x] Quick — 90 second rounds
- [x] Fair — Anyone can be last survivor
- [x] Shareable — Close escapes, clutch wins

---

## 🎯 One-Sentence Pitch

**"Run from the zombie horde — last human standing wins."**

---

*Formula: K (Infection)*
*Type: Real-time chase*
*Tension: Escalating danger*
