# IdleChain — Design & Architecture Document

> An idle hero/dungeon grinder with a player-driven economy, settled in a
> Solana token. 90s-arcade nostalgia, crypto-native loop, social show-off hub.
>
> **Status:** Design spec (pre-build). **Author target:** reuses the
> proven stack from `Waitfor App / prediction-market`.
> **Last updated:** 2026-06-11

---

## 0. TL;DR (read this first)

You play a hero who **auto-fights a dungeon while you're offline**. The hero
drops **materials**. You combine materials to craft **GOLD** — the rare,
grind-gated resource. Gold is sold to other players on a **marketplace priced
in $COIN** (your pump.fun token, USDC-paired). A shared **hub** lets players
parade their hero, gear, rank, and titles.

- **No NFTs.** Gold and items are fungible/in-DB; ownership of *value* settles
  through $COIN on-chain. This is deliberately simpler and creates a real
  economy instead of a thin "ownership" gimmick.
- **Off-chain gameplay, on-chain settlement.** The grind runs server-side
  (Supabase + tick worker). Only gold↔$COIN trades touch the chain.
- **Testnet (devnet) first**, real wallet connect from day one, mainnet later.
- **Reuses your existing stack** almost entirely (Next.js + Reown AppKit +
  Anchor + Supabase + oracle-worker pattern).

```
 IDLE GRIND (off-chain, server-authoritative)        ECONOMY (on-chain settle)
 hero auto-fights → materials drop → craft GOLD       marketplace: list gold for $COIN
 upgrade hero, prestige, deeper floors                buyer pays $COIN → gold moves
        Supabase + tick worker                        Anchor escrow program (devnet→mainnet)
                         \                            /
                          \—— THE HUB: show off ——/
                        shared town; see others' hero/gear/rank/titles
```

---

## 1. Design pillars (the "why")

1. **Number-go-up, passively.** Crypto players want accumulation, not twitch
   skill. The core verb is "check back, claim, upgrade, repeat."
2. **Gold is king, and gold is earned.** Gold must feel precious. It is gated
   behind a multi-step craft (materials → gold), so it can't be trivially
   farmed, which protects the $COIN economy.
3. **The flex is the point.** The hub is the retention + marketing engine.
   Every player showing off their hero is a free ad. Cosmetics, titles, and
   rank are the spend sinks.
4. **Server is the source of truth.** Because gold converts to real $COIN
   value, the client is never trusted. Every material drop, craft, and trade is
   validated server-side. Anti-bot is built in from day one, not bolted on.

---

## 2. Core gameplay loop

### 2.1 The idle grind
- The hero is assigned to a **dungeon floor**. While the player is offline (or
  online), the server accrues **combat ticks**.
- Each tick has a chance to drop **materials** (e.g. `iron_scrap`,
  `ember_dust`, `bone_shard`), weighted by floor depth and hero stats.
- The player returns, **claims** accrued drops (server computes elapsed time,
  capped — see §7 anti-cheat), and sees their materials grow.

### 2.2 Crafting gold
- Gold is **not** dropped directly. It is **crafted** from a recipe, e.g.:
  - `10 iron_scrap + 5 ember_dust + 2 bone_shard → 1 GOLD`
- This multi-material gate is the economic throttle. Tuning the recipe tunes
  gold's scarcity (and thus its $COIN price).

### 2.3 Progression
- **Upgrade hero:** spend materials/gold on attack/luck/speed → faster, richer
  drops.
- **Descend floors:** deeper floors drop rarer materials but need higher stats.
- **Prestige:** reset progress for a permanent multiplier + a prestige badge
  (a pure flex/retention mechanic).

### 2.4 The marketplace (where $COIN matters)
- A player lists `N GOLD` for `P $COIN`.
- A buyer pays `P $COIN`; the escrow program moves $COIN to seller and releases
  gold to buyer. **This is the only on-chain step in normal play.**
- Platform takes a small fee (basis points), mirroring your prediction-market
  `platform_fee_bps` pattern.

### 2.5 The hub (the flex layer)
- A shared 2D town (canvas) where avatars walk around.
- Each avatar visibly renders the player's hero skin, equipped gear, prestige
  badge, rank, and title.
- Functions: browse marketplace, inspect other players, leaderboard, chat.

---

## 3. Economy design

| Resource | Type | Source | Sink | On-chain? |
|---|---|---|---|---|
| Materials | fungible, in-DB | idle drops | crafting, upgrades | No |
| **GOLD** | fungible, in-DB | crafted from materials | marketplace sales, sinks | No (escrowed on trade) |
| **$COIN** | SPL token | pump.fun / DEX | buying gold, cosmetics, fees | **Yes** |
| Cosmetics/titles | flags, in-DB | bought w/ gold or $COIN | — (permanent flex) | No |

**The flywheel:** grind → gold → sell for $COIN ⇄ buy gold with $COIN to skip
grind → $COIN demand ↑ because gold demand ↑ because progression needs gold.

**Critical balancing levers** (all server-config, hot-tunable):
- material drop rates per floor
- gold recipe cost
- marketplace fee bps
- daily claim cap (anti-inflation)
- prestige multiplier curve

> ⚠️ **Economic risk:** if gold is too easy to farm, $COIN price collapses and
> bots drain it. The entire anti-cheat section (§7) exists to protect this.

---

## 4. Architecture (maps 1:1 onto your existing stack)

| Layer | Tech | Reused from `prediction-market`? |
|---|---|---|
| Frontend | Next.js 16 + React 19 + Tailwind 4 | ✅ same |
| Wallet | Reown AppKit + Solana adapter, `useWallet()` compat hook | ✅ copy verbatim |
| Game render | HTML5 `<canvas>` 2D (new) | ➕ new, small |
| API | Next.js API routes | ✅ same pattern |
| DB / state | Supabase (Postgres) | ✅ same |
| Idle tick worker | Node worker (like `run-oracle.js`) | ✅ same pattern, new logic |
| On-chain | Anchor program: escrow + marketplace | ♻️ adapts your escrow/transfer pattern |
| Config | `config.ts` with DEVNET/MAINNET switch | ✅ copy verbatim |
| Deploy | Vercel (web) + worker host (Render/Railway) | ✅ same |

### 4.1 Why this maps so cleanly
Your prediction market already does **off-chain state in Supabase + on-chain
settlement in a token via a worker (oracle)**. IdleChain is the same shape:
- `market state` → `hero / dungeon / inventory state`
- `oracle tick` (resolves markets) → `idle tick` (grants materials)
- `place bet` (on-chain USDC) → `buy gold` (on-chain $COIN)
- `config.ts DEVNET/MAINNET` → identical switch

### 4.2 Request/data flow
```
 Browser (canvas + React UI)
   │  wallet sign-in (AppKit) → session (verify-wallet pattern)
   │
   ├─► Next.js API routes ──► Supabase  (claim, craft, upgrade, list, inspect)
   │                            ▲
   │                            │ writes drops on schedule
   │                     Idle Tick Worker (Node, every N sec)
   │
   └─► Marketplace buy ──► Anchor program (devnet) ──► $COIN transfer + gold release
```

---

## 5. Data model (Supabase / Postgres)

> First-draft schema. Names are snake_case to match Postgres/Supabase norms.

```sql
-- A player, keyed by wallet.
players (
  wallet            text primary key,
  display_name      text,
  created_at        timestamptz default now(),
  last_claim_at     timestamptz default now(),  -- anti-cheat: elapsed-time cap
  prestige_level    int  default 0,
  title             text,                         -- flex
  banned            boolean default false
)

-- One hero per player (v1). Stats drive drop rates.
heroes (
  wallet        text primary key references players(wallet),
  level         int default 1,
  attack        int default 1,
  luck          int default 1,   -- drop quantity/rarity
  speed         int default 1,   -- tick frequency
  current_floor int default 1,
  skin          text default 'default'
)

-- Fungible inventory: one row per (wallet, item).
inventory (
  wallet    text references players(wallet),
  item      text,                 -- 'iron_scrap' | 'ember_dust' | 'gold' | ...
  qty       bigint default 0,
  primary key (wallet, item)
)

-- Marketplace listings (gold priced in $COIN).
listings (
  id            uuid primary key default gen_random_uuid(),
  seller        text references players(wallet),
  gold_amount   bigint,
  price_coin    bigint,           -- in $COIN base units
  status        text default 'open',  -- open | sold | cancelled
  created_at    timestamptz default now()
)

-- Audit log of every economic event (anti-cheat forensics).
ledger (
  id        bigserial primary key,
  wallet    text,
  kind      text,   -- 'claim' | 'craft' | 'upgrade' | 'list' | 'buy' | 'sell'
  detail    jsonb,
  at        timestamptz default now()
)
```

---

## 6. On-chain program (Anchor)

**Reuses your escrow + SPL `Transfer` pattern from prediction-market.**

Minimal instruction set for v1:
- `initialize_platform(fee_bps, admin)` — one-time, like your `PlatformConfig`.
- `list_gold(gold_amount, price_coin)` — records intent; gold reserved in DB.
- `buy_gold(listing)` — buyer's $COIN → seller (minus fee → platform escrow);
  server releases gold in DB on confirmed tx. Mirrors `place_bet` token flow.
- `claim_fees()` — admin withdraws accrued platform fees (you already have this).

**Config switch (copied from your `config.ts`):**
```ts
export const DEVNET_CONFIG  = { programId, coinMint, platformConfig, escrowVault, feeBps };
export const MAINNET_CONFIG = { /* filled after mainnet deploy */ };
export const ACTIVE_CONFIG  = DEVNET_CONFIG;   // flip to MAINNET at launch
export const USE_REAL_CONTRACT = true;
```

> **$COIN note:** on devnet we use a test SPL mint we control (free to mint for
> testing). At launch, `coinMint` becomes the real pump.fun token mint.

---

## 7. Anti-cheat / anti-bot (NON-OPTIONAL — gold has real value)

Because gold converts to $COIN, **gold farming has real monetary value**, so
we must assume adversarial players and bots from day one.

1. **Server-authoritative everything.** Client never reports drops/gold. The
   client only *requests* actions; the server computes outcomes.
2. **Elapsed-time claim cap.** Idle accrual computed from `last_claim_at` server
   timestamp, capped (e.g. 8h max offline accrual). No client clock trust.
3. **Rate limits** per wallet on claim/craft/list/buy endpoints.
4. **Drop validation server-side** with seeded RNG per (wallet, tick) so it's
   reproducible/auditable, never client-supplied.
5. **Ledger everything** (§5) for forensic detection of abnormal earn rates —
   the "suspicious-harvesters" idea, but for *our own* game where it's correct.
6. **Wallet sign-in proof** (reuse your `verify-wallet` / `session-auth`).
7. **Marketplace sanity bounds** (min/max price, no self-trading wash loops).

---

## 8. Build phases

### Phase 0 — Foundation (no chain yet)
- Scaffold Next.js app (copy wallet hook + config pattern).
- Supabase schema (§5).
- `useWallet()` sign-in working on devnet.

### Phase 1 — Idle core (off-chain, the fun)
- Hero + dungeon + tick worker granting materials.
- Claim / craft-gold / upgrade endpoints, all server-authoritative.
- Minimal canvas UI: hero, inventory, claim button. **Prove the loop is fun.**

### Phase 2 — The hub (flex layer)
- Shared canvas town, avatars, see-others' hero/gear/title, leaderboard, chat.

### Phase 3 — Economy on devnet
- Anchor escrow/marketplace program on devnet + test $COIN mint.
- List/buy gold for $COIN end-to-end on devnet.

### Phase 4 — Hardening + mainnet
- Anti-cheat pass (§7), load test, balance tuning.
- Flip `ACTIVE_CONFIG` to mainnet, point `coinMint` at real pump.fun token.

> **Recommendation:** ship Phase 1 and *playtest the idle loop for fun before
> writing any chain code.* If the grind isn't satisfying off-chain, the token
> won't save it. This is the #1 failure mode of crypto games.

---

## 9. Open questions (decide before/while building)

1. **One hero or a roster?** v1 assumes one hero per wallet (simpler). Roster =
   more depth + more flex, but more systems.
2. **$COIN cash-out direction:** can players also buy gold *with* $COIN (sink),
   or only sell gold *for* $COIN (faucet)? Both = healthier flywheel; design §3
   assumes both.
3. **Hub realtime transport:** Supabase Realtime (simplest, reuses stack) vs a
   dedicated WebSocket server (more control, more ops). Start with Supabase
   Realtime.
4. **Daily caps / energy?** A soft daily earn cap protects $COIN but can feel
   restrictive. Lever, not a yes/no.
5. **Cosmetic source of truth:** purely in-DB flags (cheap) vs optional NFT
   skins later (you said no NFTs for gold — cosmetics could still be in-DB).

---

## 10. Risks & honest cautions

- **Economic collapse if gold inflates.** Mitigated by §7 + tunable recipe.
- **Regulatory/financial framing.** A token with a USDC pair + in-game cash-out
  has real-money characteristics; understand the rules in your jurisdiction
  before mainnet. (Not legal advice — flag it, don't ignore it.)
- **"Fun must exist without the token."** If the idle loop isn't fun in Phase 1,
  no amount of tokenomics fixes it. Validate fun first.
- **Bots will come** the moment gold has value. Assume it; §7 is mandatory.

---

## Appendix A — Reuse map from `Waitfor App / prediction-market`

| Existing file | Reuse for IdleChain |
|---|---|
| `src/hooks/useAppKitWallet.ts` | wallet sign-in — copy almost verbatim |
| `src/lib/config.ts` | DEVNET/MAINNET switch — copy pattern |
| `src/lib/verify-wallet.ts`, `session-auth.ts` | player auth |
| `src/lib/supabase.ts`, `supabase-server.ts` | DB access |
| `scripts/run-oracle.js` | template for the idle tick worker |
| `src/lib/contract-service.ts` | template for build/send marketplace txns |
| `programs/prediction-market` (escrow + Transfer) | template for marketplace escrow program |
| `src/components/WalletProvider.tsx`, `ConnectButton.tsx` | UI wiring |
```
