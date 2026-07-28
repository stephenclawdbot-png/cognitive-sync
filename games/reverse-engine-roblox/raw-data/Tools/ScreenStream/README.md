# 📺 Screen Stream

## Status: ✅ COMPLETE & WORKING

## Purpose
Capture the Windows screen and make it available for Max to view and analyze.

## Quick Start
```batch
# First time:
install.bat

# Run server:
run.bat
```

Server runs on **http://localhost:8765**

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Server status & info |
| `GET /screenshot` | Full screen capture (JPEG) |
| `GET /screenshot?monitor=1` | Specific monitor |
| `GET /region?x=0&y=0&w=500&h=500` | Capture region |
| `GET /windows` | List all open windows |
| `GET /window/{title}` | Capture window by title |
| `GET /roblox` | Shortcut for Roblox window |
| `GET /monitors` | List all monitors |

## How Max Uses It

```python
# Take screenshot, save to file
Invoke-WebRequest -Uri "http://localhost:8765/screenshot" -OutFile "capture.jpg"

# List windows
Invoke-RestMethod -Uri "http://localhost:8765/windows"

# Capture Roblox specifically
Invoke-WebRequest -Uri "http://localhost:8765/roblox" -OutFile "roblox.jpg"
```

## Files
- `server.py` — FastAPI server
- `capture.py` — Screen capture logic
- `requirements.txt` — Python dependencies
- `run.bat` — Start server
- `install.bat` — First-time setup

## Dependencies
- Python 3.10+
- mss (screenshots)
- Pillow (image processing)
- FastAPI + uvicorn (HTTP server)
- pywin32 (Windows API)
