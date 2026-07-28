# Reverse Engine Roblox — Technical System Architecture

**Type:** Architect-level technical handoff document
**Audience:** Full Roblox development team (server, client, UI, UX, monetization)
**Based on:** 9 reverse-engineered Roblox game analyses (Catch a Monster, Tap Simulator, Your Zoo, House Tycoon, Clicker Pet Sim, Adopt Me, Auto Eye, Grow a Country, Meme Game)
**Date:** 2026-07-29

---

## 1. Roblox Studio Project Structure

The recommended Studio hierarchy for a Roblox game that combines collector, simulator, and tycoon patterns (the three dominant genres from the analysis). Every service below is a top-level Roblox container.

```
game/
├── Workspace/
│   ├── Map/                       # Static geometry (BaseParts, MeshParts)
│   │   ├── SpawnArea/
│   │   ├── Zones/
│   │   │   ├── Zone_Starter/
│   │   │   ├── Zone_Forest/
│   │   │   └── Zone_Ice/
│   │   ├── Plots/                 # Tycoon plot templates (cloned on claim)
│   │   └── EventProps/            # Event-only decorations
│   ├── NPCs/                      # Wild monsters, quest givers
│   ├── Effects/                   # Particles, beams (server-owned)
│   └── CameraAnchors/             # CFrames for cutscenes/lobbies
│
├── ReplicatedStorage/             # ⭐ Shared by server + client (read-only to client)
│   ├── Modules/                   # Pure Lua modules (no side effects)
│   │   ├── PetData/               # Pet definitions (id, rarity, multiplier, hatch chance)
│   │   │   ├── Common.lua
│   │   │   ├── Rare.lua
│   │   │   ├── Epic.lua
│   │   │   ├── Legendary.lua
│   │   │   └── Secret.lua
│   │   ├── EggData/                # Egg definitions (cost, loot table, pity)
│   │   ├── ZoneData/               # Zone unlock costs, spawn tables
│   │   ├── ShopData/               # Shop catalog (game passes, dev products, IAP)
│   │   ├── QuestData/              # Daily / weekly / milestone quest defs
│   │   ├── BalanceConfig/          # Cost curves, reward curves, rebirth math
│   │   ├── Codes/                  # Promotional code → reward table
│   │   └── Constants/              # MAX_PETS, RARITY_COLORS, etc.
│   ├── Remotes/                    # RemoteEvents & RemoteFunctions (see §4)
│   │   ├── Events/
│   │   └── Functions/
│   ├── Assets/                     # Replicated meshes, textures, sounds
│   │   ├── Meshes/
│   │   ├── Textures/
│   │   ├── Sounds/
│   │   └── Animations/
│   ├── Shared/                     # Cross-cutting utilities
│   │   ├── Signal.lua              # Lightweight event/signal implementation
│   │   ├── Maid.lua                # Janitor/cleanup pattern
│   │   ├── FormatNumber.lua        # K/M/B/T/Qa/Qi formatting
│   │   ├── TableUtil.lua
│   │   └── Promise.lua             # Promise/A+ for async ops
│   └── Types/                      # Luau type definitions (.d.luau)
│
├── ServerScriptService/           # ⭐ Server-only scripts (authoritative)
│   ├── Main/                       # Bootstrapper — requires all server systems
│   │   └── ServerInit.server.luau
│   ├── Core/                       # Core game systems
│   │   ├── PlayerData/
│   │   │   ├── DataStoreManager.luau   # DataStoreService wrapper, retries, caching
│   │   │   ├── ProfileService.luau      # (optional 3rd party) session-locked profiles
│   │   │   ├── PlayerSession.luau       # in-memory session data + dirty flags
│   │   │   └── Migration.luau           # Save-version migration
│   │   ├── RoundManager.luau           # (if round-based) state machine
│   │   ├── LobbyManager.luau
│   │   ├── LeaderboardManager.luau     # OrderedDataStore + in-memory cache
│   │   ├── EconomyManager.luau         # Currency validation, anti-inflation
│   │   └── AntiExploit/
│   │       ├── RateLimiter.luau        # Per-player action rate caps
│   │       ├── MovementValidator.luau  # WalkSpeed/JumpHeight sanity
│   │       ├── RemoteSanitizer.luau    # Argument validation on remotes
│   │       └── ExploitReporter.luau    # Auto-ban / log to Analytics
│   ├── Systems/
│   │   ├── PetSystem.luau              # Hatch, equip, trade, inventory
│   │   ├── EggSystem.luau              # Purchase, roll, pity timer
│   │   ├── RebirthSystem.luau         # Prestige reset + multiplier
│   │   ├── ClickSystem.luau            # Server-side click validation
│   │   ├── QuestSystem.luau           # Daily/weekly/milestone tracking
│   │   ├── ShopSystem.luau            # GamePass/DevProduct handlers
│   │   ├── TradeSystem.luau           # P2P trade, escrow, confirmation
│   │   ├── CodeSystem.luau            # Promotional code redemption
│   │   ├── ZoneSystem.luau            # Unlock gating, teleport
│   │   ├── EventSystem.luau           # Limited-time events, timers
│   │   ├── TycoonSystem.luau          # Plot claim, build, produce
│   │   ├── CollectionSystem.luau      # Index/Pokédex completion
│   │   └── SocialSystem.luau           # Friend luck, invites
│   └── Services/
│       ├── DataService.luau           # Wraps DataStore + OrderedDataStore
│       ├── MessagingService.luau      # Cross-server leaderboards / events
│       ├── MarketplaceService.luau    # GamePass/DevProduct purchases
│       └── AnalyticsService.luau     # Custom event tracking
│
├── StarterPlayer/
│   ├── StarterPlayerScripts/      # Client-side code
│   │   ├── Main/
│   │   │   └── ClientInit.client.luau
│   │   ├── Controllers/
│   │   │   ├── UIController.luau       # Manages all ScreenGuis
│   │   │   ├── InputController.luau    # Tap/click detection, mobile
│   │   │   ├── PetController.luau     # Pet following, equip visuals
│   │   │   ├── CameraController.luau
│   │   │   ├── ZoneController.luau     # Zone transitions, loading
│   │   │   ├── TradeController.luau    # Trade window UI flow
│   │   │   ├── ShopController.luau     # Shop UI + IAP prompts
│   │   │   ├── QuestController.luau
│   │   │   └── AudioController.luau
│   │   └── Utils/
│   │       ├── RemoteListener.luau    # Centralized remote event wiring
│   │       ├── TweenUtil.luau
│   │       └── Notification.luau
│   └── StarterCharacterScripts/
│       ├── Movement.client.luau       # Mobile-optimized controls
│       └── Ragdoll.client.luau        # Physics comedy (viral formula)
│
├── StarterGui/                   # UI templates (auto-cloned to client)
│   ├── HUD.gui                   # Currency displays, buttons
│   ├── Shop.gui
│   ├── Trade.gui
│   ├── Rebirth.gui
│   ├── EggHatch.gui
│   ├── Inventory.gui
│   ├── Quests.gui
│   ├── Leaderboard.gui
│   ├── EventPopup.gui
│   ├── DailyReward.gui
│   └── Notifications.gui
│
├── StarterPack/                  # Tools in player backpack (if any)
│   ├── CaptureTool.tool
│   └── EggOpener.tool
│
├── Lighting/                     # Atmosphere, Sky, post-processing
├── SoundService/                 # Group/SoundGroups for mixing
├── ReplicatedFirst/              # Loading screen assets
│   └── LoadingScreen.gui
└── TestService/                  # Automated test runner
```

**Naming convention:** PascalCase for instances, camelCase for locals, snake_case for data keys. `*.server.luau` = server-only, `*.client.luau` = client-only, `*.luau` = shared module.

---

## 2. System Architecture — Client-Server Model

Roblox enforces a strict **client-server boundary**. The server is authoritative for all gameplay state and persistence. Clients are renderers and input senders; they never own truth.

### 2.1 High-Level Data Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                              SERVER                                  │
│  ┌───────────────┐   ┌──────────────┐   ┌──────────────────────┐    │
│  │ PlayerSession │──▶│ SystemManager│──▶│ PetSystem/EggSystem/ │    │
│  │  (per-player  │   │  (orchestr.) │   │ RebirthSystem/...    │    │
│  │   in-memory)  │   │              │   │                      │    │
│  └──────┬────────┘   └──────┬───────┘   └──────────┬───────────┘    │
│         │                   │                      │                  │
│         ▼                   ▼                      ▼                  │
│  ┌───────────────┐   ┌──────────────┐   ┌──────────────────────┐    │
│  │ DataStoreMgr  │   │ Leaderboard  │   │  AntiExploit /       │    │
│  │ (save/load,   │   │ (OrderedDStore│  │  RateLimiter         │    │
│  │  retry, cache)│   │  + cache)     │   │                      │    │
│  └───────────────┘   └──────────────┘   └──────────────────────┘    │
│         ▲                                                              │
│         │                                                              │
└─────────┼──────────────────────────────────────────────────────────────┘
          │  RemoteEvents (fire) / RemoteFunctions (invoke)
          │
┌─────────┼──────────────────────────────────────────────────────────────┐
│         │                          CLIENT                                │
│  ┌──────▼────────┐   ┌──────────────────┐   ┌────────────────────┐     │
│  │ RemoteListener│──▶│ Controllers      │──▶│ UIController        │     │
│  │ (event router)│   │ (Input, Pet,     │   │ (ScreenGuis, HUD,   │     │
│  │               │   │  Camera, Zone...) │   │  Shop, Trade, ...)   │     │
│  └───────────────┘   └──────────────────┘   └────────────────────┘     │
│         ▲                                                              │
│         │ player input (tap, click, UI button)                          │
└─────────┼──────────────────────────────────────────────────────────────┘
          ▼
       Player (human)
```

### 2.2 Authority Rules (non-negotiable)

| Concern | Server-authoritative? | Rationale |
|---------|------------------------|-----------|
| Currency balances | ✅ Yes | Clients cannot mint currency |
| Pet ownership / rarity | ✅ Yes | Prevent forged pets |
| Egg hatch results | ✅ Yes | Roll on server, send result |
| Rebirth state / multiplier | ✅ Yes | Prestige integrity |
| Trade execution | ✅ Yes | Escrow prevents dupes |
| Leaderboard writes | ✅ Yes | OrderedDataStore only |
| Zone unlocks | ✅ Yes | Gating integrity |
| Player movement | Partial | Server validates bounds/teleports, client predicts |
| UI state | ❌ Client | Pure visual; server never trusts UI claims |
| Cosmetic effects | ❌ Client | Predict for responsiveness; server may echo |
| Tap input detection | ❌ Client (detection) → ✅ Server (validation) | Client detects, server validates rate + value |

---

## 3. Core Game Systems

### 3.1 Round Manager (for round-based game types)

State machine observed in Slappy Seals analysis: `WaitingForPlayers → MatchStarting → Countdown → InProgress → RoundEnd → Rewards → Lobby`.

```lua
-- RoundManager.luau (server)
local STATES = { WaitingForPlayers=1, MatchStarting=2, Countdown=3, InProgress=4, RoundEnd=5, Rewards=6 }
local state = STATES.WaitingForPlayers
local players = {}
local roundConfig = require(ReplicatedStorage.Modules.RoundConfig)

while true do
    if state == STATES.WaitingForPlayers then
        -- collect players until MIN_PLAYERS or timeout
    elseif state == STATES.Countdown then
        -- 3..2..1 announce via RemoteEvent
    elseif state == STATES.InProgress then
        -- tick gameplay, enforce time limit, shrink zone, spawn sharks
    elseif state == STATES.RoundEnd then
        -- determine winner, compute rewards, fire Rewards state
    end
    task.wait(1/30)
end
```

| Config field | Example | Source |
|--------------|---------|--------|
| MIN_PLAYERS | 2 | Slappy Seals: 8-player royale |
| MAX_PLAYERS | 16 | Round cap |
| ROUND_DURATION_S | 90-180 | Viral formula: short rounds |
| PLATFORM_SHRINK | 70x70 over 2.5s | Slappy Seals observed |
| SHARK_SPAWN_AT_S | 90 | Slappy Seals observed |

### 3.2 Lobby Manager

- Holds players in a lobby Zone; teleports to match arena on round start
- Handles spectating after elimination
- Provides pre-round shop UI (buy eggs, equip pets)
- Friend/party grouping (SocialSystem integration)

### 3.3 Leaderboard Manager

- **Weekly leaderboards** (Catch a Monster pattern): `WeeklyHatch`, `WeeklyCollectionPoints`, `WeeklyCapture`
- Backed by `OrderedDataStore` with one entry per category per player
- In-memory cache refreshed every N seconds; writes batched to avoid throttle (OrderedDataStore has 60+ sec write cooldown)
- Reset timer: weekly cron via `os.time()` modulo week
- Categories from analysis: `Clicks`, `Cash`, `Rebirths`, `HatchCount`, `CollectionPoints`, `CaptureCount`

### 3.4 Datastore (see §6)

### 3.5 Monetization (see §11)

---

## 4. RemoteEvents & RemoteFunctions

Roblox remotes are the only sanctioned cross-boundary channel. All remotes live under `ReplicatedStorage.Remotes`. **Server validates every argument** — clients are untrusted.

### 4.1 RemoteEvents (client → server, fire-and-forget)

| Event | Direction | Payload | Server validation |
|-------|-----------|---------|-------------------|
| `RequestTap` | C→S | `{combo=1}` | Rate cap (e.g. 30/s), combo sanity |
| `RequestEggPurchase` | C→S | `{eggId="acorn", count=1}` | Egg exists, count ≤ 3, player has currency |
| `RequestHatch` | C→S | `{eggId="acorn"}` | Player owns egg, roll on server |
| `RequestEquipPet` | C→S | `{petUid="uuid"}` | Pet owned, slot free |
| `RequestUnequipPet` | C→S | `{petUid="uuid"}` | Pet equipped |
| `RequestRebirth` | C→S | `{bulkCount=1}` | Meets threshold, bulk ≤ cap |
| `RequestZoneUnlock` | C→S | `{zoneId="forest"}` | Meets click/cash gate |
| `RequestZoneTeleport` | C→S | `{zoneId="forest"}` | Zone unlocked |
| `RequestTradeInit` | C→S | `{targetUserId=123}` | Target online, not in trade |
| `RequestTradeOffer` | C→S | `{tradeId, offerPets=[], offerCurrency=0}` | Items owned, trade active |
| `RequestTradeAccept` | C→S | `{tradeId}` | Both sides confirmed |
| `RequestTradeCancel` | C→S | `{tradeId}` | Trade active |
| `RequestCodeRedeem` | C→S | `{code="SUMMER2026"}` | Code valid, not yet redeemed |
| `RequestQuestClaim` | C→S | `{questId="q_daily_1"}` | Quest complete, unclaimed |
| `RequestClaimPlot` | C→S | `{plotId=4}` | Plot unowned, max 1 plot |
| `RequestBuildUpgrade` | C→S | `{plotId, buildingId, upgradeIdx}` | Plot owned, currency sufficient |
| `RequestCollectAll` | C→S | `{}` | Rate cap (Zoo pattern) |
| `RequestSellPet` | C→S | `{petUid="uuid"}` | Pet owned, not equipped |
| `ReportClientInfo` | C→S | `{fps=60, ping=80}` | Analytics only, no gameplay effect |

### 4.2 RemoteEvents (server → client)

| Event | Direction | Payload | Notes |
|-------|-----------|---------|-------|
| `UpdateCurrency` | S→C | `{clicks=1234, gems=5, rebirths=2}` | Push authoritative balances |
| `UpdatePets` | S→C | `{equipped=[...], inventory=[...]}` | Full inventory resync |
| `EggHatched` | S→C | `{eggId, resultPetUid, rarity, variant}` | Trigger hatch VFX |
| `RebirthComplete` | S→C | `{newRebirths=3, newMultiplier=6.25}` | Trigger rebirth VFX |
| `PityUpdate` | S→C | `{golden=3, rainbow=12, secret=47}` | Zoo pattern countdown UI |
| `QuestProgress` | S→C | `{questId, current, target}` | Live progress bar |
| `LeaderboardUpdate` | S→C | `{category, entries=[{rank, name, value}]}` | Refreshed cache |
| `RoundState` | S→C | `{state, timeLeft, playersAlive}` | Round manager broadcasts |
| `AnnounceEvent` | S→C | `{title, body, duration}` | Event popups |
| `TradeUpdate` | S→C | `{tradeId, state, myOffer, theirOffer}` | Trade window sync |
| `Notify` | S→C | `{text, kind="info"/"warn"/"reward"}` | Toast notifications |
| `TeleportPlayer` | S→C | `{zoneId}` | Trigger client-side teleport |

### 4.3 RemoteFunctions (bidirectional, await response)

| Function | C→S request | S→C response | Notes |
|----------|-------------|--------------|-------|
| `GetPlayerData` | `{}` | full PlayerData snapshot | On join / reconnect |
| `GetShopCatalog` | `{}` | shop catalog table | Cache on client |
| `GetLeaderboard` | `{category}` | top-N entries | With fallback cache |
| `GetPetDefinition` | `{petId}` | PetData row | For UI tooltips |
| `PurchaseDevProduct` | `{productId}` | `{ok, granted}` | Wraps MarketplaceService.ProcessReceipt |

---

## 5. Pet / Collection System Architecture

The pet/gacha system is the dominant engagement driver across all 9 analyzed games. Architecture below supports Hatch, Inventory, Equip, Trade, Index, Pity, and Variant (Rainbow/Golden/Glitch).

### 5.1 Component Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                            SERVER                                   │
│                                                                    │
│   EggSystem ──rolls──▶ PetSystem ──issues──▶ PlayerSession.pets[]  │
│       │                   │                        │                │
│       │                   │                        │                │
│   PetData (defs)     PityTracker            Inventory / EquipSlots  │
│       │                   │                        │                │
│       ▼                   ▼                        ▼                │
│   LootTable          pityCounters[]           TradeSystem (escrow)   │
│   (chances)          (golden/rainbow/secret)                         │
│                                                                    │
│                       CollectionSystem ◀─── index[] completion      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
        ▲ RemoteEvents: RequestEggPurchase, RequestHatch, RequestEquipPet
        ▲ RemoteEvents: EggHatched, UpdatePets, PityUpdate
        ▼
┌────────────────────────────────────────────────────────────────────┐
│                            CLIENT                                   │
│   EggController (hatch VFX, rarity reveal)                         │
│   PetController (follow player, render variants, auras)             │
│   InventoryController (grid UI, drag/equip, sell)                   │
│   TradeController (offer panels, confirm countdown)                 │
│   IndexController (Pokédex grid, completion %, rewards)             │
└────────────────────────────────────────────────────────────────────┘
```

### 5.2 Hatch flow (server-authoritative)

```
1. Client → RequestEggPurchase{eggId, count}
2. Server: validate currency, decrement, grant EggInstance{uid, eggId, opened=false}
3. Server → UpdateCurrency, UpdatePets (egg added)
4. Client → RequestHatch{eggId} (or auto-hatch)
5. Server:
   a. Load EggData.lootTable
   b. Apply pity: if pityCounter ≥ threshold → force tier; else roll RNG
   c. Roll variant (Rainbow/Golden/Glitch) per variantChance
   d. Create PetInstance{uid, petId, variant, stats}
   e. Increment pityCounters, reset on guaranteed
   f. Add to PlayerSession.pets, mark dirty for save
   g. Add to index.discovered (if new species)
6. Server → EggHatched{resultPetUid, rarity, variant}
7. Client: play hatch animation, reveal rarity with color/aura, add to inventory UI
```

### 5.3 Pet following (client-side, server-tolerant)

- Pet model is owned by client (`NetworkOwnership` set to player)
- `PetController` lerps pet CFrame toward player root part each frame
- Server does **not** simulate pet position (perf budget) but validates pets are owned before spawn
- Equipped pets contribute `tapBoost` / `passiveBoost` to server-side income calc

### 5.4 Trade flow (escrow pattern, anti-dupe)

```
1. A → RequestTradeInit{B}     Server creates Trade{tradeId, A, B, state=Open, offers={}}
2. Server → TradeUpdate to both A and B
3. B → RequestTradeInit{A} (accept)    state=Negotiating
4. A → RequestTradeOffer{tradeId, pets=[], currency=0}
   Server validates each petUid is owned by A and not already offered; locks those pets (cannot be equipped/sold during trade)
5. B → RequestTradeOffer{...}  same validation for B
6. A → RequestTradeAccept{tradeId}    state=A_Confirmed
7. B → RequestTradeAccept{tradeId}    state=Both_Confirmed
8. Server executes atomic swap: reassign ownership, move currency, unlock
9. Server → TradeUpdate{state=Complete} to both; UpdatePets to both
```

**Anti-dupe:** pets are locked the moment they are offered; trade is single-writer (server); no parallel trades of the same pet.

---

## 6. Tycoon / Build System Architecture

Observed in House Tycoon and Your Zoo. Pattern: claim plot → place buildings → upgrades raise income → rebirth multiplies.

### 6.1 Plot Claiming

- Server maintains `Plots[1..N]` with `{ownerUserId=nil, level=1, buildings={}}`
- `RequestClaimPlot{plotId}` → first-claim wins; one plot per player
- Plot template is a `Model` in `Workspace.Plots` cloned/assigned on claim; owner gets build permissions on that plot's parts

### 6.2 Building & Upgrades

```
┌────────────────────────────────────────────────────────────────┐
│  TycoonSystem (server)                                          │
│    Plots[plotId] = { owner, level, buildings={} }               │
│                                                                 │
│  RequestBuildUpgrade{plotId, buildingId, upgradeIdx}            │
│    1. Validate plot owned by caller                             │
│    2. Validate buildingId in BuildingData                       │
│    3. Validate upgradeIdx is next sequential upgrade            │
│    4. Validate currency ≥ upgradeCost(currentLevel)             │
│    5. Decrement currency, apply upgrade (new income, new model) │
│    6. Update plot visual: swap MeshPart, play build VFX         │
│    7. Mark session dirty                                        │
└────────────────────────────────────────────────────────────────┘
```

### 6.3 Production / Income

- Each plot has `incomePerSecond = Σ(building.income × building.level) × plotMultipliers`
- Server ticks production every 1s (or 0.5s) — accumulates into `PlayerSession.cash`
- `Auto Collect` gamepass toggles auto-claim (House Tycoon pattern: 99x remaining)
- Offline earnings (Your Zoo): on rejoin, compute `elapsed = now - lastLogin`, `offlineCash = min(incomePerSecond × elapsed, cap)`

---

## 7. Simulator / Clicker System Architecture

Pattern from Tap Simulator, Clicker Pet Sim, House Tycoon.

### 7.1 Click income formula (server-side)

```
income_per_tap = BASE_TAP
              × Σ(equipped_pet.tapBoost)
              × rebirthMultiplier           -- 2.5^rebirths (House Tycoon)
              × zoneMultiplier              -- current zone bonus
              × eventMultiplier              -- active event
              × boostMultiplier              -- x2 Cash pass, temporary boosts
              × gamepassMultiplier           -- x2 Taps pass
```

### 7.2 Rebirth

```
rebirth_cost(n) = BASE_REBIRTH_COST × GROWTH^(n)   -- House Tycoon observed bulk tiers
multiplier       = 2.5^rebirths                    -- observed 2.5x per rebirth

bulk_cost(k) = Σ(rebirth_cost(n+i) for i in 0..k-1) × (1 - bulkDiscount(k))
  k=1  → $1,500 / rebirth   (no discount)
  k=5  → $1,100 / rebirth
  k=15 → $1,033 / rebirth
  k=35 → $1,014 / rebirth
  k=70 → $1,007 / rebirth
```

### 7.3 Autoclicker

- Gamepass-gated; client sends `RequestTap` at the autoclick rate (server caps at e.g. 20/s)
- Server validates the gamepass is owned and the rate is within cap
- Idle income displayed as `X/s` (Tap Simulator pattern)

### 7.4 Zone progression

```
zone_unlock_cost(zoneId) = BASE_ZONE_COST × zoneNumber^ZONE_SCALING
```
Zones gate content (better eggs, higher multipliers) — observed in Tap Simulator (Forest, Island Portals) and Catch a Monster (World Portal, biome islands).

---

## 8. Data Persistence

### 8.1 DataStoreService usage

| Store | Type | Purpose |
|-------|------|---------|
| `PlayerData_v{N}` | DataStore | Per-player save (see DATA_MODELS.md) |
| `Leaderboard_<category>` | OrderedDataStore | Weekly leaderboard entries |
| `GlobalConfig` | DataStore | Live-tunable balance constants |
| `BannedPlayers` | DataStore | Anti-exploit bans |
| `TradeLog` | DataStore (optional) | Audit trail of trades |

### 8.2 Session data + caching

```
OnPlayerJoin:
  1. DataStoreManager:LoadAsync(userId) → saveData (or default)
  2. Migration:Apply(saveData, fromVersion, toVersion)
  3. PlayerSession[userId] = saveData  -- in-memory authoritative copy
  4. Apply gamepass multipliers, zone state, equipped pets
  5. RemoteFunction GetPlayerData → client snapshot

During session:
  - All mutations happen on PlayerSession (never read directly from DataStore mid-session)
  - Dirty flags mark which sub-tables changed
  - Auto-save every 60s (background task) + on PlayerRemoving + on critical events (rebirth, trade)

OnPlayerRemoving:
  1. Final PlayerSession → saveData
  2. DataStoreManager:SaveAsync(userId, saveData) with retry/backoff
  3. Release OrderedDataStore entries (deferred)
  4. Clear PlayerSession[userId]
```

### 8.3 Concurrency & safety

- Use **session locking** (ProfileService pattern) to prevent duplicate-session dupes
- `UpdateAsync` over `SetAsync` for conflict resolution
- Retry with exponential backoff on `DataStoreService` errors
- Backup writes to a secondary DataStore on failure (disaster recovery)

### 8.4 Versioning & migration

- `saveData.version = N` (integer). Migration registry: `Migrations[v1→v2]`, `Migrations[v2→v3]`, etc.
- Migrations run on load; never mutate on save
- Old accounts get default fields filled; removed fields purged

---

## 9. Anti-Exploit Design

### 9.1 Principles

1. **Server authority** — never trust a client claim about gameplay state
2. **Validate, then trust** — every remote's payload validated before mutation
3. **Rate-limit** — every player action has a per-second cap
4. **Sanity-check** — values must be in expected ranges (e.g. rebirth count ≤ 10,000)
5. **Log, don't crash** — invalid input logs + flags player; server continues

### 9.2 Rate limits (example)

| Action | Cap | Action on violation |
|--------|-----|---------------------|
| Tap | 30/s | Drop excess, warn at 3 strikes |
| Egg purchase | 5/s | Drop excess |
| Trade init | 1/2s | Drop excess |
| Code redeem | 1/10s | Drop excess |
| Quest claim | 2/s | Drop excess |
| Plot claim | 1/5s | Drop excess |

### 9.3 Movement validation

- Server tracks expected position from last teleport / spawn
- If `|clientPos - expectedPos| > MAX_DRIFT` for sustained period → flag, rubberband
- `WalkSpeed` / `JumpHeight` enforced server-side; client changes reverted
- Teleport only via server-authorized `RequestZoneTeleport`

### 9.4 Economy exploits

- Currency deltas computed server-side only; client requests are intentions, not results
- Trade uses escrow + lock (see §5.4) — no parallel use of offered pets
- DevProduct grants gated behind `MarketplaceService.ProcessReceipt` idempotency
- Refund/rollback path for failed grants

### 9.5 Detection & response

- Anomaly scoring per player (currency gained vs actions, pet rarity vs opens)
- Auto-flag for review at threshold; auto-ban for clear exploits (e.g. negative currency)
- `ExploitReporter` sends to Analytics + optional Discord webhook

---

## 10. Performance Budget

Targeting 60 FPS on mid-tier mobile (the dominant Roblox platform per all analyses).

### 10.1 Part / instance budget

| Resource | Budget | Notes |
|----------|--------|-------|
| BaseParts in Workspace | ≤ 8,000 | Use StreamingEnabled; anchor everything static |
| MeshParts | ≤ 2,000 | Reuse mesh + recolor via `Color3`, not new meshes |
| Decals/Textures | ≤ 1,500 | Atlas where possible |
| ParticleEmitters active | ≤ 200 | Pool emitters; cap concurrent hatches |
| Sounds playing | ≤ 32 | SoundGroups for mixing; cap SFX spam on taps |
| Humanoids | ≤ 60 | One per NPC + pet; cap wild spawns |
| Concurrent RemoteEvent fires/s | ≤ 100/server | Batch currency updates |

### 10.2 Script overhead

- Server tick budget: 16ms/frame (60Hz). Click validation + economy tick must fit in 4ms.
- Use `task.wait()` not `wait()`; use `RunService.Heartbeat` for fixed-rate systems.
- Avoid per-frame table allocation; pool objects.
- Client rendering budget: ≤ 10ms/frame for non-Roblox work.

### 10.3 Network

- RemoteEvent payload ≤ 1KB; batch where possible
- Avoid sending full inventory on every change — send deltas
- Throttle `UpdateCurrency` to ≤ 5/s per player (client-side interpolation smooths display)
- StreamingEnabled: only stream parts near player; reduces replication

### 10.4 Memory

- Per-player session ≤ 50KB serialized
- Client GUI pooled; do not destroy/recreate ScreenGuis per action
- Pet models pooled; cap rendered pets to N nearest

---

## 11. Module Dependency Graph

```
                          ┌──────────────┐
                          │  ServerInit  │  (bootstrapper)
                          └──────┬───────┘
                                 │
        ┌────────────┬──────────┼───────────┬─────────────┐
        ▼            ▼          ▼           ▼             ▼
   DataStoreMgr  PlayerSession  Systems*  AntiExploit  LeaderboardMgr
        │            │           │           │             │
        │            │     ┌─────┴─────┐     │             │
        │            │     ▼           ▼     │             │
        │            │  PetSystem  EggSystem │             │
        │            │     │           │     │             │
        │            │     ▼           ▼     │             │
        │            │  TradeSys  RebirthSys │             │
        │            │     │           │     │             │
        │            │     ▼           ▼     │             │
        │            │  ShopSys  QuestSystem │             │
        │            │     │           │     │             │
        │            ▼     ▼           ▼     ▼             ▼
        └──────▶ DataService ◀── MessagingService ◀─ MarketplaceService
                              ▲
                              │
                       ReplicatedStorage.Modules
                       (PetData, EggData, ShopData,
                        QuestData, BalanceConfig, Codes)
```

`Systems*` = the set of feature systems in `ServerScriptService.Systems`. Each system declares its dependencies via a `require()` graph; `ServerInit` wires them up in dependency order.

---

## 12. Signal / Event Flow Diagrams

### 12.1 Tap → income flow

```
[Player taps]
   │
   ▼
Client InputController: detect tap, fire RequestTap
   │
   ▼ RemoteEvent
Server ClickSystem: validate rate, compute income formula, +currency
   │
   ├─▶ PlayerSession.clicks += income
   ├─▶ dirty flag set
   └─▶ RemoteEvent UpdateCurrency → client HUD updates
                              │
                              ▼
                  Client HUD animates +N floating text
```

### 12.2 Egg hatch flow (full)

```
[Player taps Buy Egg]
   │
   ▼ RequestEggPurchase{eggId, count=3}
Server EggSystem:
   1. validate currency ≥ cost×3
   2. decrement currency
   3. create 3 EggInstances, push to PlayerSession.pets (as eggs)
   4. RemoteEvent UpdateCurrency + UpdatePets
   │
   ▼ Client: 3 eggs appear in inventory
[Player taps Hatch]
   │
   ▼ RequestHatch{eggId} (×3 or triple)
Server EggSystem:
   5. load loot table, apply pity, roll rarity, roll variant
   6. create PetInstance, add to pets + index
   7. update pityCounters; reset on guaranteed
   8. RemoteEvent EggHatched{result, rarity, variant} + PityUpdate
   │
   ▼ Client: play hatch VFX, reveal rarity color, pet joins follow
```

### 12.3 Rebirth flow

```
[Player taps Rebirth]
   │
   ▼ RequestRebirth{bulkCount=5}
Server RebirthSystem:
   1. validate meets threshold (clicks ≥ sum of costs)
   2. validate bulkCount ≤ MAX_BULK
   3. compute total cost with bulk discount
   4. decrement clicks to 0 (or to remainder)
   5. rebirths += bulkCount
   6. recompute multiplier = 2.5^rebirths
   7. reset zone state per rebirth rules (keep pets? keep collection?)
   8. RemoteEvent RebirthComplete{newRebirths, newMultiplier}
   │
   ▼ Client: rebirth VFX, multiplier popup, HUD refresh
```

### 12.4 Trade flow (already detailed in §5.4 — escrow with lock/unlock).

---

## 13. Monetization Integration Points

### 13.1 Integration points in the architecture

| Point | System | Trigger | Effect |
|-------|--------|---------|--------|
| GamePass check | PlayerSession load | On join | Apply permanent multipliers (x2 Taps, x2 Luck, Autoclicker, Extra Slots) |
| DevProduct purchase | ShopSystem + MarketplaceService.ProcessReceipt | Player clicks Buy | Grant gems/keys/eggs; idempotent receipt |
| Robux IAP | ShopController → Server | Buy button | `MarketplaceService:PromptProductPurchase` |
| GamePass IAP | ShopController → Server | Buy button | `MarketplaceService:PromptGamePassPurchase` |
| Limited-time offer | EventSystem timer | Timer fires | Surface bundle UI with countdown (Zoo Starter Pack 9m47s pattern) |
| Code redemption | CodeSystem | Player enters code | Grant currency/items, mark used |
| Ad placement (optional) | ShopController | Ad surface | `AdService` or third-party |
| Trading fee (optional) | TradeSystem | Trade complete | % gem fee to sink |

### 13.2 Conversion funnel (server-tracked)

```
Join → First tap (immediate gratification)
   → First egg hatch (5-10 min)            [first dopamine]
   → First rebirth (30-60 min)             [prestige hook]
   → Encounter premium barrier (1-2 hr)    [F2P slowdown]
   → Buy first pack ($0.99 entry)          [conversion]
   → Buy gamepass                           [consistent revenue]
   → Buy premium eggs                       [whale path]
   → Buy event exclusives                   [FOMO spend]
```

Every transition logged to AnalyticsService for funnel optimization. See DATA_MODELS.md §Monetization Funnel for the schema.

---

## 14. Build Order (Recommended)

1. **MVP core loop** — tap → currency → egg → pet → equip → multiplier
2. **Persistence** — DataStoreManager + PlayerSession + auto-save
3. **Rebirth** — prestige reset + multiplier
4. **Zones** — unlock gating + teleport
5. **Shop + monetization** — GamePass + DevProduct + IAP prompts
6. **Quests** — daily + milestone
7. **Trading** — escrow + UI
8. **Leaderboards** — OrderedDataStore + weekly reset
9. **Events** — limited-time eggs, timers, FOMO
10. **Anti-exploit hardening** — rate limits, validation, bans
11. **Polish** — VFX, audio, ragdolls (viral formula), mobile optimization

---

## 15. References

- `GAME_MECHANICS.md` — genre taxonomy, core loops
- `ECONOMY.md` — currency architecture, balance formulas
- `DATA_MODELS.md` — companion document with all schemas
- `ASSET_SPEC.md` — companion document with full asset list
- `raw-data/*/GAME_ANALYSIS.md` — per-game source analyses

---

*End of ARCHITECTURE.md — handoff to server, client, UI, and monetization engineers.*