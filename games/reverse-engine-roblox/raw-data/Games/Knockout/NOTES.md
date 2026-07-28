# Knockout! - Game Analysis

**Developer:** braxworks
**Rating:** 98%
**Players:** 65.6K concurrent
**Date Analyzed:** 2026-02-04

---

## Session Notes

### Screenshot 1 - Round 6, Lobby/Waiting Phase

---

## Core Mechanics
- **Round-based** (currently Round 6)
- **Hidden objectives** - "Revealing aims in 2" countdown
- Possibly assassination/target-based (players get assigned "aims")
- **Penguin theme** - players are penguins
- **AFK system** built-in (rounds can run without you)
- **Spectate mode** available

## UI/HUD Layout
| Position | Element |
|----------|---------|
| Top Center | Round # + Status Timer |
| Top Right | Spin Wheel (09:46), Free Skin countdown (4:49) |
| Top Left | Currency (ice cube icon = 10) |
| Left Side | Shop, Character, Quests, Index, AFK buttons |
| Bottom Left | Spectate, Settings |

## Map Design
- **Arctic/Winter theme**
- White snowy floor
- Penguin character models

## Monetization
- 💰 **Soft currency**: Ice cubes (10 shown)
- 🎡 **Spin wheel**: Timed reward (resets every ~10min?)
- 🎁 **Free skin**: Countdown timer engagement hook (4:49)
- 🛒 **Shop button**: Prominent red/pink
- 📜 **Quests**: Likely reward currency

## What Makes It Viral
*(observing more...)*

---

### Screenshot 2 - Round 9, Active Gameplay

## Core Gameplay Loop (Confirmed!)
```
1. Round starts
2. "Revealing aims" countdown (targets assigned)
3. Hunt your assigned target
4. Avoid being hunted by YOUR hunter
5. Knockouts = points
6. Round ends → repeat
```

## New Observations
- **9 minute rounds** (timer: 09:00)
- **Wings/Flight** - saw player with bat wings (traversal or cosmetic?)
- **Leaderboards in-game**: "Weekly Knockouts" + "Weekly Wins" boards visible
- **Multiple players**: admiralthefinest, shedlestsky, THE_EMPEROR, Aaron246737

## Assassination Mechanics
- Each player gets a SECRET target ("aim")
- You hunt YOUR target
- Someone else is hunting YOU
- Creates paranoid gameplay = tension = fun

---

### Screenshot 3 - Combat Revealed!

## Combat System
- **MELEE WEAPONS** - Ice/crystal sword visible
- **Kill feed** on right: "shedlestsky knocked out hellokitty_kitmeow16"
- Swing sword → hit target → knockout

## Map Features
- **Shop building** in-game with "SPINO SKIN!!" promo
- **NPC Penguins** standing around (decorative?)
- **Ice/winter aesthetic** consistent

## Additional Monetization
- **"Starter Pack"** button (top right) - real money purchase
- **Free Skin Spin** with countdown (engagement loop)
- **In-game shop building** - walk up and buy

## Timers Observed
- Main round: 08:32 remaining
- Free skin: 3:18
- Spin wheel: 08:16

---

### Screenshot 4 - POWER SYSTEM FOUND!

## Combat Controls (CRUCIAL!)
```
┌─────────────────────────────────┐
│      POWER BAR (bottom)         │
├─────────────────────────────────┤
│  [Q] ◄───── Power 1 ─────► [E]  │
│       10-slot charge meter      │
└─────────────────────────────────┘
```
- **Q key** = Left action (ability?)
- **E key** = Right action (ability?)
- **Power meter** = Builds up over time or through actions
- Currently at 1/10 power

## Target Arrow
- **Black arrow** above player head
- Shows direction you're facing / aiming

## Quest System
- Yellow (!) notification on Quests button
- Incomplete missions = engagement hook

---

### Screenshot 5 - Round 5 Active

## Currency Update
- **Ice cubes: 30** (was 10!) - earned 20 from gameplay

## Observations
- "Round in progress!" banner
- Power bar NOT visible (maybe only during combat phase?)
- 06:35 on timer
- Two penguins walking around

## Key Insight
Currency earned just from playing rounds = retention mechanic

---

### Screenshot 6 - AFK + Skins Menu

## Currency JUMPED
- **215 ice cubes** (was 30!) - Major rewards happening

## Kill Feed (Right Side)
- "shedlestsky knocked out EL_RAY"
- "hellokitty_kitmeow16 **slipped off**" ← Environmental death!
- "lt1 knocked out shedlestsky"

## Collection System
- **Skins: 1/58** collected
- Completionist hook = grind for all skins

## AFK Mode
- Red "AFK" button = "You will not spawn in game"
- Can browse menus while sitting out rounds
- Smart design: lets casuals stay in lobby

## Environmental Hazards
- Players can "slip off" (fall off map?)
- Not just player-vs-player combat
