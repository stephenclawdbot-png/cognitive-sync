# 💣 BOMB SQUAD

> **Formula:** O (Sacrifice)
> **Core Mechanic:** Someone must jump on the bomb or random players die
> **Theme:** Cute animals making heroic sacrifices
> **Status:** ORIGINAL CONCEPT - Social pressure + sacrifice

---

## 🎯 Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                        BOMB SQUAD                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   A BOMB spawns in the arena                                    │
│   Timer counting down: 10... 9... 8...                          │
│                                                                 │
│   THE CHOICE:                                                   │
│   - Someone can JUMP ON THE BOMB (sacrifice)                    │
│   - Sacrificer is ELIMINATED but saves everyone                 │
│   - Sacrificer gets HERO POINTS (matters for final rank)        │
│                                                                 │
│   IF NO ONE SACRIFICES:                                         │
│   - Bomb EXPLODES                                               │
│   - Random 2-3 players eliminated                               │
│   - More deaths than if someone sacrificed!                     │
│                                                                 │
│   THE TENSION:                                                  │
│   - "Will someone else do it?"                                  │
│   - "Should I be the hero?"                                     │
│   - "If no one does, I might die anyway!"                       │
│                                                                 │
│   WINNER: Last one standing (hero points = tiebreaker)          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎮 Game Flow

```
ROUND START:
- All players in arena
- Bomb spawns in center
- "BOMB ARMED! 10 SECONDS!"
- Timer starts

THE COUNTDOWN (10 sec):
- 10... 9... 8... (casual)
- 7... 6... 5... (tension building)
- 4... 3... (panic!)
- 2... 1... (LAST CHANCE!)

DURING COUNTDOWN:
- Players can move around
- Anyone can JUMP ON BOMB to sacrifice
- First to jump = becomes the hero
- Others are saved

OUTCOMES:

IF SOMEONE SACRIFICES:
- Hero eliminated
- Hero gets +100 HERO POINTS
- Everyone else survives
- "🐰 SAVED EVERYONE!"
- New round begins

IF NO ONE SACRIFICES:
- BOOM! Explosion!
- 2-3 random players eliminated
- "NO HERO... 3 PLAYERS ELIMINATED!"
- Survivors continue
- New round begins

GAME END:
- Last player standing = WINNER
- If tie, hero points = tiebreaker
- "Most heroic survivor wins!"
```

---

## 💣 Bomb Mechanics

```
BOMB VISUALS:

    ╭─────────╮
    │  💣    │
    │ ⏱️ 07  │  ← Timer display
    │ ●●●●●  │  ← Danger indicator
    ╰─────────╯

TIMER STAGES:
| Time | Visual | Sound |
|------|--------|-------|
| 10-7 | Green glow | Slow beep |
| 6-4 | Yellow glow | Medium beep |
| 3-2 | Orange, shaking | Fast beep |
| 1-0 | RED, violent shake | ALARM! |

EXPLOSION:
- Massive blast radius (whole arena)
- Random 2-3 players hit
- Spectacular visual
- NOT based on distance (random)
```

---

## 🦸 Hero System

```
SACRIFICING:
- Walk to bomb
- Press [SACRIFICE] button
- Hero animation plays
- Bomb defused (hero absorbed blast)
- Hero eliminated but honored

HERO POINTS:
- Each sacrifice = +100 hero points
- Hero points = tiebreaker for final ranking
- Displayed next to player name
- "🐰 (⭐2)" = sacrificed twice

HERO BENEFITS:
- Fame/glory
- Tiebreaker advantage
- Special "hero" badge after game
- Potential: Hero coins for shop?

WHY SACRIFICE?
- If you think you'll die anyway... might as well be a hero
- Hero points matter for ranking
- Glory!
- Save your friends (if playing with friends)
```

---

## 🧠 The Social Dilemma

```
EVERYONE'S THINKING:

"I don't want to die..."
"But if no one sacrifices, I might die randomly!"
"Should I jump on it?"
"Maybe someone else will..."
"5 seconds left... no one's moving..."
"4... 3... SOMEONE DO IT!"
"2... should I?!"
"1... FINE I'LL—"
*someone else jumps*
"Oh thank god."

THE CALCULATION:
- 8 players remaining
- If no sacrifice: 3 die (37.5% chance of being one)
- If I sacrifice: I die (100%)
- BUT: If no one moves at 2 seconds... 
- Should I risk 37.5% or guarantee my death as hero?

BYSTANDER EFFECT:
- Everyone waits for someone else
- "Surely SOMEONE will do it..."
- Countdown intensifies pressure
- Last 3 seconds = CHAOS of decisions
```

---

## 🏟️ Arena Design

```
TOP-DOWN VIEW:

╔══════════════════════════════════════════╗
║                                          ║
║    🐰         🐻                         ║
║                                          ║
║         🐼          🐱                   ║
║                                          ║
║              💣                          ║
║            (BOMB)                        ║
║                                          ║
║    🐶              🐹                    ║
║                                          ║
║         🐸                   🦊          ║
║                                          ║
╚══════════════════════════════════════════╝

Players spread around, bomb in center
Anyone can approach and sacrifice


EXPLOSION VIEW:

╔══════════════════════════════════════════╗
║                                          ║
║    🐰         💥💥💥                     ║
║            💥💥💥💥💥                    ║
║         💥💥💥💥💥💥💥                  ║
║        💥💥💥 BOOM! 💥💥💥              ║
║         💥💥💥💥💥💥💥                  ║
║            💥💥💥💥💥                    ║
║    🐶        💥💥💥          (eliminated)║
║                                          ║
║         🐸                   🦊          ║
║                                          ║
╚══════════════════════════════════════════╝

Explosion hits random players (X marks = hit)
```

---

## 📱 Mobile Controls

```
┌──────────────────────────────────────┐
│  Round 4      Left: 6      ⭐You: 0  │
│         ⚠️ BOMB: 5 SECONDS ⚠️        │
├──────────────────────────────────────┤
│                                      │
│    🐰         🐻                     │
│                                      │
│         🐼    💣    🐱               │
│              ⏱️ 5                    │
│    YOU→🐶              🐹            │
│                                      │
├──────────────────────────────────────┤
│                                      │
│   [JOYSTICK]         [🦸 SACRIFICE]  │
│       ○               (jump on bomb) │
│                                      │
└──────────────────────────────────────┘

Move toward bomb + tap SACRIFICE = hero
```

---

## 🔥 Variants

### HIDDEN BOMB:
```
Bomb spawns but location is HIDDEN
Players must FIND it first
Adds search element
Finder has advantage (knows where it is)
```

### MULTIPLE BOMBS:
```
2-3 bombs spawn
Each needs a sacrifice
More chaos
More heroes needed
```

### HERO RESURRECTION:
```
If you sacrificed earlier...
You might come back in final round!
"Heroes get second chances"
Incentivizes sacrifice
```

### POINT BOMB:
```
Instead of elimination...
Bomb removes POINTS
Sacrifice saves everyone's points
Hero loses points but gains hero status
```

---

## 💰 Monetization

### Character Skins
- Different animals
- Hero outfits (capes, masks)
- Firefighter/bomb squad uniforms

### Sacrifice Effects
- Hero explosion (golden blast)
- Angel wings appear
- Dramatic slow-mo
- "HERO!" text effect

### Bomb Skins
- Classic bomb
- Present bomb (gift-wrapped)
- Nuke
- Candy bomb
- Ice bomb

### Celebration Effects
- Survivors clapping
- Confetti for hero
- Memorial statue (temporary)

---

## ✅ Checklist

- [x] Simple — Bomb ticking, sacrifice or random death
- [x] Dramatic — 10 second countdown, who will be the hero?
- [x] Social — Bystander effect, social pressure
- [x] Quick — 10 sec per bomb, fast rounds
- [x] Fair — Anyone can sacrifice, random if not
- [x] Shareable — Heroic moments, cowardly deaths

---

## 🎯 One-Sentence Pitch

**"A bomb is ticking — sacrifice yourself to save everyone, or risk the random explosion."**

---

*Formula: O (Sacrifice)*
*Type: Social dilemma + countdown*
*Tension: "Will someone be the hero?"*
