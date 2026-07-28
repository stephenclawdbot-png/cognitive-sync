# 👁️ Vision AI

## Purpose
Analyze screenshots to extract game information automatically.

## Requirements
- Read text from UI (OCR)
- Identify UI elements (buttons, menus, health bars)
- Detect game state (in menu, playing, dead, etc.)
- Extract numbers (currency, health, damage)
- Recognize patterns (inventory grids, pet cards)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       VISION AI                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Screenshot                                                │
│        │                                                    │
│        ▼                                                    │
│   ┌─────────────┐      ┌─────────────┐      ┌───────────┐  │
│   │    OCR      │      │   Object    │      │   Game    │  │
│   │  (text)     │      │  Detection  │      │   State   │  │
│   └─────────────┘      └─────────────┘      └───────────┘  │
│        │                     │                    │         │
│        └─────────────────────┴────────────────────┘         │
│                              │                              │
│                              ▼                              │
│                     ┌───────────────┐                       │
│                     │   Analysis    │                       │
│                     │   Results     │                       │
│                     └───────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack
- **Python 3**
- **pytesseract** or **easyocr** — Text extraction
- **OpenCV** — Image processing
- **Claude Vision** — Advanced analysis (via Clawdbot)

## Capabilities
1. **OCR** — Read all text on screen
2. **Region extraction** — Crop specific UI areas
3. **Template matching** — Find known UI elements
4. **Color detection** — Health bars, rarity indicators
5. **AI analysis** — Send to Claude for complex understanding

## Status
🔴 Not started — Depends on Screen Stream
