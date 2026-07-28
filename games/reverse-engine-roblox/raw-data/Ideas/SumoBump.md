# 🔴 Sumo Bump

> **Formula:** A (Timer-Reveal, like Knockout!)
> **Physics Type:** CHARGING (direct knockback, like Knockout!)
> **Theme:** Round animals doing sumo wrestling
> **Status:** Safe Bet - Closest to proven Knockout! formula

---

## 🎯 Core Concept

```
Round animals (pandas? bears?) on a circular platform.
Classic sumo: push others out of the ring.
Pick CHARGE DIRECTION (hidden).
Pick POWER (hidden).
Bump = knockback (like Knockout!).
Circle shrinks over time.
```

---

## 🧬 Why This Could Work

| Element | Knockout! | Sumo Bump |
|---------|-----------|-----------|
| Universally understood | ✅ Ice | ✅ Sumo/pushing (universal) |
| Cute theme | ✅ Penguins | ✅ Pandas/bears (round, cute) |
| Physics comedy | ✅ Flying off ice | ✅ Flying off ring |
| Hidden decisions | ✅ Aim direction | ✅ Charge direction |
| Knockback | ✅ Push | ✅ Sumo push |
| Shrinking arena | ✅ Ice breaks | ✅ Ring shrinks |
| Turn-based | ✅ | ✅ |

**THIS IS THE SAFEST OPTION** - Essentially Knockout! with a different theme.

---

## 🎮 Turn Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        SUMO BUMP                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   PHASE 1: CHARGE DIRECTION (hidden, 10 sec)                    │
│   → Pick which direction to charge                              │
│   → 8 directions (or toward specific player?)                   │
│   → You DON'T see others' choices                               │
│                                                                 │
│   PHASE 2: CHARGE POWER (hidden)                                │
│   → Pick how hard to charge (1-10)                              │
│   → More power = more knockback                                 │
│   → But also more distance traveled = risk!                     │
│                                                                 │
│   PHASE 3: LOCK                                                 │
│   → "Charging in 3... 2... 1..."                                │
│   → Suspense builds                                             │
│                                                                 │
│   PHASE 4: BUMP!                                                │
│   → ALL animals charge at once                                  │
│   → Collisions happen                                           │
│   → Knockback based on power differential                       │
│   → Knocked out of ring = eliminated                            │
│                                                                 │
│   PHASE 5: SHRINK                                               │
│   → Ring gets smaller                                           │
│   → Less room to maneuver                                       │
│   → Repeat until winner                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏟️ Arena Design

```
TOP-DOWN VIEW (circular sumo ring):

              ╭───────────────╮
           ╭──│               │──╮
          │   │  🐼     🐻    │   │
         │    │               │    │
        │     │🐨    ⭕   🐼│     │  ⭕ = Center
        │     │               │     │
         │    │  🐻     🐨   │    │
          │   │               │   │
           ╰──│               │──╯
              ╰───────────────╯
              
    Classic circular arena
    Simple, clean, readable
    
    Outside circle = eliminated
```

---

## 🐼 Why Pandas/Bears Work

**Round animals = perfect for sumo:**
- 🐼 Pandas are ROUND (sumo body type!)
- 🐻 Bears are chunky and cute
- 🐨 Koalas are round and cuddly
- They look like they SHOULD be bumping each other
- Natural "heavy" feeling = satisfying knockback

**Comparison to penguins:**
- Penguins = sliding on ice (makes sense)
- Pandas = bumping in sumo ring (makes sense)
- Both are cute, both are round, both work!

---

## ⚡ Collision Physics

```
HEAD-ON COLLISION:

    🐼 →→→ ←←← 🐻
         💥
    Higher power wins!
    Winner: small knockback
    Loser: BIG knockback

SIDE COLLISION:

    🐼 →→→
           🐻 ↓
            💥
    Both knocked in combined direction

MISS:

    🐼 →→→
              🐻 (wasn't there)
    
    🐼 charged into empty space
    Might go off edge if high power!
```

---

## 📱 Mobile Controls

```
┌──────────────────────────────────────┐
│  Round 3      ⏱️ 7       Left: 5     │
├──────────────────────────────────────┤
│                                      │
│      [Sumo Ring View]                │
│                                      │
│         🐼 YOU                       │
│                                      │
├──────────────────────────────────────┤
│                                      │
│      CHARGE DIRECTION:               │
│   [↖️] [⬆️] [↗️]                      │
│   [⬅️] [🐼] [➡️]                      │
│   [↙️] [⬇️] [↘️]                      │
│                                      │
│   POWER: [●●●●○○○○○○]                │
│                                      │
└──────────────────────────────────────┘

Identical to Knockout! controls
Proven to work!
```

---

## 🔄 Shrinking Mechanic

```
ROUND 1-3: Full ring
╭─────────────────╮
│                 │
│  BIG RING       │
│                 │
╰─────────────────╯

ROUND 4-6: Shrinking
╭───────────╮
│           │
│  MEDIUM   │
│           │
╰───────────╯

ROUND 7+: Tiny!
╭─────╮
│SMALL│
╰─────╯
```

---

## 🆚 Knockout! vs Sumo Bump

| Aspect | Knockout! | Sumo Bump |
|--------|-----------|-----------|
| Theme | Penguins on ice | Pandas in sumo ring |
| Arena | Square-ish ice | Circular ring |
| Aesthetic | Cold, icy, blue | Warm, wooden, red |
| Character shape | Penguin (tall-ish) | Panda (round) |
| Knockback feel | Sliding | Bumping |
| Secret target? | Yes | Optional (could add or not) |

**Key difference:** Knockout! has SECRET TARGETS. Do we add that to Sumo Bump?

---

## 🎯 With or Without Secret Targets?

**Option A: No secret targets (simpler)**
- Just charge in a direction
- Pure prediction: "Where will others be?"
- Simpler than Knockout!

**Option B: With secret targets (like Knockout!)**
- Each round, assigned one player to target
- Must bump THAT player
- Adds the "who's hunting me?" paranoia
- Closer clone of Knockout!

**Recommendation:** Start with Option A to differentiate. Add Option B as a game mode if needed.

---

## 💰 Monetization

### Animal Skins
- Panda (classic)
- Bear (brown, polar)
- Koala
- Hamster (round!)
- Seal
- Costume variants

### Ring Themes
- Classic sumo (wooden)
- Neon arena
- Space platform
- Candy ring
- Ice ring (ironic!)

### Effects
- Charge trails
- Impact effects
- Elimination effects

---

## ⚠️ Potential Challenges

- [ ] Might be seen as "just a Knockout! clone"
- [ ] Need to differentiate enough
- [ ] Secret target mechanic: include or not?

---

## ✅ 50K+ CCU Checklist

- [x] Universally understood (sumo/pushing)
- [x] Cute theme (pandas/bears)
- [x] Hidden decisions (charge direction + power)
- [x] Knockback physics (sumo push)
- [x] Shrinking arena (ring shrinks)
- [x] Turn-based
- [x] Visible gameplay
- [x] Physics comedy (flying pandas!)
- [x] Dramatic reveal
- [x] Solo friendly
- [x] Any device

---

*Status: SAFE BET - Closest to proven Knockout! formula, lowest risk*
