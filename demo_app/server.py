"""
COGNITIVE-SYNC v1.1: FastAPI Backend Server

Provides:
- WebSocket endpoint for real-time thought streaming
- REST API for thought history, replay, and user management
- Integration with ThoughtSimulator for EMG-based thought generation
- Session persistence and export
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Optional, Any, Set
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import thought simulator
from thought_simulator import ThoughtSimulator, SimulatedThought

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("cognitive_server")

# FastAPI app
app = FastAPI(
    title="COGNITIVE-SYNC v1.1",
    description="Real-time EMG-driven thought visualization API",
    version="1.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
class ServerState:
    def __init__(self):
        self.simulator: Optional[ThoughtSimulator] = None
        self.active_connections: Set[WebSocket] = set()
        self.session_start_time: Optional[float] = None
        self.simulation_task: Optional[asyncio.Task] = None
        self.replay_mode: bool = False
        self.replay_data: List[Dict] = []
        self.replay_index: int = 0

state = ServerState()


# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"Client disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients."""
        if not self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.active_connections.discard(conn)
    
    async def send_to(self, websocket: WebSocket, message: Dict[str, Any]):
        """Send message to specific client."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.warning(f"Failed to send to client: {e}")


manager = ConnectionManager()


# Thought event handlers
def on_thought_created(thought: SimulatedThought):
    """Called when a new thought is generated."""
    message = {
        "type": "thought_created",
        "timestamp": time.time(),
        "data": {
            "thought_id": thought.thought_id,
            "user_id": thought.user_id,
            "text": thought.text,
            "emg_state": thought.emg_state,
            "confidence": thought.confidence,
            "position": thought.position,
            "color": thought.color,
            "metadata": thought.metadata
        }
    }
    # Async broadcast
    asyncio.create_task(manager.broadcast(message))


def on_state_changed(user_id: str, new_state: str, props: Dict):
    """Called when user's EMG state changes."""
    message = {
        "type": "state_changed",
        "timestamp": time.time(),
        "data": {
            "user_id": user_id,
            "state": new_state,
            "properties": props
        }
    }
    asyncio.create_task(manager.broadcast(message))


def on_user_moved(user_id: str, position: tuple):
    """Called when user moves in 3D space."""
    message = {
        "type": "user_moved",
        "timestamp": time.time(),
        "data": {
            "user_id": user_id,
            "position": position
        }
    }
    asyncio.create_task(manager.broadcast(message))


# API Endpoints
@app.get("/")
async def root():
    """Serve the main visualization UI."""
    return FileResponse("demo_app/web_ui/index.html")


@app.get("/api/status")
async def get_status():
    """Get server and simulation status."""
    return {
        "status": "running",
        "version": "1.1.0",
        "simulation_active": state.simulator is not None and state.simulator.running,
        "connected_clients": len(manager.active_connections),
        "session_duration": time.time() - state.session_start_time if state.session_start_time else 0,
        "replay_mode": state.replay_mode
    }


@app.get("/api/users")
async def get_users():
    """Get list of virtual users and their positions."""
    if state.simulator is None:
        return {"users": []}
    return {"users": state.simulator.get_user_positions()}


@app.get("/api/thoughts")
async def get_thoughts(
    limit: int = 100,
    since: Optional[float] = None,
    user_id: Optional[str] = None
):
    """Get recent thoughts with optional filtering."""
    if state.simulator is None:
        return {"thoughts": []}
    
    thoughts = state.simulator.get_replay_data(start_time=since)
    
    if user_id:
        thoughts = [t for t in thoughts if t["user_id"] == user_id]
    
    thoughts = thoughts[-limit:]  # Most recent
    
    return {"thoughts": thoughts, "count": len(thoughts)}


@app.get("/api/thoughts/near")
async def get_thoughts_near(
    x: float,
    y: float,
    z: float,
    radius: float = 5.0
):
    """Get thoughts near a specific position."""
    if state.simulator is None:
        return {"thoughts": []}
    
    thoughts = state.simulator.get_thoughts_in_range((x, y, z), radius)
    return {
        "thoughts": [
            {
                "thought_id": t.thought_id,
                "user_id": t.user_id,
                "text": t.text,
                "position": t.position,
                "timestamp": t.timestamp,
                "color": t.color
            }
            for t in thoughts
        ],
        "center": (x, y, z),
        "radius": radius
    }


@app.post("/api/simulation/start")
async def start_simulation(num_users: int = 3):
    """Start the EMG thought simulation."""
    if state.simulator is not None and state.simulator.running:
        raise HTTPException(status_code=400, detail="Simulation already running")
    
    state.simulator = ThoughtSimulator(num_users=num_users)
    state.simulator.on_thought_created = on_thought_created
    state.simulator.on_state_changed = on_state_changed
    state.simulator.on_user_moved = on_user_moved
    
    state.session_start_time = time.time()
    state.replay_mode = False
    
    # Start simulation in background
    state.simulation_task = asyncio.create_task(state.simulator.start())
    
    logger.info(f"Started simulation with {num_users} users")
    return {"status": "started", "num_users": num_users}


@app.post("/api/simulation/stop")
async def stop_simulation():
    """Stop the EMG thought simulation."""
    if state.simulator is None or not state.simulator.running:
        raise HTTPException(status_code=400, detail="No simulation running")
    
    await state.simulator.stop()
    
    if state.simulation_task:
        state.simulation_task.cancel()
        try:
            await state.simulation_task
        except asyncio.CancelledError:
            pass
    
    logger.info("Simulation stopped")
    return {"status": "stopped"}


@app.post("/api/simulation/export")
async def export_simulation(filepath: str = "session_export.json"):
    """Export current simulation session to file."""
    if state.simulator is None:
        raise HTTPException(status_code=400, detail="No simulation data available")
    
    state.simulator.export_session(filepath)
    return {"status": "exported", "filepath": filepath}


@app.post("/api/replay/load")
async def load_replay(filepath: str = "session_export.json"):
    """Load a session for replay."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        state.replay_data = data.get("thoughts", [])
        state.replay_index = 0
        state.replay_mode = True
        
        return {
            "status": "loaded",
            "thought_count": len(state.replay_data),
            "session_stats": data.get("stats", {})
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {filepath}")


@app.post("/api/replay/start")
async def start_replay(speed: float = 1.0):
    """Start replaying loaded session."""
    if not state.replay_data:
        raise HTTPException(status_code=400, detail="No replay data loaded")
    
    if state.replay_mode:
        raise HTTPException(status_code=400, detail="Replay already in progress")
    
    state.replay_mode = True
    asyncio.create_task(_replay_loop(speed))
    
    return {"status": "replay_started", "speed": speed}


async def _replay_loop(speed: float):
    """Background task for replay."""
    if not state.replay_data:
        return
    
    start_time = state.replay_data[0]["timestamp"]
    
    while state.replay_mode and state.replay_index < len(state.replay_data):
        thought_data = state.replay_data[state.replay_index]
        
        message = {
            "type": "thought_created",
            "timestamp": time.time(),
            "data": thought_data
        }
        
        await manager.broadcast(message)
        
        # Calculate time to next thought
        if state.replay_index + 1 < len(state.replay_data):
            next_time = state.replay_data[state.replay_index + 1]["timestamp"]
            delay = (next_time - thought_data["timestamp"]) / speed
            await asyncio.sleep(max(0.01, delay))
        
        state.replay_index += 1
    
    state.replay_mode = False
    logger.info("Replay completed")


@app.post("/api/replay/stop")
async def stop_replay():
    """Stop replay."""
    state.replay_mode = False
    return {"status": "stopped"}


@app.get("/api/replay/progress")
async def get_replay_progress():
    """Get current replay progress."""
    if not state.replay_data:
        return {"progress": 0, "total": 0, "percentage": 0}
    
    return {
        "progress": state.replay_index,
        "total": len(state.replay_data),
        "percentage": (state.replay_index / len(state.replay_data)) * 100
    }


# WebSocket endpoint for real-time streaming
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time thought streaming."""
    await manager.connect(websocket)
    
    try:
        # Send initial state
        if state.simulator:
            await websocket.send_json({
                "type": "connection_established",
                "data": {
                    "users": state.simulator.get_user_positions(),
                    "session_start": state.session_start_time
                }
            })
        else:
            await websocket.send_json({
                "type": "connection_established",
                "data": {"message": "Simulation not started"}
            })
        
        # Keep connection alive and handle client commands
        while True:
            try:
                data = await websocket.receive_json()
                cmd = data.get("command")
                
                if cmd == "get_users":
                    if state.simulator:
                        await websocket.send_json({
                            "type": "users_update",
                            "data": state.simulator.get_user_positions()
                        })
                
                elif cmd == "get_thoughts":
                    since = data.get("since")
                    if state.simulator:
                        thoughts = state.simulator.get_replay_data(start_time=since)
                        await websocket.send_json({
                            "type": "thoughts_batch",
                            "data": thoughts[-100:]  # Last 100
                        })
                
                elif cmd == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": time.time()
                    })
                    
            except Exception as e:
                logger.warning(f"WebSocket message error: {e}")
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)


# Serve static files for visualization
app.mount("/static", StaticFiles(directory="demo_app/web_ui"), name="static")


# Startup and shutdown
@app.on_event("startup")
async def startup_event():
    """Auto-start simulation on startup."""
    logger.info("COGNITIVE-SYNC v1.1 Server starting...")
    
    # Start simulation automatically
    state.simulator = ThoughtSimulator(num_users=3)
    state.simulator.on_thought_created = on_thought_created
    state.simulator.on_state_changed = on_state_changed
    state.simulator.on_user_moved = on_user_moved
    
    state.session_start_time = time.time()
    state.simulation_task = asyncio.create_task(state.simulator.start())
    
    logger.info("Auto-started simulation with 3 virtual users")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    logger.info("Server shutting down...")
    
    if state.simulator and state.simulator.running:
        await state.simulator.stop()
    
    if state.simulation_task:
        state.simulation_task.cancel()


# Main entry point
if __name__ == "__main__":
    print("=" * 60)
    print("COGNITIVE-SYNC v1.1 Demo Server")
    print("=" * 60)
    print()
    print("Starting server...")
    print("  API: http://localhost:8000")
    print("  WebSocket: ws://localhost:8000/ws")
    print("  Visualization: http://localhost:8000")
    print()
    print("Press Ctrl+C to stop")
    print("-" * 60)
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
