# Brainrot Spawn System - Script Implementation

**Focus:** Pure logic, no UI/models

---

## System Overview

Collectible items spawn randomly on walkable floor surfaces within defined zones. Uses weighted probability for rarity. Items respawn after collection.

---

## Data Structures

```lua
-- ReplicatedStorage/Data/BrainrotData.lua
local BrainrotData = {
    -- [itemId] = { Value, Rarity, SpawnWeight }
    -- SpawnWeight = relative probability (higher = more common)
    
    ["tung_tung"] = {
        Value = 10,
        Rarity = "Common",
        SpawnWeight = 60,
    },
    
    ["bombardiro"] = {
        Value = 25,
        Rarity = "Uncommon",
        SpawnWeight = 25,
    },
    
    ["trippi_troppi"] = {
        Value = 75,
        Rarity = "Rare",
        SpawnWeight = 10,
    },
    
    ["cocofanto"] = {
        Value = 200,
        Rarity = "Epic",
        SpawnWeight = 4,
    },
    
    ["bombombini"] = {
        Value = 500,
        Rarity = "Legendary",
        SpawnWeight = 1,
    },
}

return BrainrotData
```

```lua
-- ReplicatedStorage/Data/SpawnZoneConfig.lua
local SpawnZoneConfig = {
    -- [zoneName] = { MaxItems, RespawnTime, RarityBoost }
    -- RarityBoost multiplies rare/epic/legendary weights
    
    ["MainHub"] = {
        MaxItems = 30,
        RespawnTime = 10,
        RarityBoost = 1.0,
    },
    
    ["Stage1"] = {
        MaxItems = 20,
        RespawnTime = 15,
        RarityBoost = 1.0,
    },
    
    ["Stage2"] = {
        MaxItems = 25,
        RespawnTime = 12,
        RarityBoost = 1.5,  -- 50% better rare odds
    },
    
    ["VIPArea"] = {
        MaxItems = 15,
        RespawnTime = 8,
        RarityBoost = 3.0,  -- 3x better rare odds
    },
}

return SpawnZoneConfig
```

---

## Player Data Schema

```lua
PlayerData = {
    BrainrotCount = 0,          -- Total collected (for counter display)
    BrainrotValue = 0,          -- Total value (can sell for cash)
    Inventory = {},             -- Optional: list of itemIds if you want individual tracking
}
```

---

## Core Spawn Manager

```lua
-- ServerScriptService/Modules/BrainrotSpawner.lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

local BrainrotData = require(ReplicatedStorage.Data.BrainrotData)
local SpawnZoneConfig = require(ReplicatedStorage.Data.SpawnZoneConfig)

local BrainrotSpawner = {}
local ActiveItems = {}      -- [zoneName] = { item1, item2, ... }
local ZoneParts = {}        -- [zoneName] = Part (cached zone references)

-- Initialize the system
function BrainrotSpawner.Initialize()
    -- Cache zone parts
    for zoneName, _ in pairs(SpawnZoneConfig) do
        local zonePart = workspace.SpawnZones:FindFirstChild(zoneName)
        if zonePart then
            ZoneParts[zoneName] = zonePart
            ActiveItems[zoneName] = {}
        else
            warn("Missing spawn zone: " .. zoneName)
        end
    end
    
    -- Initial fill
    for zoneName, _ in pairs(SpawnZoneConfig) do
        BrainrotSpawner.FillZone(zoneName)
    end
end

-- Fill zone up to MaxItems
function BrainrotSpawner.FillZone(zoneName)
    local config = SpawnZoneConfig[zoneName]
    if not config then return end
    
    local currentCount = #ActiveItems[zoneName]
    local needed = config.MaxItems - currentCount
    
    for i = 1, needed do
        BrainrotSpawner.SpawnOne(zoneName)
    end
end

-- Spawn single item in zone
function BrainrotSpawner.SpawnOne(zoneName)
    local config = SpawnZoneConfig[zoneName]
    local zonePart = ZoneParts[zoneName]
    
    if not config or not zonePart then return nil end
    
    -- Get random floor position
    local position = BrainrotSpawner.GetRandomFloorPosition(zonePart)
    if not position then return nil end
    
    -- Pick random item
    local itemId = BrainrotSpawner.GetWeightedRandomItem(config.RarityBoost)
    local itemData = BrainrotData[itemId]
    
    -- Create the item
    local item = BrainrotSpawner.CreateItem(itemId, itemData, position, zoneName)
    
    if item then
        table.insert(ActiveItems[zoneName], item)
    end
    
    return item
end

return BrainrotSpawner
```

---

## Floor Position Detection

```lua
-- Inside BrainrotSpawner module

-- Get random walkable position using raycast
function BrainrotSpawner.GetRandomFloorPosition(zonePart)
    local size = zonePart.Size
    local cframe = zonePart.CFrame
    
    -- Try up to 10 times to find valid spot
    for attempt = 1, 10 do
        -- Random point within zone bounds (start from top)
        local randomOffset = Vector3.new(
            (math.random() - 0.5) * size.X,
            size.Y / 2,
            (math.random() - 0.5) * size.Z
        )
        
        local startPos = cframe:PointToWorldSpace(randomOffset)
        
        -- Raycast down to find floor
        local rayParams = RaycastParams.new()
        rayParams.FilterType = Enum.RaycastFilterType.Exclude
        rayParams.FilterDescendantsInstances = {
            workspace.ActiveBrainrots,
            workspace.ActiveMonsters,
        }
        
        local result = workspace:Raycast(startPos, Vector3.new(0, -100, 0), rayParams)
        
        if result then
            local hitPart = result.Instance
            
            -- Check if walkable (skip lava, water, etc.)
            if hitPart:GetAttribute("Walkable") ~= false then
                -- Return position slightly above floor
                return result.Position + Vector3.new(0, 2, 0)
            end
        end
    end
    
    return nil
end

-- Alternative: Use pre-placed spawn points
function BrainrotSpawner.GetRandomSpawnPoint(zonePart)
    local spawnPoints = zonePart:FindFirstChild("SpawnPoints")
    if not spawnPoints then return nil end
    
    local points = spawnPoints:GetChildren()
    if #points == 0 then return nil end
    
    local randomPoint = points[math.random(1, #points)]
    return randomPoint.Position + Vector3.new(0, 2, 0)
end
```

---

## Weighted Random Selection

```lua
-- Inside BrainrotSpawner module

function BrainrotSpawner.GetWeightedRandomItem(rarityBoost)
    rarityBoost = rarityBoost or 1.0
    
    -- Build weighted table
    local entries = {}
    local totalWeight = 0
    
    for itemId, data in pairs(BrainrotData) do
        local weight = data.SpawnWeight
        
        -- Apply rarity boost to rare+ items
        if data.Rarity == "Rare" or data.Rarity == "Epic" or data.Rarity == "Legendary" then
            weight = weight * rarityBoost
        end
        
        totalWeight = totalWeight + weight
        table.insert(entries, {
            Id = itemId,
            CumulativeWeight = totalWeight,
        })
    end
    
    -- Random roll
    local roll = math.random() * totalWeight
    
    -- Find selected item
    for _, entry in ipairs(entries) do
        if roll <= entry.CumulativeWeight then
            return entry.Id
        end
    end
    
    -- Fallback
    return entries[1].Id
end
```

**How weighted random works:**
```
Example weights: Common=60, Uncommon=25, Rare=10, Epic=4, Legendary=1
Total = 100

Roll random 0-100:
- 0 to 60 → Common (60% chance)
- 60 to 85 → Uncommon (25% chance)
- 85 to 95 → Rare (10% chance)
- 95 to 99 → Epic (4% chance)
- 99 to 100 → Legendary (1% chance)

With RarityBoost = 2.0:
New weights: Common=60, Uncommon=25, Rare=20, Epic=8, Legendary=2
Total = 115
Rare+ items now have doubled relative probability
```

---

## Item Creation & Collection

```lua
-- Inside BrainrotSpawner module

function BrainrotSpawner.CreateItem(itemId, itemData, position, zoneName)
    -- Get model template (your modeler provides these)
    local template = ReplicatedStorage.Brainrots:FindFirstChild(itemId)
    if not template then
        warn("Missing brainrot model: " .. itemId)
        return nil
    end
    
    local item = template:Clone()
    item.Name = itemId .. "_" .. tostring(os.clock()):gsub("%.", "")
    item:SetPrimaryPartCFrame(CFrame.new(position))
    
    -- Store metadata as attributes
    item:SetAttribute("ItemId", itemId)
    item:SetAttribute("ZoneName", zoneName)
    item:SetAttribute("Value", itemData.Value)
    item:SetAttribute("Rarity", itemData.Rarity)
    item:SetAttribute("SpawnTime", os.time())
    
    -- Setup collection
    BrainrotSpawner.SetupCollection(item)
    
    item.Parent = workspace.ActiveBrainrots
    
    return item
end

function BrainrotSpawner.SetupCollection(item)
    local hitbox = item:FindFirstChild("Hitbox") or item.PrimaryPart
    local collected = false
    
    hitbox.Touched:Connect(function(hit)
        if collected then return end
        
        local character = hit.Parent
        local player = Players:GetPlayerFromCharacter(character)
        
        if not player then return end
        
        collected = true
        
        -- Get item data
        local itemId = item:GetAttribute("ItemId")
        local value = item:GetAttribute("Value")
        local zoneName = item:GetAttribute("ZoneName")
        local rarity = item:GetAttribute("Rarity")
        
        -- Update player data
        local playerData = PlayerDataManager.GetData(player)
        playerData.BrainrotCount = (playerData.BrainrotCount or 0) + 1
        playerData.BrainrotValue = (playerData.BrainrotValue or 0) + value
        
        -- Optional: Add to inventory
        if playerData.Inventory then
            table.insert(playerData.Inventory, itemId)
        end
        
        PlayerDataManager.Save(player)
        
        -- Notify client for effects
        ReplicatedStorage.Events.BrainrotCollected:FireClient(player, itemId, value, rarity)
        
        -- Remove from active items
        local zoneItems = ActiveItems[zoneName]
        if zoneItems then
            local index = table.find(zoneItems, item)
            if index then
                table.remove(zoneItems, index)
            end
        end
        
        -- Destroy item
        item:Destroy()
        
        -- Schedule respawn
        local config = SpawnZoneConfig[zoneName]
        if config then
            task.delay(config.RespawnTime, function()
                BrainrotSpawner.SpawnOne(zoneName)
            end)
        end
    end)
end
```

---

## Auto-Despawn (Optional)

```lua
-- Inside BrainrotSpawner module

local ITEM_LIFETIME = 60  -- Despawn uncollected items after 60 seconds

function BrainrotSpawner.StartDespawnLoop()
    task.spawn(function()
        while true do
            task.wait(10)  -- Check every 10 seconds
            BrainrotSpawner.CheckLifetimes()
        end
    end)
end

function BrainrotSpawner.CheckLifetimes()
    local currentTime = os.time()
    
    for zoneName, items in pairs(ActiveItems) do
        -- Iterate backwards for safe removal
        for i = #items, 1, -1 do
            local item = items[i]
            
            if item and item.Parent then
                local spawnTime = item:GetAttribute("SpawnTime") or 0
                
                if currentTime - spawnTime > ITEM_LIFETIME then
                    table.remove(items, i)
                    item:Destroy()
                    
                    -- Spawn replacement
                    BrainrotSpawner.SpawnOne(zoneName)
                end
            else
                -- Item was destroyed elsewhere, clean up
                table.remove(items, i)
            end
        end
    end
end
```

---

## Selling System

```lua
-- ServerScriptService/SellHandler.lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PlayerDataManager = require(script.Parent.Modules.PlayerDataManager)

-- Client requests to sell all brainrot
ReplicatedStorage.Events.SellBrainrot.OnServerEvent:Connect(function(player)
    local playerData = PlayerDataManager.GetData(player)
    
    local value = playerData.BrainrotValue or 0
    if value <= 0 then
        return
    end
    
    -- Convert to cash
    playerData.Cash = (playerData.Cash or 0) + value
    
    -- Reset brainrot
    playerData.BrainrotCount = 0
    playerData.BrainrotValue = 0
    playerData.Inventory = {}
    
    PlayerDataManager.Save(player)
    
    -- Notify client
    ReplicatedStorage.Events.SoldBrainrot:FireClient(player, value)
end)
```

---

## Workspace Structure Required

```
Workspace/
├── SpawnZones/              -- Invisible Parts covering spawn areas
│   ├── MainHub (Part)       -- CanCollide=false, Transparency=1
│   ├── Stage1 (Part)
│   ├── Stage2 (Part)
│   └── VIPArea (Part)
├── ActiveBrainrots/         -- Spawned items go here
└── Floor/
    ├── GrassFloor (Part)    -- Attribute: Walkable = true (default)
    ├── LavaFloor (Part)     -- Attribute: Walkable = false
    └── Water (Part)         -- Attribute: Walkable = false

ReplicatedStorage/
├── Data/
│   ├── BrainrotData (ModuleScript)
│   └── SpawnZoneConfig (ModuleScript)
├── Brainrots/               -- Item model templates
│   ├── tung_tung (Model)
│   ├── bombardiro (Model)
│   └── ... etc
└── Events/
    ├── BrainrotCollected (RemoteEvent)
    ├── SellBrainrot (RemoteEvent)
    └── SoldBrainrot (RemoteEvent)
```

---

## Initialization Script

```lua
-- ServerScriptService/Main.lua (or init script)
local BrainrotSpawner = require(script.Parent.Modules.BrainrotSpawner)

-- Initialize on server start
BrainrotSpawner.Initialize()

-- Optional: Start auto-despawn loop
BrainrotSpawner.StartDespawnLoop()
```

---

## Key Logic Summary

```
INITIALIZATION:
1. Cache all zone Parts from workspace.SpawnZones
2. For each zone: spawn items up to MaxItems

SPAWN ONE ITEM:
1. GetRandomFloorPosition() - raycast down to find walkable floor
2. GetWeightedRandomItem() - roll weighted random for rarity
3. Clone model, set attributes, setup touch collection
4. Add to ActiveItems[zone]

COLLECTION:
1. Player touches hitbox
2. Update player data (count, value)
3. Fire BrainrotCollected event
4. Remove from ActiveItems
5. Destroy model
6. task.delay(RespawnTime) → SpawnOne()

WEIGHTED RANDOM:
totalWeight = sum(all weights with rarity boost applied)
roll = random(0, totalWeight)
iterate: if roll <= cumulativeWeight, return that item

SELLING:
1. Player fires SellBrainrot event
2. Add BrainrotValue to Cash
3. Reset BrainrotCount, BrainrotValue, Inventory
4. Fire SoldBrainrot event
```

---

## Configuration Tips

**Adjusting spawn rates:**
- Increase `MaxItems` for denser spawns
- Decrease `RespawnTime` for faster respawns
- Adjust `SpawnWeight` values to change rarity distribution

**VIP zones:**
- Use `RarityBoost > 1` to increase rare item chances
- Faster `RespawnTime` for premium feel

**Economy balance:**
- Tune `Value` per item to control income rate
- Legendary should feel special (high value, low weight)
