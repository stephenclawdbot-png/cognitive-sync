# House Tycoon - Complete Game Analysis

**Game Type:** Idle/Clicker Tycoon  
**Platform:** Roblox  
**Analyzed:** 2026-01-26  

---

## Core Game Loop

```
TAP/CLICK → Earn Cash → Buy Upgrades → Increase Income → REBIRTH → Repeat with multipliers
```

---

## Currency System

| Currency | Icon | Purpose |
|----------|------|---------|
| **Cash ($)** | Green $ | Main currency, earn by tapping/idle |
| **Gems** | Blue diamond | Premium currency |
| **Keys** | Blue key | Event currency (for special chests) |
| **Rebirths** | Cycle icon | Prestige currency |

---

## Income System

- **Base income:** Earn $/second passively
- **Tap multiplier:** Increases tap value (1x, 1.1x, etc.)
- **Observed rates:** $2/s → $13/s (after upgrades)

---

## Rebirth System (DETAILED)

**"Rebirthing resets your cash!"**

| Rebirth Package | Cost | Value Ratio |
|-----------------|------|-------------|
| +1 Rebirth | $1.5K | $1,500/rebirth |
| +5 Rebirths | $5.5K | $1,100/rebirth |
| +15 Rebirths | $15.5K | $1,033/rebirth |
| +35 Rebirths | $35.5K | $1,014/rebirth |
| +70 Rebirths | $70.5K | $1,007/rebirth |

**Key Insight:** Bulk rebirth purchases are more efficient (lower $/rebirth)

**Rebirth Multiplier:** 2.5x (shown in UI)

---

## UI Layout

### Top Bar
- **Cash display** ($2,283)
- **Income rate** ($13/s)
- **Floors** - Building progression
- **Daily** - Daily rewards (! notification)
- **Index** - Collection/achievements
- **Timer** (14:19) - Event countdown

### Left Side
- **Gems** (0)
- **Rebirths** (1)
- **Shop** button (red basket, "NEW!" badge)
- **Medal/Achievement** button

### Right Side
- **x2 Cash** (99 remaining) - Temporary boost
- **Auto Collect** (29 remaining) - Auto-pickup

### Bottom Bar
- **Keys** (5)
- **Boost indicators** (+0%, +5%)
- **Auto** toggle (On/Off)
- **Tap/Click** area (main interaction)
- **Rebirth** button (! when available)

---

## Upgrade System (Observed)

From upgrade panel glimpses:
- **Decor Limit** (0/6) - Decoration slots
- **Tap Button** upgrades - Increase tap value
- **Luck Boost** (0% → higher) - Better drops
- **Gems Boost** (0/6) - Gem earning rate

---

## Events & Special Features

### 10M Visits Event
- Special "10M Demon" reward
- Odds: 1 in 250,000
- Requires keys to participate
- "You need more keys!" prompt

### Temporary Boosts
- x2 Cash (limited uses)
- Auto Collect (limited uses)

---

## Gameplay Areas

- **Starting area** - Red brick path, basic buildings
- **Shop area** - Purchase upgrades
- **Upgrades building** - Yellow/tan structure
- **Mystery boxes** - Red boxes with "?" (use keys)
- **Water moat** - Decorative boundary
- **Multi-floor buildings** - Glass towers, brick buildings

---

## Monetization Vectors (Predicted)

1. **Gems** - Premium currency (Robux purchase)
2. **x2 Cash passes** - Boost refills
3. **Auto Collect passes** - Convenience
4. **VIP/Gamepass** - Permanent boosts
5. **Keys** - Event participation

---

## Clone Implementation Checklist

### Core Systems
- [ ] Click/tap earning system
- [ ] Passive income ($/second)
- [ ] Cash display with income rate
- [ ] Rebirth system with bulk options
- [ ] Rebirth multiplier (2.5x base)

### Currencies
- [ ] Main cash
- [ ] Premium gems
- [ ] Event keys
- [ ] Rebirth counter

### UI Components
- [ ] Top bar (cash, income, nav buttons)
- [ ] Left sidebar (currencies, shop)
- [ ] Right sidebar (boosts)
- [ ] Bottom bar (auto, tap, rebirth)
- [ ] Popup menus (rebirth panel)

### Features
- [ ] Auto-tap toggle
- [ ] Auto-collect system
- [ ] Daily rewards
- [ ] Achievement/Index system
- [ ] Floor/level progression
- [ ] Temporary boosts (x2 cash)

### Events
- [ ] Visit milestone events
- [ ] Mystery box/chest system
- [ ] Key-based rewards
- [ ] Rare item odds display

### World
- [ ] Building upgrades (visual)
- [ ] Multiple areas/zones
- [ ] Decorative elements
- [ ] Player avatar customization

---

## Key Metrics for Balancing

| Metric | Observed Value |
|--------|----------------|
| Starting income | ~$2/s |
| Mid-game income | ~$13/s |
| First rebirth cost | $1,500 |
| Rebirth multiplier | 2.5x |
| Bulk rebirth discount | ~33% at max tier |
| Event rare odds | 1/250,000 |

---

## Design Notes

1. **Rebirth bulk pricing** creates interesting decision: save up for efficiency vs. rebirth early for multiplier
2. **Limited boosts** (99x, 29x) create urgency and monetization opportunity
3. **Key system** gates event content, encouraging daily play
4. **Visual progression** (buildings) gives sense of accomplishment
5. **Multiple currencies** allows segmented monetization

---

*Analysis by Max - Clawdbot Game Research*
*Session: 2026-01-26*
