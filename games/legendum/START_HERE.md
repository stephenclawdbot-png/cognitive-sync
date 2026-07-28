# 🎮 Legendum — START HERE: Build Guide

> **Role:** You are the Game Architect + Creative Director for a new life-simulation RPG roguelite.
> **Goal:** Build a game inspired by Legendum from scratch, bottom-up.

---

## 1. ELEVATOR PITCH

**"Stardew Valley meets Hades, but you live entire lives instead of farming or fighting through hell."**

A life-simulation RPG where each playthrough is one character's entire life — from youth to death. You make choices about jobs, relationships, combat, and adventure. When you die, your soul carries forward as perks for your next life. Every life is a run. Every death makes you stronger.

---

## 2. DESIGN PEG

### Visual Style
- **Reference:** 16-bit SNES-era pixel art (think Stardew Valley × Chrono Trigger)
- **Palette:** Warm, earthy tones for town life; cooler, darker tones for combat areas
- **Characters:** Top-down, 4-directional sprites with expressive portraits for dialog
- **UI:** Cozy, parchment-style panels with hand-drawn feel

### Game Feel
- **Pacing:** Slow and contemplative in town; snappy and tactical in combat
- **Juice:** Satisfying level-up bursts, perk unlock flashes, life-review montage at death
- **Audio:** Lo-fi ambient music in town; chiptune battle themes; soft acoustic for life events

### Tone
- **Emotional arc:** Wonder (youth) → Ambition (adulthood) → Reflection (old age) → Legacy (death)
- **Themes:** Mortality, choices, consequence, generational growth
- **Vibe:** "Cozy but consequential" — your choices matter because life is finite

### Design North Star
> **Every decision should feel like it matters, because every life ends.**

If a feature doesn't serve this feeling — cut it.

---

## 3. CORE LOOP

```
┌─────────────────────────────────────────┐
│              ONE LIFE (RUN)              │
│                                          │
│  Youth → Choose path → Learn skills      │
│    ↓                                     │
│  Adulthood → Work/Jobs → Combat/Explore  │
│    ↓                                     │
│  Adventure → Dungeons → Loot → Items     │
│    ↓                                     │
│  Old Age → Mentor → Reflect → Die        │
│    ↓                                     │
│  DEATH → Life Review → Legacy Points      │
│    ↓                                     │
│  REINCARNATE → Choose Soul Perks → Youth │
└─────────────────────────────────────────┘
```

**30-second loop:** Make a choice (job, fight, talk, explore) → See immediate result
**5-minute loop:** Complete a task/encounter → Gain skill XP → Feel progression
**30-minute loop:** Age a life stage → Unlock new opportunities → Plan next stage
**2-hour loop:** Live a full life → Die → Review life → Pick Soul Perks → Start new life

---

## 4. BOTTOM-UP ARCHITECTURE

### Layer 0: Engine Foundation
```
Godot 4.x Project
├── Core/
│   ├── Reactive State System (observable values)
│   ├── Save/Load System (JSON serialization)
│   ├── Calendar/Time System (days, seasons, years)
│   ├── Event Bus (global event dispatcher)
│   └── Scene Manager (transition system)
├── Data/
│   ├── items.json
│   ├── abilities.json
│   ├── perks.json
│   ├── enemies.json
│   ├── skills.json
│   ├── jobs.json
│   ├── narratives.json
│   └── shops.json
└── Game/
    └── GameManager (singleton, orchestrates everything)
```

**Build first:**
- [ ] Reactive state system (when stats change, UI auto-updates)
- [ ] Save/load (save game state to JSON)
- [ ] Calendar system (track days, advance time)
- [ ] Event bus (decouple systems — "on_day_passed", "on_combat_end", "on_death")

### Layer 1: Character + World
```
Character/
├── CharacterBody (movement, collision)
├── StatsComponent (6 attributes, derived stats)
├── SkillsComponent (skill levels, XP)
├── InventoryComponent (items, equipment)
├── AbilitiesComponent (equipped abilities)
├── PerksComponent (active soul perks)
└── LifeComponent (age, life stage, health)

World/
├── Town (walkable hub, NPCs, shops)
├── Wilderness (combat areas, dungeons)
├── NPC System (dialog, schedules, relationships)
└── Camera (follow player, bounds per area)
```

**Build second:**
- [ ] Character can walk in 4 directions on a tilemap
- [ ] Stats display in a simple HUD
- [ ] Camera follows player
- [ ] Can enter/exit buildings (scene transitions)
- [ ] NPC with a dialog box

### Layer 2: Combat + Stats + Items
```
Combat/
├── CombatSystem (turn-based or action)
├── DamageCalculator (type effectiveness, crit, defense)
├── AbilitySystem (6 combat styles, 14 abilities)
├── EnemyAI (simple AI: attack, defend, special)
└── StatusEffects (burn, poison, stun, buff)

Items/
├── ItemDatabase (load from JSON)
├── ItemInstance (id, rarity, stats, effects)
├── EquipmentSystem (equip/unequip, stat bonuses)
├── InventoryUI (grid, drag-drop, tooltips)
└── ShopSystem (buy/sell, stock, tiers)
```

**Build third:**
- [ ] Basic combat: player vs 1 enemy, attack/defend
- [ ] Stats affect combat (STR increases damage, etc.)
- [ ] Items drop from enemies, can be equipped
- [ ] Item rarity affects stat ranges
- [ ] Shop where you can buy/sell

### Layer 3: Progression + Economy + Meta
```
Progression/
├── SkillSystem (10+ skills, XP per skill, level-up effects)
├── JobSystem (jobs require energy, give gold + XP)
├── TaskSystem (daily/weekly tasks with rewards)
├── PerkWeb (node-based perk tree with prerequisites)
├── LegacySystem (Legacy Points earned at death)
└── SoulPerkSystem (meta-progression, persists across lives)

Economy/
├── GoldEconomy (earn from jobs/combat, spend in shops)
├── XPEconomy (skill XP, combat XP, job XP)
├── EnergySystem (regenerates over time, gates actions)
├── ShopPools (item pools per shop tier)
└── RarityDistribution (drop rates per rarity tier)
```

**Build fourth:**
- [ ] Skills gain XP and level up
- [ ] Jobs cost energy, give rewards
- [ ] Death triggers life review → Legacy Points
- [ ] Soul Perks can be chosen at reincarnation
- [ ] Perk web with prerequisites

### Layer 4: Content + Polish
```
Content/
├── NarrativeSystem (story web, choices, consequences)
├── DeedSystem (achievements tracked across lives)
├── JournalSystem (log of events, discoveries)
├── ContactsSystem (relationships with NPCs)
├── HeirloomSystem (items passed between lives)
├── CalendarSystem (seasons affect gameplay)
├── LifeReviewSystem (montage at death)
└── QuietYearsSystem (narrated time jumps)

Polish/
├── VFX (level-up, perk unlock, item drop, combat hits)
├── Audio (music per area, SFX per action)
├── UI Animation (smooth transitions, tween everything)
├── TutorialSystem (contextual tips)
├── SettingsMenu (audio, controls, accessibility)
└── GameFeel (screen shake on crit, hit pause on death)
```

**Build last:**
- [ ] Narrative choices with consequences
- [ ] Deeds tracked across lives
- [ ] Journal entries for discoveries
- [ ] Heirloom items inherit between lives
- [ ] Seasonal effects on gameplay
- [ ] Life review montage at death
- [ ] All VFX, audio, UI polish

---

## 5. BUILD ORDER (Priority Sequence)

| Priority | What | Why | Time |
|----------|------|-----|------|
| 1 | Reactive state system | Foundation — everything depends on it | 1 day |
| 2 | Character walking on tilemap | Prove the engine works | 1 day |
| 3 | Stats + HUD | See the numbers | 1 day |
| 4 | Basic combat (1 enemy) | Core loop prototype | 2 days |
| 5 | Items + inventory | Rewards from combat | 2 days |
| 6 | Death → reincarnation | Meta-progression loop | 2 days |
| 7 | Soul Perks | Feel the meta-growth | 1 day |
| 8 | Skills + XP | Long-term progression | 2 days |
| 9 | Jobs + energy | Non-combat gameplay | 2 days |
| 10 | Shops | Economy sink | 1 day |
| 11 | Perk web | Build variety | 3 days |
| 12 | Narrative system | Content depth | 5 days |
| 13 | NPC relationships | Social depth | 3 days |
| 14 | Calendar + seasons | Time pressure | 2 days |
| 15 | Life review + polish | Ship quality | 5 days |

**Total: ~30 days for a vertical slice with all systems working.**

---

## 6. PHASE BREAKDOWN

### Phase 0: Foundation (Days 1-2)
**Milestone:** Character walks on a map, stats show in HUD.

- [ ] Godot 4.x project created
- [ ] Tilemap with collision
- [ ] CharacterBody with 4-directional movement
- [ ] Camera follows player
- [ ] Stats HUD (STR, DEX, VIG, PER, INT, WIS)
- [ ] Reactive state system (stat changes update HUD automatically)
- [ ] Save/load to JSON

**Playtest:** Can you walk around? Do stats display? Can you save and load?

### Phase 1: Core Loop (Days 3-6)
**Milestone:** Fight an enemy, get loot, die, reincarnate with a perk.

- [ ] Basic combat system (attack, take damage, die)
- [ ] 1 enemy type with simple AI
- [ ] Damage calculation (STR → damage, VIG → health)
- [ ] Item drops from enemies
- [ ] Inventory + equipment (equip items, stats change)
- [ ] Death screen → life review summary
- [ ] Reincarnation → choose 1 Soul Perk
- [ ] Soul Perk affects next life (e.g., +10% STR)

**Playtest:** Can you fight, die, and come back stronger? Is the loop satisfying?

### Phase 2: Progression (Days 7-14)
**Milestone:** Skills level up, jobs work, shops exist, perk web is functional.

- [ ] Skill system (10+ skills, each gains XP from related actions)
- [ ] Job system (3+ jobs, cost energy, give gold + skill XP)
- [ ] Energy system (regenerates per day, gates actions)
- [ ] Shop system (buy/sell items, stock refreshes)
- [ ] Item rarity system (8 tiers with color coding)
- [ ] Perk web (10+ nodes with prerequisites, visual node tree)
- [ ] Calendar system (days advance, seasons change)
- [ ] Age system (character ages, life stages unlock content)

**Playtest:** Do you feel progression across a life? Do choices matter?

### Phase 3: Content (Days 15-24)
**Milestone:** Multiple life paths, narrative choices, NPCs with relationships.

- [ ] Narrative system (story nodes, choices, consequences)
- [ ] 5+ NPCs with dialog, schedules, relationships
- [ ] Contact system (relationship levels affect dialog/options)
- [ ] Deed system (track achievements across lives)
- [ ] Journal system (log discoveries, events)
- [ ] Heirloom system (items pass between lives)
- [ ] 20+ enemies across multiple combat areas
- [ ] 14 abilities across 6 combat styles
- [ ] 5+ shops with different item pools

**Playtest:** Are there multiple viable life paths? Does the world feel alive?

### Phase 4: Polish (Days 25-30)
**Milestone:** Game feels complete, juicy, and shippable as a demo.

- [ ] VFX for all major events (level-up, perk unlock, crit, death)
- [ ] Music per area (town, combat, boss, death, title)
- [ ] SFX for all actions (attack, hit, pickup, level-up, etc.)
- [ ] UI animation (tween transitions, hover effects)
- [ ] Life review montage (visual summary at death)
- [ ] Tutorial system (contextual tips for new players)
- [ ] Settings menu (volume, controls, accessibility)
- [ ] CRT shader or pixel-perfect rendering
- [ ] Game feel (screen shake, hit pause, particle bursts)

**Playtest:** Would a stranger understand it in 5 minutes? Would they play for 30?

---

## 7. DESIGN PEG BOARD

Print this. Pin it up. Check every feature against it.

```
┌─────────────────────────────────────────────────────┐
│                  LEGENDUM DESIGN PEG                 │
│                                                      │
│  PITCH: Stardew Valley meets Hades, but you live    │
│         entire lives instead of farming.             │
│                                                      │
│  FEEL:  Cozy but consequential                       │
│         Every choice matters because every life ends │
│                                                      │
│  LOOK:  16-bit pixel art, warm earthy tones           │
│         Top-down, 4-directional, expressive portraits │
│                                                      │
│  SOUND: Lo-fi town, chiptune combat, acoustic death  │
│                                                      │
│  LOOP:  Live → Choose → Fight → Die → Reincarnate    │
│                                                      │
│  HOOK:  "My character lived a whole life and died    │
│         — and I got stronger for the next one."      │
│                                                      │
│  CUT IF: It doesn't serve mortality, choice, or      │
│          legacy.                                     │
└─────────────────────────────────────────────────────┘
```

---

## 8. CRITICAL DESIGN DECISIONS

### Decision 1: Combat Style
**Question:** Turn-based or action combat?
- **Turn-based:** More strategic, easier to balance, fits "life sim" pacing
- **Action:** More exciting, better for streaming, harder to balance

**Recommendation:** Turn-based for first build. It's easier and fits the contemplative tone.

### Decision 2: Life Length
**Question:** How long is one life in real time?
- **30 minutes:** Quick roguelite runs, high replayability
- **2 hours:** Deep life simulation, more emotional investment
- **Variable:** Player-controlled pacing

**Recommendation:** 45-90 minutes per life. Long enough to feel a life, short enough to replay.

### Decision 3: Perk System Scope
**Question:** How big is the Soul Perk web?
- **Small (20 perks):** Easy to balance, clear choices
- **Medium (50 perks):** Good variety, some build diversity
- **Large (100+ perks):** Deep min-maxing, hard to balance

**Recommendation:** Start with 20 perks, expand to 50 after playtesting.

### Decision 4: Narrative Depth
**Question:** How branching is the narrative?
- **Linear:** Easier to build, less replayability
- **Branching:** More work, more replayability
- **Emergent:** Systems-driven (jobs + skills + relationships create stories)

**Recommendation:** Emergent first (systems create stories), add branching narrative nodes later.

---

## 9. TECH STACK

| Component | Tool |
|-----------|------|
| Engine | Godot 4.x |
| Language | GDScript |
| Data format | JSON for content, .tres for resources |
| Save format | JSON (or Godot ConfigFile) |
| Tilemap | Godot TileMap with terrain addon |
| Dialog | Custom dialog system (or Dialogic addon) |
| UI | Godot Control nodes + custom theme |
| Audio | Godot AudioStreamPlayer |
| Version control | Git |
| Pixel art | Aseprite (or PixelLab for AI-generated) |

---

## 10. ASSET CHECKLIST

### Minimum Viable Assets (Phase 0-1)
- [ ] Player sprite (4-directional walk, idle)
- [ ] 1 enemy sprite (idle, attack, death)
- [ ] 1 tileset (town + combat area)
- [ ] 5 item icons (weapon, armor, consumable, key, misc)
- [ ] UI panels (HUD, inventory, dialog box, death screen)
- [ ] 3 SFX (attack, hit, pickup)
- [ ] 2 music tracks (town, combat)

### Full Game Assets (Phase 2-4)
- [ ] Player sprite (4-dir walk, idle, attack, hurt, death) × 3 age stages
- [ ] 20+ enemy sprites (idle, attack, hurt, death)
- [ ] 5+ tilesets (town, 4 combat areas)
- [ ] 50+ item icons
- [ ] 14 ability icons
- [ ] 20+ perk icons
- [ ] 10+ NPC portraits
- [ ] Full UI theme (buttons, panels, fonts, scrollbars)
- [ ] 20+ SFX
- [ ] 8+ music tracks
- [ ] 10+ VFX sprites/animations
- [ ] Title screen art
- [ ] Death screen / life review art

---

## 11. THE 5-MINUTE TEST

When someone picks up your game for the first time, this is what they should experience:

```
Minute 0-1: Title screen → New Game → Character creation (simple)
Minute 1-2: Youth scene → Tutorial dialog → First choice (what skill?)
Minute 2-3: Walk around town → Talk to NPC → Get first quest
Minute 3-4: First combat → Win → Get loot → Equip item
Minute 4-5: Level up → Feel the progression → "Just one more thing..."
```

If the first 5 minutes aren't fun, nothing else matters. **Playtest the 5-minute test with 5 strangers before building anything past Phase 1.**

---

## 12. COMMON PITFALLS

| Pitfall | Fix |
|---------|-----|
| Building content before the loop works | Build the core loop first, add content later |
| Too many systems with no depth | Pick 3 core systems, make them deep |
| Stats too complex for new players | Show derived stats, hide the math |
| Death feels punishing, not motivating | Life review should celebrate, not punish |
| Too much dialog, not enough gameplay | 70% gameplay, 30% dialog |
| Perk web is overwhelming | Start with 20 perks, gate the rest |
| Save system breaks on update | Version your save data from day 1 |

---

## 13. FILE STRUCTURE TEMPLATE

```
project/
├── scenes/
│   ├── Core/          (GameManager, SaveManager, SceneManager)
│   ├── Character/     (Player, Enemy, NPC scenes)
│   ├── UI/            (HUD, Inventory, Dialog, Menus)
│   ├── Combat/        (Battle scene, ability VFX)
│   ├── Town/          (Town map, buildings, interiors)
│   ├── Wilderness/    (Combat areas, dungeons)
│   └── Narrative/     (Story scenes, life review)
├── scripts/
│   ├── Core/          (ReactiveState, EventBus, SaveSystem)
│   ├── Character/     (Stats, Skills, Inventory, Perks)
│   ├── Combat/        (DamageCalc, Abilities, EnemyAI)
│   ├── Systems/       (Calendar, Economy, Jobs, Tasks)
│   └── UI/            (HUD controller, Inventory UI, etc.)
├── data/
│   ├── items.json
│   ├── abilities.json
│   ├── perks.json
│   ├── enemies.json
│   ├── skills.json
│   ├── jobs.json
│   ├── narratives.json
│   └── shops.json
├── assets/
│   ├── sprites/
│   ├── audio/
│   ├── ui/
│   └── fonts/
└── project.godot
```

---

## 14. QUICK START CHECKLIST

```
□ Read GAME_MECHANICS.md (full spec)
□ Read ECONOMY.md (economy formulas)
□ Set up Godot 4.x project
□ Create reactive state system
□ Get character walking on a tilemap
□ Build basic combat (1 enemy)
□ Implement death → reincarnation loop
□ Playtest the 5-minute test
□ Build progression (skills, jobs, shops)
□ Build perk web
□ Add narrative system
□ Polish with VFX + audio
□ Playtest with 5 strangers
□ Ship a demo
```

**Start with Layer 0. Build the foundation. Everything else stacks on top.**