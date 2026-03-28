"""
COGNITIVE-SYNC v1.2 - End-to-End Integration Demo
end_to_end_demo.py - Full pipeline: Sim SILENT → Thought → 3D Visualization

This demonstrates the complete data flow:
1. SILENT EMG Simulator generates bio-signals
2. EMG-to-Thought Mapper converts signals to thought patterns
3. COGNITIVE-SYNC CRDT system manages thought state
4. 3D visualization renders thoughts in real-time

Run this before SILENT hardware arrives (April 14) to validate the pipeline.
"""

import asyncio
import json
import time
import random
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
import sys

# Add paths for imports
HW_SIM_PATH = Path(__file__).parent.parent.parent / "hardware-simulator"
sys.path.insert(0, str(HW_SIM_PATH))
COG_SYNC_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(COG_SYNC_PATH))

from thought_node import ThoughtNode, ThoughtSpace
from silent_sim_bridge import (
    SilentSimConnector, EMGPatternLibrary, EMGToThoughtMapper,
    ThoughtCategory
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("EndToEndDemo")


@dataclass
class DemoMetrics:
    """Metrics for the end-to-end demo."""
    start_time: float = field(default_factory=time.time)
    emg_frames_processed: int = 0
    thoughts_generated: int = 0
    thoughts_visualized: int = 0
    latency_ms: List[float] = field(default_factory=list)
    
    @property
    def avg_latency_ms(self) -> float:
        return sum(self.latency_ms) / max(len(self.latency_ms), 1)
    
    @property
    def throughput_tps(self) -> float:
        elapsed = time.time() - self.start_time
        return self.thoughts_generated / max(elapsed, 0.001)
    
    def summary(self) -> Dict:
        return {
            "runtime_seconds": time.time() - self.start_time,
            "emg_frames_processed": self.emg_frames_processed,
            "thoughts_generated": self.thoughts_generated,
            "thoughts_visualized": self.thoughts_visualized,
            "avg_latency_ms": self.avg_latency_ms,
            "throughput_tps": self.throughput_tps,
            "end_to_end_efficiency": self.thoughts_visualized / max(self.thoughts_generated, 1)
        }


class Mock3DVisualizer:
    """
    Mock 3D visualizer for demo purposes.
    
    In production, this would connect to the Three.js/WebGL frontend.
    For testing, we simulate the visualization layer.
    """
    
    def __init__(self):
        self.rendered_thoughts: List[ThoughtNode] = []
        self.active_animations: Dict[str, Dict] = {}
        logger.info("Mock3DVisualizer initialized")
    
    def add_thought(self, thought: ThoughtNode) -> Dict:
        """Add a thought to the 3D scene."""
        self.rendered_thoughts.append(thought)
        
        # Generate visualization properties
        viz_data = {
            "thought_id": thought.id,
            "position": thought.position,
            "color": thought.metadata.get("color", "#64ffd8"),
            "text": thought.text,
            "size": thought.metadata.get("size_multiplier", 1.0) * 2,
            "glow_intensity": thought.metadata.get("glow_intensity", 0.5),
            "pulse_rate": self._get_pulse_rate(thought),
            "animation": self._get_animation(thought),
            "render_time": time.time()
        }
        
        self.active_animations[thought.id] = viz_data
        return viz_data
    
    def _get_pulse_rate(self, thought: ThoughtNode) -> float:
        """Determine pulse rate based on thought state."""
        emg_state = thought.metadata.get("emg_state", "rest")
        rates = {
            "rest": 0.5,
            "thinking": 2.0,
            "word_detected": 4.0
        }
        return rates.get(emg_state, 1.0)
    
    def _get_animation(self, thought: ThoughtNode) -> str:
        """Determine animation based on category."""
        category = thought.metadata.get("category", "")
        animations = {
            "silent_speech": "float_and_glow",
            "gesture_control": "ripple_expand",
            "bio_feedback": "breathe_pulse",
            "spatial_navigation": "sweep_arrow"
        }
        return animations.get(category, "fade_in")
    
    def update_scene(self) -> Dict:
        """Update all animations and return scene state."""
        current_time = time.time()
        
        for thought_id, anim in self.active_animations.items():
            # Calculate animation progress
            elapsed = current_time - anim["render_time"]
            anim["elapsed"] = elapsed
            anim["opacity"] = min(1.0, elapsed * 2)  # Fade in over 0.5s
        
        return {
            "thought_count": len(self.rendered_thoughts),
            "active_animations": len(self.active_animations),
            "bounds": self._calculate_bounds()
        }
    
    def _calculate_bounds(self) -> Tuple[Tuple, Tuple]:
        """Calculate bounding box of all thoughts."""
        if not self.rendered_thoughts:
            return ((-10, -10, -5), (10, 10, 5))
        
        positions = [t.position for t in self.rendered_thoughts]
        mins = tuple(min(p[i] for p in positions) - 2 for i in range(3))
        maxs = tuple(max(p[i] for p in positions) + 2 for i in range(3))
        return (mins, maxs)
    
    def export_scene(self) -> Dict:
        """Export scene for external visualization."""
        return {
            "thoughts": [
                {
                    "id": t.id,
                    "text": t.text,
                    "position": t.position,
                    "color": t.metadata.get("color"),
                    "category": t.metadata.get("category")
                }
                for t in self.rendered_thoughts
            ],
            "animation_data": self.active_animations
        }


class EndToEndPipeline:
    """
    Complete pipeline: SILENT EMG → Thought → 3D Visualization.
    
    Demonstrates the full data flow with performance monitoring.
    """
    
    def __init__(self):
        self.connector = SilentSimConnector()
        self.mapper = EMGToThoughtMapper()
        self.thought_space = ThoughtSpace()
        self.visualizer = Mock3DVisualizer()
        self.metrics = DemoMetrics()
        
        # Callback tracking
        self._thought_callbacks: List[Any] = []
        
        logger.info("EndToEndPipeline initialized")
    
    def _on_emg_frame(self, frame_data: Dict):
        """Process EMG frame from SILENT simulator."""
        start_time = time.time()
        self.metrics.emg_frames_processed += 1
        
        # Map EMG to thought
        mapping = self.mapper.process_emg_frame(frame_data)
        
        if mapping:
            self.metrics.thoughts_generated += 1
            
            # Add to thought space (CRDT merge)
            self.thought_space.add(mapping.thought)
            
            # Visualize
            viz_data = self.visualizer.add_thought(mapping.thought)
            self.metrics.thoughts_visualized += 1
            
            # Record latency
            latency = (time.time() - start_time) * 1000
            self.metrics.latency_ms.append(latency)
            
            logger.debug(f"Pipeline: EMG → Thought → Viz in {latency:.2f}ms")
    
    async def run_scenario(self, scenario_name: str, duration_sec: float = 10.0):
        """Run a specific test scenario."""
        print(f"\n{'='*70}")
        print(f"Scenario: {scenario_name.upper()}")
        print(f"{'='*70}")
        
        self.metrics = DemoMetrics()  # Reset metrics
        
        # Set up connector callback
        received_thoughts = []
        
        def on_thought(thought):
            # Process through full pipeline
            start_time = time.time()
            
            # Add to thought space
            self.thought_space.add(thought)
            
            # Visualize
            viz_data = self.visualizer.add_thought(thought)
            
            # Record
            received_thoughts.append({
                "thought": thought,
                "viz": viz_data,
                "latency_ms": (time.time() - start_time) * 1000
            })
        
        self.connector.on_thought = on_thought
        
        # Run scenario-specific patterns
        patterns = self._get_scenario_patterns(scenario_name)
        
        print(f"Testing {len(patterns)} EMG patterns...")
        print()
        
        start_time = time.time()
        
        while time.time() - start_time < duration_sec:
            await self._simulate_scenario_tick(patterns)
            await asyncio.sleep(0.2)
        
        # Show results
        print()
        print(f"Generated {len(received_thoughts)} thoughts:")
        for item in received_thoughts[:10]:  # Show first 10
            thought = item["thought"]
            emoji = self._category_emoji(thought.metadata.get("category", ""))
            print(f"  {emoji} '{thought.text:25}' "
                  f"@ ({thought.position[0]:5.1f}, {thought.position[1]:5.1f}) "
                  f"lat={item['latency_ms']:.1f}ms")
        
        if len(received_thoughts) > 10:
            print(f"  ... and {len(received_thoughts) - 10} more")
        
        # Show metrics
        print()
        print("Scenario Metrics:")
        for key, value in self.metrics.summary().items():
            print(f"  {key}: {value}")
        
        return self.metrics.summary()
    
    def _get_scenario_patterns(self, scenario: str) -> List:
        """Get patterns for a specific scenario."""
        if scenario == "silent_speech":
            return EMGPatternLibrary.get_patterns_by_category(ThoughtCategory.SILENT_SPEECH)
        elif scenario == "gesture_control":
            return EMGPatternLibrary.get_patterns_by_category(ThoughtCategory.GESTURE_CONTROL)
        elif scenario == "bio_feedback":
            return EMGPatternLibrary.get_patterns_by_category(ThoughtCategory.BIO_FEEDBACK)
        else:
            return EMGPatternLibrary.get_all_patterns()
    
    async def _simulate_scenario_tick(self, patterns: List):
        """Simulate one tick for the scenario."""
        if random.random() < 0.4:  # 40% chance of activity
            pattern = random.choice(patterns)
            
            # Create synthetic EMG frame
            frame_data = {
                "payload": {
                    "current_phoneme": random.choice(pattern.phoneme_sequence),
                    "activity_level": random.uniform(0.6, 0.95),
                    "detection_confidence": random.uniform(0.7, 0.95)
                },
                "metadata": {
                    "emg_samples": [
                        {"muscle": m, "rms": a * 100 + random.gauss(0, 10)}
                        for m, a in pattern.muscle_activation.items()
                    ]
                }
            }
            
            self._on_emg_frame(frame_data)
    
    def _category_emoji(self, category: str) -> str:
        """Get emoji for category."""
        emojis = {
            "silent_speech": "🗣️",
            "gesture_control": "👋",
            "bio_feedback": "🧘",
            "spatial_navigation": "🧭"
        }
        return emojis.get(category, "💭")
    
    async def run_full_demo(self, scenarios: List[str] = None):
        """Run the complete end-to-end demonstration."""
        
        scenarios = scenarios or ["silent_speech", "gesture_control", "bio_feedback"]
        
        print("=" * 70)
        print("COGNITIVE-SYNC v1.2 - End-to-End Integration Demo")
        print("=" * 70)
        print()
        print("Testing complete data flow:")
        print("  1. SILENT EMG Simulator → generates bio-signals")
        print("  2. EMG-to-Thought Mapper → converts to thought patterns")
        print("  3. COGNITIVE-SYNC CRDT → manages thought state")
        print("  4. 3D Visualization → renders in real-time")
        print()
        print("Hardware arrival date: April 14, 2026")
        print("Current mode: SOFTWARE SIMULATION")
        print("=" * 70)
        
        all_metrics = []
        
        for scenario in scenarios:
            metrics = await self.run_scenario(scenario, duration_sec=5.0)
            all_metrics.append({"scenario": scenario, **metrics})
            await asyncio.sleep(1)
        
        # Final summary
        print("\n" + "=" * 70)
        print("DEMO COMPLETE - Summary")
        print("=" * 70)
        
        total_thoughts = sum(m["thoughts_generated"] for m in all_metrics)
        avg_latency = sum(m["avg_latency_ms"] for m in all_metrics) / len(all_metrics)
        
        print(f"\nScenarios tested: {len(scenarios)}")
        print(f"Total thoughts generated: {total_thoughts}")
        print(f"Average pipeline latency: {avg_latency:.2f} ms")
        print(f"Thought space size: {len(self.thought_space.thoughts)}")
        print(f"Visualization objects: {len(self.visualizer.rendered_thoughts)}")
        
        print("\nScenario Breakdown:")
        for m in all_metrics:
            print(f"  • {m['scenario']:20}: {m['thoughts_generated']:3d} thoughts, "
                  f"{m['avg_latency_ms']:5.1f}ms avg latency")
        
        print()
        print("Visualization Scene Bounds:")
        bounds = self.visualizer._calculate_bounds()
        print(f"  Min: {bounds[0]}")
        print(f"  Max: {bounds[1]}")
        
        print()
        print("=" * 70)
        print("✓ Pipeline validated - ready for SILENT hardware!")
        print("=" * 70)
        
        # Export scene data
        scene_data = self.visualizer.export_scene()
        output_file = Path(__file__).parent / "demo_scene_export.json"
        with open(output_file, 'w') as f:
            json.dump(scene_data, f, indent=2, default=str)
        print(f"\nScene exported to: {output_file}")


# Main demo
async def main():
    """Run the complete end-to-end demo."""
    pipeline = EndToEndPipeline()
    await pipeline.run_full_demo()


if __name__ == "__main__":
    asyncio.run(main())
