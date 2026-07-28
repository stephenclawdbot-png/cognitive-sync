# BlockFall.io — Backend & API Study

> Source: https://blockfall.io (production at blockfall-game-production.up.railway.app)
> Studied: homepage HTML, production JS bundles (Turbopack chunks), live API probing
> Date: 2025

## Overview

BlockFall is a Skyblock MMO on Solana. Players stake $BLOCK tokens to power "Box Machines" that produce Lucky Boxes containing collectible blocks of varying rarity. Players place blocks on their sky-island, trade on a P2P market, and climb leaderboards.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (Turbopack, app router, RSC) + React + Three.js (WebGL voxel renderer) |
| 2D blocks | CSS 3D transforms (rotateZ/rotateX cube faces) for isometric previews |
| Backend | Next.js API routes (server-side) |
| Hosting | Railway.app (blockfall-game-production.up.railway.app) |
| Blockchain | Solana ($BLOCK SPL token) |
| Textures | Pixel art PNGs from `/textures/blocks/` and `/textures/ui/` |
| Fonts | "Press Start 2P" + "Silkscreen" (Google Fonts) |
| Theme | #070a1c (dark navy) |

## Token

- **$BLOCK** — SPL token on Solana
- Contract: `GKUwfyQoJ9apCaoWyYaQ9RT8inZed469v41M1Ljb1ock`
- Twitter: @BlockFallX

## Game Loop

1. Player connects Solana wallet
2. Stake $BLOCK to activate a Box Machine (0 for free tier, up to 1M for Mythic)
3. Machine produces a Lucky Box every 12-15 minutes
4. Open box → reveals a collectible block of varying rarity
5. Place block on island / sell on market / climb leaderboards
6. Stake locked 24h, returned in full (not spent)
7. Daily quests give additional rewards
8. XP/leveling system with diminishing returns

## Generator (Box Machine) Tiers

| Tier | Name | Stake ($BLOCK) | Box Interval |
|---|---|---|---|
| 1 | Free (Cobblestone) | 0 | 15 min |
| 2 | Common | 12,500 | ~14 min |
| 3 | Uncommon | 50,000 | ~13 min |
| 4 | Rare | 100,000 | ~12 min |
| 5 | Epic | 250,000 | ~12 min |
| 6 | Legendary | 500,000 | ~12 min |
| 7 | Mythic | 1,000,000 | ~12 min |

## Rarity Tiers

| Tier | Name | Color | Drop Rate (Rare machine) |
|---|---|---|---|
| 1 | Common | #9aa0a6 | 33.1% |
| 2 | Uncommon | #5fcf6a | 12.6% |
| 3 | Rare | #4aa3ff | — |
| 4 | Epic | #b06bff | — |
| 5 | Legendary | #f5b53d | — |
| 6 | Mythic | #ff5a7a | 54.3% (rare-or-better) |
| 7 | Special | #ffe14d | — |

## Block Types (100+)

From the JS bundle, blocks include:
- **Basic**: grass_block, dirt, stone, cobblestone, sand, gravel, oak_log, leaves, chest
- **Building**: bricks, stone_bricks, cobblestone_mossy, planks_oak, glass, terracotta, bookshelf, crafting_table, furnace
- **Ores**: coal_ore, iron_ore, copper_ore, gold_ore, diamond_ore, emerald_ore, lapis_ore, redstone_ore (+ deepslate variants)
- **Blocks**: coal_block, iron_block, gold_block, diamond_block, emerald_block, lapis_block, redstone_block, netherite_block, quartz_block, obsidian
- **Special**: dragon_egg, beacon, command_block, end_portal_frame, enchanting_table, ender_chest, bedrock, lucky_box, tnt
- **Wool**: white, red, blue, green, black, pink
- **Nether**: netherrack, blackstone, nether_bricks, quartz_bricks, ancient_debris
- **Decor**: torch, rose, allium, cactus, ice, sea_lantern, glowstone, slime_block, jukebox

Each block has a `baseValue` (in $BLOCK) and a `tier` (1-7).

## Voxel World System

- Chunk size: 16x16 columns
- Y range: -64 to 191 (256 blocks tall)
- Render distance: 8 chunks
- Chunks gzip-compressed for network transfer
- Blocks encoded as Uint8 indices into a block palette
- 255 = bedrock (unbreakable), 230 = water, 0 = air
- Oriented blocks (torch, furnace, chest, etc.) use directional sub-IDs

## Inventory System

- 175 total slots (7 hotbar + 56 backpack + overflow)
- Max stack size: Infinity (stacks unlimited)
- Hotbar slots 168-174 (bottom row), backpack 0-167

## XP & Leveling

- Exponential level curve: `base_xp * growth^level`
- Diminishing returns for repeated actions (metered)
- XP orbs animate from action point to counter
- Level-up triggers visual effects

---

## API Endpoints

### Public (No Auth)

#### `GET /api/market`
Returns market listings and stats. Supports query params:
- `?tier=N` — filter by rarity tier (1-7)
- `?sort=price_asc` — cheapest first
- `?sort=price_desc` — most expensive first
- `?limit=N` — limit results

**Response:**
```json
{
  "stats": {
    "totalSales": 18624,
    "volume": 6938613,
    "avgSale": 373,
    "activeListings": 158524
  },
  "listings": [
    {
      "id": "uuid",
      "itemType": "coal_block",
      "quantity": 1,
      "price": 290,
      "sellerHandle": "username",
      "sellerWallet": "SOL_WALLET_ADDRESS",
      "name": "Block of Coal",
      "baseValue": 290,
      "tier": 3,
      "tierColor": "#4aa3ff"
    }
  ]
}
```

**Live market data (sampled):**
- Total sales: 18,624
- Total volume: 6,938,613 $BLOCK
- Avg sale: 373 $BLOCK
- Active listings: ~159,000
- Most expensive: Ender Chest (298k), Dragon Egg (200k), Bedrock (138k), Command Block (160k)
- Cheapest: Dirt (5), Stone (25)

### Auth-Required (Solana Wallet — 401 without)

#### `GET /api/me`
Player profile + inventory.
```json
{ "inventory": [{ "itemType": "stone", "quantity": 5 }] }
```

#### `GET /api/economy`
Economy state, level, XP, generators, boxes.
```json
{ "level": { "xp": 12345, "rate": 1.0 } }
```

#### `POST /api/economy/generator/activate`
Activate (stake) a generator.
```json
// Request:
{ "generatorId": 1, "lockAccount": "...", "signature": "..." }
```

#### `POST /api/economy/generator/unstake`
Unstake from a generator (24h lock).
```json
{ "generatorId": 1 }
```

#### `POST /api/economy/box/open`
Open one Lucky Box.

#### `POST /api/economy/box/open-all`
Open all pending Lucky Boxes.

#### `POST /api/economy/box/accelerate`
Boost box production (costs $BLOCK).
```json
{ "signature": "...", "count": 1 }
```

#### `POST /api/economy/inventory/consume`
Place a block (consume from inventory).
```json
{ "itemId": "stone" }
```

#### `POST /api/economy/inventory/credit`
Break a block (credit to inventory).
```json
{ "itemId": "stone" }
```

#### `GET /api/daily`
Daily quest state.
```json
{ "missionId": "break_50", "progress": 12, "target": 50, "done": false, "claimed": false }
```

#### `POST /api/daily/claim`
Claim daily quest reward.

### World/Chunk API (Auth-Required)

#### `GET /api/world/{worldId}/meta`
World metadata.

#### `GET /api/world/{worldId}/chunks?region=x1,z1,x2,z2`
Get chunk data for a rectangular region. Returns gzip-compressed chunk data as base64.

#### `POST /api/world/chunks`
Save/persist chunk data.
```json
{ "chunks": [{ "cx": 0, "cz": 0, "data": "base64_gzip_data" }] }
```

---

## Static Assets

### Block Textures
- `/textures/blocks/{name}.png` (16x16 pixel art)
- Examples: dirt.png, grass_top.png, grass_side.png, cobblestone.png, planks_oak.png, glass.png, stone.png, log_oak.png, log_oak_top.png, leaves_oak.png, sand.png, gravel.png, coal_block.png, diamond_block.png, beacon.png, dragon_egg.png, lucky_box.png, etc.

### UI Textures
- `/textures/ui/lucky_box.png`
- `/textures/ui/heart_full.png`
- `/textures/ui/trophy.png`
- `/textures/ui/music_note.png`

### Audio
- `/audio/sfx/{name}.mp3` — step_grass, step_stone, step_wood, dig_grass, dig_stone, glass, chest_open, chest_close, click, levelup, orb, pop

### Logo
- `/logo-blockfall.png`

---

## What We Can Build

### Option A: Market Analytics Dashboard (Immediate, Public API)
A real-time market tracker web app using only the public `/api/market` endpoint.
- **Price history**: Poll market API every N minutes, store in DB
- **Volume analysis**: Track sales over time
- **Rarity tier breakdowns**: Filter by tier, show price distributions
- **Top traders**: Leaderboard from sellerHandle/sellerWallet
- **Block price lookup**: Search any block, see all listings
- **Market sentiment**: Buy/sell pressure indicators
- **Alerts**: Price drop / rare listing notifications
- **ROI calculator**: Generator stake vs expected box value

**Pros**: No auth needed, buildable now, real value to players
**Cons**: Read-only (can't execute trades without wallet auth)

### Option B: Companion Tool (Wallet-Connected)
Extend Option A with Solana wallet connection for authenticated endpoints.
- Portfolio tracker (your inventory + island value)
- Auto-open boxes
- Market sniping (buy underpriced listings)
- Generator management dashboard

**Pros**: More functionality, sticky product
**Cons**: Requires Solana wallet integration, auth flow reverse-engineering

### Option C: Voxel Game on EVM (Inspired by BlockFall)
Build a similar game using our existing Stack Refinery contracts on Robinhood Chain.
- Reuse: generator/staking concept, box opening, block tiers, market
- Different: EVM instead of Solana, our own contracts
- Three.js voxel renderer (same approach as BlockFall)
- PixelLab assets (already generated for stack-refinery)

**Pros**: Full control, our own economy, EVM ecosystem
**Cons**: Significant build effort, need voxel renderer

### Option D: Market Bot / API Service
Backend service that wraps BlockFall's API with added features.
- REST/GraphQL API with historical data
- Webhook notifications for price alerts
- Arbitrage detection
- Market indexing/search
- Embeddable widgets for Discord/community

**Pros**: Infrastructure play, can power other tools
**Cons**: Need to handle rate limiting, data storage

---

## Recommended Path

**Start with Option A** (Market Analytics Dashboard) in cognitive-sync:
1. Public API, no auth, immediately buildable
2. Poll `/api/market` every 5 min, store in SQLite
3. Next.js + Tailwind dashboard with charts
4. Deploy to Vercel
5. Later extend to Option B (wallet connection) or Option D (API service)

This gives us a live product quickly while we decide on the bigger game build.