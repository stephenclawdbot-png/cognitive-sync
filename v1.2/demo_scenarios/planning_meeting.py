"""
COGNITIVE-SYNC v1.2 Demo Scenario: Planning Meeting

Simulates a collaborative planning session with mixed thought styles.
Tests real-time synchronization, consensus building, and multi-perspective integration.

Scenario Details:
- 4 users: PM, tech lead, designer, stakeholder
- Mixed vocabulary (technical, business, creative)
- Consensus-seeking behavior
- Decision point visualization
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, List

WORKSPACE = Path("/Users/clawdbot/.openclaw/workspace")
sys.path.insert(0, str(WORKSPACE / "COGNITIVE-SYNC"))
sys.path.insert(0, str(WORKSPACE / "SILENT-001" / "firmware"))

from v1_2.simulated_input import SimulatedInputManager, UserPersona, ThoughtMapping, EMGPattern
from thought_node import ThoughtNode


class PlanningMeetingScenario:
    """
    Collaborative planning meeting scenario.
    
    Participants:
    - Priya (PM): Scope, timeline, resources
    - Tom (Tech Lead): Implementation, complexity, risks
    - Sofia (Designer): UX, user needs, flows
    - Alex (Stakeholder): Business value, priorities
    
    Meeting Structure:
    1. Problem framing
    2. Option exploration
    3. Trade-off analysis
    4. Decision making
    5. Action items
    """
    
    MEETING_AGENDA = [
        "problem_framing",
        "option_exploration",
        "tradeoff_analysis",
        "decision_making",
        "action_items"
    ]
    
    def __init__(self):
        self.manager = SimulatedInputManager(
            num_users=4,
            mapping=ThoughtMapping(
                confidence_threshold=0.7,
                text_expansion={
                    "scope": ["Scope definition:", "In scope:", "Scope boundary:"],
                    "timeline": ["Timeline estimate:", "Schedule constraint:", "Milestone:"],
                    "risk": ["Risk identified:", "Potential blocker:", "Mitigation:"],
                    "user": ["User perspective:", "UX consideration:", "User need:"],
                    "value": ["Business value:", "ROI consideration:", "Priority:"],
                    "decide": ["Decision:", "Consensus reached:", "Approved:"],
                    "action": ["Action item:", "Next step:", "Assigned to:"]
                }
            )
        )
        
        self.session_duration = 60
    
    def _setup_planning_personas(self) -> None:
        """Configure planning-focused personas."""
        personas = [
            {
                "name": "Priya",
                "role": "PM",
                "style": "analytical",
                "emg_pattern": EMGPattern.SUBVOCAL,
                "color": "#64ffd8",
                "vocabulary": [
                    "scope", "timeline", "resource", "milestone", "deliverable",
                    "dependency", "critical path", "stakeholder", "gantt", "status"
                ],
                "mobility": 1.0
            },
            {
                "name": "Tom",
                "role": "Tech Lead",
                "style": "technical",
                "emg_pattern": EMGPattern.COMBINED,
                "color": "#64aaff",
                "vocabulary": [
                    "implement", "architecture", "complexity", "risk", "dependency",
                    "technical", "integration", "api", "performance", "scalability"
                ],
                "mobility": 0.7
            },
            {
                "name": "Sofia",
                "role": "Designer",
                "style": "creative",
                "emg_pattern": EMGPattern.FACIAL,
                "color": "#ff64d8",
                "vocabulary": [
                    "user", "experience", "flow", "journey", "interface",
                    "interaction", "visual", "usability", "accessibility", "design"
                ],
                "mobility": 1.5
            },
            {
                "name": "Alex",
                "role": "Stakeholder",
                "style": "social",
                "emg_pattern": EMGPattern.NECK,
                "color": "#ffd864",
                "vocabulary": [
                    "value", "priority", "business", "roi", "objective",
                    "strategy", "market", "customer", "revenue", "impact"
                ],
                "mobility": 0.8
            }
        ]
        
        for i, p in enumerate(personas):
            persona = UserPersona(
                user_id=f"plan_{i}",
                name=p["name"],
                style=p["style"],
                emg_pattern=p["emg_pattern"],
                vocabulary=p["vocabulary"],
                creativity_level=0.55,
                color=p["color"],
                mobility=p["mobility"],
                position=(random.uniform(-8, 8), random.uniform(-5, 5), random.uniform(-2, 2))
            )
            
            self.manager.personas[persona.user_id] = persona
            self.manager._last_thought_time[persona.user_id] = 0
            self.manager._thought_buffer[persona.user_id] = []
    
    def _get_agenda_item(self, elapsed: float) -> str:
        """Get current agenda item based on elapsed time."""
        item_duration = self.session_duration / len(self.MEETING_AGENDA)
        index = int(elapsed / item_duration)
        return self.MEETING_AGENDA[min(index, len(self.MEETING_AGENDA) - 1)]
    
    async def run(self) -> Dict[str, Any]:
        """Run the planning meeting scenario."""
        print("=" * 70)
        print("📋 PLANNING MEETING SCENARIO")
        print("=" * 70)
        print()
        print("Participants:")
        print("  • Priya (PM) - Scope, timeline, resources")
        print("  • Tom (Tech Lead) - Implementation, complexity, risks")
        print("  • Sofia (Designer) - UX, user needs, flows")
        print("  • Alex (Stakeholder) - Business value, priorities")
        print()
        print("Meeting Agenda:")
        for i, item in enumerate(self.MEETING_AGENDA):
            print(f"  {i+1}. {item.replace('_', ' ').title()}")
        print()
        print(f"Duration: {self.session_duration}s")
        print("-" * 70)
        
        self._setup_planning_personas()
        self.manager._setup_simulators()
        
        # Track by agenda and user
        agenda_thoughts: Dict[str, List[str]] = {a: [] for a in self.MEETING_AGENDA}
        user_thoughts: Dict[str, int] = {}
        
        start_time = asyncio.get_event_loop().time()
        
        def on_thought(thought: ThoughtNode, user_id: str):
            elapsed = asyncio.get_event_loop().time() - start_time
            agenda = self._get_agenda_item(elapsed)
            agenda_thoughts[agenda].append(thought.text)
            
            # Track per user
            if thought.author not in user_thoughts:
                user_thoughts[thought.author] = 0
            user_thoughts[thought.author] += 1
            
            agenda_num = self.MEETING_AGENDA.index(agenda) + 1
            persona = self.manager.personas[user_id]
            
            print(f"  [{persona.name:6}] A{agenda_num} 📝 {thought.text[:45]:45} "
                  f"@ ({thought.position[0]:5.1f}, {thought.position[1]:5.1f})")
        
        self.manager.on_thought_created = on_thought
        
        try:
            await self.manager.start()
            await asyncio.sleep(self.session_duration)
        except asyncio.CancelledError:
            pass
        finally:
            await self.manager.stop()
        
        all_thoughts = self.manager.thought_space.all_thoughts()
        
        # Identify convergent thoughts (decisions)
        decision_words = ["decide", "consensus", "approved", "agreed", "final"]
        decision_count = sum(
            1 for t in all_thoughts
            if any(w in t.text.lower() for w in decision_words)
        )
        
        return {
            "scenario": "planning_meeting",
            "duration_seconds": self.session_duration,
            "thoughts_generated": len(all_thoughts),
            "thoughts_by_role": {
                self.manager.personas[uid].name: count
                for uid, count in user_thoughts.items()
            },
            "thoughts_by_agenda": {
                item.replace('_', ' ').title(): len(ts)
                for item, ts in agenda_thoughts.items()
            },
            "decision_points": decision_count
        }


import random


async def main():
    """Run planning meeting demo."""
    scenario = PlanningMeetingScenario()
    results = await scenario.run()
    
    print("\n" + "=" * 70)
    print("Meeting Complete")
    print("=" * 70)
    print(f"  Total thoughts: {results['thoughts_generated']}")
    print(f"  Decision points: {results['decision_points']}")
    print("\n  By participant:")
    for role, count in results['thoughts_by_role'].items():
        print(f"    {role}: {count}")
    print("\n  By agenda item:")
    for item, count in results['thoughts_by_agenda'].items():
        print(f"    {item}: {count}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
