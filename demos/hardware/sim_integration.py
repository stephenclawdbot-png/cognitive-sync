"""
COGNITIVE-SYNC v1.2 - Hardware Simulator Integration
sim_integration.py - Connect COGNITIVE-SYNC thought streams to hardware simulator

Bridges the COGNITIVE-SYNC 3D thought space with the Hardware Simulator's
WebSocket streaming infrastructure for end-to-end testing before physical
SILENT hardware arrives (April 14).
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Callable, Any, Set
from dataclasses import dataclass, field
from pathlib import Path
import sys

# Add hardware simulator to path
HW_SIM_PATH = Path(__file__).parent.parent.parent / "hardware-simulator"
sys.path.insert(0, str(HW_SIM_PATH))

# Import COGNITIVE-SYNC core
COG_SYNC_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(COG_SYNC_PATH))

from thought_node import ThoughtNode, ThoughtSpace

# Hardware Simulator imports
try:
    from hardware_simulator import HardwareSimulator, DeviceModel, DeviceFrame
    from websocket_bridge import WebSocketBridge, WebSocketClient
    from silent_sim import SilentSimulator
    HW_SIM_AVAILABLE = True
except ImportError:
    HW_SIM_AVAILABLE = False
    logging.warning("Hardware Simulator not available - running in mock mode")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SimIntegration")


@dataclass
class IntegrationConfig:
    """Configuration for simulator integration."""
    websocket_port: int = 8767  # Separate port from main sim
    simulator_port: int = 8765  # Hardware simulator port
    enable_metrics: bool = True
    latency_target_ms: float = 50.0
    throughput_target_fps: int = 60
    auto_connect: bool = True
    thought_buffer_size: int = 1000


@dataclass
class StreamMetrics:
    """Performance metrics for the integration."""
    thoughts_received: int = 0
    thoughts_sent: int = 0
    thoughts_dropped: int = 0
    avg_latency_ms: float = 0.0
    throughput_fps: float = 0.0
    connection_uptime_s: float = 0.0
    errors: int = 0
    
    # History for analysis
    latency_history: List[float] = field(default_factory=list)
    max_history_size: int = 1000
    
    def record_latency(self, latency_ms: float):
        """Record a latency measurement."""
        self.latency_history.append(latency_ms)
        if len(self.latency_history) > self.max_history_size:
            self.latency_history = self.latency_history[-self.max_history_size:]
        self.avg_latency_ms = sum(self.latency_history) / len(self.latency_history)


class ThoughtStreamAdapter:
    """
    Adapts COGNITIVE-SYNC thought nodes to hardware simulator streams.
    
    Converts between:
    - COGNITIVE-SYNC: ThoughtNode (CRDT-based 3D thoughts)
    - Hardware Simulator: DeviceFrame (unified simulation data)
    """
    
    def __init__(self, config: IntegrationConfig = None):
        self.config = config or IntegrationConfig()
        self.metrics = StreamMetrics()
        
        # Reference to thought space
        self.thought_space: Optional[ThoughtSpace] = None
        
        # Callbacks for thought events
        self.on_thought_created: Optional[Callable[[ThoughtNode], None]] = None
        self.on_thought_updated: Optional[Callable[[ThoughtNode], None]] = None
        self.on_thought_moved: Optional[Callable[[str, tuple], None]] = None
        
        # Frame callbacks from hardware simulator
        self._frame_callbacks: List[Callable[[DeviceFrame], None]] = []
        
        logger.info("ThoughtStreamAdapter initialized")
    
    def attach_thought_space(self, space: ThoughtSpace):
        """Attach to a COGNITIVE-SYNC thought space."""
        self.thought_space = space
        logger.info(f"Attached to thought space with {len(space.thoughts)} thoughts")
    
    def thought_to_device_frame(self, thought: ThoughtNode) -> Dict[str, Any]:
        """Convert a ThoughtNode to simulator-compatible format."""
        return {
            "device_id": f"cognitive-sync-{thought.author}",
            "timestamp": thought.timestamp / 1000.0,  # Convert ms to s
            "frame_number": self.metrics.thoughts_sent,
            "data_type": "cognitive_thought",
            "payload": {
                "thought_id": thought.id,
                "text": thought.text,
                "author": thought.author,
                "position": thought.position,
                "confidence": thought.metadata.get("confidence", 1.0),
                "emg_state": thought.metadata.get("emg_state", "unknown"),
                "thought_style": thought.metadata.get("thought_style", "neutral")
            },
            "metadata": {
                "vector_clock": thought.vector_clock,
                "color": thought.metadata.get("color", "#64ffd8"),
                "size": thought.metadata.get("size_multiplier", 1.0),
                "glow_intensity": thought.metadata.get("glow_intensity", 0.5),
                "source": "COGNITIVE-SYNC",
                "version": "1.2"
            }
        }
    
    def device_frame_to_thought(self, frame: DeviceFrame) -> Optional[ThoughtNode]:
        """Convert a DeviceFrame to ThoughtNode (if applicable)."""
        if frame.data_type != "cognitive_thought":
            return None
        
        payload = frame.payload
        return ThoughtNode(
            id=payload.get("thought_id"),
            text=payload.get("text", ""),
            author=payload.get("author", "unknown"),
            position=tuple(payload.get("position", [0, 0, 0])),
            timestamp=frame.timestamp * 1000,  # Convert s to ms
            metadata=frame.metadata
        )
    
    def add_frame_callback(self, callback: Callable[[DeviceFrame], None]):
        """Register callback for incoming frames."""
        self._frame_callbacks.append(callback)
    
    def _notify_frame(self, frame: DeviceFrame):
        """Notify all frame callbacks."""
        for callback in self._frame_callbacks:
            try:
                callback(frame)
            except Exception as e:
                logger.error(f"Frame callback error: {e}")


class CognitiveSimulatorBridge:
    """
    Main bridge connecting COGNITIVE-SYNC to Hardware Simulator.
    
    Manages WebSocket connections, data transformation, and synchronization
    between the two systems.
    """
    
    def __init__(self, config: IntegrationConfig = None):
        self.config = config or IntegrationConfig()
        self.adapter = ThoughtStreamAdapter(self.config)
        
        # Hardware simulator references
        self.simulator: Optional[HardwareSimulator] = None
        self.bridge: Optional[WebSocketBridge] = None
        self.silent_device: Optional[SilentSimulator] = None
        
        # Client connections
        self._clients: Dict[str, Any] = {}
        self._ws_client: Optional[WebSocketClient] = None
        
        # State
        self._running = False
        self._start_time = None
        self._bridge_task = None
        
        # Callbacks
        self.on_connected: Optional[Callable] = None
        self.on_disconnected: Optional[Callable] = None
        self.on_thought_stream: Optional[Callable[[ThoughtNode], None]] = None
        
        logger.info("CognitiveSimulatorBridge initialized")
    
    async def initialize(self) -> bool:
        """Initialize the bridge and connect to hardware simulator."""
        if not HW_SIM_AVAILABLE:
            logger.warning("Hardware Simulator not available - using mock mode")
            return await self._initialize_mock()
        
        try:
            # Create hardware simulator
            self.simulator = HardwareSimulator()
            
            # Create SILENT device for EMG simulation
            self.silent_device = SilentSimulator(device_id="silent-cog-sync")
            await self.silent_device.initialize()
            
            # Register with simulator
            self.simulator.register_device(self.silent_device)
            
            # Create WebSocket bridge
            self.bridge = WebSocketBridge(
                self.simulator,
                port=self.config.websocket_port
            )
            
            logger.info(f"Bridge initialized on port {self.config.websocket_port}")
            return True
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            return False
    
    async def _initialize_mock(self) -> bool:
        """Initialize in mock mode (no hardware simulator)."""
        logger.info("Initializing in MOCK mode")
        return True
    
    async def start(self):
        """Start the bridge and begin streaming."""
        self._running = True
        self._start_time = time.time()
        
        if HW_SIM_AVAILABLE and self.bridge:
            # Start WebSocket bridge
            self._bridge_task = asyncio.create_task(self.bridge.start())
            
            # Start simulator
            self.simulator.start()
            
            logger.info("Bridge started - accepting connections")
            
            if self.on_connected:
                self.on_connected()
        else:
            logger.info("Bridge started in MOCK mode")
    
    async def connect_to_simulator(self) -> bool:
        """Connect to existing hardware simulator instance."""
        if not HW_SIM_AVAILABLE:
            logger.warning("Cannot connect - Hardware Simulator not available")
            return False
        
        try:
            self._ws_client = WebSocketClient(
                uri=f"ws://localhost:{self.config.simulator_port}"
            )
            
            welcome = await self._ws_client.connect()
            logger.info(f"Connected to simulator: {welcome}")
            
            # Subscribe to SILENT device
            await self._ws_client.subscribe(["silent-01", "silent-cog-sync"])
            
            # Set up frame callback
            self._ws_client.on_message(self._handle_simulator_message)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to simulator: {e}")
            return False
    
    def _handle_simulator_message(self, message: Dict):
        """Handle messages from hardware simulator."""
        if message.get("data_type") == "silent_emg_imu":
            # Convert EMG data to thought suggestion
            self._process_emg_for_thoughts(message)
    
    def _process_emg_for_thoughts(self, emg_data: Dict):
        """Process EMG data and suggest thoughts."""
        payload = emg_data.get("payload", {})
        activity_level = payload.get("activity_level", 0)
        phoneme = payload.get("current_phoneme", "silence")
        
        # High activity might indicate intentional thought
        if activity_level > 0.5 and phoneme != "silence":
            # Create thought suggestion
            thought = ThoughtNode(
                text=f"[EMG detected: {phoneme}]",
                author="silent-user",
                position=(0, 0, 0),
                metadata={
                    "emg_state": "word_detected" if activity_level > 0.8 else "thinking",
                    "confidence": payload.get("detection_confidence", 0.5),
                    "source": "SILENT_SIMULATOR",
                    "phoneme": phoneme
                }
            )
            
            if self.on_thought_stream:
                self.on_thought_stream(thought)
    
    async def publish_thought(self, thought: ThoughtNode):
        """Publish a thought to the simulator stream."""
        if not self._running:
            logger.warning("Bridge not running, cannot publish")
            return
        
        frame_data = self.adapter.thought_to_device_frame(thought)
        
        # In real mode, broadcast via bridge
        if HW_SIM_AVAILABLE and self.bridge:
            # Create DeviceFrame
            frame = DeviceFrame(
                device_id=frame_data["device_id"],
                timestamp=frame_data["timestamp"],
                frame_number=frame_data["frame_number"],
                data_type=frame_data["data_type"],
                payload=frame_data["payload"],
                metadata=frame_data["metadata"]
            )
            
            # Broadcast via simulator callback
            self.adapter._notify_frame(frame)
        
        self.adapter.metrics.thoughts_sent += 1
        
        # Calculate latency
        latency = (time.time() - frame_data["timestamp"]) * 1000
        self.adapter.metrics.record_latency(latency)
    
    async def stop(self):
        """Stop the bridge and cleanup."""
        self._running = False
        
        if self.bridge:
            self.bridge.stop()
        
        if self.simulator:
            self.simulator.stop()
        
        if self._ws_client:
            await self._ws_client.close()
        
        if self._bridge_task:
            self._bridge_task.cancel()
            try:
                await self._bridge_task
            except asyncio.CancelledError:
                pass
        
        if self.on_disconnected:
            self.on_disconnected()
        
        logger.info("Bridge stopped")
    
    def get_metrics(self) -> StreamMetrics:
        """Get current performance metrics."""
        if self._start_time:
            self.adapter.metrics.connection_uptime_s = time.time() - self._start_time
        return self.adapter.metrics


class CognitiveSimulatorClient:
    """
    Client for connecting to the Cognitive Simulator Bridge.
    
    Simple interface for applications to receive thought streams
    from the integrated simulator.
    """
    
    def __init__(self, uri: str = "ws://localhost:8767"):
        self.uri = uri
        self._client: Optional[WebSocketClient] = None
        self._thought_callbacks: List[Callable[[ThoughtNode], None]] = []
        self._connected = False
    
    async def connect(self) -> bool:
        """Connect to the cognitive simulator bridge."""
        if not HW_SIM_AVAILABLE:
            logger.warning("Cannot connect - Hardware Simulator not available")
            return False
        
        try:
            self._client = WebSocketClient(uri=self.uri)
            await self._client.connect()
            self._client.on_message(self._handle_message)
            self._connected = True
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    def _handle_message(self, message: Dict):
        """Handle incoming message."""
        if message.get("data_type") == "cognitive_thought":
            thought = ThoughtStreamAdapter().device_frame_to_thought(
                DeviceFrame(**message)
            )
            if thought:
                for callback in self._thought_callbacks:
                    callback(thought)
    
    def on_thought(self, callback: Callable[[ThoughtNode], None]):
        """Register thought callback."""
        self._thought_callbacks.append(callback)
    
    async def subscribe_thoughts(self):
        """Subscribe to thought stream."""
        if self._client:
            await self._client.subscribe(["*"])
    
    async def disconnect(self):
        """Disconnect from bridge."""
        if self._client:
            await self._client.close()
        self._connected = False


# Demo
async def demo():
    """Demonstrate simulator integration."""
    print("=" * 70)
    print("COGNITIVE-SYNC v1.2 - Hardware Simulator Integration Demo")
    print("=" * 70)
    print()
    
    config = IntegrationConfig(
        websocket_port=8767,
        enable_metrics=True
    )
    
    # Create bridge
    bridge = CognitiveSimulatorBridge(config)
    
    # Initialize
    success = await bridge.initialize()
    if not success:
        print("Failed to initialize bridge")
        return
    
    # Set up thought callback
    def on_thought(thought):
        print(f"  [THOUGHT] '{thought.text[:30]}...' by {thought.author}")
    
    bridge.on_thought_stream = on_thought
    
    # Start bridge
    await bridge.start()
    
    print("Bridge running on ws://localhost:8767")
    print("Generating sample thoughts...")
    print()
    
    # Generate some test thoughts
    for i in range(5):
        thought = ThoughtNode(
            text=f"Test thought {i+1}: Simulated EMG integration working!",
            author="test-user",
            position=(i * 2, i, i * 0.5),
            metadata={
                "emg_state": "word_detected",
                "confidence": 0.85,
                "source": "SILENT_SIMULATOR",
                "color": "#64ffd8"
            }
        )
        
        await bridge.publish_thought(thought)
        await asyncio.sleep(0.5)
    
    # Show metrics
    print()
    print("=" * 70)
    print("Performance Metrics:")
    metrics = bridge.get_metrics()
    print(f"  Thoughts sent: {metrics.thoughts_sent}")
    print(f"  Avg latency: {metrics.avg_latency_ms:.2f} ms")
    print(f"  Uptime: {metrics.connection_uptime_s:.2f} s")
    print("=" * 70)
    
    # Keep running briefly
    await asyncio.sleep(2)
    
    # Cleanup
    await bridge.stop()
    print("\nDemo complete!")


if __name__ == "__main__":
    asyncio.run(demo())
