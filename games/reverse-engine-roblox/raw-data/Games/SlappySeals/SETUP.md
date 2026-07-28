# 🦭 SLAPPY SEALS - Setup Guide

## 📁 Files Created

```
I:\Reverse Engine Roblox\Games\SlappySeals\
├── GAME_DESIGN.md              # Full game design document
├── SETUP.md                    # This file
│
├── ServerScriptService/        # Copy contents to ServerScriptService
│   ├── MainInit.lua            # Main script (Script, not ModuleScript)
│   ├── GameManager.lua         # ModuleScript
│   ├── PlayerManager.lua       # ModuleScript
│   ├── PlatformManager.lua     # ModuleScript
│   ├── SharkManager.lua        # ModuleScript
│   └── SlapManager.lua         # ModuleScript
│
└── StarterPlayerScripts/       # Copy contents to StarterPlayerScripts
    └── SlappyClient.lua        # LocalScript
```

## 🚀 Quick Setup in Roblox Studio

### Step 1: Create Workspace Parts

Create these parts in `workspace`:

```
workspace/
├── LobbySpawn        # Part - center of lobby area
├── BattlePlatform    # Part - the shrinking platform (make it big, ~100x100)
└── BattleSpawn       # Part - center of battle platform (optional)
```

**LobbySpawn:**
- Create a Part, name it "LobbySpawn"
- Position it where you want players to spawn in lobby
- Can be Anchored, CanCollide false, Transparency 1

**BattlePlatform:**
- Create a large Part (100 x 5 x 100 studs recommended)
- Name it "BattlePlatform"
- Position it away from lobby (e.g., X=200)
- Anchored = true
- This is the platform that shrinks!

### Step 2: Server Scripts

1. In `ServerScriptService`, create a **Folder** named "SlappySeals"

2. Inside that folder, create:
   - **Script** named "MainInit" → paste MainInit.lua
   - **ModuleScript** named "GameManager" → paste GameManager.lua
   - **ModuleScript** named "PlayerManager" → paste PlayerManager.lua
   - **ModuleScript** named "PlatformManager" → paste PlatformManager.lua
   - **ModuleScript** named "SharkManager" → paste SharkManager.lua
   - **ModuleScript** named "SlapManager" → paste SlapManager.lua

```
ServerScriptService/
└── SlappySeals/
    ├── MainInit         (Script)
    ├── GameManager      (ModuleScript)
    ├── PlayerManager    (ModuleScript)
    ├── PlatformManager  (ModuleScript)
    ├── SharkManager     (ModuleScript)
    └── SlapManager      (ModuleScript)
```

### Step 3: Client Script

1. In `StarterPlayer` → `StarterPlayerScripts`
2. Create a **LocalScript** named "SlappyClient"
3. Paste SlappyClient.lua contents

```
StarterPlayer/
└── StarterPlayerScripts/
    └── SlappyClient     (LocalScript)
```

### Step 4: Test!

1. Click Play
2. Check Output for initialization messages:
   ```
   ========================================
   🦭 SLAPPY SEALS - Initializing...
   ========================================
   ```

3. You should spawn in lobby (spread position)
4. Status should show "Waiting for players..."

### Step 5: Test with Multiple Players

1. Use "Test" → "Start Server" with 4+ players
2. Or publish and test with friends
3. Once 4 players join, 20-second countdown starts
4. Game begins!

---

## ⚙️ Configuration

Edit values in each module's `Config` table:

### GameManager.lua
```lua
local Config = {
    MIN_PLAYERS = 4,              -- Change for testing
    LOBBY_COUNTDOWN = 20,         -- Seconds before game
    PLATFORM_SHRINK_INTERVAL = 12,
    SHARK_THRESHOLD = 7,
}
```

### PlayerManager.lua
```lua
local Config = {
    LOBBY_SPAWN_RADIUS = 25,
    BATTLE_SPAWN_RADIUS = 35,
}
```

### SlapManager.lua
```lua
local Config = {
    SLAP_RANGE = 6,
    SLAP_FLING_POWER = 55,
    SLAP_COOLDOWN = 0.8,
    RAGDOLL_DURATION = 0.6,
}
```

---

## 🎨 Customizing UI

The client script creates UI automatically. To use your **existing placeholder UI**:

1. Find these lines in SlappyClient.lua:
```lua
local ShrinkTimer = UI:WaitForChild("ShrinkTimer")
local ShrinkLabel = ShrinkTimer:WaitForChild("Label")
```

2. Replace with references to your existing UI elements

3. The server fires these events your UI should listen to:
   - `ShrinkTimerUpdate` → (timeRemaining, totalTime)
   - `CountdownUpdate` → (seconds, message)
   - `ShowResultCard` → (cardType, winnerName)
   - `QueueUpdate` → (data table with queuedCount, afkCount)

---

## 🔧 Troubleshooting

### "SlappyEvents not found"
- Make sure MainInit.lua runs first (it creates the events folder)
- Check it's a Script, not ModuleScript

### "No platform found"
- Create a Part named "BattlePlatform" in workspace
- Or "IcePlatform" or "Platform"

### Players stacking on spawn
- Make sure LobbySpawn part exists
- Check PlayerManager is initializing correctly

### Shrink timer not showing
- Timer only shows during IN_PROGRESS state
- Make sure game actually starts (4+ players needed)

### Sharks not spawning
- Sharks only spawn when <7 players remain
- Check SharkManager is getting the platform reference

---

## 📝 Adding Your Seal Character

Replace the default Roblox character with a seal model:

1. Create seal R15/R6 character rig
2. Use StarterCharacter in StarterPlayer, OR
3. Use CharacterAdded to swap models

---

## 🐛 Debug Commands (Output Console)

Access modules from command bar:
```lua
_G.SlappySeals.GameManager:SetState("Countdown")
_G.SlappySeals.PlayerManager:GetQueuedPlayers()
_G.SlappySeals.PlatformManager:ShrinkPlatform()
_G.SlappySeals.SharkManager:SpawnSharkAttack(Vector3.new(0,50,0), "large")
```

---

*Setup guide version 1.0*
*Created: 2026-02-06*
