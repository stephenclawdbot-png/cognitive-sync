"""
COGNITIVE-SYNC v1.2 - SILENT Simulator Bridge
silent_sim_bridge.py - Map simulated EMG signals to thought patterns for testing

This module creates the mapping layer between SILENT EMG/IMU signals
and COGNITIVE-SYNC thought patterns, enabling pre-hardware testing of
the entire thought→visualization pipeline.
"""

import asyncio
import random
import time
import json
import logging
from typing import Dict, List, Optional, Tuple, Callable, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import sys
import numpy as np

# Add paths
HW_SIM_PATH = Path(__file__).parent.parent.parent / "hardware-simulator"
sys.path.insert(0, str(HW_SIM_PATH))
COG_SYNC_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(COG_SYNC_PATH))

from thought_node import ThoughtNode, ThoughtSpace, EmbeddingGenerator

# SILENT phoneme patterns from hardware simulator
SILENT_PHONEMES = [
    'silence', 'p', 'b', 'm', 'f', 'v', 'th', 's', 'sh',
    't', 'd', 'n', 'k', 'g', 'ng', 'a', 'e', 'i', 'o', 'u'
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SilentSimBridge")


class EMGState(Enum):
    """EMG activity states."""
    REST = "rest"
    THINKING = "thinking"
    WORD_DETECTED = "word_detected"
    GESTURE = "gesture"


class ThoughtCategory(Enum):
    """Categories of thoughts for different EMG patterns."""
    SILENT_SPEECH = "silent_speech"
    GESTURE_CONTROL = "gesture_control"
    BIO_FEEDBACK = "bio_feedback"
    SPATIAL_NAV = "spatial_navigation"


@dataclass
class EMGPattern:
    """Defines an EMG signal pattern and its thought mapping."""
    name: str
    phoneme_sequence: List[str]
    muscle_activation: Dict[str, float]  # muscle -> activation level
    duration_ms: float
    confidence_threshold: float
    category: ThoughtCategory
    thought_template: str
    thought_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EMGSignal:
    """Represents processed EMG signal data."""
    channel_id: int
    muscle_group: str
    rms_uv: float  # RMS voltage
    peak_uv: float
    frequency_bands: Dict[str, float]  # low, mid, high power
    timestamp: float


@dataclass 
class ThoughtMapping:
    """Maps an EMG pattern to a generated thought."""
    pattern: EMGPattern
    thought: ThoughtNode
    confidence: float
    trigger_time: float


class EMGPatternLibrary:
    """
    Library of pre-defined EMG patterns for testing.
    
    These patterns simulate different user activities that would
    generate EMG signals on the SILENT device.
    """
    
    PATTERNS = {
        # Silent speech patterns
        "hello_pattern": EMGPattern(
            name="hello_pattern",
            phoneme_sequence=['h', 'e', 'l', 'o'],
            muscle_activation={
                'thyrohyoid': 0.7,
                'geniohyoid': 0.5,
                'orbicularis_oris': 0.3
            },
            duration_ms=800,
            confidence_threshold=0.75,
            category=ThoughtCategory.SILENT_SPEECH,
            thought_template="Hello there!",
            thought_metadata={
                "intent": "greeting",
                "language": "english",
                "formality": "casual"
            }
        ),
        
        "yes_pattern": EMGPattern(
            name="yes_pattern",
            phoneme_sequence=['y', 'e', 's'],
            muscle_activation={
                'platysma': 0.6,
                'mentalis': 0.4
            },
            duration_ms=400,
            confidence_threshold=0.70,
            category=ThoughtCategory.SILENT_SPEECH,
            thought_template="Yes, I agree",
            thought_metadata={
                "intent": "affirmation",
                "sentiment": "positive"
            }
        ),
        
        "no_pattern": EMGPattern(
            name="no_pattern",
            phoneme_sequence=['n', 'o'],
            muscle_activation={
                'platysma': 0.5,
                'orbicularis_oris': 0.6
            },
            duration_ms=350,
            confidence_threshold=0.70,
            category=ThoughtCategory.SILENT_SPEECH,
            thought_template="No, I disagree",
            thought_metadata={
                "intent": "negation",
                "sentiment": "neutral"
            }
        ),
        
        # Gesture control patterns
        "chin_lift": EMGPattern(
            name="chin_lift",
            phoneme_sequence=['silence', 'silence'],
            muscle_activation={
                'mentalis': 0.8,
                'platysma': 0.4
            },
            duration_ms=600,
            confidence_threshold=0.65,
            category=ThoughtCategory.GESTURE_CONTROL,
            thought_template="[Move Up]",
            thought_metadata={
                "intent": "gesture",
                "gesture_type": "chin_lift",
                "action": "navigate_up"
            }
        ),
        
        "jaw_clench": EMGPattern(
            name="jaw_clench",
            phoneme_sequence=['silence', 'silence', 'silence'],
            muscle_activation={
                'masseter': 0.9,  # High activation
                'mentalis': 0.3
            },
            duration_ms=500,
            confidence_threshold=0.80,
            category=ThoughtCategory.GESTURE_CONTROL,
            thought_template="[Select/Confirm]",
            thought_metadata={
                "intent": "gesture",
                "gesture_type": "jaw_clench",
                "action": "select"
            }
        ),
        
        # Bio-feedback patterns
        "deep_breath": EMGPattern(
            name="deep_breath",
            phoneme_sequence=['silence'],
            muscle_activation={
                'thyrohyoid': 0.3,
                'platysma': 0.2
            },
            duration_ms=3000,
            confidence_threshold=0.50,
            category=ThoughtCategory.BIO_FEEDBACK,
            thought_template="[Breathing: Calm]",
            thought_metadata={
                "intent": "bio_feedback",
                "physiological_state": "relaxed",
                "breathing_phase": "inhale"
            }
        ),
        
        "focused_concentration": EMGPattern(
            name="focused_concentration",
            phoneme_sequence=['silence'],
            muscle_activation={
                'mentalis': 0.4,
                'buccinator': 0.3
            },
            duration_ms=2000,
            confidence_threshold=0.55,
            category=ThoughtCategory.BIO_FEEDBACK,
            thought_template="[Focus: High]",
            thought_metadata={
                "intent": "bio_feedback",
                "cognitive_state": "focused",
                "attention_level": "high"
            }
        ),
        
        # Spatial navigation
        "look_left": EMGPattern(
            name="look_left",
            phoneme_sequence=['silence'],
            muscle_activation={
                'sternocleidomastoid_left': 0.7,
                'platysma': 0.3
            },
            duration_ms=400,
            confidence_threshold=0.60,
            category=ThoughtCategory.SPATIAL_NAV,
            thought_template="[Pan Left]",
            thought_metadata={
                "intent": "navigation",
                "direction": "left",
                "action": "pan_view"
            }
        ),
        
        "look_right": EMGPattern(
            name="look_right",
            phoneme_sequence=['silence'],
            muscle_activation={
                'sternocleidomastoid_right': 0.7,
                'platysma': 0.3
            },
            duration_ms=400,
            confidence_threshold=0.60,
            category=ThoughtCategory.SPATIAL_NAV,
            thought_template="[Pan Right]",
            thought_metadata={
                "intent": "navigation",
                "direction": "right",
                "action": "pan_view"
            }
        )
    }
    
    @classmethod
    def get_pattern(cls, name: str) -> Optional[EMGPattern]:
        """Get a pattern by name."""
        return cls.PATTERNS.get(name)
    
    @classmethod
    def get_patterns_by_category(cls, category: ThoughtCategory) -> List[EMGPattern]:
        """Get all patterns in a category."""
        return [p for p in cls.PATTERNS.values() if p.category == category]
    
    @classmethod
    def get_all_patterns(cls) -> List[EMGPattern]:
        """Get all available patterns."""
        return list(cls.PATTERNS.values())


class EMGToThoughtMapper:
    """
    Maps EMG signal features to thought pattern templates.
    
    Uses a combination of:
    - Phoneme recognition patterns
    - Muscle activation signatures
    - Temporal sequence analysis
    - Confidence-based filtering
    """
    
    def __init__(self, pattern_library: EMGPatternLibrary = None):
        self.pattern_library = pattern_library or EMGPatternLibrary()
        
        # Pattern matching weights
        self.phoneme_weight = 0.4
        self.muscle_weight = 0.35
        self.temporal_weight = 0.25
        
        # Current state
        self._phoneme_buffer: List[str] = []
        self._emg_buffer: List[EMGSignal] = []
        self._buffer_duration_ms = 1000
        
        # Callbacks
        self.on_thought_mapped: Optional[Callable[[ThoughtMapping], None]] = None
        
        logger.info("EMGToThoughtMapper initialized")
    
    def process_emg_frame(self, frame_data: Dict) -> Optional[ThoughtMapping]:
        """
        Process an EMG frame and generate thought if pattern matches.
        
        Args:
            frame_data: Raw EMG frame from SILENT simulator
            
        Returns:
            ThoughtMapping if pattern detected, None otherwise
        """
        payload = frame_data.get("payload", {})
        metadata = frame_data.get("metadata", {})
        
        # Extract features
        current_phoneme = payload.get("current_phoneme", "silence")
        activity_level = payload.get("activity_level", 0)
        
        # Get EMG samples
        emg_samples = metadata.get("emg_samples", [])
        
        # Update buffers
        self._phoneme_buffer.append(current_phoneme)
        if len(self._phoneme_buffer) > 20:  # Keep last 20 phonemes
            self._phoneme_buffer = self._phoneme_buffer[-20:]
        
        # Analyze for patterns
        if activity_level < 0.1:
            return None  # Not enough activity
        
        # Find matching pattern
        best_match = self._find_best_pattern(current_phoneme, emg_samples, activity_level)
        
        if best_match and best_match.confidence >= best_match.pattern.confidence_threshold:
            return best_match
        
        return None
    
    def _find_best_pattern(
        self,
        current_phoneme: str,
        emg_samples: List[Dict],
        activity_level: float
    ) -> Optional[ThoughtMapping]:
        """Find the best matching pattern."""
        best_score = 0
        best_pattern = None
        
        # Quick heuristic: check for silence patterns
        if current_phoneme == "silence" and activity_level < 0.2:
            return None
        
        # Score each pattern
        for pattern in self.pattern_library.get_all_patterns():
            score = self._score_pattern(pattern, current_phoneme, emg_samples, activity_level)
            
            if score > best_score:
                best_score = score
                best_pattern = pattern
        
        if best_pattern and best_score > 0.3:  # Minimum threshold
            # Generate thought from pattern
            thought = self._thought_from_pattern(best_pattern, best_score)
            
            return ThoughtMapping(
                pattern=best_pattern,
                thought=thought,
                confidence=best_score,
                trigger_time=time.time()
            )
        
        return None
    
    def _score_pattern(
        self,
        pattern: EMGPattern,
        current_phoneme: str,
        emg_samples: List[Dict],
        activity_level: float
    ) -> float:
        """Score how well current signals match a pattern."""
        scores = []
        
        # Phoneme match
        if current_phoneme in pattern.phoneme_sequence:
            phoneme_score = self.phoneme_weight * 0.8
        elif current_phoneme == "silence" and "silence" in pattern.phoneme_sequence:
            phoneme_score = self.phoneme_weight * 0.5
        else:
            phoneme_score = self.phoneme_weight * 0.1
        scores.append(phoneme_score)
        
        # Muscle activation match (from EMG samples)
        muscle_score = 0
        if emg_samples:
            for sample in emg_samples:
                muscle = sample.get("muscle", "")
                rms = sample.get("rms", 0)
                
                if muscle in pattern.muscle_activation:
                    expected = pattern.muscle_activation[muscle]
                    actual = min(rms / 100, 1.0)  # Normalize
                    muscle_score += 1 - abs(expected - actual)
            
            if pattern.muscle_activation:
                muscle_score = self.muscle_weight * (muscle_score / len(pattern.muscle_activation))
        scores.append(muscle_score)
        
        # Activity level match
        activity_score = self.temporal_weight * activity_level
        scores.append(activity_score)
        
        return sum(scores)
    
    def _thought_from_pattern(self, pattern: EMGPattern, confidence: float) -> ThoughtNode:
        """Generate a thought node from a matched pattern."""
        # Generate slightly varied position based on category
        base_position = self._category_to_position(pattern.category)
        
        # Add some randomness
        position = (
            base_position[0] + random.gauss(0, 0.5),
            base_position[1] + random.gauss(0, 0.5),
            base_position[2] + random.gauss(0, 0.2)
        )
        
        # Generate embedding for semantic similarity
        embedding = EmbeddingGenerator.generate(pattern.thought_template)
        
        # Color based on category
        color = self._category_to_color(pattern.category)
        
        return ThoughtNode(
            text=pattern.thought_template,
            author="silent-user",
            position=position,
            embedding=embedding,
            metadata={
                **pattern.thought_metadata,
                "emg_pattern": pattern.name,
                "emg_state": "word_detected" if confidence > 0.8 else "thinking",
                "confidence": confidence,
                "category": pattern.category.value,
                "color": color,
                "source": "SILENT_EMG"
            }
        )
    
    def _category_to_position(self, category: ThoughtCategory) -> Tuple[float, float, float]:
        """Map category to spatial region."""
        positions = {
            ThoughtCategory.SILENT_SPEECH: (0, 2, 0),      # Center, slightly elevated
            ThoughtCategory.GESTURE_CONTROL: (-5, 0, 0),   # Left side
            ThoughtCategory.BIO_FEEDBACK: (5, 0, 0),      # Right side
            ThoughtCategory.SPATIAL_NAV: (0, -2, 0)       # Lower center
        }
        return positions.get(category, (0, 0, 0))
    
    def _category_to_color(self, category: ThoughtCategory) -> str:
        """Map category to color."""
        colors = {
            ThoughtCategory.SILENT_SPEECH: "#64ffd8",     # Teal
            ThoughtCategory.GESTURE_CONTROL: "#ff64d8",   # Pink
            ThoughtCategory.BIO_FEEDBACK: "#64aaff",      # Blue
            ThoughtCategory.SPATIAL_NAV: "#ffd864"        # Gold
        }
        return colors.get(category, "#ffffff")


class SilentSimConnector:
    """
    Connects to hardware simulator's SILENT device and maps EMG to thoughts.
    
    Runs continuously, processing EMG frames and emitting thought events.
    """
    
    def __init__(self, hardware_ws_uri: str = "ws://localhost:8765"):
        self.hardware_uri = hardware_ws_uri
        self.mapper = EMGToThoughtMapper()
        
        # State
        self._running = False
        self._thought_count = 0
        self._mapping_history: List[ThoughtMapping] = []
        
        # Callbacks
        self.on_thought: Optional[Callable[[ThoughtNode], None]] = None
        self.on_metrics: Optional[Callable[[Dict], None]] = None
        
        logger.info(f"SilentSimConnector initialized for {hardware_uri}")
    
    async def start_simulation_mode(self):
        """Run in standalone simulation mode (no hardware required)."""
        self._running = True
        logger.info("Starting SILENT simulation mode")
        
        while self._running:
            # Simulate EMG data
            await self._simulate_emg_tick()
            await asyncio.sleep(0.1)  # 10Hz simulation
    
    async def _simulate_emg_tick(self):
        """Simulate one tick of EMG data."""
        # Simulate random EMG activity
        if random.random() < 0.3:  # 30% chance of activity
            # Pick a random pattern
            patterns = EMGPatternLibrary.get_all_patterns()
            pattern = random.choice(patterns)
            
            # Simulate frame data
            frame_data = {
                "payload": {
                    "current_phoneme": random.choice(pattern.phoneme_sequence),
                    "activity_level": random.uniform(0.5, 0.95),
                    "detection_confidence": random.uniform(0.7, 0.95)
                },
                "metadata": {
                    "emg_samples": [
                        {
                            "muscle": muscle,
                            "rms": activation * 100
                        }
                        for muscle, activation in pattern.muscle_activation.items()
                    ]
                }
            }
            
            # Process through mapper
            mapping = self.mapper.process_emg_frame(frame_data)
            
            if mapping:
                self._thought_count += 1
                self._mapping_history.append(mapping)
                
                if self.on_thought:
                    self.on_thought(mapping.thought)
                
                logger.debug(f"Mapped thought: {mapping.thought.text} "
                           f"(confidence: {mapping.confidence:.2f})")
    
    def get_stats(self) -> Dict:
        """Get mapping statistics."""
        categories = {}
        for mapping in self._mapping_history:
            cat = mapping.pattern.category.value
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_thoughts_mapped": self._thought_count,
            "unique_patterns_triggered": len(set(
                m.pattern.name for m in self._mapping_history
            )),
            "category_breakdown": categories,
            "avg_confidence": sum(m.confidence for m in self._mapping_history) / max(len(self._mapping_history), 1),
            "run_time": getattr(self, '_run_time', 0)
        }
    
    def stop(self):
        """Stop the connector."""
        self._running = False
        logger.info("SilentSimConnector stopped")


# Demo
async def demo():
    """Demonstrate SILENT EMG to thought mapping."""
    print("=" * 70)
    print("COGNITIVE-SYNC v1.2 - SILENT EMG → Thought Pattern Bridge")
    print("=" * 70)
    print()
    
    print("Available EMG Patterns:")
    for name, pattern in EMGPatternLibrary.PATTERNS.items():
        print(f"  • {name:20} - {pattern.category.value:20} - '{pattern.thought_template}'")
    print()
    
    # Create connector
    connector = SilentSimConnector()
    
    # Set up thought callback
    thoughts_received = []
    
    def on_thought(thought):
        emoji = {
            "silent_speech": "🗣️",
            "gesture_control": "👋",
            "bio_feedback": "🧘",
            "spatial_navigation": "🧭"
        }.get(thought.metadata.get("category", ""), "💭")
        
        print(f"  {emoji} [{thought.metadata.get('category', 'unknown'):20}] "
              f"'{thought.text:25}' "
              f"conf={thought.metadata.get('confidence', 0):.2f}")
        thoughts_received.append(thought)
    
    connector.on_thought = on_thought
    
    print("Simulating EMG signal patterns...")
    print("-" * 70)
    
    # Run simulation for a few seconds
    try:
        await asyncio.wait_for(connector.start_simulation_mode(), timeout=5.0)
    except asyncio.TimeoutError:
        pass
    
    connector.stop()
    
    print("-" * 70)
    print()
    
    # Show stats
    stats = connector.get_stats()
    print("Mapping Statistics:")
    print(f"  Total thoughts mapped: {stats['total_thoughts_mapped']}")
    print(f"  Unique patterns: {stats['unique_patterns_triggered']}")
    print(f"  Average confidence: {stats['avg_confidence']:.2f}")
    print(f"  Category breakdown:")
    for cat, count in stats['category_breakdown'].items():
        print(f"    - {cat}: {count}")
    
    print()
    print("=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demo())
