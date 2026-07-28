"""
COGNITIVE-SYNC v1.2 Demo Scenarios

Pre-built test scenarios for validating hardware-simulator integration.

Scenarios:
- creative_flow: Artistic brainstorming session
- debugging_session: Technical debugging workflow
- planning_meeting: Collaborative project planning

Usage:
    from v1_2.demo_scenarios.creative_flow import CreativeFlowScenario
    
    scenario = CreativeFlowScenario()
    results = await scenario.run()
"""

from .creative_flow import CreativeFlowScenario
from .debugging_session import DebuggingSessionScenario
from .planning_meeting import PlanningMeetingScenario

__all__ = [
    "CreativeFlowScenario",
    "DebuggingSessionScenario",
    "PlanningMeetingScenario",
]
