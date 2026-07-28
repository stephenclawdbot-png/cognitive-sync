# Reverse Engineering - Script Implementation

**Pure systems code. No UI, no models, no visual effects.**

Your team handles: Models, UI, Visual Effects  
You handle: These scripts

---

## Files

| File | System | Est. Time |
|------|--------|-----------|
| `01_JetpackSystem.md` | Level-gated unlocks, equip system | 1 hour |
| `02_MonsterSystem.md` | Patrol AI (waypoint, bounce, circle, linear, pivot) | 2-3 hours |
| `03_BrainrotSpawnSystem.md` | Weighted random floor spawning | 2-3 hours |

---

## Each File Contains

- Data structures (Lua tables)
- Core module code (copy-paste ready)
- Server event handlers
- Required RemoteEvents list
- Workspace folder structure
- Logic flow summary

---

## Quick Start

### 1. Create folder structure in workspace
### 2. Create ModuleScripts from data structures
### 3. Create server scripts from core modules
### 4. Create RemoteEvents in ReplicatedStorage/Events
### 5. Have your modeler add model templates
### 6. Have your UI person connect to the events

---

## Dependencies

All three systems need a `PlayerDataManager` module. Basic template:

```lua
-- ServerScriptService/Modules/PlayerDataManager.lua
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

local PlayerDataManager = {}
local PlayerData = {}
local DataStore = DataStoreService:GetDataStore("PlayerData_v1")

-- Bindable for other scripts to listen to
PlayerDataManager.OnLevelUp = Instance.new("BindableEvent")

function PlayerDataManager.GetData(player)
    return PlayerData[player.UserId]
end

function PlayerDataManager.Save(player)
    local data = PlayerData[player.UserId]
    if data then
        pcall(function()
            DataStore:SetAsync(tostring(player.UserId), data)
        end)
    end
end

function PlayerDataManager.Load(player)
    local success, data = pcall(function()
        return DataStore:GetAsync(tostring(player.UserId))
    end)
    
    if success and data then
        PlayerData[player.UserId] = data
    else
        -- Default data
        PlayerData[player.UserId] = {
            Level = 1,
            Steps = 0,
            Speed = 1,
            Trophies = 0,
            Cash = 0,
            OwnedJetpacks = {},
            EquippedJetpack = nil,
            BrainrotCount = 0,
            BrainrotValue = 0,
            LastCheckpoint = 1,
        }
    end
    
    return PlayerData[player.UserId]
end

function PlayerDataManager.AddLevel(player, amount)
    local data = PlayerData[player.UserId]
    local oldLevel = data.Level
    data.Level = data.Level + (amount or 1)
    
    -- Fire event for other systems
    PlayerDataManager.OnLevelUp:Fire(player, data.Level)
end

Players.PlayerAdded:Connect(function(player)
    PlayerDataManager.Load(player)
end)

Players.PlayerRemoving:Connect(function(player)
    PlayerDataManager.Save(player)
    PlayerData[player.UserId] = nil
end)

return PlayerDataManager
```

---

## Integration Points

**Jetpack System:**
- Fires `JetpackEquipped` → Your modeler attaches model to character
- Fires `JetpackUnlocked` → Your UI shows unlock popup

**Monster System:**
- Fires `MonsterHit` → Your UI/effects person shows hit effect
- Requires model templates in `ReplicatedStorage/Monsters/`

**Brainrot System:**
- Fires `BrainrotCollected` → Your UI shows +value popup
- Fires `SoldBrainrot` → Your UI shows cash gained
- Requires model templates in `ReplicatedStorage/Brainrots/`

---

## Workspace Structure (Combined)

```
Workspace/
├── SpawnZones/          -- Brainrot spawn areas
├── ActiveBrainrots/     -- Spawned collectibles
├── ActiveMonsters/      -- Spawned monsters
├── Stages/
│   ├── Stage1/
│   │   └── MonsterSpawns/
│   └── Stage2/
│       └── MonsterSpawns/
├── StageTriggers/       -- Stage entry detection
├── Checkpoints/         -- Respawn points
└── Floor/               -- Walkable surfaces

ReplicatedStorage/
├── Data/
│   ├── JetpackData
│   ├── MonsterData
│   ├── BrainrotData
│   └── SpawnZoneConfig
├── Jetpacks/            -- Model templates
├── Monsters/            -- Model templates
├── Brainrots/           -- Model templates
└── Events/
    ├── UnlockJetpack
    ├── EquipJetpack
    ├── JetpackUnlocked
    ├── JetpackEquipped
    ├── MonsterHit
    ├── BrainrotCollected
    ├── SellBrainrot
    └── SoldBrainrot

ServerScriptService/
├── Modules/
│   ├── PlayerDataManager
│   ├── JetpackSystem
│   ├── MonsterSpawner
│   └── BrainrotSpawner
├── JetpackHandler
├── StageManager
├── DeathHandler
├── SellHandler
└── Main (init)
```
