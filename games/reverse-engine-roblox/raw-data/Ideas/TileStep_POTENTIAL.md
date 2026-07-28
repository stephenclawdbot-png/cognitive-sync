# ⬜ TILE STEP

> **Formula:** A (Timer-Reveal) + SPATIAL
> **Core Mechanic:** Grid movement, tiles vanish, position matters
> **Theme:** Cute animals on a disappearing grid
> **Status:** ORIGINAL CONCEPT - Knockout! Spatial Feel

---

## 🎯 Why This Has The KNOCKOUT! Feel

```
KNOCKOUT!:
- See positions ✓
- Hidden intentions ✓
- Shrinking arena ✓
- Spatial strategy ✓

TILE STEP:
- See positions on grid ✓
- Hidden: which direction everyone steps ✓
- Tiles vanish = shrinking ✓
- "If I go north and he's there..." ✓
```

**This is SPATIAL prediction, not just social prediction.**

---

## 🧬 Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                        TILE STEP                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Everyone standing on a GRID of tiles                          │
│   Each player on their own tile                                 │
│                                                                 │
│   Pick DIRECTION to step: ⬆️⬇️⬅️➡️ or STAY                       │
│                                                                 │
│   "Stepping in 3... 2... 1..."                                  │
│                                                                 │
│   Everyone moves ONE tile simultaneously                        │
│   THEN: Random tiles VANISH                                     │
│                                                                 │
│   Standing on vanishing tile = FALL = eliminated                │
│   Two players on same tile = COLLISION = one falls              │
│   Edge tiles vanish first (shrinking grid)                      │
│                                                                 │
│   Repeat until one winner                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎮 Turn Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                   TILE STEP - TURN FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   PHASE 1: OBSERVE (2 sec)                                      │
│   → See the grid                                                │
│   → See where everyone is standing                              │
│   → See which tiles look "dangerous" (edge, cracked?)           │
│   → "CHOOSE YOUR STEP!"                                         │
│                                                                 │
│   PHASE 2: SECRET CHOICE (5 sec)                                │
│   → Pick: ⬆️ North, ⬇️ South, ⬅️ West, ➡️ East, or ⏹️ Stay       │
│   → Consider: "Where is everyone else going?"                   │
│   → Consider: "Which tiles might vanish?"                       │
│   → Consider: "Will I collide with someone?"                    │
│                                                                 │
│   PHASE 3: LOCK                                                 │
│   → "Stepping in 3... 2... 1..."                                │
│   → No changing                                                 │
│   → Tension builds                                              │
│                                                                 │
│   PHASE 4: STEP                                                 │
│   → Everyone moves simultaneously                               │
│   → See where people went                                       │
│   → COLLISIONS happen (two on same tile)                        │
│                                                                 │
│   PHASE 5: VANISH                                               │
│   → Random tiles start SHAKING                                  │
│   → Then VANISH (fall away)                                     │
│   → Anyone standing there = FALLS                               │
│   → Edge tiles more likely to vanish                            │
│                                                                 │
│   PHASE 6: ELIMINATE                                            │
│   → Fallen players = eliminated                                 │
│   → Collision losers = eliminated                               │
│   → Survivors remain on grid                                    │
│   → Grid is now smaller                                         │
│   → Repeat until winner                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 The Spatial Mind Games

### Position Reading:
```
"He's at C3, I'm at C4..."
"If I go NORTH, I land on C3... but he might still be there!"
"If he goes NORTH too, we both move and I'm safe"
"But if he STAYS, we COLLIDE!"
```

### Edge Awareness:
```
"I'm near the edge..."
"Edge tiles vanish first!"
"I NEED to move toward center"
"But everyone else is moving center too..."
"COLLISION RISK!"
```

### Predicting Vanish:
```
"That tile looks cracked..."
"It might vanish this round..."
"I should NOT step there"
"But what if it's a fake-out?"
```

### Collision Calculation:
```
"3 players left..."
"He's at A1, she's at C1, I'm at B2"
"If I go WEST to A2, I'm safe from them"
"But if she goes NORTH to C2, and I go WEST..."
"We don't collide! Safe!"
"Unless the tile vanishes..."
```

---

## 🏟️ Arena Design

```
THE GRID (5x5 starting):

    ┌─────┬─────┬─────┬─────┬─────┐
    │ A1  │ A2  │ A3  │ A4  │ A5  │
    │     │ 🐰  │     │     │     │
    ├─────┼─────┼─────┼─────┼─────┤
    │ B1  │ B2  │ B3  │ B4  │ B5  │
    │     │     │ 🐻  │     │ 🐱  │
    ├─────┼─────┼─────┼─────┼─────┤
    │ C1  │ C2  │ C3  │ C4  │ C5  │
    │ 🐼  │     │     │ 🐶  │     │
    ├─────┼─────┼─────┼─────┼─────┤
    │ D1  │ D2  │ D3  │ D4  │ D5  │
    │     │ 🐹  │     │     │ 🐸  │
    ├─────┼─────┼─────┼─────┼─────┤
    │ E1  │ E2  │ E3  │ E4  │ E5  │
    │     │     │ 🦊  │     │     │
    └─────┴─────┴─────┴─────┴─────┘


AFTER VANISH (edges gone):

    ┌─────┬─────┬─────┐
    │ B2  │ B3  │ B4  │
    │ 🐰  │ 🐻  │     │
    ├─────┼─────┼─────┤
    │ C2  │ C3  │ C4  │
    │     │ 🐱  │ 🐶  │
    ├─────┼─────┼─────┤
    │ D2  │ D3  │ D4  │
    │ 🐹  │     │     │
    └─────┴─────┴─────┘

(🐼, 🐸, 🦊 were on edge = eliminated)
```

---

## ⚡ Collision Rules

```
TWO PLAYERS SAME TILE:

Option A: RANDOM
- Random player eliminated
- Other survives
- 50/50 luck

Option B: PUSH-BACK
- Both bounce back to original tile
- If original tile vanished = eliminated
- If original tile exists = safe

Option C: BOTH FALL
- Tile can't hold two
- Both eliminated
- Harsh but clear

RECOMMENDED: Option A (adds luck, less frustrating)
```

---

## 🎨 Tile Visuals

```
TILE STATES:

SAFE TILE:
┌─────────┐
│ ░░░░░░░ │  Solid color
│ ░░░░░░░ │  Stable
└─────────┘

CRACKED TILE (warning):
┌─────────┐
│ ╱░░░░╲░ │  Visible cracks
│ ░░╱╲░░░ │  Might vanish soon
└─────────┘

VANISHING TILE:
┌─────────┐
│ ▓▓▓▓▓▓▓ │  Shaking
│ ▓▓▓▓▓▓▓ │  Red glow
└─────────┘
     ↓
   💨 (falls away)

PLAYER ON TILE:
┌─────────┐
│         │
│   🐰    │  Character visible
│         │
└─────────┘
```

---

## 📱 Mobile Controls

```
┌──────────────────────────────────────┐
│  Round 4      ⏱️ 4       Left: 5     │
│         "CHOOSE YOUR STEP!"          │
├──────────────────────────────────────┤
│                                      │
│    ┌───┬───┬───┐                     │
│    │🐰 │   │🐻 │                     │
│    ├───┼───┼───┤                     │
│    │   │YOU│🐱 │  ← You are here     │
│    ├───┼───┼───┤                     │
│    │🐹 │   │   │                     │
│    └───┴───┴───┘                     │
│                                      │
├──────────────────────────────────────┤
│                                      │
│           [ ⬆️ ]                      │
│      [ ⬅️ ][ ⏹️ ][ ➡️ ]               │
│           [ ⬇️ ]                      │
│                                      │
│    Your choice: [ ⬆️ ]   ✓ LOCKED    │
│                                      │
└──────────────────────────────────────┘

D-PAD style controls. 5 options.
Intuitive, fast.
```

---

## 💰 Monetization

### Character Skins
- Different animals
- Costumes
- Seasonal themes

### Tile Themes
- Stone tiles (default)
- Glass tiles
- Ice tiles
- Candy tiles
- Space tiles

### Step Effects
- Footprint trails
- Sparkle step
- Fire trail

### Fall Effects
- Standard fall
- Poof
- Dramatic slow-mo
- Feathers

---

## ✅ 50K+ CCU Checklist

- [x] **Universally understood** — Move on grid, don't fall
- [x] **Cute theme** — Animals on tiles
- [x] **Hidden decisions** — Secret direction choice
- [x] **Visible positions** — See where everyone is
- [x] **Spatial strategy** — "If I go here, he might go there..."
- [x] **Shrinking arena** — Tiles vanish from edges
- [x] **Collision risk** — Same tile = danger
- [x] **Knockout! feel** — Position-based prediction
- [x] **Any device** — D-pad controls

---

## 🎯 One-Sentence Pitch

**"Step on the grid — but tiles vanish and collisions kill."**

---

*Status: ORIGINAL CONCEPT - Spatial Strategy*
*Formula: A (Timer-Reveal) + SPATIAL*
*Core: Grid movement + vanishing tiles + collision*
----------------------------------------------------------------------

What if we changed the game play to, based on how many people standing on the tiles, so when 8 round start, if > 4 player standing on the same tiles, tiles will be broken and all 4 get eliminated, we dont know each other tiles position too right, soo its based on rng and reading mind tension, i do think we have some potential here