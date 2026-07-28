"""
COGNITIVE-SYNC: Demo Server

Full working prototype with:
- HTTP server for static files
- WebSocket endpoint for real-time sync
- 3D visualization with HTML5 Canvas
- Create, move, and merge thoughts
"""

import asyncio
import websockets
import json
import http.server
import socketserver
import threading
import time
import random
from pathlib import Path
from typing import Set, Dict, Any, Optional
import sys
import os

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from thought_node import ThoughtNode, ThoughtSpace, EmbeddingGenerator
from websocket_bridge import WebSocketBridge, Client

# HTML/CSS/JS for the 3D visualization
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COGNITIVE-SYNC | Collaborative Thinking Space</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0f;
            color: #e0e0ff;
            overflow: hidden;
        }
        
        #canvas {
            display: block;
            width: 100vw;
            height: 100vh;
            cursor: grab;
        }
        
        #canvas:active {
            cursor: grabbing;
        }
        
        .ui {
            position: fixed;
            pointer-events: none;
            z-index: 10;
        }
        
        #header {
            top: 20px;
            left: 20px;
        }
        
        #header h1 {
            font-size: 24px;
            font-weight: 300;
            letter-spacing: 2px;
            color: #64ffd8;
            text-shadow: 0 0 20px rgba(100, 255, 216, 0.5);
        }
        
        #header h1 span {
            font-weight: 700;
        }
        
        #header p {
            font-size: 12px;
            opacity: 0.6;
            margin-top: 4px;
        }
        
        #stats {
            top: 20px;
            right: 20px;
            text-align: right;
            font-size: 12px;
            opacity: 0.7;
        }
        
        #stats .stat {
            margin-bottom: 4px;
        }
        
        #status {
            bottom: 20px;
            left: 20px;
            font-size: 11px;
            opacity: 0.5;
        }
        
        #status .connected { color: #64ff8a; }
        #status .connecting { color: #ffd664; }
        #status .disconnected { color: #ff6464; }
        
        #add-btn {
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            border-radius: 30px;
            background: linear-gradient(135deg, #64ffd8, #64aaff);
            border: none;
            color: #0a0a0f;
            font-size: 28px;
            cursor: pointer;
            pointer-events: all;
            box-shadow: 0 4px 20px rgba(100, 255, 216, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        #add-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(100, 255, 216, 0.6);
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            align-items: center;
            justify-content: center;
            z-index: 100;
        }
        
        .modal.active {
            display: flex;
            pointer-events: all;
        }
        
        .modal-content {
            background: #151520;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid rgba(100, 255, 216, 0.2);
            min-width: 300px;
        }
        
        .modal-content h3 {
            margin-bottom: 15px;
            font-weight: 300;
            color: #64ffd8;
        }
        
        .modal-content input,
        .modal-content textarea {
            width: 100%;
            padding: 12px;
            margin-bottom: 10px;
            background: #0a0a0f;
            border: 1px solid #333;
            border-radius: 6px;
            color: #e0e0ff;
            font-size: 14px;
        }
        
        .modal-content textarea {
            min-height: 80px;
            resize: vertical;
        }
        
        .modal-content input:focus,
        .modal-content textarea:focus {
            outline: none;
            border-color: #64ffd8;
        }
        
        .modal-buttons {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }
        
        .modal-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: opacity 0.2s;
        }
        
        .modal-btn:hover {
            opacity: 0.8;
        }
        
        .btn-primary {
            background: #64ffd8;
            color: #0a0a0f;
        }
        
        .btn-secondary {
            background: transparent;
            color: #999;
            border: 1px solid #444;
        }
        
        #help {
            bottom: 90px;
            right: 20px;
            font-size: 11px;
            opacity: 0.4;
            text-align: right;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    
    <div id="header" class="ui">
        <h1><span>COGNITIVE</span>-SYNC</h1>
        <p>Collaborative Thinking Space</p>
    </div>
    
    <div id="stats" class="ui">
        <div class="stat">Thoughts: <span id="thought-count">0</span></div>
        <div class="stat">Connected Users: <span id="user-count">1</span></div>
        <div class="stat">FPS: <span id="fps">60</span></div>
    </div>
    
    <div id="status" class="ui">
        <span id="connection-status" class="connecting">● Connecting...</span>
    </div>
    
    <div id="help" class="ui">
        Double-click to create<br>
        Drag to move<br>
        Mouse wheel to zoom
    </div>
    
    <button id="add-btn" class="ui">+</button>
    
    <div id="modal" class="modal">
        <div class="modal-content">
            <h3>New Thought</h3>
            <input type="text" id="author-input" placeholder="Your name" maxlength="30">
            <textarea id="thought-input" placeholder="What are you thinking?" maxlength="500"></textarea>
            <div class="modal-buttons">
                <button class="modal-btn btn-secondary" id="cancel-btn">Cancel</button>
                <button class="modal-btn btn-primary" id="create-btn">Create</button>
            </div>
        </div>
    </div>
    
    <script>
        // ============================================
        // COGNITIVE-SYNC Client: 3D Visualization
        // ============================================
        
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        // State
        let thoughts = new Map();
        let clientCursors = new Map();
        let camera = { x: 0, y: 0, z: 10, zoom: 1 };
        let isDragging = false;
        let dragThought = null;
        let mouse = { x: 0, y: 0, worldX: 0, worldY: 0 };
        let lastTime = performance.now();
        let frameCount = 0;
        let ws = null;
        let reconnectAttempts = 0;
        
        // Colors
        const colors = [
            '#64ffd8', '#64aaff', '#ff64d8', '#ffd864', 
            '#ff6464', '#64ff8a', '#c964ff', '#64c9ff'
        ];
        
        function resize() {
            canvas.width = window.innerWidth * window.devicePixelRatio;
            canvas.height = window.innerHeight * window.devicePixelRatio;
            ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
            // Reset camera center
            camera.x = canvas.width / (2 * window.devicePixelRatio);
            camera.y = canvas.height / (2 * window.devicePixelRatio);
        }
        
        window.addEventListener('resize', resize);
        resize();
        
        // Project 3D to 2D
        function project(x, y, z) {
            const scale = camera.zoom * 100 / (z + camera.z);
            return {
                x: camera.x + x * scale,
                y: camera.y - y * scale,
                scale: scale,
                visible: scale > 0.1 && z + camera.z > 0.1
            };
        }
        
        // Screen to world
        function screenToWorld(sx, sy) {
            const x = (sx - camera.x) / camera.zoom / 10;
            const y = -(sy - camera.y) / camera.zoom / 10;
            return { x, y };
        }
        
        // Draw functions
        function drawThought(thought) {
            const pos = project(thought.position[0], thought.position[1], thought.position[2]);
            if (!pos.visible) return;
            
            const size = Math.max(8, pos.scale * 3);
            const color = thought.metadata.color || colors[thought.id.charCodeAt(0) % colors.length];
            
            // Glow
            const gradient = ctx.createRadialGradient(
                pos.x, pos.y, 0,
                pos.x, pos.y, size * 2
            );
            gradient.addColorStop(0, color + '40');
            gradient.addColorStop(1, color + '00');
            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(pos.x, pos.y, size * 2, 0, Math.PI * 2);
            ctx.fill();
            
            // Core dot
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(pos.x, pos.y, size, 0, Math.PI * 2);
            ctx.fill();
            
            // Ring
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.globalAlpha = 0.5;
            ctx.beginPath();
            ctx.arc(pos.x, pos.y, size * 1.5, 0, Math.PI * 2);
            ctx.stroke();
            ctx.globalAlpha = 1;
            
            // Text label (if zoomed in enough or has text)
            if (thought.text && (pos.scale > 0.5 || isDragging)) {
                ctx.fillStyle = '#e0e0ff';
                ctx.font = `${Math.max(10, pos.scale * 4)}px sans-serif`;
                ctx.textAlign = 'center';
                ctx.shadowColor = '#000';
                ctx.shadowBlur = 4;
                
                // Wrap text
                const words = thought.text.split(' ');
                let line = '';
                let lines = [];
                const maxWidth = 150;
                
                for (let word of words) {
                    const test = line + word + ' ';
                    if (ctx.measureText(test).width > maxWidth && line) {
                        lines.push(line);
                        line = word + ' ';
                    } else {
                        line = test;
                    }
                }
                lines.push(line);
                
                const lineHeight = Math.max(12, pos.scale * 5);
                const startY = pos.y + size + 10 + (lines.length - 1) * lineHeight / 2;
                
                lines.forEach((l, i) => {
                    ctx.fillText(l, pos.x, startY - i * lineHeight);
                });
                
                // Author
                ctx.fillStyle = color;
                ctx.font = `${Math.max(8, pos.scale * 3)}px sans-serif`;
                ctx.fillText(thought.author, pos.x, pos.y - size - lineHeight);
                
                ctx.shadowBlur = 0;
            }
        }
        
        function drawConnections() {
            ctx.strokeStyle = 'rgba(100, 255, 216, 0.1)';
            ctx.lineWidth = 1;
            
            const thoughtList = Array.from(thoughts.values());
            for (let i = 0; i < thoughtList.length; i++) {
                for (let j = i + 1; j < thoughtList.length; j++) {
                    const t1 = thoughtList[i];
                    const t2 = thoughtList[j];
                    const dx = t1.position[0] - t2.position[0];
                    const dy = t1.position[1] - t2.position[1];
                    const dz = t1.position[2] - t2.position[2];
                    const dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
                    
                    if (dist < 5) {
                        const p1 = project(t1.position[0], t1.position[1], t1.position[2]);
                        const p2 = project(t2.position[0], t2.position[1], t2.position[2]);
                        if (p1.visible && p2.visible) {
                            ctx.globalAlpha = 1 - dist / 5;
                            ctx.beginPath();
                            ctx.moveTo(p1.x, p1.y);
                            ctx.lineTo(p2.x, p2.y);
                            ctx.stroke();
                            ctx.globalAlpha = 1;
                        }
                    }
                }
            }
        }
        
        function drawGrid() {
            ctx.strokeStyle = 'rgba(100, 255, 216, 0.05)';
            ctx.lineWidth = 1;
            
            const spacing = 50 * camera.zoom;
            const offsetX = camera.x % spacing;
            const offsetY = camera.y % spacing;
            
            ctx.beginPath();
            for (let x = offsetX; x < canvas.width / window.devicePixelRatio; x += spacing) {
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height / window.devicePixelRatio);
            }
            for (let y = offsetY; y < canvas.height / window.devicePixelRatio; y += spacing) {
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width / window.devicePixelRatio, y);
            }
            ctx.stroke();
        }
        
        function drawCursor(clientId, pos) {
            const projected = project(pos.x, pos.y, pos.z || 0);
            if (!projected.visible) return;
            
            const color = colors[clientId.charCodeAt(7) % colors.length];
            
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(projected.x, projected.y, 5, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.fillStyle = color;
            ctx.font = '10px sans-serif';
            ctx.fillText(clientId.slice(0, 8), projected.x + 8, projected.y + 10);
        }
        
        function render() {
            const now = performance.now();
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            
            // FPS
            frameCount++;
            if (frameCount % 30 === 0) {
                document.getElementById('fps').textContent = Math.round(1 / dt);
            }
            
            // Clear
            ctx.fillStyle = '#0a0a0f';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw grid
            drawGrid();
            
            // Draw connections
            drawConnections();
            
            // Draw thoughts (sort by Z for proper overlap)
            const sorted = Array.from(thoughts.values()).sort((a, b) => b.position[2] - a.position[2]);
            for (const thought of sorted) {
                drawThought(thought);
            }
            
            // Draw other clients' cursors
            for (const [clientId, pos] of clientCursors) {
                drawCursor(clientId, pos);
            }
            
            // Update UI
            document.getElementById('thought-count').textContent = thoughts.size;
            
            requestAnimationFrame(render);
        }
        
        // WebSocket
        function connect() {
            const statusEl = document.getElementById('connection-status');
            statusEl.className = 'connecting';
            statusEl.textContent = '● Connecting...';
            
            const wsUrl = `ws://${window.location.hostname}:8765`;
            ws = new WebSocket(wsUrl);
            
            ws.onopen = () => {
                console.log('Connected to Cognitive Sync');
                statusEl.className = 'connected';
                statusEl.textContent = '● Connected';
                reconnectAttempts = 0;
            };
            
            ws.onmessage = (e) => {
                const msg = JSON.parse(e.data);
                handleMessage(msg);
            };
            
            ws.onclose = () => {
                statusEl.className = 'disconnected';
                statusEl.textContent = '● Disconnected';
                thoughts.clear();
                clientCursors.clear();
                
                // Reconnect with backoff
                reconnectAttempts++;
                const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
                setTimeout(connect, delay);
            };
            
            ws.onerror = (err) => {
                console.error('WebSocket error:', err);
            };
        }
        
        function handleMessage(msg) {
            switch (msg.type) {
                case 'full_sync':
                    thoughts.clear();
                    for (const [id, data] of Object.entries(msg.data.thoughts)) {
                        thoughts.set(id, data);
                    }
                    break;
                    
                case 'thought_created':
                case 'thought_updated':
                    thoughts.set(msg.data.id, msg.data);
                    break;
                    
                case 'thought_deleted':
                    thoughts.delete(msg.thought_id);
                    break;
                    
                case 'thought_moved':
                    const t = thoughts.get(msg.thought_id);
                    if (t) {
                        t.position = msg.position;
                    }
                    break;
                    
                case 'presence':
                    document.getElementById('user-count').textContent = msg.client_count;
                    break;
                    
                case 'cursor_update':
                    clientCursors.set(msg.client_id, msg.position);
                    break;
            }
        }
        
        function send(msg) {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify(msg));
            }
        }
        
        // Input handling
        canvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            const rect = canvas.getBoundingClientRect();
            mouse.x = e.clientX - rect.left;
            mouse.y = e.clientY - rect.top;
            
            // Check if clicking on a thought
            const worldPos = screenToWorld(mouse.x, mouse.y);
            for (const [id, thought] of thoughts) {
                const pos = project(thought.position[0], thought.position[1], thought.position[2]);
                const dist = Math.hypot(pos.x - mouse.x, pos.y - mouse.y);
                if (dist < 20) {
                    dragThought = thought;
                    break;
                }
            }
        });
        
        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mouse.x = e.clientX - rect.left;
            mouse.y = e.clientY - rect.top;
            const worldPos = screenToWorld(mouse.x, mouse.y);
            
            if (isDragging && dragThought) {
                dragThought.position[0] = worldPos.x;
                dragThought.position[1] = worldPos.y;
                send({
                    type: 'move',
                    thought_id: dragThought.id,
                    position: dragThought.position
                });
            } else if (isDragging) {
                // Pan camera
                camera.x += e.movementX;
                camera.y += e.movementY;
            }
            
            // Send cursor position
            send({
                type: 'cursor_update',
                position: { x: worldPos.x, y: worldPos.y, z: 0 }
            });
        });
        
        canvas.addEventListener('mouseup', () => {
            isDragging = false;
            dragThought = null;
        });
        
        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
            camera.zoom *= zoomFactor;
            camera.zoom = Math.max(0.1, Math.min(10, camera.zoom));
        });
        
        canvas.addEventListener('dblclick', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const worldPos = screenToWorld(x, y);
            
            // Store position for new thought
            window.newThoughtPos = [worldPos.x, worldPos.y, 0];
            document.getElementById('modal').classList.add('active');
            document.getElementById('thought-input').value = '';
            document.getElementById('thought-input').focus();
        });
        
        // Modal handling
        document.getElementById('add-btn').addEventListener('click', () => {
            window.newThoughtPos = [
                (Math.random() - 0.5) * 4,
                (Math.random() - 0.5) * 4,
                0
            ];
            document.getElementById('modal').classList.add('active');
            document.getElementById('thought-input').value = '';
            document.getElementById('thought-input').focus();
        });
        
        document.getElementById('cancel-btn').addEventListener('click', () => {
            document.getElementById('modal').classList.remove('active');
        });
        
        document.getElementById('create-btn').addEventListener('click', createThought);
        document.getElementById('thought-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) createThought();
        });
        
        function createThought() {
            const text = document.getElementById('thought-input').value.trim();
            const author = document.getElementById('author-input').value.trim() || 'Anonymous';
            
            if (!text) return;
            
            const thought = {
                id: 'thought_' + Date.now() + '_' + Math.random().toString(36).slice(2),
                text: text,
                author: author,
                position: window.newThoughtPos || [0, 0, 0],
                timestamp: Date.now(),
                metadata: {
                    color: colors[Math.floor(Math.random() * colors.length)]
                }
            };
            
            send({ type: 'create', data: thought });
            document.getElementById('modal').classList.remove('active');
        }
        
        // Start
        connect();
        render();
    </script>
</body>
</html>
'''


class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler that serves the demo HTML."""
    
    def do_GET(self):
        """Serve the index.html for root path."""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        else:
            super().do_GET()
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


class CognitiveSyncServer:
    """
    Combined HTTP + WebSocket server for the cognitive sync demo.
    """
    
    def __init__(self, http_port: int = 8080, ws_port: int = 8765):
        self.http_port = http_port
        self.ws_port = ws_port
        self.bridge = WebSocketBridge()
        self._add_sample_thoughts()
    
    def _add_sample_thoughts(self):
        """Add some initial thoughts to the space."""
        samples = [
            ("Welcome to Cognitive Sync! 🧠", "system", (0, 0, 0)),
            ("Double-click anywhere to create new thoughts 💭", "system", (3, 2, 1)),
            ("Drag thoughts to organize your ideas ➡️", "system", (-3, 1.5, -1)),
            ("Thoughts sync in real-time across all clients 🌐", "system", (0, -2.5, 0)),
            ("Use your mouse wheel to zoom in/out 🔍", "system", (2.5, -1, 1)),
            ("Collaborative thinking is powerful! 🤝", "system", (-2, 3, 0.5)),
        ]
        
        colors = ['#64ffd8', '#64aaff', '#ff64d8', '#ffd864', '#ff6464', '#64ff8a']
        
        for i, (text, author, pos) in enumerate(samples):
            thought = ThoughtNode(text=text, author=author, position=pos)
            thought.metadata['color'] = colors[i % len(colors)]
            thought.increment_clock()
            self.bridge.space.add(thought)
    
    def _start_http(self):
        """Start HTTP server in a thread."""
        with socketserver.TCPServer(("", self.http_port), HTTPHandler) as httpd:
            print(f"  HTTP server running at http://localhost:{self.http_port}")
            httpd.serve_forever()
    
    async def _start_ws(self):
        """Start WebSocket server."""
        print(f"  WebSocket server running at ws://localhost:{self.ws_port}")
        await self.bridge.start(host="0.0.0.0", port=self.ws_port)
    
    async def run(self):
        """Run both servers."""
        print("\n" + "=" * 60)
        print("COGNITIVE-SYNC: Real-time Collaborative Thinking Platform")
        print("=" * 60 + "\n")
        
        # Start HTTP in background thread
        http_thread = threading.Thread(target=self._start_http, daemon=True)
        http_thread.start()
        
        print(f"🚀 Starting servers...")
        print(f"\n📡 WebSocket: ws://localhost:{self.ws_port}")
        print(f"🌐 Web Interface: http://localhost:{self.http_port}")
        print(f"\nOpen your browser to http://localhost:{self.http_port}")
        print("Connect multiple clients to see real-time sync!\n")
        print("Press Ctrl+C to stop\n")
        
        try:
            await self._start_ws()
        except asyncio.CancelledError:
            print("\n🛑 Server stopping...")


def main():
    """Entry point."""
    server = CognitiveSyncServer(http_port=8080, ws_port=8765)
    
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
