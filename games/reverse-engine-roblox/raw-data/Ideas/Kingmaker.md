# Kingmaker 👑⚔️

**Status:** SAVED - High potential
**Theme:** Power struggle + betrayal
**Style:** Real-time asymmetric combat with hot seat pressure

---

## 🎮 Core Concept

One player is the KING with a powerful weapon. King can one-shot anyone. BUT King has a BOUNTY TIMER — if it expires, King dies. Only way to reset timer? Get a kill. Whoever kills the King becomes the new King.

**The Twist:** Being King is a CURSE disguised as power. Everyone wants you dead.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                      KINGMAKER LOOP                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → All players spawn in arena                               │
│      → Crown spawns in CENTER                                   │
│      → First to grab crown = becomes KING                       │
│      → King gets: Royal Sword (one-hit kill)                    │
│      → King's bounty timer starts: 20 SECONDS                   │
│                                                                 │
│   2. KING'S DILEMMA                                             │
│      → Timer counting down (visible to all)                     │
│      → Must KILL someone before timer hits 0                    │
│      → Each kill = timer RESETS to 15 seconds                   │
│      → Timer never goes above 20 sec (no stacking)              │
│                                                                 │
│   3. PEASANT'S CHOICE                                           │
│      → Non-kings are PEASANTS (no weapon)                       │
│      → Can RUN and SURVIVE (avoid king)                         │
│      → OR try to KILL the king (risky but rewarding)            │
│      → Peasants can punch (weak, but 5 punches = kill king)     │
│      → Kill king = YOU become king (with fresh 20 sec timer)    │
│                                                                 │
│   4. KING DEATH                                                 │
│      → Timer expires = King DIES (crown drops)                  │
│      → Killed by peasant = that peasant becomes King            │
│      → Crown on ground = anyone can grab it                     │
│                                                                 │
│   5. WIN CONDITION                                              │
│      → Last player alive = WINS                                 │
│      → OR most "King Time" after 3 minutes                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👑 King Mechanics

### Royal Sword
| Property | Value |
|----------|-------|
| Damage | ONE-HIT KILL |
| Range | Melee (medium) |
| Speed | Normal swing |
| Cooldown | 0.5 seconds |

### Bounty Timer
```
INITIAL TIMER: 20 seconds

KILL SOMEONE:
→ Timer resets to 15 seconds
→ Extends your reign
→ But now everyone knows you're dangerous

TIMER HITS 0:
→ You DIE instantly
→ Crown drops on ground
→ Free-for-all to grab it
```

### King Appearance
- Golden crown above head
- Royal cape (flowing)
- Glowing sword
- Timer visible above (red when low)
- Everyone can see king's timer

### King Strategy
```
AGGRESSIVE KING:
- Hunt peasants actively
- Keep timer healthy
- Risk: everyone focuses you

DEFENSIVE KING:
- Kill only when timer low
- Conserve energy
- Risk: peasants gang up, 5 punches = dead

BAITING KING:
- Let peasants approach
- Punish greedy attackers
- Risk: getting surrounded
```

---

## 🧑‍🌾 Peasant Mechanics

### Punch Attack
| Property | Value |
|----------|-------|
| Damage | 1 HP (King has 5 HP) |
| Range | Short melee |
| Speed | Fast |
| Cooldown | 0.3 seconds |

### Peasant Strategy
```
SURVIVOR:
- Run from king
- Let others fight
- Win by being last alive

ASSASSIN:
- Team up with other peasants
- 5 punches together = dead king
- Risk: king might kill you first

OPPORTUNIST:
- Wait for king's timer to get low
- Strike when king is desperate
- Steal the crown at last second

VULTURE:
- Let others weaken king
- Swoop in for killing blow
- Become king with fresh timer
```

---

## ⚔️ Combat Scenarios

### King vs 1 Peasant
```
King advantage: One-hit kill
Peasant advantage: Mobility, patience

King should: Chase and kill quickly
Peasant should: Kite, wait for help
```

### King vs 2+ Peasants
```
King problem: Can only kill one at a time
Peasant advantage: Gang up, 5 punches = dead

King should: Pick off isolated targets, don't get surrounded
Peasants should: Coordinate attack, sacrifice one to land hits
```

### Low Timer King
```
KING (5 seconds left):
- Desperate, will chase anyone
- Might make mistakes
- Must kill NOW

PEASANTS:
- Stay away, let timer expire
- OR risk attacking (might get killed)
- Mind game: who gets the crown after?
```

---

## 🔄 Crown Transitions

### Timer Death
```
King's timer → 0
King dies (dramatic death animation)
Crown DROPS on ground
5 second delay before pickup
All peasants race for crown
First touch = new King (20 sec timer)
```

### Assassination
```
Peasant lands killing blow
King dies
Crown TRANSFERS directly to killer
New King (20 sec timer)
Brief invincibility (2 sec) to escape swarm
```

### King Falls Off Map
```
King dies
Crown respawns in CENTER
Race to center
First touch = new King
```

---

## 🗺️ Map Design

### Key Elements
- Open center (crown spawns, king fights)
- Escape routes (peasants can flee)
- No true hiding spots (king must find victims)
- Environmental hazards? (pits, spikes)

### Map Ideas

**"Throne Room"**
- Medieval castle interior
- Central throne (crown spawn)
- Pillars for cover
- Balcony overlooking

**"Colosseum"**
- Roman arena
- Spectator stands (can climb)
- Sand floor
- Gates that open/close

**"Pirate Ship"**
- Deck of ship
- Masts to climb
- Plank to push people off
- Cannons as obstacles

---

## 📊 Scoring System

### Points Earned
| Action | Points |
|--------|--------|
| Kill as King | +50 |
| Kill the King | +100 |
| Survive a round | +25 |
| Each second as King | +2 |
| Win the game | +200 |

### Win Conditions

**Option A: Last Standing**
- Play until 1 player left
- Pure elimination

**Option B: Timed Mode**
- 3 minute match
- Most points wins
- King time matters most

**Option C: Kill Target**
- First to 5 kills wins
- King kills count double

---

## 🎮 Game Modes

### Classic Kingmaker
- Described above
- 8 players, last standing

### Team Kingmaker
- 2 teams
- Only enemy team can become king
- Protect your king, assassinate theirs

### Double Crown
- TWO kings at once
- Kings can't hurt each other
- More chaos, more kills needed

### Peasant Uprising
- Peasants respawn after 10 sec
- King must survive 2 minutes
- King vs endless peasants

### Shrinking Throne
- Arena shrinks over time
- Harder to escape king
- Faster games

---

## 🧠 Strategic Depth

### Early Game
- Race for crown (do you want it?)
- Being first king = risky (everyone attacks)
- Let someone else take it first?

### Mid Game
- King established, hunting
- Peasants deciding: run or fight?
- Alliances form and break

### Late Game
- Few players left
- King's kills are easier (fewer targets)
- But timer pressure is constant
- Final showdowns

### Mind Games
```
"Do I want to be king?"
- Power is tempting
- But everyone hunts you
- Timer is stressful

"Who should I help?"
- Help someone kill king?
- But they become king...
- Temporary alliances only
```

---

## 🎨 Visual Design

### King
- Golden crown (glowing)
- Royal cape (red velvet)
- Sword with particle effects
- Timer displayed prominently

### Peasants
- Simple clothes
- No weapons (fists only)
- Scared expressions
- Ragged appearance

### Crown Drop
- Slow-motion crown falling
- Light beam from crown
- Sound cue when dropped

### Throne Effects
- Kill = blood splatter (kid-friendly version: confetti?)
- Timer warning = screen pulse red
- Crown pickup = royal fanfare

---

## 💰 Monetization Ideas

- King skins (different crowns, capes)
- Peasant skins
- Sword skins
- Kill effects
- Crown drop effects
- Victory thrones

---

## ❓ Open Questions

1. **King HP?** 5 punches or less/more?
2. **Timer values?** 20/15 or different?
3. **Respawn?** Peasants respawn or one life?
4. **Crown grab delay?** Instant or waiting period?
5. **Theme?** Medieval? Modern? Brainrot reskin?

---

## 🎯 Why This Could Work

1. ✅ **Power fantasy** (being king feels good)
2. ✅ **But balanced** (king is hunted, timer pressure)
3. ✅ **Asymmetric gameplay** (king vs peasants)
4. ✅ **Betrayal moments** (alliances break)
5. ✅ **Fast transitions** (king changes frequently)
6. ✅ **Multiple strategies** (run, fight, survive)
7. ✅ **Easy to understand** (king kills, peasants survive)
8. ✅ **Dramatic moments** (clutch kills, crown steals)
