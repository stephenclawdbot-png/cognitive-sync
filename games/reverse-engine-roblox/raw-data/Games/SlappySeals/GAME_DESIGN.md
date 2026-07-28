# 🦭 SLAPPY SEALS - Complete Game Design Document

> **Tagline:** Slap. Survive. Be the Last Seal Standing.

---

## 📋 TABLE OF CONTENTS

1. [Core Concept](#-core-concept)
2. [Game Flow & States](#-game-flow--states)
3. [Auto-Queue System](#-auto-queue-system)
4. [Lobby System](#-lobby-system)
5. [Battle System](#-battle-system)
6. [Platform Shrinking](#-platform-shrinking)
7. [Shark System](#-shark-system)
8. [Slap Mechanics](#-slap-mechanics)
9. [Elimination & Win](#-elimination--win)
10. [UI Requirements](#-ui-requirements)
11. [Technical Configuration](#-technical-configuration)
12. [Scripts Overview](#-scripts-overview)

---

## 🎯 CORE CONCEPT

**Formula:** Slap Battles + Knockout! + Shark Survival

- 4-16 seals on a shrinking ice platform
- Slap other players to fling them off
- Ragdoll on impact (vulnerable window)
- Sharks spawn as hazards when <7 players remain
- Last seal standing wins

**Core Elements:**
| Element | Description |
|---------|-------------|
| PvP | Slap other seals to knock them off |
| PvE | Survive shark attacks from below |
| Shrinking | Ice platform shrinks every 12 seconds |
| Simple | One button to slap, WASD to move |

---

## 🔄 GAME FLOW & STATES

### State Machine

```
┌─────────────────────────────────────────────────────────────────┐
│                     SLAPPY SEALS GAME STATES                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐    enough players    ┌───────────┐              │
│   │ WAITING  │ ──────────────────→  │ COUNTDOWN │              │
│   │          │ ←──────────────────  │  (20 sec) │              │
│   └──────────┘   not enough players └─────┬─────┘              │
│        ↑                                  │                    │
│        │                          countdown ends               │
│        │                                  ↓                    │
│        │                          ┌─────────────┐              │
│        │                          │ IN_PROGRESS │              │
│        │                          │   (game)    │              │
│        │                          └──────┬──────┘              │
│        │                                 │                     │
│        │                          1 player left                │
│        │                                 ↓                     │
│        │                          ┌──────────┐                 │
│        └────────────────────────  │  ENDING  │                 │
│              after winner card    │ (results)│                 │
│                                   └──────────┘                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### State Descriptions

| State | Description | Duration |
|-------|-------------|----------|
| **WAITING** | Waiting for minimum players (4). No countdown. New players auto-queue. | Until 4+ queued |
| **COUNTDOWN** | Countdown to game start. Players see "Game starting in X..." | 20 seconds |
| **IN_PROGRESS** | Active game. Platform shrinks. Sharks spawn. Players fight. | Until 1 left |
| **ENDING** | Show winner/eliminated cards. Teleport everyone to lobby. | ~5 seconds |

---

## 🎮 AUTO-QUEUE SYSTEM

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      AUTO-QUEUE FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Player Joins Server                                           │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────────┐                                          │
│   │ AUTO-ADDED TO    │ ← Default state for all new players     │
│   │ QUEUE            │                                          │
│   └────────┬─────────┘                                          │
│            │                                                    │
│            ▼                                                    │
│   ┌──────────────────┐     Click AFK      ┌──────────────────┐ │
│   │   IN QUEUE       │ ←───────────────→  │   AFK (Opt-out)  │ │
│   │ (will join game) │    Click AFK       │ (won't join)     │ │
│   └──────────────────┘                    └──────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Queue Rules

| Rule | Description |
|------|-------------|
| **Auto-Queue** | Players automatically queued when joining server |
| **AFK Toggle** | Single button to toggle AFK on/off |
| **AFK = Opt-out** | AFK players excluded from next game |
| **Mid-Game Join** | New players wait in lobby until current game ends |
| **No Countdown During Game** | Countdown ONLY starts after game ends |

### Player States

```lua
PlayerData = {
    isAFK = false,      -- true = opted out of queue
    isInGame = false,   -- true = currently in battle
}

-- Queue = players where isAFK == false AND isInGame == false
```

---

## 🏠 LOBBY SYSTEM

### Lobby Spawn (No Stacking!)

When players spawn in lobby, they must NOT stack on top of each other.

**Spread Algorithm:**
```
┌─────────────────────────────────────────────────────────────────┐
│                     LOBBY SPAWN SPREAD                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    Lobby Center (SpawnLocation)                 │
│                              ●                                  │
│                                                                 │
│              🦭          🦭          🦭                          │
│                    4 players: square pattern                    │
│              🦭                      🦭                          │
│                                                                 │
│        🦭      🦭      🦭      🦭      🦭      🦭                │
│              8 players: circle pattern                          │
│        🦭      🦭      🦭      🦭      🦭      🦭                │
│                                                                 │
│   • Each player gets unique position                            │
│   • Golden angle distribution for even spread                   │
│   • Radius: 25 studs from center                                │
│   • Players face toward center                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Spread Position Calculation:**
```lua
-- Golden angle for even distribution
local goldenAngle = math.pi * (3 - math.sqrt(5))  -- ~137.5°

function GetSpreadPosition(center, radius, playerIndex, totalPlayers)
    local angle = playerIndex * goldenAngle
    local distance = radius * (0.3 + 0.7 * math.sqrt(playerIndex / totalPlayers))
    
    return Vector3.new(
        center.X + math.cos(angle) * distance,
        center.Y + 3,  -- Height offset
        center.Z + math.sin(angle) * distance
    )
end
```

### Lobby Behavior

| Scenario | Behavior |
|----------|----------|
| Player joins, no game active | Spawn in lobby, add to queue |
| Player joins, game in progress | Spawn in lobby, wait for game to end |
| Player eliminated | Teleport to lobby, re-add to queue |
| Winner after game | Teleport to lobby, re-add to queue |
| Game ends | 20 second countdown starts |

---

## ⚔️ BATTLE SYSTEM

### Battle Platform Spawn (No Stacking!)

When game starts, teleport queued players to battle platform - spread out!

**Battle Spawn Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│                   BATTLE PLATFORM SPAWN                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     Platform Center                             │
│                          ●                                      │
│                                                                 │
│               🦭                    🦭                           │
│                                                                 │
│         🦭                                🦭                     │
│                                                                 │
│     🦭              (center)                  🦭                 │
│                                                                 │
│         🦭                                🦭                     │
│                                                                 │
│               🦭                    🦭                           │
│                                                                 │
│   • Players spawn on OUTER EDGE of platform                     │
│   • Facing toward center                                        │
│   • Radius: 35 studs from center                                │
│   • Equal spacing around circle                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Battle Start Sequence

```
1. Countdown reaches 0
2. State → IN_PROGRESS
3. Get all queued players (non-AFK)
4. Mark players as isInGame = true
5. Teleport all to battle platform (spread)
6. Reset platform to full size
7. Enable slapping
8. Start shrink timer (12 second loop)
9. Start game loop (check win condition)
```

---

## 🧊 PLATFORM SHRINKING

### Shrink Timer (ALWAYS VISIBLE)

**UI Requirement:** Timer showing "Platform shrinks in: X" must be visible at ALL times during gameplay.

```
┌─────────────────────────────────────────────────────────────────┐
│                     SHRINK TIMER UI                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────┐                       │
│   │  ⚠️ Platform shrinks in: 8         │  ← Always visible     │
│   └─────────────────────────────────────┘                       │
│                                                                 │
│   Position: Top center of screen                                │
│   Updates: Every 0.1 seconds (smooth countdown)                 │
│   Color: Yellow/Orange when < 5 seconds                         │
│   Effect: Pulse/flash when < 3 seconds                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Shrink Configuration

| Setting | Value |
|---------|-------|
| **Shrink Interval** | 12 seconds |
| **Shrink Amount** | 18% smaller each time (multiply by 0.82) |
| **Shrink Animation** | 1.5 second tween |
| **Minimum Size** | 15 studs radius |
| **Warning** | Visual/audio at 3 seconds before |

### Shrink Timeline Example

```
0:00  - Game starts, full platform (50 stud radius)
0:12  - SHRINK #1 → 41 studs
0:24  - SHRINK #2 → 34 studs
0:36  - SHRINK #3 → 28 studs
0:48  - SHRINK #4 → 23 studs
1:00  - SHRINK #5 → 19 studs
1:12  - SHRINK #6 → 15 studs (minimum)
1:24+ - Platform stays at minimum
```

### Shrink Visuals

```
BEFORE SHRINK (3 sec warning):
• Timer turns red
• Cracks appear on outer edge
• Warning sound plays
• "Ice cracking!" notification

DURING SHRINK:
• Outer ring falls/crumbles
• Splash effects at edges
• Camera shake (subtle)
• Players on edge fall off = eliminated

AFTER SHRINK:
• New edge clearly visible
• Less space for players
• Timer resets to 12
```

---

## 🦈 SHARK SYSTEM

### Spawn Condition

**Sharks appear when: Active players < 7**

```
Players Remaining    Sharks
──────────────────────────────
7+                   ❌ No sharks
6                    ✅ Sharks spawn (slow)
5                    ✅ More frequent
4                    ✅ Even more frequent  
3                    ✅ Chaos mode
2                    ✅ Maximum chaos
1                    Game over (winner)
```

### Shark Escalation Table

| Players Left | Spawn Interval | Shark Size |
|--------------|----------------|------------|
| 6 | 4.0 seconds | Small |
| 5 | 3.0 seconds | Medium |
| 4 | 2.5 seconds | Medium |
| 3 | 2.0 seconds | Large |
| 2 | 1.5 seconds | Large |

### Shark Attack Sequence

```
┌─────────────────────────────────────────────────────────────────┐
│                     SHARK ATTACK SEQUENCE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. SHADOW APPEARS (1.8 sec warning)                           │
│      • Dark circle on platform                                  │
│      • Grows larger over time                                   │
│      • Players should MOVE!                                     │
│                                                                 │
│   2. SHARK ATTACKS                                              │
│      • Shark bursts up through platform                         │
│      • Anyone in radius gets FLUNG                              │
│      • Upward + outward momentum                                │
│      • Can knock players off edge                               │
│                                                                 │
│   3. SHARK RETREATS                                             │
│      • Falls back into water                                    │
│      • Shadow disappears                                        │
│      • Next shark spawns after interval                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Shark Visual Reference

```
PLATFORM VIEW (shadow appearing):

        🦭        🦭
              ⚫ ← Dark shadow growing!
    🦭              🦭
          🦭

PLATFORM VIEW (shark attacks):

        🦭        🦭
              🦈💥 CHOMP!
    🦭    (player flung!) 🦭
          🦭
```

---

## 👋 SLAP MECHANICS

### Slap Stats

| Stat | Value |
|------|-------|
| **Range** | 6 studs |
| **Angle** | 90° cone in front |
| **Fling Power** | 55 studs/sec |
| **Cooldown** | 0.8 seconds |
| **Ragdoll Duration** | 0.6 seconds |

### Slap Flow

```
SLAPPER (Attacker):
1. Player clicks/taps SLAP
2. Check cooldown (0.8s)
3. Check for targets in range + cone
4. If hit: Apply fling to closest target
5. Play slap animation
6. Camera shake (satisfaction)
7. Start cooldown

VICTIM (Target):
1. Get hit by slap
2. Fling applied (direction: away from slapper)
3. RAGDOLL activates (0.6s)
4. No control during ragdoll!
5. Can be combo'd while ragdolled
6. Ragdoll ends, regain control
7. If flung off platform → ELIMINATED
```

### Ragdoll Importance

```
WHY RAGDOLL?
• Creates vulnerable window
• Allows combo attacks
• Satisfying visual feedback
• Skill expression (timing)
• Funny physics moments

RAGDOLL RULES:
• Duration: 0.6 seconds
• Player has NO CONTROL
• Can receive additional slaps
• Momentum carries through
• Ends automatically
```

---

## 💀 ELIMINATION & WIN

### Elimination Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     ELIMINATION FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Player falls off platform                                     │
│           │                                                     │
│           ▼                                                     │
│   ┌───────────────────┐                                         │
│   │ Remove from       │                                         │
│   │ ActivePlayers     │                                         │
│   └─────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│   ┌───────────────────┐                                         │
│   │ Show ELIMINATED   │  "You've been eliminated!"              │
│   │ Card (2 sec)      │                                         │
│   └─────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│   ┌───────────────────┐                                         │
│   │ Teleport to Lobby │  Spread position, not stacked           │
│   └─────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│   ┌───────────────────┐                                         │
│   │ Wait for next     │  isInGame = false                       │
│   │ game              │  Back in queue (unless AFK)             │
│   └───────────────────┘                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Win Condition

**Game ends when: ActivePlayers ≤ 1**

### Winner Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                       WINNER FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Only 1 player remains                                         │
│           │                                                     │
│           ▼                                                     │
│   ┌───────────────────┐                                         │
│   │ State → ENDING    │                                         │
│   └─────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│   ┌───────────────────┐                                         │
│   │ Stop shrinking    │  Platform stops, sharks disabled        │
│   │ Stop sharks       │                                         │
│   └─────────┬─────────┘                                         │
│             │                                                   │
│             ├────────────────────────────┐                      │
│             │                            │                      │
│             ▼                            ▼                      │
│   ┌─────────────────┐          ┌─────────────────┐              │
│   │ WINNER sees:    │          │ ELIMINATED see: │              │
│   │ "🏆 WINNER!"    │          │ "Winner: Name"  │              │
│   │ (3 sec)         │          │ (3 sec)         │              │
│   └────────┬────────┘          └────────┬────────┘              │
│            │                            │                       │
│            └─────────────┬──────────────┘                       │
│                          │                                      │
│                          ▼                                      │
│            ┌─────────────────────────┐                          │
│            │ Teleport winner to      │                          │
│            │ lobby (spread position) │                          │
│            └───────────┬─────────────┘                          │
│                        │                                        │
│                        ▼                                        │
│            ┌─────────────────────────┐                          │
│            │ Reset platform          │                          │
│            └───────────┬─────────────┘                          │
│                        │                                        │
│                        ▼                                        │
│            ┌─────────────────────────┐                          │
│            │ State → WAITING or      │  Check player count      │
│            │ State → COUNTDOWN       │  If 4+ → start countdown │
│            └─────────────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Result Cards

**Winner Card (shown to winner):**
```
┌─────────────────────────────┐
│                             │
│       🏆 WINNER! 🏆         │
│                             │
│      You are the last       │
│      seal standing!         │
│                             │
│        +50 🐟 Fish          │
│                             │
└─────────────────────────────┘
```

**Eliminated Card (shown when eliminated):**
```
┌─────────────────────────────┐
│                             │
│      ❌ ELIMINATED          │
│                             │
│   Better luck next time!    │
│                             │
│    Returning to lobby...    │
│                             │
└─────────────────────────────┘
```

**Announcement Card (shown to lobby/eliminated when game ends):**
```
┌─────────────────────────────┐
│                             │
│       🎉 GAME OVER 🎉       │
│                             │
│    Winner: PlayerName       │
│                             │
│   Next game starting soon   │
│                             │
└─────────────────────────────┘
```

---

## 🖥️ UI REQUIREMENTS

### Required UI Elements

| Element | Location | When Visible |
|---------|----------|--------------|
| **AFK Button** | Bottom/corner | Always in lobby |
| **Queue Status** | Top corner | Always |
| **Player Count** | Top corner | Always |
| **Countdown** | Center | During COUNTDOWN state |
| **Shrink Timer** | Top center | During IN_PROGRESS |
| **Result Card** | Center | When eliminated/won |
| **Slap Cooldown** | Near slap button | During game |

### Shrink Timer UI (Placeholder Integration)

```
YOUR EXISTING PLACEHOLDER:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   The placeholder UI you created should display:                │
│                                                                 │
│   ┌─────────────────────────────────────┐                       │
│   │  ⚠️ Platform shrinks in: 12        │                       │
│   └─────────────────────────────────────┘                       │
│                                                                 │
│   RemoteEvent: "ShrinkTimerUpdate"                              │
│   Fires: (timeRemaining, totalTime)                             │
│   Update rate: 0.1 seconds                                      │
│                                                                 │
│   Client code:                                                  │
│   Events.ShrinkTimerUpdate.OnClientEvent:Connect(function(t)    │
│       ShrinkTimerLabel.Text = "Platform shrinks in: " .. t      │
│   end)                                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ TECHNICAL CONFIGURATION

### Game Settings

```lua
Config = {
    -- Players
    MIN_PLAYERS = 4,              -- Minimum to start (test mode)
    MAX_PLAYERS = 16,             -- Server limit
    LOBBY_COUNTDOWN = 20,         -- Seconds before game starts
    
    -- Platform
    PLATFORM_SHRINK_INTERVAL = 12,  -- Seconds between shrinks
    PLATFORM_SHRINK_AMOUNT = 0.82,  -- Size multiplier per shrink
    PLATFORM_MIN_SIZE = 15,         -- Minimum radius
    
    -- Sharks
    SHARK_THRESHOLD = 7,          -- Sharks spawn when players < this
    SHARK_WARNING_TIME = 1.8,     -- Shadow visible before attack
    SHARK_FLING_POWER = 80,       -- How hard sharks fling
    
    -- Slap
    SLAP_RANGE = 6,               -- Studs
    SLAP_FLING_POWER = 55,        -- Studs/sec
    SLAP_COOLDOWN = 0.8,          -- Seconds
    RAGDOLL_DURATION = 0.6,       -- Seconds
    
    -- Spawning
    LOBBY_SPAWN_RADIUS = 25,      -- Spread radius in lobby
    BATTLE_SPAWN_RADIUS = 35,     -- Spread radius on platform
    
    -- Timing
    WINNER_CARD_DURATION = 3,     -- Seconds
    ELIMINATED_CARD_DURATION = 2, -- Seconds
    FALL_DETECTION_Y = -20,       -- Y position = fallen
}
```

### Workspace Requirements

```
workspace/
├── LobbySpawn          -- Part marking lobby center
├── BattlePlatform      -- The shrinking platform part
│   └── (or "IcePlatform" or "Platform")
└── BattleSpawn         -- Part marking platform center (optional, uses platform center)
```

### RemoteEvents (SlappyEvents folder)

```
ReplicatedStorage/
└── SlappyEvents/
    ├── GameStateChanged     -- (newState, oldState)
    ├── CountdownUpdate      -- (seconds, message)
    ├── ShowResultCard       -- (type, winnerName)
    ├── ShrinkTimerUpdate    -- (timeRemaining, totalTime)
    ├── PlatformShrink       -- (newSize, duration, shrinkCount)
    ├── PlatformWarning      -- (type, countdown)
    ├── AFKToggle            -- Client → Server (toggle)
    ├── AFKStatusUpdate      -- Server → Client (isAFK)
    ├── QueueUpdate          -- (queueData)
    ├── SharkWarning         -- (position, size, duration)
    ├── SharkAttack          -- (position, size)
    ├── SlapRequest          -- Client → Server (slap input)
    ├── SlapHit              -- (targetName, hitType)
    ├── SlapCooldown         -- (cooldownTime)
    └── RagdollEvent         -- (enable, duration)
```

---

## 📁 SCRIPTS OVERVIEW

### Server Scripts (ServerScriptService/SlappySeals/)

| Script | Purpose |
|--------|---------|
| **MainInit.lua** | Initializes all modules, connects references |
| **GameManager.lua** | State machine, game flow, win conditions |
| **PlayerManager.lua** | Queue, AFK, spawn spreading, teleportation |
| **PlatformManager.lua** | Shrinking, timer, fall detection |
| **SharkManager.lua** | Shark spawning, escalation, attacks |
| **SlapManager.lua** | Slap detection, fling, ragdoll |

### Client Scripts (StarterPlayerScripts/SlappySeals/)

| Script | Purpose |
|--------|---------|
| **ClientMain.lua** | Initializes client modules |
| **UIController.lua** | All UI updates (timer, cards, buttons) |
| **SlapController.lua** | Input handling, slap requests |
| **RagdollController.lua** | Client-side ragdoll physics |
| **EffectsController.lua** | VFX, camera shake, sounds |

---

## 🔄 COMPLETE GAME FLOW SUMMARY

```
┌─────────────────────────────────────────────────────────────────┐
│                  COMPLETE GAME FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PLAYER JOINS SERVER                                         │
│     → Spawn in lobby (spread position)                          │
│     → Auto-added to queue                                       │
│     → Can click AFK to opt-out                                  │
│                                                                 │
│  2. WAITING FOR PLAYERS                                         │
│     → Need 4+ queued players                                    │
│     → No countdown during active game                           │
│     → UI shows "Waiting for players... (X/4)"                   │
│                                                                 │
│  3. COUNTDOWN (20 seconds)                                      │
│     → Starts when 4+ players queued AND no game active          │
│     → UI shows "Game starting in: X"                            │
│     → Cancelled if players drop below 4                         │
│                                                                 │
│  4. GAME STARTS                                                 │
│     → Teleport queued players to platform (spread)              │
│     → Enable slapping                                           │
│     → Start shrink timer (12 seconds)                           │
│     → UI shows shrink countdown (ALWAYS VISIBLE)                │
│                                                                 │
│  5. DURING GAME                                                 │
│     → Players slap each other                                   │
│     → Platform shrinks every 12 seconds                         │
│     → Sharks spawn when <7 players remain                       │
│     → Eliminated players → show card → lobby                    │
│                                                                 │
│  6. GAME ENDS (1 player left)                                   │
│     → Stop shrinking, disable sharks                            │
│     → Winner sees victory card (3 sec)                          │
│     → Others see announcement card                              │
│     → Winner teleports to lobby                                 │
│                                                                 │
│  7. NEXT GAME                                                   │
│     → Platform resets to full size                              │
│     → Check player count                                        │
│     → If 4+ queued → start 20 sec countdown                     │
│     → Loop back to step 3                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 QUICK REFERENCE

| Feature | Value |
|---------|-------|
| Min Players | 4 (test) |
| Countdown | 20 seconds |
| Shrink Interval | 12 seconds |
| Shark Threshold | <7 players |
| Slap Cooldown | 0.8 seconds |
| Ragdoll Duration | 0.6 seconds |
| Lobby Spawn Radius | 25 studs |
| Battle Spawn Radius | 35 studs |

---

*Document Version: 2.0*
*Created: 2026-02-06*
*By: Admiral + Max*
