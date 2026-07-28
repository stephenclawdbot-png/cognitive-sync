# 🎮 Input Controller

## Purpose
Send keyboard and mouse inputs to control Roblox Player remotely.

## Requirements
- Keyboard input (WASD, space, E for interact, numbers)
- Mouse movement and clicks
- Hold keys (for walking)
- Click at specific screen coordinates
- Work even when Roblox is not focused (optional)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT CONTROLLER                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Max (commands)                                            │
│        │                                                    │
│        ▼                                                    │
│   ┌─────────────┐      ┌─────────────┐      ┌───────────┐  │
│   │   HTTP      │ ───► │   Input     │ ───► │  Roblox   │  │
│   │   Server    │      │   Sender    │      │  Player   │  │
│   └─────────────┘      └─────────────┘      └───────────┘  │
│                                                             │
│   Endpoints:                                                │
│   - POST /key          → Press/release key                 │
│   - POST /type         → Type string                       │
│   - POST /mouse/move   → Move mouse to x,y                 │
│   - POST /mouse/click  → Click at position                 │
│   - POST /macro        → Run predefined sequence           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack
- **Python 3**
- **pynput** or **pyautogui** — Input simulation
- **Flask** or **FastAPI** — HTTP server
- **win32api** — Low-level Windows input (optional)

## Commands
```json
// Press key
{"action": "press", "key": "w", "duration": 0.5}

// Click at position
{"action": "click", "x": 500, "y": 300, "button": "left"}

// Move mouse
{"action": "move", "x": 500, "y": 300}

// Type text
{"action": "type", "text": "hello"}
```

## Status
🔴 Not started — Build after Screen Stream + Vision AI
