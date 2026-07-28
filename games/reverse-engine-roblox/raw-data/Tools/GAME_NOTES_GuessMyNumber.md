# Guess My Number - Reverse Engineering Notes

## Game Overview
- **Name**: Guess My Number
- **Platform**: Roblox
- **Genre**: 1v1 number guessing game
- **Player account**: admiralthefinest

---

## CURRENCIES
| Currency | Icon | Purchasable |
|----------|------|-------------|
| Cash ($) | Green bills | Yes (blue [+] button) |
| Premium (trophies) | Trophy/crown | Yes (blue [+] button) |
| Robux | Robux icon | Real money |

- Starting cash observed: $67 (on join), went to $367 after rewards, then $467 after 1st win
- Win reward: $100 per win

---

## CORE GAMEPLAY LOOP

### 1. Lobby Phase
- Open green field with multiple **tables** (2 chairs each)
- Players walk around freely using WASD
- Walk up to a table and press **Play** (or sit) to queue
- Tables show: "0/2 Players - Win $100"
- Countdown "Starting in 3...2...1" when 2 players sit

### 2. Choosing Phase
- Text: **"Choosing"** with thinking emoji
- Then: **"Choose A Number"** with a scrollable grid of yellow tiles
- Number range displayed above: **"1-100"** (with devil emoji)
- Grid shows numbers in rows of 5 (e.g., 11-15, 16-20, 21-25...)
- Player picks a secret number (observed picks: 33, 40)
- Both players show **"Ready"** with green checkmark when done

### 3. Guessing Phase
- Text: **"Guessing"** with eyes emoji
- Players take turns guessing opponent's number
- Prompt: **"Is your number X?"** (with thinking emoji)
- After each guess, feedback appears (automated by the game):
  - **"Higher"** (with pointing up emoji) - target number is higher
  - **"Lower"** (with pointing down emoji) - target number is lower
- On the number grid: eliminated numbers get **red X marks**
  - Numbers already guessed wrong turn gray with red X overlay
  - Remaining valid numbers stay yellow
- Papers on table show: **"?"** (opponent's hidden number) and **your number** visible to you

### 4. Win/Loss
- When guessed correctly: round ends
- Winner gets **$100 cash**
- After loss: **"David's number was 73!"** (reveals opponent's number)
- Streak system: **"You lost your 1 streak!"**
- **"RECOVER NOW"** button appears (likely Robux purchase to save streak)

---

## UI LAYOUT

### Top Bar (HUD)
- **Left**: Cash display ($XXX) + [+] buy button
- **Center-left**: Trophy currency (0) + [+] buy button
- **Right**: Daily Quests timer (14:XX:XX countdown)

### Left Side Buttons
- **SHOP** (basket icon) - pink/red
- **ITEMS** (brick icon) - orange
- **REWARDS** (gift icon) - purple

### Right Side
- **Leaderboard** panel (People | Streak | Wins columns)
- **Daily Quests**: "Play 5 Times (X/5)", "Win 3 Times (X/3)"
- Quest rewards: $300, $400 with CLAIM buttons
- **STARTER PACK** promo
- Rotating promos: 2X WINS (99 Robux), 2X CASH (99 Robux), 2X STREAK (99 Robux)

### Right Side (During Game)
- **REVEAL NUMBER** button (39 Robux) - reveals opponent's number (cheat)
- **HINT** button (19 Robux) - gives a hint about opponent's number

---

## SHOP (Robux Purchases)
| Item | Price |
|------|-------|
| VIP ([VIP] Chat + VIP Cosmetics) | 179 Robux |
| Double Streak | 79 Robux |
| Double Cash | 99 Robux |
| Double Wins | 199 Robux |
| 300 Cash | 29 Robux |
| 1,000 Cash | 89 Robux |
| 2,500 Cash | 199 Robux |

---

## REWARDS SYSTEM

### Playtime Rewards
- Tracked by time played (00:00:40 observed)
- Tiers: 5min, 10min, 15min, 20min
- Rewards: $250-$300 + multiplier boosts + items

### Daily Rewards (! notification badge)
### Group Rewards
### Social Rewards
### VIP Daily Rewards
### Robux Spent Rewards

---

## ITEMS / COSMETICS
- **COSMETICS** panel with avatar preview
- Categories: **Chairs**, **Deaths** (death effects)
- Default skin equipped
- Items likely purchased with cash or Robux

---

## LEADERBOARD (Sample)
| Player | Streak | Wins |
|--------|--------|------|
| Kai | 6 | 9 |
| chakor345 | 5 | 5 |
| YVLclyde | 4 | 4 |
| David | 2 | 2 |
| admiralthefinest | 1 | 1 |

---

## KEY OBSERVATIONS FOR AUTOMATION

### Binary Search Strategy
- Range is 1-100
- Optimal strategy: binary search = ~10 guesses max
- Feedback is "Higher" or "Lower" - perfect for binary search
- Grid eliminates numbers visually (red X) but the text feedback is the key signal

### Automation Flow
1. **Walk to table** → detect "0/2 Players" text, walk to table, sit
2. **Choose number** → pick a number (e.g., always 500 for middle)
3. **Wait for turn** → detect "Choose A Number" or "Is your number X?"
4. **Guess using binary search** → read "Higher"/"Lower" feedback, narrow range
5. **Repeat** → walk to next table after round ends

### Key Text to OCR
- "Choose A Number" - number selection phase
- "Is your number X?" - opponent guessing (wait)
- "Higher" / "Lower" - feedback after your guess
- "Guessing" - opponent's turn
- "Starting in X" - countdown
- "Ready" - both players ready
- "$XXX" - cash amount
- "Win $100" - table prize
- "You lost your X streak!" - loss detection
- "RECOVER NOW" - streak recovery prompt

### Robux Pay-to-Win Elements
- REVEAL NUMBER (39 Robux) - instantly see opponent's number
- HINT (19 Robux) - narrows down the range
- Double Cash/Wins/Streak multipliers
- VIP bundle (179 Robux)

---

## SESSION STATS
- Games played: ~3
- Wins: 1
- Losses: 1 (to David, his number was 73)
- Final cash: $467
- Final trophies: 1
- Daily quest progress: Play 3/5, Win 1/3
