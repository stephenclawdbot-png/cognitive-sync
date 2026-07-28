# Memory Mayhem 🧠💥

**Status:** SAVED - High potential
**Theme:** Simon Says memory game + physical chaos
**Style:** Turn-based pattern memory with real-time interference

---

## 🎮 Core Concept

Platform lights up in a PATTERN (like Simon Says). Players must step on tiles IN ORDER. Wrong step = zapped = eliminated. BUT other players can PUSH you onto wrong tiles. Memory + chaos.

**The Twist:** It's not just memory — it's memory UNDER PRESSURE with physical interference.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                     MEMORY MAYHEM LOOP                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. PATTERN DISPLAY PHASE (5-10 seconds)                       │
│      → All players stand on SAFE ZONE (edges)                   │
│      → Platform tiles light up in SEQUENCE                      │
│      → Tile 1 lights... Tile 2 lights... Tile 3 lights...       │
│      → Players must MEMORIZE the order                          │
│      → Pattern length increases each round                      │
│                                                                 │
│   2. EXECUTION PHASE (Timer based)                              │
│      → "GO!" - Players must step on tiles IN ORDER              │
│      → Step on Tile 1 → Tile 2 → Tile 3...                      │
│      → Correct step = tile lights GREEN, move to next           │
│      → Wrong step = tile lights RED, you get ZAPPED             │
│      → Zapped = ELIMINATED from game                            │
│                                                                 │
│   3. CHAOS PHASE (During execution)                             │
│      → Players can PUSH each other!                             │
│      → Push enemy onto wrong tile = they get zapped             │
│      → Push enemy off platform = eliminated                     │
│      → Shoving, blocking, chaos                                 │
│                                                                 │
│   4. ROUND END                                                  │
│      → Timer expires OR only 1 player completes pattern         │
│      → Survivors continue to next round                         │
│      → Pattern gets LONGER (more tiles)                         │
│      → Speed gets FASTER (less time to memorize)                │
│                                                                 │
│   5. VICTORY                                                    │
│      → Last player standing wins                                │
│      → OR complete the final impossible pattern                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔢 Pattern Progression

| Round | Pattern Length | Display Speed | Execute Time |
|-------|----------------|---------------|--------------|
| 1 | 3 tiles | Slow | 15 sec |
| 2 | 4 tiles | Slow | 15 sec |
| 3 | 5 tiles | Medium | 12 sec |
| 4 | 6 tiles | Medium | 12 sec |
| 5 | 7 tiles | Fast | 10 sec |
| 6 | 8 tiles | Fast | 10 sec |
| 7+ | 9+ tiles | Very Fast | 8 sec |

### Pattern Display Example
```
Round 3 Pattern (5 tiles):

Display sequence:
1. Tile A4 lights up (1 sec)
2. Tile B2 lights up (1 sec)
3. Tile C5 lights up (1 sec)
4. Tile A1 lights up (1 sec)
5. Tile D3 lights up (1 sec)

Players memorize: A4 → B2 → C5 → A1 → D3
```

---

## 🗺️ Platform Layout

### Grid Design
```
    1   2   3   4   5
  ┌───┬───┬───┬───┬───┐
A │   │   │   │   │   │
  ├───┼───┼───┼───┼───┤
B │   │   │   │   │   │
  ├───┼───┼───┼───┼───┤
C │   │   │   │   │   │  ← 5x5 Grid
  ├───┼───┼───┼───┼───┤
D │   │   │   │   │   │
  ├───┼───┼───┼───┼───┤
E │   │   │   │   │   │
  └───┴───┴───┴───┴───┘

Safe zones: Around the edges (before execution starts)
```

### Tile States
| State | Visual | Meaning |
|-------|--------|---------|
| Neutral | Gray | Inactive |
| Pattern | Yellow flash | Part of sequence |
| Correct | Green glow | Stepped correctly |
| Wrong | Red flash + ZAP | Wrong step, eliminated |
| Active | Pulsing | Current tile to step on |

---

## ⚡ Elimination Mechanics

### Wrong Step
```
Player steps on wrong tile:
→ Tile flashes RED
→ Electric zap effect
→ Player ragdolls
→ "ELIMINATED!" text
→ Player becomes spectator
```

### Pushed Off
```
Player pushed off platform edge:
→ Falls into void
→ "ELIMINATED!" text
→ Player becomes spectator
```

### Pushed Onto Wrong Tile
```
Player A pushes Player B
Player B lands on wrong tile
→ Same as wrong step
→ Player B eliminated
→ Player A continues (if they didn't mess up their own sequence)
```

### Timeout
```
Timer expires, player hasn't finished:
→ All remaining tiles flash RED
→ Player zapped
→ "TOO SLOW!" text
```

---

## 🤜 Combat/Push Mechanics

### Push Attack
| Property | Value |
|----------|-------|
| Range | Short (must be close) |
| Cooldown | 1 second |
| Knockback | Medium (1-2 tiles) |
| Stun | 0.5 sec (can't move) |

### Push Strategies
```
DEFENSIVE PUSH:
- Someone running at you
- Push them away from your path
- Continue your pattern

OFFENSIVE PUSH:
- Find someone concentrating
- Push them onto wrong tile
- They get eliminated

BLOCKING:
- Stand on a tile someone needs
- They have to go around or push you
- Wastes their time

CHAIN PUSH:
- Push Player A into Player B
- Both get knocked off course
- Double elimination potential
```

---

## 🧠 Memory Strategies

### Memorization Techniques
```
CHUNKING:
- Group tiles: "A4-B2, C5-A1, D3"
- Remember in pairs/triplets
- Easier for longer patterns

VISUALIZATION:
- Imagine the path as a shape
- "It makes an L then zigzags"
- Spatial memory

REPETITION:
- Whisper to yourself
- "4-2-5-1-3, 4-2-5-1-3..."
- Verbal memory
```

### Execution Strategies
```
SPEED RUN:
- Memorize perfectly
- Execute as fast as possible
- Finish before chaos reaches you

WAIT AND WATCH:
- Let others go first
- See if they get zapped (confirms wrong tiles)
- But timer is running...

FOLLOW THE LEADER:
- Watch someone who seems confident
- Follow their path
- Risk: they might be wrong too

CHAOS AGENT:
- Don't care about winning
- Just push everyone
- Fun but low score
```

---

## 🎮 Game Modes

### Classic (Described above)
- Memorize pattern
- Step in order
- Push others
- Last standing wins

### Team Memory
- 2 teams
- Each player memorizes PART of pattern
- Must communicate
- First team to complete wins

### No Push Mode
- Pure memory challenge
- No interference
- Fastest completion wins
- Good for practice

### Speed Memory
- Very fast patterns
- Short execution time
- Pure reflex memory
- No time for pushing

### Reverse Memory
- Pattern shown BACKWARDS
- Must step in REVERSE order
- Extra brain twist

### Mirror Memory
- Pattern shows on display
- But platform is MIRRORED
- Must translate in your head

---

## 📊 Scoring System

| Action | Points |
|--------|--------|
| Complete pattern | +100 × round number |
| Push someone into elimination | +50 |
| Survive a round | +25 |
| First to complete pattern | +50 bonus |
| Win the game | +300 |

---

## 🎨 Visual Design

### Platform Aesthetic
**"Neon Arcade"**
- Glowing neon tiles
- Dark background
- Synthwave vibes
- Satisfying light effects

**"Game Show"**
- TV studio look
- Audience (NPCs cheering)
- Host voice announcements
- Confetti for wins

**"Sci-Fi Lab"**
- Holographic tiles
- Futuristic environment
- Electric effects
- Robot announcer

### Tile Effects
- Pattern display: Bright flash + sound
- Correct step: Satisfying green + "ding!"
- Wrong step: Red flash + electric zap + "BZZT!"
- Push: Shockwave effect

### Elimination
- Dramatic slow-mo
- Ragdoll physics
- Sparks flying
- Comedic death sounds

---

## 🔊 Audio Design

### Pattern Display
- Each tile = different musical note
- Creates melody to remember
- Audio memory helps!

### Feedback
- Correct step: Ascending tone
- Wrong step: Buzzer
- Push: Impact sound
- Timer low: Warning beeps

---

## 💰 Monetization Ideas

- Character skins
- Tile themes (neon, nature, space)
- Zap effects
- Victory dances
- Announcer voice packs
- Trail effects

---

## ❓ Open Questions

1. **Grid size?** 5x5? 6x6? Dynamic?
2. **Push strength?** 1 tile? 2 tiles?
3. **Elimination mode?** Immediate or lives?
4. **Audio patterns?** Musical tiles help memory?
5. **Theme?** Arcade? Game show? Sci-fi?

---

## 🎯 Why This Could Work

1. ✅ **Known mechanic** (Simon Says is universal)
2. ✅ **Added twist** (push interference)
3. ✅ **Skill expression** (memory + combat)
4. ✅ **Escalating difficulty** (longer patterns)
5. ✅ **Fast rounds** (30-60 sec each)
6. ✅ **Party game energy** (chaos with friends)
7. ✅ **Multiple strategies** (memory vs chaos)
8. ✅ **Satisfying feedback** (lights, sounds)
9. ✅ **Spectator friendly** (fun to watch others fail)
