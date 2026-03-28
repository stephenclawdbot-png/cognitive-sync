"""
COGNITIVE-SYNC v1.1: Thought Simulator

Integrates SILENT_SIMULATOR for synthetic EMG→thought data generation.
Maps EMG states (rest, thinking, word_detected) to spatial thought nodes.
Supports multiple simulated users with distinct thought patterns.
"""

import asyncio
import random
import time
import json
import logging
from typing import Optional, Dict, List, Callable, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import sys

# Add SILENT-001 to path
SILENT_PATH = Path(__file__).parent.parent.parent / "SILENT-001" / "firmware"
sys.path.insert(0, str(SILENT_PATH))

from SILENT_SIMULATOR import SilentSimulator, SimulatorConfig, EMGWaveformSimulator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("thought_simulator")


@dataclass
class VirtualUser:
    """Represents a simulated user with unique thought patterns."""
    user_id: str
    name: str
    color: str
    position: Tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))
    
    # Personal vocabulary and thought style
    vocabulary: List[str] = field(default_factory=list)
    thought_style: str = "analytical"  # analytical, creative, technical, social
    
    # Spatial movement parameters
    mobility: float = 1.0  # How much they move around 3D space
    cluster_tendency: float = 0.5  # Tendency to group thoughts
    
    def __post_init__(self):
        if not self.vocabulary:
            self.vocabulary = self._generate_vocabulary()
    
    def _generate_vocabulary(self) -> List[str]:
        """Generate vocabulary based on thought style."""
        vocabularies = {
            "analytical": [
                "analyze", "data", "pattern", "logic", "structure",
                "system", "optimize", "efficiency", "metrics", "solution"
            ],
            "creative": [
                "imagine", "create", "design", "inspire", "beauty",
                "art", "vision", "concept", "innovate", "dream"
            ],
            "technical": [
                "code", "build", "debug", "implement", "function",
                "algorithm", "interface", "architecture", "deploy", "test"
            ],
            "social": [
                "connect", "share", "collaborate", "community", "team",
                "support", "discuss", "meet", "engage", "network"
            ]
        }
        return vocabularies.get(self.thought_style, vocabularies["analytical"])
    
    def get_next_position(self, current: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Generate next position based on mobility."""
        if self.mobility <= 0:
            return current
        
        # Random walk with momentum
        delta = (
            random.gauss(0, self.mobility * 2),
            random.gauss(0, self.mobility * 2),
            random.gauss(0, self.mobility * 0.5)  # Less Z movement
        )
        
        # Constrain to reasonable bounds
        new_pos = (
            max(-15, min(15, current[0] + delta[0])),
            max(-10, min(10, current[1] + delta[1])),
            max(-5, min(5, current[2] + delta[2]))
        )
        return new_pos


@dataclass
class SimulatedThought:
    """A thought generated from EMG simulation."""
    thought_id: str
    user_id: str
    text: str
    emg_state: str  # rest, thinking, word_detected
    confidence: float
    position: Tuple[float, float, float]
    timestamp: float
    color: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class ThoughtSimulator:
    """
    Main simulator that bridges SILENT EMG simulator to 3D thought space.
    
    Features:
    - Multiple virtual users with distinct behaviors
    - EMG state → thought mapping
    - Real-time spatial visualization data
    - Thought persistence and replay
    """
    
    # EMG state → visual properties mapping
    STATE_PROPERTIES = {
        "rest": {
            "glow_intensity": 0.2,
            "pulse_rate": 0.5,
            "color_shift": "cool",
            "size_multiplier": 0.8,
            "label": ""
        },
        "thinking": {
            "glow_intensity": 0.6,
            "pulse_rate": 2.0,
            "color_shift": "warm",
            "size_multiplier": 1.0,
            "label": "Thinking..."
        },
        "word_detected": {
            "glow_intensity": 1.0,
            "pulse_rate": 4.0,
            "color_shift": "bright",
            "size_multiplier": 1.3,
            "label": "Word!"
        }
    }
    
    def __init__(self, num_users: int = 3):
        self.num_users = num_users
        self.users: Dict[str, VirtualUser] = {}
        self.user_simulators: Dict[str, SilentSimulator] = {}
        self.user_positions: Dict[str, Tuple[float, float, float]] = {}
        self.user_states: Dict[str, str] = {}
        
        # Event callbacks
        self.on_thought_created: Optional[Callable[[SimulatedThought], None]] = None
        self.on_state_changed: Optional[Callable[[str, str, Dict], None]] = None
        self.on_user_moved: Optional[Callable[[str, Tuple], None]] = None
        
        # Persistence
        self.thought_history: List[SimulatedThought] = []
        self.max_history = 10000
        
        # Stats
        self.stats = {
            "thoughts_generated": 0,
            "words_detected": 0,
            "start_time": None
        }
        
        self.running = False
        self._setup_virtual_users()
    
    def _setup_virtual_users(self) -> None:
        """Create virtual users with different personas."""
        styles = ["analytical", "creative", "technical", "social"]
        colors = ["#64ffd8", "#ff64d8", "#64aaff", "#ffd864"]
        names = ["Alice", "Bob", "Charlie", "Diana"]
        
        for i in range(min(self.num_users, len(styles))):
            user_id = f"user_{i}_{random.randint(1000, 9999)}"
            
            user = VirtualUser(
                user_id=user_id,
                name=names[i],
                color=colors[i],
                position=(
                    random.uniform(-10, 10),
                    random.uniform(-8, 8),
                    random.uniform(-3, 3)
                ),
                thought_style=styles[i],
                mobility=random.uniform(0.5, 2.0),
                cluster_tendency=random.uniform(0.3, 0.8)
            )
            
            self.users[user_id] = user
            self.user_positions[user_id] = user.position
            self.user_states[user_id] = "rest"
            
            # Create simulator config per user
            config = SimulatorConfig(
                rest_duration_min=1500 + random.randint(-500, 500),
                rest_duration_max=4000 + random.randint(-1000, 1000),
                thinking_ramp_up_min=200 + random.randint(-100, 100),
                thinking_ramp_up_max=600 + random.randint(-200, 200),
                thinking_duration_min=400 + random.randint(-100, 200),
                thinking_duration_max=1200 + random.randint(-300, 300),
                word_detection_probability=0.7 + random.uniform(-0.2, 0.2),
                vocabulary=user.vocabulary,
                add_jitter=True
            )
            
            # Initialize waveform simulator
            sim = SilentSimulator(config=config, mode="stdout")
            sim.waveform = EMGWaveformSimulator(config)
            self.user_simulators[user_id] = sim
            
            logger.info(f"Created virtual user: {user.name} ({user.thought_style})")
    
    async def start(self) -> None:
        """Start the simulation for all users."""
        self.running = True
        self.stats["start_time"] = time.time()
        
        logger.info(f"Starting ThoughtSimulator with {len(self.users)} users")
        
        # Initialize all simulators
        for user_id, sim in self.user_simulators.items():
            sim.waveform.start()
        
        # Run simulation loop
        await self._simulation_loop()
    
    async def _simulation_loop(self) -> None:
        """Main simulation loop - ticks all user simulators."""
        tick_interval = 0.05  # 50ms tick
        
        while self.running:
            for user_id, sim in self.user_simulators.items():
                user = self.users[user_id]
                
                # Tick the EMG simulator
                result = sim.waveform.tick()
                
                if result:
                    state, timestamp, word, confidence = result
                    
                    # Update position based on mobility
                    current_pos = self.user_positions[user_id]
                    new_pos = user.get_next_position(current_pos)
                    if new_pos != current_pos:
                        self.user_positions[user_id] = new_pos
                        if self.on_user_moved:
                            self.on_user_moved(user_id, new_pos)
                    
                    # Handle state change
                    if state != self.user_states[user_id]:
                        self.user_states[user_id] = state
                        props = self.STATE_PROPERTIES.get(state, {})
                        if self.on_state_changed:
                            self.on_state_changed(user_id, state, props)
                    
                    # Create thought based on state
                    if state == "word_detected" and word:
                        thought = self._create_thought(
                            user_id=user_id,
                            text=word,
                            emg_state=state,
                            confidence=confidence,
                            position=self.user_positions[user_id]
                        )
                        self.stats["words_detected"] += 1
                        
                        if self.on_thought_created:
                            self.on_thought_created(thought)
                    
                    elif state == "thinking":
                        # Create ephemeral "thinking" thought
                        thought = self._create_thought(
                            user_id=user_id,
                            text="...",
                            emg_state=state,
                            confidence=0.5,
                            position=self.user_positions[user_id],
                            ephemeral=True
                        )
                        
                        if self.on_thought_created:
                            self.on_thought_created(thought)
                
                # Random movement updates (even without state change)
                if random.random() < 0.1:  # 10% chance per tick
                    current_pos = self.user_positions[user_id]
                    new_pos = user.get_next_position(current_pos)
                    self.user_positions[user_id] = new_pos
                    if self.on_user_moved:
                        self.on_user_moved(user_id, new_pos)
            
            await asyncio.sleep(tick_interval)
    
    def _create_thought(
        self,
        user_id: str,
        text: str,
        emg_state: str,
        confidence: float,
        position: Tuple[float, float, float],
        ephemeral: bool = False
    ) -> SimulatedThought:
        """Create a new simulated thought."""
        user = self.users[user_id]
        thought_id = f"thought_{int(time.time() * 1000)}_{user_id}_{random.randint(1000, 9999)}"
        
        props = self.STATE_PROPERTIES.get(emg_state, {})
        
        thought = SimulatedThought(
            thought_id=thought_id,
            user_id=user_id,
            text=text,
            emg_state=emg_state,
            confidence=confidence,
            position=position,
            timestamp=time.time(),
            color=user.color,
            metadata={
                "user_name": user.name,
                "thought_style": user.thought_style,
                "glow_intensity": props.get("glow_intensity", 0.5),
                "pulse_rate": props.get("pulse_rate", 1.0),
                "size_multiplier": props.get("size_multiplier", 1.0),
                "ephemeral": ephemeral,
                "label": props.get("label", "")
            }
        )
        
        self.thought_history.append(thought)
        if len(self.thought_history) > self.max_history:
            self.thought_history = self.thought_history[-self.max_history:]
        
        self.stats["thoughts_generated"] += 1
        
        return thought
    
    def get_thoughts_in_range(
        self,
        center: Tuple[float, float, float],
        radius: float
    ) -> List[SimulatedThought]:
        """Get thoughts within spatial range."""
        in_range = []
        cx, cy, cz = center
        
        for thought in reversed(self.thought_history):
            tx, ty, tz = thought.position
            dist = ((tx - cx) ** 2 + (ty - cy) ** 2 + (tz - cz) ** 2) ** 0.5
            if dist <= radius:
                in_range.append(thought)
        
        return in_range
    
    def get_user_positions(self) -> Dict[str, Dict]:
        """Get current positions of all users."""
        return {
            user_id: {
                "position": self.user_positions[user_id],
                "state": self.user_states[user_id],
                "name": self.users[user_id].name,
                "color": self.users[user_id].color
            }
            for user_id in self.users
        }
    
    def get_replay_data(
        self,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> List[Dict]:
        """Get thought history for replay."""
        filtered = self.thought_history
        
        if start_time:
            filtered = [t for t in filtered if t.timestamp >= start_time]
        if end_time:
            filtered = [t for t in filtered if t.timestamp <= end_time]
        
        return [{
            "thought_id": t.thought_id,
            "user_id": t.user_id,
            "text": t.text,
            "emg_state": t.emg_state,
            "confidence": t.confidence,
            "position": t.position,
            "timestamp": t.timestamp,
            "color": t.color,
            "metadata": t.metadata
        } for t in filtered]
    
    def export_session(self, filepath: str) -> None:
        """Export simulation session to file."""
        data = {
            "export_time": time.time(),
            "stats": self.stats,
            "users": {
                uid: {
                    "name": u.name,
                    "style": u.thought_style,
                    "color": u.color
                }
                for uid, u in self.users.items()
            },
            "thoughts": self.get_replay_data()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported session to {filepath}")
    
    async def stop(self) -> None:
        """Stop the simulation."""
        self.running = False
        logger.info("ThoughtSimulator stopped")
        logger.info(f"Stats: {self.stats}")


async def demo():
    """Run interactive demonstration."""
    print("=" * 70)
    print("COGNITIVE-SYNC v1.1: Thought Simulator Demo")
    print("=" * 70)
    print()
    print("Simulating EMG → Thought mapping with 3 virtual users:")
    print("  • Alice (analytical) - Blue-green")
    print("  • Bob (creative) - Pink")
    print("  • Charlie (technical) - Light blue")
    print()
    print("Each user's EMG activity creates thoughts in 3D space")
    print("-" * 70)
    print()
    
    simulator = ThoughtSimulator(num_users=3)
    
    def on_thought(thought: SimulatedThought):
        user = simulator.users[thought.user_id]
        emoji = {"rest": "💤", "thinking": "💭", "word_detected": "✨"}.get(
            thought.emg_state, "❓"
        )
        print(f"  [{user.name:8}] {emoji} '{thought.text:15}' "
              f"@ ({thought.position[0]:5.1f}, {thought.position[1]:5.1f}, {thought.position[2]:4.1f}) "
              f"conf={thought.confidence:.2f}")
    
    def on_state_change(user_id: str, state: str, props: Dict):
        user = simulator.users[user_id]
        print(f"  [{user.name:8}] State: {state.upper()}")
    
    simulator.on_thought_created = on_thought
    simulator.on_state_changed = on_state_change
    
    try:
        await simulator.start()
    except KeyboardInterrupt:
        print("\n--- Stopping simulation ---")
        await simulator.stop()
        
        # Export session
        simulator.export_session("demo_session.json")
        print(f"\nSession exported to demo_session.json")
        print(f"Total thoughts: {simulator.stats['thoughts_generated']}")
        print(f"Words detected: {simulator.stats['words_detected']}")


if __name__ == "__main__":
    asyncio.run(demo())
