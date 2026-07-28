# Clone Chaos 👥👥👥

**Status:** SAVED - High potential
**Theme:** Multiplying clones + confusion
**Style:** Real-time deception with escalating chaos

---

## 🎮 Core Concept

Players get CLONED every round. Your clone mimics your movements with a delay. Hunter must identify and kill REAL players among the growing crowd of clones. More rounds = more chaos.

**The Twist:** The arena gets MORE confusing over time, not less.

---

## 🔄 Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLONE CHAOS LOOP                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. ROUND START                                                │
│      → 8 players spawn in arena                                 │
│      → One random player becomes HUNTER                         │
│      → Hunter has RED outline (visible to all)                  │
│      → Clone count: 0 (just real players)                       │
│                                                                 │
│   2. CLONING WAVE (Every 15 seconds)                            │
│      → "CLONING IN 3... 2... 1..."                              │
│      → Every LIVING player gets duplicated                      │
│      → Clone spawns next to you                                 │
│      → Clone mimics your movement (3 sec delay)                 │
│      → Clones look IDENTICAL to real players                    │
│                                                                 │
│   3. HUNTER'S MISSION                                           │
│      → Hunter has 45 seconds total                              │
│      → Must identify and KILL real players                      │
│      → Attack a REAL player = they're eliminated                │
│      → Attack a CLONE = clone poofs, nothing happens            │
│      → Hunter has unlimited attacks                             │
│                                                                 │
│   4. SURVIVOR'S MISSION                                         │
│      → Stay alive until timer ends                              │
│      → Use clones as SHIELDS/DECOYS                             │
│      → Move unpredictably to confuse hunter                     │
│      → Blend in with your own clones                            │
│                                                                 │
│   5. ROUND END                                                  │
│      → Timer ends OR all real players eliminated                │
│      → Survivors get points                                     │
│      → Hunter gets points per kill                              │
│      → New hunter selected, clones reset                        │
│      → After 5 rounds, most points wins                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📈 Escalation Timeline

| Time | Event | Arena State |
|------|-------|-------------|
| 0:00 | Round starts | 8 real players |
| 0:15 | Clone Wave 1 | 8 real + 8 clones = 16 total |
| 0:30 | Clone Wave 2 | 8 real + 16 clones = 24 total |
| 0:45 | Round ends | Maximum chaos! |

### Clone Math Example
```
Start: 8 players, 0 clones

After Wave 1:
- 8 players × 1 clone each = 8 clones
- Total entities: 16

If 2 players died before Wave 2:
- 6 remaining players × 1 new clone = 6 more clones
- Previous clones still exist: 8
- Total: 6 real + 14 clones = 20 entities

CHAOS ESCALATES!
```

---

## 🤖 Clone Behavior

### Movement Mimic
```
REAL PLAYER ACTION        →    CLONE COPIES (3 sec delay)
─────────────────────────────────────────────────────────
Player walks left         →    Clone walks left (3 sec later)
Player jumps              →    Clone jumps (3 sec later)
Player stops              →    Clone stops (3 sec later)
Player changes direction  →    Clone changes direction (3 sec later)
```

### Clone Properties
| Property | Real Player | Clone |
|----------|-------------|-------|
| Appearance | Normal | Identical |
| Movement | Player control | Mimics player (delayed) |
| Can be killed | Yes (eliminated) | Yes (poofs, respawns) |
| Collision | Solid | Solid |
| Name tag | Shown | Shown (same name!) |

### Clone Death & Respawn
- Killed clone = POOFS into smoke
- Clone respawns near its real player after 5 seconds
- Clones never permanently die

---

## 🎯 Hunter Mechanics

### Attack
- Click to SLASH (melee range)
- Fast attack speed
- No cooldown
- Must be close to target

### Identifying Real Players
**TELLS to look for:**
```
❌ Clones have 3 sec delay (watch for "original" mover)
❌ Clones can't react to hunter (no fear response)
❌ Real players might panic when hunter approaches
❌ Clone paths are predictable (following past movement)
❌ Multiple clones follow same player = find the leader
```

### Hunter Strategy
- Watch for the FIRST mover in a group
- Cause chaos, see who reacts naturally
- Target isolated players (fewer clones to confuse)
- Quick decisive strikes when confident

---

## 🏃 Survivor Strategies

### Beginner: Blend In
- Move smoothly, no sudden changes
- Let your clones catch up to you
- Stay in crowds of clones

### Intermediate: Clone Shield
- Keep clones between you and hunter
- Use clones as body blockers
- Sacrifice clones to escape

### Advanced: Misdirection
- Move toward hunter, then reverse (clone goes toward hunter while you escape)
- Create complex movement patterns
- "Park" in a spot, let clones stack on you, then slip away

### Pro: Prediction
- Watch hunter's attention
- When hunter targets someone else, reposition
- Use other players' chases as cover

---

## 🗺️ Map Design

### Key Requirements
- Medium size (not too big or finding people is impossible)
- Some obstacles (break line of sight)
- Open areas (clones can gather)
- No hiding spots (clones can't follow into tight spaces = tells)

### Map Ideas

**"Clone Lab"**
- Sci-fi laboratory aesthetic
- Glass walls (see through but can't pass)
- Clone tubes decoration
- Conveyor belts (forced movement)

**"Mirror Maze"**
- Hall of mirrors theme
- Reflective surfaces (visual confusion)
- Symmetrical layout
- Dead ends for trapping

**"City Streets"**
- Urban environment
- Cars/benches as obstacles
- Alleyways for clone chains
- Open plaza centers

---

## 🎨 Visual Design

### Player Appearance
- Everyone looks identical (same model)
- Customizable colors (but all clones match their player)
- Hunter has red glow/outline

### Clone Effects
- Spawn: Flash of light, duplicate appears
- Death: Poof into smoke/particles
- Moving: Slight ghost trail?

### Clone Wave
- Screen flash warning
- "CLONING!" text
- All clones spawn simultaneously
- Dramatic sound effect

---

## 🎮 Game Modes

### Classic (Described above)
- 1 hunter, 7 survivors
- 45 second rounds
- Clone wave every 15 sec

### Infection Clone
- Killed players become hunters too
- Their clones also become hunter clones
- Last survivor wins

### Clone Limit
- Max 3 clones per player
- Oldest clone disappears when new one spawns
- More strategic clone management

### No Clone Zone
- Certain areas don't allow clones
- Standing there = definitely real
- But exposed and dangerous

---

## 💰 Monetization Ideas

- Character skins (cosmetic, clones copy skin)
- Clone spawn effects
- Death effects
- Hunter weapon skins
- Victory animations
- Clone trail effects

---

## ❓ Open Questions

1. **Clone delay?** 3 sec? 2 sec? 5 sec?
2. **Max clones?** Unlimited or capped?
3. **Clone AI?** Pure mimic or slight randomness?
4. **Hunter cooldown?** Any penalty for wrong kills?
5. **Multiple hunters?** For larger lobbies?

---

## 🎯 Why This Could Work

1. ✅ **Unique mechanic** (escalating clone army)
2. ✅ **Visual chaos** (gets crazier each wave)
3. ✅ **Skill expression** (movement patterns, misdirection)
4. ✅ **Easy to understand** ("don't get caught, use clones")
5. ✅ **Streamable** (fun to watch, guess who's real)
6. ✅ **Fast rounds** (45 sec)
7. ✅ **Replayable** (different strategies each time)
8. ✅ **Scales well** (more players = more chaos)
