# 🐹 Hamster Wheel

> **Formula:** A (Timer-Reveal, like Knockout!)
> **Physics Type:** RUNNING (momentum, treadmill, falling)
> **Theme:** Hamsters running on a giant wheel
> **Status:** Experimental - Novel vertical arena

---

## 🎯 Core Concept

```
All hamsters on one GIANT wheel.
Wheel spinning constantly.
Pick which way to RUN (hidden).
Bump into others = knockback.
Fall off wheel = eliminated.
Wheel speeds up over time.
```

---

## 🧬 Why This Could Work

| Element | Knockout! | Hamster Wheel |
|---------|-----------|---------------|
| Universally understood | ✅ Ice | ✅ Hamster wheel (everyone knows) |
| Cute theme | ✅ Penguins | ✅ Hamsters (round, cute) |
| Physics comedy | ✅ Flying off ice | ✅ Tumbling, falling off wheel |
| Hidden decisions | ✅ Aim direction | ✅ Run direction |
| Knockback | ✅ Push | ✅ Bump while running |
| Shrinking arena | ✅ Ice breaks | ✅ Wheel speeds up |
| Turn-based | ✅ | ✅ |

**UNIQUE VALUE:** VERTICAL curved arena - running on a wheel creates unique gameplay space.

---

## 🎮 Turn Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      HAMSTER WHEEL                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CONSTANT: Wheel is always spinning (sets the pace)            │
│                                                                 │
│   PHASE 1: RUN DIRECTION (hidden, 10 sec)                       │
│   → Pick: Run WITH wheel, AGAINST wheel, or SIDEWAYS            │
│   → Running against = move backward relative to wheel           │
│   → Running with = move forward relative to wheel               │
│   → You DON'T see others' choices                               │
│                                                                 │
│   PHASE 2: RUN POWER (hidden)                                   │
│   → Pick how fast to run (1-10)                                 │
│   → Faster = more movement = more collision power               │
│                                                                 │
│   PHASE 3: LOCK                                                 │
│   → "Running in 3... 2... 1..."                                 │
│                                                                 │
│   PHASE 4: RUN!                                                 │
│   → ALL hamsters run at once                                    │
│   → Collisions happen                                           │
│   → Knockback from bumping                                      │
│   → Knocked off wheel = eliminated                              │
│                                                                 │
│   PHASE 5: SPEED UP                                             │
│   → Wheel spins faster                                          │
│   → Need to run faster just to stay in place                    │
│   → Repeat until winner                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏟️ Arena Design

```
SIDE VIEW (the wheel):

              ╭─────────────╮
           ╭──│             │──╮
          │   │  🐹      🐹 │   │
         │    │             │    │
        │     │🐹         🐹│     │
        │     ├─────────────┤     │  ← Wheel edge
        │     │🐹    🐹    🐹│     │
         │    │             │    │
          │   │  🐹      🐹 │   │
           ╰──│             │──╯
              ╰─────────────╯
                    ↻ SPINNING
                    
    Hamsters run on the INSIDE surface
    Wheel rotates constantly
    Fall out of either side = eliminated
```

### Top-Down View (Looking into wheel)

```
    ←── WHEEL SPINNING THIS WAY ───→
    
    ════════════════════════════════════
    │ 🐹    🐹       🐹      🐹    🐹 │
    ════════════════════════════════════
    
    Hamsters spread across the width
    Can bump each other sideways
```

---

## 🏃 Running Physics

```
THE TREADMILL EFFECT:

Wheel spins → floor moves under you
Not running = you slide backward
Running WITH wheel = stay in place
Running AGAINST wheel = move forward

RELATIVE MOVEMENT:

    Wheel speed: →→→ (3 units/turn)
    
    Hamster A runs →→ (2 with wheel): Net = →→→→→ (moves forward 5)
    Hamster B runs ← (1 against wheel): Net = →→ (moves forward 2)
    Hamster C stands still: Net = →→→ (slides with wheel 3)
    
COLLISION:

    🐹 →→→ ←←← 🐹
         💥
    Faster hamster knocks slower one
    Knocked hamster might fall off wheel!
```

---

## 🐹 Why Hamsters Work

**Hamsters are perfect for this:**
- 🐹 Round, cute, fluffy
- 🎡 Hamster wheels = iconic association
- 🏃 Known for running (energetic)
- 📱 Simple shape (reads well)
- 😊 Non-threatening, family-friendly

**Skin variations:**
- Different hamster colors
- Costumes (superhero, ninja)
- Different rodents (mice, gerbils)

---

## 📱 Mobile Controls

```
┌──────────────────────────────────────┐
│  Round 3      ⏱️ 7       Left: 5     │
├──────────────────────────────────────┤
│                                      │
│      [Wheel View - inside]           │
│                                      │
│   ════🐹═══🐹══YOU══🐹════           │
│                                      │
├──────────────────────────────────────┤
│                                      │
│      RUN DIRECTION:                  │
│                                      │
│   [⬅️ AGAINST] [⏹️ STOP] [WITH ➡️]    │
│                                      │
│   SPEED: [●●●●○○○○○○]                │
│                                      │
└──────────────────────────────────────┘

3 direction options + speed
Simple!
```

---

## ⚡ Shrinking Mechanic: Wheel Speeds Up

```
ROUND 1-3: Slow wheel
- Easy to stay in place
- Gentle bumps

ROUND 4-6: Medium speed
- Need to run to stay in place
- More chaotic bumps

ROUND 7+: FAST WHEEL!
- Hard to keep up
- Lots of tumbling
- Survival mode
```

---

## ⚠️ Potential Challenges

- [ ] Wheel concept might be hard to visualize
- [ ] Running "against" vs "with" might confuse
- [ ] Vertical/cylindrical arena is unusual
- [ ] Camera angle needs careful design

---

## ✅ 50K+ CCU Checklist

- [x] Universally understood (hamster wheel)
- [x] Cute theme (hamsters)
- [x] Hidden decisions (run direction + speed)
- [x] Knockback physics (bumping)
- [x] Shrinking mechanic (wheel speeds up)
- [x] Turn-based
- [x] Visible gameplay
- [⚠️] Physics comedy (needs good animation)
- [x] Dramatic reveal
- [x] Solo friendly
- [x] Any device

---

*Status: EXPERIMENTAL - Novel arena shape, needs prototyping*
