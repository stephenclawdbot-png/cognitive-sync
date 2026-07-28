# Reverse Engine Roblox — Economy Document

**Type:** Roblox game analysis collection  
**Date:** 2026-01-2x  

---

## 1. Multi-Game Economy Patterns

### 1.1 Common Currency Architecture

All analyzed Roblox games share a similar currency structure:

| Currency Tier | Examples | Source | Sink | Persistence |
|---------------|----------|--------|------|-------------|
| Primary (Soft) | Clicks, Cash | Gameplay | Upgrades, eggs | Reset on rebirth |
| Premium (Hard) | Gems, Robux | Real money, events | Special items, speed boosts | Permanent |
| Prestige | Rebirths | Rebirth milestone | Permanent multiplier | Permanent |
| Event | Event Tokens, Keys | Limited-time events | Exclusive items | Time-limited |

### 1.2 Economy Flow Pattern
```
Player Action → Soft Currency → Eggs/Upgrades → More Soft Currency
                    ↓                                    ↑
              Rebirth (reset) → Multiplier → Faster Earning ┘
                    ↓
              Premium Currency → Exclusive Items → Advantage
```

---

## 2. Game-by-Game Economy Details

### 2.1 Catch a Monster Economy

**Currencies:**
| Currency | Earn | Spend |
|----------|------|-------|
| Cash | Selling monsters, quests | Basic eggs, items |
| Robux | Real money | Premium eggs, game passes |
| Event Tokens | Events | Limited-time items |

**Key Economic Mechanics:**
- Level-gated pet slots (creates progression gate)
- Friend luck boost (social engagement driver)
- World portal system (content gating by progression)
- Weekly leaderboard rewards (competitive engagement)
- Mount system (status symbol, additional revenue)

**Monetization:**
- Premium eggs (better odds than basic eggs)
- Game passes (extra slots, x2 luck, auto-collect)
- Cosmetics (skins, auras, mounts)
- Event-exclusive monsters (FOMO)

### 2.2 Tap Simulator Economy

**Currencies:**
| Currency | Earn | Spend |
|----------|------|-------|
| Clicks | Tapping, passive income | Eggs, upgrades |
| Gems | Premium purchases, events | Special eggs, autoclicker |
| Rebirths | Rebirth at 1,000 clicks | Permanent multiplier |

**Key Economic Mechanics:**
- Click multiplier from pets (exponential scaling)
- 71 rebirth tiers observed (deep prestige system)
- Zone progression (clicks required to unlock)
- Special egg: Lightning Egg (event-limited)
- Ultra-rare: Empyrean Sovereign (1 in 1,000,000)

**Multiplier Stack:**
```
Total Income = Base Click × Pet Multiplier × Rebirth Multiplier × Zone Bonus × Event Bonus
```

**Monetization:**
- Autoclicker (pay for convenience)
- Special eggs (premium pets)
- Event passes (exclusive access)
- Luck boosters (better egg odds)

### 2.3 Your Zoo Economy

**Currencies:**
| Currency | Earn | Spend |
|----------|------|-------|
| Cash | Zoo visitors, offline earnings | Eggs, enclosures |
| Robux | Real money | Premium eggs, speed boosts |

**Key Economic Mechanics:**
- Offline earnings (zoo generates income while away)
- Pity timer system:
  - Golden: 47 seconds guaranteed
  - Rainbow: 4m47s guaranteed
  - Secret: 14m47s guaranteed
- Rebirth keeps animals (soft prestige)
- "Collect all" completion incentive

**Pity Timer Formula:**
```
guaranteed_drop = total_time_spent >= pity_threshold
```

**Monetization:**
- Premium eggs (better animals)
- Speed boosts (farser earnings)
- Enclosure upgrades (more visitor income)
- Exclusive animals (event-limited)

### 2.4 House Tycoon Economy

**Currencies:**
| Currency | Earn | Spend |
|----------|------|-------|
| Cash | Clicking, idle income | Build, upgrade |
| Gems | Premium | Special upgrades |
| Keys | Events, quests | Unlock content |
| Rebirths | Rebirth milestone | 2.5x multiplier |

**Key Economic Mechanics:**
- 2.5x multiplier per rebirth (exponential growth)
- Bulk rebirth pricing (discount for buying multiple)
- Upgrade system (incremental improvements)
- 10M visits event (1/250,000 odds — extreme rarity)

**Rebirth Economy:**
```
rebirth_cost(n) = base_cost × scaling_factor^n
bulk_discount = 1 - (bulk_count × discount_rate)
multiplier_total = 2.5^rebirth_count
```

**Monetization:**
- Gem purchases (premium upgrades)
- Key purchases (unlock content faster)
- Event participation (exclusive rewards)
- Idle income boosters

### 2.5 Clicker Pet Sim Economy

**Currencies:** Clicks, Gems, Rebirths (same as Tap Simulator)

**Key Economic Mechanics:**
- Click-to-earn (active gameplay)
- Pet multiplier system
- Rebirth prestige loop
- Trading economy (player-driven)
- Code redemption (promotional)

---

## 3. Cross-Game Economy Patterns

### 3.1 The Gacha Economy

All games use a **gacha/egg system** as the primary engagement driver:

```
Earn Currency → Buy Egg → Hatch → Get Pet/Animal
                                   ↓
                              Common (70%) → Duplicate → Sell/Trade
                              Rare (20%) → New → Equip
                              Epic (8%) → New → Show Off
                              Legendary (1.9%) → New → Flex
                              Secret (0.1%) → New → Status Symbol
```

**Gacha Design Rules:**
1. Always give *something* (even duplicates have value)
2. Pity timer prevents frustration
3. Visual rarity distinction (colors, effects, auras)
4. Tradeable duplicates create player economy
5. Event-exclusive creates FOMO
6. Ultra-rare (1 in 1M) creates aspiration

### 3.2 The Rebirth Economy

**Standard Rebirth Pattern:**
```
Progress → Hit Wall → Rebirth (reset progress) → Get Multiplier → Progress Faster
     ↑                                                                    │
     └────────────────────────────────────────────────────────────────────┘
```

**Rebirth Design Rules:**
1. First rebirth should be achievable in 30-60 minutes
2. Multiplier should be significant (2x-2.5x minimum)
3. Some progress should carry (pets, collection, rank)
4. Higher rebirths should cost exponentially more
5. Bulk rebirth pricing for convenience
6. Rebirth count is a status symbol

### 3.3 The Trading Economy

**Trading creates player-driven market:**
- Duplicates have trade value
- Rarity determines market price
- Scam prevention (trade confirmation UI)
- Limited-time pets become valuable over time
- Trading drives social engagement

### 3.4 The Event Economy

**Event Design Pattern:**
```
Event Starts → New Currency/Items Available → Limited Time → Event Ends → Items Become Rare
                                                                              ↓
                                                                    Secondary Market Value
```

**Event Types:**
- Currency events (earn special tokens)
- Egg events (limited-time eggs with exclusive pets)
- Multiplier events (x2 luck, x2 earnings)
- Visit milestone events (community goals)
- Seasonal events (holiday-themed)

---

## 4. Monetization Architecture

### 4.1 Revenue Streams

| Stream | Implementation | Revenue Potential |
|--------|----------------|-------------------|
| Premium currency | Gems/Robux purchases | High (whales) |
| Game passes | Permanent perks | Medium (consistent) |
| Limited items | Event exclusives | High (FOMO) |
| Cosmetics | Skins, auras | Medium |
| Convenience | Autoclicker, speed boosts | Medium |
| Slot expansion | More pet/inventory slots | High (pay-to-progress) |

### 4.2 Pricing Psychology

- **$0.99 entry point** — Low barrier for first purchase
- **Bulk discounts** — Buy more, save more (10+1 free)
- **Time-limited offers** — "Only available this weekend!"
- **Tiered pricing** — $4.99, $9.99, $19.99, $49.99
- **Visual escalation** — Premium items look visibly better
- **Social proof** — Show others wearing/using premium items

### 4.3 Free-to-Play Balance

**F2P Player Journey:**
1. Start game → Immediate gratification (first pet/progress)
2. 5-10 min → First egg hatch (dopamine hit)
3. 30-60 min → First rebirth (prestige hook)
4. 1-2 hours → Encounter premium barrier (slower progress)
5. Days → Pity timer gives rare drop (retention)
6. Weeks → Trading economy engagement (social hook)

**Paying Player Journey:**
1. Buy first pack → Instant gratification
2. Buy game pass → Permanent advantage
3. Buy premium eggs → Better pets
4. Buy event items → Exclusive content
5. Buy cosmetics → Status display

---

## 5. Economy Balance Formulas

### 5.1 Income Formula
```
income_per_second = base_rate × pet_multiplier × rebirth_multiplier × zone_multiplier × event_multiplier × boost_multiplier
```

### 5.2 Egg Cost Formula
```
egg_cost = base_cost × (1 + eggs_purchased × increment_rate)
```

### 5.3 Rebirth Cost Formula
```
rebirth_cost = base_cost × growth_rate^current_rebirths
bulk_cost = sum(rebirth_cost(n) for n in range(count)) × (1 - bulk_discount)
```

### 5.4 Pity Timer Formula
```
if time_since_last_rare >= pity_threshold:
    force_rare_drop()
elif random() < drop_rate:
    drop_rare()
else:
    drop_common()
```

### 5.5 Zone Unlock Formula
```
zone_unlock_cost = base_cost × zone_number^scaling_factor
```

---

## 6. Economy Retention Mechanics

### 6.1 Daily Engagement
- Daily login rewards
- Daily quests (give reason to return)
- Limited-time events (FOMO)
- Trading market activity
- Leaderboard competition

### 6.2 Long-term Retention
- Rebirth system (infinite progression)
- Collection completion ("gotta catch em all")
- Trading economy (social engagement)
- New content updates (zones, pets, events)
- Social features (friends, trading, leaderboards)

### 6.3 Whale Mechanics
- Ultra-rare items (1 in 1M chance)
- Exclusive cosmetics (visual status)
- Leaderboard positions (competitive status)
- Bulk purchasing (value for money)
- Early access to new content

---

## 7. Blockchain Economy (IdleChain Design)

### 7.1 Token Economics
**From IDLECHAIN_DESIGN.md:**

- **Token:** SPL token on Solana
- **Earning:** Play-to-earn through idle gameplay
- **Spending:** Marketplace purchases (heroes, items)
- **Anti-inflation:** Token burning mechanics
- **Seasonal resets:** Prevent infinite accumulation

### 7.2 NFT Integration
- Hero NFTs with unique stats
- Tradable on marketplace
- Rarity tiers with visual distinction
- Staking mechanics (earn while not playing)

### 7.3 Anti-Cheat
- Server-authoritative validation
- Cryptographic proof of actions
- Rate limiting
- Bot detection
- Economic exploit prevention

---

## Summary

The Roblox game economy analysis reveals a consistent pattern across successful games:

1. **Simple core loop** — One action earns currency, currency buys progression
2. **Gacha system** — Random rewards drive engagement and monetization
3. **Prestige system** — Rebirth creates long-term retention
4. **Social economy** — Trading and leaderboards drive engagement
5. **Event economy** — Limited-time content creates FOMO and spending urgency
6. **Pity timers** — Ensure F2P players get rewarded (retention)
7. **Premium barriers** — Pay for convenience, exclusivity, and speed
8. **Visual status** — Rare items are visually distinct (social signaling)

The key insight: **the economy IS the game**. The core loop is designed to keep players earning and spending in a cycle that feels rewarding but never quite "complete," driving both engagement and monetization indefinitely.