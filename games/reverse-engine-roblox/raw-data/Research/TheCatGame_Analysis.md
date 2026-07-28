# The Cat Game :3 — Complete Analysis

**Game:** The Cat Game :3
**Researched:** 2026-02-23
**By:** Admiral + Max

---

## 🎮 Core Loop

```
Buy Food → Feed Cats → Cats Generate ¥/s → Sell Cats → Buy More Food → Repeat
```

**Idle income mechanic:** Cats passively generate Yen per second based on:
1. **Cat Type** (biggest factor — Void, Alien, etc.)
2. **Weight** (heavier = more income)
3. **Rarity** (Common < Uncommon < Rare < Legendary < Mythic < Impossible)

---

## 💰 Economy & Currency

**Currency:** ¥ (Yen)

**Scaling observed during session:**
- Started: ¥0
- 5 min: ¥5K
- 10 min: ¥1M
- 15 min: ¥1B
- 20 min: ¥1T
- End: ¥27Qi (Quintillion)

**Leaderboard shows:** Players with 590+ **Nonillion** (10^30)

---

## 🐱 Cat Rarity Tiers

| Tier | Color | Example Cats |
|------|-------|--------------|
| Common | White | Basic Cat |
| Uncommon | Cyan | Grey Long Cat, Orange Fat Cat |
| Rare | Green | Bull Cat, Pizza Delivery Cat |
| Legendary | Pink/Magenta | Skeleton Cat, Evil Spirit Cat, Luck Cat |
| Mythic | Purple | Alien Cat, Knight Cat |
| Impossible | ??? | Painter Cat (¥9.5B value) |

---

## 📊 Income Examples (Weight Matters!)

| Cat | Weight | Rarity | Income |
|-----|--------|--------|--------|
| Bull Cat | 1.33lbs | Rare | ¥11/s |
| Grey Long Cat | 1.52lbs | Uncommon | ¥52/s |
| Void Bull Cat | 1.07lbs | Rare | ¥469/s |
| Orange Bull Cat | 2.44lbs | Rare | ¥1,220/s |
| Pizza Delivery Cat | 1lbs | Rare | ¥1,875/s |
| Alien Cat | 4lbs | Mythic | ¥62,500/s |

**Key insight:** Cat TYPE > Weight > Rarity for income. Void/Alien variants have massive multipliers.

---

## 🍖 Food System

**Food Booth:** Buy food to place for cats

**Food Mutation Chances:**
| Rarity | Chance |
|--------|--------|
| Gold | 12% |
| Diamond | 7% |
| Platinum | 5% |
| Emerald | 3% |
| Ruby | 2% |
| Rainbow | 1% |

**Food Types Seen:**
- Fish
- Chicken
- Canned Cat Food
- Sushi Pizza

**Trash Food:** Dispose unwanted food at trash bin

---

## 🌦️ Weather System

**Weather events cycle every ~10 minutes**

| Weather | Effect |
|---------|--------|
| Snow ❄️ | "Small chance to mutate cats while snowing" |
| Rain 🌧️ | "Small chance to mutate cats while raining" |

**SKIP button:** Pay to trigger weather early (monetization)

---

## 🧬 Fusion System

**Fuse Cats menu** — Combine specific cats to create rarer ones

**Warning:** "Cat mutations / weight WON'T carry over. Fused cats will have a random weight"

**Example Recipes:**
- Bicycle Cat + Bigfoot Cat = **Bicycle Bigfoot** (15m)
- Hamburger + Burrito + Taco + Lazy Cat = **Hungry Cat** (15m)
- Evil + Good Cats → Genie + All-Seeing = **Evil Spirit Cat**

**Timer:** Fusion takes 15 minutes

---

## 📖 Journal / Collection

**Categories:**
- Normal
- Fused
- Daily
- Party
- Valentines (seasonal)
- Taco (themed)
- Memes

**Pokédex-style:** Silhouettes for undiscovered cats

**Example Legendary cats:**
- Skeleton Cat
- Bicycle Bigfoot
- Hungry Cat
- Evil Spirit Cat
- Luck Cat (rainbow unicorn)

**Higher tier (Orange/Gold):**
- Super Catman
- Super Phoenix Cat
- King of the Cats

---

## 🏠 Plot System

**Personal plot:** Fenced area for your cats

**Max Cats:** Upgradeable limit (started at ~20, upgradeable to 26+)

**Upgrade costs:**
- Early: ¥218,893
- Mid: ¥1.6 Trillion
- Late: Requires Robux OR massive grind

**Plot sign:** Shows your username + max cats

---

## 💵 Monetization

**Robux purchases:**
- "Upgrade Max Cats" — R$29
- Weather SKIP — instant weather trigger
- 500 + 400 bonus Robux bundle = Rp90,000 (IDR)

**Pay-or-grind model:** Can upgrade with in-game currency OR Robux

---

## 🤝 Trading / Gifting

**"Hold out cat to gift"** — Trade cats with other players

**Trade popup shows:**
- Cat name
- Rarity
- **Value in ¥** (transparency!)

**Example trades received:**
- Knight Cat (Mythic) — Worth ¥281,250,000
- Painter Cat (Impossible) — Worth ¥9,562,499,821

---

## 🏪 Shops

| Shop | Function |
|------|----------|
| BUY FOOD | Purchase food items |
| GEARS | Equipment/accessories |
| SELL CATS | Sell cats for ¥ |
| TRASH FOOD | Dispose unwanted food |

**Sell dialog options:**
- "Tell me a cat fact"
- "Sell inventory" (bulk)
- "Sell item" (individual)
- "How much is this worth?"

---

## 🎨 Visual Style

**Aesthetic:** Blocky/LEGO-like Minecraft style

**Cats:** Chunky pixel art, very cute

**Size scaling:** Heavier cats appear LARGER

**VFX:**
- Green glow = selected
- Purple portal = spawning
- Fire/sparkles = special cats
- Coins rain from sky during income

---

## 🏆 Leaderboard

Shows top players by total ¥ earned

Top players have **Nonillion** (10^30) amounts

---

## 🔑 Key Mechanics Summary

1. **Idle Income** — Cats generate ¥/s passively
2. **Weight System** — Heavier = more income + bigger model
3. **Type Variants** — Void, Alien, etc. have huge multipliers
4. **Food Mutations** — RNG rarity when feeding
5. **Weather Bonuses** — Time-limited mutation boosts
6. **Fusion** — Combine cats for rarer ones
7. **Collection** — Journal tracks all discovered cats
8. **Trading** — Player-to-player gifting with value display
9. **Upgrades** — Max cats limit, plot expansions
10. **Leaderboard** — Competitive element

---

## 💡 What Makes It Work

**Satisfying loops:**
- Coins raining = dopamine
- Cats growing bigger = visual progress
- Collection completion = completionist hook
- Trading rare cats = social status

**Monetization hooks:**
- Max cats limit (pay to expand faster)
- Weather skip (impatience tax)
- Cosmetics (assumed from GEARS shop)

**Retention:**
- Weather events every 10 min
- Daily cats category
- Seasonal content (Valentines)
- Trading economy

---

## 🎯 Takeaways for Our Game

1. **Weight/size scaling** is satisfying — visual feedback
2. **Weather events** create urgency without being annoying
3. **Transparent trade values** build trust
4. **Fusion with timers** = engagement + wait mechanic
5. **Extreme number scaling** (Quintillion+) feels epic
6. **Blocky cute style** is universally appealing
7. **Collection journal** drives completionism
8. **Type variants** (Void, Alien) add depth to rarity

---

*Notes compiled by Max ⚡*
