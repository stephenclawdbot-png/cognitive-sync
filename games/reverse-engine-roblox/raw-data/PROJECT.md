# 🎮 Roblox Reverse Engineering Project

## Goal
Build tools to analyze viral Roblox games → Document mechanics → Build clones

---

## 🔥 The Full Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: BUILD TOOLS                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Screen Stream → Vision AI → Input Controller → MaxBridge          │
│   (see game)      (analyze)   (play game)        (build in Studio)  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        PHASE 2: RESEARCH                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Play viral games → Analyze everything → Document findings         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        PHASE 3: BUILD CLONES                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Placeholder map → Lua scripts → Admiral adds assets → Done!       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
📁 I:\Reverse Engine Roblox\
├── PROJECT.md           # This file - master plan
├── PROGRESS.md          # What's done, what's next
├── Tools/               # All the tools we build
│   ├── ScreenStream/    # Capture & stream screen
│   ├── VisionAI/        # Analyze screenshots
│   ├── InputController/ # Send keyboard/mouse
│   ├── MaxBridge/       # Roblox Studio plugin
│   └── youtube_transcript.py  # Extract YouTube transcripts
├── Docs/                # Tutorials & documentation
│   ├── ViewportFrame-Tutorial.md    # Complete ViewportFrame guide
│   └── ViewportFrame-Transcript-Raw.txt
├── Ideas/               # Game concepts (40+ ideas)
└── Games/               # Game analysis docs (Phase 2)
```

---

## Project Started
- **Date:** 2025-01-27
- **Team:** Admiral (direction, assets) + Max (code, analysis)
