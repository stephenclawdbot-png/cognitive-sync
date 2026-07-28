# Pet Rescue Rush 🐕🐈🚨

**Status:** SAVED - Wholesome + competitive
**Theme:** Rescue pets + Collection race
**Style:** Real-time collection with sabotage

---

## 🎮 Core Concept

Map is full of LOST PETS. Race to collect them and return to shelter. Most pets rescued = WIN. Can carry multiple pets but you're slower. Can steal pets from others and set traps.

**The Twist:** Wholesome theme + competitive sabotage = unique combo.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                     PET RESCUE RUSH                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → Map spawns with scattered LOST PETS                      │
│      → Pets: dogs, cats, bunnies, hamsters, etc.                │
│      → Shelter (safe zone) in center                            │
│      → All players start at shelter                             │
│      → Timer: 90 seconds                                        │
│                                                                 │
│   2. COLLECTION PHASE                                           │
│      → Run to pets, PICK UP (auto on contact)                   │
│      → Can carry 1-3 pets at once                               │
│      → More pets = SLOWER movement                              │
│      → Pets follow you in a line                                │
│                                                                 │
│   3. DELIVERY PHASE                                             │
│      → Return to shelter with pets                              │
│      → Pets safely deposited = POINTS                           │
│      → 1 pet = 1 point                                          │
│      → Rare pets = 2-3 points                                   │
│                                                                 │
│   4. SABOTAGE OPTIONS                                           │
│      → PUSH other players = they DROP all pets                  │
│      → Dropped pets can be stolen                               │
│      → Set TRAPS on paths                                       │
│      → Steal pets mid-carry                                     │
│                                                                 │
│   5. ROUND END                                                  │
│      → Timer hits 0                                             │
│      → Pets being carried = NOT counted                         │
│      → Only delivered pets count                                │
│      → Most points = WINNER                                     │
│                                                                 │
│   6. MATCH END                                                  │
│      → Play 3 rounds                                            │
│      → Total points across rounds                               │
│      → Highest total = CHAMPION                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🐾 Pet Types

### Common Pets (1 Point)
| Pet | Speed When Carried | Spawn Rate |
|-----|-------------------|------------|
| Puppy 🐕 | -10% per pet | Common |
| Kitten 🐈 | -10% per pet | Common |
| Bunny 🐰 | -10% per pet | Common |
| Hamster 🐹 | -5% per pet | Common |

### Rare Pets (2 Points)
| Pet | Speed When Carried | Spawn Rate |
|-----|-------------------|------------|
| Golden Retriever 🦮 | -15% per pet | Uncommon |
| Persian Cat 🐱 | -15% per pet | Uncommon |
| Parrot 🦜 | -10% per pet | Uncommon |

### Legendary Pets (3 Points)
| Pet | Speed When Carried | Spawn Rate |
|-----|-------------------|------------|
| Panda 🐼 | -25% | Rare |
| Penguin 🐧 | -20% | Rare |
| Red Panda 🦊 | -20% | Rare |

---

## 🏃 Movement Mechanics

### Carry System
```
CARRYING PETS:
- Auto-pickup on contact
- Max 3 pets at once
- Pets follow in a line behind you
- Each pet slows you down

SPEED PENALTY:
- 0 pets: 100% speed
- 1 pet: 90% speed
- 2 pets: 75% speed
- 3 pets: 60% speed
- Rare/Legendary: extra penalty
```

### Movement Options
| Action | Speed | Use |
|--------|-------|-----|
| Walk | Slow | Precise navigation |
| Run | Normal | Standard travel |
| Sprint | Fast | Limited stamina |
| Dash | Burst | Escape/Chase |

---

## ⚔️ Sabotage Mechanics

### Push Attack
```
PUSH EFFECT:
- Knock player back
- They DROP ALL PETS
- Pets scatter nearby
- 2 second stun

COUNTER:
- Dash away when pushed
- Keep some pets
- Fight back
```

### Traps
| Trap | Cost | Effect | Duration |
|------|------|--------|----------|
| Net | $50 | Stops player 2 sec | 30 sec |
| Banana | $25 | Slip, drop 1 pet | 20 sec |
| Cage | $100 | Steals 1 pet from passers | 45 sec |
| Alarm | $75 | Alerts you when triggered | 60 sec |

### Stealing
```
STEAL OPTIONS:
- Push = drop all pets
- Pet Snatch = grab pet from enemy's line
- Trap Cage = auto-steal passers

DEFENSE:
- Dash through traps
- Stay away from others
- Travel in groups (protection)
```

---

## 🗺️ Map Design

### Map Layout
```
┌─────────────────────────────────────────┐
│  [Pets]          [Pets]         [Pets]  │
│                                         │
│     [Pets]    ┌─────────┐    [Pets]     │
│               │ SHELTER │               │
│               │ (safe)  │               │
│     [Pets]    └─────────┘    [Pets]     │
│                                         │
│  [Pets]          [Pets]         [Pets]  │
└─────────────────────────────────────────┘

- Shelter in center
- Pets scattered around edges
- Multiple paths to shelter
- Hiding spots for traps
```

### Map Themes
**"City Streets"**
- Urban environment
- Alleyways, parks
- Cars as obstacles
- Fire hydrants, benches

**"Farm"**
- Barn is shelter
- Fields with pets
- Mud puddles (slow)
- Hay bales for cover

**"Beach"**
- Lifeguard station is shelter
- Beach pets (crabs, seals)
- Sand slows movement
- Water areas

---

## 💰 Economy System

### Earning Money
| Action | Reward |
|--------|--------|
| Deliver common pet | +$10 |
| Deliver rare pet | +$25 |
| Deliver legendary pet | +$50 |
| Push enemy | +$5 |
| Win round | +$100 |

### Spending Money
- Buy traps
- Buy power-ups
- Buy cosmetics (permanent)

---

## 🎁 Power-Ups

| Power-Up | Effect | Duration |
|----------|--------|----------|
| Speed Shoes | No carry penalty | 15 sec |
| Pet Magnet | Nearby pets come to you | 10 sec |
| Shield | Can't be pushed | 8 sec |
| Extra Carry | Carry 5 pets max | Round |
| Teleport | Instant return to shelter | 1 use |

---

## 🎮 Game Modes

### Classic (Above)
- 8 players
- 90 sec rounds
- 3 rounds total

### Team Rescue
- 2 teams of 4
- Shared team score
- Protect each other

### No Sabotage
- Pure collection race
- No pushing or traps
- Family friendly

### Golden Rush
- Only legendary pets
- High stakes
- Shorter rounds (60 sec)

### Endless
- Pets keep spawning
- Play until tired
- Personal best tracking

---

## 🎨 Visual Design

### Art Style
- Cute, cartoony pets
- Big eyes, fluffy
- Happy animations
- Hearts when delivered

### Shelter
- Cozy building
- Pets visible inside
- Counter showing score
- Celebration on delivery

### Effects
- Pet pickup: sparkles
- Delivery: hearts explosion
- Steal: dramatic grab
- Trap: cartoon effects

---

## 💰 Monetization Ideas

- Character skins
- Pet skins (cosmetic only)
- Shelter decorations
- Trap skins
- Victory celebrations
- Pet accessories

---

## 🎯 Why This Could Work

1. ✅ **Wholesome theme** (rescue pets = feel good)
2. ✅ **Competitive twist** (sabotage + stealing)
3. ✅ **Cute animals** (kids love pets)
4. ✅ **Simple goal** (collect and return)
5. ✅ **Strategic depth** (carry amount, routes, traps)
6. ✅ **Fast rounds** (90 sec)
7. ✅ **Risk/reward** (more pets = slower)
8. ✅ **Social chaos** (stealing from friends)
