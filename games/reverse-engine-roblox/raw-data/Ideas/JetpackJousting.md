# Jetpack Jousting 🚀⚔️

**Status:** SAVED - Exploring variations
**Theme:** Jetpack aerial combat
**Style:** Two versions — Real-time OR Turn-based

---

## 🎮 Core Concept

Players with jetpacks on a platform over the void. Movement IS the weapon. You can only damage while BOOSTING. Hovering = safe but can't kill. Commit to boost = risk/reward.

**The Twist:** Your attack IS your movement. No separate attack button.

---

# VERSION A: Real-Time (Action)

## 🔄 Core Loop (Real-Time)

```
┌─────────────────────────────────────────────────────────────────┐
│                 JETPACK JOUSTING - REAL TIME                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. SPAWN                                                      │
│      → All players on floating platform                         │
│      → Everyone has jetpack                                     │
│      → Infinite fuel for hovering                               │
│                                                                 │
│   2. MOVEMENT STATES                                            │
│      → HOVER: Float in place, safe, can't damage                │
│      → FLY: Move around, safe, can't damage                     │
│      → BOOST: Fast dash, CAN damage, has cooldown               │
│                                                                 │
│   3. COMBAT                                                     │
│      → Press BOOST to dash in facing direction                  │
│      → Hit someone while boosting = KNOCKBACK                   │
│      → Strong enough knockback = off platform = DEAD            │
│      → Boost has 3 second cooldown                              │
│                                                                 │
│   4. RISK/REWARD                                                │
│      → Boosting = commitment (can't stop mid-boost)             │
│      → Miss = you might fly off yourself!                       │
│      → Cooldown = vulnerable after missing                      │
│      → Hoverers are safe but can't win                          │
│                                                                 │
│   5. WIN                                                        │
│      → Last player on platform wins                             │
│      → OR most knockouts after time limit                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# VERSION B: Turn-Based (Like Knockout!)

## 🔄 Core Loop (Turn-Based)

```
┌─────────────────────────────────────────────────────────────────┐
│                 JETPACK JOUSTING - TURN BASED                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → All players on floating platform                         │
│      → Everyone has jetpack                                     │
│      → Players positioned around edges                          │
│                                                                 │
│   2. AIM PHASE (Timer: 5 seconds)                               │
│      → Everyone SIMULTANEOUSLY aims their boost direction       │
│      → Rotate your character to point where you'll dash         │
│      → Set POWER (1-10) = how far/fast you boost                │
│      → Can see others aiming (mind games!)                      │
│                                                                 │
│   3. LOCK PHASE                                                 │
│      → Timer ends, everyone locked in                           │
│      → "3... 2... 1... BOOST!"                                  │
│                                                                 │
│   4. EXECUTION PHASE                                            │
│      → Everyone boosts SIMULTANEOUSLY                           │
│      → Collisions = knockback based on power difference         │
│      → Higher power wins collision, but goes further (risk!)    │
│      → Some players might boost off the edge themselves!        │
│                                                                 │
│   5. RESOLUTION                                                 │
│      → Players who fell off = eliminated                        │
│      → Survivors reposition for next round                      │
│      → Platform SHRINKS slightly each round                     │
│      → Repeat until 1 player left                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🆚 Comparing Both Versions

| Aspect | Real-Time | Turn-Based |
|--------|-----------|------------|
| Pacing | Fast, chaotic | Strategic, deliberate |
| Skill Type | Reflexes, timing | Prediction, positioning |
| Commitment | Boost cooldown | Round-by-round |
| Mind Games | React in moment | Read others' aims |
| Casual Friendly | Medium | High (no reflex needed) |
| Similar To | Super Smash Bros | Knockout! |

---

## 🚀 Boost Mechanics (Both Versions)

### Power Levels (Turn-Based)
| Power | Distance | Speed | Knockback Dealt |
|-------|----------|-------|-----------------|
| 1-3 | Short | Slow | Light |
| 4-6 | Medium | Medium | Medium |
| 7-9 | Long | Fast | Heavy |
| 10 | MAX | Very Fast | Massive (but risky!) |

### Collision Physics
```
When two players collide mid-boost:

HIGHER POWER WINS:
- Winner continues (reduced speed)
- Loser gets knocked back hard

EQUAL POWER:
- Both bounce off each other
- Both take medium knockback

THE RISK:
- High power = more knockback dealt
- BUT high power = travel further
- Might boost yourself off the edge!
```

---

## 🗺️ Platform Design

### Basic Platform
- Circular floating island
- Void below (fall = death)
- Shrinks each round (turn-based)
- Or stays same (real-time)

### Platform Variations

**"Sky Ring"**
- Donut shape
- Hole in middle (extra danger)
- Can boost through center

**"Cloud Platforms"**
- Multiple small platforms
- Gaps between them
- Risk boosting between platforms

**"Moving Islands"**
- Platforms slowly rotate
- Or drift apart
- Changes geometry each round

---

## 🧠 Strategic Depth

### Turn-Based Strategy

**Reading Opponents**
- Watch where they aim
- Predict their power level
- Counter-position yourself

**Positioning**
- Stay center = safer but predictable
- Stay edge = risky but can bait
- Group with others = avoid 1v1

**Power Mind Games**
- High power = scary, people dodge
- Low power = safe, but low impact
- Fake high (aim away) then go low

### Real-Time Strategy

**Timing**
- Wait for others to boost first
- Punish missed boosts (cooldown window)
- Chain boosts (hit multiple people)

**Spacing**
- Stay near center
- Bait boosts then dodge
- Counter-boost into enemy boosts

---

## 🎨 Visual Design

### Jetpack Effects
- Flame trail while boosting
- Hover particles
- Different colored flames (customization)

### Characters
- Could be any theme:
  - Robots
  - Astronauts
  - Penguins with jetpacks
  - Italian brainrot with rockets

### Platform
- Floating island
- Clear edges (glow/outline)
- Void below with clouds/stars

### Impact Effects
- Collision sparks
- Knockback trails
- Fall = dramatic camera follow

---

## 🎮 Alternative Cores (Same Feel, Different Mechanic)

### **Cannonball Clash** 🎱
*Turn-based pool/golf style*
```
- Players are balls on a platform
- Aim direction + set power
- Everyone "shoots" simultaneously  
- Knock others off, stay on yourself
- Physics-based chaos
```

### **Bumper Penguins** 🐧
*Turn-based bumper cars*
```
- Penguins on ice platform
- Choose direction + slide power
- Slide simultaneously
- Bounce off each other
- Ice shrinks each round
```

### **Rocket Dodge** 🚀
*Turn-based projectile game*
```
- Everyone aims and fires a rocket
- Rockets fly simultaneously
- Dodge others' rockets
- Get hit = eliminated
- Rockets can collide mid-air
```

### **Sumo Seals** 🦭
*Turn-based pushing*
```
- Seals on shrinking platform
- Choose push direction + power
- Execute simultaneously
- Push = affect self AND target
- Sumo-style ring-out
```

---

## 💰 Monetization Ideas

- Jetpack skins
- Character skins
- Boost trail effects
- Impact effects
- Victory poses
- Platform themes

---

## ❓ Open Questions

1. **Which version?** Real-time or turn-based?
2. **Theme?** Robots? Animals? Brainrot?
3. **Platform shape?** Circle? Square? Complex?
4. **Power-ups?** Shield? Double boost? Magnet pull?
5. **Team mode?** 2v2 jetpack battles?

---

## 🎯 Recommendation

**For your goal (1M in 2026, kids audience):**

I'd recommend **Turn-Based** version because:
1. ✅ Proven formula (Knockout has 68K+ players)
2. ✅ Casual friendly (no reflexes needed)
3. ✅ Easy to develop (no real-time netcode)
4. ✅ Clear moments (aim → execute → result)
5. ✅ Mind games appeal to all skill levels

**Best alternative core: "Bumper Penguins"**
- Penguins = proven cute animal appeal
- Ice = natural shrinking mechanic
- Sliding = funny physics
- Turn-based = accessible

---

## 🎯 Why This Could Work

1. ✅ **Movement = weapon** (unique hook)
2. ✅ **Risk/reward** (power vs control)
3. ✅ **Visual clarity** (see boosts, see falls)
4. ✅ **Fast rounds** (quick eliminations)
5. ✅ **Skill expression** (prediction, positioning)
6. ✅ **Flexible theme** (can reskin to any trend)
