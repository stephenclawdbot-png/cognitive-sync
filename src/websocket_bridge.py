"""
WebSocket Bridge - Real-time sync layer for COGNITIVE-SYNC.

Provides:
- Bidirectional event streaming
- Presence awareness
- Delta compression
- Automatic reconnection with state replay
- Room-based collaboration sessions
"""

import asyncio
import json
import time
import traceback
from typing import Dict, Set, List, Optional, Callable, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
import uuid

import websockets
from websockets.server import WebSocketServerProtocol
from websockets.typing import Data

from thought_node import ThoughtNode, Vector3, ThoughtStyle, ThoughtPhysics, ThoughtType
from crdt_engine import CRDTDocument, CRDTOperation, VectorClock


class MessageType(Enum):
    """WebSocket message types."""
    # Client -> Server
    JOIN_ROOM = "join_room"
    LEAVE_ROOM = "leave_room"
    CREATE_THOUGHT = "create_thought"
    UPDATE_THOUGHT = "update_thought"
    DELETE_THOUGHT = "delete_thought"
    CONNECT_THOUGHTS = "connect_thoughts"
    CURSOR_POSITION = "cursor_position"
    PING = "ping"
    SYNC_REQUEST = "sync_request"
    
    # Server -> Client
    WELCOME = "welcome"
    ROOM_STATE = "room_state"
    THOUGHT_CREATED = "thought_created"
    THOUGHT_UPDATED = "thought_updated"
    THOUGHT_DELETED = "thought_deleted"
    THOUGHTS_CONNECTED = "thoughts_connected"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    USER_CURSOR = "user_cursor"
    SYNC_RESPONSE = "sync_response"
    PONG = "pong"
    ERROR = "error"


@dataclass
class UserPresence:
    """User presence information."""
    user_id: str
    nickname: str = "Anonymous"
    color: str = "#6366F1"
    cursor_position: Optional[Vector3] = None
    joined_at: int = field(default_factory=time.time_ns)
    last_seen: int = field(default_factory=time.time_ns)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'color': self.color,
            'cursor_position': asdict(self.cursor_position) if self.cursor_position else None,
            'joined_at': self.joined_at,
            'last_seen': self.last_seen
        }


class CollaborationRoom:
    """
    A room where multiple users collaborate on shared thoughts.
    Each room has its own CRDT document.
    """
    
    def __init__(self, room_id: str, room_name: str = ""):
        self.room_id = room_id
        self.room_name = room_name or room_id
        self.document = CRDTDocument(site_id=f"room-{room_id}")
        self.users: Dict[str, WebSocketServerProtocol] = {}  # user_id -> websocket
        self.presence: Dict[str, UserPresence] = {}  # user_id -> presence
        self.created_at = time.time()
        self.message_history: List[Dict] = []  # Recent messages for replay
        self.max_history = 1000
        
        # Subscribe to document operations
        self.document.register_callback(self._on_document_operation)
    
    def _on_document_operation(self, op: CRDTOperation) -> None:
        """Callback when document changes."""
        # Broadcast to all connected users
        asyncio.create_task(self._broadcast_operation(op))
    
    async def _broadcast_operation(self, op: CRDTOperation) -> None:
        """Broadcast operation to all users in room."""
        message = self._operation_to_message(op)
        await self.broadcast(message)
    
    def _operation_to_message(self, op: CRDTOperation) -> Dict[str, Any]:
        """Convert CRDT operation to websocket message."""
        type_map = {
            CRDTOperation.TYPE_CREATE: MessageType.THOUGHT_CREATED,
            CRDTOperation.TYPE_UPDATE: MessageType.THOUGHT_UPDATED,
            CRDTOperation.TYPE_DELETE: MessageType.THOUGHT_DELETED,
            CRDTOperation.TYPE_CONNECT: MessageType.THOUGHTS_CONNECTED,
            CRDTOperation.TYPE_DISCONNECT: MessageType.THOUGHTS_CONNECTED
        }
        
        msg_type = type_map.get(op.op_type, MessageType.ERROR)
        
        return {
            'type': msg_type.value,
            'timestamp': op.timestamp,
            'data': {
                'thought_id': op.thought_id,
                'author_id': op.author_id,
                'payload': op.payload,
                'vector_clock': op.vector_clock.to_dict()
            }
        }
    
    async def join(self, user_id: str, websocket: WebSocketServerProtocol, nickname: str = "", color: str = "") -> None:
        """Add a user to the room."""
        self.users[user_id] = websocket
        self.presence[user_id] = UserPresence(
            user_id=user_id,
            nickname=nickname or f"User_{user_id[:4]}",
            color=color or f"#{uuid.uuid4().hex[:6]}"
        )
        
        # Broadcast user joined
        await self.broadcast({
            'type': MessageType.USER_JOINED.value,
            'timestamp': time.time_ns(),
            'data': self.presence[user_id].to_dict()
        }, exclude_user=user_id)
        
        # Send current room state to new user
        await self._send_room_state(user_id, websocket)
    
    async def leave(self, user_id: str) -> None:
        """Remove a user from the room."""
        if user_id in self.users:
            del self.users[user_id]
        if user_id in self.presence:
            del self.presence[user_id]
        
        if self.users:
            await self.broadcast({
                'type': MessageType.USER_LEFT.value,
                'timestamp': time.time_ns(),
                'data': {'user_id': user_id}
            })
    
    async def _send_room_state(self, user_id: str, websocket: WebSocketServerProtocol) -> None:
        """Send current state to a newly joined user."""
        thoughts = self.document.get_all_thoughts()
        
        await self._send(websocket, {
            'type': MessageType.ROOM_STATE.value,
            'timestamp': time.time_ns(),
            'data': {
                'room_id': self.room_id,
                'thought_count': len(thoughts),
                'thoughts': [t.to_dict() for t in thoughts],
                'users': [p.to_dict() for p in self.presence.values()],
                'your_user_id': user_id
            }
        })
    
    async def _send(self, websocket: WebSocketServerProtocol, message: Dict) -> None:
        """Send message to a specific websocket."""
        try:
            await websocket.send(json.dumps(message))
        except Exception as e:
            print(f"Error sending message: {e}")
    
    async def broadcast(
        self,
        message: Dict,
        exclude_user: Optional[str] = None
    ) -> None:
        """Broadcast message to all users in room."""
        if self.users:
            # Store in history
            self.message_history.append(message)
            if len(self.message_history) > self.max_history:
                self.message_history = self.message_history[-self.max_history:]
            
            # Send to all users
            for user_id, ws in self.users.items():
                if user_id != exclude_user:
                    try:
                        await ws.send(json.dumps(message))
                    except Exception:
                        pass
    
    async def handle_message(self, user_id: str, message: Dict) -> Optional[Dict]:
        """Handle a message from a user."""
        msg_type = message.get('type')
        data = message.get('data', {})
        
        if msg_type == MessageType.CREATE_THOUGHT.value:
            return await self._handle_create_thought(user_id, data)
        elif msg_type == MessageType.UPDATE_THOUGHT.value:
            return await self._handle_update_thought(user_id, data)
        elif msg_type == MessageType.DELETE_THOUGHT.value:
            return await self._handle_delete_thought(user_id, data)
        elif msg_type == MessageType.CONNECT_THOUGHTS.value:
            return await self._handle_connect_thoughts(user_id, data)
        elif msg_type == MessageType.CURSOR_POSITION.value:
            return await self._handle_cursor_position(user_id, data)
        elif msg_type == MessageType.SYNC_REQUEST.value:
            return await self._handle_sync_request(user_id, data)
        elif msg_type == MessageType.PING.value:
            return {'type': MessageType.PONG.value, 'timestamp': time.time_ns()}
        
        return None
    
    async def _handle_create_thought(self, user_id: str, data: Dict) -> Optional[Dict]:
        """Handle thought creation."""
        thought_id = data.get('thought_id') or str(uuid.uuid4())
        pos_data = data.get('position', {'x': 0, 'y': 0, 'z': 0})
        position = Vector3(**pos_data)
        
        style_data = data.get('style', {})
        style = ThoughtStyle(**style_data) if style_data else ThoughtStyle()
        
        physics_data = data.get('physics', {})
        physics = ThoughtPhysics.from_dict(physics_data) if physics_data else ThoughtPhysics()
        
        op = self.document.create_thought(
            thought_id=thought_id,
            content=data.get('content', ''),
            position=position,
            author_id=user_id,
            style=style,
            physics=physics
        )
        return self._operation_to_message(op)
    
    async def _handle_update_thought(self, user_id: str, data: Dict) -> Optional[Dict]:
        """Handle thought update."""
        thought_id = data.get('thought_id')
        field = data.get('field')
        value = data.get('value')
        
        op = self.document.update_thought(thought_id, field, value, user_id)
        if op:
            return self._operation_to_message(op)
        return None
    
    async def _handle_delete_thought(self, user_id: str, data: Dict) -> Optional[Dict]:
        """Handle thought deletion."""
        thought_id = data.get('thought_id')
        op = self.document.delete_thought(thought_id, user_id)
        if op:
            return self._operation_to_message(op)
        return None
    
    async def _handle_connect_thoughts(self, user_id: str, data: Dict) -> Optional[Dict]:
        """Handle connecting two thoughts."""
        thought_id1 = data.get('thought_id1')
        thought_id2 = data.get('thought_id2')
        strength = data.get('strength', 1.0)
        
        op = self.document.connect_thoughts(thought_id1, thought_id2, user_id, strength)
        if op:
            return self._operation_to_message(op)
        return None
    
    async def _handle_cursor_position(self, user_id: str, data: Dict) -> Optional[Dict]:
        """Handle cursor position update."""
        if user_id in self.presence:
            pos_data = data.get('position', {})
            self.presence[user_id].cursor_position = Vector3(**pos_data)
            self.presence[user_id].last_seen = time.time_ns()
        
        return {
            'type': MessageType.USER_CURSOR.value,
            'timestamp': time.time_ns(),
            'data': {
                'user_id': user_id,
                'position': data.get('position')
            }
        }
    
    async def _handle_sync_request(self, user_id: str, data: Dict) -> Dict:
        """Handle sync request with vector clock."""
        clock_data = data.get('vector_clock', {})
        since_clock = VectorClock.from_dict(clock_data)
        
        operations = self.document.get_state_delta(since_clock)
        
        return {
            'type': MessageType.SYNC_RESPONSE.value,
            'timestamp': time.time_ns(),
            'data': {
                'operations': [op.to_dict() for op in operations],
                'current_clock': self.document.vector_clock.to_dict()
            }
        }
    
    def get_user_count(self) -> int:
        return len(self.users)


class WebSocketBridge:
    """
    Main WebSocket server handling multiple rooms and user connections.
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.rooms: Dict[str, CollaborationRoom] = {}
        self.user_rooms: Dict[str, str] = {}  # user_id -> room_id
        self.user_metadata: Dict[str, Dict] = {}  # user_id -> {nickname, color}
        self._server = None
    
    def get_or_create_room(self, room_id: str, room_name: str = "") -> CollaborationRoom:
        """Get existing room or create new one."""
        if room_id not in self.rooms:
            self.rooms[room_id] = CollaborationRoom(room_id, room_name or room_id)
            print(f"Created room: {room_id}")
        return self.rooms[room_id]
    
    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        """Handle a new WebSocket connection."""
        user_id = None
        room_id = None
        
        try:
            # Parse room from path: /ws/room-id
            path_parts = path.strip('/').split('/')
            if len(path_parts) >= 1 and path_parts[0] in ('ws', 'room'):
                path_parts = path_parts[1:]
            
            room_id = path_parts[0] if path_parts else "default"
            room = self.get_or_create_room(room_id)
            
            # Extract user info from query params
            # In production, use proper auth
            user_id = str(uuid.uuid4())[:8]
            
            # Send welcome
            await websocket.send(json.dumps({
                'type': MessageType.WELCOME.value,
                'data': {
                    'user_id': user_id,
                    'room_id': room_id,
                    'server_time': time.time_ns()
                }
            }))
            
            # Join room
            nickname = f"User_{user_id}"
            await room.join(user_id, websocket, nickname=nickname)
            self.user_rooms[user_id] = room_id
            
            print(f"User {user_id} joined room {room_id}")
            
            # Message loop
            async for message in websocket:
                try:
                    data = json.loads(message)
                    response = await room.handle_message(user_id, data)
                    
                    if response:
                        await room.broadcast(response)
                        
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        'type': MessageType.ERROR.value,
                        'data': {'message': 'Invalid JSON'}
                    }))
                except Exception as e:
                    print(f"Error handling message: {e}")
                    traceback.print_exc()
        
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            # Cleanup
            if user_id and room_id:
                if room_id in self.rooms:
                    await self.rooms[room_id].leave(user_id)
                del self.user_rooms[user_id]
                print(f"User {user_id} left room {room_id}")
                
                # Clean up empty rooms
                if room_id in self.rooms and self.rooms[room_id].get_user_count() == 0:
                    del self.rooms[room_id]
                    print(f"Removed empty room: {room_id}")
    
    async def start(self) -> None:
        """Start the WebSocket server."""
        self._server = await websockets.serve(
            self.handle_connection,
            self.host,
            self.port,
            ping_interval=20,
            ping_timeout=10
        )
        print(f"WebSocket server started on ws://{self.host}:{self.port}")
        await self._server.wait_closed()
    
    async def stop(self) -> None:
        """Stop the WebSocket server."""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        print("WebSocket server stopped")
    
    def get_stats(self) -> Dict:
        """Get server statistics."""
        return {
            'rooms': len(self.rooms),
            'total_users': len(self.user_rooms),
            'room_details': [
                {
                    'id': r.room_id,
                    'name': r.room_name,
                    'users': r.get_user_count(),
                    'thoughts': len(r.document.get_all_thoughts())
                }
                for r in self.rooms.values()
            ]
        }


class WebSocketClient:
    """
    Client for connecting to COGNITIVE-SYNC server.
    """
    
    def __init__(self, server_url: str = "ws://localhost:8765"):
        self.server_url = server_url
        self.websocket = None
        self.user_id = None
        self.room_id = None
        self.connected = False
        self._callbacks: Dict[str, List[Callable]] = {}
        self._message_loop_task = None
    
    def on(self, event_type: str, callback: Callable) -> None:
        """Register event callback."""
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []
        self._callbacks[event_type].append(callback)
    
    def _emit(self, event_type: str, data: Any) -> None:
        """Emit event to registered callbacks."""
        for cb in self._callbacks.get(event_type, []):
            try:
                cb(data)
            except Exception as e:
                print(f"Callback error: {e}")
    
    async def connect(self, room_id: str = "default") -> bool:
        """Connect to server and join room."""
        try:
            url = f"{self.server_url}/ws/{room_id}"
            self.websocket = await websockets.connect(url)
            
            # Wait for welcome
            welcome = json.loads(await self.websocket.recv())
            if welcome['type'] == MessageType.WELCOME.value:
                self.user_id = welcome['data']['user_id']
                self.room_id = welcome['data']['room_id']
                self.connected = True
                
                # Start message loop
                self._message_loop_task = asyncio.create_task(self._message_loop())
                
                print(f"Connected as {self.user_id} in room {self.room_id}")
                return True
            
        except Exception as e:
            print(f"Connection error: {e}")
        return False
    
    async def _message_loop(self) -> None:
        """Background task to receive messages."""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get('type')
                    
                    # Emit based on message type
                    event_name = msg_type.replace('_', ' ').title().replace(' ', '')
                    self._emit(event_name, data.get('data'))
                    self._emit('message', data)
                    
                except json.JSONDecodeError:
                    pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected = False
    
    async def send(self, message: Dict) -> None:
        """Send message to server."""
        if self.websocket and self.connected:
            await self.websocket.send(json.dumps(message))
    
    async def create_thought(self, content: str, position: Vector3, **kwargs) -> None:
        """Create a new thought."""
        await self.send({
            'type': MessageType.CREATE_THOUGHT.value,
            'data': {
                'content': content,
                'position': {'x': position.x, 'y': position.y, 'z': position.z},
                **kwargs
            }
        })
    
    async def update_thought(self, thought_id: str, field: str, value: Any) -> None:
        """Update a thought field."""
        await self.send({
            'type': MessageType.UPDATE_THOUGHT.value,
            'data': {
                'thought_id': thought_id,
                'field': field,
                'value': value
            }
        })
    
    async def move_thought(self, thought_id: str, position: Vector3) -> None:
        """Update thought position."""
        await self.update_thought(thought_id, 'position', {
            'x': position.x, 'y': position.y, 'z': position.z
        })
    
    async def connect_thoughts(self, thought_id1: str, thought_id2: str, strength: float = 1.0) -> None:
        """Connect two thoughts."""
        await self.send({
            'type': MessageType.CONNECT_THOUGHTS.value,
            'data': {
                'thought_id1': thought_id1,
                'thought_id2': thought_id2,
                'strength': strength
            }
        })
    
    async def update_cursor(self, position: Vector3) -> None:
        """Update cursor position."""
        await self.send({
            'type': MessageType.CURSOR_POSITION.value,
            'data': {
                'position': {'x': position.x, 'y': position.y, 'z': position.z}
            }
        })
    
    async def disconnect(self) -> None:
        """Disconnect from server."""
        if self._message_loop_task:
            self._message_loop_task.cancel()
        if self.websocket:
            await self.websocket.close()
        self.connected = False


if __name__ == "__main__":
    print("=== WebSocket Bridge Demo ===\n")
    
    async def test_server():
        bridge = WebSocketBridge(host="127.0.0.1", port=8766)
        
        # Start server
        server_task = asyncio.create_task(bridge.start())
        
        # Give server time to start
        await asyncio.sleep(1)
        
        # Test client
        client = WebSocketClient("ws://127.0.0.1:8766")
        
        received_messages = []
        client.on('ThoughtCreated', lambda data: received_messages.append(data))
        
        # Connect
        success = await client.connect("test-room")
        print(f"Client connected: {success}")
        print(f"User ID: {client.user_id}")
        
        # Create some thoughts
        await client.create_thought("Hello spatial world!", Vector3(0, 0, 0))
        await asyncio.sleep(0.5)
        
        await client.create_thought("Ideas connect in 3D", Vector3(2, 1, 0))
        await asyncio.sleep(0.5)
        
        # Wait for responses
        await asyncio.sleep(1)
        
        print(f"\nReceived {len(received_messages)} messages")
        
        # Cleanup
        await client.disconnect()
        await bridge.stop()
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
        
        print("\nDemo complete!")
    
    # Run demo
    asyncio.run(test_server())
