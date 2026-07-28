# Infection: Puppy Edition 🐶🦠

**Status:** SAVED - Classic + Cute
**Theme:** Muddy puppies tag game
**Style:** Infection tag with adorable twist

---

## 🎮 Core Concept

Classic infection tag but with puppies. One "Muddy Puppy" starts. Tag others = they become muddy too. Mud spreads like infection. Last clean puppy wins. Bath powerups to cleanse. Dog park map.

**The Twist:** Not scary zombies — just dirty adorable puppies. Kid-friendly infection.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                   INFECTION: PUPPY EDITION                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → All puppies spawn CLEAN (shiny, happy)                   │
│      → One random puppy becomes MUDDY                           │
│      → Muddy puppy: brown, dripping mud, mischievous            │
│      → Timer: 2 minutes                                         │
│                                                                 │
│   2. INFECTION CHASE                                            │
│      → Muddy puppy chases clean puppies                         │
│      → TAG = clean puppy becomes MUDDY                          │
│      → Newly muddy joins the chase                              │
│      → Mud spreads through the pack                             │
│                                                                 │
│   3. CLEAN PUPPY SURVIVAL                                       │
│      → Run, hide, evade                                         │
│      → Use obstacles and hiding spots                           │
│      → Find BATH powerups (limited)                             │
│      → Stay clean as long as possible                           │
│                                                                 │
│   4. BATH MECHANIC                                              │
│      → Bath tubs spawn around map (rare)                        │
│      → If MUDDY, jump in = CLEANSED                             │
│      → Become clean again!                                      │
│      → Bath disappears after use                                │
│      → Limited baths per round                                  │
│                                                                 │
│   5. ROUND END                                                  │
│      → Timer ends OR all puppies muddy                          │
│      → Last clean puppy = WINNER                                │
│      → If timer ends with clean puppies = they win              │
│      → Points based on survival time                            │
│                                                                 │
│   6. MATCH END                                                  │
│      → Play 3 rounds                                            │
│      → Different starting muddy each round                      │
│      → Most total points = CHAMPION                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🐕 Puppy Types

### Clean Puppies (Survivors)
| Appearance | Abilities |
|------------|-----------|
| Shiny, fluffy coat | Slightly faster |
| Happy expression | Can use baths |
| Sparkle effects | Can hide in small spots |
| Bright colors | Scared bark (alert others) |

### Muddy Puppies (Infected)
| Appearance | Abilities |
|------------|-----------|
| Brown muddy coat | Mud trail (visible path) |
| Mischievous grin | Can see clean puppies through walls briefly |
| Dripping mud | Pounce attack (short dash) |
| Dirty paw prints | Teamwork (coordinate with other muddy) |

---

## 🏃 Movement Mechanics

### All Puppies
| Action | Effect |
|--------|--------|
| Run | Standard movement |
| Sprint | Faster, leaves trail |
| Jump | Hop over obstacles |
| Crawl | Fit through small spaces |
| Bark | Alert or distract |

### Clean Puppy Exclusive
```
HIDE:
- Fit in dog houses
- Under benches
- In bushes
- Muddy can't fit (too messy)

BATH USE:
- Jump in bath tub
- 2 sec channel
- Become clean (if muddy)
- Bath disappears
```

### Muddy Puppy Exclusive
```
POUNCE:
- Short dash forward
- Faster than running
- 3 sec cooldown
- Good for catching runners

MUD SENSE:
- Briefly see nearest clean puppy
- Through walls
- 10 sec cooldown
- Helps coordinate hunts
```

---

## 🛁 Bath Mechanic

### Bath Spawns
| Time | Baths Available |
|------|-----------------|
| Start | 0 |
| 30 sec | 2 baths spawn |
| 60 sec | 1 more bath |
| 90 sec | 1 more bath |
| Total | 4 baths per round |

### Using Baths
```
WHO CAN USE:
- Only MUDDY puppies
- Clean puppies can't use (already clean)

HOW TO USE:
- Jump into bath tub
- 2 second channel (vulnerable!)
- Emerge CLEAN
- Bath disappears

STRATEGY:
- Save bath location knowledge
- Race to bath when tagged
- Guard baths to deny muddy players
```

---

## 🗺️ Map Design

### "Dog Park" (Main Map)
```
┌─────────────────────────────────────────┐
│  🏠    🌳🌳    🛝        🌳🌳    🏠     │
│       🌳  🌳   ┌──┐     🌳  🌳          │
│               │🧺│         💧          │
│  🪑    🛁     └──┘              🪑      │
│                                         │
│       🏠              🏠                │
│  💧        🌳🌳🌳           🛁    🌳    │
│            🌳  🌳                 🌳    │
│  🪑              🐕              🪑     │
│                (spawn)                  │
└─────────────────────────────────────────┘

🏠 = Dog house (hiding spot)
🌳 = Trees (vision block)
🪑 = Bench (hide under)
🛁 = Bath tub spawn
💧 = Puddle (slows movement)
🧺 = Toy basket (climbable)
🛝 = Playground equipment
```

### Other Map Ideas
**"Pet Store"**
- Aisles of pet supplies
- Cages to hide in
- Fish tanks as obstacles
- Checkout counters

**"Backyard"**
- Fenced yard
- Pool (instant bath!)
- Garden (hiding)
- Shed

**"Puppy Daycare"**
- Indoor facility
- Play pens
- Nap rooms
- Ball pits

---

## 📊 Infection Progression

### Typical Round Timeline
```
0:00 - 1 muddy puppy, 7 clean
0:20 - First tag, 2 muddy
0:35 - Chain tags, 4 muddy
0:50 - Half infected, 4 muddy
1:00 - Bath spawns, maybe 1 cleansed
1:20 - Hunting gets intense
1:40 - 1-2 clean remaining
2:00 - Round ends
```

### Infection Speed Balance
- Early: Muddy is alone, hard to catch
- Mid: Growing pack, easier to surround
- Late: Swarm hunting, very hard for clean

---

## 🎮 Game Modes

### Classic (Above)
- 1 starting muddy
- 8 players
- 2 minute rounds

### Double Trouble
- 2 starting muddy
- Faster infection
- Shorter rounds (90 sec)

### Bath Party
- More baths spawn
- Longer rounds
- More back-and-forth

### No Baths
- Pure survival
- No cleansing
- Once muddy, always muddy

### Muddy Wins
- Muddy team tries to infect ALL
- Clean team tries to survive timer
- Team scoring

### Freeze Tag Variant
- Tagged = frozen (not muddy)
- Clean can unfreeze friends
- All frozen = muddy wins

---

## 🎨 Visual Design

### Clean Puppies
- Golden retriever, dalmatian, corgi, etc.
- Shiny coats with sparkles
- Wagging tails
- Happy barks

### Muddy Puppies
- Same breeds but DIRTY
- Brown mud covering
- Mud splatter effects
- Playful mischievous look (not scary!)

### Map Aesthetics
- Bright, colorful dog park
- Sunny day
- Butterflies, birds
- Happy atmosphere (despite infection theme)

### Sound Design
- Puppy barks and yips
- Playful music
- Splashing bath sounds
- Squeaky toys

---

## 💰 Monetization Ideas

- Puppy breed skins
- Collar accessories
- Mud patterns (funny shapes)
- Bath effects (bubbles)
- Bark sounds
- Victory poses
- Puppy toys (cosmetic)

---

## 🎯 Why This Could Work

1. ✅ **Proven mechanic** (infection tag)
2. ✅ **Cute theme** (puppies!)
3. ✅ **Kid-friendly** (not scary like zombies)
4. ✅ **Wholesome** (just mud, not death)
5. ✅ **Bath twist** (comeback mechanic)
6. ✅ **Fast rounds** (2 min)
7. ✅ **Social** (hunting together)
8. ✅ **Accessible** (everyone knows tag)
