# Jetpack System - Script Implementation

**Focus:** Pure logic, no UI/models

---

## System Overview

Players unlock jetpacks at level thresholds. Some are free (auto-unlock), some cost trophies.

---

## Data Structure

```lua
-- ReplicatedStorage/Data/JetpackData.lua
local JetpackData = {
    [1] = { RequiredLevel = 10,  Price = 0 },      -- Free at level 10
    [2] = { RequiredLevel = 25,  Price = 35 },     -- 35 trophies
    [3] = { RequiredLevel = 40,  Price = 0 },      -- Free at level 40
    [4] = { RequiredLevel = 60,  Price = 500 },    -- 500 trophies
    [5] = { RequiredLevel = 80,  Price = 0 },      -- Free at level 80
    [6] = { RequiredLevel = 100, Price = 7300 },   -- 7300 trophies (Pulse)
}

return JetpackData
```

---

## Player Data Schema

```lua
PlayerData = {
    Level = 1,
    Trophies = 0,
    OwnedJetpacks = {},      -- {1, 2, 3} = owns jetpack 1, 2, 3
    EquippedJetpack = nil,   -- Currently equipped jetpack ID
}
```

---

## Core Module

```lua
-- ServerScriptService/Modules/JetpackSystem.lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local JetpackData = require(ReplicatedStorage.Data.JetpackData)

local JetpackSystem = {}

-- Check if player meets requirements
function JetpackSystem.CanUnlock(playerData, jetpackId)
    local jetpack = JetpackData[jetpackId]
    if not jetpack then 
        return false, "INVALID_ID" 
    end
    
    -- Already owned
    if table.find(playerData.OwnedJetpacks, jetpackId) then
        return false, "ALREADY_OWNED"
    end
    
    -- Level check
    if playerData.Level < jetpack.RequiredLevel then
        return false, "LEVEL_TOO_LOW"
    end
    
    -- Price check (skip if free)
    if jetpack.Price > 0 and playerData.Trophies < jetpack.Price then
        return false, "NOT_ENOUGH_TROPHIES"
    end
    
    return true, "OK"
end

-- Unlock jetpack (call after CanUnlock passes)
function JetpackSystem.Unlock(playerData, jetpackId)
    local jetpack = JetpackData[jetpackId]
    
    -- Deduct price
    if jetpack.Price > 0 then
        playerData.Trophies = playerData.Trophies - jetpack.Price
    end
    
    -- Add to owned
    table.insert(playerData.OwnedJetpacks, jetpackId)
    
    -- Auto-equip if first jetpack
    if playerData.EquippedJetpack == nil then
        playerData.EquippedJetpack = jetpackId
    end
    
    return true
end

-- Equip owned jetpack
function JetpackSystem.Equip(playerData, jetpackId)
    if not table.find(playerData.OwnedJetpacks, jetpackId) then
        return false, "NOT_OWNED"
    end
    
    playerData.EquippedJetpack = jetpackId
    return true
end

-- Check for free unlocks on level up
function JetpackSystem.CheckAutoUnlocks(playerData)
    local unlocked = {}
    
    for jetpackId, jetpack in pairs(JetpackData) do
        -- Skip if owned
        if table.find(playerData.OwnedJetpacks, jetpackId) then
            continue
        end
        
        -- Free unlock check (Price = 0)
        if jetpack.Price == 0 and playerData.Level >= jetpack.RequiredLevel then
            JetpackSystem.Unlock(playerData, jetpackId)
            table.insert(unlocked, jetpackId)
        end
    end
    
    return unlocked -- Returns list of newly unlocked jetpacks
end

-- Get all available (purchasable) jetpacks for player
function JetpackSystem.GetAvailable(playerData)
    local available = {}
    
    for jetpackId, jetpack in pairs(JetpackData) do
        if not table.find(playerData.OwnedJetpacks, jetpackId) then
            local canUnlock, reason = JetpackSystem.CanUnlock(playerData, jetpackId)
            table.insert(available, {
                Id = jetpackId,
                CanUnlock = canUnlock,
                Reason = reason,
                RequiredLevel = jetpack.RequiredLevel,
                Price = jetpack.Price,
            })
        end
    end
    
    return available
end

return JetpackSystem
```

---

## Server Event Handlers

```lua
-- ServerScriptService/JetpackHandler.lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local JetpackSystem = require(script.Parent.Modules.JetpackSystem)
local PlayerDataManager = require(script.Parent.Modules.PlayerDataManager)

local Events = ReplicatedStorage.Events

-- Client requests to unlock jetpack
Events.UnlockJetpack.OnServerEvent:Connect(function(player, jetpackId)
    local playerData = PlayerDataManager.GetData(player)
    
    local canUnlock, reason = JetpackSystem.CanUnlock(playerData, jetpackId)
    if not canUnlock then
        Events.UnlockJetpack:FireClient(player, false, reason)
        return
    end
    
    JetpackSystem.Unlock(playerData, jetpackId)
    PlayerDataManager.Save(player)
    
    Events.UnlockJetpack:FireClient(player, true, jetpackId)
    Events.JetpackEquipped:FireClient(player, jetpackId) -- Tell client to attach model
end)

-- Client requests to equip jetpack
Events.EquipJetpack.OnServerEvent:Connect(function(player, jetpackId)
    local playerData = PlayerDataManager.GetData(player)
    
    local success, reason = JetpackSystem.Equip(playerData, jetpackId)
    if not success then
        return
    end
    
    PlayerDataManager.Save(player)
    Events.JetpackEquipped:FireClient(player, jetpackId)
end)

-- Hook into level up system
PlayerDataManager.OnLevelUp:Connect(function(player, newLevel)
    local playerData = PlayerDataManager.GetData(player)
    local unlocked = JetpackSystem.CheckAutoUnlocks(playerData)
    
    if #unlocked > 0 then
        PlayerDataManager.Save(player)
        for _, jetpackId in ipairs(unlocked) do
            Events.JetpackUnlocked:FireClient(player, jetpackId)
        end
    end
end)
```

---

## Required RemoteEvents

```
ReplicatedStorage/Events/
├── UnlockJetpack (RemoteEvent)   -- Client → Server: request unlock
├── EquipJetpack (RemoteEvent)    -- Client → Server: request equip
├── JetpackUnlocked (RemoteEvent) -- Server → Client: notify unlock
└── JetpackEquipped (RemoteEvent) -- Server → Client: notify equip (for model attachment)
```

---

## Integration Points

**Your modeler handles:** Attaching jetpack model to character when `JetpackEquipped` fires

**Your UI person handles:** Shop display using `JetpackSystem.GetAvailable()` data

**You provide:** The above scripts + data structure

---

## Key Logic Summary

```
UNLOCK FLOW:
1. Client fires UnlockJetpack(jetpackId)
2. Server checks: owned? level? trophies?
3. If pass: deduct trophies, add to OwnedJetpacks, save
4. Fire JetpackEquipped to client

LEVEL UP FLOW:
1. Player levels up
2. Call CheckAutoUnlocks(playerData)
3. Any free jetpacks (Price=0) at or below new level get auto-unlocked
4. Fire JetpackUnlocked for each
```
