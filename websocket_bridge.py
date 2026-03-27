"""
COGNITIVE-SYNC: WebSocket Bridge for Real-time Synchronization

Handles WebSocket connections, broadcasts updates to all clients,
and manages the sync protocol for collaborative thought spaces.
"""

import asyncio
import websockets
import json
import logging
from typing import Set, Dict, Any, Optional, Callable
from dataclasses import asdict
from pathlib import Path

from thought_node import ThoughtNode, ThoughtSpace


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("cognitive_bridge")


class Client:
    """Represents a connected WebSocket client."""
    
    def __init__(self, websocket: websockets.WebSocketServerProtocol, client_id: str):
        self.websocket = websocket
        self.id = client_id
        self.connected_at = asyncio.get_event_loop().time()
        self.last_sync: float = 0
        self.active_thoughts: Set[str] = set()  # Thoughts client is "near"
    
    async def send(self, message: Dict[str, Any]) -> bool:
        """Send a message to this client."""
        try:
            await self.websocket.send(json.dumps(message))
            return True
        except Exception as e:
            logger.warning(f"Failed to send to client {self.id}: {e}")
            return False
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Client) and self.id == other.id


class WebSocketBridge:
    """
    WebSocket bridge for real-time thought space synchronization.
    
    Protocol:
    - Client connects: receives full state sync
    - Client sends: {type: "create|update|delete|move", data: {...}}
    - Server broadcasts: {type: "sync", data: {...}, timestamp: ...}
    - Heartbeat: {type: "ping"} -> {type: "pong"}
    """
    
    def __init__(self, thought_space: Optional[ThoughtSpace] = None):
        self.space = thought_space or ThoughtSpace()
        self.clients: Set[Client] = set()
        self.clients_lock = asyncio.Lock()
        self.message_handlers: Dict[str, Callable] = {}
        self._register_handlers()
        self._shutdown_event = asyncio.Event()
    
    def _register_handlers(self) -> None:
        """Register message type handlers."""
        self.message_handlers = {
            "create": self._handle_create,
            "update": self._handle_update,
            "delete": self._handle_delete,
            "move": self._handle_move,
            "sync_request": self._handle_sync_request,
            "ping": self._handle_ping,
            "cursor_update": self._handle_cursor_update,
        }
    
    async def register_client(self, websocket: websockets.WebSocketServerProtocol) -> Client:
        """Register a new client connection."""
        client_id = f"client_{id(websocket):x}"
        client = Client(websocket, client_id)
        
        async with self.clients_lock:
            self.clients.add(client)
        
        logger.info(f"Client {client_id} connected. Total: {len(self.clients)}")
        
        # Send full state sync
        await self._send_full_sync(client)
        
        # Broadcast join notification
        await self._broadcast({
            "type": "presence",
            "event": "join",
            "client_id": client_id,
            "client_count": len(self.clients)
        }, exclude=client)
        
        return client
    
    async def unregister_client(self, client: Client) -> None:
        """Remove a client connection."""
        async with self.clients_lock:
            self.clients.discard(client)
        
        logger.info(f"Client {client.id} disconnected. Total: {len(self.clients)}")
        
        # Broadcast leave notification
        await self._broadcast({
            "type": "presence",
            "event": "leave",
            "client_id": client.id,
            "client_count": len(self.clients)
        })
    
    async def handle_connection(self, websocket: websockets.WebSocketServerProtocol, path: str = "/") -> None:
        """Handle a single WebSocket connection."""
        client = await self.register_client(websocket)
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._process_message(client, data)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from {client.id}")
                    await client.send({"type": "error", "message": "Invalid JSON"})
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await client.send({"type": "error", "message": str(e)})
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed: {client.id}")
        finally:
            await self.unregister_client(client)
    
    async def _process_message(self, client: Client, data: Dict[str, Any]) -> None:
        """Route message to appropriate handler."""
        msg_type = data.get("type")
        handler = self.message_handlers.get(msg_type)
        
        if handler:
            await handler(client, data)
        else:
            logger.warning(f"Unknown message type: {msg_type}")
            await client.send({"type": "error", "message": f"Unknown type: {msg_type}"})
    
    # --- Message Handlers ---
    
    async def _handle_create(self, client: Client, data: Dict[str, Any]) -> None:
        """Handle create thought message."""
        thought_data = data.get("data", {})
        thought_data["author"] = client.id  # Enforce author
        
        try:
            thought = ThoughtNode.from_dict(thought_data)
            thought.increment_clock()
            self.space.add(thought)
            
            logger.info(f"Thought created by {client.id}: {thought.id[:8]}...")
            
            # Broadcast to all clients
            await self._broadcast({
                "type": "thought_created",
                "data": thought.to_dict(),
                "by": client.id
            })
        except Exception as e:
            await client.send({"type": "error", "message": f"Create failed: {e}"})
    
    async def _handle_update(self, client: Client, data: Dict[str, Any]) -> None:
        """Handle update thought message."""
        thought_data = data.get("data", {})
        thought_id = thought_data.get("id")
        
        if not thought_id or thought_id not in self.space.thoughts:
            await client.send({"type": "error", "message": "Thought not found"})
            return
        
        try:
            updated = ThoughtNode.from_dict(thought_data)
            updated.increment_clock()
            self.space.add(updated)  # Merge into space
            
            logger.debug(f"Thought updated by {client.id}: {thought_id[:8]}...")
            
            await self._broadcast({
                "type": "thought_updated",
                "data": updated.to_dict(),
                "by": client.id
            })
        except Exception as e:
            await client.send({"type": "error", "message": f"Update failed: {e}"})
    
    async def _handle_delete(self, client: Client, data: Dict[str, Any]) -> None:
        """Handle delete thought message."""
        thought_id = data.get("thought_id")
        
        if thought_id and thought_id in self.space.thoughts:
            self.space.remove(thought_id)
            logger.info(f"Thought deleted by {client.id}: {thought_id[:8]}...")
            
            await self._broadcast({
                "type": "thought_deleted",
                "thought_id": thought_id,
                "by": client.id
            })
    
    async def _handle_move(self, client: Client, data: Dict[str, Any]) -> None:
        """Handle move thought to new position."""
        thought_id = data.get("thought_id")
        new_pos = data.get("position")
        
        if not thought_id or not new_pos:
            await client.send({"type": "error", "message": "Missing thought_id or position"})
            return
        
        thought = self.space.get(thought_id)
        if thought:
            thought.position = tuple(new_pos)
            thought.increment_clock()
            self.space.add(thought)
            
            await self._broadcast({
                "type": "thought_moved",
                "thought_id": thought_id,
                "position": new_pos,
                "by": client.id
            })
    
    async def _handle_sync_request(self, client: Client, data: Dict[str, Any]) -> None:
        """Handle explicit sync request."""
        await self._send_full_sync(client)
    
    async def _handle_ping(self, client: Client, data: Dict[str, Any]) -> None:
        """Handle keepalive ping."""
        await client.send({"type": "pong", "timestamp": asyncio.get_event_loop().time()})
    
    async def _handle_cursor_update(self, client: Client, data: Dict[str, Any]) -> None:
        """Handle cursor position update from a client."""
        position = data.get("position")
        if position:
            # Broadcast cursor position to other clients
            await self._broadcast({
                "type": "cursor_update",
                "client_id": client.id,
                "position": position
            }, exclude=client)
    
    # --- Broadcasting ---
    
    async def _send_full_sync(self, client: Client) -> None:
        """Send full state to a client."""
        thoughts = self.space.to_dict()
        await client.send({
            "type": "full_sync",
            "data": thoughts,
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def _broadcast(self, message: Dict[str, Any], exclude: Optional[Client] = None) -> None:
        """Broadcast message to all clients."""
        dead_clients = set()
        
        async with self.clients_lock:
            clients_snapshot = list(self.clients)
        
        for client in clients_snapshot:
            if client == exclude:
                continue
            if not await client.send(message):
                dead_clients.add(client)
        
        # Clean up dead clients
        if dead_clients:
            async with self.clients_lock:
                for client in dead_clients:
                    self.clients.discard(client)
    
    # --- Server Lifecycle ---
    
    async def start(self, host: str = "0.0.0.0", port: int = 8765) -> None:
        """Start the WebSocket server."""
        logger.info(f"Starting WebSocket server on ws://{host}:{port}")
        
        async with websockets.serve(
            self.handle_connection,
            host,
            port,
            ping_interval=20,
            ping_timeout=60
        ) as server:
            await self._shutdown_event.wait()
    
    def shutdown(self) -> None:
        """Signal server shutdown."""
        self._shutdown_event.set()


class ThoughtSpaceClient:
    """
    Client-side WebSocket handler for connecting to a thought space.
    """
    
    def __init__(self, server_url: str = "ws://localhost:8765"):
        self.server_url = server_url
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.local_space = ThoughtSpace()
        self.connected = False
        self._message_callbacks: Dict[str, list] = {}
    
    async def connect(self) -> None:
        """Connect to the WebSocket server."""
        self.websocket = await websockets.connect(self.server_url)
        self.connected = True
        
        # Start receive loop
        asyncio.create_task(self._receive_loop())
    
    async def _receive_loop(self) -> None:
        """Receive and process server messages."""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self._handle_server_message(data)
        except websockets.exceptions.ConnectionClosed:
            self.connected = False
            logger.info("Disconnected from server")
    
    async def _handle_server_message(self, data: Dict[str, Any]) -> None:
        """Process incoming server message."""
        msg_type = data.get("type")
        
        if msg_type == "full_sync":
            # Merge full state
            self.local_space.merge(data.get("data", {}))
            logger.info(f"Synced {len(self.local_space.thoughts)} thoughts")
        
        elif msg_type == "thought_created":
            thought = ThoughtNode.from_dict(data["data"])
            self.local_space.add(thought)
        
        elif msg_type == "thought_updated":
            thought = ThoughtNode.from_dict(data["data"])
            self.local_space.add(thought)
        
        elif msg_type == "thought_deleted":
            self.local_space.remove(data.get("thought_id"))
        
        elif msg_type == "thought_moved":
            thought = self.local_space.get(data.get("thought_id"))
            if thought:
                thought.position = tuple(data.get("position"))
        
        elif msg_type == "presence":
            event = data.get("event")
            count = data.get("client_count")
            logger.info(f"Client {event}ed. {count} total.")
        
        # Trigger callbacks
        for callback in self._message_callbacks.get(msg_type, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def on(self, msg_type: str, callback: Callable) -> None:
        """Register a callback for message type."""
        if msg_type not in self._message_callbacks:
            self._message_callbacks[msg_type] = []
        self._message_callbacks[msg_type].append(callback)
    
    async def send(self, message: Dict[str, Any]) -> None:
        """Send message to server."""
        if self.websocket and self.connected:
            await self.websocket.send(json.dumps(message))
    
    async def create_thought(self, text: str, position: tuple, 
                             author: Optional[str] = None) -> None:
        """Create a new thought."""
        thought = ThoughtNode(
            text=text,
            author=author or "anonymous",
            position=position
        )
        thought.increment_clock()
        await self.send({
            "type": "create",
            "data": thought.to_dict()
        })
    
    async def disconnect(self) -> None:
        """Close connection."""
        if self.websocket:
            await self.websocket.close()
            self.connected = False


if __name__ == "__main__":
    # Demo: Start server
    print("=" * 60)
    print("COGNITIVE-SYNC: WebSocket Bridge Demo")
    print("=" * 60)
    
    bridge = WebSocketBridge()
    
    # Add some sample thoughts
    sample = ThoughtNode("Welcome to Cognitive Sync!", "system", (0, 0, 0))
    sample.increment_clock()
    bridge.space.add(sample)
    
    sample2 = ThoughtNode("Double-click to create new thoughts", "system", (2, 1, 0))
    sample2.increment_clock()
    bridge.space.add(sample2)
    
    sample3 = ThoughtNode("Thoughts sync in real-time across all clients", "system", (-2, 0.5, 0))
    sample3.increment_clock()
    bridge.space.add(sample3)
    
    print("\nStarting server...")
    print("Connect using: ws://localhost:8765")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        asyncio.run(bridge.start())
    except KeyboardInterrupt:
        print("\nServer stopped.")
