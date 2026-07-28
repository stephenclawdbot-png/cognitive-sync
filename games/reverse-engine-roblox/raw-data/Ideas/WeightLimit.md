# ⚖️ WEIGHT LIMIT

> **Formula:** L (Stack & Collapse) + Chicken Game
> **Core Mechanic:** Platform has hidden weight limit, add weight until collapse
> **Theme:** Cute animals on a breaking platform
> **Status:** ORIGINAL CONCEPT - Chicken/Pressure game

---

## 🎯 Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                       WEIGHT LIMIT                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Everyone standing on a PLATFORM                               │
│   Platform has a HIDDEN weight limit                            │
│                                                                 │
│   EACH ROUND:                                                   │
│   - Items spawn that you can GRAB                               │
│   - Grabbing items = adds weight to platform                    │
│   - More items = more points (if you survive)                   │
│                                                                 │
│   THE CATCH:                                                    │
│   - Platform shows STRESS (cracks, tilting, sounds)             │
│   - When weight limit exceeded = COLLAPSE                       │
│   - Everyone still on platform = ELIMINATED                     │
│                                                                 │
│   THE ESCAPE:                                                   │
│   - At ANY time, you can JUMP OFF to safety                     │
│   - But you keep NO POINTS from that round                      │
│   - It's a CHICKEN GAME                                         │
│                                                                 │
│   WINNER: Most points after X rounds                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎮 Game Flow

```
ROUND START:
- All players on platform
- Weight limit randomly set (hidden)
- "GRAB ITEMS FOR POINTS!"
- Items start appearing

GRABBING PHASE (30 sec):
- Items spawn on platform
- Grab items = +points, +weight
- 🪙 Coin = 10 points, light weight
- 💎 Diamond = 50 points, medium weight  
- 🏆 Trophy = 100 points, heavy weight
- Platform shows stress as weight increases

STRESS SIGNS:
- Cracks appear
- Platform tilts
- Creaking sounds
- Shaking
- Color changes (green → yellow → orange → red)

DECISION POINT:
- Stay and grab more? (GREEDY)
- Jump to safety? (SAFE but no points)
- "Is it about to collapse?!"

COLLAPSE:
- Weight limit exceeded
- Platform BREAKS
- Everyone still on it = LOSES all round points
- Those who jumped = KEEP their jumped-at-moment points

REPEAT:
- New round, new weight limit
- After X rounds, highest total points = WINNER
```

---

## ⚖️ Weight Mechanics

```
WEIGHT LIMIT:
- Randomly set each round: 500-1500 units
- Players don't know the exact number
- Only see STRESS INDICATORS

ITEM WEIGHTS:
| Item | Points | Weight |
|------|--------|--------|
| 🪙 Coin | 10 | 20 units |
| 💰 Cash | 25 | 40 units |
| 💎 Diamond | 50 | 80 units |
| 👑 Crown | 75 | 120 units |
| 🏆 Trophy | 100 | 200 units |

PLAYER WEIGHT:
- Each player = 100 units base
- 8 players = 800 units already
- So actual item limit = Weight limit - 800

STRESS LEVELS:
| % of Limit | Visual | Sound |
|------------|--------|-------|
| 0-50% | Green, stable | Silent |
| 50-70% | Yellow, slight cracks | Creak |
| 70-85% | Orange, more cracks, tilting | Groaning |
| 85-95% | Red, heavy shaking | Loud cracking |
| 95-100% | FLASHING, about to break | ALARM |
| 100%+ | COLLAPSE! | CRASH! |
```

---

## 🏟️ Arena Design

```
SIDE VIEW:

    🐰 🪙  🐻 💎  🐼 🪙 🪙  🐱
   ═══════════════════════════════
   ║         PLATFORM           ║
   ╚═══════════════════════════╝
              │││
              │││ (supports)
              │││
   ════════════════════════════════
           GROUND BELOW
           (safe zone)


STRESS PROGRESSION:

SAFE (green):
   ═══════════════════════
   ║                     ║
   ╚═════════════════════╝

STRESSED (yellow):
   ═══════════════════════
   ║    ─╱─    ╲─       ║ (cracks)
   ╚═════════════════════╝

DANGER (red):
   ══════════════════════
   ║  ╱─╱─╲  ╱─╲─╱─╲   ║ (many cracks)
   ╚════════════════════╝
         ↘ tilting ↙

COLLAPSE:
         💥 CRASH! 💥
      🐰 🐻 🐼 🐱 falling!
   ▓▓▓▓▓ ▓▓▓ ▓▓▓▓▓ ▓▓▓
        debris everywhere
```

---

## 🚪 Safe Zone

```
JUMP TO SAFETY:

At any time, player can jump OFF:

    🐰 (jumping off!)
     ↘
   ═══════════════════════
   ║  🐻  💎  🐼  🐱     ║
   ╚═════════════════════╝
     ↓
    🐰 (landed safe!)
   ════════════════════════
        SAFE GROUND

RULES:
- Jump off = KEEP points grabbed so far
- Can't return to platform
- Watch others from safety
- If platform doesn't collapse = jumpers wasted opportunity
- If platform collapses = jumpers made right call!
```

---

## 📱 Mobile Controls

```
┌──────────────────────────────────────┐
│  Round 3/5    Your Points: 245       │
│  Platform: 🟡 STRESSED               │
├──────────────────────────────────────┤
│                                      │
│   🪙  💎  🐰YOU  🪙  🐻  💰         │
│   ════════════════════════════       │
│   ║ ─╱─    PLATFORM    ╲─  ║        │
│   ╚════════════════════════╝         │
│                                      │
│   Items this round: +85 pts          │
│                                      │
├──────────────────────────────────────┤
│                                      │
│   [GRAB NEARBY]        [JUMP OFF!]   │
│       🪙                   🚪        │
│                                      │
└──────────────────────────────────────┘

LEFT: Grab items near you
RIGHT: Jump to safety (locks in points)
```

---

## 🧠 Strategic Depth

```
THE CHICKEN GAME:
- "Platform is yellow... still safe?"
- "It's orange now... should I jump?"
- "That guy grabbed the trophy... heavy!"
- "If I jump now I have 85 points..."
- "But if I grab one more diamond... 135!"
- "IS IT GOING TO COLLAPSE?!"

READING OTHERS:
- "He's walking toward the edge... is he jumping?"
- "She grabbed the trophy... risky!"
- "3 people jumped... maybe they know something?"
- "Or maybe they're scared and I should keep grabbing!"

GREEDY VS SAFE:
- Jump early = guaranteed small points
- Stay late = high points OR zero
- Risk/reward every round
```

---

## 💰 Monetization

### Character Skins
- Different animals
- Treasure hunter outfits
- Daredevil costumes

### Item Skins
- Different coin/gem styles
- Seasonal items
- Rare collectibles

### Effects
- Grab sparkles
- Jump trails
- Collapse effects

### Platform Themes
- Construction platform
- Ice sheet (cracks = ice breaking)
- Glass floor
- Cloud platform

---

## ✅ Checklist

- [x] Simple — Grab items, don't be on platform when it breaks
- [x] Dramatic — "Is it about to collapse?!"
- [x] Social — Watching others' greed/fear
- [x] Quick — 30 sec rounds
- [x] Fair — Risk/reward applies to all
- [x] Shareable — Greedy deaths, clutch escapes

---

## 🎯 One-Sentence Pitch

**"Grab treasures on a breaking platform — jump to safety or risk losing everything."**

---

*Formula: L (Stack & Collapse) + Chicken Game*
*Type: Risk/reward collection*
*Tension: "How much can I take before it breaks?"*
