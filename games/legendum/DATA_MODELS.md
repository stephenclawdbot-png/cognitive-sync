# Legendum — JSON Data Schemas

> **Engine:** Godot 4.6.2 · **Format:** JSON for content, `.tres` for engine resources · **Save:** single JSON document per slot
> **Audience:** Content designers, data engineers, save-system maintainers.
> **Conventions:** Every schema is presented as a TypeScript-style interface followed by a JSON example. `StringName` fields are JSON strings; `DefRef` fields use `"def!<type>.<id>"` syntax resolvable by the define-it database. All enums are stringly-typed for forward compatibility.

---

## 0. Common Types

```typescript
type DefRef<T extends string> = string;        // "def!item.sword_4"
type StringName = string;                       // interned at runtime
type ColorHex   = string;                        // "#RRGGBB" or "#RRGGBBAA"
type TimeOfDay  = "MORNING" | "DAY" | "EVENING";
type Season     = "GREENRISE" | "HIGHSUN" | "AMBERFALL";
type LifeStageId = "stage1_young" | "stage3_veteran" | "stage4_elder" | "stage5_decrepit";
type StatId     = "STAT_STRENGTH" | "STAT_DEXTERITY" | "STAT_VIGOR"
                | "STAT_PERCEPTION" | "STAT_INTELLECT" | "STAT_WISDOM"
                | "ALL_STATS" | "CHARACTER_LEVEL";
type SkillId    = "SKILL_BLADES" | "SKILL_ARCHERY" | "SKILL_FARMING"
                | "SKILL_FORAGING" | "SKILL_HUNTING" | "SKILL_MINING"
                | "SKILL_PIETY" | "SKILL_ROGUERY" | "SKILL_SCHOLAR"
                | "SKILL_DELVING" | "SKILL_SOCIAL";
type RegionId   = "EXPLORATION_POINTS_PRISON" | "EXPLORATION_POINTS_ROADS"
                | "EXPLORATION_POINTS_TOWN" | "EXPLORATION_POINTS_WOODLANDS";
type RarityId   = "UNAWOKEN" | "GRAY" | "GREEN" | "BLUE" | "RED" | "GOLD" | "WHITE" | "DESTINY";
type DeathCause = "NATURAL" | "COMBAT" | "EVENT" | "QUIT";
```

---

## 1. Character Data

### 1.1 CharacterState (per-life, persisted)

```typescript
interface CharacterState {
  name: string;                  // "Marcus"
  origin_id: DefRef<"origin">;   // "def!origin.prisoner"
  backstory_id: DefRef<"backstory">;
  age_years: number;             // 0..70+
  life_stage_id: LifeStageId;
  character_level: number;
  character_xp: number;           // progress toward next character level

  attributes: Record<StatId, AttributeState>;
  skills: Record<SkillId, SkillState>;

  hp_current: number;
  hp_max_derived: number;        // recomputed by ComputedReactive
  energy_current: number;
  energy_max_derived: number;

  base_movement_speed: number;  // px/sec in town
  combat_style_id: DefRef<"combat_style">;

  status_effect_ids: DefRef<"status_effect">[];   // active status effects
  equipped_ability_ids: DefRef<"ability">[];       // slotted abilities

  stat_quality_tiers: Record<StatId, "AVERAGE"|"GOOD"|"GREAT"|"EXCELLENT">;

  attribute_focus: StatId | null;  // currently trained attribute in combat
}

interface AttributeState {
  level: number;          // 1..80+
  xp: number;             // progress toward next attribute level
  effective_level: number;// after item/perk/stage modifiers — recomputed
}

interface SkillState {
  level: number;
  xp: number;
  sp: number;             // skill points banked for this skill
}
```

```json
{
  "name": "Marcus",
  "origin_id": "def!origin.prisoner",
  "backstory_id": "def!backstory.fighter",
  "age_years": 28,
  "life_stage_id": "stage3_veteran",
  "character_level": 14,
  "character_xp": 2340,
  "attributes": {
    "STAT_STRENGTH":    { "level": 22, "xp": 410,  "effective_level": 22 },
    "STAT_DEXTERITY":   { "level": 18, "xp": 90,   "effective_level": 18 },
    "STAT_VIGOR":       { "level": 20, "xp": 250,  "effective_level": 20 },
    "STAT_PERCEPTION":  { "level": 14, "xp": 0,    "effective_level": 15 },
    "STAT_INTELLECT":   { "level": 11, "xp": 0,    "effective_level": 11 },
    "STAT_WISDOM":      { "level": 9,  "xp": 0,    "effective_level": 9  }
  },
  "skills": {
    "SKILL_BLADES":  { "level": 12, "xp": 800,  "sp": 0 },
    "SKILL_MINING":  { "level": 5,  "xp": 120,  "sp": 3 },
    "SKILL_FORAGING":{ "level": 3,  "xp": 60,   "sp": 1 },
    "SKILL_PIETY":   { "level": 1,  "xp": 0,    "sp": 0 },
    "SKILL_ROGUERY": { "level": 4,  "xp": 200,  "sp": 0 },
    "SKILL_HUNTING": { "level": 2,  "xp": 30,   "sp": 0 },
    "SKILL_ARCHERY": { "level": 0,  "xp": 0,    "sp": 0 },
    "SKILL_FARMING": { "level": 0,  "xp": 0,    "sp": 0 },
    "SKILL_SCHOLAR": { "level": 0,  "xp": 0,    "sp": 0 },
    "SKILL_DELVING": { "level": 1,  "xp": 0,    "sp": 0 },
    "SKILL_SOCIAL":  { "level": 2,  "xp": 40,   "sp": 0 }
  },
  "hp_current": 88,
  "hp_max_derived": 102,
  "energy_current": 6,
  "energy_max_derived": 10,
  "base_movement_speed": 80,
  "combat_style_id": "def!combat_style.sword_style",
  "status_effect_ids": ["def!status_effect.early_years"],
  "equipped_ability_ids": [
    "def!ability.blades_slash",
    "def!ability.bow_piercing_strike",
    "def!ability.guardian_spirit"
  ],
  "stat_quality_tiers": {
    "STAT_STRENGTH": "GOOD",
    "STAT_DEXTERITY": "AVERAGE",
    "STAT_VIGOR": "GOOD",
    "STAT_PERCEPTION": "AVERAGE",
    "STAT_INTELLECT": "AVERAGE",
    "STAT_WISDOM": "AVERAGE"
  },
  "attribute_focus": "STAT_STRENGTH"
}
```

### 1.2 Origin (static content)

```typescript
interface LifeOrigin {
  id: DefRef<"origin">;
  display_name: string;
  description: string;            // rich text
  backstory_scene: DefRef<"scene">;
  opening_narrative: DefRef<"narrative_event">;

  starting_attributes: Record<StatId, number>;   // base levels
  stat_quality_tiers: Record<StatId, "AVERAGE"|"GOOD"|"GREAT"|"EXCELLENT">;
  starting_items: DefRef<"item">[];
  starting_status_effects: DefRef<"status_effect">[];
  starting_combat_style: DefRef<"combat_style">;
  starting_regions: DefRef<"region">[];
  starting_web_id: DefRef<"web">;
  max_age: number;                // 70 default
  tags: string[];                 // used by conditions like origin_tag
}
```

```json
{
  "id": "def!origin.prisoner",
  "display_name": "Prisoner",
  "description": "You wake in a cold cell. The bars are loose. Beyond them, a world you barely remember waits.",
  "backstory_scene": "res://scenes/narrative/origin_prisoner.scn",
  "opening_narrative": "def!narrative.character_open",
  "starting_attributes": {
    "STAT_STRENGTH": 10, "STAT_DEXTERITY": 10, "STAT_VIGOR": 10,
    "STAT_PERCEPTION": 10, "STAT_INTELLECT": 10, "STAT_WISDOM": 10
  },
  "stat_quality_tiers": {
    "STAT_STRENGTH": "AVERAGE", "STAT_DEXTERITY": "AVERAGE", "STAT_VIGOR": "AVERAGE",
    "STAT_PERCEPTION": "AVERAGE", "STAT_INTELLECT": "AVERAGE", "STAT_WISDOM": "AVERAGE"
  },
  "starting_items": ["def!item.dagger_1", "def!item.cloth_armor"],
  "starting_status_effects": ["def!status_effect.early_years"],
  "starting_combat_style": "def!combat_style.power",
  "starting_regions": ["def!region.ashvale"],
  "starting_web_id": "def!web.prison_origin",
  "max_age": 70,
  "tags": ["origin", "prison", "outlaw"]
}
```

---

## 2. Life Events (Story Web)

### 2.1 WebDef (static)

```typescript
interface WebDef {
  id: DefRef<"web">;
  root_node_id: DefRef<"web_node">;
  nodes: Record<DefRef<"web_node">, WebNode>;
  sockets: WebSocketDef[];        // visual connections between nodes
}

interface WebNode {
  id: DefRef<"web_node">;
  display_name: string;
  skin: DefRef<"web_node_skin">;
  narrative_event_id: DefRef<"narrative_event">;
  encounter_id: DefRef<"encounter"> | null;
  quest_id: DefRef<"quest"> | null;
  requirements: Requirement[];
  rewards: Reward[];
  unlocks: UnlockDef[];           // location, region, perk, contact, etc.
  next_node_options: WebNodeOption[];
  is_terminal: boolean;
}

interface WebNodeOption {
  option_id: string;
  display_text: string;
  effects: NarrativeOptionEffect[];
  next_node_id: DefRef<"web_node"> | null;
  selector: WebNodeSelector | null;
}

interface WebNodeSelector {
  kind: "CONDITIONS" | "CAMPAIGN_FLAG" | "LIVES_LIVED" | "POOL";
  // CONDITION: evaluate against current state
  // CAMPAIGN_FLAG: branch on a campaign flag
  // LIVES_LIVED: branch on how many prior lives were lived
  // POOL: pick one option from a weighted pool
  options: ConditionalOption[];
}
```

### 2.2 NarrativeEvent (static)

```typescript
interface NarrativeEvent {
  id: DefRef<"narrative_event">;
  speaker: DefRef<"speaker">;
  pages: NarrativePage[];
  options: NarrativeOption[];
}

interface NarrativePage {
  text: string;                    // rich text with [wave], [color=#hex], {TOKEN} placeholders
  portrait: string | null;         // speaker portrait path
}

interface NarrativeOption {
  id: string;
  text: string;
  effects: NarrativeOptionEffect[];
  requirements: Requirement[];
}

interface NarrativeOptionEffect {
  type:
    | "reward"            // applies a Reward
    | "world_state_change"// mutates WorldState
    | "set_campaign_flag" // sets a campaign flag
    | "close_web"         // closes the current web
    | "advance_to_node"   // navigates to a new web node
    | "unlock_narrative"; // unlocks a new narrative event
  payload: any;           // type-specific
}
```

```json
{
  "id": "def!narrative.goblins_conclusion",
  "speaker": "def!speaker.narrator",
  "pages": [
    {
      "text": "You've cut down the last of the raiders. Only one remains: a scrawny goblin trembling before you, weapon dropped. But he isn't fleeing. He just... stares, eyes glazed and distant.",
      "portrait": "res://assets/portraits/goblin.png"
    }
  ],
  "options": [
    {
      "id": "spare",
      "text": "Lower your weapon. Let him go.",
      "effects": [
        { "type": "reward",         "payload": { "type": "reward_deed", "deed_id": "def!deed.av_mizgrub_spared" } },
        { "type": "set_campaign_flag", "payload": { "flag": "mizgrub_spared", "value": true } }
      ],
      "requirements": []
    },
    {
      "id": "execute",
      "text": "Run him through. Bandits don't get mercy.",
      "effects": [
        { "type": "reward",         "payload": { "type": "reward_deed", "deed_id": "def!deed.av_mizgrub_executed" } },
        { "type": "set_campaign_flag", "payload": { "flag": "mizgrub_executed", "value": true } }
      ],
      "requirements": []
    }
  ]
}
```

### 2.3 WebState (per-life)

```typescript
interface WebState {
  active_web_id: DefRef<"web"> | null;
  current_node_id: DefRef<"web_node"> | null;
  completed_node_ids: DefRef<"web_node">[];
  visited_node_ids: DefRef<"web_node">[];
  sockets_resolved: DefRef<"web_socket">[];
  campaign_flags: Record<string, boolean | number | string>;
}
```

```json
{
  "active_web_id": "def!web.ashvale_main",
  "current_node_id": "def!node.goblins_conclusion",
  "completed_node_ids": [
    "def!node.arrival",
    "def!node.caravan_investigation",
    "def!node.find_raiders"
  ],
  "visited_node_ids": [
    "def!node.arrival",
    "def!node.caravan_investigation",
    "def!node.find_raiders",
    "def!node.goblins_conclusion"
  ],
  "sockets_resolved": ["def!web_socket.arrival_to_caravan"],
  "campaign_flags": {
    "arrived_in_ashvale": true,
    "caravans_saved": true,
    "training_grounds_upgraded": false
  }
}
```

---

## 3. Soul Perks (Meta-Progression)

### 3.1 SoulPerkDef (static)

```typescript
interface SoulPerkDef {
  id: DefRef<"soul_perk">;
  display_name: string;
  description: string;
  cost_lp: number;                // Legend Point cost
  category: "TIME" | "STAT" | "SKILL" | "NARRATIVE" | "MISC";
  effects: MetaEffect[];          // applied at draft time of every new life
  requirements: Requirement[];
  max_stacks: number;             // 1 default
  icon: string;
}

interface MetaEffect {
  type:
    | "meta_boost_xp_yield"          // +XP gain for next life
    | "meta_gain_speed_stars"        // +1 to all speed-related perk slots
    | "meta_gain_yield_stars"        // +1 to all yield-related perk slots
    | "start_with_perk"              // grant a per-life perk at draft
    | "max_age_bonus"                // +N years to max_age
    | "starting_attribute_bonus"     // +N to a starting attribute
    | "starting_skill_bonus";        // +N to a starting skill level
  payload: any;
}
```

### 3.2 Stacking Rules

- If `max_stacks > 1`, purchasing the perk N times applies its effects N times.
- Additive effects (e.g. `starting_attribute_bonus: +5 STR`) sum across stacks and across perks.
- Multiplicative effects (e.g. `meta_boost_xp_yield: ×1.05`) multiply across stacks/perks. **Order of application**: additive first, multiplicative second, then any flat overrides.
- A perk with `max_stacks = 1` cannot be repurchased; the UI hides the buy button after purchase.
- Soul Perks apply at `GameManager.begin_life()` — they pre-populate `CharacterState` and per-life `PerkSelectionState`.

```json
{
  "id": "def!soul_perk.early_bird",
  "display_name": "Early Bird",
  "description": "Start all lives with the Early Bird perk, unlocking the Morning slot.",
  "cost_lp": 5,
  "category": "TIME",
  "effects": [
    { "type": "start_with_perk", "payload": { "perk_id": "def!perk.early_riser" } }
  ],
  "requirements": [],
  "max_stacks": 1,
  "icon": "res://assets/icons/soul_perk_early_bird.png"
}
```

```json
{
  "id": "def!soul_perk.dreamer_xp",
  "display_name": "Dreamer's Echo",
  "description": "+5% XP gain across all sources for the next life.",
  "cost_lp": 8,
  "category": "STAT",
  "effects": [
    { "type": "meta_boost_xp_yield", "payload": { "mult": 1.05 } }
  ],
  "requirements": [
    { "type": "req_legend_rank", "min_rank": 2 }
  ],
  "max_stacks": 5,
  "icon": "res://assets/icons/soul_perk_dreamer.png"
}
```

### 3.3 MetaState (persistent)

```typescript
interface MetaState {
  legend_points: number;          // unspent LP currency
  legend_points_earned_total: number;  // drives Legend Rank
  legend_rank: number;            // derived, cached
  soul_perks: SoulPerkInstance[];
  heirlooms: HeirloomInstance[];
  deeds: DeedInstance[];          // permanent record
  key_bindings: Record<string, InputBinding>;
  metrics: Metrics;
  milestones: MilestoneInstance[];
}

interface SoulPerkInstance {
  perk_id: DefRef<"soul_perk">;
  stacks: number;
  purchased_at_life: number;
}

interface HeirloomInstance {
  heirloom_id: DefRef<"heirloom">;
  item_instance_id: string;       // UUID for the carried ItemInstance
  equipped_in_new_life: boolean;
}

interface DeedInstance {
  deed_id: DefRef<"deed">;
  recorded_at_life: number;        // which life number recorded it
  recorded_at_age: number;
  variant: string | null;          // for deeds with variants (spare/execute)
}
```

```json
{
  "legend_points": 47,
  "legend_points_earned_total": 122,
  "legend_rank": 3,
  "soul_perks": [
    { "perk_id": "def!soul_perk.early_bird", "stacks": 1, "purchased_at_life": 1 },
    { "perk_id": "def!soul_perk.dreamer_xp", "stacks": 2, "purchased_at_life": 2 }
  ],
  "heirlooms": [
    {
      "heirloom_id": "def!heirloom.temple_relic_coffer",
      "item_instance_id": "01HMQ...",
      "equipped_in_new_life": false
    }
  ],
  "deeds": [
    { "deed_id": "def!deed.av_caravans",       "recorded_at_life": 1, "recorded_at_age": 24, "variant": null },
    { "deed_id": "def!deed.av_mizgrub_spared", "recorded_at_life": 1, "recorded_at_age": 27, "variant": "spared" }
  ],
  "key_bindings": { "move_up": "KeyW", "interact": "KeyE" },
  "metrics": { "total_lives": 3, "total_combats": 89, "total_xp_earned": 124500 },
  "milestones": [
    { "milestone_id": "def!milestone.first_death",   "achieved_at_life": 1 },
    { "milestone_id": "def!milestone.spared_mizgrub","achieved_at_life": 1 }
  ]
}
```

---

## 4. Items & Equipment

### 4.1 ItemDef (static)

```typescript
interface ItemDef {
  id: DefRef<"item">;
  display_name: string;
  description: string;
  icon: string;
  category: "WEAPON" | "ARMOR" | "HELMET" | "SHIELD" | "ACCESSORY" | "GENERIC" | "TASK_ITEM";
  rarity: RarityId;
  tier: number;                  // 1..10 (used by weapons, 0 for non-tiered)
  equip_slot: EquipSlot | null;
  effects: ItemEffect[];        // applied when equipped / consumed
  weapon: WeaponDef | null;     // only if category === "WEAPON"
  stackable: boolean;
  value_gold: number;            // base shop value
  tags: string[];                // used by requirements, e.g. "holy_text"
}

type EquipSlot = "WEAPON" | "ARMOR" | "HELMET" | "SHIELD" | "ACCESSORY" | "BOOTS" | "GLOVES";

interface WeaponDef {
  class: "weapon_melee" | "weapon_ranged" | "weapon_magic";
  damage_min: number;
  damage_max: number;
  scaling_damage: number;        // 0.8..1.3 multiplier on stat-scaled damage
  scaling_stat: StatId;          // which attribute scales the damage
  attack_speed: number;          // attacks per second
  damage_type: "PHYSICAL" | "PIERCING" | "MAGIC" | "FIRE" | "LIGHTNING" | "HOLY";
  projectile_scene: string | null;   // null for melee
  ability_granted: DefRef<"ability"> | null;  // some weapons grant an ability
}
```

### 4.2 ItemEffect (static)

Effects are polymorphic by `$type`. See `GAME_MECHANICS.md §5.4` for the full list (40+ types). Common shape:

```typescript
interface ItemEffect {
  type: string;       // one of: effect_armor, effect_mod_attribute, eff_crit_chance, ...
  payload: ItemEffectPayload;
}

// Examples (one per type — designers extend as needed):
interface EffectArmor           { armor: number; }
interface EffectModAttribute    { stat: StatId; delta: number; }
interface EffCritChance         { crit_chance: number; }       // additive percent
interface EffWeaponDmg          { mult: number; }
interface EffAbilityDmg         { mult: number; }
interface EffAbilitySpeed      { mult: number; }
interface EffTypedDamage       { damage_type: string; mult: number; }
interface EffEnableAbility     { ability_id: DefRef<"ability">; }
interface EffMaxHpPercent       { percent: number; }
interface EffHealthRegen       { hp_per_sec: number; }
interface EffDayDuration       { mult: number; }
interface EffBoostXpGain       { mult: number; }
interface EffBoostSpGain       { skill_id: SkillId; mult: number; }
interface ModTaskEnergy        { mult: number; }
interface ModTaskMoney         { mult: number; }
interface ModMaxEnergy         { delta: number; }
interface ModMovementSpeed     { delta: number; }
interface GainBlockChance      { chance: number; }
interface GainLifesteal        { percent: number; }
interface EffSpiritSpawn       { spirit_id: DefRef<"spirit">; }
```

### 4.3 ItemInstance (per-life, persisted)

```typescript
interface ItemInstance {
  instance_id: string;            // UUID
  item_def_id: DefRef<"item">;
  rarity_override: RarityId | null; // for items with rarity rolls
  quantity: number;                 // for stackables
  equipped_slot: EquipSlot | null;
  rolled_modifiers: RolledModifier[];  // for items with random stat rolls
  durability: number | null;
}

interface RolledModifier {
  effect_type: string;
  value: number;                    // the rolled value within the effect's range
}
```

```json
{
  "instance_id": "01HMQ8X9...",
  "item_def_id": "def!item.sword_4",
  "rarity_override": "BLUE",
  "quantity": 1,
  "equipped_slot": "WEAPON",
  "rolled_modifiers": [
    { "effect_type": "eff_crit_chance", "value": 4 },
    { "effect_type": "effect_weapon_dmg", "value": 0.1 }
  ],
  "durability": null
}
```

### 4.4 WeaponDef Example

```json
{
  "id": "def!item.sword_4",
  "display_name": "Sword 4",
  "description": "A finely balanced blade. Tier 4 sword.",
  "icon": "res://assets/icons/weapons/sword_4.png",
  "category": "WEAPON",
  "rarity": "BLUE",
  "tier": 7,
  "equip_slot": "WEAPON",
  "effects": [
    { "type": "effect_weapon_dmg",  "payload": { "mult": 1.0 } }
  ],
  "weapon": {
    "class": "weapon_melee",
    "damage_min": 11.0,
    "damage_max": 12.0,
    "scaling_damage": 1.1,
    "scaling_stat": "STAT_STRENGTH",
    "attack_speed": 1.0,
    "damage_type": "PHYSICAL",
    "projectile_scene": null,
    "ability_granted": null
  },
  "stackable": false,
  "value_gold": 240,
  "tags": ["weapon", "sword", "tier7"]
}
```

### 4.5 Armor Example

```json
{
  "id": "def!item.iron_body",
  "display_name": "Iron Body Armor",
  "description": "Heavy iron plate. Excellent protection, slows you down.",
  "icon": "res://assets/icons/armor/iron_body.png",
  "category": "ARMOR",
  "rarity": "GREEN",
  "tier": 3,
  "equip_slot": "ARMOR",
  "effects": [
    { "type": "effect_armor",            "payload": { "armor": 12 } },
    { "type": "effect_damage_resistance", "payload": { "percent": 0.10 } },
    { "type": "mod_movement_speed",      "payload": { "delta": -8 } }
  ],
  "weapon": null,
  "stackable": false,
  "value_gold": 180,
  "tags": ["armor", "iron"]
}
```

### 4.6 Consumable Example

```json
{
  "id": "def!item.holy_water",
  "display_name": "Holy Water",
  "description": "Restores 30 HP and removes one negative status effect.",
  "icon": "res://assets/icons/consumables/holy_water.png",
  "category": "GENERIC",
  "rarity": "GRAY",
  "tier": 0,
  "equip_slot": null,
  "effects": [
    { "type": "gain_max_hp",            "payload": { "amount": 30, "heal": true } },
    { "type": "reward_remove_status_effect", "payload": { "any_negative": true } }
  ],
  "weapon": null,
  "stackable": true,
  "value_gold": 25,
  "tags": ["consumable", "holy"]
}
```

---

## 5. Combat Data

### 5.1 CombatStyle (static)

```typescript
interface CombatStyle {
  id: DefRef<"combat_style">;
  display_name: string;
  description: string;
  target_strategy: "NEAREST" | "WEAKEST" | "STRONGEST";
  base_attack_speed_mult: number;
  crit_chance_bonus: number;
  hp_mult: number;
  dodge_chance: number;
  block_rating: number;
  auto_abilities: DefRef<"ability">[];
  icon: string;
}
```

```json
{
  "id": "def!combat_style.sword_style",
  "display_name": "Sword Style",
  "description": "Technical swordplay. Balanced offense and defense.",
  "target_strategy": "NEAREST",
  "base_attack_speed_mult": 1.1,
  "crit_chance_bonus": 0.05,
  "hp_mult": 1.0,
  "dodge_chance": 0.05,
  "block_rating": 8,
  "auto_abilities": ["def!ability.blades_slash"],
  "icon": "res://assets/icons/combat_styles/sword_style.png"
}
```

### 5.2 AbilityDef (static)

```typescript
interface AbilityDef {
  id: DefRef<"ability">;
  ability_name: string;
  ability_description: string;   // rich text
  ability_stats_description: string; // rich text with {DMG} {SPD} {CRIT} tokens
  ability_type: "ACTIVE" | "PASSIVE";
  is_auto: boolean;              // auto-fired on cooldown if true
  cooldown_sec: number;
  damage_min: number | null;
  damage_max: number | null;
  crit_chance: number;           // 0..1
  aoe: boolean;
  targets_max: number;           // 1 for single, 3 for piercing, 0 for self-buff
  damage_type: string;
  ability_icon: string;
  projectile_scene: string | null;
  targeting: "WEAKEST" | "NEAREST" | "STRONGEST" | "SELF" | "ALL_ENEMIES";
}
```

```json
{
  "id": "def!ability.assassinate",
  "ability_name": "Assassinate",
  "ability_description": "Leap to a target and deal a deadly strike.\nAUTO: Chooses the weakest target.\n",
  "ability_stats_description": "[color=#DAA520]{DMG} 8 - 12[/color]\n[color=#DAA520]{SPD} 10s[/color]\n{CRIT} 10%\n",
  "ability_type": "ACTIVE",
  "is_auto": true,
  "cooldown_sec": 10.0,
  "damage_min": 8.0,
  "damage_max": 12.0,
  "crit_chance": 0.10,
  "aoe": false,
  "targets_max": 1,
  "damage_type": "PHYSICAL",
  "ability_icon": "res://assets/icons/abilities/assassinate.png",
  "projectile_scene": "res://scenes/projectiles/leap_slash.scn",
  "targeting": "WEAKEST"
}
```

### 5.3 EncounterDef (static)

```typescript
interface EncounterDef {
  id: DefRef<"encounter">;
  display_name: string;
  category: "COMBAT" | "GATHERING" | "TREASURE" | "PEACEFUL";
  stages: EncounterStage[];
  scaling_profile_id: DefRef<"scaling_profile">;
  waves: Wave[] | null;           // for COMBAT encounters
  loot_table_id: DefRef<"loot_table"> | null;
  info: string | null;            // "Boss" for boss encounters
}

interface Wave {
  mob_def_ids: DefRef<"mob">[];   // possible mobs in this wave
  count_min: number;
  count_max: number;
  spawn_interval_base_sec: number;
  spawn_interval_decrease_per_minute: number;
  spawn_interval_min_sec: number;
  spawn_cap: number;
  grid_spawn: boolean;
  no_overlap_spawn: boolean;
}

interface ScalingProfile {
  id: DefRef<"scaling_profile">;
  scaling_damage: number;         // 0.8..1.3
  scaling_health: number;         // 0.8..3.5
}
```

```json
{
  "id": "def!encounter.southern_woods",
  "display_name": "Southern Woods Patrol",
  "category": "COMBAT",
  "stages": [
    { "stage_index": 0, "wave_ids": ["wave_1", "wave_2"] }
  ],
  "scaling_profile_id": "def!scaling_profile.woods_standard",
  "waves": [
    {
      "mob_def_ids": ["def!mob.wolf2", "def!mob.bat"],
      "count_min": 4,
      "count_max": 6,
      "spawn_interval_base_sec": 2.5,
      "spawn_interval_decrease_per_minute": 0.4,
      "spawn_interval_min_sec": 1.0,
      "spawn_cap": 3,
      "grid_spawn": true,
      "no_overlap_spawn": true
    },
    {
      "mob_def_ids": ["def!mob.wolf3"],
      "count_min": 1,
      "count_max": 1,
      "spawn_interval_base_sec": 4.0,
      "spawn_interval_decrease_per_minute": 0.0,
      "spawn_interval_min_sec": 4.0,
      "spawn_cap": 1,
      "grid_spawn": false,
      "no_overlap_spawn": true
    }
  ],
  "loot_table_id": "def!loot.woodlands1",
  "info": null
}
```

### 5.4 MobDef (static)

```typescript
interface MobDef {
  id: DefRef<"mob">;
  display_name: string;
  sprite_scene: string;
  hp: number;
  damage_min: number;
  damage_max: number;
  speed: number;                 // px/sec in combat viewport
  attack_interval_sec: number;
  attack_range_px: number;
  ai_class: "Mob" | "ArcherMob" | "CasterMob" | "DummyMob";
  damage_type: string;
  armor_type: string;
  tags: string[];
  loot_table_id: DefRef<"loot_table"> | null;
  projectile_scene: string | null;  // for ArcherMob / CasterMob
  info: string | null;               // "Boss"
  xp_reward: number;
  gold_reward_min: number;
  gold_reward_max: number;
}
```

```json
{
  "id": "def!mob.wolf3",
  "display_name": "Danger Wolf",
  "sprite_scene": "res://scenes/mobs/wolf3.scn",
  "hp": 60,
  "damage_min": 8,
  "damage_max": 12,
  "speed": 70,
  "attack_interval_sec": 1.2,
  "attack_range_px": 36,
  "ai_class": "Mob",
  "damage_type": "PHYSICAL",
  "armor_type": "BEAST",
  "tags": ["beast", "wolf", "danger"],
  "loot_table_id": "def!loot.wolf_drops",
  "projectile_scene": null,
  "info": null,
  "xp_reward": 35,
  "gold_reward_min": 5,
  "gold_reward_max": 12
}
```

### 5.5 CombatResult (transient)

```typescript
interface CombatResult {
  outcome: "VICTORY" | "DEFEAT" | "RETREAT";
  encounter_id: DefRef<"encounter">;
  waves_cleared: number;
  enemies_killed: number;
  damage_dealt: number;
  damage_taken: number;
  crits_landed: number;
  duration_sec: number;
  rewards_applied: Reward[];
  loot_drops: ItemInstance[];
  death_cause: DeathCause | null;   // set if DEFEAT
}
```

---

## 6. World & Locations

### 6.1 WorldRegion (static)

```typescript
interface WorldRegion {
  id: DefRef<"region">;
  display_name: string;
  description: string;
  exploration_points_type: RegionId;   // goods sub-currency
  map_icon: string;
  scene: string;                        // town/area scene path
  encounter_ids: DefRef<"encounter">[];
  location_ids: DefRef<"location">[];
  unlock_requirements: Requirement[];
  is_demo_locked: boolean;             // Valenthar etc.
}
```

### 6.2 Location (static)

```typescript
interface LocationDef {
  id: DefRef<"location">;
  display_name: string;
  description: string;
  region_id: DefRef<"region">;
  kind: "TOWN" | "BUILDING" | "DUNGEON" | "ADVENTURE_AREA" | "TREASURE";
  scene: string;
  icon: string;
  npc_ids: DefRef<"npc">[];
  shop_id: DefRef<"shop"> | null;
  encounter_id: DefRef<"encounter"> | null;
  unlock_requirements: Requirement[];
  parent_location_id: DefRef<"location"> | null;  // for interiors
}
```

```json
{
  "id": "def!location.training_grounds",
  "display_name": "Training Grounds",
  "description": "A scarred woman eyes you from beside a rack of weapons.",
  "region_id": "def!region.ashvale",
  "kind": "BUILDING",
  "scene": "res://scenes/locations/training_grounds.scn",
  "icon": "res://assets/icons/locations/training_grounds.png",
  "npc_ids": ["def!npc.helga"],
  "shop_id": null,
  "encounter_id": "def!encounter.training_grounds_upgrade2",
  "unlock_requirements": [
    { "type": "req_campaign_flag", "flag": "met_helga", "value": true }
  ],
  "parent_location_id": "def!location.ashvale_center"
}
```

### 6.3 WorldState (per-life)

```typescript
interface WorldState {
  unlocked_region_ids: DefRef<"region">[];
  unlocked_location_ids: DefRef<"location">[];
  region_flags: Record<string, boolean | number | string>;
  goods_by_region: Record<RegionId, number>;
  location_states: Record<DefRef<"location">, LocationState>;
  npc_states: Record<DefRef<"npc">, NPCState>;
  active_shortages: ShopShortage[];
}

interface LocationState {
  visited: boolean;
  cleared: boolean;             // for dungeons
  times_visited: number;
  last_visited_day: number;
}

interface ShopShortage {
  shop_id: DefRef<"shop">;
  shortage_id: string;
  expires_day: number;
}
```

---

## 7. Jobs & Tasks

### 7.1 JobDef (static)

```typescript
interface JobDef {
  id: DefRef<"job">;
  display_name: string;
  description: string;
  primary_skill: SkillId;
  tier: number;                  // 1..3 (t1_farmhand, t3_hunter)
  energy_cost: number;
  time_cost_sec: number;         // base time (modified by speed mult)
  xp_reward: number;
  gold_reward_min: number;
  gold_reward_max: number;
  sp_reward: number;
  task_effects: TaskEffect[];    // additional rewards (items, narrative events, LP)
  time_of_day_bonuses: Partial<Record<TimeOfDay, number>>;
  tags: string[];                 // "roguery" jobs give "extra coin on the side"
  requirements: Requirement[];
}

interface TaskEffect {
  type:
    | "gain_money" | "gain_xp" | "gain_xp_simple" | "gain_sp_simple"
    | "gain_lp_simple" | "gain_rp_simple" | "gain_tp_simple"
    | "gain_goods" | "gain_item" | "gain_energy" | "gain_opportunity"
    | "gain_narrative_event" | "gain_prayer_point" | "chance_gain";
  payload: any;
}
```

```json
{
  "id": "def!job.t3_hunter",
  "display_name": "Novice Hunter",
  "description": "Trains {SKILL_HUNTING} [color=#DAA520]Hunting[/color].",
  "primary_skill": "SKILL_HUNTING",
  "tier": 3,
  "energy_cost": 3,
  "time_cost_sec": 120,
  "xp_reward": 80,
  "gold_reward_min": 8,
  "gold_reward_max": 18,
  "sp_reward": 2,
  "task_effects": [
    { "type": "gain_xp",         "payload": { "skill_id": "SKILL_HUNTING", "amount": 80 } },
    { "type": "gain_sp_simple",  "payload": { "skill_id": "SKILL_HUNTING", "amount": 2 } }
  ],
  "time_of_day_bonuses": { "MORNING": 1.15, "EVENING": 0.85 },
  "tags": ["hunting", "outdoors"],
  "requirements": [
    { "type": "req_skill_level", "skill_id": "SKILL_HUNTING", "min_level": 5 }
  ]
}
```

### 7.2 TaskState (per-life)

```typescript
interface TasksState {
  active_slots: TaskSlot[];       // max 3 by default, expanded by perks
  cooldowns: Record<DefRef<"job">, number>; // cooldown end day
  professions_unlocked: DefRef<"profession">[];
  profession_levels: Record<DefRef<"profession">, number>;
}

interface TaskSlot {
  slot_id: string;
  job_id: DefRef<"job">;
  started_day: number;
  started_time_of_day: TimeOfDay;
  completes_at_day: number;
  completes_at_time_of_day: TimeOfDay;
  state: "PENDING" | "IN_PROGRESS" | "COMPLETE" | "CANCELLED";
}

interface ProfessionDef {
  id: DefRef<"profession">;
  display_name: string;
  job_ids: DefRef<"job">[];
  tier_max: number;
  unlock_requirements: Requirement[];
}
```

```json
{
  "active_slots": [
    {
      "slot_id": "slot_1",
      "job_id": "def!job.t3_hunter",
      "started_day": 42,
      "started_time_of_day": "MORNING",
      "completes_at_day": 42,
      "completes_at_time_of_day": "DAY",
      "state": "IN_PROGRESS"
    }
  ],
  "cooldowns": { "def!job.t3_hunter": 43 },
  "professions_unlocked": ["def!profession.hunter", "def!profession.miner"],
  "profession_levels": { "def!profession.hunter": 2, "def!profession.miner": 1 }
}
```

---

## 8. NPCs & Contacts

### 8.1 NPCDef / ContactDef (static)

```typescript
interface NPCDef {
  id: DefRef<"npc">;
  display_name: string;
  portrait: string;
  schedule: NPCSchedule | null;   // null for non-roaming NPCs
  speaker_id: DefRef<"speaker">;
  shop_id: DefRef<"shop"> | null;
  services: NPCService[];
  initial_relationship: number;   // 0..100
  contact_id: DefRef<"contact"> | null;
}

interface NPCSchedule {
  morning_location: DefRef<"location">;
  day_location: DefRef<"location">;
  evening_location: DefRef<"location">;
}

interface NPCService {
  type: "SHOP" | "TRAINING" | "DIALOGUE" | "QUEST_GIVER" | "HEAL";
  payload: any;
}

interface ContactDef {
  id: DefRef<"contact">;
  display_name: string;
  description: string;
  yields: ContactYield[];         // benefits unlocked at relationship thresholds
  unlock_requirements: Requirement[];
}

interface ContactYield {
  relationship_threshold: number; // 0..100
  yield_type: "SHOP_ACCESS" | "QUEST" | "BONUS" | "STORY";
  payload: any;
}
```

### 8.2 NPCState (per-life)

```typescript
interface NPCState {
  relationship: number;            // 0..100
  interactions_count: number;
  last_interaction_day: number;
  quests_completed: DefRef<"quest">[];
  topics_unlocked: DefRef<"contact_topic">[];
}
```

```json
{
  "relationship": 45,
  "interactions_count": 12,
  "last_interaction_day": 38,
  "quests_completed": ["def!quest.caravan_investigation"],
  "topics_unlocked": ["def!contact_topic.ashvale_merchant_yields"]
}
```

### 8.3 DialogueSpeaker (static)

```typescript
interface DialogueSpeaker {
  id: DefRef<"speaker">;
  display_name: string;
  portrait: string;
  default_color: ColorHex;
  voice_sfx: string | null;
}
```

```json
{
  "id": "def!speaker.narrator",
  "display_name": "Narrator",
  "portrait": "res://assets/portraits/narrator.png",
  "default_color": "#E8D9B0",
  "voice_sfx": null
}
```

---

## 9. Save File Structure

### 9.1 Top-Level Save Document

```typescript
interface SaveFile {
  save_version: number;            // CURRENT = 3
  meta: SaveMeta;
  calendar_state: CalendarState;
  campaign_state: CampaignState;
  character_state: CharacterState;
  inventories_state: InventoriesState;
  journal_state: JournalState;
  loot_state: LootState;
  meta_state: MetaState;
  narrative_state: NarrativeState;
  perk_selection_state: PerkSelectionState;
  run_state: RunState;
  shop_data: ShopData;
  tasks_state: TasksState;
  web_state: WebState;
  world_state: WorldState;
  metrics: Metrics;
  milestones: MilestoneState;
}

interface SaveMeta {
  origin_id: DefRef<"origin">;
  backstory_id: DefRef<"backstory">;
  played_at: string;              // ISO 8601
  playtime_sec: number;
  lifetime_id: string;             // UUID for this run
  lives_lived: number;
}

interface RunState {
  run_id: string;
  origin_id: DefRef<"origin">;
  backstory_id: DefRef<"backstory">;
  started_at_real: string;
  life_number: number;
  started_age_years: number;
  current_age_years: number;
  days_played: number;
}

interface CalendarState {
  day: number;
  year: number;
  season: Season;
  time_of_day: TimeOfDay;
  day_duration_sec: number;         // modified by eff_day_duration
  turn_of_the_year_resolved: boolean;
}

interface CampaignState {
  flags: Record<string, boolean | number | string>;
  unlocked_webs: DefRef<"web">[];
  unlocked_regions: DefRef<"region">[];
  unlocked_combat_styles: DefRef<"combat_style">[];
  unlocked_tabs: string[];
  unlocked_perks_categories: string[];
  unlocked_professions: DefRef<"profession">[];
}

interface InventoriesState {
  gold: number;
  backpack: ItemInstance[];        // items not equipped
  equipment: Partial<Record<EquipSlot, ItemInstance>>;
  heirloom_bag: ItemInstance[];     // carried from meta_state into life
}

interface JournalState {
  threads: JournalThread[];
  side_quests: JournalSideQuest[];
  events: JournalEvent[];
  entries: JournalEntry[];
}

interface JournalThread {
  thread_id: DefRef<"journal_thread">;
  display_name: string;
  objectives: JournalThreadObjective[];
  impacts: JournalThreadImpact[];
  segments: JournalThreadSegment[];
  state: "ACTIVE" | "COMPLETED" | "FAILED";
}

interface PerkSelectionState {
  unlocked_perk_ids: DefRef<"perk">[];
  selected_perk_ids: DefRef<"perk">[];
  perk_points_available: number;
  blocked_perk_ids: DefRef<"perk">[];   // eff_blocks_perk
}

interface ShopData {
  shops: Record<DefRef<"shop">, ShopStockInstance>;
}

interface ShopStockInstance {
  shop_id: DefRef<"shop">;
  tier: number;
  items: ShopItemInstance[];      // currently stocked
  shortages: ShopShortage[];
  refresh_day: number;
}

interface ShopItemInstance {
  shop_item_id: DefRef<"shop_item">;
  item_def_id: DefRef<"item">;
  price_gold: number;
  stock_count: number;            // -1 for infinite
  is_guaranteed: boolean;
}

interface LootState {
  pending_loot_table_ids: DefRef<"loot_table">[];
  discovered_loot_ids: DefRef<"loot">[];
  pending_drops: ItemInstance[];
}

interface LootTable {
  id: DefRef<"loot_table">;
  guaranteed_items: DefRef<"item">[];
  fixed_items: DefRef<"item">[];
  extra_items: LootTableEntry[];
  discoveries: DefRef<"loot">[];
}

interface LootTableEntry {
  item_def_id: DefRef<"item">;
  weight: number;
  min_rarity: RarityId;
  max_rarity: RarityId;
  chance: number;                 // 0..1
}

interface NarrativeState {
  active_event_id: DefRef<"narrative_event"> | null;
  current_page_index: number;
  dialogue_history: DialogueLine[];
  pending_options: NarrativeOption[];
}

interface Metrics {
  total_lives: number;
  total_combats: number;
  total_xp_earned: number;
  total_gold_earned: number;
  total_deeds: number;
  deaths_by_cause: Record<DeathCause, number>;
  longest_life_days: number;
}

interface MilestoneState {
  achieved: MilestoneInstance[];
}

interface MilestoneInstance {
  milestone_id: DefRef<"milestone">;
  achieved_at_life: number;
  achieved_at_age: number;
}
```

### 9.2 Full Save Example

```json
{
  "save_version": 3,
  "meta": {
    "origin_id": "def!origin.prisoner",
    "backstory_id": "def!backstory.fighter",
    "played_at": "2026-07-29T05:34:13+08:00",
    "playtime_sec": 4123,
    "lifetime_id": "01HMQ8X9R4V2Z3...",
    "lives_lived": 3
  },
  "run_state": {
    "run_id": "01HMQ8X9R4V2Z3",
    "origin_id": "def!origin.prisoner",
    "backstory_id": "def!backstory.fighter",
    "started_at_real": "2026-07-28T22:00:00+08:00",
    "life_number": 4,
    "started_age_years": 14,
    "current_age_years": 28,
    "days_played": 420
  },
  "calendar_state": {
    "day": 420,
    "year": 2,
    "season": "AMBERFALL",
    "time_of_day": "DAY",
    "day_duration_sec": 180,
    "turn_of_the_year_resolved": false
  },
  "campaign_state": {
    "flags": {
      "arrived_in_ashvale": true,
      "caravans_saved": true,
      "training_grounds_upgraded": false,
      "mizgrub_spared": true
    },
    "unlocked_webs": ["def!web.ashvale_main", "def!web.woodlands_main"],
    "unlocked_regions": ["def!region.ashvale", "def!region.woodlands"],
    "unlocked_combat_styles": ["def!combat_style.power", "def!combat_style.sword_style"],
    "unlocked_tabs": ["character", "inventory", "perks", "quests", "shop", "region", "abilities", "story"],
    "unlocked_perks_categories": ["combat", "skill", "utility"],
    "unlocked_professions": ["def!profession.hunter", "def!profession.miner"]
  },
  "character_state": { "...": "see §1.1" },
  "inventories_state": {
    "gold": 540,
    "backpack": [
      {
        "instance_id": "01HMR...",
        "item_def_id": "def!item.holy_water",
        "rarity_override": null,
        "quantity": 3,
        "equipped_slot": null,
        "rolled_modifiers": [],
        "durability": null
      }
    ],
    "equipment": {
      "WEAPON": { "instance_id": "01HMS...", "item_def_id": "def!item.sword_4",
                  "rarity_override": "BLUE", "quantity": 1, "equipped_slot": "WEAPON",
                  "rolled_modifiers": [{"effect_type":"eff_crit_chance","value":4}], "durability": null },
      "ARMOR":  { "instance_id": "01HMA...", "item_def_id": "def!item.iron_body",
                  "rarity_override": "GREEN", "quantity": 1, "equipped_slot": "ARMOR",
                  "rolled_modifiers": [], "durability": null }
    },
    "heirloom_bag": []
  },
  "journal_state": {
    "threads": [
      {
        "thread_id": "def!journal_thread.ashvale_arrival",
        "display_name": "Arrival in Ashvale",
        "objectives": [
          { "objective_id": "obj_1", "text": "Speak to the merchant", "complete": true },
          { "objective_id": "obj_2", "text": "Investigate the caravans", "complete": true }
        ],
        "impacts": [],
        "segments": [],
        "state": "COMPLETED"
      },
      {
        "thread_id": "def!journal_thread.goblin_trouble",
        "display_name": "Goblin Raiders",
        "objectives": [
          { "objective_id": "obj_1", "text": "Find the goblin camp", "complete": true },
          { "objective_id": "obj_2", "text": "Deal with Mizgrub", "complete": false }
        ],
        "impacts": [],
        "segments": [],
        "state": "ACTIVE"
      }
    ],
    "side_quests": [],
    "events": [
      { "event_id": "def!journal_event.first_combat", "day": 12, "text": "You fought your first wolf." }
    ],
    "entries": [
      { "entry_id": "def!journal_entry.ashvale_history", "title": "Ashvale",
        "text": "Kingdoms rose and fell in this region eons ago..." }
    ]
  },
  "loot_state": {
    "pending_loot_table_ids": [],
    "discovered_loot_ids": ["def!loot.lost_temple", "def!loot.woodlands1"],
    "pending_drops": []
  },
  "meta_state": { "...": "see §3.3" },
  "narrative_state": {
    "active_event_id": null,
    "current_page_index": 0,
    "dialogue_history": [],
    "pending_options": []
  },
  "perk_selection_state": {
    "unlocked_perk_ids": ["def!perk.blademaster_i", "def!perk.forager", "def!perk.shop_discount"],
    "selected_perk_ids": ["def!perk.blademaster_i", "def!perk.shop_discount"],
    "perk_points_available": 1,
    "blocked_perk_ids": []
  },
  "shop_data": {
    "shops": {
      "def!shop.village_trader": {
        "shop_id": "def!shop.village_trader",
        "tier": 2,
        "items": [
          {
            "shop_item_id": "def!shop_item.trader_sword_3",
            "item_def_id": "def!item.sword_3",
            "price_gold": 140,
            "stock_count": 1,
            "is_guaranteed": true
          }
        ],
        "shortages": [],
        "refresh_day": 425
      }
    }
  },
  "tasks_state": { "...": "see §7.2" },
  "web_state": { "...": "see §2.3" },
  "world_state": {
    "unlocked_region_ids": ["def!region.ashvale", "def!region.woodlands"],
    "unlocked_location_ids": ["def!location.ashvale_center","def!location.training_grounds","def!location.mine"],
    "region_flags": {},
    "goods_by_region": {
      "EXPLORATION_POINTS_PRISON": 0,
      "EXPLORATION_POINTS_ROADS": 12,
      "EXPLORATION_POINTS_TOWN": 8,
      "EXPLORATION_POINTS_WOODLANDS": 24
    },
    "location_states": {
      "def!location.training_grounds": { "visited": true, "cleared": false, "times_visited": 3, "last_visited_day": 418 }
    },
    "npc_states": {
      "def!npc.ashvale_merchant": { "relationship": 45, "interactions_count": 12,
                                     "last_interaction_day": 38, "quests_completed": [],
                                     "topics_unlocked": [] }
    },
    "active_shortages": []
  },
  "metrics": {
    "total_lives": 3, "total_combats": 89, "total_xp_earned": 124500,
    "total_gold_earned": 4200, "total_deeds": 4,
    "deaths_by_cause": { "NATURAL": 1, "COMBAT": 2, "EVENT": 0, "QUIT": 0 },
    "longest_life_days": 510
  },
  "milestones": {
    "achieved": [
      { "milestone_id": "def!milestone.first_death",   "achieved_at_life": 1, "achieved_at_age": 70 },
      { "milestone_id": "def!milestone.spared_mizgrub","achieved_at_life": 1, "achieved_at_age": 27 }
    ]
  }
}
```

---

## 10. Balance Curves

### 10.1 XP Curves (lvl_curve / smart_lvl_curve)

Two curve implementations ship; both are pure functions of level. Designers pick one per system (attributes use `smart_lvl_curve`, character level uses `lvl_curve`).

```typescript
interface LvlCurveDef {
  id: DefRef<"lvl_curve">;
  kind: "LINEAR" | "EXPONENTIAL" | "SMART" | "TABLE";
  base_xp: number;                // xp needed for level 1→2
  growth_rate: number;            // multiplier per level (exponential) or slope (linear)
  table?: number[];               // explicit XP-per-level for TABLE kind
  cap_level?: number;             // hard cap, beyond which xp_for_level returns Infinity
}

// xp_for_level(n) = base_xp * growth_rate^(n-1)            // EXPONENTIAL
// xp_for_level(n) = base_xp + (n-1) * growth_rate          // LINEAR
// xp_for_level(n) = table[n]                                // TABLE
// xp_for_level(n) = base_xp * (n^1.5)                       // SMART (smoothed)
```

```json
{
  "id": "def!lvl_curve.attribute_default",
  "kind": "EXPONENTIAL",
  "base_xp": 100,
  "growth_rate": 1.18,
  "cap_level": 80
}
```

| Level | XP needed (EXPONENTIAL base 100, growth 1.18) |
|-------|-----------------------------------------------|
| 1→2   | 100                                            |
| 5→6   | ~194                                           |
| 10→11 | ~512                                           |
| 20→21 | ~2,620                                         |
| 40→41 | ~13,720                                        |
| 80    | cap                                            |

### 10.2 Aging Curve (life stage transitions)

```typescript
interface AgingCurveDef {
  id: DefRef<"aging_curve">;
  stages: { stage_id: LifeStageId; min_age: number; max_age: number; }[];
  default_max_age: number;
  soul_perk_max_age_bonus_cap: number;
}
```

```json
{
  "id": "def!aging_curve.default",
  "stages": [
    { "stage_id": "stage1_young",   "min_age": 0,  "max_age": 14 },
    { "stage_id": "stage3_veteran", "min_age": 15, "max_age": 34 },
    { "stage_id": "stage4_elder",   "min_age": 35, "max_age": 54 },
    { "stage_id": "stage5_decrepit","min_age": 55, "max_age": 120 }
  ],
  "default_max_age": 70,
  "soul_perk_max_age_bonus_cap": 20
}
```

### 10.3 Attribute Scaling (derived stats)

```typescript
interface AttributeScalingDef {
  id: DefRef<"attribute_scaling">;
  // For each derived stat, list source attributes and their weights
  derivations: {
    max_hp:        { base: number; per_vig: number; per_str: number; mult_per_level: number };
    max_energy:    { base: number; per_vig: number };
    crit_chance:   { base: number; per_per: number; cap: number };
    crit_mult:     { base: number; per_per: number };
    block_rating:  { base: number; per_str: number; per_vig: number };
    dodge_chance:  { base: number; per_dex: number; cap: number };
    move_speed:    { base: number; per_dex: number };
    // Weapon-scaled damage uses weapon.scaling_damage * (stat.effective_level / 10)
  };
}
```

```json
{
  "id": "def!attribute_scaling.default",
  "derivations": {
    "max_hp":       { "base": 30, "per_vig": 4, "per_str": 1, "mult_per_level": 1.05 },
    "max_energy":   { "base": 8,  "per_vig": 0.3 },
    "crit_chance":  { "base": 0.02, "per_per": 0.004, "cap": 0.50 },
    "crit_mult":    { "base": 1.5, "per_per": 0.02 },
    "block_rating": { "base": 0,  "per_str": 0.4, "per_vig": 0.4 },
    "dodge_chance": { "base": 0.02, "per_dex": 0.004, "cap": 0.40 },
    "move_speed":   { "base": 70, "per_dex": 0.6 }
  }
}
```

### 10.4 Damage Tier Curve (weapons)

```typescript
interface WeaponTierCurveDef {
  id: DefRef<"weapon_tier_curve">;
  // damage_min/max for each tier — designers extend per weapon class
  melee:  { tier: number; damage_min: number; damage_max: number; scaling_damage: number }[];
  ranged: { tier: number; damage_min: number; damage_max: number; scaling_damage: number }[];
  magic:   { tier: number; damage_min: number; damage_max: number; scaling_damage: number }[];
}
```

```json
{
  "id": "def!weapon_tier_curve.swords",
  "melee": [
    { "tier": 1, "damage_min": 4,  "damage_max": 5,  "scaling_damage": 0.8 },
    { "tier": 2, "damage_min": 5,  "damage_max": 6,  "scaling_damage": 0.9 },
    { "tier": 3, "damage_min": 6,  "damage_max": 7,  "scaling_damage": 0.95 },
    { "tier": 4, "damage_min": 7,  "damage_max": 8,  "scaling_damage": 1.0 },
    { "tier": 5, "damage_min": 8,  "damage_max": 9,  "scaling_damage": 1.05 },
    { "tier": 6, "damage_min": 10, "damage_max": 11, "scaling_damage": 1.1 },
    { "tier": 7, "damage_min": 11, "damage_max": 12, "scaling_damage": 1.15 },
    { "tier": 8, "damage_min": 13, "damage_max": 14, "scaling_damage": 1.2 },
    { "tier": 9, "damage_min": 15, "damage_max": 16, "scaling_damage": 1.25 },
    { "tier": 10,"damage_min": 16, "damage_max": 18, "scaling_damage": 1.3 }
  ],
  "ranged": [],
  "magic": []
}
```

### 10.5 Shop Tier Distribution (drop rates)

```typescript
interface RarityDistributionDef {
  id: DefRef<"rarity_distribution">;
  // per shop tier, the weight for each rarity
  tiers: Record<number, Record<RarityId, number>>;
}
```

```json
{
  "id": "def!rarity_distribution.shop_default",
  "tiers": {
    "1": { "GRAY": 70, "GREEN": 25, "BLUE": 5,  "RED": 0,  "GOLD": 0, "WHITE": 0, "DESTINY": 0 },
    "2": { "GRAY": 50, "GREEN": 35, "BLUE": 12, "RED": 3,  "GOLD": 0, "WHITE": 0, "DESTINY": 0 },
    "3": { "GRAY": 30, "GREEN": 40, "BLUE": 22, "RED": 7,  "GOLD": 1, "WHITE": 0, "DESTINY": 0 },
    "4": { "GRAY": 10, "GREEN": 30, "BLUE": 35, "RED": 20, "GOLD": 4, "WHITE": 1, "DESTINY": 0 },
    "5": { "GRAY": 0,  "GREEN": 15, "BLUE": 35, "RED": 35, "GOLD": 12,"WHITE": 3, "DESTINY": 0 }
  }
}
```

### 10.6 Energy & Task Curves

```typescript
interface EnergyCurveDef {
  id: DefRef<"energy_curve">;
  base_max: number;                // 10
  per_vig: number;                 // 0.3
  rest_per_day: number;            // 6
  rest_per_day_with_perk: number;  // 8 (nap perk)
}
```

---

## 11. Reward & Requirement Polymorphism

### 11.1 Reward (static, polymorphic by `type`)

```typescript
type Reward =
  | { type: "reward_xp";                  amount: number; skill_id?: SkillId; stat_id?: StatId }
  | { type: "reward_gold";                amount: number }
  | { type: "reward_goods";                amount: number; region: RegionId }
  | { type: "reward_lp";                  amount: number }
  | { type: "reward_rp";                  amount: number }
  | { type: "reward_sp";                  amount: number; skill_id: SkillId }
  | { type: "reward_item";                item_def_id: DefRef<"item">; rarity?: RarityId; quantity?: number }
  | { type: "reward_heirloom";            heirloom_id: DefRef<"heirloom"> }
  | { type: "reward_ability";             ability_id: DefRef<"ability"> }
  | { type: "reward_talent";              talent_id: DefRef<"talent"> }
  | { type: "reward_deed";                deed_id: DefRef<"deed"> }
  | { type: "reward_contact";             contact_id: DefRef<"contact"> }
  | { type: "reward_location";            location_id: DefRef<"location"> }
  | { type: "reward_region";              region_id: DefRef<"region"> }
  | { type: "reward_journal_entry";       entry_id: DefRef<"journal_entry"> }
  | { type: "reward_flag";                flag: string; value: boolean | number | string }
  | { type: "reward_world_state";         change: WorldStateChange }
  | { type: "reward_remove_status_effect"; status_effect_id: DefRef<"status_effect"> | "ANY_NEGATIVE" }
  | { type: "reward_unlock_perks";        category: string }
  | { type: "reward_unlock_profession";   profession_id: DefRef<"profession"> }
  | { type: "reward_unlock_tab";           tab_id: string }
  | { type: "reward_unlock_web";          web_id: DefRef<"web"> }
  | { type: "reward_upgrade_encounter";   encounter_id: DefRef<"encounter">; upgrade_id: string }
  | { type: "reward_combat_styles";       combat_style_ids: DefRef<"combat_style">[] }
  | { type: "reward_close_web";           web_id: DefRef<"web"> }
  | { type: "reward_show_task";           task_id: DefRef<"task"> }
  | { type: "reward_title";              title_id: DefRef<"title"> };
```

### 11.2 Requirement (static, polymorphic by `type`)

```typescript
type Requirement =
  | { type: "req_attribute";          stat: StatId; min_level: number }
  | { type: "req_skill_level";        skill_id: SkillId; min_level: number }
  | { type: "req_has_perk";           perk_id: DefRef<"perk"> }
  | { type: "req_talent_lvl";         talent_id: DefRef<"talent">; min_level: number }
  | { type: "req_world_state";        key: string; value: any }
  | { type: "req_campaign_flag";      flag: string; value: any }
  | { type: "req_deed";                deed_id: DefRef<"deed"> }
  | { type: "req_complete_node";      node_id: DefRef<"web_node"> }
  | { type: "req_legend_rank";        min_rank: number }
  | { type: "req_domain_rank";        domain: string; min_rank: number }
  | { type: "req_kill_mob";           mob_id: DefRef<"mob">; count: number }
  | { type: "req_kill_mob_matching_tag"; tag: string; count: number }
  | { type: "req_beat_encounter";     encounter_id: DefRef<"encounter"> }
  | { type: "req_beat_encounter_archetype"; archetype: string }
  | { type: "req_perform_task";       task_id: DefRef<"task">; count: number }
  | { type: "req_perform_task_with_tag"; tag: string; count: number }
  | { type: "req_profession_lvl";     profession_id: DefRef<"profession">; min_level: number }
  | { type: "req_earn_goods";         region: RegionId; amount: number }
  | { type: "req_not";                inner: Requirement }
  | { type: "trait_requirement";      trait_id: DefRef<"trait"> }
  | { type: "world_state_requirement";key: string; value: any }
  | { type: "condition_group";        op: "AND"|"OR"; inner: Requirement[] }
  | { type: "condition_has_campaign_flag"; flag: string; value: any }
  | { type: "condition_has_deed";     deed_id: DefRef<"deed"> }
  | { type: "condition_has_origin_tag"; tag: string }
  | { type: "condition_has_prior_life_deed"; deed_id: DefRef<"deed"> }
  | { type: "condition_complete_node";node_id: DefRef<"web_node"> }
  | { type: "condition_not";          inner: Requirement }
  | { type: "condition_has_cohort";   cohort_id: string };
```

### 11.3 PerkDef (static)

```typescript
interface PerkDef {
  id: DefRef<"perk">;
  display_name: string;
  description: string;
  category: "COMBAT" | "SKILL" | "UTILITY" | "LIFESTYLE" | "SPECIAL";
  effects: PerkEffect[];
  requirements: Requirement[];
  blocks_perks: DefRef<"perk">[];     // mutually exclusive perks
  icon: string;
}

interface PerkEffect {
  type: string;        // mirrors ItemEffect type list (see §4.2)
  payload: any;
}
```

```json
{
  "id": "def!perk.dense",
  "display_name": "Dense",
  "description": "[color=green]+25%[/color] Loot Chance (Wilds)",
  "category": "UTILITY",
  "effects": [
    { "type": "eff_boost_feat_lp", "payload": { "feature": "loot_chance", "region": "WOODLANDS", "mult": 1.25 } }
  ],
  "requirements": [
    { "type": "req_skill_level", "skill_id": "SKILL_DELVING", "min_level": 3 }
  ],
  "blocks_perks": [],
  "icon": "res://assets/icons/perks/dense.png"
}
```

---

## 12. Heirlooms & Deeds

### 12.1 HeirloomDef (static)

```typescript
interface HeirloomDef {
  id: DefRef<"heirloom">;
  display_name: string;
  description: string;
  source_quest_id: DefRef<"quest"> | null;
  item_def_id: DefRef<"item">;     // the underlying item that carries across lives
  granted_by_reward: DefRef<"reward_heirloom">;
}
```

```json
{
  "id": "def!heirloom.temple_relic_coffer",
  "display_name": "Temple Relic Coffer",
  "description": "An ancient coffer unearthed from a lost temple. It carries a sliver of past lives with it.",
  "source_quest_id": "def!quest.lost_temple",
  "item_def_id": "def!item.temple_relic_coffer",
  "granted_by_reward": "def!reward_heirloom.temple_relic_coffer"
}
```

### 12.2 DeedDef (static)

```typescript
interface DeedDef {
  id: DefRef<"deed">;
  display_name: string;
  description: string;
  category: "STORY" | "COMBAT" | "ECONOMY" | "SOCIAL";
  variants: { id: string; display_name: string; description: string }[] | null;
  lp_bonus: number;
  affects_narrative: boolean;      // if true, future lives can react to this deed
  review_text_template: string;    // shown in life review
}
```

```json
{
  "id": "def!deed.av_mizgrub_spared",
  "display_name": "Mizgrub Spared",
  "description": "You spared the goblin raider when you did not have to.",
  "category": "STORY",
  "variants": null,
  "lp_bonus": 5,
  "affects_narrative": true,
  "review_text_template": "{NAME} spared the merchant's supply lines, allowing him to expand his stock."
}
```

---

## 13. Status Effects

### 13.1 StatusEffectDef (static)

```typescript
interface StatusEffectDef {
  id: DefRef<"status_effect">;
  display_name: string;
  description: string;
  icon: string;
  category: "BUFF" | "DEBUFF" | "STARTING" | "INJURY";
  duration_sec: number | null;     // null = permanent until removed
  tick_sec: number;                // 0 = no tick
  effects: ItemEffect[];            // applied continuously / on tick
  is_removable_by_rest: boolean;
  is_removable_by_item: boolean;
}
```

```json
{
  "id": "def!status_effect.early_years",
  "display_name": "Early Years",
  "description": "The vigor of youth. +10% to all physical stats.",
  "icon": "res://assets/icons/status/early_years.png",
  "category": "STARTING",
  "duration_sec": null,
  "tick_sec": 0,
  "effects": [
    { "type": "effect_mod_attribute", "payload": { "stat": "STAT_STRENGTH",   "delta": 1 } },
    { "type": "effect_mod_attribute", "payload": { "stat": "STAT_DEXTERITY",  "delta": 1 } },
    { "type": "effect_mod_attribute", "payload": { "stat": "STAT_VIGOR",      "delta": 1 } }
  ],
  "is_removable_by_rest": false,
  "is_removable_by_item": false
}
```

---

## 14. Quiet Years

### 14.1 QuietYearPath (static)

```typescript
interface QuietYearPath {
  id: DefRef<"qy_path">;
  display_name: string;
  description: string;
  blurb_template: string;          // per-year blurb text with {YEAR} {AGE} placeholders
  available_from_stage: LifeStageId;
  impacts: QuietYearImpact[];
  event_ids: DefRef<"qy_event">[];  // events that can fire per year on this path
}

interface QuietYearImpact {
  type: "stat_delta" | "skill_delta" | "gold_delta" | "lp_delta" | "narrative_unlock";
  payload: any;
  chance: number;                  // 0..1, rolled per year
}

interface QYTimelineEvent {
  event_id: DefRef<"qy_event">;
  year: number;
  age: number;
  choice: QYTimelineEventChoice | null;
  applied_impacts: QuietYearImpact[];
}

interface QYTimelineEventChoice {
  option_id: string;
  display_text: string;
  impacts: QuietYearImpact[];
}
```

```json
{
  "id": "def!qy_path.mentor",
  "display_name": "Mentor",
  "description": "Take on apprentices. Pass on what you've learned.",
  "blurb_template": "In year {YEAR}, you took on another apprentice. They were eager, if clumsy.",
  "available_from_stage": "stage4_elder",
  "impacts": [
    { "type": "stat_delta", "payload": { "stat": "STAT_WISDOM", "delta": 1 }, "chance": 0.6 },
    { "type": "lp_delta",   "payload": { "amount": 2 },                      "chance": 0.3 }
  ],
  "event_ids": ["def!qy_event.apprentice_arrives", "def!qy_event.apprentice_graduates"]
}
```

---

## 15. Validation Rules

- All `DefRef` values must resolve in the define-it database at boot. Unresolved references are a hard error (game refuses to boot).
- All numeric ranges must satisfy `min ≤ max`.
- All `Requirement` types must have a registered evaluator in `RequirementEvaluator` (one function per type).
- All `Reward` types must have a registered applier in `RewardApplier`.
- `ItemEffect.type` must match a registered effect applier.
- A perk's `requirements` must not transitively require itself.
- A web's nodes must not form cycles that bypass terminal nodes.
- A `LootTable`'s weights must sum to > 0 (zero-weight entries are dropped at load).
- A save file's `save_version` must be ≤ `CURRENT_SAVE_VERSION` on load. Newer saves are rejected with a UI message.

These run as a JSON validator at boot and in CI on every content commit.

---

End of `DATA_MODELS.md`. For systems layout, see `ARCHITECTURE.md`. For asset pipeline, see `ASSET_SPEC.md`.