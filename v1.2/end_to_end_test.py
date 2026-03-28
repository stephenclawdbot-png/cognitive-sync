"""
COGNITIVE-SYNC v1.2: End-to-End Integration Test

Complete pipeline test: Simulated EMG → Thought Node → Visualization → AETHER Display

Test Coverage:
1. EMG signal generation via SILENT_SIMULATOR
2. Thought conversion via thought_node CRDT
3. Particle target generation
4. AETHER volumetric display simulation
5. Latency validation (<100ms requirement)
6. MYCOSENTINEL environmental integration
"""

import asyncio
import json
import time
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict

# Setup paths
WORKSPACE = Path("/Users/clawdbot/.openclaw/workspace")
COGNITIVE_PATH = WORKSPACE / "COGNITIVE-SYNC"
SILENT_PATH = WORKSPACE / "SILENT-001" / "firmware"
HARDWARE_PATH = WORKSPACE / "hardware-simulator"

sys.path.insert(0, str(COGNITIVE_PATH))
sys.path.insert(0, str(SILENT_PATH))
sys.path.insert(0, str(HARDWARE_PATH))

from integration_bridge import IntegrationBridge, LatencyMetrics, SimulationTarget
from simulated_input import SimulatedInputManager, ThoughtMapping
from thought_to_simulation import ThoughtGraphConverter, RealtimeThoughtExporter
from thought_node import ThoughtNode, ThoughtSpace
from aether_sim import AetherSimulator
from mycosentinel_sim import MycosentinelSimulator
from SILENT_SIMULATOR import SilentSimulator, SimulatorConfig


@dataclass
class TestResult:
    """Result of a single test."""
    name: str
    passed: bool
    latency_ms: float
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class PipelineStage:
    """Metrics for a pipeline stage."""
    name: str
    start_time: float
    end_time: Optional[float] = None
    
    @property
    def latency_ms(self) -> float:
        if self.end_time is None:
            return (time.time() * 1000) - self.start_time
        return self.end_time - self.start_time
    
    def complete(self):
        self.end_time = time.time() * 1000


class EndToEndPipeline:
    """
    Complete end-to-end pipeline for testing.
    
    Pipeline Stages:
    1. EMG Generation (SILENT_SIMULATOR)
    2. Thought Creation (COGNITIVE-SYNC thought_node)
    3. Thought-to-Particle Conversion
    4. AETHER Display Simulation
    5. MYCOSENTINEL Environment Check
    """
    
    TARGET_LATENCY_MS = 100.0
    
    def __init__(self):
        # Subsystems
        self.input_manager: Optional[SimulatedInputManager] = None
        self.thought_space = ThoughtSpace()
        self.converter = ThoughtGraphConverter()
        self.aether_sim: Optional[AetherSimulator] = None
        self.myco_sim: Optional[MycosentinelSimulator] = None
        
        # Timing
        self.latency_tracker = LatencyMetrics()
        self.stage_timings: Dict[str, List[PipelineStage]] = defaultdict(list)
        
        # Statistics
        self.total_emg_events = 0
        self.total_thoughts = 0
        self.total_particles = 0
        
        # Active timings
        self._active_timings: Dict[str, float] = {}
    
    async def initialize(self) -> bool:
        """Initialize all pipeline components."""
        print("  Initializing pipeline components...")
        
        # Initialize input manager
        self.input_manager = SimulatedInputManager(
            num_users=2,
            mapping=ThoughtMapping(confidence_threshold=0.6)
        )
        self.input_manager._create_personas()
        self.input_manager._setup_simulators()
        
        # Set up callbacks
        self.input_manager.on_thought_created = self._on_thought_created
        
        print("  ✓ Input manager ready")
        
        # Initialize AETHER
        self.aether_sim = AetherSimulator(
            device_id="test-aether-01",
            config={"max_particles": 10000}
        )
        await self.aether_sim.initialize()
        print("  ✓ AETHER simulator ready")
        
        # Initialize MYCOSENTINEL
        self.myco_sim = MycosentinelSimulator(
            device_id="test-myco-01",
            config={}
        )
        await self.myco_sim.initialize()
        print("  ✓ MYCOSENTINEL simulator ready")
        
        return True
    
    def _on_thought_created(self, thought: ThoughtNode, user_id: str) -> None:
        """Handle thought creation."""
        # Complete thought creation timing
        if f"emg_{user_id}" in self._active_timings:
            latency = (time.time() * 1000) - self._active_timings[f"emg_{user_id}"]
            self.latency_tracker.add_emg_thought(latency)
            del self._active_timings[f"emg_{user_id}"]
        
        # Add to thought space
        self.thought_space.add(thought)
        self.total_thoughts += 1
        
        # Start particle conversion timing
        self._active_timings[f"thought_{thought.id}"] = time.time() * 1000
        
        # Convert to particles
        asyncio.create_task(self._convert_and_display(thought))
    
    async def _convert_and_display(self, thought: ThoughtNode) -> None:
        """Convert thought to particles and display."""
        # Convert to targets
        targets = self.converter.convert_thought(thought)
        self.total_particles += len(targets)
        
        # Complete conversion timing
        if f"thought_{thought.id}" in self._active_timings:
            latency = (time.time() * 1000) - self._active_timings[f"thought_{thought.id}"]
            self.latency_tracker.add_thought_particle(latency)
            del self._active_timings[f"thought_{thought.id}"]
        
        # Spawn particles in AETHER
        for target in targets[:3]:  # Limit per thought
            burst_size = int(target.intensity * 20)
            self.aether_sim.spawn_particle_burst(
                count=burst_size,
                position=(target.x, target.y, target.z)
            )
    
    async def run_test(self, duration_seconds: float = 10.0) -> Dict[str, Any]:
        """Run complete pipeline test."""
        print(f"\n  Running pipeline for {duration_seconds}s...")
        
        # Reset stats
        self.total_emg_events = 0
        self.total_thoughts = 0
        self.total_particles = 0
        
        # Start input manager
        self.input_manager.running = True
        for sim in self.input_manager.simulators.values():
            sim.waveform.start()
        
        start_time = time.time()
        
        # Run loop
        while time.time() - start_time < duration_seconds:
            # Process EMG
            for user_id, sim in self.input_manager.simulators.items():
                result = sim.waveform.tick()
                
                if result:
                    state, timestamp, word, confidence = result
                    self.total_emg_events += 1
                    
                    # Start timing for word detection
                    if state == "word_detected" and word:
                        self._active_timings[f"emg_{user_id}"] = time.time() * 1000
            
            # Update AETHER
            await self.aether_sim.update(1.0 / 60.0)
            
            # Update MYCOSENTINEL
            await self.myco_sim.update(1.0)
            
            await asyncio.sleep(0.01)
        
        # Wait for remaining processing
        await asyncio.sleep(0.5)
        
        # Calculate total pipeline latency
        if self.latency_tracker.emg_to_thought_ms:
            avg_emg_thought = sum(self.latency_tracker.emg_to_thought_ms) / len(self.latency_tracker.emg_to_thought_ms)
            avg_thought_particle = sum(self.latency_tracker.thought_to_particle_ms) / len(self.latency_tracker.thought_to_particle_ms)
            total_avg = avg_emg_thought + avg_thought_particle
        else:
            total_avg = 0
        
        return {
            "emg_events": self.total_emg_events,
            "thoughts_created": self.total_thoughts,
            "particles_spawned": self.total_particles,
            "emg_to_thought_avg_ms": avg_emg_thought,
            "thought_to_particle_avg_ms": avg_thought_particle,
            "total_pipeline_avg_ms": total_avg,
            "latency_target_met": total_avg < self.TARGET_LATENCY_MS
        }


class TestSuite:
    """Complete test suite for v1.2 integration."""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.pipeline = EndToEndPipeline()
    
    async def run_all_tests(self) -> List[TestResult]:
        """Execute all tests."""
        print("=" * 70)
        print("COGNITIVE-SYNC v1.2: End-to-End Test Suite")
        print("=" * 70)
        
        # Initialize pipeline
        print("\n🔧 Initializing pipeline...")
        init_start = time.time()
        initialized = await self.pipeline.initialize()
        init_time = (time.time() - init_start) * 1000
        
        if not initialized:
            self.results.append(TestResult(
                name="Pipeline Initialization",
                passed=False,
                latency_ms=init_time,
                error="Failed to initialize one or more components"
            ))
            return self.results
        
        self.results.append(TestResult(
            name="Pipeline Initialization",
            passed=True,
            latency_ms=init_time,
            details={"components": 4}
        ))
        
        # Run tests
        await self.test_emg_to_thought_conversion()
        await self.test_thought_to_particle_conversion()
        await self.test_aether_rendering()
        await self.test_mycosentinel_integration()
        await self.test_latency_requirement()
        await self.test_full_pipeline()
        
        return self.results
    
    async def test_emg_to_thought_conversion(self) -> None:
        """Test EMG to thought conversion."""
        print("\n🧪 Test: EMG to Thought Conversion")
        start = time.time()
        
        # Generate EMG events
        manager = SimulatedInputManager(num_users=1)
        manager._create_personas()
        manager._setup_simulators()
        
        thoughts_generated = 0
        
        def on_thought(thought, user_id):
            nonlocal thoughts_generated
            thoughts_generated += 1
        
        manager.on_thought_created = on_thought
        manager.running = True
        
        for sim in manager.simulators.values():
            sim.waveform.start()
        
        # Run for 2 seconds
        test_start = time.time()
        while time.time() - test_start < 2.0:
            for user_id, sim in manager.simulators.items():
                result = sim.waveform.tick()
                if result:
                    state, timestamp, word, confidence = result
                    if state == "word_detected" and word:
                        await self._mock_process_word(manager, user_id, word, confidence)
            await asyncio.sleep(0.02)
        
        await manager.stop()
        
        elapsed_ms = (time.time() - start) * 1000
        passed = thoughts_generated >= 1
        
        self.results.append(TestResult(
            name="EMG to Thought Conversion",
            passed=passed,
            latency_ms=elapsed_ms,
            details={"thoughts_generated": thoughts_generated}
        ))
        
        print(f"  {'✓' if passed else '✗'} Generated {thoughts_generated} thoughts in {elapsed_ms:.1f}ms")
    
    async def _mock_process_word(self, manager, user_id, word, confidence):
        """Mock processing for test."""
        from thought_node import ThoughtNode
        
        persona = manager.personas[user_id]
        text = manager._expand_text(word, persona)
        
        thought = ThoughtNode(
            text=text,
            author=user_id,
            position=persona.position,
            metadata={"emg_word": word, "confidence": confidence}
        )
        
        manager.thought_space.add(thought)
        
        if manager.on_thought_created:
            manager.on_thought_created(thought, user_id)
    
    async def test_thought_to_particle_conversion(self) -> None:
        """Test thought to particle conversion."""
        print("\n🧪 Test: Thought to Particle Conversion")
        start = time.time()
        
        # Create sample thoughts
        thought_space = ThoughtSpace()
        for i in range(5):
            thought = ThoughtNode(
                text=f"Test thought {i}",
                author="test",
                position=(i * 2, i * 1.5, i * 0.5),
                metadata={}
            )
            thought_space.add(thought)
        
        # Convert
        converter = ThoughtGraphConverter()
        targets = converter.convert_thought_space(thought_space)
        
        elapsed_ms = (time.time() - start) * 1000
        
        total_particles = sum(len(t_list) for t_list in targets.values())
        passed = total_particles > 0
        
        self.results.append(TestResult(
            name="Thought to Particle Conversion",
            passed=passed,
            latency_ms=elapsed_ms,
            details={"thoughts": 5, "particles": total_particles}
        ))
        
        print(f"  {'✓' if passed else '✗'} Converted 5 thoughts to {total_particles} particles in {elapsed_ms:.1f}ms")
    
    async def test_aether_rendering(self) -> None:
        """Test AETHER rendering."""
        print("\n🧪 Test: AETHER Volumetric Rendering")
        start = time.time()
        
        aether = AetherSimulator(device_id="test-aether")
        await aether.initialize()
        
        # Spawn particles
        initial_count = len(aether.particles)
        
        for i in range(10):
            aether.spawn_particle_burst(
                count=50,
                position=(150 + i * 5, 150, 100)
            )
        
        final_count = len(aether.particles)
        
        elapsed_ms = (time.time() - start) * 1000
        passed = final_count > initial_count
        
        self.results.append(TestResult(
            name="AETHER Volumetric Rendering",
            passed=passed,
            latency_ms=elapsed_ms,
            details={"initial_particles": initial_count, "final_particles": final_count}
        ))
        
        print(f"  {'✓' if passed else '✗'} Spawned {final_count - initial_count} particles in {elapsed_ms:.1f}ms")
    
    async def test_mycosentinel_integration(self) -> None:
        """Test MYCOSENTINEL environmental integration."""
        print("\n🧪 Test: MYCOSENTINEL Environmental Integration")
        start = time.time()
        
        myco = MycosentinelSimulator(device_id="test-myco")
        await myco.initialize()
        
        # Update several frames
        frames = []
        for _ in range(10):
            frame = await myco.update(1.0)
            if frame:
                frames.append(frame)
        
        elapsed_ms = (time.time() - start) * 1000
        passed = len(frames) > 5
        
        self.results.append(TestResult(
            name="MYCOSENTINEL Integration",
            passed=passed,
            latency_ms=elapsed_ms,
            details={"frames_received": len(frames)}
        ))
        
        print(f"  {'✓' if passed else '✗'} Processed {len(frames)} frames in {elapsed_ms:.1f}ms")
    
    async def test_latency_requirement(self) -> None:
        """Test latency requirement."""
        print("\n🧪 Test: Latency Requirement (<100ms)")
        
        # Run pipeline for 3 seconds
        result = await self.pipeline.run_test(duration_seconds=3.0)
        
        total_latency = result.get("total_pipeline_avg_ms", float('inf'))
        passed = total_latency < 100.0
        
        self.results.append(TestResult(
            name="Latency Requirement",
            passed=passed,
            latency_ms=total_latency,
            details=result
        ))
        
        status = "✓" if passed else "✗"
        print(f"  {status} Total pipeline latency: {total_latency:.1f}ms (target: <100ms)")
    
    async def test_full_pipeline(self) -> None:
        """Test full end-to-end pipeline."""
        print("\n🧪 Test: Full End-to-End Pipeline")
        
        result = await self.pipeline.run_test(duration_seconds=5.0)
        
        passed = (
            result["emg_events"] > 0 and
            result["thoughts_created"] > 0 and
            result["particles_spawned"] > 0 and
            result["latency_target_met"]
        )
        
        self.results.append(TestResult(
            name="Full End-to-End Pipeline",
            passed=passed,
            latency_ms=result.get("total_pipeline_avg_ms", 0),
            details=result
        ))
        
        status = "✓" if passed else "✗"
        print(f"  {status} Pipeline complete: {result['emg_events']} EMG → {result['thoughts_created']} thoughts → {result['particles_spawned']} particles")
        print(f"    Latency: {result.get('total_pipeline_avg_ms', 0):.1f}ms")
    
    def print_summary(self) -> None:
        """Print test summary."""
        print("\n" + "=" * 70)
        print("Test Summary")
        print("=" * 70)
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"  {status}: {result.name} ({result.latency_ms:.1f}ms)")
            if result.error:
                print(f"      Error: {result.error}")
        
        print(f"\n{'='*70}")
        print(f"Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! v1.2 integration is ready.")
        else:
            print(f"⚠️  {total - passed} test(s) failed. Review results above.")
        
        print("=" * 70)


async def main():
    """Run the test suite."""
    suite = TestSuite()
    await suite.run_all_tests()
    suite.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
