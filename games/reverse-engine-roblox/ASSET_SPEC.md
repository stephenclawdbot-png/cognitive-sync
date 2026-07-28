# Reverse Engine Roblox — Complete Asset Specification

**Type:** Full asset list, naming conventions, hierarchy, and priority tiers
**Audience:** Art team, UI team, audio team, Roblox Studio integrators
**Based on:** 9 reverse-engineered Roblox game analyses
**Date:** 2026-07-29

---

## 1. Naming Conventions

Consistent naming makes assets findable in Studio's Explorer and in the Roblox Creator Hub asset manager.

| Category | Prefix | Pattern | Example |
|----------|--------|---------|---------|
| 3D MeshPart | `M_` | `M_<category>_<name>_<variant>` | `M_Pet_FireDragon_Rainbow` |
| Texture | `T_` | `T_<category>_<name>_<variant>_<size>` | `T_Pet_FireDragon_Rainbow_256` |
| Decal | `D_` | `D_<surface>_<name>` | `D_Sign_ShopFront` |
| GUI Image | `UI_` | `UI_<screen>_<element>_<state>` | `UI_Shop_BuyButton_Hover` |
| Icon | `IC_` | `IC_<category>_<name>_<size>` | `IC_Pet_FireDragon_64` |
| Animation | `A_` | `A_<subject>_<action>_<dir>` | `A_Pet_Idle_South` |
| Audio SFX | `SFX_` | `SFX_<category>_<name>` | `SFX_Egg_Hatch` |
| Audio Music | `MUS_` | `MUS_<zone>_<mood>` | `MUS_Forest_Calm` |
| Particle | `P_` | `P_<effect>_<color>` | `P_Hatch_Golden` |
| Thumbnail | `TH_` | `TH_<game>_<theme>_<size>` | `TH_PetWin_Launch_512` |
| Badge | `BD_` | `BD_<name>_<size>` | `BD_FirstRebirth_60` |
| Gamepass icon | `GP_` | `GP_<key>_<size>` | `GP_Autoclicker_150` |
| DevProduct icon | `DP_` | `DP_<key>_<size>` | `DP_GemPackSmall_150` |

**General rules:** PascalCase words, underscores between tokens, no spaces, no version numbers in name (use Creator Hub versioning). Robux store icons MUST be PNG with transparent backgrounds.

---

## 2. Explorer Hierarchy in Roblox Studio

How assets should be organized once imported. Mirrors ARCHITECTURE.md §1.

```
ReplicatedStorage/
├── Assets/
│   ├── Meshes/
│   │   ├── Pets/                 M_Pet_*
│   │   ├── Eggs/                 M_Egg_*
│   │   ├── Buildings/             M_Building_*
│   │   ├── Props/                 M_Prop_*
│   │   └── UI3D/                  M_UI3D_* (viewport models)
│   ├── Textures/
│   │   ├── Pets/                 T_Pet_*
│   │   ├── Buildings/             T_Building_*
│   │   ├── Terrain/               T_Terrain_*
│   │   ├── Skybox/                T_Sky_*
│   │   └── GUI/                   T_GUI_* (atlases)
│   ├── Sounds/
│   │   ├── SFX/
│   │   │   ├── UI/                SFX_UI_*
│   │   │   ├── Gameplay/          SFX_Game_*
│   │   │   └── Pets/              SFX_Pet_*
│   │   └── Music/
│   │       ├── Menu/             MUS_Menu_*
│   │       └── Zones/             MUS_Zone_*
│   ├── Animations/
│   │   ├── Pets/                  A_Pet_*
│   │   ├── Player/                 A_Player_*
│   │   └── NPCs/                   A_NPC_*
│   ├── Particles/
│   │   ├── Hatch/                  P_Hatch_*
│   │   ├── Rebirth/                P_Rebirth_*
│   │   └── Ambient/                P_Ambient_*
│   └── Icons/
│       ├── Pets/                   IC_Pet_*
│       ├── Eggs/                   IC_Egg_*
│       ├── Currencies/             IC_Currency_*
│       ├── Gamepasses/             GP_*
│       └── DevProducts/            DP_*
│
├── Remotes/                       (instances, see ARCHITECTURE.md §4)
└── Modules/                       (Lua data, see DATA_MODELS.md)

Workspace/
├── Map/
│   ├── SpawnArea/
│   ├── Zones/
│   │   ├── Zone_Starter/
│   │   ├── Zone_Forest/
│   │   └── Zone_Ice/
│   ├── Plots/                     (tycoon plot templates)
│   └── EventProps/
├── NPCs/
├── Effects/
└── CameraAnchors/

StarterGui/
├── HUD.gui
├── Shop.gui
├── Trade.gui
├── Rebirth.gui
├── EggHatch.gui
├── Inventory.gui
├── Quests.gui
├── Leaderboard.gui
├── EventPopup.gui
├── DailyReward.gui
└── Notifications.gui

Lighting/
├── Atmosphere
├── Sky
└── ColorCorrectionEffect (post-FX)

SoundService/
├── SoundGroups/
│   ├── Master
│   ├── Music
│   ├── SFX
│   └── UI
```

---

## 3. Full Asset List by Category

### 3.1 GUI / 2D Assets

All ScreenGui elements. Sizes are pixel dimensions at 1080p reference; Roblox uses `UDim2`/Scale so design at this resolution and let it scale.

#### 3.1.1 HUD

| Asset name | Type | Dimensions | Format | Description |
|------------|------|------------|--------|-------------|
| UI_HUD_TopBar | Frame | 1920×80 | PNG/9-slice | Top currency bar background |
| UI_HUD_CurrencyClicks | ImageLabel | 64×64 | PNG | Clicks icon |
| UI_HUD_CurrencyGems | ImageLabel | 64×64 | PNG | Gems icon |
| UI_HUD_CurrencyRebirths | ImageLabel | 64×64 | PNG | Rebirths icon |
| UI_HUD_CurrencyCash | ImageLabel | 64×64 | PNG | Cash icon |
| UI_HUD_CurrencyKeys | ImageLabel | 64×64 | PNG | Keys icon |
| UI_HUD_IncomeRate | TextLabel | 200×40 | Font | "X/s" passive income display |
| UI_HUD_TapValue | TextLabel | 120×40 | Font | "+N per tap" |
| UI_HUD_FriendLuck | TextLabel | 200×40 | Font | "Friend Luck +N%" |
| UI_HUD_LevelBar | Frame+Image | 600×24 | PNG/9-slice | XP progress bar |
| UI_HUD_BottomBar | Frame | 1920×120 | PNG/9-slice | Bottom action bar |
| UI_HUD_TapButton | ImageButton | 200×200 | PNG | Main tap button |
| UI_HUD_AutoToggle | ImageButton | 80×80 | PNG ×2 states | Autoclicker on/off |
| UI_HUD_RebirthButton | ImageButton | 120×120 | PNG ×2 states | Rebirth (with "!" badge) |
| UI_HUD_ShopButton | ImageButton | 80×80 | PNG | Shop |
| UI_HUD_TradeButton | ImageButton | 80×80 | PNG | Trade |
| UI_HUD_CodesButton | ImageButton | 80×80 | PNG | Codes |
| UI_HUD_PetsButton | ImageButton | 80×80 | PNG | Pets/inventory |
| UI_HUD_QuestsButton | ImageButton | 80×80 | PNG | Quests (with "!" badge) |
| UI_HUD_IndexButton | ImageButton | 80×80 | PNG | Pokédex/index |
| UI_HUD_SellButton | ImageButton | 80×80 | PNG | Sell (Zoo) |
| UI_HUD_CollectAllButton | ImageButton | 80×80 | PNG | Collect All (Zoo) |
| UI_HUD_DailyButton | ImageButton | 80×80 | PNG | Daily rewards (with "!" badge) |
| UI_HUD_SkinsButton | ImageButton | 80×80 | PNG | Cosmetics |
| UI_HUD_SettingsButton | ImageButton | 48×48 | PNG | Settings gear |
| UI_HUD_MenuButton | ImageButton | 48×48 | PNG | Hamburger menu |
| UI_HUD_ChatButton | ImageButton | 48×48 | PNG | Chat |
| UI_HUD_EventTimer | Frame | 300×60 | PNG | Event banner with countdown |

#### 3.1.2 Shop Screen

| Asset name | Type | Dimensions | Format | Description |
|------------|------|------------|--------|-------------|
| UI_Shop_Bg | ImageLabel | 1200×800 | PNG/9-slice | Shop panel background |
| UI_Shop_Tab | ImageButton | 200×60 | PNG ×3 states | Tab (Eggs/Pets/Passes/Cosmetics) |
| UI_Shop_ItemCard | Frame | 240×320 | PNG/9-slice | Item card background |
| UI_Shop_BuyButton | ImageButton | 200×60 | PNG ×3 states | Buy button (Normal/Hover/Disabled) |
| UI_Shop_BuyButton_Robux | ImageButton | 200×60 | PNG ×3 states | Robux buy variant |
| UI_Shop_BundleCard | Frame | 400×400 | PNG/9-slice | Limited-time bundle card |
| UI_Shop_CountdownBg | Frame | 200×40 | PNG/9-slice | Limited-time countdown strip |
| UI_Shop_LockIcon | ImageLabel | 32×32 | PNG | Locked item indicator |
| UI_Shop_NewBadge | ImageLabel | 48×48 | PNG | "NEW!" badge |

#### 3.1.3 Egg Hatch Screen

| Asset name | Type | Dimensions | Format | Description |
|------------|------|------------|--------|-------------|
| UI_Egg_Bg | ImageLabel | 1600×900 | PNG | Hatch screen backdrop |
| UI_Egg_Crate | ImageLabel | 300×300 | PNG ×4 rarities | Egg/crate image per tier |
| UI_Egg_RarityGlow | ImageLabel | 600×600 | PNG ×4 | Rarity-colored glow |
| UI_Egg_RevealCard | Frame | 500×600 | PNG/9-slice | Pet reveal card |
| UI_Egg_VariantAura | ImageLabel | 800×800 | PNG ×3 | Golden/Rainbow/Glitch aura |
| UI_Egg_HatchButton | ImageButton | 240×80 | PNG ×3 | Hatch / Triple Hatch |
| UI_Egg_SkipButton | ImageButton | 120×60 | PNG | Skip animation |

#### 3.1.4 Inventory / Pets

| Asset name | Type | Dimensions | Format | Description |
|------------|------|------------|--------|-------------|
| UI_Inv_Bg | ImageLabel | 1400×900 | PNG/9-slice | Inventory panel |
| UI_Inv_PetSlot | Frame | 120×120 | PNG/9-slice | Pet grid cell |
| UI_Inv_EquipSlot | Frame | 140×140 | PNG ×2 | Equipped slot (empty/filled) |
| UI_Inv_RarityBorder | ImageLabel | 124×124 | PNG ×5 | Rarity-colored frame |
| UI_Inv_VariantTag | ImageLabel | 80×24 | PNG ×3 | Golden/Rainbow/Glitch tag |
| UI_Inv_SellButton | ImageButton | 80×40 | PNG ×3 | Sell per pet |
| UI_Inv_EquipButton | ImageButton | 80×40 | PNG ×3 | Equip/Unequip |
| UI_Inv_FilterTab | ImageButton | 120×40 | PNG ×2 | Filter by rarity |

#### 3.1.5 Rebirth Screen

| Asset name | Type | Dimensions | Format | Description |
|------------|------|------------|--------|-------------|
| UI_Rebirth_Bg | ImageLabel | 1000×700 | PNG/9-slice | Rebirth panel |
| UI_Rebirth_BulkTier | Frame | 200×80 | PNG ×5 | Bulk tier buttons (1/5/15/35/70) |
| UI_Rebirth_ConfirmButton | ImageButton | 240×80 | PNG ×3 | Confirm rebirth |
| UI_Rebirth_MultiplierText | TextLabel | 400×60 | Font | "2.5x per rebirth" |
| UI_Rebirth_WarningText | TextLabel | 600×40 | Font | "Rebirthing resets X!" |
| UI_Rebirth_KeepCollectionText | TextLabel | 600×40 | Font | "Will NOT reset animals!" (Zoo) |

#### 3.1.6 Trade Screen

| Asset name | Type | Dimensions | Format | Description |
|------------|------|------------|--------|-------------|
| UI_Trade_Bg | ImageLabel | 1600×900 | PNG/9-slice | Trade window |
| UI_Trade_OfferPanel | Frame | 600×700 | PNG/9-slice ×2 | Player offer panel |
| UI_Trade_AddPetSlot | Frame | 120×120 | PNG ×2 | Add-pet slot |
| UI_Trade_CurrencyInput | Frame | 200×40 | PNG | Currency input |
| UI_Trade_ConfirmButton | ImageButton | 240×80 | PNG ×3 | Accept |
| UI_Trade_CancelButton | ImageButton | 200×60 | PNG ×3 | Cancel |
| UI_Trade_StatusBadge | ImageLabel | 200×40 | PNG ×4 | Trade state indicator |
| UI_Trade_CountdownText | TextLabel | 100×40 | Font | Confirmation countdown |

#### 3.1.7 Quests / Leaderboard / Events / Daily

| Asset name | Type | Dimensions | Format | Description |
|------------|------|------------|--------|-------------|
| UI_Quest_Card | Frame | 600×80 | PNG/9-slice | Quest row |
| UI_Quest_ProgressBar | Frame | 500×20 | PNG/9-slice | Progress bar |
| UI_Quest_ClaimButton | ImageButton | 100×50 | PNG ×3 | Claim |
| UI_Quest_Checkmark | ImageLabel | 32×32 | PNG | Complete check |
| UI_Leaderboard_Bg | ImageLabel | 600×800 | PNG/9-slice | Leaderboard panel |
| UI_Leaderboard_Row | Frame | 560×60 | PNG/9-slice ×3 | Rank row (1st/2nd/3rd gold/silver/bronze) |
| UI_Leaderboard_CatTab | ImageButton | 180×60 | PNG ×2 | Category tab |
| UI_Leaderboard_MyRank | Frame | 560×60 | PNG | Highlighted my-rank row |
| UI_EventPopup_Bg | ImageLabel | 800×500 | PNG/9-slice | Event announcement |
| UI_EventPopup_Timer | TextLabel | 300×40 | Font | Countdown |
| UI_Daily_Bg | ImageLabel | 800×600 | PNG/9-slice | Daily reward calendar |
| UI_Daily_DayCell | Frame | 100×100 | PNG ×3 | Day cell (claimed/claimable/locked) |
| UI_Daily_StreakText | TextLabel | 300×40 | Font | "7 day streak" |
| UI_Notif_Toast | Frame | 400×80 | PNG/9-slice ×3 | Toast (info/warn/reward) |

### 3.2 3D Models (MeshParts)

Polycount budget for mobile target (60 FPS). All meshes in `.rbxmx` or `.obj` → Roblox MeshPart via Creator Hub.

#### 3.2.1 Pets

Each pet needs: base mesh + 4 variant recolors (where applicable) + idle/walk animations. Pets follow the player (NetworkOwnership = player).

| Asset name | Polycount | Texture res | Format | Description |
|------------|-----------|-------------|--------|-------------|
| M_Pet_Dummee_Base | 1,200 tris | 256² | GLB/.rbxm | Starter yellow monster |
| M_Pet_Leafet_Base | 1,200 tris | 256² | GLB/.rbbm | Nature squirrel |
| M_Pet_FireDragon_Base | 2,400 tris | 256² | GLB | Legendary dragon |
| M_Pet_FireDragon_Golden | reuse | 256² (recolor) | recolor | Golden variant |
| M_Pet_FireDragon_Rainbow | reuse | 256² (rainbow shader) | shader | Rainbow variant |
| M_Pet_FireDragon_Glitch | reuse | 256² (glitch shader) | shader | Glitch variant |
| M_Pet_InfernoDragon_Base | 3,000 tris | 256² | GLB | Evolution of FireDragon |
| M_Pet_IceDragon_Base | 2,400 tris | 256² | GLB | Ice zone dragon (Lv.32+ wild) |
| M_Pet_EmpyreanSovereign_Base | 4,000 tris | 512² | GLB | 1-in-1M secret pet |
| M_Pet_Zeck_Base | 1,000 tris | 128² | GLB | Tap Sim basic pet |
| M_Pet_Squirrel | 800 tris | 128² | GLB | Forest zone pet |
| M_Pet_Chipmunk | 800 tris | 128² | GLB | Forest zone pet |
| M_Pet_GoldenSquirrel | reuse | 128² (recolor) | recolor | Variant |
| M_Pet_RainbowSquirrel | reuse | 128² (shader) | shader | Variant |
| M_Pet_Lion | 1,600 tris | 256² | GLB | Zoo animal |
| M_Pet_Bear | 1,800 tris | 256² | GLB | Zoo/wild |
| M_Pet_Penguin | 1,000 tris | 128² | GLB | Zoo animal |
| M_Pet_RebirthDragon | 2,800 tris | 256² | GLB | Milestone reward pet |

**Pet count estimate:** 40 base pets × 4 variants = ~160 visual variants (most reuse mesh with recolor/shader). Budget 40 unique meshes.

#### 3.2.2 Eggs / Crates

| Asset name | Polycount | Texture | Description |
|------------|-----------|---------|-------------|
| M_Egg_Basic | 200 tris | 128² | Standard egg |
| M_Egg_Acorn | 200 tris | 128² | Forest egg |
| M_Egg_Lightning | 300 tris | 128² | Event egg |
| M_Egg_Rift | 400 tris | 256² | Rift Ball event egg |
| M_Egg_Golden | reuse | recolor | Premium egg variant |
| M_Egg_Rainbow | reuse | shader | Premium egg variant |
| M_Egg_Secret | 500 tris | 256² | Secret-tier egg |
| M_Crate_Basic | 300 tris | 256² | Zoo basic crate |
| M_Crate_Golden | 400 tris | 256² | Zoo golden crate |
| M_Crate_Rainbow | 400 tris | 256² | Zoo rainbow crate |
| M_Crate_Secret | 500 tris | 256² | Zoo secret crate |

**Egg count estimate:** ~15 unique meshes (variants reuse).

#### 3.2.3 Buildings (Tycoon)

| Asset name | Polycount | Texture | Description |
|------------|-----------|---------|-------------|
| M_Building_House_L1 | 800 tris | 256² | Starter house |
| M_Building_House_L2 | 1,200 tris | 256² | Upgraded |
| M_Building_House_L3 | 1,800 tris | 256² | Mid tier (glass tower observed) |
| M_Building_House_L4 | 2,400 tris | 512² | High tier |
| M_Building_House_L5 | 3,200 tris | 512² | Max tier |
| M_Building_Mine_L1..L5 | 800-3,200 | 256-512 | Income mine progression |
| M_Building_Decor_* | 200-600 | 128² | Decorations (0/6 limit observed) |
| M_Building_Enclosure_S | 600 tris | 256² | Zoo enclosure small |
| M_Building_Enclosure_M | 1,000 tris | 256² | Zoo enclosure medium |
| M_Building_Enclosure_L | 1,600 tris | 512² | Zoo enclosure large |
| M_Building_Shrine | 1,200 tris | 256² | Zoo shrine (boost area) |
| M_Building_UpgradesHouse | 1,500 tris | 256² | House Tycoon upgrades building |
| M_Building_MysteryBox | 400 tris | 256² | Red "?" box (key-gated) |

**Building count estimate:** ~30 unique meshes (5 levels × ~6 building types).

#### 3.2.4 Environment / Map

| Asset name | Polycount | Texture | Description |
|------------|-----------|---------|-------------|
| M_Prop_Tree_Forest | 400 tris | 128² | Forest tree |
| M_Prop_Tree_Ice | 400 tris | 128² | Ice tree |
| M_Prop_Rock | 200 tris | 128² | Generic rock |
| M_Prop_Sign_Shop | 200 tris | 128² | Shop signboard |
| M_Prop_Sign_Rebirth | 200 tris | 128² | Rebirth sign |
| M_Prop_Portal | 600 tris | 256² | Zone/world portal |
| M_Prop_EggMachine | 800 tris | 256² | Egg purchase station |
| M_Prop_Leaderboard | 600 tris | 256² | In-world leaderboard board |
| M_Prop_GiftBox | 200 tris | 128² | Central gift box |
| M_Prop_Moat | — | — | Water moat boundary (terrain/water) |
| M_Plot_Template | varies | — | Tycoon plot base (cloned on claim) |

**Environment count estimate:** ~40 unique props + 5 plot templates.

#### 3.2.5 NPCs / Wild Monsters

| Asset name | Polycount | Texture | Description |
|------------|-----------|---------|-------------|
| M_NPC_QuestGiver | 1,500 tris | 256² | Quest giver character |
| M_NPC_WildSquirrel | 800 tris | 128² | Forest wild spawn |
| M_NPC_WildBear | 1,800 tris | 256² | Forest wild spawn |
| M_NPC_WildIceDragon | 2,400 tris | 256² | Ice zone wild (Lv.32+) |
| M_NPC_Shark | 1,200 tris | 256² | Slappy Seals shark (90s spawn) |
| M_NPC_Shopkeeper | 1,500 tris | 256² | Shop vendor |

**NPC count estimate:** ~12 unique meshes.

#### 3.2.6 Player Avatar Cosmetics (optional)

| Asset name | Polycount | Texture | Description |
|------------|-----------|---------|-------------|
| M_Cosmetic_Aura_Golden | billboard | — | Golden aura particle |
| M_Cosmetic_Aura_Rainbow | billboard | — | Rainbow aura |
| M_Cosmetic_Hat_* | 200-600 | 128² | Cosmetic hats |
| M_Cosmetic_Mount_* | 1,500-3,000 | 256² | Rideable mounts (Catch a Monster) |

### 3.3 Animations

Roblox animations are `.rbxm` Animation instances referencing `rbxassetid://`. Used by Humanoids.

| Asset name | Subject | Frames | Loop | Description |
|------------|---------|--------|------|-------------|
| A_Pet_Idle_South | Pet | 30 | yes | Idle breathing |
| A_Pet_Idle_* (8 dirs) | Pet | 30 | yes | 8-direction idle (or rotate model) |
| A_Pet_Walk_South | Pet | 24 | yes | Walk follow player |
| A_Pet_Walk_* (8 dirs) | Pet | 24 | yes | 8-direction walk |
| A_Pet_Hatch | Pet | 60 | no | Hatch reveal animation |
| A_Pet_Evolve | Pet | 90 | no | Evolution animation |
| A_Player_Idle | Player | 30 | yes | Default idle |
| A_Player_Walk | Player | 24 | yes | Walk |
| A_Player_Tap | Player | 12 | no | Tap reaction |
| A_Player_Rebirth | Player | 120 | no | Rebirth celebration |
| A_NPC_Wild_Idle | NPC | 30 | yes | Wild monster idle |
| A_NPC_Wild_Hit | NPC | 18 | no | Reaction to capture attempt |
| A_NPC_QuestGiver_Idle | NPC | 30 | yes | Quest giver idle |
| A_NPC_Shark_Swim | NPC | 24 | yes | Shark patrol |
| A_Prop_Portal_Spin | Prop | 60 | yes | Portal rotation |
| A_Prop_EggMachine_Drop | Prop | 30 | no | Egg dispense |

**Animation count estimate:** ~60 unique animations (8-dir × few actions + one-offs). Use AnimationTrack priorities.

### 3.4 Audio

Audio is `.ogg` or `.mp3` uploaded to Roblox (`.ogg` preferred). Use SoundGroups for mixing.

#### 3.4.1 SFX

| Asset name | Duration | Format | Description |
|------------|----------|--------|-------------|
| SFX_UI_ButtonClick | 0.15s | OGG | Generic button |
| SFX_UI_ButtonHover | 0.10s | OGG | Hover |
| SFX_UI_TabSwitch | 0.20s | OGG | Tab change |
| SFX_UI_Popup | 0.30s | OGG | Notification |
| SFX_UI_Error | 0.30s | OGG | Invalid action |
| SFX_Tap_01..05 | 0.08s | OGG ×5 | Tap variations (avoid fatigue) |
| SFX_Currency_Gain | 0.20s | OGG | Currency increment |
| SFX_Egg_Purchase | 0.40s | OGG | Egg bought |
| SFX_Egg_Hatch | 1.50s | OGG | Hatch build-up |
| SFX_Egg_Reveal_Common | 0.50s | OGG | Common reveal |
| SFX_Egg_Reveal_Rare | 0.80s | OGG | Rare reveal |
| SFX_Egg_Reveal_Epic | 1.00s | OGG | Epic reveal |
| SFX_Egg_Reveal_Legendary | 1.50s | OGG | Legendary reveal (fanfare) |
| SFX_Egg_Reveal_Secret | 2.50s | OGG | Secret reveal (big fanfare) |
| SFX_Pet_Equip | 0.30s | OGG | Pet equipped |
| SFX_Pet_Unequip | 0.20s | OGG | Pet unequipped |
| SFX_Rebirth_Charge | 2.00s | OGG | Rebirth build-up |
| SFX_Rebirth_Boom | 1.50s | OGG | Rebirth completion |
| SFX_Trade_Open | 0.40s | OGG | Trade window opens |
| SFX_Trade_Confirm | 0.50s | OGG | Both confirmed |
| SFX_Trade_Complete | 1.00s | OGG | Trade done |
| SFX_Quest_Complete | 1.00s | OGG | Quest claimed |
| SFX_Daily_Claim | 0.80s | OGG | Daily reward |
| SFX_Boost_Activate | 0.60s | OGG | x2 Cash boost |
| SFX_Zone_Unlock | 1.20s | OGG | Zone unlocked |
| SFX_Zone_Teleport | 0.80s | OGG | Teleport whoosh |
| SFX_Code_Redeem | 0.60s | OGG | Code success |
| SFX_Capture_Throw | 0.30s | OGG | Capture device throw |
| SFX_Capture_Hit | 0.40s | OGG | Capture hits |
| SFX_Capture_Success | 1.20s | OGG | Monster caught |
| SFX_LevelUp | 0.80s | OGG | Player/pet level up |
| SFX_Evolution | 2.00s | OGG | Pet evolution |
| SFX_Elimination | 0.60s | OGG | Round-based elimination |
| SFX_RoundWin | 2.50s | OGG | Round victory |
| SFX_RoundLose | 1.50s | OGG | Round loss |
| SFX_Shark_Spawn | 1.00s | OGG | Shark appears (Slappy Seals) |

**SFX count estimate:** ~45 unique SFX.

#### 3.4.2 Music

| Asset name | Duration | Format | Description |
|------------|----------|--------|-------------|
| MUS_Menu_Main | 120s loop | OGG | Main menu / lobby theme |
| MUS_Zone_Starter | 120s loop | OGG | Starter zone calm |
| MUS_Zone_Forest | 120s loop | OGG | Forest playful |
| MUS_Zone_Ice | 120s loop | OGG | Ice zone ethereal |
| MUS_Zone_Volcano | 120s loop | OGG | Volcano intense |
| MUS_Shop | 90s loop | OGG | Shop browse |
| MUS_Trade | 90s loop | OGG | Trade window |
| MUS_Event_RiftBall | 120s loop | OGG | Event theme |
| MUS_Rebirth | 30s loop | OGG | Rebirth screen build-up |
| MUS_Round_InProgress | 120s loop | OGG | Round action theme |
| MUS_Round_End | 30s | OGG | Round end stinger |

**Music count estimate:** ~11 loops.

### 3.5 Particles / VFX

| Asset name | Type | Description |
|------------|------|-------------|
| P_Hatch_Common | ParticleEmitter | Common hatch sparkles |
| P_Hatch_Rare | ParticleEmitter | Blue sparkles |
| P_Hatch_Epic | ParticleEmitter | Purple burst |
| P_Hatch_Legendary | ParticleEmitter | Golden rays |
| P_Hatch_Secret | ParticleEmitter | Rainbow explosion |
| P_Hatch_GoldenVariant | ParticleEmitter | Golden variant shimmer |
| P_Hatch_RainbowVariant | ParticleEmitter | Rainbow variant shimmer |
| P_Hatch_GlitchVariant | ParticleEmitter | Glitch distortion |
| P_Rebirth_Burst | ParticleEmitter | Rebirth completion burst |
| P_Rebirth_Ring | Beam/Ring | Expanding ring |
| P_Tap_Spark | ParticleEmitter | Tap feedback spark |
| P_Currency_Float | ParticleEmitter | Currency floating numbers |
| P_Pet_Equip | ParticleEmitter | Equip poof |
| P_Trade_Complete | ParticleEmitter | Trade handshake effect |
| P_Ambient_Fireflies | ParticleEmitter | Forest ambient |
| P_Ambient_Snow | ParticleEmitter | Ice zone ambient |
| P_Ambient_Embers | ParticleEmitter | Volcano ambient |
| P_Portal_Swirl | ParticleEmitter | Portal swirl |
| P_EggMachine_Glow | ParticleEmitter | Egg machine glow |
| P_Boost_Activate | ParticleEmitter | x2 boost activation |
| P_Elimination_Smoke | ParticleEmitter | Round elimination |
| P_Shark_Splash | ParticleEmitter | Shark spawn splash |

**Particle count estimate:** ~25 unique emitters.

### 3.6 Icons (small UI assets)

| Asset name | Size | Format | Description |
|------------|------|--------|-------------|
| IC_Pet_* | 64² | PNG | Pet icons for inventory/index (40 pets) |
| IC_Egg_* | 64² | PNG | Egg icons (15 eggs) |
| IC_Currency_Clicks | 64² | PNG | Clicks icon |
| IC_Currency_Gems | 64² | PNG | Gems icon |
| IC_Currency_Cash | 64² | PNG | Cash icon |
| IC_Currency_Rebirths | 64² | PNG | Rebirths icon |
| IC_Currency_Keys | 64² | PNG | Keys icon |
| IC_Currency_EventTokens | 64² | PNG | Event tokens |
| IC_Badge_* | 32² | PNG | UI badges (NEW!, !, lock) |
| IC_Achievement_* | 64² | PNG | Achievement icons (~20) |
| IC_Quest_* | 48² | PNG | Quest icons (~30) |
| IC_Mount_* | 64² | PNG | Mount icons |
| IC_Skin_* | 64² | PNG | Cosmetic skin icons |

**Icon count estimate:** ~200 icons (pet icons dominate).

---

## 4. Thumbnail / Icon Requirements (Robux Store)

Required by Roblox Creator Hub for publishing. All PNG, sRGB.

| Asset | Required sizes | Format | Notes |
|-------|----------------|--------|-------|
| Game thumbnail | 1920×1080 (16:9) | PNG/JPG | Up to 10; first is main |
| Game icon | 512×512 (1:1) | PNG | Square game icon |
| Gamepass icon | 150×150 (1:1) | PNG | Transparent bg preferred |
| DevProduct icon | 150×150 (1:1) | PNG | Transparent bg preferred |
| Badge icon | 60×60 (1:1) | PNG | Achievement badge |
| Asset thumbnail | 256×256 or 512×512 | PNG | Mesh/texture preview |
| Bundle preview | 700×700 | PNG | For Robux bundle listing |
| Loading screen | 1920×1080 | PNG | Shown during load |
| Splash logo | 1024×1024 | PNG | Brand splash |

### 4.1 Game thumbnails (concepts)

| Thumbnail | Theme | Text overlay | Source pattern |
|-----------|-------|--------------|----------------|
| TH_PetWin_Launch_512 | Hero pets + "COLLECT 40+ PETS!" | Bold sans | Tap Sim style |
| TH_PetWin_Hatch_512 | Egg cracking, rainbow reveal | "HATCH RAINBOW PETS!" | Your Zoo pity timer hook |
| TH_PetWin_Rebirth_512 | Player glowing, x2.5 text | "REBIRTH FOR 2.5x!" | House Tycoon |
| TH_PetWin_Event_512 | Rift portal, "LIMITED EVENT!" | Event countdown | Catch a Monster Rift Ball |
| TH_PetWin_Trade_512 | Two players shaking hands | "TRADE PETS!" | Tap Sim Plaza |
| TH_PetWin_Offline_512 | "EARNS OFFLINE" badge | Sleep + coins | Your Zoo |
| TH_PetWin_Update_512 | "NEW UPDATE!" + new pet | Version text | Common Roblox pattern |

### 4.2 Badge icons

| Badge | Description |
|-------|-------------|
| BD_FirstRebirth_60 | "First Rebirth" |
| BD_TenRebirths_60 | "Decuple" |
| BD_HundredRebirths_60 | "Centurion" |
| BD_FirstSecret_60 | "Lucky!" (first secret pet) |
| BD_AllPets_60 | "Completionist" (full index) |
| BD_FirstTrade_60 | "Trader" |
| BD_FirstCapture_60 | "Catcher" |
| BD_ZoneUnlockedAll_60 | "Explorer" |
| BD_Day7_60 | "Weekly Streak" |
| BD_RoundWin_60 | "Champion" |

### 4.3 Robux store asset requirements

For each GamePass/DevProduct, Roblox requires:
- **Icon:** 150×150 PNG (transparent background recommended)
- **Name:** ≤ 30 chars
- **Description:** ≤ 200 chars (used in the Robux store listing)
- **Preview image (optional):** 700×700 PNG for bundle previews

| Robux item | Icon asset | Description example |
|------------|------------|---------------------|
| Autoclicker | GP_Autoclicker_150 | "Automatically taps for you. Never miss a click!" |
| 2x Taps | GP_x2Taps_150 | "Doubles all tap income permanently. Best value!" |
| +3 Pet Slots | GP_ExtraSlots_150 | "Equip 3 more pets at once for huge multipliers." |
| 500 Gems | DP_GemPackSmall_150 | "A pocket of premium gems for special eggs." |
| 6,000+1,000 Gems | DP_GemPackBulk_150 | "Bulk gem pack with bonus. Best value per Robux." |
| 10 Event Keys | DP_KeyPack_150 | "Unlock mystery boxes and event rewards." |
| Starter Pack (limited) | DP_StarterPack_150 | "Limited-time bundle: eggs + gems + boost." |

---

## 5. Total Asset Count Estimate

| Category | Unique assets | Variants/States | Total |
|----------|---------------|------------------|-------|
| GUI / 2D | ~150 | ×3 states avg | ~450 |
| 3D Meshes (pets) | 40 | ×4 variants | ~160 visual (40 meshes) |
| 3D Meshes (eggs) | 12 | ×3 variants | ~36 visual (12 meshes) |
| 3D Meshes (buildings) | 30 | — | 30 |
| 3D Meshes (environment) | 40 | — | 40 |
| 3D Meshes (NPCs) | 12 | — | 12 |
| 3D Meshes (cosmetics) | ~20 | — | 20 |
| Animations | 60 | — | 60 |
| SFX | 45 | — | 45 |
| Music loops | 11 | — | 11 |
| Particles | 25 | — | 25 |
| Icons (pet/UI) | 200 | — | 200 |
| Thumbnails | 10 | — | 10 |
| Badges | 20 | — | 20 |
| Robux store icons | ~15 | — | 15 |
| **TOTAL** | **~640 unique** | | **~900 incl. variants** |

---

## 6. Priority Tiers

### Tier 0 — MVP (ship-blocking, build first)

Required for the core loop (tap → egg → pet → rebirth).

| Asset | Why |
|-------|-----|
| HUD core (top bar, tap button, currency icons, rebirth button) | Core loop UI |
| 5 base pets (Common/Rare/Epic/Legendary/Secret) + 4 variant recolors | Egg system demo |
| 3 eggs (Basic, Acorn, Special) | Gacha loop |
| Egg hatch screen + reveal VFX | Dopamine moment |
| Inventory (pet slots, rarity borders, equip) | Pet management |
| Rebirth screen + bulk tiers + VFX | Prestige loop |
| 1 zone (Starter) + 3 props (tree, rock, sign) | World |
| 8 SFX (tap, currency, purchase, hatch×4 tiers, rebirth) | Audio feedback |
| 2 music loops (menu, starter zone) | Ambience |
| 10 pet icons + 3 egg icons + 5 currency icons | UI |
| 3 thumbnails + game icon + 5 gamepass icons | Store launch |
| Loading screen + splash | First impression |

**MVP count:** ~120 assets.

### Tier 1 — Core feature complete

- Trade system (full trade UI + SFX)
- Quest system (cards, progress, claim)
- Shop (tabs, item cards, Robux buy)
- Leaderboard (panel, rows, categories)
- Daily rewards (calendar)
- Code redemption (input + success)
- 15 more pets + 5 more eggs
- 2 more zones (Forest, Ice) + props
- 5 NPCs (quest giver, shopkeeper, 3 wild)
- 20 more SFX + 3 more music loops
- 10 badges + 10 achievements

**Tier 1 count:** ~250 additional assets.

### Tier 2 — Polish (post-launch)

- 20 more pets (full collection to 40)
- Event system (event popup, timers, event eggs)
- Cosmetics (hats, auras, mounts)
- 5 more zones + props
- Skins shop
- 15 more SFX + 4 more music loops
- Ragdoll physics (viral formula) + elimination VFX
- All 10 thumbnails + bundle previews
- Particle polish (ambient, hatches, rebirth)

**Tier 2 count:** ~300 additional assets.

### Tier 3 — Live-ops / seasonal

- Holiday event assets (Halloween, Christmas, Summer)
- Limited-time eggs/pets per event
- New zones with content updates
- New rebirth tiers / cosmetics
- Ad placement assets (if monetizing via ads)

**Tier 3 count:** ongoing, ~100+ assets per event.

---

## 7. Technical Specs for Roblox Import

### 7.1 MeshPart import

- Upload `.glb`/`.obj` via Creator Hub → MeshPart asset
- Set `DoubleSided = false` (perf), `CastShadow` per asset budget
- For recolors: reuse mesh, set `Color3` or swap `TextureID` (cheaper than new mesh)
- For Rainbow/Glitch variants: use a `SurfaceAppearance` or shader-like `Decal`

### 7.2 Texture specs

- PNG, power-of-two (128², 256², 512²), max 1024²
- sRGB for color, linear for data textures (roughness/metalness)
- Use `SurfaceAppearance` for PBR (ColorMap, MetalnessMap, RoughnessMap, NormalMap)
- Atlas small UI textures into a single 1024² atlas to reduce draw calls

### 7.3 GUI element specs

- Use `Scale` (UDim2 with relative coords) for responsive layout
- 9-slice for scalable panels (define SliceCenter in import)
- ImageButtons need 3 states: Normal/Hover/Pressed (or use single + Color3 tint)
- Reference resolution: 1920×1080 (landscape) and 1080×1920 (portrait if mobile-portrait)

### 7.4 Animation specs

- Upload `.rbxm` Animation instances; reference by `AnimationId`
- Use `AnimationTrack.Priority` (Idle < Move < Action < Action2/3/4)
- Loop idles/walks; one-shot hatches/evolutions/rebirths
- 30 FPS default; cap bone count for mobile

### 7.5 Audio specs

- `.ogg` (Vorbis) preferred for SFX (smaller), `.mp3` for music
- Mono for SFX (positional), stereo for music
- Normalize to -3 dB peak; master bus in SoundService SoundGroup
- Cap concurrent playing sounds (32 budget)

---

## 8. Asset Pipeline (Workflow)

```
[Artist exports .glb/.png/.ogg]
   │
   ▼
[Creator Hub upload] → assetId assigned
   │
   ▼
[Add to ReplicatedStorage.Assets.* per hierarchy §2]
   │
   ▼
[Reference assetId in Modules (PetData.meshId, etc. — see DATA_MODELS.md)]
   │
   ▼
[Client Controllers load assetId at runtime; pool instances]
```

**Versioning:** Creator Hub auto-versions assets. Never rename a published asset id — old clients depend on it. To replace, publish a new version of the same asset id.

**QA checklist per asset:**
- [ ] Follows naming convention (§1)
- [ ] Placed in correct Explorer hierarchy (§2)
- [ ] Polycount / texture res within budget (§3)
- [ ] AssetId referenced in the correct data module (DATA_MODELS.md)
- [ ] Tested in-game on mobile (FPS stable)
- [ ] Icon/thumbnail meets Robux store size (§4)

---

## 9. References

- `ARCHITECTURE.md` — where each asset plugs into systems
- `DATA_MODELS.md` — assetId fields in PetData, EggData, etc.
- `GAME_MECHANICS.md` — which mechanics drive which assets
- `ECONOMY.md` — which assets gate monetization
- `raw-data/*/GAME_ANALYSIS.md` — UI screenshots per game (source for visual reference)

---

*End of ASSET_SPEC.md — handoff to art, UI, and audio teams.*