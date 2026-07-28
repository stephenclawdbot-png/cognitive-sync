# 🛠️ Roblox Reverse Engine Tools

## Overview

These tools allow Max (Clawdbot) to see, control, and build in Roblox.

```
┌──────────────────────────────────────────────────────────────────┐
│                         TOOL STACK                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│   │   Screen    │  │   Input     │  │   Vision    │             │
│   │   Stream    │  │  Controller │  │     AI      │             │
│   │  :8765      │  │   :8766     │  │   :8767     │             │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│          │                │                │                     │
│          └────────────────┼────────────────┘                     │
│                           │                                      │
│                           ▼                                      │
│                    ┌─────────────┐                               │
│                    │     Max     │                               │
│                    │ (Clawdbot)  │                               │
│                    └──────┬──────┘                               │
│                           │                                      │
│                           ▼                                      │
│                    ┌─────────────┐      ┌─────────────┐         │
│                    │  MaxBridge  │ ───► │   Roblox    │         │
│                    │   :8768     │      │   Studio    │         │
│                    └─────────────┘      └─────────────┘         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Quick Start

### First Time Setup
```batch
INSTALL_ALL.bat
```

### Start All Servers
```batch
START_ALL.bat
```

## Tools

| Tool | Port | Description |
|------|------|-------------|
| [Screen Stream](./ScreenStream/) | 8765 | Captures screen/windows |
| [Input Controller](./InputController/) | 8766 | Sends keyboard/mouse |
| [Vision AI](./VisionAI/) | 8767 | OCR & image analysis |
| [MaxBridge](./MaxBridge/) | 8768 | Roblox Studio control |

## How Max Uses Them

1. **See** - Screen Stream captures what's on screen
2. **Understand** - Vision AI reads text and analyzes UI
3. **Control** - Input Controller sends keyboard/mouse
4. **Build** - MaxBridge creates parts/scripts in Studio

## Dependencies

- Python 3.10+
- Tesseract OCR (for Vision AI) - [Download](https://github.com/UB-Mannheim/tesseract/wiki)
- Roblox Studio (for MaxBridge)
