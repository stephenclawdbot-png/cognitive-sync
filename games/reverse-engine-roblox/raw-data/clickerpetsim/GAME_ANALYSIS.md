# Tap Simulator - Game Analysis

**Game:** [TREATS!] Tap Simulator  
**Developer:** Cursor Makers  
**Platform:** Roblox  
**Analyzed:** 2026-01-26  

---

## Core Loop

1. **Click/Tap** → Earn clicks (currency)
2. **Buy Eggs** → Open eggs to get pets
3. **Pets boost income** → Passive/active multipliers
4. **Rebirth** → Reset progress for permanent multipliers
5. **Repeat** with higher earnings

---

## Currencies

| Currency | Icon | Purpose |
|----------|------|---------|
| Clicks | Cursor icon | Main currency, earn by tapping |
| Gems | Blue diamond | Premium currency |
| Rebirths | Green cycle icon | Prestige level |

---

## UI Layout

### Left Side
- **Rebirths counter** (0 Rebirths)
- **Clicks/sec** (passive income rate)
- **Total clicks** (main currency display)
- **Gems** (premium currency)

### Bottom Left
- **Shop** (red basket) - Buy upgrades
- **Trade** (orange arrows) - Player trading
- **Codes** (purple ABX) - Redeem codes

### Bottom Center
- **Pets** (paw icon) - View/manage pets
- **Click multiplier** (+7 shown)
- **Autoclicker** (toggle Off/On)

### Right Side
- **Quests panel** - Daily/progression quests

### Top
- **Event timer** (Electric Wheel, Portals)
- **Special egg areas** (Lightning Egg)

---

## Mechanics Observed

### Rebirth System
- First rebirth requires **1,000 clicks**
- Progress shown: "Save up 434/1k for first rebirth!"
- Rebirths likely give permanent multipliers

### Eggs & Pets
- **Basic Egg** - Starter eggs
- **Lightning Egg** - Special/rare eggs
- Pets follow player
- Pet observed: "Zeck" (brown creature)

### Events
- **Electric Wheel** - Spin for rewards
- **Portals** - Timed event (2:18:03 countdown)
- **Empyrean Sovereign** - Rare pet (1 in 1,000,000 chance)

### Quests
| Quest | Reward |
|-------|--------|
| Open a Basic egg | x100 |
| Open 5 Basic eggs | x1 (item?) |
| Get 1 rebirth | x500 |

---

## Areas/Zones

- **Plaza** - "Trade and sell your pets & items"
- Starting area (sandy ground)
- Egg purchase areas (visible machines)
- Portal zone (right side)

---

## Monetization (Predicted)

- Gem purchases (premium currency)
- Autoclicker unlock (possibly premium)
- Special eggs/pets
- Event passes

---

## Clone Checklist

- [ ] Click-to-earn system
- [ ] Currency display UI
- [ ] Rebirth/prestige system
- [ ] Egg gacha system
- [ ] Pet following system
- [ ] Pet inventory
- [ ] Quest system
- [ ] Shop system
- [ ] Trading system
- [ ] Code redemption
- [ ] Event system with timers
- [ ] Multiple zones/areas

---

*Analysis by Max - Clawdbot Game Research*
