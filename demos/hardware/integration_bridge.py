"""
COGNITIVE-SYNC v1.2: Integration Bridge

Bridges COGNITIVE-SYNC thought_node system with HARDWARE-SIMULATOR.
Enables pre-hardware testing by connecting:
- COGNITIVE-SYNC thought nodes → HARDWARE-SIMULATOR inputs
- HARDWARE-SIMULATOR outputs → COGNITIVE-SYNC visualization

Features:
- Real-time WebSocket pipeline (<100ms latency target)
- Bidirectional data flow
- Automatic protocol translation
- Latency monitoring and optimization
"""

import asyncio
import json
import time
import logging
from typing import Optional, Dict, Any, List, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("integration_bridge")

# Add paths for imports
WORKSPACE = Path("/Users/clawdbot/.openclaw/workspace")
COGNITIVE_PATH = WORKSPACE / "COGNITIVE-SYNC"
SILENT_PATH = WORKSPACE / "SILENT-001" / "firmware"
HARDWARE_PATH = WORKSPACE / "hardware-simulator"

sys.path.insert(0, str(COGNITIVE_PATH))
sys.path.insert(0, str(SILENT_PATH))
sys.path.insert(0, str(HARDWARE_PATH))

from thought_node import ThoughtNode, ThoughtSpace
from SILENT_SIMULATOR import SilentSimulator, SimulatorConfig, EMGWaveformSimulator
from aether_sim import AetherSimulator, VolumeConfig
from mycosentinel_sim import MycosentinelSimulator


class IntegrationState(Enum):
    """Bridge operational states."""
    DISCONNECTED = auto()
    CONNECTING = auto()
    EMG_CONNECTED = auto()
    AETHER_CONNECTED = auto()
    MYCO_CONNECTED = auto()
    FULLY_CONNECTED = auto()
    ERROR = auto()


@dataclass
class LatencyMetrics:
    """Track latency across the pipeline."""
    emg_to_thought_ms: List[float] = field(default_factory=list)
    thought_to_particle_ms: List[float] = field(default_factory=list)
    total_pipeline_ms: List[float] = field(default_factory=list)
    
    def add_emg_thought(self, latency: float):
        self.emg_to_thought_ms.append(latency)
        if len(self.emg_to_thought_ms) > 1000:
            self.emg_to_thought_ms = self.emg_to_thought_ms[-1000:]
    
    def add_thought_particle(self, latency: float):
        self.thought_to_particle_ms.append(latency)
        if len(self.thought_to_particle_ms) > 1000:
            self.thought_to_particle_ms = self.thought_to_particle_ms[-1000:]
    
    def add_total(self, latency: float):
        self.total_pipeline_ms.append(latency)
        if len(self.total_pipeline_ms) > 1000:
            self.total_pipeline_ms = self.total_pipeline_ms[-1000:]
    
    def stats(self) -> Dict[str, Any]:
        def calc_avg(latencies: List[float]) -> float:
            return sum(latencies) / len(latencies) if latencies else 0.0
        
        def calc_p99(latencies: List[float]) -> float:
            if not latencies:
                return 0.0
            sorted_lats = sorted(latencies)
            idx = int(len(sorted_lats) * 0.99)
            return sorted_lats[min(idx, len(sorted_lats) - 1)]
        
        return {
            "emg_to_thought_avg_ms": calc_avg(self.emg_to_thought_ms),
            "emg_to_thought_p99_ms": calc_p99(self.emg_to_thought_ms),
            "thought_to_particle_avg_ms": calc_avg(self.thought_to_particle_ms),
            "thought_to_particle_p99_ms": calc_p99(self.thought_to_particle_ms),
            "total_pipeline_avg_ms": calc_avg(self.total_pipeline_ms),
            "total_pipeline_p99_ms": calc_p99(self.total_pipeline_ms),
            "samples": len(self.total_pipeline_ms)
        }


@dataclass
class SimulationTarget:
    """Target position for AETHER particles based on thought."""
    thought_id: str
    position: Tuple[float, float, float]
    intensity: float
    hue: float
    lifetime: float
    created_at: float


class IntegrationBridge:
    """
    Main integration bridge connecting COGNITIVE-SYNC with HARDWARE-SIMULATOR.
    
    Data Flow:
    1. SILENT_SIMULATOR generates EMG signals
    2. Signals converted to ThoughtNode objects
    3. ThoughtNodes formatted as AETHER particle targets
    4. MYCOSENTINEL provides environmental context
    5. Real-time sync via WebSocket pipeline
    """
    
    def __init__(
        self,
        ws_port: int = 8765,
        target_latency_ms: float = 100.0
    ):
        self.ws_port = ws_port
        self.target_latency_ms = target_latency_ms
        
        # State
        self.state = IntegrationState.DISCONNECTED
        self.running = False
        self.metrics = LatencyMetrics()
        
        # Subsystems
        self.thought_space = ThoughtSpace()
        self.silent_sim: Optional[SilentSimulator] = None
        self.aether_sim: Optional[AetherSimulator] = None
        self.myco_sim: Optional[MycosentinelSimulator] = None
        
        # Data buffers
        self.thought_targets: Dict[str, SimulationTarget] = {}
        self.clients: set = set()
        self.server: Optional[Any] = None
        
        # Callbacks
        self.on_thought_created: Optional[Callable[[ThoughtNode], None]] = None
        self.on_particle_target: Optional[Callable[[SimulationTarget], None]] = None
        self.on_environment_update: Optional[Callable[[Dict], None]] = None
        
        # Performance tracking
        self._emg_timestamps: Dict[str, float] = {}
        self._thought_timestamps: Dict[str, float] = {}
        
        logger.info(f"IntegrationBridge initialized (target latency: {target_latency_ms}ms)")
    
    async def initialize(self) -> bool:
        """Initialize all simulators."""
        logger.info("Initializing Integration Bridge...")
        self.state = IntegrationState.CONNECTING
        
        try:
            # Initialize SILENT simulator
            config = SimulatorConfig(
                word_detection_probability=0.8,
                vocabulary=[
                    "explore", "create", "analyze", "connect", "focus",
                    "search", "build", "design", "optimize", "imagine"
                ]
            )
            self.silent_sim = SilentSimulator(config=config, mode="stdout")
            self.silent_sim.waveform = EMGWaveformSimulator(config)
            self.state = IntegrationState.EMG_CONNECTED
            logger.info("✓ SILENT simulator initialized")
            
            # Initialize AETHER simulator
            self.aether_sim = AetherSimulator(
                device_id="aether-cognitive-01",
                config={"max_particles": 50000}
            )
            await self.aether_sim.initialize()
            self.state = IntegrationState.AETHER_CONNECTED
            logger.info("✓ AETHER simulator initialized")
            
            # Initialize MYCOSENTINEL simulator
            self.myco_sim = MycosentinelSimulator(
                device_id="myco-cognitive-01",
                config={}
            )
            await self.myco_sim.initialize()
            self.state = IntegrationState.MYCO_CONNECTED
            logger.info("✓ MYCOSENTINEL simulator initialized")
            
            self.state = IntegrationState.FULLY_CONNECTED
            return True
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            self.state = IntegrationState.ERROR
            return False
    
    async def start(self) -> None:
        """Start the integration bridge."""
        if not self.state == IntegrationState.FULLY_CONNECTED:
            logger.error("Cannot start: not fully initialized")
            return
        
        self.running = True
        logger.info("Starting Integration Bridge...")
        
        # Start WebSocket server
        try:
            import websockets
            self.server = await websockets.serve(
                self._handle_client,
                "localhost",
                self.ws_port
            )
            logger.info(f"✓ WebSocket server listening on port {self.ws_port}")
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
        
        # Start simulation loop
        await self._simulation_loop()
    
    async def _simulation_loop(self) -> None:
        """Main simulation loop."""
        self.silent_sim.waveform.start()
        
        tick_interval = 0.01  # 10ms tick for <100ms latency target
        
        while self.running:
            loop_start = time.time() * 1000
            
            # Process EMG signals
            await self._process_emg()
            
            # Update AETHER with thought targets
            await self._update_aether()
            
            # Get environmental factors from MYCOSENTINEL
            await self._update_environment()
            
            # Broadcast state to clients
            await self._broadcast_state()
            
            # Calculate and enforce latency target
            elapsed = (time.time() * 1000) - loop_start
            if elapsed < self.target_latency_ms / 10:  # Target distributed across subsystems
                await asyncio.sleep(max(0, (self.target_latency_ms / 10 - elapsed) / 1000))
            
            await asyncio.sleep(tick_interval)
    
    async def _process_emg(self) -> None:
        """Process EMG signals and convert to thoughts."""
        result = self.silent_sim.waveform.tick()
        
        if result:
            state, timestamp, word, confidence = result
            
            # Track EMG timestamp
            emg_key = f"{state}_{timestamp}"
            self._emg_timestamps[emg_key] = time.time() * 1000
            
            if state == "word_detected" and word:
                # Convert to thought
                thought_id = f"thought_{int(timestamp)}_{word}"
                thought = ThoughtNode(
                    id=thought_id,
                    text=word,
                    author="simulated_user",
                    position=(
                        random.uniform(-10, 10),
                        random.uniform(-8, 8),
                        random.uniform(-3, 3)
                    ),
                    metadata={
                        "emg_confidence": confidence,
                        "emg_state": state,
                        "emg_timestamp": timestamp
                    }
                )
                
                # Add to thought space
                self.thought_space.add(thought)
                
                # Calculate EMG→thought latency
                emg_latency = (time.time() * 1000) - self._emg_timestamps.get(emg_key, 0)
                self.metrics.add_emg_thought(emg_latency)
                self._thought_timestamps[thought_id] = time.time() * 1000
                
                # Create particle target
                target = SimulationTarget(
                    thought_id=thought_id,
                    position=thought.position,
                    intensity=confidence,
                    hue=self._word_to_hue(word),
                    lifetime=30.0,
                    created_at=time.time()
                )
                self.thought_targets[thought_id] = target
                
                # Callbacks
                if self.on_thought_created:
                    self.on_thought_created(thought)
                if self.on_particle_target:
                    self.on_particle_target(target)
                
                logger.debug(f"Thought created: '{word}' (latency: {emg_latency:.1f}ms)")
    
    def _word_to_hue(self, word: str) -> float:
        """Map word to color hue for visualization."""
        word_hues = {
            "explore": 120,  # Green
            "create": 60,     # Yellow
            "analyze": 240,   # Blue
            "connect": 280,   # Purple
            "focus": 0,       # Red
            "search": 180,    # Cyan
            "build": 30,      # Orange
            "design": 300,    # Magenta
            "optimize": 200,  # Light blue
            "imagine": 320    # Pink
        }
        return word_hues.get(word, random.uniform(0, 360))
    
    async def _update_aether(self) -> None:
        """Update AETHER simulator with thought particle targets."""
        if not self.aether_sim:
            return
        
        # Spawn particles at thought positions
        for thought_id, target in list(self.thought_targets.items()):
            # Calculate thought→particle latency
            if thought_id in self._thought_timestamps:
                particle_latency = (time.time() * 1000) - self._thought_timestamps[thought_id]
                self.metrics.add_thought_particle(particle_latency)
                
                # Calculate total pipeline latency
                emg_key = None
                for key in self._emg_timestamps:
                    if target.thought_id.endswith(key.split('_')[-1]) if '_' in key else False:
                        emg_key = key
                        break
                
                if emg_key:
                    total_latency = (time.time() * 1000) - self._emg_timestamps[emg_key]
                    self.metrics.add_total(total_latency)
            
            # Spawn burst at thought position
            burst_size = int(target.intensity * 50) + 10
            self.aether_sim.spawn_particle_burst(
                count=burst_size,
                position=(target.position[0] * 10 + 150,  # Scale to AETHER volume
                         target.position[1] * 10 + 150,
                         target.position[2] * 10 + 100)
            )
            
            # Swarm behavior toward thought
            self.aether_sim.create_swarm_behavior(
                center=(target.position[0] * 10 + 150,
                       target.position[1] * 10 + 150,
                       target.position[2] * 10 + 100),
                radius=30.0
            )
        
        # Update AETHER
        await self.aether_sim.update(1.0 / 60.0)
    
    async def _update_environment(self) -> None:
        """Get environmental factors from MYCOSENTINEL."""
        if not self.myco_sim:
            return
        
        # Update MYCOSENTINEL
        frame = await self.myco_sim.update(1.0)
        
        if frame and self.on_environment_update:
            # Extract stress factors that might affect thought visualization
            env_data = {
                "timestamp": frame.timestamp,
                "fluorescence": frame.payload.get("fluorescence", 0),
                "growth_rate": frame.payload.get("growth_rate", 0),
                "stress_level": frame.metadata.get("fitness_score", 0),
                "optical_density": frame.payload.get("od600", 0)
            }
            self.on_environment_update(env_data)
    
    async def _handle_client(self, websocket) -> None:
        """Handle WebSocket client connection."""
        self.clients.add(websocket)
        logger.info(f"Client connected. Total: {len(self.clients)}")
        
        try:
            # Send initial state
            await websocket.send(json.dumps({
                "type": "connection_established",
                "data": {
                    "state": self.state.name,
                    "thoughts": len(self.thought_space.thoughts),
                    "targets": len(self.thought_targets),
                    "latency_target_ms": self.target_latency_ms
                }
            }))
            
            # Handle messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._process_client_message(websocket, data)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from client: {message}")
        except Exception as e:
            logger.error(f"Client error: {e}")
        finally:
            self.clients.discard(websocket)
            logger.info(f"Client disconnected. Total: {len(self.clients)}")
    
    async def _process_client_message(self, websocket, data: Dict) -> None:
        """Process message from client."""
        cmd = data.get("command")
        
        if cmd == "get_state":
            await websocket.send(json.dumps({
                "type": "state",
                "data": {
                    "thoughts": self.thought_space.to_dict(),
                    "particles": self.aether_sim.get_particle_cloud() if self.aether_sim else [],
                    "metrics": self.metrics.stats(),
                    "state": self.state.name
                }
            }))
        
        elif cmd == "ping":
            await websocket.send(json.dumps({
                "type": "pong",
                "timestamp": time.time()
            }))
        
        elif cmd == "spawn_thought":
            # Manual thought injection for testing
            text = data.get("text", "test")
            thought = ThoughtNode(
                text=text,
                author="manual",
                position=(
                    data.get("x", 0),
                    data.get("y", 0),
                    data.get("z", 0)
                )
            )
            self.thought_space.add(thought)
            
            target = SimulationTarget(
                thought_id=thought.id,
                position=thought.position,
                intensity=0.9,
                hue=self._word_to_hue(text),
                lifetime=30.0,
                created_at=time.time()
            )
            self.thought_targets[thought.id] = target
    
    async def _broadcast_state(self) -> None:
        """Broadcast current state to all connected clients."""
        if not self.clients:
            return
        
        message = json.dumps({
            "type": "state_update",
            "timestamp": time.time(),
            "data": {
                "thought_count": len(self.thought_space.thoughts),
                "target_count": len(self.thought_targets),
                "particle_count": len(self.aether_sim.particles) if self.aether_sim else 0,
                "metrics": self.metrics.stats()
            }
        })
        
        disconnected = []
        for client in self.clients:
            try:
                await client.send(message)
            except Exception:
                disconnected.append(client)
        
        for client in disconnected:
            self.clients.discard(client)
    
    async def stop(self) -> None:
        """Stop the integration bridge."""
        self.running = False
        logger.info("Stopping Integration Bridge...")
        
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        # Clean up clients
        if self.clients:
            for client in self.clients:
                await client.close()
            self.clients.clear()
        
        logger.info("Integration Bridge stopped")
        logger.info(f"Final metrics: {json.dumps(self.metrics.stats(), indent=2)}")


async def demo():
    """Run integration bridge demo."""
    print("=" * 70)
    print("COGNITIVE-SYNC v1.2: Integration Bridge Demo")
    print("=" * 70)
    print()
    print("Connecting COGNITIVE-SYNC with HARDWARE-SIMULATOR")
    print("Pipeline: EMG → Thought → Particle Target → AETHER Display")
    print("Target Latency: <100ms")
    print()
    
    bridge = IntegrationBridge(ws_port=8765)
    
    # Set up callbacks
    def on_thought(thought):
        print(f"  💭 Thought: '{thought.text}' @ {thought.position}")
    
    def on_target(target):
        print(f"    → Particle target created (intensity: {target.intensity:.2f})")
    
    def on_env(env):
        if env.get("stress_level", 0) > 0.8:
            print(f"  ⚠️  High environmental stress detected")
    
    bridge.on_thought_created = on_thought
    bridge.on_particle_target = on_target
    bridge.on_environment_update = on_env
    
    # Initialize and start
    if await bridge.initialize():
        print("✓ All systems initialized\n")
        print("WebSocket: ws://localhost:8765")
        print("Press Ctrl+C to stop\n")
        
        try:
            await bridge.start()
        except KeyboardInterrupt:
            print("\n--- Stopping ---")
            await bridge.stop()
    else:
        print("✗ Failed to initialize")


if __name__ == "__main__":
    import random
    asyncio.run(demo())
