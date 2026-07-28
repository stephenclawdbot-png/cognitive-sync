# Reverse Engine Roblox — Data Models (JSON / Lua Schemas)

**Type:** Complete data schemas for the architecture described in ARCHITECTURE.md
**Format:** Each schema given as a Lua table structure AND a JSON example
**Based on:** 9 reverse-engineered Roblox game analyses
**Date:** 2026-07-29

---

## 1. Player Data

The single authoritative per-player save. Lives in `PlayerSession[userId]` on the server, persisted to `DataStore("PlayerData_vN")`.

### 1.1 Lua table structure

```lua
-- PlayerData (server-authoritative, persisted)
local PlayerData = {
    version = 5,                -- schema version for migration

    -- Identity
    userId = 0,
    displayName = "",
    firstJoin = 0,              -- os.time()
    lastLogin = 0,               -- os.time()
    playtimeSeconds = 0,

    -- Currencies
    clicks = 0,                  -- primary soft currency (Tap Simulator)
    cash = 0,                    -- alt soft currency (Your Zoo, House Tycoon)
    gems = 0,                    -- premium hard currency
    keys = 0,                    -- event currency (House Tycoon)

    -- Prestige
    rebirths = 0,
    rebirthMultiplier = 1,       -- 2.5^rebirths (cached)
    prestigePoints = 0,          -- meta-progression currency

    -- Progression
    level = 1,
    xp = 0,
    currentZoneId = "starter",
    unlockedZones = { starter = true },

    -- Pets / collection
    pets = {},                   -- [petUid] = PetInstance
    equippedPets = {},           -- [slot] = petUid
    petSlots = 2,                -- level-gated (Catch a Monster: Lv.7 → slot 2)
    eggInventory = {},           -- [eggUid] = EggInstance (purchased, not hatched)
    index = {},                   -- [petId] = { discovered=true, ownedCount=N, variants={} }

    -- Tycoon / Zoo
    plotId = nil,                -- claimed plot (Tycoon/Zoo)
    buildings = {},              -- [buildingId] = { level, lastUpgradeAt }
    zooSlots = {},               -- [slotId] = petUid (placed animals)

    -- Pity timers (Your Zoo pattern)
    pityCounters = { golden = 0, rainbow = 0, secret = 0 },
    -- Thresholds may be in EggData; duplicated here for fast access
    pityThresholds = { golden = 10, rainbow = 60, secret = 180 },

    -- Quests
    quests = {},                 -- [questId] = { progress, claimed, expiresAt }
    dailyStreak = 0,
    lastDailyClaim = 0,

    -- Monetization
    gamepasses = {},             -- [gamepassId] = true (owned)
    devProductsClaimed = {},    -- [receiptId] = true (idempotency)
    codesRedeemed = {},          -- [code] = true

    -- Boosts
    activeBoosts = {},           -- [boostId] = { expiresAt, multiplier }
    autoclicker = false,         -- gamepass-gated
    autoclickerUsesRemaining = 0,-- House Tycoon pattern: 99 remaining

    -- Social
    friends = {},                -- [friendUserId] = true
    friendLuck = 0,              -- Catch a Monster pattern
    trades = {},                  -- recent trade ids

    -- Settings
    settings = {
        haptics = true,
        music = true,
        sfx = true,
        reducedMotion = false,
    },

    -- Stats
    stats = {
        totalTaps = 0,
        totalEggsOpened = 0,
        totalRebirths = 0,
        totalTrades = 0,
        bestClicksPerTap = 0,
    },

    -- Meta
    banned = false,
    banReason = "",
    flags = {},                  -- anti-exploit flags
    lastSaveAt = 0,
}
```

### 1.2 JSON example

```json
{
  "version": 5,
  "userId": 123456789,
  "displayName": "MaxPlays",
  "firstJoin": 1766910000,
  "lastLogin": 1767996000,
  "playtimeSeconds": 86400,
  "clicks": 1250000,
  "cash": 500,
  "gems": 455,
  "keys": 5,
  "rebirths": 71,
  "rebirthMultiplier": 1.0,
  "prestigePoints": 0,
  "level": 18,
  "xp": 160,
  "currentZoneId": "forest",
  "unlockedZones": { "starter": true, "forest": true },
  "pets": {
    "p_001": { "uid": "p_001", "petId": "fire_dragon", "variant": "Rainbow", "level": 12, "xp": 340, "equipped": true, "obtainedAt": 1767000000 },
    "p_002": { "uid": "p_002", "petId": "leafet",     "variant": null,      "level": 6,  "xp": 40,  "equipped": false,"obtainedAt": 1767100000 }
  },
  "equippedPets": { "1": "p_001" },
  "petSlots": 2,
  "eggInventory": { "e_010": { "uid": "e_010", "eggId": "acorn", "opened": false, "purchasedAt": 1767996000 } },
  "index": {
    "fire_dragon": { "discovered": true, "ownedCount": 1, "variants": { "Normal": true, "Rainbow": true } },
    "leafet":      { "discovered": true, "ownedCount": 1, "variants": { "Normal": true } }
  },
  "plotId": 4,
  "buildings": { "house": { "level": 3, "lastUpgradeAt": 1767900000 }, "mine": { "level": 1, "lastUpgradeAt": 1767800000 } },
  "zooSlots": {},
  "pityCounters": { "golden": 3, "rainbow": 12, "secret": 47 },
  "pityThresholds": { "golden": 10, "rainbow": 60, "secret": 180 },
  "quests": {
    "q_daily_1": { "progress": 4, "target": 5, "claimed": false, "expiresAt": 1768000000 },
    "q_milestone_rebirth5": { "progress": 1, "target": 5, "claimed": false, "expiresAt": 0 }
  },
  "dailyStreak": 7,
  "lastDailyClaim": 1767900000,
  "gamepasses": { "autoclicker": true, "x2_taps": true },
  "devProductsClaimed": {},
  "codesRedeemed": { "SUMMER2026": true },
  "activeBoosts": { "x2_cash": { "expiresAt": 1768000000, "multiplier": 2.0 } },
  "autoclicker": true,
  "autoclickerUsesRemaining": 99,
  "friends": { 987654321: true },
  "friendLuck": 0.05,
  "trades": [],
  "settings": { "haptics": true, "music": true, "sfx": true, "reducedMotion": false },
  "stats": { "totalTaps": 2500000, "totalEggsOpened": 480, "totalRebirths": 71, "totalTrades": 12, "bestClicksPerTap": 1728 },
  "banned": false,
  "banReason": "",
  "flags": {},
  "lastSaveAt": 1767996060
}
```

---

## 2. Pet Definitions

Static pet catalog in `ReplicatedStorage.Modules.PetData`. Read-only on client (for UI), authoritative on server.

### 2.1 Lua table structure

```lua
PetDefinitions = {
    [petId] = {
        id = "fire_dragon",
        name = "Fire Dragon",
        rarity = "Legendary",           -- Common | Rare | Epic | Legendary | Secret
        elements = { "Fire" },            -- for type-effectiveness (Catch a Monster)
        baseStats = { hp=80, attack=20, defense=15, speed=10 },
        tapBoost = 500,                  -- multiplier to tap income (Tap Simulator)
        passiveBoost = 50,               -- passive income/s
        evolvesTo = "inferno_dragon",    -- nil if no evolution
        evolvesAtLevel = 16,
        hatchChance = 0.019,             -- base chance in parent egg (overridden by egg loot table)
        variants = {
            Normal  = { chance = 1.0,   multiplier = 1.0, color = nil },
            Golden  = { chance = 0.05,  multiplier = 1.5, color = Color3.fromRGB(255,215,0) },
            Rainbow  = { chance = 0.01,  multiplier = 2.0, color = "rainbow" },
            Glitch   = { chance = 0.001, multiplier = 3.0, color = Color3.fromRGB(0,255,0) },
        },
        tradeValue = 1500,               -- suggested trade value (gems)
        meshId = "rbxassetid://1234567890",
        textureId = "rbxassetid://1234567891",
        iconId = "rbxassetid://1234567892",  -- for UI
        description = "A fierce dragon wreathed in flame.",
        secret = false,                   -- secret pets are ultra-rare (1 in 1M observed)
    },
}
```

### 2.2 JSON example

```json
{
  "fire_dragon": {
    "id": "fire_dragon",
    "name": "Fire Dragon",
    "rarity": "Legendary",
    "elements": ["Fire"],
    "baseStats": { "hp": 80, "attack": 20, "defense": 15, "speed": 10 },
    "tapBoost": 500,
    "passiveBoost": 50,
    "evolvesTo": "inferno_dragon",
    "evolvesAtLevel": 16,
    "hatchChance": 0.019,
    "variants": {
      "Normal":  { "chance": 1.0,   "multiplier": 1.0, "color": null },
      "Golden":  { "chance": 0.05,  "multiplier": 1.5, "color": [255,215,0] },
      "Rainbow": { "chance": 0.01,  "multiplier": 2.0, "color": "rainbow" },
      "Glitch":  { "chance": 0.001, "multiplier": 3.0, "color": [0,255,0] }
    },
    "tradeValue": 1500,
    "meshId": "rbxassetid://1234567890",
    "textureId": "rbxassetid://1234567891",
    "iconId": "rbxassetid://1234567892",
    "description": "A fierce dragon wreathed in flame.",
    "secret": false
  },
  "emperyean_sovereign": {
    "id": "emperyean_sovereign",
    "name": "Empyrean Sovereign",
    "rarity": "Secret",
    "elements": ["Light"],
    "baseStats": { "hp": 999, "attack": 999, "defense": 999, "speed": 999 },
    "tapBoost": 99999,
    "passiveBoost": 9999,
    "evolvesTo": null,
    "evolvesAtLevel": null,
    "hatchChance": 0.000001,
    "variants": { "Normal": { "chance": 1.0, "multiplier": 1.0, "color": null } },
    "tradeValue": 1000000,
    "meshId": "rbxassetid://2222222220",
    "textureId": "rbxassetid://2222222221",
    "iconId": "rbxassetid://2222222222",
    "description": "A 1-in-1,000,000 secret sovereign of the empyrean realm.",
    "secret": true
  }
}
```

### 2.3 PetInstance (owned pet, per-player)

```lua
PetInstance = {
    uid = "p_001",                -- unique instance id (UUID-ish)
    petId = "fire_dragon",        -- references PetDefinitions
    variant = "Rainbow",          -- nil | "Golden" | "Rainbow" | "Glitch"
    level = 12,
    xp = 340,
    equipped = true,
    obtainedAt = 1767000000,      -- os.time()
    obtainedFrom = "egg:acorn",   -- provenance: egg, trade, event, code
}
```

```json
{
  "uid": "p_001",
  "petId": "fire_dragon",
  "variant": "Rainbow",
  "level": 12,
  "xp": 340,
  "equipped": true,
  "obtainedAt": 1767000000,
  "obtainedFrom": "egg:acorn"
}
```

---

## 3. Egg Definitions

### 3.1 Lua table structure

```lua
EggDefinitions = {
    [eggId] = {
        id = "acorn",
        name = "Acorn Egg",
        cost = 1000,                       -- in clicks/cash
        currency = "clicks",               -- "clicks" | "cash" | "gems"
        zone = "forest",                   -- zone where sold
        hatchTime = 5,                     -- seconds (or 0 for instant)
        tripleHatch = true,                -- 3x hatch allowed (Tap Sim: now free)
        pityTier = "golden",               -- which pity bucket this egg fills
        lootTable = {
            { petId = "squirrel",         chance = 50.0 },
            { petId = "chipmunk",         chance = 30.0 },
            { petId = "golden_squirrel",  chance = 15.0 },
            { petId = "rainbow_squirrel", chance = 4.9 },
            { petId = "emperyean_sovereign", chance = 0.0001 },
        },
        iconId = "rbxassetid://...",
        modelId = "rbxassetid://...",
    },
}
```

### 3.2 JSON example

```json
{
  "acorn": {
    "id": "acorn",
    "name": "Acorn Egg",
    "cost": 1000,
    "currency": "clicks",
    "zone": "forest",
    "hatchTime": 5,
    "tripleHatch": true,
    "pityTier": "golden",
    "lootTable": [
      { "petId": "squirrel",         "chance": 50.0 },
      { "petId": "chipmunk",         "chance": 30.0 },
      { "petId": "golden_squirrel",  "chance": 15.0 },
      { "petId": "rainbow_squirrel", "chance": 4.9 },
      { "petId": "emperyean_sovereign", "chance": 0.0001 }
    ],
    "iconId": "rbxassetid://3000000001",
    "modelId": "rbxassetid://3000000002"
  }
}
```

### 3.3 EggInstance (owned, not hatched)

```lua
EggInstance = { uid = "e_010", eggId = "acorn", opened = false, purchasedAt = 1767996000 }
```

---

## 4. Round / Match Data

For round-based game types (Slappy Seals pattern). Lives in `RoundManager` server state.

### 4.1 Lua table structure

```lua
RoundConfig = {
    id = "default",
    minPlayers = 2,
    maxPlayers = 16,
    durationSeconds = 120,
    countdownSeconds = 5,
    platformShrink = { startSize = 70, endSize = 10, duration = 2.5 },
    sharkSpawnAtSecond = 90,
    rewardFormula = "rank_bonus",        -- function key in RewardCurves
    zones = { "arena_1" },
}

RoundState = {
    roundId = "r_20260729_001",
    state = "InProgress",                 -- WaitingForPlayers|MatchStarting|Countdown|InProgress|RoundEnd|Rewards
    players = {},                         -- [userId] = { alive=true, score=0, plot=4 }
    startedAt = 1767996000,
    endsAt = 1767996120,
    winnerUserId = nil,
    rewardsDistributed = false,
}
```

### 4.2 JSON example

```json
{
  "roundConfig": {
    "id": "default",
    "minPlayers": 2,
    "maxPlayers": 16,
    "durationSeconds": 120,
    "countdownSeconds": 5,
    "platformShrink": { "startSize": 70, "endSize": 10, "duration": 2.5 },
    "sharkSpawnAtSecond": 90,
    "rewardFormula": "rank_bonus",
    "zones": ["arena_1"]
  },
  "roundState": {
    "roundId": "r_20260729_001",
    "state": "InProgress",
    "players": {
      "123456789": { "alive": true, "score": 420, "plot": 4 },
      "987654321": { "alive": false, "score": 80,  "plot": 2 }
    },
    "startedAt": 1767996000,
    "endsAt": 1767996120,
    "winnerUserId": null,
    "rewardsDistributed": false
  }
}
```

---

## 5. Tycoon Data

### 5.1 Plot / buildings

```lua
Plot = {
    id = 4,
    ownerUserId = 123456789,
    template = "house_tycoon",           -- which plot template
    level = 3,
    buildings = {
        house = { level = 3, lastUpgradeAt = 1767900000 },
        mine  = { level = 1, lastUpgradeAt = 1767800000 },
    },
    incomePerSecond = 13,                -- cached, recomputed on upgrade
    decor = {},                          -- placed decorations (House Tycoon: 0/6 limit)
}
```

```json
{
  "id": 4,
  "ownerUserId": 123456789,
  "template": "house_tycoon",
  "level": 3,
  "buildings": {
    "house": { "level": 3, "lastUpgradeAt": 1767900000 },
    "mine":  { "level": 1, "lastUpgradeAt": 1767800000 }
  },
  "incomePerSecond": 13,
  "decor": []
}
```

### 5.2 Building definitions

```lua
BuildingDefinitions = {
    [buildingId] = {
        id = "house",
        name = "House",
        baseIncome = 2,                   -- income/s at level 1
        upgradeCost = function(level) return 500 * (1.5 ^ level) end,
        upgradeIncome = function(level) return baseIncome * level end,
        maxLevel = 50,
        meshByLevel = { "rbxassetid://a", "rbxassetid://b", ... },
    },
}
```

```json
{
  "house": {
    "id": "house",
    "name": "House",
    "baseIncome": 2,
    "maxLevel": 50,
    "upgradeCostCurve": "exponential_1.5_base_500",
    "meshByLevel": ["rbxassetid://a1", "rbxassetid://a2", "rbxassetid://a3"]
  }
}
```

---

## 6. Leaderboard Data

Backed by `OrderedDataStore("Leaderboard_<category>")` with a weekly reset. In-memory cache refreshed every 30s.

### 6.1 Lua table structure

```lua
LeaderboardCategory = {
    id = "WeeklyHatch",
    name = "Weekly Hatch",
    resetSchedule = "weekly",             -- "weekly" | "daily" | "never"
    resetAt = 1768200000,                -- next reset timestamp
    scoreKey = "eggsHatched",            -- which PlayerData field to rank
    entries = {
        { rank = 1, userId = 111, name = "Alpha", value = 1200 },
        { rank = 2, userId = 222, name = "Beta",  value = 980  },
    },
    myRank = nil,                          -- filled for requesting player
}
```

### 6.2 JSON example

```json
{
  "id": "WeeklyHatch",
  "name": "Weekly Hatch",
  "resetSchedule": "weekly",
  "resetAt": 1768200000,
  "scoreKey": "eggsHatched",
  "entries": [
    { "rank": 1, "userId": 111, "name": "Alpha", "value": 1200 },
    { "rank": 2, "userId": 222, "name": "Beta",  "value": 980  },
    { "rank": 3, "userId": 333, "name": "Gamma", "value": 760  }
  ],
  "myRank": 12
}
```

Categories observed across analyses: `WeeklyHatch`, `WeeklyCollectionPoints`, `WeeklyCapture` (Catch a Monster); `Clicks`, `Rebirths` (Tap Simulator); `Cash` (Your Zoo, House Tycoon).

---

## 7. GamePass / DevProduct Definitions

Monetization catalog in `ReplicatedStorage.Modules.ShopData`. Server validates ownership; client uses for display.

### 7.1 GamePass

```lua
GamePasses = {
    [gamepassId] = {
        id = 1234567,                     -- Roblox gamepass product id
        key = "autoclicker",               -- internal key
        name = "Autoclicker",
        description = "Automatically taps for you while enabled.",
        priceRobux = 199,
        iconId = "rbxassetid://...",
        effect = { type = "toggle", field = "autoclicker" },
    },
    x2_taps = {
        id = 1234568,
        key = "x2_taps",
        name = "2x Taps",
        description = "Doubles all your tap income permanently.",
        priceRobux = 299,
        iconId = "rbxassetid://...",
        effect = { type = "multiplier", field = "tapMultiplier", value = 2.0 },
    },
    extra_slots = {
        id = 1234569,
        key = "extra_slots",
        name = "+3 Pet Slots",
        description = "Equip 3 more pets at once.",
        priceRobux = 499,
        effect = { type = "additive", field = "petSlots", value = 3 },
    },
}
```

### 7.2 DevProduct (consumable)

```lua
DevProducts = {
    [productId] = {
        id = 987654,
        key = "gem_pack_small",
        name = "500 Gems",
        description = "Pocket of premium gems.",
        priceRobux = 99,
        iconId = "rbxassetid://...",
        grant = { currency = "gems", amount = 500 },
    },
    gem_pack_bulk = {
        id = 987655,
        key = "gem_pack_bulk",
        name = "6,000 Gems + 1,000 Bonus",
        priceRobux = 1999,
        grant = { currency = "gems", amount = 7000 },
    },
    key_pack = {
        id = 987656,
        key = "key_pack",
        name = "10 Event Keys",
        priceRobux = 149,
        grant = { currency = "keys", amount = 10 },
    },
}
```

### 7.3 JSON example (combined)

```json
{
  "gamepasses": [
    { "id": 1234567, "key": "autoclicker", "name": "Autoclicker", "priceRobux": 199, "effect": { "type": "toggle", "field": "autoclicker" } },
    { "id": 1234568, "key": "x2_taps", "name": "2x Taps", "priceRobux": 299, "effect": { "type": "multiplier", "field": "tapMultiplier", "value": 2.0 } }
  ],
  "devproducts": [
    { "id": 987654, "key": "gem_pack_small", "name": "500 Gems", "priceRobux": 99,  "grant": { "currency": "gems", "amount": 500 } },
    { "id": 987655, "key": "gem_pack_bulk", "name": "6,000 Gems + 1,000 Bonus", "priceRobux": 1999, "grant": { "currency": "gems", "amount": 7000 } }
  ]
}
```

---

## 8. DataStore Schema (save structure, versioning, migration)

### 8.1 Save envelope

```lua
SaveEnvelope = {
    version = 5,                  -- schema version
    userId = 0,
    savedAt = 0,                  -- os.time()
    sessionLock = "uuid-or-nil",  -- for ProfileService-style locking
    data = PlayerData,            -- see §1
}
```

```json
{
  "version": 5,
  "userId": 123456789,
  "savedAt": 1767996060,
  "sessionLock": "7f3b2a-...",
  "data": { "...": "PlayerData from §1" }
}
```

### 8.2 Migration registry

```lua
Migrations = {
    [1] = function(data) data.clicks = data.clicks or 0 end,
    [2] = function(data) data.gems = data.gems or 0 end,
    [3] = function(data)
        -- v3: split cash from clicks
        data.cash = data.cash or 0
    end,
    [4] = function(data)
        -- v4: add pity system (Your Zoo addition)
        data.pityCounters = { golden = 0, rainbow = 0, secret = 0 }
    end,
    [5] = function(data)
        -- v5: add rebirth bulk + prestige points
        data.prestigePoints = data.prestigePoints or 0
    end,
}

-- On load:
local function Migrate(data)
    local from = data.version or 1
    for v = from + 1, CURRENT_VERSION do
        Migrations[v](data)
        data.version = v
    end
end
```

### 8.3 Backup schema (disaster recovery)

`DataStore("PlayerData_v5_backup")` mirrors primary with `savedAt` for reconciliation. On primary failure, server falls back to backup and flags the player for review.

---

## 9. Event / RemoteEvent Definitions

Full catalogue — see ARCHITECTURE.md §4 for the authoritative list. Here we give the schema for one example in detail.

### 9.1 RequestEggPurchase (C→S)

```lua
-- payload (client sends)
{ eggId = "acorn", count = 3 }

-- server response (via UpdatePets + UpdateCurrency events, not a return)
-- Server validates:
--   1. EggDefinitions[eggId] exists
--   2. count ∈ {1, 3} and tripleHatch allowed if count == 3
--   3. PlayerData[ currency ] ≥ cost × count
--   4. Rate limit: ≤ 5 purchases/sec
```

```json
{ "eggId": "acorn", "count": 3 }
```

### 9.2 EggHatched (S→C)

```lua
{
    eggId = "acorn",
    resultPetUid = "p_042",
    petId = "golden_squirrel",
    rarity = "Epic",
    variant = "Golden",
    isNew = true,
    indexTotal = 47,
    pityUpdate = { golden = 0, rainbow = 12, secret = 47 },
}
```

```json
{
  "eggId": "acorn",
  "resultPetUid": "p_042",
  "petId": "golden_squirrel",
  "rarity": "Epic",
  "variant": "Golden",
  "isNew": true,
  "indexTotal": 47,
  "pityUpdate": { "golden": 0, "rainbow": 12, "secret": 47 }
}
```

### 9.3 Remote function: GetPlayerData (C→S, returns)

Returns the full `PlayerData` snapshot (§1). Client caches locally and diffs against future `Update*` events.

---

## 10. Balance Curves

Tunable constants in `ReplicatedStorage.Modules.BalanceConfig` — hot-reloadable via `GlobalConfig` DataStore.

### 10.1 Lua definitions

```lua
BalanceConfig = {
    BASE_TAP_VALUE = 1,
    TAP_RATE_LIMIT_PER_SEC = 30,

    -- Egg cost scaling (ECONOMY.md §5.2)
    eggCost = function(eggsPurchased)
        return BASE_EGG_COST * (1 + eggsPurchased * 0.05)
    end,

    -- Rebirth cost (House Tycoon observed)
    rebirthCost = function(currentRebirths)
        return 1500 * (1.4 ^ currentRebirths)
    end,
    rebirthMultiplier = 2.5,        -- per rebirth
    bulkDiscount = { [1] = 0.0, [5] = 0.10, [15] = 0.20, [35] = 0.30, [70] = 0.40 },

    -- Zone unlock (ECONOMY.md §5.5)
    zoneUnlockCost = function(zoneNumber)
        return 1000 * (zoneNumber ^ 2.0)
    end,

    -- Pity thresholds (Your Zoo observed times → opens)
    pity = {
        golden  = { opens = 10,  labelSeconds = 47 },
        rainbow = { opens = 60,  labelSeconds = 287 },
        secret  = { opens = 180, labelSeconds = 887 },
    },

    -- Offline earnings (Your Zoo)
    offlineEarningsCapSeconds = 8 * 3600,    -- 8 hours
    offlineEarningsRate = 0.5,                 -- 50% of active income

    -- Reward scaling (rank-based)
    rankReward = function(rank, playerCount)
        return math.max(10, (playerCount - rank + 1) * 50)
    end,

    -- Income formula multipliers (ECONOMY.md §5.1)
    -- income = BASE × petMult × rebirthMult × zoneMult × eventMult × boostMult × gamepassMult
}
```

### 10.2 JSON example

```json
{
  "BASE_TAP_VALUE": 1,
  "TAP_RATE_LIMIT_PER_SEC": 30,
  "eggCostCurve": "BASE_EGG_COST * (1 + n * 0.05)",
  "rebirthCostCurve": "1500 * 1.4^rebirths",
  "rebirthMultiplier": 2.5,
  "bulkDiscount": { "1": 0.0, "5": 0.10, "15": 0.20, "35": 0.30, "70": 0.40 },
  "zoneUnlockCostCurve": "1000 * zoneNumber^2.0",
  "pity": {
    "golden":  { "opens": 10,  "labelSeconds": 47 },
    "rainbow": { "opens": 60,  "labelSeconds": 287 },
    "secret":  { "opens": 180, "labelSeconds": 887 }
  },
  "offlineEarningsCapSeconds": 28800,
  "offlineEarningsRate": 0.5,
  "rankRewardCurve": "max(10, (playerCount - rank + 1) * 50)"
}
```

### 10.3 Sample balance table (House Tycoon rebirth tiers observed)

| Rebirth Package | Cost ($) | $/Rebirth | Discount |
|-----------------|----------|-----------|----------|
| +1   | 1,500  | 1,500 | 0% |
| +5   | 5,500  | 1,100 | 27% |
| +15  | 15,500 | 1,033 | 31% |
| +35  | 35,500 | 1,014 | 32% |
| +70  | 70,500 | 1,007 | 33% |

---

## 11. Monetization Funnel Data

### 11.1 Conversion points (server-tracked via AnalyticsService)

```lua
FunnelEvents = {
    "join",                      -- 100%
    "first_tap",                  -- target >95%
    "first_egg_hatch",            -- target >80% (5-10 min)
    "first_rebirth",              -- target >40% (30-60 min)
    "hit_premium_barrier",        -- target >30% (1-2 hr)
    "view_shop",                  -- target >25%
    "prompt_purchase",            -- target >10%
    "first_purchase",             -- target >3%   (whale entry)
    "buy_gamepass",               -- target >2%
    "buy_devproduct",             -- target >5%   (repeatable)
    "buy_event_item",             -- target >1%   (FOMO)
    "trade_completed",            -- target >10%  (social hook)
    "d7_retention",               -- target >25%
    "d30_retention",               -- target >8%
}
```

### 11.2 Funnel event payload

```lua
{
    eventName = "first_purchase",
    userId = 123456789,
    timestamp = 1767996060,
    sessionSeconds = 5400,
    properties = {
        productId = 987654,
        priceRobux = 99,
        currencyGranted = 500,
        source = "shop_button",
        abVariant = "A",
    },
}
```

```json
{
  "eventName": "first_purchase",
  "userId": 123456789,
  "timestamp": 1767996060,
  "sessionSeconds": 5400,
  "properties": {
    "productId": 987654,
    "priceRobux": 99,
    "currencyGranted": 500,
    "source": "shop_button",
    "abVariant": "A"
  }
}
```

### 11.3 Ad placement data (optional)

```lua
AdPlacements = {
    [placementId] = {
        id = "shop_interstitial",
        surface = "ShopController",       -- which UI surface
        trigger = "shop_open",             -- event that shows ad
        cooldownSeconds = 120,
        reward = { currency = "gems", amount = 5 },  -- reward for watching
        provider = "AdService",           -- or third-party
    },
}
```

### 11.4 IAP catalog tiers (pricing psychology)

| Tier | Robux | USD equiv | Contents | Psychology |
|------|-------|-----------|----------|------------|
| Entry | 99   | $0.99   | 500 Gems | Low barrier — first purchase |
| Small | 299  | $2.99   | 2x Taps gamepass | Permanent value |
| Mid   | 499  | $4.99   | +3 Slots | Pay-to-progress |
| Large | 1999 | $19.99  | 6,000+1,000 Gems | Bulk discount (whale) |
| Mega  | 4999 | $49.99  | Event egg bundle | FOMO |

---

## 12. Quest Definitions

```lua
QuestDefinitions = {
    [questId] = {
        id = "q_daily_taps",
        type = "daily",                  -- "daily" | "weekly" | "milestone" | "event"
        name = "Tap 1,000 times",
        description = "Keep tapping!",
        target = 1000,
        metric = "totalTaps",             -- which PlayerData.stats field
        reward = { currency = "clicks", amount = 5000 },
        expiresAt = 0,                    -- 0 = no expiry for milestone
        prereq = nil,
    },
    q_milestone_rebirth5 = {
        id = "q_milestone_rebirth5",
        type = "milestone",
        name = "Reach 5 rebirths",
        target = 5,
        metric = "rebirths",
        reward = { pet = "rebirth_dragon" },
    },
}
```

```json
{
  "q_daily_taps": {
    "id": "q_daily_taps",
    "type": "daily",
    "name": "Tap 1,000 times",
    "description": "Keep tapping!",
    "target": 1000,
    "metric": "totalTaps",
    "reward": { "currency": "clicks", "amount": 5000 },
    "expiresAt": 0,
    "prereq": null
  }
}
```

---

## 13. Zone Definitions

```lua
ZoneDefinitions = {
    [zoneId] = {
        id = "forest",
        name = "Forest",
        unlockCost = 10000,               -- clicks (BalanceConfig.zoneUnlockCost)
        unlockCurrency = "clicks",
        multiplier = 1.5,                  -- zone income multiplier
        eggs = { "acorn", "forest_special" },
        spawns = { "wild_squirrel", "wild_bear" },
        skybox = "rbxassetid://...",
        ambient = Color3.fromRGB(120,180,120),
        musicId = "rbxassetid://...",
    },
}
```

```json
{
  "forest": {
    "id": "forest",
    "name": "Forest",
    "unlockCost": 10000,
    "unlockCurrency": "clicks",
    "multiplier": 1.5,
    "eggs": ["acorn", "forest_special"],
    "spawns": ["wild_squirrel", "wild_bear"],
    "skybox": "rbxassetid://4001",
    "ambient": [120,180,120],
    "musicId": "rbxassetid://5001"
  }
}
```

---

## 14. Trade Record (audit)

```lua
TradeRecord = {
    tradeId = "t_20260729_001",
    state = "Complete",                   -- Open|Negotiating|A_Confirmed|Both_Confirmed|Complete|Cancelled
    a = { userId = 111, offer = { pets = { "p_001" }, currency = { clicks = 1000 } } },
    b = { userId = 222, offer = { pets = { "p_005" }, currency = { gems = 50 } } },
    startedAt = 1767996000,
    completedAt = 1767996060,
    fee = { gems = 5 },                    -- optional sink
}
```

```json
{
  "tradeId": "t_20260729_001",
  "state": "Complete",
  "a": { "userId": 111, "offer": { "pets": ["p_001"], "currency": { "clicks": 1000 } } },
  "b": { "userId": 222, "offer": { "pets": ["p_005"], "currency": { "gems": 50 } } },
  "startedAt": 1767996000,
  "completedAt": 1767996060,
  "fee": { "gems": 5 }
}
```

---

## 15. Event Definitions (limited-time)

```lua
EventDefinitions = {
    [eventId] = {
        id = "rift_ball",
        name = "Rift Ball Event",
        type = "currency",                 -- "currency"|"egg"|"multiplier"|"milestone"
        startsAt = 1767000000,
        endsAt = 1768000000,
        bannerText = "Ends in 5D",
        rewards = { ... },
        exclusiveEggs = { "rift_egg" },
        multipliers = { luck = 2.0 },
    },
}
```

```json
{
  "rift_ball": {
    "id": "rift_ball",
    "name": "Rift Ball Event",
    "type": "currency",
    "startsAt": 1767000000,
    "endsAt": 1768000000,
    "bannerText": "Ends in 5D",
    "exclusiveEggs": ["rift_egg"],
    "multipliers": { "luck": 2.0 }
  }
}
```

---

## References

- `ARCHITECTURE.md` — system wiring for these schemas
- `ECONOMY.md` — formula derivations
- `ASSET_SPEC.md` — asset ids referenced above

*End of DATA_MODELS.md.*