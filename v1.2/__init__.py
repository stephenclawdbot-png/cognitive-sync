"""
COGNITIVE-SYNC v1.2 - HARDWARE-SIMULATOR Integration Module

This module provides end-to-end integration between COGNITIVE-SYNC thought nodes
and the HARDWARE-SIMULATOR digital twin system.

Components:
- integration_bridge: Main bridge between thought_node and hardware simulators
- simulated_input: EMG signal simulation for thought generation
- thought_to_simulation: Export thoughts as particle targets
- end_to_end_test: Complete pipeline validation
- demo_scenarios: Pre-built test scenarios

Usage:
    from COGNITIVE_SYNC.v1_2 import IntegrationBridge
    
    bridge = IntegrationBridge()
    await bridge.initialize()
    await bridge.start()
"""

__version__ = "1.2.0"
__author__ = "COGNITIVE-SYNC Team"

from .integration_bridge import IntegrationBridge, SimulationTarget, LatencyMetrics
from .simulated_input import SimulatedInputManager, ThoughtMapping, UserPersona
from .thought_to_simulation import ThoughtGraphConverter, ParticleTarget, RealtimeThoughtExporter

__all__ = [
    "IntegrationBridge",
    "SimulationTarget",
    "LatencyMetrics",
    "SimulatedInputManager",
    "ThoughtMapping",
    "UserPersona",
    "ThoughtGraphConverter",
    "ParticleTarget",
    "RealtimeThoughtExporter",
]
