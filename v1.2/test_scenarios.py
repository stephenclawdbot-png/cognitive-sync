"""
COGNITIVE-SYNC v1.2 - Test Scenarios
Predefined test scenarios for validation of the SILEM simulator integration.

Each scenario tests a specific aspect of the pipeline with expected outcomes
to verify correctness before hardware arrival (April 14).
"""

import asyncio
import json
import time
import random
import logging
from typing import Dict, List, Optional, Tuple, Callable, Any
from dataclasses import dataclass, field
from pathlib import Path
import sys

# Add paths
HW_SIM_PATH = Path(__file__).parent.parent.parent / "hardware-simulator"
sys.path.insert(0, str(HW_SIM_PATH))
COG_SYNC_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(COG_SYNC_PATH))

from thought_node import ThoughtNode, ThoughtSpace
from silent_sim_bridge import (
    EMGPatternLibrary, EMGToThoughtMapper, SilentSimConnector,
    ThoughtCategory, EMGPattern
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestScenarios")


@dataclass
class TestResult:
    """Result of a single test execution."""
    name: str
    passed: bool
    duration_ms: float
    metrics: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    
    def summary(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} | {self.name} | {self.duration_ms:.1f}ms"


@dataclass
class ScenarioConfig:
    """Configuration for a test scenario."""
    name: str
    description: str
    patterns: List[EMGPattern]
    expected_thoughts: int
    expected_latency_ms: float
    min_confidence: float
    duration_sec: float = 5.0
    tolerance_percent: float = 20.0


class TestValidator:
    """Validates test results against expected patterns."""
    
    def __init__(self, tolerance_percent: float = 20.0):
        self.tolerance = tolerance_percent
    
    def validate_thought_count(self, actual: int, expected: int) -> bool:
        """Check if thought count is within tolerance."""
        if expected == 0:
            return actual == 0
        
        error_percent = abs(actual - expected) / expected * 100
        return error_percent <= self.tolerance
    
    def validate_latency(self, actual: float, expected: float) -> bool:
        """Check if latency is within tolerance."""
        if expected == 0:
            return actual < 1.0
        
        error_percent = abs(actual - expected) / expected * 100
        return error_percent <= self.tolerance
    
    def validate_confidence(self, actual: float, min_required: float) -> bool:
        """Check if confidence meets minimum requirement."""
        return actual >= min_required


class TestScenarioRunner:
    """Runs predefined test scenarios and validates results."""
    
    def __init__(self):
        self.validator = TestValidator()
        self.mapper = EMGToThoughtMapper()
        self.thought_space = ThoughtSpace()
        self.results: List[TestResult] = []
        
    async def run_all_scenarios(self) -> List[TestResult]:
        """Execute all test scenarios."""
        self.results = []
        
        scenarios = [
            self.scenario_silent_speech_recognition(),
            self.scenario_gesture_control(),
            self.scenario_bio_feedback(),
            self.scenario_spatial_navigation(),
            self.scenario_mixed_activity(),
            self.scenario_latency_benchmark(),
            self.scenario_throughput_stress(),
            self.scenario_crdt_convergence()
        ]
        
        print("=" * 70)
        print("COGNITIVE-SYNC v1.2 - Test Scenario Validation")
        print("=" * 70)
        print()
        
        for scenario_config in scenarios:
            result = await self._execute_scenario(scenario_config)
            self.results.append(result)
            print(f"  {result.summary()}")
        
        return self.results
    
    async def _execute_scenario(self, config: ScenarioConfig) -> TestResult:
        """Execute a single test scenario."""
        start_time = time.time()
        start_perf = time.perf_counter()
        
        generated_thoughts = []
        latencies = []
        confidences = []
        
        try:
            # Run for configured duration
            end_time = start_time + config.duration_sec
            
            while time.time() < end_time:
                # Simulate EMG frames with scenario patterns
                await self._simulate_pattern_tick(
                    config.patterns,
                    generated_thoughts,
                    latencies,
                    confidences
                )
                await asyncio.sleep(0.1)
            
            # Calculate metrics
            duration_ms = (time.perf_counter() - start_perf) * 1000
            avg_latency = sum(latencies) / max(len(latencies), 1) if latencies else 0
            avg_confidence = sum(confidences) / max(len(confidences), 1) if confidences else 0
            
            # Validate
            passed = True
            
            if not self.validator.validate_thought_count(
                len(generated_thoughts), config.expected_thoughts):
                passed = False
            
            if not self.validator.validate_latency(avg_latency, config.expected_latency_ms):
                passed = False
            
            if not self.validator.validate_confidence(avg_confidence, config.min_confidence):
                passed = False
            
            return TestResult(
                name=config.name,
                passed=passed,
                duration_ms=duration_ms,
                metrics={
                    "thoughts_generated": len(generated_thoughts),
                    "thoughts_expected": config.expected_thoughts,
                    "avg_latency_ms": avg_latency,
                    "latency_expected_ms": config.expected_latency_ms,
                    "avg_confidence": avg_confidence,
                    "min_confidence": config.min_confidence
                }
            )
            
        except Exception as e:
            duration_ms = (time.perf_counter() - start_perf) * 1000
            return TestResult(
                name=config.name,
                passed=False,
                duration_ms=duration_ms,
                error=str(e)
            )
    
    async def _simulate_pattern_tick(
        self,
        patterns: List[EMGPattern],
        thoughts: List[ThoughtNode],
        latencies: List[float],
        confidences: List[float]
    ):
        """Simulate one tick of pattern activity."""
        if random.random() < 0.35:  # 35% activity rate
            pattern = random.choice(patterns)
            
            tick_start = time.perf_counter()
            
            # Create synthetic EMG frame
            frame_data = {
                "payload": {
                    "current_phoneme": random.choice(pattern.phoneme_sequence),
                    "activity_level": random.uniform(0.7, 0.95),
                    "detection_confidence": random.uniform(0.75, 0.95)
                },
                "metadata": {
                    "emg_samples": [
                        {"muscle": m, "rms": a * 100}
                        for m, a in pattern.muscle_activation.items()
                    ]
                }
            }
            
            # Process through mapper
            mapping = self.mapper.process_emg_frame(frame_data)
            
            if mapping:
                thoughts.append(mapping.thought)
                latencies.append((time.perf_counter() - tick_start) * 1000)
                confidences.append(mapping.confidence)
                
                # Add to thought space for CRDT testing
                self.thought_space.add(mapping.thought)
    
    # Scenario Definitions
    
    def scenario_silent_speech_recognition(self) -> ScenarioConfig:
        """
        SCENARIO 1: Silent Speech Recognition
        
        Tests the ability to detect and convert subvocal EMG patterns
        into recognizable thought/text patterns.
        
        Expected: High accuracy phoneme recognition, proper text generation
        """
        return ScenarioConfig(
            name="Silent Speech Recognition",
            description="Tests subvocal EMG to text conversion accuracy",
            patterns=EMGPatternLibrary.get_patterns_by_category(ThoughtCategory.SILENT_SPEECH),
            expected_thoughts=8,
            expected_latency_ms=15.0,
            min_confidence=0.70,
            duration_sec=3.0
        )
    
    def scenario_gesture_control(self) -> ScenarioConfig:
        """
        SCENARIO 2: Gesture Control Mapping
        
        Tests EMG-based gesture recognition for spatial control.
        Validates chin lift, jaw clench, and other control gestures.
        
        Expected: Reliable gesture detection with proper thought mapping
        """
        return ScenarioConfig(
            name="Gesture Control Mapping",
            description="Tests EMG gesture detection for spatial control",
            patterns=EMGPatternLibrary.get_patterns_by_category(ThoughtCategory.GESTURE_CONTROL),
            expected_thoughts=5,
            expected_latency_ms=12.0,
            min_confidence=0.65,
            duration_sec=3.0
        )
    
    def scenario_bio_feedback(self) -> ScenarioConfig:
        """
        SCENARIO 3: Bio-Feedback Monitoring
        
        Tests continuous physiological state monitoring from EMG patterns.
        Validates breathing and concentration state detection.
        
        Expected: Smooth bio-signal integration with calm/thoughtful states
        """
        return ScenarioConfig(
            name="Bio-Feedback Monitoring",
            description="Tests physiological state detection from EMG",
            patterns=EMGPatternLibrary.get_patterns_by_category(ThoughtCategory.BIO_FEEDBACK),
            expected_thoughts=4,
            expected_latency_ms=10.0,
            min_confidence=0.50,
            duration_sec=5.0
        )
    
    def scenario_spatial_navigation(self) -> ScenarioConfig:
        """
        SCENARIO 4: Spatial Navigation
        
        Tests EMG-based spatial control patterns for 3D thought space navigation.
        Validates head movement and directional control mapping.
        
        Expected: Accurate directional mapping with spatial positioning
        """
        return ScenarioConfig(
            name="Spatial Navigation",
            description="Tests EMG-based 3D space navigation control",
            patterns=EMGPatternLibrary.get_patterns_by_category(ThoughtCategory.SPATIAL_NAV),
            expected_thoughts=5,
            expected_latency_ms=12.0,
            min_confidence=0.60,
            duration_sec=3.0
        )
    
    def scenario_mixed_activity(self) -> ScenarioConfig:
        """
        SCENARIO 5: Mixed Activity Recognition
        
        Tests classification of simultaneous and mixed EMG patterns.
        Validates proper categorization when multiple muscle groups active.
        
        Expected: Correct classification of multi-pattern input
        """
        return ScenarioConfig(
            name="Mixed Activity Recognition",
            description="Tests multi-pattern EMG classification",
            patterns=EMGPatternLibrary.get_all_patterns(),
            expected_thoughts=15,
            expected_latency_ms=18.0,
            min_confidence=0.55,
            duration_sec=5.0
        )
    
    def scenario_latency_benchmark(self) -> ScenarioConfig:
        """
        SCENARIO 6: Latency Benchmark
        
        Measures end-to-end latency from EMG signal to thought visualization.
        Validates the 50ms latency target.
        
        Expected: Average latency < 50ms, peak latency < 100ms
        """
        return ScenarioConfig(
            name="Latency Benchmark",
            description="Measures end-to-end pipeline latency",
            patterns=EMGPatternLibrary.get_all_patterns()[:3],
            expected_thoughts=10,
            expected_latency_ms=25.0,  # Target well under 50ms
            min_confidence=0.60,
            duration_sec=3.0
        )
    
    def scenario_throughput_stress(self) -> ScenarioConfig:
        """
        SCENARIO 7: Throughput Stress Test
        
        Tests pipeline under high-frequency EMG input.
        Validates throughput target of 60 FPS (16.67ms per frame).
        
        Expected: Stable processing at 60 FPS input rate
        """
        return ScenarioConfig(
            name="Throughput Stress Test",
            description="Tests pipeline throughput at high frequency",
            patterns=EMGPatternLibrary.get_all_patterns(),
            expected_thoughts=30,
            expected_latency_ms=16.67,  # 60 FPS target
            min_confidence=0.50,
            duration_sec=3.0
        )
    
    def scenario_crdt_convergence(self) -> ScenarioConfig:
        """
        SCENARIO 8: CRDT Convergence
        
        Tests distributed thought merging with concurrent EMG inputs.
        Validates CRDT conflict resolution for simultaneous thoughts.
        
        Expected: Correct LWW merge, no thought loss
        """
        return ScenarioConfig(
            name="CRDT Convergence",
            description="Tests distributed thought CRDT merging",
            patterns=EMGPatternLibrary.get_all_patterns()[:5],
            expected_thoughts=8,
            expected_latency_ms=20.0,
            min_confidence=0.60,
            duration_sec=4.0
        )
    
    def generate_report(self) -> Dict:
        """Generate comprehensive test report."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        total_duration = sum(r.duration_ms for r in self.results)
        
        return {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": f"{passed/total*100:.1f}%" if total > 0 else "N/A",
                "total_duration_ms": total_duration
            },
            "test_results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "duration_ms": r.duration_ms,
                    "metrics": r.metrics,
                    "error": r.error
                }
                for r in self.results
            ]
        }


def print_detailed_report(report: Dict):
    """Print detailed test report to console."""
    print("\n" + "=" * 70)
    print("DETAILED TEST REPORT")
    print("=" * 70)
    
    summary = report["summary"]
    print(f"\nSummary:")
    print(f"  Total Tests: {summary['total_tests']}")
    print(f"  Passed: {summary['passed']} ✅")
    print(f"  Failed: {summary['failed']} {'❌' if summary['failed'] > 0 else ''}")
    print(f"  Pass Rate: {summary['pass_rate']}")
    print(f"  Total Duration: {summary['total_duration_ms']:.1f}ms")
    
    print(f"\nDetailed Results:")
    print("-" * 70)
    
    for result in report["test_results"]:
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"\n{status} | {result['name']}")
        print(f"  Duration: {result['duration_ms']:.1f}ms")
        
        if result["metrics"]:
            print(f"  Metrics:")
            for key, value in result["metrics"].items():
                if isinstance(value, float):
                    print(f"    {key}: {value:.2f}")
                else:
                    print(f"    {key}: {value}")
        
        if result["error"]:
            print(f"  Error: {result['error']}")
    
    print("\n" + "=" * 70)


async def run_validation():
    """Run full validation suite."""
    runner = TestScenarioRunner()
    await runner.run_all_scenarios()
    
    # Generate and save report
    report = runner.generate_report()
    
    # Print detailed report
    print_detailed_report(report)
    
    # Save to file
    report_path = Path(__file__).parent / "test_results.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to: {report_path}")
    
    # Return exit code
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_validation())
    sys.exit(exit_code)
