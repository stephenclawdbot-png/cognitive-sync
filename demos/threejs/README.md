# COGNITIVE-SYNC v1.1 Demo Application

## Overview

Real-time EMG-driven thought visualization using the SILENT simulator for synthetic EMG→thought data. Multiple virtual users generate thoughts in 3D space based on simulated EMG states (rest, thinking, word_detected).

![Demo Video Placeholder](docs/demo-v1.1-preview.png)

**[📺 Watch Demo Video](docs/demo-v1.1.mp4)** *(coming soon)*

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
cd demo_app
docker-compose up
```

Open browser: http://localhost:8000

### Option 2: Local Python

```bash
# Install dependencies
pip install -r demo_app/requirements.txt

# Start server
python demo_app/server.py
```

Open browser: http://localhost:8000

## 📁 Project Structure

```
demo_app/
├── server.py              # FastAPI backend with WebSocket
├── thought_simulator.py   # EMG→thought mapping using SILENT_SIMULATOR
├── visualizer.py          # 3D graph layout engine
├── web_ui/
│   └── index.html        # Three.js frontend
├── docker-compose.yml     # One-command startup
├── Dockerfile            # Container definition
└── requirements.txt      # Python dependencies
```

## ✨ Features

### v1.1 Features:

- **🔮 3D Spatial Visualization**
  - Three.js-powered real-time 3D rendering
  - Thought nodes with glow/pulse effects based on EMG state
  - Proximity-based connection lines
  - Interactive camera controls (drag to rotate, scroll to zoom)

- **⚡ Real-Time WebSocket Streaming**
  - ~50ms latency for thought updates
  - Bidirectional WebSocket communication
  - Automatic reconnection with backoff

- **👥 Multiple Virtual Users**
  - 3 distinct personas: Alice (analytical), Bob (creative), Charlie (technical)
  - Each user has unique:
    - Color coding (cyan, pink, light blue)
    - Vocabulary based on thought style
    - Movement patterns in 3D space
    - EMG timing characteristics

- **💾 Thought Persistence & Replay**
  - Session recording and export
  - JSON-based replay format
  - Adjustable replay speed

### EMG State→Visual Mapping

| EMG State | Visual Style |
|-----------|--------------|
| `rest` | Dim, slow pulse, cool cyan |
| `thinking` | Medium glow, faster pulse, warm yellow |
| `word_detected` | Bright glow, rapid spin, bright pink |

## 🎮 Controls

- **Mouse Drag**: Rotate camera
- **Scroll**: Zoom in/out
- **Reset View**: Click the Reset button
- **Pause/Resume**: Toggle simulation

## 🔌 API Endpoints

### REST API

| Endpoint | Description |
|----------|-------------|
| `GET /api/status` | Server and simulation status |
| `GET /api/users` | Virtual user positions and states |
| `GET /api/thoughts` | Recent thoughts with filtering |
| `POST /api/simulation/start` | Start simulation (default: 3 users) |
| `POST /api/simulation/stop` | Stop simulation |
| `POST /api/simulation/export` | Export session to file |
| `POST /api/replay/load` | Load session for replay |
| `POST /api/replay/start` | Start replay |

### WebSocket

Connect to: `ws://localhost:8000/ws`

Incoming events:
- `thought_created` - New thought generated
- `state_changed` - User EMG state transition
- `user_moved` - User position update

## 📊 Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  SILENT_SIMULATOR│────→│ thought_simulator│────→│   FastAPI       │
│  (EMG states)   │     │ (EMG→thought map)│     │   (WebSocket)   │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                  ┌──────────────────────┘
                                  │
                         ┌────────▼────────┐
                         │  Three.js WebUI │
                         │  (3D Rendering) │
                         └─────────────────┘
```

## 🧠 Thought Model

```json
{
  "thought_id": "thought_1234567890_user1_1234",
  "user_id": "user_0_5678",
  "text": "analyze",
  "emg_state": "word_detected",
  "confidence": 0.89,
  "position": [5.2, -3.1, 1.0],
  "timestamp": 1711512345.678,
  "color": "#64ffd8",
  "metadata": {
    "user_name": "Alice",
    "thought_style": "analytical",
    "glow_intensity": 1.0,
    "size_multiplier": 1.3
  }
}
```

## 🐳 Docker Commands

```bash
# Build and start
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Export volume data
docker-compose down -v
```

## 📝 Session Export Format

```json
{
  "export_time": 1711512345.678,
  "stats": {
    "thoughts_generated": 156,
    "words_detected": 89,
    "start_time": 1711512000.000
  },
  "users": {
    "user_0_5678": {
      "name": "Alice",
      "style": "analytical",
      "color": "#64ffd8"
    }
  },
  "thoughts": [...]
}
```

## 🛣️ Roadmap

### v1.2 Planned:
- [ ] Real EMG hardware integration (SILENT-001)
- [ ] VR/AR visualization
- [ ] Thought persistence with database
- [ ] Multi-room support

## 📚 Dependencies

- **Backend**: FastAPI, Uvicorn, WebSockets, NumPy
- **Frontend**: Three.js (CDN)
- **Container**: Docker, Docker Compose

## 🤝 Integration

This demo integrates with:
- **SILENT-001/firmware/SILENT_SIMULATOR.py** - EMG simulation
- **COGNITIVE-SYNC/thought_node.py** - Core thought data model
- **COGNITIVE-SYNC/websocket_bridge.py** - Real-time sync layer

## 📄 License

Part of the COGNITIVE-SYNC project. See main repository for license details.

---

**Version**: 1.1.0  
**Last Updated**: 2026-03-28  
**Status**: ✅ Working Demo
