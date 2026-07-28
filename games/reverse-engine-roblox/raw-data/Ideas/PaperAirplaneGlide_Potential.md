# ✈️ Paper Airplane Glide

> **Formula:** A (Timer-Reveal, like Knockout!) with unique SURVIVAL twist
> **Physics Type:** GLIDING (air currents, staying airborne)
> **Theme:** Paper airplanes floating through the air
> **Status:** Experimental - Unique "stay up" mechanic

---

## 🎯 Core Concept

```
Everyone IS a paper airplane.
Gliding through the air.
Pick TILT direction (hidden).
Pick TILT amount (hidden).
Crash into others = both lose altitude.
Ground = eliminated.
STAY AIRBORNE longest = win!
Wind gusts push everyone (environmental chaos).
```

---

## 🧬 Why This Could Work

| Element | Knockout! | Paper Airplane Glide |
|---------|-----------|---------------------|
| Universally understood | ✅ Ice | ✅ Paper airplanes (everyone made one!) |
| Cute theme | ✅ Penguins | ✅ Colorful paper planes |
| Physics comedy | ✅ Flying off ice | ✅ Spiraling, crashing, nosediving |
| Hidden decisions | ✅ Aim direction | ✅ Tilt direction |
| Elimination | ✅ Fall off edge | ✅ Hit the ground |
| Shrinking arena | ✅ Ice breaks | ✅ Altitude drops / ceiling lowers |
| Turn-based | ✅ | ✅ |

**UNIQUE VALUE:**
- VERTICAL survival (stay UP, not stay ON)
- Different spatial feel than flat arena games
- Paper airplane = universal childhood memory
- Graceful + chaotic physics

---

## 🎮 Turn Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                   PAPER AIRPLANE GLIDE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CONSTANT: Everyone slowly losing altitude (gravity)           │
│                                                                 │
│   PHASE 1: TILT DIRECTION (hidden, 10 sec)                      │
│   → Pick which way to tilt your plane                           │
│   → Up-tilt = gain altitude but slow down                       │
│   → Down-tilt = lose altitude but speed up                      │
│   → Left/right = turn                                           │
│                                                                 │
│   PHASE 2: TILT AMOUNT (hidden)                                 │
│   → Pick how much to tilt (1-10)                                │
│   → More tilt = more dramatic move                              │
│   → Too much tilt = might stall or nosedive!                    │
│                                                                 │
│   PHASE 3: LOCK                                                 │
│   → "Gliding in 3... 2... 1..."                                 │
│                                                                 │
│   PHASE 4: GLIDE!                                               │
│   → ALL planes adjust simultaneously                            │
│   → Paths cross, collisions happen                              │
│   → Collision = both lose altitude!                             │
│   → Wind gust might push everyone! (random event)               │
│                                                                 │
│   PHASE 5: ALTITUDE CHECK                                       │
│   → Anyone below minimum altitude = CRASH = eliminated          │
│   → Minimum altitude RISES each round (shrinking!)              │
│   → Repeat until one plane left                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏟️ Arena Design

```
SIDE VIEW (showing altitude):

    CEILING (optional upper boundary)
    ═══════════════════════════════════════════
    
    HIGH ALTITUDE
         ✈️        ✈️
              ✈️              ✈️
    MEDIUM ALTITUDE
                   ✈️    ✈️
         ✈️                        ✈️
    LOW ALTITUDE
    
    ─ ─ ─ ─ ─ ─ DANGER LINE ─ ─ ─ ─ ─ ─
    (rises each round!)
    
    ═══════════════════════════════════════════
    GROUND (touch = eliminated!)
```

### Top-Down View

```
    ╭───────────────────────────────────╮
    │                                   │
    │   ✈️→     ↙️✈️      ✈️↓           │
    │                                   │
    │      ✈️↗️     ←✈️      ✈️↖️        │
    │                                   │
    │   ✈️←              ✈️→            │
    │                                   │
    ╰───────────────────────────────────╯
    
    Planes moving in different directions
    Can see everyone's position (horizontal)
    Altitude shown by shadow size or indicator
```

---

## ✈️ Glide Physics

```
BASIC FLIGHT:

    All planes constantly losing altitude (gravity)
    Must actively TILT UP to gain height
    
    ✈️ ----→ (level flight, slowly descending)
    
    ✈️ ↗️ (tilt up = gain altitude, slow down)
    
    ✈️ ↘️ (tilt down = lose altitude, speed up)

COLLISION:

    ✈️→    ←✈️
        💥
    Both planes knocked DOWN (lose altitude)
    Both planes spin briefly (visual chaos)
    
STALL (too much up-tilt):

    ✈️
    │ (plane stalls!)
    │
    ↓ (falls straight down!)
    
    Risk of over-correcting!

WIND GUST (environmental):

    💨💨💨💨💨💨💨
    ✈️→  ✈️→  ✈️→  (all pushed!)
    
    Random gusts push all planes
    Creates chaos and upsets plans
```

---

## 📄 Paper Airplane Design

**Why paper airplanes work:**
- 📄 Universal (everyone has made one)
- ✈️ Graceful flight = satisfying
- 🎨 Easy to customize (colors, patterns)
- 📱 Simple shape (reads well on any device)
- 🧒 Nostalgic (classroom, childhood)

**Visual style:**
- Clean, colorful paper
- Folded paper texture
- Simple geometric shape
- Trail effects as they glide

---

## 🌬️ Wind Mechanic (Environmental Chaos)

```
WIND EVENTS (random each round):

"Calm skies"
→ No wind, pure skill round

"Light breeze from left"
→ All planes pushed slightly right

"Strong gust from below!"  
→ All planes pushed UP (bonus altitude!)

"Downdraft!"
→ All planes pushed DOWN (danger!)

"Turbulence!"
→ Random small pushes in all directions
```

**This adds unpredictability** - even skilled players can get surprised!

---

## 📱 Mobile Controls

```
┌──────────────────────────────────────┐
│  Round 3      ⏱️ 7       Left: 5     │
│  Altitude: ████████░░ (HIGH)         │
├──────────────────────────────────────┤
│                                      │
│      [Sky View]                      │
│                                      │
│   ☁️    ✈️ YOU    ☁️    ✈️           │
│                                      │
├──────────────────────────────────────┤
│                                      │
│      TILT DIRECTION:                 │
│   [↖️⬆️] [⬆️⬆️] [↗️⬆️]  (gain alt)    │
│   [⬅️ ] [ ✈️ ] [ ➡️]  (level)       │
│   [↙️⬇️] [⬇️⬇️] [↘️⬇️]  (lose alt)    │
│                                      │
│   TILT AMOUNT: [●●●●○○○○○○]          │
│                                      │
└──────────────────────────────────────┘
```

---

## 📉 Shrinking Mechanic: Rising Floor

```
ROUND 1-3: Low danger line
═══════════════════════════════════════
    Lots of airspace!
    Easy to stay up
─ ─ ─ ─ (danger line low) ─ ─ ─ ─
═══════════════════════════════════════

ROUND 4-6: Rising danger
═══════════════════════════════════════
    Less room!
─ ─ ─ (danger line rising) ─ ─ ─
═══════════════════════════════════════

ROUND 7+: Tight squeeze!
═══════════════════════════════════════
─ ─ (danger line HIGH!) ─ ─
═══════════════════════════════════════
    Must stay very high!
    One collision = death!
```

---

## 💰 Monetization

### Plane Skins
- Classic white paper
- Colored paper (red, blue, green)
- Patterned paper (stripes, polka dots)
- Origami style (more folds)
- Special materials (gold, galaxy)

### Trail Effects
- Sparkle trail
- Rainbow trail
- Cloud trail
- Fire trail (ironic for paper!)

### Sky Themes
- Blue sky with clouds
- Sunset
- Night sky with stars
- Indoor (classroom ceiling)
- Space (floating in zero-g variant?)

### Crash Effects
- Crumple animation
- Confetti burst
- Poof into paper bits

---

## 🎯 What Makes This DIFFERENT

```
KNOCKOUT!: Stay ON (horizontal survival)
PAPER AIRPLANE: Stay UP (vertical survival)

KNOCKOUT!: Push others OFF
PAPER AIRPLANE: Knock others DOWN

KNOCKOUT!: Platform shrinks inward
PAPER AIRPLANE: Floor rises upward

It's the SAME FORMULA but in a different DIMENSION!
```

---

## ⚠️ Potential Challenges

- [ ] Altitude might be hard to visualize on 2D screen
- [ ] Vertical gameplay less intuitive than horizontal
- [ ] "Stay up" vs "knock off" - different feel
- [ ] Wind randomness might feel unfair
- [ ] Paper airplanes less "cute" than animals?

---

## 💡 Solution: Add Pilots!

```
What if tiny animals are PILOTING the paper airplanes?

    ✈️🐰 (bunny pilot!)
    ✈️🐱 (cat pilot!)
    
Now we have:
- Cute animals ✅
- Paper airplane physics ✅
- Best of both worlds!
```

---

## ✅ 50K+ CCU Checklist

- [x] Universally understood (paper airplanes)
- [⚠️] Cute theme (needs animal pilots to be cuter)
- [x] Hidden decisions (tilt direction + amount)
- [x] Knockback physics (collision = altitude loss)
- [x] Shrinking mechanic (rising danger line)
- [x] Turn-based
- [x] Visible gameplay
- [x] Physics comedy (spiraling, crashing, wind chaos)
- [x] Dramatic reveal
- [x] Solo friendly
- [x] Any device

---

*Status: EXPERIMENTAL - Unique vertical gameplay, needs animal pilots*
------------
This have a potential, but is hard to implement in terms of physic of the game, and 2 phase of action controlling would take a lot of time.