# Color Dash 🎨🏃

**Status:** SAVED - Fall Guys energy
**Theme:** Color-coded survival
**Style:** Quick reaction + elimination

---

## 🎮 Core Concept

Floor tiles are different COLORS. Announcer calls a color. You have 3 SECONDS to reach that color. Wrong color tiles DISAPPEAR. Fall = eliminated. Colors get faster, tiles get fewer. Fall Guys meets musical chairs.

**The Twist:** Simple concept, frantic execution. Everyone understands colors.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                        COLOR DASH                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → Floor grid of COLORED TILES                              │
│      → Colors: Red, Blue, Yellow, Green, Purple, Orange         │
│      → All players standing on tiles                            │
│      → Void/water below the floor                               │
│                                                                 │
│   2. COLOR CALL                                                 │
│      → Announcer: "BLUE!"                                       │
│      → Timer appears: 3 SECONDS                                 │
│      → Music intensifies                                        │
│      → Players scramble                                         │
│                                                                 │
│   3. SCRAMBLE PHASE                                             │
│      → Run to BLUE tiles                                        │
│      → Push others out of the way                               │
│      → Find a spot, HOLD position                               │
│      → Limited blue tiles = competition                         │
│                                                                 │
│   4. TILE COLLAPSE                                              │
│      → Timer hits 0                                             │
│      → ALL non-blue tiles SHAKE                                 │
│      → Then FALL into void                                      │
│      → Anyone on wrong tile = FALLS                             │
│      → Eliminated!                                              │
│                                                                 │
│   5. FLOOR RESET                                                │
│      → Tiles regenerate (new layout)                            │
│      → Fewer of each color                                      │
│      → Next color call                                          │
│      → Repeat                                                   │
│                                                                 │
│   6. ESCALATION                                                 │
│      → Faster calls (less time)                                 │
│      → Fewer safe tiles                                         │
│      → Multiple colors at once ("BLUE OR GREEN!")               │
│      → Color CHANGES mid-countdown                              │
│                                                                 │
│   7. VICTORY                                                    │
│      → Last player standing = WINNER                            │
│      → Or survive X rounds                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Tile System

### Tile Colors
| Color | Visual | Rarity (Start) | Rarity (Late) |
|-------|--------|----------------|---------------|
| Red 🔴 | Bright red | Common | Rare |
| Blue 🔵 | Bright blue | Common | Rare |
| Yellow 🟡 | Bright yellow | Common | Uncommon |
| Green 🟢 | Bright green | Common | Uncommon |
| Purple 🟣 | Bright purple | Uncommon | Very Rare |
| Orange 🟠 | Bright orange | Uncommon | Very Rare |

### Tile Distribution
```
ROUND 1-3: (Easy)
- Floor: 80 tiles
- Each color: ~13 tiles
- Plenty of options

ROUND 4-6: (Medium)
- Floor: 50 tiles
- Each color: ~8 tiles
- Getting crowded

ROUND 7-9: (Hard)
- Floor: 30 tiles
- Each color: ~5 tiles
- Fighting for spots

ROUND 10+: (Chaos)
- Floor: 15 tiles
- Some colors: 2-3 tiles only
- Pure mayhem
```

---

## ⏱️ Timer Progression

| Round | Time Given | Difficulty |
|-------|-----------|------------|
| 1-3 | 5 seconds | Easy |
| 4-6 | 4 seconds | Medium |
| 7-9 | 3 seconds | Hard |
| 10-12 | 2.5 seconds | Very Hard |
| 13+ | 2 seconds | Insane |

---

## 🗣️ Announcer Calls

### Basic Calls
```
"RED!"         → Get on red tiles
"BLUE!"        → Get on blue tiles
"YELLOW!"      → Get on yellow tiles
(etc.)
```

### Advanced Calls (Later Rounds)
```
"BLUE OR GREEN!"     → Either color safe
"NOT RED!"           → Any color except red
"PRIMARY COLORS!"    → Red, blue, or yellow only
"WARM COLORS!"       → Red, orange, yellow
"COOL COLORS!"       → Blue, green, purple
```

### Chaos Calls (Very Late)
```
"BLUE!... WAIT, YELLOW!"   → Changes mid-countdown
"???"                       → Random, revealed at last second
"RAINBOW!"                  → Only multi-colored tiles safe
```

---

## 🏃 Movement & Combat

### Movement
| Action | Speed | Use |
|--------|-------|-----|
| Walk | Slow | Precise positioning |
| Run | Fast | Get to distant color |
| Sprint | Very Fast | Emergency dash |
| Jump | Hop | Cross gaps, avoid pushes |
| Dive | Lunge | Last-second tile reach |

### Combat (Optional Push Mode)
```
PUSH:
- Shove another player
- They stumble/move back
- Can push off tiles
- Can push into wrong colors
- Adds chaos layer
```

### Diving Mechanic
```
DIVE (Spacebar):
- Lunge forward
- Cover extra distance
- Reach tile at last second
- Risk: might overshoot
- Clutch play potential
```

---

## 🗺️ Floor Layouts

### "Standard Grid"
```
🔴🔵🟡🟢🟣🟠🔴🔵
🔵🟡🟢🟣🟠🔴🔵🟡
🟡🟢🟣🟠🔴🔵🟡🟢
🟢🟣🟠🔴🔵🟡🟢🟣
🟣🟠🔴🔵🟡🟢🟣🟠
🟠🔴🔵🟡🟢🟣🟠🔴

- Predictable layout
- Colors evenly spread
- Fair distribution
```

### "Clustered"
```
🔴🔴🔴🔵🔵🔵🟡🟡
🔴🔴🔵🔵🔵🟡🟡🟡
🟢🟢🟢🟣🟣🟣🟠🟠
🟢🟢🟣🟣🟣🟠🟠🟠

- Colors grouped
- Must travel far for some
- Strategic positioning
```

### "Random Chaos"
```
🔴🟣🔵🟠🟡🔴🟢🔵
🟡🔴🟢🔵🟣🟡🟠🔴
🔵🟠🔵🟡🔴🟢🔵🟣
🟢🔵🟣🟠🔵🔴🟡🟢

- Completely random
- No patterns
- Chaotic scrambles
```

---

## 🎮 Game Modes

### Classic (Above)
- 12 players
- Escalating difficulty
- Last standing wins

### Team Colors
- 2-4 teams
- Teams share safe color
- "Red Team" always safe on red
- Knock other teams off

### Speed Dash
- 1.5 second timer always
- Fast from start
- Quick games

### Memory Mode
- Color shown ONCE at start
- Then called without visual
- Must remember layout

### Survival
- Survive 3 minutes
- Constant calls
- No winner, just survival

### Color Blind Mode
- Shapes instead of colors
- Circle, square, triangle, etc.
- Accessibility + variety

---

## 🎨 Visual Design

### Tile Aesthetics
- Bright, saturated colors
- Glowing outlines
- Visible from any angle
- Shake animation before fall

### Tile Fall Animation
```
CALL ENDS:
1. Wrong tiles shake (0.5 sec)
2. Cracks appear
3. Tiles crumble/fall
4. Players on them fall
5. Dramatic void below
```

### Arena Theme Options
**"Neon Arcade"**
- Dark background
- Glowing tiles
- Synthwave aesthetic

**"Candy World"**
- Tiles are candies
- Sweet aesthetics
- Colorful and cheerful

**"Space Station"**
- Tiles are panels
- Fall into space
- Sci-fi vibes

---

## 🎁 Power-Ups

| Power-Up | Effect | Duration |
|----------|--------|----------|
| Speed Boost | Faster running | 8 sec |
| Teleport | Instant move to any tile | 1 use |
| Color Reveal | See next color early | Next call |
| Float | Don't fall if wrong tile | 1 save |
| Freeze | Others can't move | 2 sec |

---

## 🎵 Audio Design

### Announcer Voice
- Clear, energetic
- Dramatic color calls
- Building tension
- Celebration on survival

### Music
- Upbeat, fast tempo
- Intensifies with timer
- Silence at call moment
- Beat drop on tile fall

### Sound Effects
- Tile shake rumble
- Tile fall crash
- Crowd reactions
- Victory fanfare

---

## 💰 Monetization Ideas

- Character skins
- Trail effects
- Fall animations
- Victory dances
- Announcer voice packs
- Tile themes
- Color blind assists

---

## 🎯 Why This Could Work

1. ✅ **Instant understanding** (reach the color)
2. ✅ **Fall Guys proven** (tile survival)
3. ✅ **Visual clarity** (colors are universal)
4. ✅ **Fast rounds** (2-3 min total)
5. ✅ **Escalating tension** (harder each round)
6. ✅ **Spectator friendly** (easy to watch)
7. ✅ **Stream moments** (clutch dives, fails)
8. ✅ **All ages** (toddlers know colors)
9. ✅ **Simple to scale** (more players, bigger grid)
