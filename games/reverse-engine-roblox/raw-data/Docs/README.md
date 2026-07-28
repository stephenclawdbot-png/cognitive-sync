# 📚 Roblox Documentation & Tutorials

This folder contains tutorials, guides, and documentation for Roblox development.

## Contents

### GUI Tutorials
- **[ViewportFrame-Tutorial.md](ViewportFrame-Tutorial.md)** - Complete guide to ViewportFrames
  - Creating 3D displays in 2D UI
  - Custom cameras
  - WorldModel for physics/animations
  - Interactive hover effects
  - Shop display systems

## Sources

Tutorials are extracted from YouTube using `youtube-transcript-api` and then processed into comprehensive documentation.

### How to Extract New Tutorials

```powershell
# Get transcript from any YouTube video
python "I:\Reverse Engine Roblox\Tools\youtube_transcript.py" VIDEO_URL

# Save to file
python "I:\Reverse Engine Roblox\Tools\youtube_transcript.py" VIDEO_URL --output transcript.txt

# Get as JSON for processing
python "I:\Reverse Engine Roblox\Tools\youtube_transcript.py" VIDEO_URL --json
```

## Recommended Channels

- **BrawlDev** - GUI tutorials, scripting fundamentals, advanced topics
- **TheDevKing** - Beginner-friendly tutorials
- **AlvinBlox** - Advanced scripting

---

*Last updated: 2026-02-09*
