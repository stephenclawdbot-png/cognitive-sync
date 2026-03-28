"""
COGNITIVE-SYNC v1.2 Demo Scenario: Creative Flow Session

Simulates a creative brainstorming session with multiple users generating ideas.
Ideal for testing thought clustering, visual connections, and collaborative ideation.

Scenario Details:
- 3 users: designer, writer, architect
- Creative vocabulary emphasis
- High-mobility thought patterns
- Frequent semantic clustering
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any

WORKSPACE = Path("/Users/clawdbot/.openclaw/workspace")
sys.path.insert(0, str(WORKSPACE / "COGNITIVE-SYNC"))
sys.path.insert(0, str(WORKSPACE / "SILENT-001" / "firmware"))

from v1_2.simulated_input import SimulatedInputManager, UserPersona, ThoughtMapping, EMGPattern
from thought_node import ThoughtNode


class CreativeFlowScenario:
    """
    Creative brainstorming scenario.
    
    Participants:
    - Maya (Designer): Visual thinking, color concepts
    - Leo (Writer): Narrative, storytelling
    - Nina (Architect): Spatial, structural ideas
    """
    
    def __init__(self):
        self.manager = SimulatedInputManager(
            num_users=3,
            mapping=ThoughtMapping(
                confidence_threshold=0.65,
                text_expansion={
                    "imagine": ["Let's imagine a world where...", "Picture this:", "I envision..."],
                    "create": ["We could create", "Let's build", "Design concept:"],
                    "inspire": ["This inspires me to", "The spark of inspiration:", "Creative direction:"],
                    "color": ["Color palette:", "Visual harmony in", "The tones suggest..."],
                    "space": ["The spatial arrangement", "Architectural flow", "Interconnected areas"],
                    "story": ["The narrative arc", "Character development", "Plot twist idea:"]
                }
            )
        )
        
        self.thought_count = 0
        self.session_duration = 60  # seconds
    
    def _setup_creative_personas(self) -> None:
        """Configure creative-focused personas."""
        self.manager._create_personas = self._creative_persona_override
    
    def _creative_persona_override(self) -> None:
        """Override default personas with creative profiles."""
        personas = [
            {
                "name": "Maya",
                "style": "creative",
                "emg_pattern": EMGPattern.FACIAL,
                "vocabulary": [
                    "imagine", "color", "visual", "design", "texture",
                    "pattern", "harmony", "contrast", "mood", "style"
                ],
                "color": "#ff64d8",
                "mobility": 2.5,
                "creativity": 0.9
            },
            {
                "name": "Leo",
                "style": "creative",
                "emg_pattern": EMGPattern.SUBVOCAL,
                "vocabulary": [
                    "story", "narrative", "character", "plot", "scene",
                    "dialogue", "theme", "emotion", "journey", "climax"
                ],
                "color": "#ffd864",
                "mobility": 1.8,
                "creativity": 0.85
            },
            {
                "name": "Nina",
                "style": "creative",
                "emg_pattern": EMGPattern.COMBINED,
                "vocabulary": [
                    "space", "structure", "flow", "connected", "organic",
                    "framework", "layer", "dimension", "perspective", "form"
                ],
                "color": "#64ffd8",
                "mobility": 2.0,
                "creativity": 0.8
            }
        ]
        
        for i, p in enumerate(personas):
            persona = UserPersona(
                user_id=f"creative_{i}",
                name=p["name"],
                style=p["style"],
                emg_pattern=p["emg_pattern"],
                vocabulary=p["vocabulary"],
                creativity_level=p["creativity"],
                color=p["color"],
                mobility=p["mobility"],
                position=(random.uniform(-8, 8), random.uniform(-6, 6), random.uniform(-2, 2))
            )
            
            self.manager.personas[persona.user_id] = persona
            self.manager._last_thought_time[persona.user_id] = 0
            self.manager._thought_buffer[persona.user_id] = []
    
    async def run(self) -> Dict[str, Any]:
        """
        Run the creative flow scenario.
        
        Returns:
            Session metrics and generated content
        """
        print("=" * 70)
        print("🎨 CREATIVE FLOW SCENARIO")
        print("=" * 70)
        print()
        print("Participants:")
        print("  • Maya (Designer) - Visual thinking, color concepts")
        print("  • Leo (Writer) - Narrative, storytelling")
        print("  • Nina (Architect) - Spatial, structural ideas")
        print()
        print(f"Duration: {self.session_duration}s")
        print("-" * 70)
        
        self._setup_creative_personas()
        self.manager._setup_simulators()
        
        # Track thoughts
        thoughts_by_user: Dict[str, list] = {}
        clusters_formed = []
        
        def on_thought(thought: ThoughtNode, user_id: str):
            self.thought_count += 1
            if user_id not in thoughts_by_user:
                thoughts_by_user[user_id] = []
            thoughts_by_user[user_id].append(thought)
            
            persona = self.manager.personas[user_id]
            print(f"  [{persona.name:6}] 💡 {thought.text[:50]:50} "
                  f"@ ({thought.position[0]:5.1f}, {thought.position[1]:5.1f})")
        
        self.manager.on_thought_created = on_thought
        
        # Run session
        try:
            await self.manager.start()
            await asyncio.sleep(self.session_duration)
        except asyncio.CancelledError:
            pass
        finally:
            await self.manager.stop()
        
        # Compile results
        all_thoughts = self.manager.thought_space.all_thoughts()
        
        return {
            "scenario": "creative_flow",
            "duration_seconds": self.session_duration,
            "thoughts_generated": len(all_thoughts),
            "thoughts_by_user": {uid: len(thoughts) for uid, thoughts in thoughts_by_user.items()},
            "sample_thoughts": [t.text for t in all_thoughts[:5]]
        }


import random


async def main():
    """Run creative flow demo."""
    scenario = CreativeFlowScenario()
    results = await scenario.run()
    
    print("\n" + "=" * 70)
    print("Session Complete")
    print("=" * 70)
    print(f"  Total thoughts: {results['thoughts_generated']}")
    print(f"  By user: {results['thoughts_by_user']}")
    print("\n  Sample thoughts:")
    for t in results['sample_thoughts']:
        print(f"    • {t}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
