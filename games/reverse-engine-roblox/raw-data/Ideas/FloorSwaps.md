# Floor Swaps 🔄🏃

**Status:** SAVED - Unique randomness mechanic
**Theme:** Tiles swap positions unpredictably
**Style:** Survival with RNG positioning

---

## 🎮 Core Concept

Floor is a grid of tiles. Each tile has players on it. Tiles SWAP POSITIONS periodically — your tile might suddenly be at the edge next to the void. You can't control where you end up. Adapt, survive, push others off.

**The Twist:** The GROUND moves, not just you. Randomness you can't control, only react to.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                        FLOOR SWAPS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → Grid of tiles (5x5 = 25 tiles)                           │
│      → All players spawn on tiles                               │
│      → Void surrounds the grid                                  │
│      → Combat enabled                                           │
│                                                                 │
│   2. NORMAL PHASE (10 seconds)                                  │
│      → Move freely between tiles                                │
│      → Push/fight other players                                 │
│      → Try to knock others off                                  │
│      → Standard battle royale                                   │
│                                                                 │
│   3. SWAP WARNING                                               │
│      → "SWAPPING IN 3... 2... 1..."                             │
│      → Tiles start glowing                                      │
│      → Players brace themselves                                 │
│      → Can't predict outcome                                    │
│                                                                 │
│   4. SWAP PHASE                                                 │
│      → Tiles TELEPORT to new positions                          │
│      → Random shuffle                                           │
│      → Your safe center tile = might be edge now                │
│      → Edge tiles = might be center                             │
│      → Players teleport WITH their tiles                        │
│                                                                 │
│   5. CHAOS                                                      │
│      → New layout revealed                                      │
│      → Some players now at edge (danger!)                       │
│      → Some players now next to enemies                         │
│      → Quick adaptation needed                                  │
│                                                                 │
│   6. TILE REMOVAL (Every 2 swaps)                               │
│      → 1-2 random tiles DISAPPEAR                               │
│      → Anyone on them = falls = eliminated                      │
│      → Grid shrinks over time                                   │
│                                                                 │
│   7. REPEAT                                                     │
│      → Normal phase → Swap → Normal phase                       │
│      → Until 1 player remains                                   │
│                                                                 │
│   8. VICTORY                                                    │
│      → Last player standing = WINNER                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏁 Grid Layout

### Starting Grid (5x5)
```
┌───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │
├───┼───┼───┼───┼───┤
│ 6 │ 7 │ 8 │ 9 │10 │
├───┼───┼───┼───┼───┤
│11 │12 │13 │14 │15 │  VOID surrounds
├───┼───┼───┼───┼───┤
│16 │17 │18 │19 │20 │
├───┼───┼───┼───┼───┤
│21 │22 │23 │24 │25 │
└───┴───┴───┴───┴───┘

SAFE: Center tiles (7,8,9,12,13,14,17,18,19)
RISKY: Edge tiles (1,2,3,4,5,6,10,11,15,16,20,21,22,23,24,25)
CORNERS: Most dangerous (1,5,21,25)
```

### After Swap Example
```
┌───┬───┬───┬───┬───┐
│17 │ 3 │21 │ 9 │12 │
├───┼───┼───┼───┼───┤
│ 5 │19 │ 1 │23 │ 7 │
├───┼───┼───┼───┼───┤
│14 │11 │ 8 │ 2 │18 │  Completely shuffled!
├───┼───┼───┼───┼───┤
│22 │ 6 │15 │13 │ 4 │
├───┼───┼───┼───┼───┤
│10 │24 │16 │20 │25 │
└───┴───┴───┴───┴───┘

Player on tile 13 (was center) = now edge!
Player on tile 21 (was corner) = now center!
```

---

## 🔄 Swap Mechanics

### Swap Rules
```
WHAT SWAPS:
- Tile positions shuffle
- Players go WITH their tile
- Items on tiles (if any) travel too

WHAT DOESN'T SWAP:
- Grid shape stays same
- Void stays around edges
- Player positions ON tile stay same
```

### Swap Frequency
| Phase | Swap Timer | Intensity |
|-------|------------|-----------|
| Early | Every 15 sec | Calm |
| Mid | Every 10 sec | Active |
| Late | Every 7 sec | Chaotic |
| Final | Every 5 sec | Insane |

### Swap Animation
```
BEFORE:
- Warning countdown (3 sec)
- Tiles glow
- Rising hum sound

DURING:
- Quick teleport (0.5 sec)
- Flash effect
- Disorienting

AFTER:
- New layout revealed
- 1 sec freeze (process new positions)
- Resume action
```

---

## 💀 Elimination Methods

### Fall Off
- Step off tile edge
- Pushed off by enemy
- Tile at edge, pushed into void

### Tile Removal
```
EVERY 2 SWAPS:
- 1-2 random tiles DISAPPEAR
- No warning which ones
- Anyone standing on it = falls
- Grid gets smaller

REMOVAL VISUAL:
- Tile shakes
- Cracks appear
- Falls into void
- Player falls with it
```

### Combat Push
- Push attack
- Knockback
- Into void = eliminated

---

## ⚔️ Combat System

### Push Attack
| Property | Value |
|----------|-------|
| Range | Short melee |
| Knockback | 1-2 tile distances |
| Cooldown | 1.5 seconds |

### Combat Strategy
```
BEFORE SWAP:
- Push enemies to edge tiles
- When swap happens, they might stay at edge
- Or get unlucky with new position

AFTER SWAP:
- Quick assess new positions
- If enemy at edge, RUSH them
- If YOU'RE at edge, escape to center

TILE AWARENESS:
- Know which tiles are about to disappear
- Push enemies onto doomed tiles
- Stay on healthy tiles
```

---

## 🧠 Strategic Depth

### Tile Position Strategy
```
CAN'T CONTROL WHERE YOU END UP
BUT YOU CAN:
- Stay center of your TILE (not tile center of grid)
- React quickly after swap
- Push enemies at vulnerable moments
- Avoid standing on edges of tiles
```

### Reading the Grid
```
AFTER SWAP, QUICKLY:
1. Where am I? (edge/center)
2. Where are enemies?
3. Who's most vulnerable?
4. Escape route if I'm in danger
```

### Luck vs Skill Balance
```
LUCK (40%):
- Where your tile ends up
- Which tiles get removed

SKILL (60%):
- Quick adaptation
- Combat timing
- Positioning on tile
- Reaction speed
```

---

## 🎮 Game Modes

### Classic (Above)
- 8-12 players
- 5x5 grid
- Tiles shrink over time

### Mega Grid
- 16-20 players
- 7x7 grid
- Longer games

### Speed Swaps
- Swaps every 5 sec from start
- Pure chaos
- Quick rounds

### Team Swaps
- 2 teams
- Only knock enemy team off
- Teammates can't hurt each other

### No Combat
- Pure survival
- Only tile removal eliminates
- Luck-heavy

### Preview Swaps
- Brief preview of next layout
- 2 sec to see where you'll be
- More strategic

---

## 🎨 Visual Design

### Tile Aesthetics
**"Floating Platforms"**
- Stone/metal tiles
- Hovering over void
- Sci-fi energy

**"Candy Grid"**
- Colorful candy tiles
- Chocolate void below
- Sweet theme

**"Ice Floes"**
- Ice tiles on water
- Crack before removal
- Arctic theme

### Swap Effects
- Teleport flash
- Grid shimmer
- Disorientation blur
- Sound whoosh

### Removal Effects
- Tiles crack
- Fall with debris
- Dramatic void pull

---

## 🎁 Power-Ups

| Power-Up | Effect | Duration |
|----------|--------|----------|
| Anchor | Stay in same position next swap | 1 swap |
| Preview | See where you'll end up | Next swap |
| Tile Jump | Teleport to any tile | 1 use |
| Float | Don't fall if tile removed | 1 removal |
| Mega Push | 2x knockback | 10 sec |

---

## ❓ Special Tiles

| Tile Type | Effect |
|-----------|--------|
| Bouncy | Bounce off instead of fall |
| Sticky | Can't be pushed off |
| Speed | Move faster on this tile |
| Cracked | Breaks after 2 more swaps |
| Golden | Worth bonus points if survive on it |

---

## 💰 Monetization Ideas

- Character skins
- Tile themes
- Fall effects
- Victory dances
- Swap effects
- Power-up skins

---

## 🎯 Why This Could Work

1. ✅ **Unique mechanic** (ground shuffles)
2. ✅ **Controlled chaos** (structured randomness)
3. ✅ **Quick adaptation** (tests reactions)
4. ✅ **Fair RNG** (everyone equally affected)
5. ✅ **Fast rounds** (shrinking grid)
6. ✅ **Tense moments** (swap reveals)
7. ✅ **Combat + Chance** (balanced mix)
8. ✅ **Easy to understand** (don't fall off)
