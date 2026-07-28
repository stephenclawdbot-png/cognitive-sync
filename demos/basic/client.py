#!/usr/bin/env python3
"""
COGNITIVE-SYNC Interactive Client

A simple terminal-based client for testing the collaborative thinking platform.

Usage:
    python client.py                    # Connect to default server
    python client.py --host ws://host:port   # Custom server
"""

import argparse
import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from websocket_bridge import WebSocketClient, MessageType
from thought_node import Vector3, ThoughtStyle, ThoughtType
import json


class InteractiveClient:
    """Interactive terminal client for COGNITIVE-SYNC."""
    
    def __init__(self, server_url: str = "ws://localhost:8765", room_id: str = "default"):
        self.server_url = server_url
        self.room_id = room_id
        self.client = WebSocketClient(server_url)
        self.running = False
        self.thoughts = {}  # Local cache
        self.presence = {}  # User presence
    
    def _setup_handlers(self):
        """Setup event handlers."""
        
        def on_welcome(data):
            print(f"\n✓ Connected! Your ID: {data.get('user_id')}")
            print(f"  Room: {data.get('room_id')}")
            print(f"  Server time: {data.get('server_time')}")
        
        def on_room_state(data):
            print(f"\n📥 Room state received:")
            print(f"  Room: {data.get('room_name', 'Unknown')}")
            print(f"  Thoughts: {data.get('thought_count', 0)}")
            print(f"  Users: {len(data.get('users', []))}")
            
            for thought in data.get('thoughts', []):
                self.thoughts[thought.get('id')] = thought
            
            print("\n  Existing thoughts:")
            for t in data.get('thoughts', [])[:5]:
                content = t.get('content', '')[:50]
                pos = t.get('position', {})
                print(f"    • '{content}' at ({pos.get('x', 0):.1f}, {pos.get('y', 0):.1f}, {pos.get('z', 0):.1f})")
            
            print("\n  Commands: create, move, connect, list, cursor, help, quit")
        
        def on_thought_created(data):
            self.thoughts[data.get('thought_id')] = data
            content = data.get('payload', {}).get('content', '')[:40]
            author = data.get('author_id', 'unknown')[:8]
            print(f"\n✨ New thought from {author}: '{content}'")
        
        def on_thought_updated(data):
            thought_id = data.get('thought_id')
            field = data.get('payload', {}).get('field')
            print(f"\n📝 Thought {thought_id[:8]} updated: {field}")
        
        def on_user_joined(data):
            uid = data.get('user_id', 'unknown')[:8]
            nick = data.get('nickname', 'Anonymous')
            print(f"\n👤 {nick} ({uid}) joined")
        
        def on_user_left(data):
            uid = data.get('user_id', 'unknown')[:8]
            print(f"\n👋 User {uid} left")
        
        def on_user_cursor(data):
            uid = data.get('user_id', '')[:8]
            pos = data.get('position', {})
            # Don't spam console with cursor updates
            pass
        
        def on_thoughts_connected(data):
            t1 = data.get('thought_id', '')[:8]
            t2 = data.get('payload', {}).get('other_id', '')[:8]
            print(f"\n🔗 Connected: {t1} <-> {t2}")
        
        def on_error(data):
            msg = data.get('message', 'Unknown error')
            print(f"\n❌ Error: {msg}")
        
        # Register handlers
        self.client.on('Welcome', on_welcome)
        self.client.on('RoomState', on_room_state)
        self.client.on('ThoughtCreated', on_thought_created)
        self.client.on('ThoughtUpdated', on_thought_updated)
        self.client.on('ThoughtsConnected', on_thoughts_connected)
        self.client.on('UserJoined', on_user_joined)
        self.client.on('UserLeft', on_user_left)
        self.client.on('UserCursor', on_user_cursor)
        self.client.on('Error', on_error)
    
    async def _command_loop(self):
        """Interactive command loop."""
        cursor_pos = Vector3(0, 0, 0)
        
        while self.running:
            try:
                command = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: input("\nclient> ")
                )
                command = command.strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                args = parts[1:]
                
                if cmd in ('quit', 'exit', 'q'):
                    self.running = False
                    break
                
                elif cmd == 'help':
                    print("""
Commands:
  create <text> [x y z]     - Create a thought at position
  move <id> <x> <y> <z>     - Move thought to position
  connect <id1> <id2>         - Connect two thoughts
  list                        - List all thoughts
  cursor <x> <y> <z>         - Update cursor position
  ping                        - Test connection
  help                        - Show this help
  quit                        - Disconnect
                    """)
                
                elif cmd == 'create':
                    if len(args) < 1:
                        print("Usage: create <text> [x y z]")
                        continue
                    
                    # Find where text ends and coords begin
                    text_parts = []
                    coords = []
                    for i, arg in enumerate(args):
                        if arg.replace('-', '').replace('.', '').isdigit() and i >= len(args) - 3:
                            coords.append(float(arg))
                        else:
                            if not coords:
                                text_parts.append(arg)
                            else:
                                coords.append(float(arg))
                    
                    content = ' '.join(text_parts)
                    x = coords[0] if len(coords) > 0 else random.randint(-5, 5)
                    y = coords[1] if len(coords) > 1 else random.randint(-5, 5)
                    z = coords[2] if len(coords) > 2 else random.randint(-2, 2)
                    
                    await self.client.create_thought(
                        content=content,
                        position=Vector3(x, y, z)
                    )
                    print(f"✓ Created thought at ({x}, {y}, {z})")
                
                elif cmd == 'move':
                    if len(args) < 4:
                        print("Usage: move <thought-id> <x> <y> <z>")
                        continue
                    
                    thought_id = args[0]
                    x, y, z = float(args[1]), float(args[2]), float(args[3])
                    
                    await self.client.move_thought(thought_id, Vector3(x, y, z))
                    print(f"✓ Moving {thought_id[:8]}... to ({x}, {y}, {z})")
                
                elif cmd == 'connect':
                    if len(args) < 2:
                        print("Usage: connect <thought-id1> <thought-id2>")
                        continue
                    
                    id1, id2 = args[0], args[1]
                    await self.client.connect_thoughts(id1, id2)
                    print(f"✓ Connecting {id1[:8]}... and {id2[:8]}...")
                
                elif cmd == 'list':
                    print(f"\n🧠 {len(self.thoughts)} thoughts cached:")
                    if not self.thoughts:
                        print("  (empty)")
                    for tid, t in self.thoughts.items():
                        content = t.get('content', '')[:40] if isinstance(t, dict) else str(t)
                        print(f"  • {tid[:8]}: {content}")
                
                elif cmd == 'cursor':
                    if len(args) < 3:
                        print("Usage: cursor <x> <y> <z>")
                        continue
                    
                    x, y, z = float(args[0]), float(args[1]), float(args[2])
                    cursor_pos = Vector3(x, y, z)
                    await self.client.update_cursor(cursor_pos)
                    print(f"✓ Cursor at ({x}, {y}, {z})")
                
                elif cmd == 'ping':
                    await self.client.send({
                        'type': MessageType.PING.value,
                        'data': {}
                    })
                    print("Ping sent...")
                
                elif cmd == 'auto':
                    print("\n🤖 Auto-creating thoughts...")
                    ideas = [
                        "The mind is a spatial navigator",
                        "Collaboration is physics",
                        "Ideas attract and repel",
                        "Distance creates meaning",
                        "Connections form constellations",
                    ]
                    for i, idea in enumerate(ideas):
                        await self.client.create_thought(
                            content=idea,
                            position=Vector3(
                                random.randint(-5, 5),
                                random.randint(-5, 5),
                                random.randint(-2, 2)
                            )
                        )
                        await asyncio.sleep(0.5)
                    print("✓ Auto-creation complete")
                
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for commands.")
                    
            except ValueError as e:
                print(f"Invalid arguments: {e}")
            except Exception as e:
                print(f"Error: {e}")
    
    async def run(self):
        """Run the interactive client."""
        self.running = True
        
        print(f"\n🧠 COGNITIVE-SYNC Interactive Client")
        print(f"   Connecting to: {self.server_url}")
        
        self._setup_handlers()
        
        # Connect
        success = await self.client.connect(self.room_id)
        if not success:
            print("✗ Failed to connect")
            return
        
        try:
            await self._command_loop()
        finally:
            await self.client.disconnect()
            print("\n👋 Goodbye!")


def main():
    parser = argparse.ArgumentParser(description="COGNITIVE-SYNC Client")
    parser.add_argument("--host", default="ws://localhost:8765", help="Server URL")
    parser.add_argument("--room", default="default", help="Room ID")
    parser.add_argument("--auto", action="store_true", help="Auto-generate thoughts")
    
    args = parser.parse_args()
    
    client = InteractiveClient(server_url=args.host, room_id=args.room)
    
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("\n\nInterrupted.")


if __name__ == "__main__":
    import random
    main()
