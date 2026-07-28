# v1.0.00 (wizdung) Sprite Manifest

Generated via PixelLab API (v3 mode) as placeholder art for the reverse-engineered ARPG dungeon crawler.

## Scale
- Characters: 48px sprite on ~96px canvas, 8-directional
- Enemies: 48-64px, 1-direction
- Items/Equipment: 32px, 1-direction
- NPCs: 48px, 1-direction

## File Structure

```
sprites/
├── characters/
│   ├── dex-wizard/     (8 dirs × 96px)  — Agile lightning wizard
│   ├── int-wizard/     (8 dirs × 92px)  — Frost wisdom wizard
│   └── str-wizard/     (8 dirs × 96px)  — Power battle wizard
├── enemies/
│   ├── skeleton-warrior.png     (48px)  — Basic melee enemy
│   ├── skeleton-archer.png      (48px)  — Ranged enemy
│   ├── elite-skeleton-knight.png(48px)  — Elite melee enemy
│   ├── mimic.png                (48px)  — Treasure chest monster
│   ├── elite-mimic.png          (48px)  — Upgraded mimic
│   └── dungeon-boss.png         (64px)  — Minotaur boss
├── items/
│   ├── health-potion.png  (32px)  — Restores HP
│   ├── mana-potion.png    (32px)  — Restores MP
│   ├── gold-coins.png     (32px)  — Currency
│   └── iron-key.png       (32px)  — Dungeon key
├── equipment/
│   ├── iron-sword.png     (32px)  — Basic weapon
│   └── magic-staff.png    (32px)  — Wizard weapon
├── npcs/
│   ├── mysterious-wizard.png  (48px)  — Identify service NPC
│   └── trinket-witch.png      (48px)  — Enchant/sell NPC
└── SPRITE_MANIFEST.md
```

## Character Directions
Each character has 8 directional sprites: south, east, north, west, south-east, north-east, north-west, south-west

## Usage Notes
- These are placeholder/generated sprites, not extracted from the original game
- Original game PCK is encrypted (flags=2), actual sprites cannot be extracted
- Use these as art references or starting points for your new game build
- All sprites have transparent backgrounds (PNG)

## Still Needed (not generated — out of credits)
- 6 additional classes: Ranger, Paladin, Necromancer, Berserker, Rogue, Battle Mage
- Dungeon tilesets (floor, walls)
- VFX sprites (hit effects, spell effects)
- UI elements (health bar, mana bar, inventory slots)
- Additional equipment (armor pieces, shields, helmets)
- Additional enemies (more varieties, elite variants with visual differences)

## PixelLab Asset IDs (for reference)
### Characters
| Class | ID |
|-------|-----|
| Dex Wizard | e15ec753-9acb-4d29-aee9-07f28c1084d5 |
| Int Wizard | 7e58bf45-dc80-467e-90dd-cacfbde27009 |
| Str Wizard | a284de00-700b-4048-a901-7d4f242f10dd |

### Objects
| Asset | ID |
|-------|-----|
| Skeleton Warrior | 7b706abc-1cee-4e0d-bce6-a5d35e55e408 |
| Skeleton Archer | beaa7381-f9dd-4b54-8ff4-cb6cc1c0cfa6 |
| Elite Skeleton Knight | 14690605-a960-4e8e-bcc7-99300b3085fd |
| Mimic | 9b3cbeb3-5b99-4752-acbe-fa4b736ee064 |
| Elite Mimic | 7f3eda79-d5c8-4000-945d-895629d6dc74 |
| Dungeon Boss | 00ea076b-ac7d-4301-ad74-e628232efab4 |
| Health Potion | e74b4291-ff17-430c-b008-9dd9bcc4688c |
| Mana Potion | 87595970-4a89-47c3-b692-5949fe43f6eb |
| Gold Coins | 199864ca-3277-4778-87ba-2f8ce03adfd7 |
| Iron Key | 1e4b6a8a-8bdb-470d-af1e-fdeb7b727cdd |
| Iron Sword | cdb7bfee-7154-47c6-bed2-b87b5c3b0169 |
| Magic Staff | e04b1345-2375-46b9-97d9-9a537540236a |
| Mysterious Wizard NPC | b4093ad0-f049-458c-a91a-36d632529467 |
| Trinket Witch NPC | 2f3ff577-afca-4b9f-9056-b8b605a507a9 |