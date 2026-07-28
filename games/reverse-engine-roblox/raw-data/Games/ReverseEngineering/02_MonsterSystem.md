# Monster/Hazard System - Script Implementation

**Focus:** Pure logic, no UI/models

---

## System Overview

Monsters patrol on fixed paths within stages. Contact with player = penalty (death/teleport/step loss). Monsters spawn when player enters stage.

---

## Data Structure

```lua
-- ReplicatedStorage/Data/MonsterData.lua
local MonsterData = {
    ["LavaSlime"] = {
        Speed = 8,
        PatrolType = "Waypoint",  -- Waypoint, Bounce, Circle
        Damage = 100,             -- 100 = instant kill
    },
    
    ["FireBall"] = {
        Speed = 15,
        PatrolType = "Linear",    -- Shoots straight, despawns at end
        Damage = 100,
        RespawnDelay = 3,         -- Seconds before respawn
    },
    
    ["SwingingAxe"] = {
        Speed = 2,                -- Rotation speed for pivot
        PatrolType = "Pivot",     -- Swings back and forth
        Damage = 100,
    },
}

return MonsterData
```

---

## Spawn Point Configuration

Spawn points are Parts in workspace with these **Attributes**:

```
SpawnPoint (Part)
├── Attribute: MonsterType (string) = "LavaSlime"
├── Attribute: PatrolDistance (number) = 20
├── Attribute: PatrolDirection (Vector3) = (1, 0, 0)
├── Attribute: StartDelay (number) = 0
└── Child: Waypoints (Folder) -- Only for Waypoint patrol type
    ├── 1 (Part)
    ├── 2 (Part)
    └── 3 (Part)
```

---

## Core Spawn Manager

```lua
-- ServerScriptService/Modules/MonsterSpawner.lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local Players = game:GetService("Players")

local MonsterData = require(ReplicatedStorage.Data.MonsterData)

local MonsterSpawner = {}
local ActiveMonsters = {}  -- [monsterName] = { Model, SpawnPoint, Connection }
local StageMonsters = {}   -- [stageNumber] = { monsterName1, monsterName2, ... }

-- Spawn monster at a spawn point
function MonsterSpawner.Spawn(spawnPoint)
    local monsterType = spawnPoint:GetAttribute("MonsterType")
    local data = MonsterData[monsterType]
    
    if not data then
        warn("Unknown monster type: " .. tostring(monsterType))
        return nil
    end
    
    -- Get model from storage (your modeler puts these here)
    local template = ReplicatedStorage.Monsters:FindFirstChild(monsterType)
    if not template then
        warn("Missing monster model: " .. monsterType)
        return nil
    end
    
    local monster = template:Clone()
    monster.Name = monsterType .. "_" .. spawnPoint.Name
    monster:SetPrimaryPartCFrame(spawnPoint.CFrame)
    monster.Parent = workspace.ActiveMonsters
    
    -- Setup collision
    local hitConnection = MonsterSpawner.SetupCollision(monster, data, spawnPoint)
    
    -- Setup patrol movement
    local moveConnection = MonsterSpawner.SetupPatrol(monster, spawnPoint, data)
    
    -- Track
    ActiveMonsters[monster.Name] = {
        Model = monster,
        SpawnPoint = spawnPoint,
        HitConnection = hitConnection,
        MoveConnection = moveConnection,
    }
    
    return monster
end

-- Despawn monster
function MonsterSpawner.Despawn(monsterName)
    local monsterInfo = ActiveMonsters[monsterName]
    if not monsterInfo then return end
    
    if monsterInfo.HitConnection then
        monsterInfo.HitConnection:Disconnect()
    end
    if monsterInfo.MoveConnection then
        monsterInfo.MoveConnection:Disconnect()
    end
    if monsterInfo.Model then
        monsterInfo.Model:Destroy()
    end
    
    ActiveMonsters[monsterName] = nil
end

-- Despawn all monsters in a stage
function MonsterSpawner.DespawnStage(stageNumber)
    local monsters = StageMonsters[stageNumber]
    if not monsters then return end
    
    for _, monsterName in ipairs(monsters) do
        MonsterSpawner.Despawn(monsterName)
    end
    
    StageMonsters[stageNumber] = nil
end

return MonsterSpawner
```

---

## Collision Detection

```lua
-- Inside MonsterSpawner module
function MonsterSpawner.SetupCollision(monster, data, spawnPoint)
    local hitbox = monster:FindFirstChild("Hitbox") or monster.PrimaryPart
    
    local connection = hitbox.Touched:Connect(function(hit)
        local character = hit.Parent
        local humanoid = character:FindFirstChildOfClass("Humanoid")
        
        if not humanoid or humanoid.Health <= 0 then return end
        
        local player = Players:GetPlayerFromCharacter(character)
        if not player then return end
        
        -- Debounce per player
        local debounceKey = "MonsterHit_" .. player.UserId
        if character:GetAttribute(debounceKey) then return end
        character:SetAttribute(debounceKey, true)
        
        -- Apply damage
        humanoid:TakeDamage(data.Damage)
        
        -- Fire event for client effects
        ReplicatedStorage.Events.MonsterHit:FireClient(player, monster.Name)
        
        -- Remove debounce after delay
        task.delay(1, function()
            if character then
                character:SetAttribute(debounceKey, nil)
            end
        end)
    end)
    
    return connection
end
```

---

## Patrol Movement Systems

```lua
-- Inside MonsterSpawner module
function MonsterSpawner.SetupPatrol(monster, spawnPoint, data)
    local patrolType = data.PatrolType
    
    if patrolType == "Waypoint" then
        return MonsterSpawner.WaypointPatrol(monster, spawnPoint, data)
    elseif patrolType == "Bounce" then
        return MonsterSpawner.BouncePatrol(monster, spawnPoint, data)
    elseif patrolType == "Circle" then
        return MonsterSpawner.CirclePatrol(monster, spawnPoint, data)
    elseif patrolType == "Linear" then
        return MonsterSpawner.LinearPatrol(monster, spawnPoint, data)
    elseif patrolType == "Pivot" then
        return MonsterSpawner.PivotPatrol(monster, spawnPoint, data)
    end
    
    return nil
end

-- WAYPOINT: Follow a series of points in order
function MonsterSpawner.WaypointPatrol(monster, spawnPoint, data)
    local waypointsFolder = spawnPoint:FindFirstChild("Waypoints")
    if not waypointsFolder then return nil end
    
    local waypoints = {}
    for _, wp in ipairs(waypointsFolder:GetChildren()) do
        table.insert(waypoints, wp.Position)
    end
    table.insert(waypoints, spawnPoint.Position) -- Return to start
    
    local currentIndex = 1
    local rootPart = monster.PrimaryPart
    
    local connection = RunService.Heartbeat:Connect(function(dt)
        if not monster or not monster.Parent then return end
        
        local targetPos = waypoints[currentIndex]
        local currentPos = rootPart.Position
        local direction = (targetPos - currentPos)
        local distance = direction.Magnitude
        
        if distance < 1 then
            -- Next waypoint
            currentIndex = currentIndex + 1
            if currentIndex > #waypoints then
                currentIndex = 1
            end
        else
            -- Move toward target
            local moveDir = direction.Unit
            local newPos = currentPos + (moveDir * data.Speed * dt)
            rootPart.CFrame = CFrame.new(newPos, targetPos)
        end
    end)
    
    return connection
end

-- BOUNCE: Move back and forth on one axis
function MonsterSpawner.BouncePatrol(monster, spawnPoint, data)
    local distance = spawnPoint:GetAttribute("PatrolDistance") or 10
    local direction = spawnPoint:GetAttribute("PatrolDirection") or Vector3.new(1, 0, 0)
    
    local startPos = spawnPoint.Position
    local endPos = startPos + (direction.Unit * distance)
    local goingForward = true
    local rootPart = monster.PrimaryPart
    
    local connection = RunService.Heartbeat:Connect(function(dt)
        if not monster or not monster.Parent then return end
        
        local targetPos = goingForward and endPos or startPos
        local currentPos = rootPart.Position
        local toTarget = targetPos - currentPos
        
        if toTarget.Magnitude < 1 then
            goingForward = not goingForward
        else
            local moveDir = toTarget.Unit
            local newPos = currentPos + (moveDir * data.Speed * dt)
            rootPart.CFrame = CFrame.new(newPos, targetPos)
        end
    end)
    
    return connection
end

-- CIRCLE: Orbit around spawn point
function MonsterSpawner.CirclePatrol(monster, spawnPoint, data)
    local radius = spawnPoint:GetAttribute("PatrolDistance") or 5
    local centerPos = spawnPoint.Position
    local angle = 0
    local rootPart = monster.PrimaryPart
    
    local connection = RunService.Heartbeat:Connect(function(dt)
        if not monster or not monster.Parent then return end
        
        angle = angle + (data.Speed * dt * 0.5)
        
        local x = centerPos.X + math.cos(angle) * radius
        local z = centerPos.Z + math.sin(angle) * radius
        local y = centerPos.Y
        
        local newPos = Vector3.new(x, y, z)
        local lookDir = Vector3.new(-math.sin(angle), 0, math.cos(angle))
        
        rootPart.CFrame = CFrame.new(newPos, newPos + lookDir)
    end)
    
    return connection
end

-- LINEAR: Projectile that despawns at distance, then respawns
function MonsterSpawner.LinearPatrol(monster, spawnPoint, data)
    local direction = spawnPoint:GetAttribute("PatrolDirection") or spawnPoint.CFrame.LookVector
    local maxDistance = spawnPoint:GetAttribute("PatrolDistance") or 50
    
    local startPos = spawnPoint.Position
    local rootPart = monster.PrimaryPart
    
    local connection = RunService.Heartbeat:Connect(function(dt)
        if not monster or not monster.Parent then return end
        
        local traveled = (rootPart.Position - startPos).Magnitude
        
        if traveled >= maxDistance then
            -- Despawn and schedule respawn
            local monsterName = monster.Name
            MonsterSpawner.Despawn(monsterName)
            
            task.delay(data.RespawnDelay or 3, function()
                MonsterSpawner.Spawn(spawnPoint)
            end)
        else
            -- Move forward
            rootPart.CFrame = rootPart.CFrame + (direction.Unit * data.Speed * dt)
        end
    end)
    
    return connection
end

-- PIVOT: Swing back and forth (like a pendulum)
function MonsterSpawner.PivotPatrol(monster, spawnPoint, data)
    local pivotPoint = spawnPoint.Position
    local angle = 0
    local swingRange = math.rad(90) -- 90 degrees each way
    local rootPart = monster.PrimaryPart
    local armLength = spawnPoint:GetAttribute("PatrolDistance") or 5
    
    local connection = RunService.Heartbeat:Connect(function(dt)
        if not monster or not monster.Parent then return end
        
        angle = angle + (data.Speed * dt)
        local swing = math.sin(angle) * swingRange
        
        local offsetX = math.sin(swing) * armLength
        local offsetY = -math.cos(swing) * armLength
        
        local newPos = pivotPoint + Vector3.new(offsetX, offsetY, 0)
        rootPart.CFrame = CFrame.new(newPos) * CFrame.Angles(0, 0, swing)
    end)
    
    return connection
end
```

---

## Stage Activation

```lua
-- ServerScriptService/StageManager.lua
local MonsterSpawner = require(script.Parent.Modules.MonsterSpawner)

local StageManager = {}
local PlayerStages = {} -- [player] = currentStageNumber

-- Called when player enters a stage zone
function StageManager.OnEnterStage(player, stageNumber)
    local previousStage = PlayerStages[player]
    PlayerStages[player] = stageNumber
    
    -- Spawn monsters for this stage if not already spawned
    local stageFolder = workspace.Stages:FindFirstChild("Stage" .. stageNumber)
    if not stageFolder then return end
    
    local spawnsFolder = stageFolder:FindFirstChild("MonsterSpawns")
    if not spawnsFolder then return end
    
    for _, spawnPoint in ipairs(spawnsFolder:GetChildren()) do
        if spawnPoint:IsA("BasePart") then
            local delay = spawnPoint:GetAttribute("StartDelay") or 0
            task.delay(delay, function()
                MonsterSpawner.Spawn(spawnPoint)
            end)
        end
    end
end

-- Setup stage trigger zones
function StageManager.Initialize()
    for _, trigger in ipairs(workspace.StageTriggers:GetChildren()) do
        local stageNum = trigger:GetAttribute("StageNumber")
        
        trigger.Touched:Connect(function(hit)
            local player = game.Players:GetPlayerFromCharacter(hit.Parent)
            if player then
                StageManager.OnEnterStage(player, stageNum)
            end
        end)
    end
end

return StageManager
```

---

## Death/Respawn Handler

```lua
-- ServerScriptService/DeathHandler.lua
local Players = game:GetService("Players")

local function OnCharacterAdded(player, character)
    local humanoid = character:WaitForChild("Humanoid")
    
    humanoid.Died:Connect(function()
        -- Get last checkpoint
        local checkpoint = player:GetAttribute("LastCheckpoint") or 1
        
        -- Wait for respawn
        task.wait(2)
        
        -- Teleport to checkpoint
        local spawnPoint = workspace.Checkpoints:FindFirstChild("Checkpoint_" .. checkpoint)
        if spawnPoint and player.Character then
            player.Character:SetPrimaryPartCFrame(spawnPoint.CFrame + Vector3.new(0, 3, 0))
        end
    end)
end

Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function(character)
        OnCharacterAdded(player, character)
    end)
end)
```

---

## Workspace Structure Required

```
Workspace/
├── ActiveMonsters/          -- Spawned monsters go here
├── Stages/
│   ├── Stage1/
│   │   └── MonsterSpawns/   -- Spawn point Parts with Attributes
│   └── Stage2/
│       └── MonsterSpawns/
├── StageTriggers/           -- Parts that detect player entry
│   ├── Stage1Trigger        -- Attribute: StageNumber = 1
│   └── Stage2Trigger        -- Attribute: StageNumber = 2
└── Checkpoints/
    ├── Checkpoint_1 (Part)
    └── Checkpoint_2 (Part)

ReplicatedStorage/
├── Data/
│   └── MonsterData (ModuleScript)
├── Monsters/                -- Monster model templates
│   ├── LavaSlime (Model)
│   └── FireBall (Model)
└── Events/
    └── MonsterHit (RemoteEvent)
```

---

## Key Logic Summary

```
SPAWN FLOW:
1. Player touches StageTrigger
2. StageManager.OnEnterStage() called
3. Loop through MonsterSpawns folder
4. For each spawn point: clone model, setup collision, setup patrol
5. Track in ActiveMonsters table

PATROL TYPES:
- Waypoint: Follow child Parts in order, loop
- Bounce: A to B to A, repeat
- Circle: Orbit center point
- Linear: Shoot forward, despawn at distance, respawn after delay
- Pivot: Pendulum swing

COLLISION:
1. Hitbox.Touched fires
2. Check if player (not NPC)
3. Debounce check
4. TakeDamage(100) = instant kill
5. Fire MonsterHit event for client effects
```
