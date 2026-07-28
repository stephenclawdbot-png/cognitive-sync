# ⚖️ Seesaw Scramble

> **Formula:** A (Timer-Reveal, like Knockout!)
> **Physics Type:** BALANCE (tipping, weight distribution)
> **Theme:** Animals on a giant seesaw/balance beam
> **Status:** Experimental - Novel mechanic

---

## 🎯 Core Concept

```
Animals on a giant seesaw (or multiple seesaws).
Seesaw tips based on weight distribution.
Pick where to MOVE (hidden).
If seesaw tips too far = one side falls off.
Must balance while trying to unbalance others.
```

---

## 🧬 Why This Could Work

| Element | Knockout! | Seesaw Scramble |
|---------|-----------|-----------------|
| Universally understood | ✅ Ice | ✅ Seesaw (playground classic) |
| Cute theme | ✅ Penguins | ✅ Cute animals |
| Physics comedy | ✅ Flying off ice | ✅ Tipping, sliding, falling |
| Hidden decisions | ✅ Aim direction | ✅ Movement position |
| Knockback | ✅ Push | ⚠️ Gravity/tipping instead |
| Shrinking arena | ✅ Ice breaks | ⚠️ Need different mechanic |
| Turn-based | ✅ | ✅ |

**UNIQUE VALUE:** BALANCE physics - collective weight matters, creates cooperation/betrayal dynamics.

---

## 🎮 Turn Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                     SEESAW SCRAMBLE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   PHASE 1: MOVE DECISION (hidden, 10 sec)                       │
│   → Everyone picks where to move on the seesaw                  │
│   → Left side? Right side? Center?                              │
│   → You DON'T see others' choices                               │
│                                                                 │
│   PHASE 2: LOCK                                                 │
│   → "Moving in 3... 2... 1..."                                  │
│   → Suspense builds                                             │
│                                                                 │
│   PHASE 3: MOVE + TIP                                           │
│   → ALL animals move to their chosen positions                  │
│   → Seesaw calculates weight on each side                       │
│   → If unbalanced = seesaw TIPS                                 │
│   → Animals on lower side SLIDE toward edge                     │
│   → Slide off = eliminated                                      │
│                                                                 │
│   PHASE 4: REBALANCE                                            │
│   → Seesaw resets to neutral                                    │
│   → Eliminated players removed                                  │
│   → Repeat until winner                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏟️ Arena Design

### Single Giant Seesaw

```
BALANCED:
                    ┌───────┐
                    │FULCRUM│
    ════════════════╪═══════╪════════════════
    🐻  🐰       🐹  │       │  🐸  🐰    🐻
                    └───────┘

TIPPED LEFT (too much weight on left):

         🐻🐻🐰🐹
    ═══════════╲
                ╲
                 ╲═══════════
                        🐸🐰
                    └───────┘
    
    Left side animals SLIDE OFF!
```

### Multiple Smaller Seesaws

```
    ════╪════     ════╪════     ════╪════
    🐰  │  🐻     🐹  │  🐸     🐰  │  🐻
        │             │             │
    
    Each seesaw is a mini-battle
    Eliminated from your seesaw = out
    Winners from each seesaw face off?
```

---

## 🐾 The Weight System

```
WEIGHT DISTRIBUTION:

LEFT SIDE          CENTER          RIGHT SIDE
   -3    -2    -1    0    +1    +2    +3
    ├─────┼─────┼─────┼─────┼─────┼─────┤
    
Each animal = 1 weight unit
Position determines which side gets weight

EXAMPLE:
- 3 animals on left (-3 total)
- 2 animals on right (+2 total)
- Net: -1 (tips LEFT)
- Left side animals at risk!
```

---

## 🎭 The Social Dynamic

```
COOPERATION:
"If we all go center, nobody falls..."
"Let's balance it out..."

BETRAYAL:
"I said I'd go right but actually went left..."
"Everyone went left, I'll go right and watch them fall!"

CHAOS:
"Where is everyone going?!"
"The seesaw is tipping!"
```

**This creates SOCIAL GAMEPLAY that Knockout! has with secret targets, but different flavor.**

---

## 📱 Mobile Controls

```
┌──────────────────────────────────────┐
│  Round 3      ⏱️ 7       Left: 5     │
├──────────────────────────────────────┤
│                                      │
│      [Seesaw View - side angle]      │
│                                      │
│      ════════╪════════               │
│      🐰 🐻   │   🐹 🐸               │
│                                      │
├──────────────────────────────────────┤
│                                      │
│      WHERE DO YOU MOVE?              │
│                                      │
│   [FAR    [LEFT] [CENTER] [RIGHT] [FAR  │
│    LEFT]                          RIGHT]│
│                                      │
└──────────────────────────────────────┘

5 positions to choose from
Simple tap selection
```

---

## 🔄 Shrinking Mechanic Options

**Option A: Seesaw gets shorter**
- Each round, edges break off
- Less room to spread out
- More forced to cluster

**Option B: Fulcrum becomes sensitive**
- Each round, less weight difference needed to tip
- Round 1: Need 3+ difference to tip
- Round 5: Need 1+ difference to tip

**Option C: Multiple seesaws merge**
- Start with 4 small seesaws (2 players each)
- Winners merge onto bigger seesaw
- Final round: one giant seesaw

---

## ⚠️ Potential Challenges

- [ ] Might feel like pure luck (everyone guessing)
- [ ] Less "physics comedy" than bouncing/sliding
- [ ] Balance mechanic might be confusing
- [ ] Need to visualize weight clearly
- [ ] Different from Knockout! (risky - untested)

---

## ✅ 50K+ CCU Checklist

- [x] Universally understood (seesaw)
- [x] Cute theme (animals)
- [x] Hidden decisions (position choice)
- [⚠️] Knockback physics (tipping instead - different)
- [⚠️] Shrinking arena (needs design work)
- [x] Turn-based
- [x] Visible gameplay
- [⚠️] Physics comedy (tipping less funny than flying?)
- [x] Dramatic reveal
- [x] Solo friendly
- [x] Any device

---

*Status: EXPERIMENTAL - Novel mechanic, needs validation*
