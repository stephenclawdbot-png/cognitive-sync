# Dice of Death 🎲💀

**Status:** SAVED - High potential
**Theme:** RNG game selection + mini-game mastery
**Style:** Party game with rotating challenges

---

## 🎮 Core Concept

Giant dice rolls each round, determining the CHALLENGE everyone must face. Different numbers = different mini-games. Must be good at MULTIPLE skills to win. Can earn REROLLS to change unfavorable dice.

**The Twist:** You never know what's coming — adaptability is key.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                      DICE OF DEATH LOOP                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. DICE ROLL PHASE                                            │
│      → Giant dice appears in center                             │
│      → Dramatic roll animation                                  │
│      → All players watch nervously                              │
│      → Dice lands on NUMBER (1-6)                               │
│      → REROLL window (3 seconds)                                │
│                                                                 │
│   2. REROLL OPTION                                              │
│      → Players with reroll tokens can use them                  │
│      → First to use reroll = dice rolls again                   │
│      → Only 1 reroll per round max                              │
│      → Rerolls are earned (not bought)                          │
│                                                                 │
│   3. MINI-GAME PHASE                                            │
│      → Number determines the game                               │
│      → 1 = Race        4 = Push Battle                          │
│      → 2 = Memory      5 = Hot Potato                           │
│      → 3 = Dodge       6 = FREE (no elim)                       │
│      → Mini-game plays out (30-45 sec)                          │
│                                                                 │
│   4. ELIMINATION                                                │
│      → Losers of mini-game = ELIMINATED                         │
│      → Bottom 1-3 players out (depends on game)                 │
│      → Survivors continue                                       │
│                                                                 │
│   5. REPEAT                                                     │
│      → New dice roll                                            │
│      → New mini-game                                            │
│      → Until 1 player remains                                   │
│                                                                 │
│   6. VICTORY                                                    │
│      → Last player standing = WINNER                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎲 The Six Games

### 1️⃣ RACE - "Sprint for Survival"
```
TYPE: Racing / Platforming
TIME: 30 seconds

RULES:
- Obstacle course race
- First to finish = safe
- Last 2 players = eliminated

SKILLS NEEDED:
- Speed
- Platforming
- Route optimization

OBSTACLES:
- Jumps
- Moving platforms
- Pendulum swings
- Treadmills
```

### 2️⃣ MEMORY - "Simon Says"
```
TYPE: Memory pattern
TIME: 45 seconds

RULES:
- Platform lights up pattern
- Players repeat the pattern
- Wrong step = eliminated
- Pattern gets longer each "sub-round"

SKILLS NEEDED:
- Memory
- Focus
- Quick recall

PATTERN:
- Round 1: 3 tiles
- Round 2: 4 tiles
- Round 3: 5 tiles
- Continue until 1-2 players remain
```

### 3️⃣ DODGE - "Falling Fury"
```
TYPE: Dodging / Survival
TIME: 40 seconds

RULES:
- Objects fall from sky
- Shadows show where they'll land
- Get hit = eliminated
- Last survivors win

SKILLS NEEDED:
- Awareness
- Quick movement
- Prediction

FALLING OBJECTS:
- Anvils
- Bombs
- Giant fruit
- Meteorites
```

### 4️⃣ PUSH BATTLE - "King of the Hill"
```
TYPE: Combat / Platform control
TIME: 45 seconds

RULES:
- Small platform over void
- Push others off
- Last on platform = wins
- Can jump, dash, push

SKILLS NEEDED:
- Combat
- Positioning
- Timing

MECHANICS:
- Push attack
- Dodge roll
- Jump over sweeps
- Platform shrinks over time
```

### 5️⃣ HOT POTATO - "Bomb Tag"
```
TYPE: Tag / Chase
TIME: 30 seconds

RULES:
- One player has bomb
- Tag someone to pass it
- Bomb explodes when timer ends
- Bomb holder = eliminated
- Repeat until 2-3 players left

SKILLS NEEDED:
- Speed
- Awareness
- Evasion

MECHANICS:
- Sprint
- Juke moves
- Corner trapping
```

### 6️⃣ FREE - "Lucky Break"
```
TYPE: No challenge
TIME: 10 seconds

RULES:
- Nobody eliminated!
- Everyone survives this round
- Brief celebration
- RARE and exciting

REACTION:
- Players cheer
- Confetti falls
- Short break from tension
- About 16% chance (1 in 6)
```

---

## 🔄 Reroll System

### Earning Rerolls
| Action | Rerolls Earned |
|--------|----------------|
| Win a mini-game (1st place) | +1 reroll |
| Survive 3 rounds in a row | +1 reroll |
| Complete daily challenge | +1 reroll |
| Watch ad (optional) | +1 reroll |

### Using Rerolls
```
WHEN:
- After dice lands
- 3 second window
- First to use = reroll happens

STRATEGY:
- Bad at Memory? Reroll 2
- Bad at Push? Reroll 4
- Never reroll 6 (free pass!)

LIMITATION:
- Only 1 reroll per round total
- If someone else uses first, yours is saved
- Max 3 rerolls held at once
```

---

## 🏆 Elimination Rules

### Per-Game Eliminations
| Game | Players Eliminated |
|------|-------------------|
| Race | Last 2 (or last 25%) |
| Memory | Anyone who fails pattern |
| Dodge | Anyone hit |
| Push Battle | Anyone who falls |
| Hot Potato | Bomb holder(s) |
| Free | Nobody! |

### Minimum Players
```
8+ players: Full eliminations
4-7 players: Reduced eliminations
3 players: 1 eliminated per round
2 players: FINAL SHOWDOWN (always Push Battle)
```

---

## 🎯 Final Showdown

### When 2 Players Remain
```
FINAL DICE ROLL:
- Special "Final" dice
- Only shows: 1, 3, or 4
- No Free, no Memory, no Hot Potato
- Pure skill finale

FINAL GAMES:
1 = Head-to-head RACE
3 = Head-to-head DODGE (last hit wins)
4 = Head-to-head PUSH BATTLE

WINNER:
- Takes it all
- Victory celebration
- Top of podium
```

---

## 🎨 Visual Design

### The Dice
- GIANT 3D dice (car-sized)
- Dramatic roll physics
- Slow-motion landing
- Glow effect on result
- Number announcement

### Arena Hub
- Central waiting area
- Dice pedestal in middle
- Teleporters to mini-games
- Leaderboard display

### Mini-Game Arenas
- Each game has unique arena
- Teleport between rounds
- Consistent style but varied themes

---

## 🎮 Game Modes

### Classic (Above)
- 8-12 players
- Random dice each round
- Last standing wins

### Weighted Dice
- Vote before match
- More liked games appear more often
- Community choice

### No Rerolls
- Pure RNG
- No reroll tokens
- Accept your fate

### Practice Mode
- Choose specific mini-game
- No eliminations
- Learn and improve

### Team Dice
- 2 teams
- Both teams play same mini-game
- Losing team loses 1 player
- Team with last member wins

---

## 🧠 Strategic Depth

### Game Mastery
```
SPECIALIST:
- Master 1-2 games
- Hope dice lands favorable
- Use rerolls to avoid weaknesses

GENERALIST:
- Okay at everything
- No bad matchups
- Never need rerolls

REROLL HOARDER:
- Save rerolls
- Use late game when stakes high
- Control final rounds
```

### Reading Other Players
```
WATCH FOR:
- Who rerolls what?
- That reveals their weakness
- Target them in Push Battle
- They'll struggle in that game
```

---

## 💰 Monetization Ideas

- Character skins
- Dice skins (special effects)
- Mini-game emotes
- Victory celebrations
- Kill effects per game
- Trail effects

---

## ❓ Open Questions

1. **More than 6 games?** D10? D12?
2. **Custom games?** Community mini-games?
3. **Seasonal games?** Halloween, Christmas themed?
4. **Difficulty scaling?** Harder mini-games late game?
5. **Spectator mode?** Watch after elimination?

---

## 🎯 Why This Could Work

1. ✅ **Variety** (6+ different games)
2. ✅ **Never boring** (always different)
3. ✅ **RNG excitement** (dice drama)
4. ✅ **Skill expression** (master all games)
5. ✅ **Fair** (everyone faces same challenge)
6. ✅ **Party energy** (great with friends)
7. ✅ **Clip moments** (clutch plays, lucky rolls)
8. ✅ **Replayable** (random every time)
9. ✅ **Easy to update** (add new mini-games)
