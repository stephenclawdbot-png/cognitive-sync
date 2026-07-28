# Reverse Engine Roblox — Game Mechanics Document

**Type:** Roblox game analysis & reverse engineering collection  
**Author:** Max (Clawdbot Game Research)  
**Date:** 2026-01-2x  
**Source:** Reverse Engine Roblox.zip (91MB)  

---

## 1. Overview

This is a **research collection** of reverse-engineered Roblox games, game design theory, and original game concepts. It contains:

- **9 game analysis folders** with screenshots, session logs, and GAME_ANALYSIS.md files
- **Design theory documents** (Universal Game Thesis, Viral Formula, Experimentation)
- **5 mobile game concepts** (Mobile Game Bible)
- **IdleChain design doc** (idle game with Solana token economy)
- **60+ game idea documents** in the Ideas folder
- **Tool infrastructure** for automated Roblox game analysis

---

## 2. Analyzed Games

### 2.1 Catch a Monster (Pokémon-style Collector)
**Status:** Full GAME_ANALYSIS.md available

**Core Loop:**
1. Explore world → Encounter wild monsters
2. Throw capture device → Catch monster (probability-based)
3. Level up monsters → Battle other trainers
4. Trade monsters → Get rare variants
5. Complete quests → Earn currency
6. Repeat with stronger monsters

**Currencies:**
| Currency | Source | Use |
|----------|--------|-----|
| Cash | Selling, quests | Basic purchases |
| Robux | Real money | Premium pets, items |
| Event Tokens | Events | Limited-time items |

**Key Mechanics:**
- Level-gated pet slots (more slots at higher levels)
- Weekly leaderboards (top players get rewards)
- Friend luck system (friends boost your capture rate)
- World portal system (travel between worlds)
- Mount system (ride certain pets)
- Monster rarity tiers (Common → Rare → Epic → Legendary → Secret)
- Egg hatching system with pity timer

**Economy:**
- Cash is earned by selling duplicate monsters and completing quests
- Robux buys premium eggs, game passes, and cosmetics
- Event tokens earned during limited-time events
- Trading economy between players (player-driven market)

### 2.2 Tap Simulator (Clicker + Pet Collector)
**Status:** Full GAME_ANALYSIS.md available

**Core Loop:**
1. Click/tap → Earn clicks (currency)
2. Buy eggs → Open eggs to get pets
3. Pets boost income → Passive/active multipliers
4. Rebirth → Reset progress for permanent multipliers
5. Repeat with higher earnings

**Currencies:**
| Currency | Source | Use |
|----------|--------|-----|
| Clicks | Tapping, passive income | Main currency |
| Gems | Premium purchases, events | Premium items |
| Rebirths | Rebirth milestone | Prestige counter |

**Key Mechanics:**
- Click multiplier (shown as +7 in UI)
- Autoclicker toggle (premium feature)
- Rebirth system (first rebirth at 1,000 clicks, 71 rebirths observed)
- Egg hatching with rarity variants (Rainbow, Golden, Glitch)
- Zone progression (unlock new areas with more clicks)
- Quest system (daily/progression quests)
- Trading system (player-to-player)
- Code redemption (promotional codes)
- Event system with timers (Electric Wheel, Portals)
- Special pets (Empyrean Sovereign — 1 in 1,000,000 chance)

**Economy:**
- Clicks scale with pets and rebirths
- Gems are premium currency for special eggs
- Rebirth multipliers compound with pet multipliers
- Zones gate progression (need X clicks to unlock)

### 2.3 Your Zoo (Zoo Tycoon + Gacha)
**Status:** Full GAME_ANALYSIS.md available

**Core Loop:**
1. Build zoo enclosures → Attract visitors
2. Earn cash from visitors → Buy gacha eggs
3. Hatch animals → Display in zoo
4. Collect all animals → Complete collection
5. Rebirth → Keep animals, reset cash
6. Repeat with better zoo

**Currencies:**
| Currency | Source | Use |
|----------|--------|-----|
| Cash | Zoo visitors, offline earnings | Buy eggs, build enclosures |
| Robux | Real money | Premium eggs, speed boosts |

**Key Mechanics:**
- Pity timer system:
  - Golden: 47 seconds
  - Rainbow: 4 minutes 47 seconds
  - Secret: 14 minutes 47 seconds
- Offline earnings (zoo generates income while away)
- Rebirth keeps animals (only resets cash/progress)
- "Collect all" completion system
- Gacha egg system with rarity tiers

**Economy:**
- Cash flows from visitors → eggs → more animals → more visitors
- Offline earnings create idle game loop
- Pity timers ensure F2P players get rare drops eventually
- Rebirth is soft (keeps collection, resets economy)

### 2.4 House Tycoon (Idle/Clicker Tycoon)
**Status:** Full GAME_ANALYSIS.md available

**Core Loop:**
1. Click to earn cash → Build house parts
2. Buy upgrades → Increase income
3. Rebirth → Reset for multiplier
4. Repeat with higher multiplier

**Currencies:**
| Currency | Source | Use |
|----------|--------|-----|
| Cash | Clicking, idle income | Build, upgrade |
| Gems | Premium | Special upgrades |
| Keys | Events/quests | Unlock special content |
| Rebirths | Rebirth milestone | Permanent multiplier |

**Key Mechanics:**
- Bulk rebirth pricing tiers (cost scales with count)
- 2.5x multiplier per rebirth
- Upgrade system (incremental improvements)
- 10M visits event (1 in 250,000 odds for special reward)
- Idle income (generates cash while away)

**Economy:**
- Linear cash scaling with upgrades
- Rebirth multiplier (2.5x) creates exponential growth
- Keys gate special content
- Event rewards create FOMO

### 2.5 Clicker Pet Sim (Clicker + Pet Sim)
**Status:** GAME_ANALYSIS.md available (2.5KB)

**Core Loop:**
1. Click to earn → Buy eggs → Get pets
2. Pets boost income → Click more
3. Rebirth → Reset for multiplier
4. Trade pets → Get better ones

**Currencies:** Clicks, Gems, Rebirths (same as Tap Simulator)

**Key Mechanics:**
- Click-to-earn system
- Egg gacha system
- Pet following system
- Rebirth/prestige system
- Quest system
- Shop system
- Trading system
- Code redemption
- Event system with timers
- Multiple zones/areas

### 2.6 Other Analyzed Games (Screenshots Only)
| Game | Folder | Analysis Status |
|------|--------|-----------------|
| Adopt Me | adoptme/ | Screenshots + session JSONL only |
| Auto Eye | autoeye/ | README only |
| Grow a Country | growacountry/ | Screenshots only |
| Meme Game | memegame/ | Screenshots only |

---

## 3. Design Theory Documents

### 3.1 Universal Game Thesis
**File:** UNIVERSAL_GAME_THESIS.md

**10 Universal Satisfactions:**
1. Slicing — Cutting through things
2. Smashing — Breaking/destroying
3. Growing — Getting bigger/stronger
4. Completing — Finishing collections
5. Surviving — Last one standing
6. Catching — Capturing targets
7. Matching — Finding pairs/sorting
8. Bonking — Hitting things
9. Avoiding — Dodging obstacles
10. Chasing — Pursuing targets

**8 Game Loops:**
1. Timer-Reveal (wait → reveal → react)
2. Action-Reveal (act → reveal → react)
3. Asymmetric Hunt (hunter vs hunted)
4. Collection Loop (gather → complete → reward)
5. Growth Loop (earn → upgrade → earn more)
6. Survival Loop (survive → last standing → win)
7. Social Loop (interact → trade → status)
8. Prestige Loop (progress → reset → permanent bonus)

**3 Proven Formulas:**
1. **Timer-Reveal Formula:** Hidden information + timed reveal + dramatic reaction
2. **Action-Reveal Formula:** Player action + hidden consequence + reaction
3. **Asymmetric Hunt Formula:** One hunter, many prey (or vice versa)

### 3.2 Viral Formula
**File:** VIRAL_FORMULA.md

**Case Study: Knockout! (50K+ CCU)**

**Formula:**
```
Universal Satisfaction + Cute Theme + Hidden Decisions + Dramatic Reveal + Physics Comedy = VIRAL
```

**Checklist:**
- [ ] Core mechanic taps a universal satisfaction
- [ ] Theme is cute/broadly appealing
- [ ] Players make hidden decisions (creates suspense)
- [ ] Dramatic reveal moment
- [ ] Physics-based comedy (ragdolls, knockback, chaos)
- [ ] Simple controls (mobile-friendly)
- [ ] Short rounds (2-5 minutes)
- [ ] Spectator-friendly (fun to watch)

**Untapped Physics Concepts:**
- Buoyancy/floatation
- Elastic/rubber physics
- Wind/aerodynamics
- Magnetism
- Surface tension

### 3.3 Experimentation — Formulas D-Q
**File:** EXPERIMENTATION.md

| Formula | Name | Core Mechanic |
|---------|------|---------------|
| D | Reaction | React to stimulus fastest |
| E | Timing | Time your action perfectly |
| F | Chaos Race | Race through chaotic obstacles |
| G | Bluff | Hidden information, poker-style |
| H | Risk Bet | Risk resources for bigger reward |
| I | Memory | Remember and recall |
| J | Rhythm | Time actions to beat |
| K | Infection | Spread/avoid infection |
| L | Stack & Collapse | Build tower, knock down |
| M | Shrinking Resources | Resources deplete over time |
| N | Escalating Chaos | Difficulty increases over time |
| O | Sacrifice | Give up something to gain |
| P | Spectator Power | Viewers affect gameplay |
| Q | Copycat | Mimic others' actions |

### 3.4 Mobile Game Bible
**File:** MOBILE_GAME_BIBLE.md

**5 Mobile Game Concepts:**

1. **Parachute Panic** — Skydiving with obstacle avoidance
2. **Snowball Fight** — Roll snowball, throw at opponents
3. **Grapple Yeet** — Grappling hook physics, yeet opponents
4. **Crown Rush** — Grab crown, hold it longest
5. **Duck Dodge** — Dodge obstacles, last standing

**Mobile Optimization Rules:**
- One-thumb controls
- 2-3 minute rounds
- Portrait orientation preferred
- Minimal UI
- Big tap targets
- Haptic feedback
- Vertical video friendly (for sharing)

### 3.5 IdleChain Design
**File:** IDLECHAIN_DESIGN.md

**Genre:** Idle hero/dungeon grinder with blockchain economy

**Architecture:**
- Frontend: Unity or Godot
- Backend: Supabase + Solana Anchor
- Anti-cheat: Server-authoritative with cryptographic verification
- Token economy: SPL token on Solana

**Key Systems:**
- Hero NFTs with stats and abilities
- Dungeon auto-battler
- Resource generation (idle mining)
- Marketplace (buy/sell heroes)
- Hub/Flex layer (social space)
- Seasonal content

---

## 4. Game Ideas (60+ Concepts)

### 4.1 Key Game Ideas
| Game | File | Core Concept |
|------|------|---------------|
| CloneChaos | CloneChaos.md | Turn-based clone strategy |
| GrappleWars | GrappleWars.md | Turn-based grappling |
| InfectionPuppyEdition | InfectionPuppyEdition.md | Turn-based infection game |
| Kingmaker | Kingmaker.md | King/crown game |
| PenguinBowling | PenguinBowling_V4_FINAL_POTENTIAL.md | Turn-based bowling (players are pins/ball) |
| ShrinkRay | ShrinkRay.md | Shrink opponents |
| SumoSlap | SumoSlap.md | Turn-based sumo stomp |
| BalloonPopBattle | BalloonPopBattle.md | Balloon popping combat |
| BombSquad | BombSquad.md | Bomb defusal/throwing |
| BouncyCastleBump | BouncyCastleBump.md | Castle bouncing physics |
| BrainrotMusicalChairs | BrainrotMusicalChairs.md | Musical chairs with brainrot meme theme |
| BubbleBattle | BubbleBattle_POTENTIAL.md | Bubble physics combat |
| Buildbreak | Buildbreak.md | Build and break structures |
| CaptureTheCrown | CaptureTheCrown.md | Crown capture game |
| CatapultChaos | CatapultChaos.md | Catapult physics game |
| CatBurglar | CatBurglar.md | Steal as a cat |
| ChainLink | ChainLink_POTENTIAL.md | Chain physics game |
| ChainReaction | ChainReaction.md | Domino chain reaction |
| ColorDash | ColorDash.md | Color matching race |
| ConveyorChaos | ConveyorChaos.md | Conveyor belt physics |
| CopsAndRobbers | CopsAndRobbers.md | Classic cops vs robbers |
| Copycat | Copycat.md | Mimicry game |
| CopycatChaos | CopycatChaos.md | Chaos copycat variant |
| CrownChase | CrownChase.md | Crown chase game |
| DiceOfDeath | DiceOfDeath.md | Dice-based death game |
| DogParkDodge | DogParkDodge.md | Dodgeball with dogs |
| DuckHunt | DuckHunt.md | Duck hunting game |
| FloorIsLava | FloorIsLava.md | Lava floor survival |
| FloorSwaps | FloorSwaps.md | Floor tile swapping |
| GlassSmash | GlassSmash.md | Glass breaking physics |
| GravityGauntlet | GravityGauntlet.md | Gravity manipulation |
| HamsterWheel | HamsterWheel.md | Hamster wheel physics |
| HotPotatoBomb | HotPotatoBomb_POTENTIAL.md | Hot potato with bombs |
| JetpackJousting | JetpackJousting.md | Jetpack jousting |
| MajorityRules | MajorityRules.md | Voting-based game |
| MemoryMayhem | MemoryMayhem.md | Memory challenge |
| PaperAirplaneGlide | PaperAirplaneGlide_Potential.md | Paper airplane physics |
| PetRescueRush | PetRescueRush.md | Pet rescue racing |
| PillowFight | PillowFight.md | Pillow fighting physics |
| PortalPick | PortalPick.md | Portal selection game |
| RubberDuckSplash | RubberDuckSplash_POTENTIAL.md | Rubber duck water game |
| SafeSpot | SafeSpot_POTENTIAL.md | Find safe spots |
| SeesawScramble | SeesawScramble.md | Seesaw physics |
| ShoppingCartChaos | ShoppingCartChaos.md | Shopping cart physics |
| Snowball | Snowball.md | Snowball fight |
| SpinningTeacups | SpinningTeacups_POTENTIAL.md | Teacup ride physics |
| SpinPush | SpinPush_POTENTIAL.md | Spin and push |
| SumoBump | SumoBump.md | Sumo bumping |
| TeachersPet | TeachersPet.md | Teacher's pet game |
| TileStep | TileStep_POTENTIAL.md | Tile stepping |
| TowerTerror | TowerTerror.md | Tower building/falling |
| WeightLimit | WeightLimit.md | Weight management |
| WobbleRoyale | WobbleRoyale.md | Wobble physics battle royale |
| ZombieRush | ZombieRush.md | Zombie survival |
| ZoneOrDie | ZoneOrDie.md | Zone survival |

### 4.2 Additional Game Files
- 1SpeedForJetpack.md — Jetpack speed game
- JumpForBrainrot.md — Jump game with meme theme
- TheCatGame_Analysis.md — Cat game analysis (Research folder)
- NEW_IDEAS_BATCH_2.md — Batch of additional ideas (29KB)

### 4.3 Slappy Seals (Game Log)
**File:** max can you help me perfect this id.txt

A Roblox game log showing:
- 8-player battle royale
- Shrinking platform mechanic
- Shark enemy system (sharks spawn at 90s)
- Platform shrink (70x70 over 2.5s)
- Elimination when falling off
- Round system: WaitingForPlayers → MatchStarting → Countdown → InProgress
- UI: TopTimer, AnnouncementPopUp, GameSituationBox, WinnerCard, RewardCard
- MaxBridge V2.5 plugin (connects to AI assistant)
- StudioLink v1.0 plugin (connects to Claude Code)

---

## 5. Tool Infrastructure

### 5.1 Phase 1 Tools (Complete)
**File:** PROGRESS.md

| Tool | Port | Purpose |
|------|------|---------|
| Screen Stream | 8765 | Stream Roblox screen to external viewer |
| Input Controller | 8766 | Control Roblox remotely |
| Vision AI | 8767 | AI analysis of game screen |
| MaxBridge | 8768 | Bridge between Roblox and AI assistant |

### 5.2 Project Pipeline
**File:** PROJECT.md

**3-Phase Pipeline:**
1. **Build Tools** — Automated game analysis infrastructure
2. **Research** — Reverse engineer successful games
3. **Build Clones** — Create new games based on research

**Project Structure:**
```
Reverse Engine Roblox/
├── Docs/           # Tutorials and documentation
├── Games/          # Game design docs
├── Ideas/          # 60+ game concept documents
├── Research/        # Additional game analysis
├── Tools/          # Analysis tool scripts
├── Tutorial Notes/ # Learning materials
├── UI-Analysis/    # UI design analysis
├── adoptme/        # Game analysis: Adopt Me
├── autoeye/        # Game analysis: Auto Eye
├── catchamonster/  # Game analysis: Catch a Monster
├── clickerpetsim/  # Game analysis: Clicker Pet Sim
├── growacountry/   # Game analysis: Grow a Country
├── housetycoon/    # Game analysis: House Tycoon
├── memegame/       # Game analysis: Meme Game
├── tapsimulator/   # Game analysis: Tap Simulator
└── yourzoo/        # Game analysis: Your Zoo
```

---

## 6. UI Analysis

### 6.1 Knockout Bundle Shop UI
**File:** UI-Analysis/Knockout-BundleShop-UI.md

Analysis of Knockout!'s monetization UI:
- Bundle shop layout
- Pricing tiers
- Visual design patterns
- Call-to-action placement
- Limited-time offer presentation

### 6.2 ViewportFrame Tutorial
**File:** Docs/ViewportFrame-Tutorial.md

Tutorial on using Roblox ViewportFrames for:
- 3D model previews in UI
- Character display in shop
- Item inspection

---

## 7. Key Takeaways for Game Cloning

### 7.1 Success Factors (from analyzed games)
1. **Simple core loop** — One button primary action
2. **Collection mechanic** — Gacha/eggs drive engagement
3. **Prestige system** — Rebirth keeps players engaged long-term
4. **Social features** — Trading, leaderboards, friend bonuses
5. **Limited-time events** — FOMO drives engagement
6. **Pity timers** — Ensure F2P players get rare drops
7. **Zone progression** — Gate content to maintain progression curve
8. **Mobile-first design** — One-thumb controls, short sessions

### 7.2 Monetization Patterns
1. **Premium currency** (Gems/Robux) for special eggs/items
2. **Game passes** for permanent perks (autoclicker, x2 luck)
3. **Limited-time event items** (exclusive pets/cosmetics)
4. **Trading economy** (player-driven market creates value)
5. **Bulk pricing** (discounts for buying in bulk)
6. **Rarity tiers** (create aspiration for rare items)

### 7.3 Viral Mechanics
1. **Physics comedy** — Ragdolls, knockback, chaos
2. **Hidden decisions** — Creates suspense and social moments
3. **Dramatic reveals** — Big moments worth sharing
4. **Short rounds** — 2-5 minutes, easy to share clips
5. **Cute themes** — Broad appeal across age groups
6. **Spectator-friendly** — Fun to watch even when not playing

---

## Clone Checklist

To build a Roblox game based on this research:

### Core Systems
- [ ] Click/tap earning system
- [ ] Currency display UI (clicks, gems, rebirths)
- [ ] Egg gacha system with rarity tiers
- [ ] Pet following system
- [ ] Pet inventory management
- [ ] Rebirth/prestige system with multipliers
- [ ] Quest system (daily + progression)
- [ ] Shop system with tiers
- [ ] Trading system (player-to-player)
- [ ] Code redemption system
- [ ] Event system with timers
- [ ] Zone progression gating
- [ ] Leaderboard system
- [ ] Friend luck/social bonus system
- [ ] Autoclicker (premium feature)
- [ ] Offline earnings system
- [ ] Pity timer for rare drops

### Mobile Optimization
- [ ] One-thumb control scheme
- [ ] 2-3 minute round/session
- [ ] Portrait orientation support
- [ ] Minimal UI clutter
- [ ] Large tap targets
- [ ] Haptic feedback
- [ ] Vertical video sharing

### Monetization
- [ ] Premium currency (Gems)
- [ ] Game passes (autoclicker, x2 luck, extra slots)
- [ ] Limited-time event shop
- [ ] Bulk purchase discounts
- [ ] Rarity tiers with visual distinction
- [ ] Trading system for player economy