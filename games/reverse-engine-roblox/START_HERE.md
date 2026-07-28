# 🎮 Reverse Engine Roblox — START HERE: Build Guide

> **Role:** You are the Game Architect + Creative Director for a new Roblox game.
> **Goal:** Build a viral Roblox game using patterns from 9 reverse-engineered titles.

---

## 1. ELEVATOR PITCH

**"A 3-minute party game that's so simple your little cousin can play it, but so competitive you'll rage-quit — and every loss makes you want to spend 10 Robux to try again."**

Roblox hits aren't built — they're **engineered for virality**. This guide uses the patterns from 9 analyzed games (Catch a Monster, Tap Simulator, Your Zoo, House Tycoon, Clicker Pet Sim, and more) to build a game optimized for retention, social spread, and monetization.

---

## 2. DESIGN PEG

### Visual Style
- **Reference:** Bright, saturated colors. Think Adopt Me meets Pet Simulator X
- **Palette:** Rainbow-friendly, high contrast, readable at thumbnail size
- **Characters:** Blocky Roblox avatars with夸张 accessories (pets, auras, trails)
- **UI:** Large buttons, big numbers, satisfying animations, mobile-first

### Game Feel
- **Pacing:** Frantic 3-minute rounds → 10-second results → instant replay
- **Juice:** Screen shake on big hits, number popups everywhere, particle explosions on rewards
- **Audio:** Bass-boosted sound effects, trending music, satisfying "cha-ching" on purchases

### Tone
- **Emotional arc:** Curiosity (join) → Excitement (play) → Frustration (lose) → Determination (retry)
- **Themes:** Competition, collection, status, social proof
- **Vibe:** "Everyone's playing it and I don't want to be left out"

### Design North Star
> **If a 8-year-old can't understand it in 30 seconds, simplify it.**

Roblox's audience skews young. Complexity kills retention. Simplicity drives virality.

---

## 3. CORE LOOP

### The Roblox Viral Loop

```
┌──────────────────────────────────────────────────┐
│                THE VIRAL CYCLE                     │
│                                                   │
│  Join (free) → Play 3-min round → Win or Lose    │
│      ↓                                            │
│  Earn currency → Buy pet/upgrade → Feel stronger  │
│      ↓                                            │
│  Share/Invite friends → Social proof → More join   │
│      ↓                                            │
│  Rebirth/Prestige → Reset → Play again (stronger) │
│      ↓                                            │
│  Spend Robux (optional) → Skip timer → Win more   │
└──────────────────────────────────────────────────┘
```

**30-second loop:** Tap/click → See number go up → Feel good
**3-minute loop:** Complete a round → Earn rewards → Buy upgrade
**15-minute loop:** Rebirth → Reset progression → Play with multipliers
**1-hour loop:** Max out current rebirth → Unlock new world/area → New goals

---

## 4. GAME TYPE DECISION

Based on the 9 analyzed games, you have 4 proven game types to choose from:

### Option A: Simulator (Tap/Clicker)
**Pattern from:** Tap Simulator, Clicker Pet Sim
- **Core:** Click to earn → Buy upgrades → Earn faster → Rebirth
- **Retention hook:** Pets with multipliers, gacha for rare pets
- **Monetization:** Pet packs, luck boosts, auto-clickers
- **Build complexity:** LOW
- **Virality:** MEDIUM (needs social features)
- **Best for:** First Roblox game, simple to build and monetize

### Option B: Collection (Catch/Train)
**Pattern from:** Catch a Monster, Your Zoo
- **Core:** Explore → Find creature → Catch → Train → Battle
- **Retention hook:** "Gotta catch 'em all" completion drive
- **Monetization:** Egg hatching, rare creature sales, shiny variants
- **Build complexity:** MEDIUM
- **Virality:** HIGH (trading, showing off collection)
- **Best for:** Long-term retention, social trading economy

### Option C: Tycoon (Build/Manage)
**Pattern from:** House Tycoon, Grow a Country
- **Core:** Buy plot → Build structure → Earn passive income → Expand
- **Retention hook:** Base customization, status display
- **Monetization:** Premium plots, exclusive decorations, speed-ups
- **Build complexity:** MEDIUM
- **Virality:** MEDIUM (show off your base)
- **Best for:** Creative players, long sessions

### Option D: Party Game (Minigame)
**Pattern from:** Knockout, Slappy Seals, 60+ idea docs
- **Core:** Join lobby → 3-min minigame → Win/lose → Rewards → Replay
- **Retention hook:** Quick rounds, leaderboard, season rewards
- **Monetization:** Cosmetics, death effects, kill effects, VIP passes
- **Build complexity:** MEDIUM-HIGH (multiplayer, anticheat)
- **Virality:** VERY HIGH (streamable, shareable clips)
- **Best for:** Viral explosion, trending potential

### Recommendation

| If you want... | Choose... |
|----------------|-----------|
| Fastest to build and monetize | Simulator (A) |
| Best long-term retention | Collection (B) |
| Creative self-expression | Tycoon (C) |
| Viral explosion potential | Party Game (D) |

**First-time builder? Start with Simulator (A).** It's the simplest, and you can add collection elements later.

---

## 5. BOTTOM-UP ARCHITECTURE

### Layer 0: Roblox Studio Foundation
```
Roblox Studio Project
├── ServerScriptService/
│   ├── GameManager (round logic, rewards)
│   ├── DataStore (player save data)
│   ├── EconomyManager (currency, purchases)
│   ├── RebirthSystem (prestige reset)
│   └── Anticheat (basic validation)
├── ReplicatedStorage/
│   ├── Modules/
│   │   ├── ItemDefinitions (all items, pets, upgrades)
│   │   ├── StatFormulas (multiplier calculations)
│   │   ├── PetSystem (pet logic, multipliers)
│   │   └── NotificationSystem (UI messages)
│   ├── Events/ (RemoteEvents for client-server comms)
│   └── Assets/ (shared models, sprites)
├── StarterGui/
│   ├── HUD (currency, stats, buttons)
│   ├── ShopUI (buy upgrades/pets)
│   ├── InventoryUI (manage pets/items)
│   └── NotificationUI (popups, rewards)
└── StarterPlayer/
    └── StarterPlayerScripts/ (client-side input, UI updates)
```

**Build first:**
- [ ] Roblox Studio project setup
- [ ] DataStore save/load (player currency, upgrades, pets)
- [ ] RemoteEvent for client-server communication
- [ ] Basic HUD showing currency
- [ ] Click/tap to earn currency

### Layer 1: Core Gameplay
```
Gameplay/
├── ClickHandler (tap to earn)
├── UpgradeSystem (buy upgrades, increase earn rate)
├── PetSystem (equip pets, calculate multipliers)
├── RebirthSystem (reset for permanent multiplier)
├── LeaderboardSystem (top players by currency/rebirths)
└── RewardSystem (distribute rewards after actions)
```

**Build second:**
- [ ] Click/tap gives currency (number goes up)
- [ ] Buy upgrade → earn rate increases
- [ ] Equip pet → multiplier applied to earnings
- [ ] Rebirth → reset currency/upgrades, gain permanent multiplier
- [ ] Leaderboard updates in real-time

### Layer 2: Collection + Gacha
```
Collection/
├── EggSystem (hatch eggs, random pet with rarity)
├── PetDatabase (all pets with stats, rarity, multiplier)
├── TradingSystem (trade pets with other players)
├── InventorySystem (manage owned pets)
└── RaritySystem (common, rare, epic, legendary, secret)
```

**Build third:**
- [ ] Buy egg → hatch → get random pet
- [ ] Pet rarity system with drop rates
- [ ] Pet multipliers stack when equipped
- [ ] Trade pets with other players
- [ ] Pet inventory UI

### Layer 3: Social + Monetization
```
Social/
├── InviteSystem (invite friends for rewards)
├── GuildSystem (group bonuses)
├── ChatSystem (safe chat, emotes)
├── DailyRewards (login streak)
├── EventSystem (limited-time events, seasonal)
└── SocialDisplay (show off pets, rank, title)

Monetization/
├── GamePassSystem (permanent perks)
├── DeveloperProducts (consumable purchases)
├── RobuxShop (buy currency, eggs, boosts)
├── LuckBoost (temporary rare pet chance increase)
├── AutoClicker (gamepass, auto-earn)
└── VIPServer (private servers)
```

**Build fourth:**
- [ ] Daily login rewards (streak system)
- [ ] Invite friends → both get bonus
- [ ] Gamepass for auto-clicker
- [ ] Developer product for luck boost (10 min)
- [ ] Limited-time event with exclusive pet
- [ ] Leaderboard with top 10 players

### Layer 4: Content + Polish
```
Content/
├── WorldExpansion (new areas, new eggs, higher tiers)
├── QuestSystem (daily/weekly quests for extra rewards)
├── AchievementSystem (track milestones)
├── SeasonSystem (seasonal content, leaderboards)
├── CodesSystem (redeem codes for free rewards)
└── UpdateSystem (content updates drive re-engagement)

Polish/
├── VFX (particle effects on hatch, purchase, rebirth)
├── Animations (UI tweens, pet animations, character effects)
├── Audio (click sounds, hatch sounds, music)
├── Tutorial (first-time player guidance)
├── Mobile optimization (touch controls, performance)
└── Anticheat (server-side validation, exploit prevention)
```

**Build last:**
- [ ] 5+ egg types with different pet pools
- [ ] 20+ pets across rarities
- [ ] 3+ worlds/areas to unlock
- [ ] Daily/weekly quest system
- [ ] Achievement system with milestones
- [ ] Promo codes system
- [ ] Particle VFX on all major events
- [ ] Mobile-optimized UI (large buttons, responsive)
- [ ] Server-side anticheat (validate all purchases)

---

## 6. BUILD ORDER (Priority Sequence)

| Priority | What | Why | Time |
|----------|------|-----|------|
| 1 | Roblox Studio project + DataStore | Foundation | 1 day |
| 2 | Click to earn + HUD | Core loop prototype | 1 day |
| 3 | Buy upgrades | First monetization hook | 1 day |
| 4 | Pet system + multipliers | Collection hook | 2 days |
| 5 | Egg hatching (gacha) | Retention driver | 2 days |
| 6 | Rebirth system | Long-term progression | 1 day |
| 7 | Leaderboard | Social competition | 1 day |
| 8 | Trading system | Social economy | 2 days |
| 9 | Gamepass + dev products | Monetization | 1 day |
| 10 | Daily rewards | Retention | 1 day |
| 11 | Invite system | Virality | 1 day |
| 12 | Event system | Re-engagement | 2 days |
| 13 | Quest system | Session length | 2 days |
| 14 | VFX + audio polish | Game feel | 3 days |
| 15 | Mobile optimization + anticheat | Ship quality | 2 days |

**Total: ~20 days for a fully featured, monetized Roblox game.**

---

## 7. PHASE BREAKDOWN

### Phase 0: Foundation (Days 1-2)
**Milestone:** Player can click to earn, see their currency, and save/load.

- [ ] Roblox Studio project
- [ ] DataStore save system (currency, upgrades, pets, rebirths)
- [ ] HUD with currency display
- [ ] Click/tap button → +1 currency
- [ ] Server validates all currency gains
- [ ] Save on leave, load on join

**Playtest:** Can you click, earn, leave, come back, and still have your currency?

### Phase 1: Core Loop (Days 3-5)
**Milestone:** Click → upgrade → earn faster → buy first pet → feel multiplier.

- [ ] Upgrade shop (buy earn-rate upgrades)
- [ ] Pet system (buy pet → equip → multiplier applied)
- [ ] Pet multiplier calculation (pets stack additively or multiplicatively)
- [ ] Visual feedback on earnings (number popups)
- [ ] Basic VFX on purchase

**Playtest:** Do you feel the progression? Is buying upgrades satisfying?

### Phase 2: Gacha + Rebirth (Days 6-10)
**Milestone:** Hatch eggs for random pets, rebirth for permanent multipliers, see leaderboard.

- [ ] Egg shop (buy egg → random pet with rarity)
- [ ] Pet rarity system (Common 60%, Rare 25%, Epic 10%, Legendary 4%, Secret 1%)
- [ ] Rebirth system (reset for permanent multiplier)
- [ ] Rebirth UI (show current vs. next multiplier)
- [ ] Leaderboard (top 10 by currency, top 10 by rebirths)
- [ ] Pet inventory UI (view all pets, equip/unequip)

**Playtest:** Do you want to hatch "just one more egg"? Does rebirth feel rewarding?

### Phase 3: Social + Monetization (Days 11-15)
**Milestone:** Daily rewards, invite friends, buy Robux items, trade pets.

- [ ] Daily login reward system (streak bonuses)
- [ ] Invite friends → both get reward
- [ ] Gamepass: Auto-clicker (permanent)
- [ ] Dev product: Luck boost (10 min, 2x rare chance)
- [ ] Dev product: Currency pack (buy coins with Robux)
- [ ] Pet trading system (secure, server-validated)
- [ ] Limited-time event with exclusive pet

**Playtest:** Would you spend Robux? Is trading fun? Do daily rewards make you want to return?

### Phase 4: Content + Polish (Days 16-20)
**Milestone:** Multiple worlds, 20+ pets, quests, VFX, mobile-optimized.

- [ ] 3+ worlds/areas (unlock with rebirth count)
- [ ] 5+ egg types (different pet pools per world)
- [ ] 20+ pets across all rarities
- [ ] Daily/weekly quest system
- [ ] Achievement system
- [ ] Promo code system
- [ ] VFX: hatch, purchase, rebirth, level-up
- [ ] Audio: click, purchase, hatch, music
- [ ] Mobile UI optimization (large buttons, responsive)
- [ ] Server-side anticheat (validate all transactions)
- [ ] Tutorial for new players

**Playtest:** Would a 8-year-old understand it in 30 seconds? Would a streamer enjoy it?

---

## 8. DESIGN PEG BOARD

```
┌─────────────────────────────────────────────────────┐
│              ROBLOX GAME DESIGN PEG                  │
│                                                      │
│  PITCH: 3-minute fun that's so simple an 8-year-old │
│         can play it, but so addictive you can't stop │
│                                                      │
│  FEEL:  Satisfying, rewarding, social                │
│         Every tap gives feedback. Every upgrade feels│
│         like power. Every hatch is a dopamine hit.   │
│                                                      │
│  LOOK:  Bright, saturated, readable at thumbnail    │
│         Big buttons, big numbers, big pets          │
│                                                      │
│  SOUND: Bass-boosted SFX, trending music             │
│         "Cha-ching" on purchase, fireworks on hatch  │
│                                                      │
│  LOOP:  Tap → Earn → Upgrade → Hatch → Rebirth      │
│                                                      │
│  HOOK:  "I hatched a SECRET pet and my multiplier    │
│         went INSANE"                                 │
│                                                      │
│  CUT IF: It adds complexity without adding dopamine.│
│          If it doesn't drive taps, trades, or        │
│          purchases, cut it.                          │
└─────────────────────────────────────────────────────┘
```

---

## 9. ECONOMY BLUEPRINT

### Currency Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Soft Currency│     │  Hard Currency│    │  Premium     │
│  (Coins)     │     │  (Gems)      │    │  (Robux)     │
│              │     │              │    │              │
│ EARN:        │     │ EARN:        │    │ SPEND:       │
│ • Tapping    │     │ • Quests     │    │ • Buy gems   │
│ • Upgrades   │     │ • Daily      │    │ • Buy eggs   │
│ • Rebirth    │     │ • Events     │    │ • Buy boosts │
│              │     │ • Achievements│    │ • Buy passes │
│ SPEND:       │     │              │    │              │
│ • Upgrades   │     │ SPEND:       │    │              │
│ • Eggs       │     │ • Premium    │    │              │
│ • Areas      │     │   eggs       │    │              │
│ • Rebirth    │     │ • Exclusive  │    │              │
│              │     │   pets       │    │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Rarity Drop Rates (Proven Pattern)

| Rarity | Drop Rate | Multiplier | Status |
|--------|-----------|-----------|--------|
| Common | 50% | 1.5x | Basic |
| Uncommon | 25% | 3x | Basic |
| Rare | 15% | 8x | Mid |
| Epic | 7% | 20x | Mid |
| Legendary | 2.5% | 50x | High |
| Secret | 0.5% | 250x | Whale |

### Key Economy Formulas

```
earn_per_click = base_earn × upgrade_multiplier × pet_multiplier × rebirth_multiplier × event_multiplier

pet_multiplier = sum_of_equipped_pet_multipliers (or product for multiplicative stacking)

rebirth_multiplier = 1 + (rebirth_count × 0.1)  // +10% per rebirth

egg_cost = base_cost × (1.15 ^ eggs_hatched)  // cost scaling

luck_boost_effect = base_rarity_chance × boost_multiplier
```

---

## 10. VIRAL MECHANICS CHECKLIST

These are the mechanics that drove virality in the analyzed games:

| Mechanic | Implementation | Priority |
|----------|---------------|----------|
| **Leaderboard** | Server-updated, visible in-game | MUST HAVE |
| **Pet showing off** | Equipped pets follow player, visible to others | MUST HAVE |
| **Trade system** | Player-to-player pet trading | MUST HAVE |
| **Invite rewards** | Get bonus when friend joins | MUST HAVE |
| **Social proof** | "X players playing now" counter | HIGH |
| **Share button** | Share to social media with screenshot | HIGH |
| **Guild/Team** | Group bonuses, team leaderboard | MEDIUM |
| **Limited events** | FOMO-driven time-limited content | HIGH |
| **Codes** | Streamers give codes → viewers join | HIGH |
| **Streamer friendly** | Spectator mode, clip-worthy moments | MEDIUM |

---

## 11. RETENTION MECHANICS

### Session Retention (keeps them playing this session)

| Mechanic | Pattern From | Effect |
|----------|-------------|--------|
| Number go up | Tap Simulator | Dopamine every tap |
| Near-miss hatching | Catch a Monster | "Almost got legendary!" |
| Upgrade milestones | Clicker Pet Sim | Visible progress bars |
| Leaderboard chasing | All games | Competitive drive |

### Daily Retention (brings them back tomorrow)

| Mechanic | Pattern From | Effect |
|----------|-------------|--------|
| Daily login streak | Your Zoo | Loss aversion (don't break streak) |
| Daily quests | Catch a Monster | Goal for the session |
| Limited-time events | All games | FOMO |
| New egg/pet drops | All games | Curiosity |
| Rebirth milestones | Tap Simulator | Long-term goal |

### Social Retention (brings friends back together)

| Mechanic | Pattern From | Effect |
|----------|-------------|--------|
| Trading | Catch a Monster | Need to negotiate |
| Guild bonuses | House Tycoon | Social obligation |
| Leaderboard competition | All games | Rivalry |
| Show off base/pets | Your Zoo, House Tycoon | Status display |

---

## 12. CRITICAL DESIGN DECISIONS

### Decision 1: Pet Multiplier Stacking
**Question:** Additive or multiplicative pet stacking?
- **Additive:** Pet1 (2x) + Pet2 (3x) = 5x total. Easier to balance.
- **Multiplicative:** Pet1 (2x) × Pet2 (3x) = 6x total. More exciting, harder to balance.

**Recommendation:** Multiplicative for excitement, but cap the number of equipped pets (3-6).

### Decision 2: Rebirth Reset Depth
**Question:** What resets on rebirth?
- **Shallow:** Reset currency + upgrades. Keep pets. (Forgiving, more rebirths)
- **Deep:** Reset currency + upgrades + pets. Keep rebirth multiplier. (Hardcore, fewer rebirths)

**Recommendation:** Shallow. Keep pets — they're the collection hook. Reset currency + upgrades only.

### Decision 3: P2W Balance
**Question:** How much can Robux skip?
- **Minimal:** Only cosmetics and minor boosts. (Fair, lower revenue)
- **Moderate:** Boosts, luck increases, auto-play. (Balanced, good revenue)
- **Aggressive:** Buy directly to top. (High revenue, kills retention)

**Recommendation:** Moderate. Sell convenience (auto-clicker, luck boost, time-saver) but not power directly.

### Decision 4: Game Length Per Session
**Question:** How long should a session last?
- **3 minutes:** Party game style, high replayability
- **15 minutes:** Simulator style, grinding session
- **30+ minutes:** Tycoon style, base building

**Recommendation:** For Simulator — 15-minute sessions with 3-minute micro-goals (hatch an egg, buy an upgrade, check leaderboard).

---

## 13. TECH STACK

| Component | Tool |
|-----------|------|
| Engine | Roblox Studio |
| Language | Luau (Roblox Lua) |
| Data storage | DataStoreService (with caching) |
| Communication | RemoteEvents / RemoteFunctions |
| UI | ScreenGui + Frame + TextLabel |
| Version control | Rojo (external Git) or built-in |
| Modeling | Roblox Studio built-in + Blender |
| Image editing | Any (for textures, icons) |
| Analytics | GameAnalytics or custom |

---

## 14. ASSET CHECKLIST

### Minimum Viable Assets (Phase 0-1)
- [ ] Game icon (thumbnail, 512x512)
- [ ] Game thumbnail (banner, 1920x1080)
- [ ] 3 pet models (common, rare, legendary)
- [ ] 1 egg model
- [ ] HUD background
- [ ] Button textures (buy, equip, hatch)
- [ ] Currency icon
- [ ] 3 SFX (click, purchase, hatch)
- [ ] Background music

### Full Game Assets (Phase 2-4)
- [ ] 20+ pet models across rarities
- [ ] 5+ egg models
- [ ] 3+ world/area environments
- [ ] Full UI theme (buttons, panels, fonts)
- [ ] Particle effects (hatch, purchase, rebirth, level-up)
- [ ] 10+ SFX
- [ ] 3+ music tracks
- [ ] Gamepass icons
- [ ] Developer product icons
- [ ] Loading screen
- [ ] Tutorial UI overlays

---

## 15. THE 30-SECOND TEST

Roblox players decide in 30 seconds whether to stay. This is what they should experience:

```
Second 0-5: Spawn in → See other players with cool pets → "I want that"
Second 5-15: UI shows big "CLICK" button → Click → Number goes up → "Satisfying"
Second 15-25: See "BUY EGG" button → Buy → Hatch animation → Got a pet!
Second 25-30: Pet follows you → Multiplier shown → "I need more pets"
```

If the first 30 seconds don't hook them, they leave. **Test with 10 strangers before adding any content past Phase 1.**

---

## 16. COMMON PITFALS

| Pitfall | Fix |
|---------|-----|
| Too many features, none polished | Ship with 3 polished features, not 10 broken ones |
| Economy inflates too fast | Test your formulas, add cost scaling |
| Pets feel worthless | Make rarity meaningful with big multiplier jumps |
| Trading gets exploited | Server-validate every trade, add trade cooldowns |
| Data loss on update | Version your DataStore schema from day 1 |
| Mobile players can't play | Test on phone, make buttons big, optimize performance |
| Nobody comes back after day 1 | Daily rewards + limited events + leaderboard |
| Anticheat is an afterthought | Build server-side validation from Phase 0 |

---

## 17. FILE STRUCTURE TEMPLATE

```
Roblox Project (via Rojo)
├── src/
│   ├── server/
│   │   ├── GameManager.lua (round logic, main loop)
│   │   ├── DataStore.lua (save/load system)
│   │   ├── EconomyManager.lua (currency validation)
││   ├── RebirthSystem.lua (prestige reset)
│   │   ├── TradingSystem.lua (pet trading)
│   │   ├── Anticheat.lua (server validation)
│   │   └── Leaderboard.lua (leaderboard updates)
│   ├── client/
│   │   ├── UIManager.lua (HUD, shop, inventory)
│   │   ├── InputHandler.lua (click/tap detection)
│   │   ├── PetDisplay.lua (equipped pet rendering)
│   │   ├── NotificationUI.lua (popups, rewards)
│   │   └── TutorialUI.lua (first-time guidance)
│   ├── shared/
│   │   ├── PetDefinitions.lua (all pets, stats, rarity)
│   │   ├── UpgradeDefinitions.lua (all upgrades)
│   │   ├── EggDefinitions.lua (egg types, costs, pools)
│   │   ├── Formulas.lua (economy calculations)
│   │   └── Constants.lua (game constants)
│   └── assets/ (models, textures, sounds)
├── default.project.json (Rojo config)
└── wally.toml (package manager, optional)
```

---

## 18. QUICK START CHECKLIST

```
□ Read GAME_MECHANICS.md (all 9 game analyses)
□ Read ECONOMY.md (economy patterns)
□ Choose game type (Simulator / Collection / Tycoon / Party)
□ Set up Roblox Studio project
□ Build DataStore save system
□ Click to earn + HUD
□ Buy upgrades
□ Pet system + multipliers
□ Egg hatching gacha
□ Rebirth system
□ Leaderboard
□ Trading
□ Gamepass + dev products
□ Daily rewards
□ VFX + audio polish
□ Mobile optimization
□ Anticheat validation
□ Playtest with 10 strangers
□ Publish
□ Run first event
```

**Start with Layer 0. Make the number go up. Everything else follows.**