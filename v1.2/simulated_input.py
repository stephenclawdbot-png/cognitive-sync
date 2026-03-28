"""
COGNITIVE-SYNC v1.2: Simulated Input Module

Converts simulated EMG signals from SILENT_SIMULATOR into COGNITIVE-SYNC thought nodes.
Provides realistic EMG→thought conversion with configurable mappings and thresholds.

Features:
- Multi-user EMG simulation with distinct personas
- Realistic muscle activation patterns
- Configurable word→thought mapping
- Temporal smoothing for natural thought flow
- Integration with thought_node CRDT system
"""

import asyncio
import random
import time
import logging
from typing import Optional, Dict, Any, List, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("simulated_input")

# Add paths for imports
WORKSPACE = Path("/Users/clawdbot/.openclaw/workspace")
SILENT_PATH = WORKSPACE / "SILENT-001" / "firmware"
COGNITIVE_PATH = WORKSPACE / "COGNITIVE-SYNC"

sys.path.insert(0, str(SILENT_PATH))
sys.path.insert(0, str(COGNITIVE_PATH))

from SILENT_SIMULATOR import (
    SilentSimulator, SimulatorConfig, EMGWaveformSimulator,
    SimState
)
from thought_node import ThoughtNode, ThoughtSpace


class EMGPattern(Enum):
    """Types of EMG activation patterns."""
    SUBVOCAL = auto()      # Internal speech muscle activation
    FACIAL = auto()        # Facial muscle patterns
    NECK = auto()          # Neck muscle engagement
    COMBINED = auto()      # Combined multi-channel


@dataclass
class UserPersona:
    """Defines simulated user characteristics."""
    user_id: str
    name: str
    style: str  # analytical, creative, technical, social
    emg_pattern: EMGPattern
    vocabulary: List[str]
    creativity_level: float = 0.5  # 0-1
    response_latency_ms: float = 100.0
    position: Tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))
    color: str = "#64ffd8"
    
    # Movement characteristics
    mobility: float = 1.0  # Movement range
    focus_duration: float = 30.0  # Seconds spent in one area
    cluster_tendency: float = 0.3  # Tendency to cluster thoughts


@dataclass
class ThoughtMapping:
    """Maps EMG signals to thought characteristics."""
    confidence_threshold: float = 0.7
    text_expansion: Dict[str, List[str]] = field(default_factory=dict)
    positional_bias: Optional[Tuple[float, float, float]] = None
    temporal_smoothing_ms: float = 200.0
    max_thoughts_per_second: float = 2.0
    
    def __post_init__(self):
        if not self.text_expansion:
            self.text_expansion = {
                "yes": ["Yes, let's proceed", "Confirmed", "Absolutely"],
                "no": ["No, not now", "Declined", "Let's reconsider"],
                "search": ["Search for solutions", "Explore options", "Find patterns"],
                "create": ["Create new connection", "Generate idea", "Build something"],
                "analyze": ["Analyze data", "Investigate pattern", "Study structure"],
                "connect": ["Connect thoughts", "Link ideas", "Bridge concepts"]
            }


class SimulatedInputManager:
    """
    Manages simulated EMG input for COGNITIVE-SYNC.
    
    Core functions:
    1. Simulate multiple users with EMG devices
    2. Convert EMG states to thought nodes
    3. Apply temporal smoothing for natural flow
    4. Integrate with COGNITIVE-SYNC CRDT system
    """
    
    STYLE_VOCABULARIES = {
        "analytical": [
            "analyze", "data", "pattern", "structure", "optimize",
            "metrics", "verify", "evaluate", "compare", "quantify"
        ],
        "creative": [
            "imagine", "create", "design", "innovate", "inspire",
            "envision", "dream", "compose", "visualize", "concept"
        ],
        "technical": [
            "implement", "code", "build", "deploy", "test",
            "debug", "refactor", "integrate", "compile", "execute"
        ],
        "social": [
            "collaborate", "share", "discuss", "connect", "team",
            "engage", "participate", "support", "communicate", "coordinate"
        ]
    }
    
    STYLE_COLORS = {
        "analytical": "#64ffd8",  # Teal
        "creative": "#ff64d8",     # Pink
        "technical": "#64aaff",    # Blue
        "social": "#ffd864"        # Gold
    }
    
    def __init__(
        self,
        num_users: int = 3,
        mapping: Optional[ThoughtMapping] = None
    ):
        self.num_users = num_users
        self.mapping = mapping or ThoughtMapping()
        
        # User management
        self.personas: Dict[str, UserPersona] = {}
        self.simulators: Dict[str, SilentSimulator] = {}
        self.waveforms: Dict[str, EMGWaveformSimulator] = {}
        
        # Thought space
        self.thought_space = ThoughtSpace()
        
        # Event callbacks
        self.on_thought_created: Optional[Callable[[ThoughtNode, str], None]] = None
        self.on_state_change: Optional[Callable[[str, str, Dict], None]] = None
        
        # Rate limiting
        self._last_thought_time: Dict[str, float] = {}
        self._thought_buffer: Dict[str, List[Dict]] = {}
        
        # Statistics
        self.stats = {
            "emg_events": 0,
            "thoughts_created": 0,
            "words_detected": 0,
            "start_time": None
        }
        
        self.running = False
        
        logger.info(f"SimulatedInputManager initialized for {num_users} users")
    
    def _create_personas(self) -> None:
        """Create distinct user personas."""
        styles = ["analytical", "creative", "technical", "social"]
        patterns = [EMGPattern.SUBVOCAL, EMGPattern.FACIAL, EMGPattern.NECK, EMGPattern.COMBINED]
        names = ["Ada", "Bruno", "Celia", "Diego", "Eva", "Finn"]
        
        for i in range(self.num_users):
            style = styles[i % len(styles)]
            pattern = patterns[i % len(patterns)]
            
            persona = UserPersona(
                user_id=f"user_{i}_{random.randint(1000, 9999)}",
                name=names[i] if i < len(names) else f"User{i}",
                style=style,
                emg_pattern=pattern,
                vocabulary=self.STYLE_VOCABULARIES[style],
                creativity_level=random.uniform(0.3, 0.8),
                response_latency_ms=random.uniform(80, 150),
                position=(
                    random.uniform(-10, 10),
                    random.uniform(-8, 8),
                    random.uniform(-3, 3)
                ),
                color=self.STYLE_COLORS[style],
                mobility=random.uniform(0.5, 2.0),
                focus_duration=random.uniform(20, 60)
            )
            
            self.personas[persona.user_id] = persona
            self._last_thought_time[persona.user_id] = 0
            self._thought_buffer[persona.user_id] = []
            
            logger.info(f"Created persona: {persona.name} ({style}, {pattern.name})")
    
    def _setup_simulators(self) -> None:
        """Initialize EMG simulators for each user."""
        for user_id, persona in self.personas.items():
            config = SimulatorConfig(
                rest_duration_min=1500 + random.randint(-300, 300),
                rest_duration_max=4000 + random.randint(-500, 500),
                thinking_ramp_up_min=200,
                thinking_ramp_up_max=600,
                thinking_duration_min=400,
                thinking_duration_max=1200,
                word_detection_probability=0.6 + persona.creativity_level * 0.3,
                vocabulary=persona.vocabulary,
                add_jitter=True,
                jitter_ms=5
            )
            
            sim = SilentSimulator(config=config, mode="stdout")
            sim.waveform = EMGWaveformSimulator(config)
            
            self.simulators[user_id] = sim
            self.waveforms[user_id] = sim.waveform
    
    async def start(self) -> None:
        """Start simulated input generation."""
        if not self.personas:
            self._create_personas()
            self._setup_simulators()
        
        self.running = True
        self.stats["start_time"] = time.time()
        
        logger.info(f"Starting simulated input for {len(self.personas)} users")
        
        # Start simulators
        for user_id, sim in self.simulators.items():
            sim.waveform.start()
        
        # Run main loop
        await self._simulation_loop()
    
    async def _simulation_loop(self) -> None:
        """Main simulation loop processing EMG for all users."""
        tick_interval = 0.02  # 20ms tick
        
        while self.running:
            for user_id, sim in self.simulators.items():
                persona = self.personas[user_id]
                
                # Tick the waveform simulator
                result = sim.waveform.tick()
                
                if result:
                    state, timestamp, word, confidence = result
                    self.stats["emg_events"] += 1
                    
                    # Update user position
                    persona.position = self._update_position(persona)
                    
                    # Handle state change
                    if self.on_state_change:
                        self.on_state_change(user_id, state, {
                            "confidence": confidence,
                            "position": persona.position
                        })
                    
                    # Process word detection
                    if state == "word_detected" and word:
                        self.stats["words_detected"] += 1
                        await self._process_word(
                            user_id=user_id,
                            word=word,
                            confidence=confidence,
                            timestamp=timestamp,
                            persona=persona
                        )
                    
                    # Process thinking state
                    elif state == "thinking":
                        self._buffer_thinking_activity(user_id, confidence, persona)
            
            await asyncio.sleep(tick_interval)
    
    def _update_position(self, persona: UserPersona) -> Tuple[float, float, float]:
        """Update user's 3D position based on mobility."""
        if persona.mobility <= 0:
            return persona.position
        
        # Random walk with momentum
        delta = (
            random.gauss(0, persona.mobility * 0.5),
            random.gauss(0, persona.mobility * 0.5),
            random.gauss(0, persona.mobility * 0.2)
        )
        
        # Constrain to bounds
        new_pos = (
            max(-15, min(15, persona.position[0] + delta[0])),
            max(-10, min(10, persona.position[1] + delta[1])),
            max(-5, min(5, persona.position[2] + delta[2]))
        )
        
        return new_pos
    
    async def _process_word(
        self,
        user_id: str,
        word: str,
        confidence: float,
        timestamp: float,
        persona: UserPersona
    ) -> None:
        """Convert detected word to thought node."""
        # Rate limiting
        now = time.time()
        min_interval = 1.0 / self.mapping.max_thoughts_per_second
        
        if now - self._last_thought_time.get(user_id, 0) < min_interval:
            return
        
        self._last_thought_time[user_id] = now
        
        # Apply confidence threshold
        if confidence < self.mapping.confidence_threshold:
            logger.debug(f"Word '{word}' below confidence threshold ({confidence:.2f})")
            return
        
        # Expand text based on mapping
        text = self._expand_text(word, persona)
        
        # Create thought node
        thought = ThoughtNode(
            text=text,
            author=user_id,
            position=persona.position,
            metadata={
                "emg_word": word,
                "emg_confidence": confidence,
                "user_name": persona.name,
                "style": persona.style,
                "color": persona.color,
                "emg_pattern": persona.emg_pattern.name,
                "timestamp_ms": timestamp
            }
        )
        
        # Add to thought space
        self.thought_space.add(thought)
        self.stats["thoughts_created"] += 1
        
        # Callback
        if self.on_thought_created:
            self.on_thought_created(thought, user_id)
        
        logger.debug(f"Created thought for {persona.name}: '{text}'")
    
    def _expand_text(self, word: str, persona: UserPersona) -> str:
        """Expand simple word into richer thought text."""
        # Get expansions for this word
        expansions = self.mapping.text_expansion.get(word.lower(), [word])
        
        # Add persona-specific flair
        if persona.style == "creative" and random.random() < persona.creativity_level:
            # Creative users get more varied text
            return random.choice(expansions)
        
        return expansions[0] if expansions else word
    
    def _buffer_thinking_activity(
        self,
        user_id: str,
        confidence: float,
        persona: UserPersona
    ) -> None:
        """Buffer thinking activity for temporal smoothing."""
        buffer = self._thought_buffer[user_id]
        buffer.append({
            "confidence": confidence,
            "position": persona.position,
            "timestamp": time.time()
        })
        
        # Keep only recent buffer
        cutoff = time.time() - (self.mapping.temporal_smoothing_ms / 1000)
        buffer[:] = [b for b in buffer if b["timestamp"] > cutoff]
    
    def get_all_thoughts(self) -> List[ThoughtNode]:
        """Get all generated thoughts."""
        return self.thought_space.all_thoughts()
    
    def get_user_thoughts(self, user_id: str) -> List[ThoughtNode]:
        """Get thoughts for specific user."""
        return [
            t for t in self.thought_space.all_thoughts()
            if t.author == user_id
        ]
    
    def get_thoughts_near(
        self,
        position: Tuple[float, float, float],
        radius: float
    ) -> List[ThoughtNode]:
        """Get thoughts near a position."""
        return self.thought_space.get_nearby(position, radius)
    
    def export_state(self) -> Dict[str, Any]:
        """Export current state for persistence."""
        return {
            "personas": {
                uid: {
                    "name": p.name,
                    "style": p.style,
                    "color": p.color,
                    "position": p.position
                }
                for uid, p in self.personas.items()
            },
            "thoughts": self.thought_space.to_dict(),
            "stats": self.stats
        }
    
    async def stop(self) -> None:
        """Stop simulation."""
        self.running = False
        logger.info("SimulatedInputManager stopped")
        logger.info(f"Stats: {self.stats}")


async def demo():
    """Run simulated input demo."""
    print("=" * 70)
    print("COGNITIVE-SYNC v1.2: Simulated Input Demo")
    print("=" * 70)
    print()
    print("Simulating EMG → Thought conversion:")
    print("3 users with different cognitive styles:")
    print("  • Analytical (subvocal EMG pattern)")
    print("  • Creative (facial EMG pattern)")
    print("  • Technical (neck EMG pattern)")
    print()
    print("Press Ctrl+C to stop\n")
    
    manager = SimulatedInputManager(num_users=3)
    
    # Track latency
    emg_times: Dict[str, float] = {}
    
    def on_thought(thought, user_id):
        persona = manager.personas[user_id]
        latency = 0
        if user_id in emg_times:
            latency = (time.time() - emg_times[user_id]) * 1000
        
        print(f"  [{persona.name:8}] 💭 {thought.text[:40]:40} "
              f"@ ({thought.position[0]:5.1f}, {thought.position[1]:5.1f}) "
              f"[{latency:5.1f}ms]")
    
    def on_state(user_id, state, props):
        if state == "word_detected":
            emg_times[user_id] = time.time()
    
    manager.on_thought_created = on_thought
    manager.on_state_change = on_state
    
    try:
        await manager.start()
    except KeyboardInterrupt:
        print("\n--- Stopping ---")
        await manager.stop()
        
        print(f"\n{'='*70}")
        print("Summary:")
        print(f"  EMG events: {manager.stats['emg_events']}")
        print(f"  Words detected: {manager.stats['words_detected']}")
        print(f"  Thoughts created: {manager.stats['thoughts_created']}")
        print(f"{'='*70}")


if __name__ == "__main__":
    asyncio.run(demo())
