# 🎮 START HERE — Game Build Guides

> **You have 3 reverse-engineered games. This is your creative director's playbook for building new games based on each.**

---

## What's In This Folder

Each game folder now contains a **`START_HERE.md`** — a top-down, creative-director-level blueprint for building a new game inspired by that reverse-engineered title. Read that first. Then drill into `GAME_MECHANICS.md` and `ECONOMY.md` for the full design spec.

| Game | Type | Start Here | Full Spec |
|------|------|------------|-----------|
| **Legendum** | Life-sim RPG roguelite | [START_HERE.md](./legendum/START_HERE.md) | [GAME_MECHANICS.md](./legendum/GAME_MECHANICS.md) · [ECONOMY.md](./legendum/ECONOMY.md) |
| **Reverse Engine Roblox** | Roblox game patterns | [START_HERE.md](./reverse-engine-roblox/START_HERE.md) | [GAME_MECHANICS.md](./reverse-engine-roblox/GAME_MECHANICS.md) · [ECONOMY.md](./reverse-engine-roblox/ECONOMY.md) |
| **v1.0.00 "wizdung"** | Action RPG dungeon crawler | [START_HERE.md](./v1.0.00/START_HERE.md) | [GAME_MECHANICS.md](./v1.0.00/GAME_MECHANICS.md) · [ECONOMY.md](./v1.0.00/ECONOMY.md) |

---

## How To Use These Guides

### The Bottom-Up Philosophy

Every guide is structured **bottom-up**: you build the foundation first, then stack systems on top. This means:

```
Layer 0: Engine + Core Loop Skeleton     ← Build this first
Layer 1: Character + Movement + Camera   ← Make it feel good
Layer 2: Stats + Combat + Items           ← Make it playable
Layer 3: Progression + Economy + Enemies ← Make it addictive
Layer 4: Content + Polish + Juice        ← Make it ship
```

**Never skip layers.** A game with great progression but bad movement will fail. A game with great content but no core loop will drift. Build the foundation, then stack.

### The Design Peg

Each guide includes a **Design Peg** — a north star reference that defines:

- **Visual style** — What does it look like?
- **Game feel** — What does it feel like to play?
- **Tone** — What emotion does it evoke?
- **Elevator pitch** — "X meets Y" in one sentence

Print this. Pin it to your wall. When you're deciding whether to add a feature, check it against the peg. If it doesn't serve the peg, cut it.

### The Phase System

Each guide breaks development into **phases** — each phase produces a **playable milestone**:

- **Phase 0** — Engine setup + walking character (1-2 days)
- **Phase 1** — Core combat loop (3-5 days)
- **Phase 2** — Progression + items (5-7 days)
- **Phase 3** — Content systems (7-14 days)
- **Phase 4** — Polish + juice (5-7 days)

By the end of each phase, you should be able to **play the game** and feel the difference. If you can't play it, you're not done with the phase.

---

## The Creative Director's Checklist

Before you start building any of these games, answer these questions:

### 1. What's the ONE thing?
> If your game does nothing else, what's the single mechanic that makes someone say "just one more run"?

- **Legendum:** "My character lived a whole life and died — and I got stronger for the next one."
- **wizdung:** "I found a legendary item in a dungeon and my build completely changed."
- **Roblox (your pick):** Define your own — what's the hook?

### 2. What's the core loop?
> What does the player do every 30 seconds? Every 5 minutes? Every 30 minutes?

Write it as a cycle. If you can't draw the cycle as a circle, your loop has a leak.

### 3. What's the 5-minute experience?
> A new player picks up your game. What happens in the first 5 minutes?

If the first 5 minutes aren't fun, nothing else matters.

### 4. What's the failure state?
> What happens when the player loses? Is it punishing? Educational? Quick?

Good failure states make the player want to try again, not quit.

### 5. What's the 50-hour experience?
> What keeps someone playing after 50 hours? What's the long-term hook?

If you can't answer this, your game will have a 2-hour retention ceiling.

---

## Architecture Principles (All Games)

### 1. Data-Driven Design
Separate **data** from **logic**. Items, enemies, skills, levels should be defined in data files (JSON, .tres, CSV), not hardcoded. This lets you add content without touching code.

### 2. State Machines for Characters
Every character (player + enemy) should have a state machine: Idle → Walk → Attack → Hit → Death. This prevents animation bugs and makes adding new states trivial.

### 3. Modular Behavior System
Don't hardcode what a skill does. Build a behavior system where skills are composed of modular behaviors (projectile, AOE, dash, status effect). This lets you create new skills by combining behaviors.

### 4. Curve-Based Scaling
Every number that scales with level should use a **curve** (animation curve, math function), not a flat formula. This gives you control over difficulty progression by editing curves, not rewriting code.

### 5. Pool Everything
Objects that spawn/despawn frequently (projectiles, loot, VFX, enemies) should be **pooled** — pre-allocated and reused, not instantiated/destroyed. This prevents GC spikes.

### 6. Build Vertical Slice Early
Don't build all content first. Build **one complete vertical slice** — one character, one enemy, one level, one item, one skill — that goes through every system. Then scale horizontally.

---

## Cross-Game Patterns

All 3 reverse-engineered games share these patterns:

| Pattern | Legendum | wizdung | Roblox Games |
|---------|----------|---------|--------------|
| **Stat system** | 6 attributes → derived stats | 4 attributes → 40+ stats | Multiplier-based |
| **Rarity tiers** | 8 tiers | 5 tiers + unidentified | Gacha rarity |
| **Progression reset** | Death → reincarnation with perks | Hub → dungeon run | Rebirth/prestige |
| **Economy** | Gold + XP + Legacy Points | Gold + XP + Mana | Multi-currency |
| **Content gating** | Age/life stage | Keys + room level | Unlock costs |
| **Meta-progression** | Soul Perks web | Stash + character switch | Rebirth multipliers |

**Takeaway:** No matter which game you build, you need: a stat system, a rarity system, a progression reset mechanic, an economy, content gating, and meta-progression. The guides tell you how each game implements these.

---

## Quick Decision Matrix

| If you want... | Build... |
|----------------|---------|
| A deep single-player RPG with life simulation | Legendum-style |
| A tight combat-focused dungeon crawler | wizdung-style |
| A viral multiplayer casual game | Roblox-style |
| Deep build variety + min-maxing | wizdung-style |
| Long-term progression across "lives" | Legendum-style |
| Social virality + monetization | Roblox-style |

---

## Next Steps

1. **Read the START_HERE.md** for the game you want to build
2. **Read GAME_MECHANICS.md** for the full system spec
3. **Read ECONOMY.md** for the economy design
4. **Set up your engine** (Godot 4.x for Legendum/wizdung, Roblox Studio for Roblox)
5. **Build Phase 0** — get a character walking on screen
6. **Iterate** — playtest after every phase

**You can build all 3 games. Start with the one that excites you most.**