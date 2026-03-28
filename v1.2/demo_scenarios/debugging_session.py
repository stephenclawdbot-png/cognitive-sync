"""
COGNITIVE-SYNC v1.2 Demo Scenario: Debugging Session

Simulates a technical debugging session with analytical thought patterns.
Tests structured problem-solving, issue tracking, and solution generation.

Scenario Details:
- 3 users: senior dev, QA engineer, system architect
- Technical vocabulary emphasis
- Methodical thought progression
- Error → Analysis → Fix workflow
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


class DebuggingSessionScenario:
    """
    Technical debugging scenario.
    
    Participants:
    - Dev (Senior Developer): Code analysis, implementation
    - QA (QA Engineer): Testing, reproduction steps
    - Arch (System Architect): Pattern analysis, root cause
    
    Session Flow:
    1. Error identification
    2. Context gathering
    3. Analysis phase
    4. Solution generation
    5. Verification
    """
    
    DEBUGGING_PHASES = [
        "error_identification",
        "context_gathering", 
        "analysis",
        "solution",
        "verification"
    ]
    
    PHASE_VOCABULARIES = {
        "error_identification": [
            "bug", "error", "exception", "crash", "failure",
            "unexpected", "broken", "issue", "problem", "fault"
        ],
        "context_gathering": [
            "log", "trace", "stack", "context", "reproduce",
            "trigger", "condition", "state", "input", "environment"
        ],
        "analysis": [
            "analyze", "investigate", "debug", "trace", "isolate",
            "pattern", "correlation", "dependency", "root cause", "hypothesis"
        ],
        "solution": [
            "fix", "implement", "refactor", "patch", "solution",
            "optimize", "redesign", "alternative", "workaround", "correct"
        ],
        "verification": [
            "test", "verify", "validate", "confirm", "check",
            "assert", "pass", "coverage", "regression", "green"
        ]
    }
    
    def __init__(self):
        self.manager = SimulatedInputManager(
            num_users=3,
            mapping=ThoughtMapping(
                confidence_threshold=0.75,  # More deliberate
                text_expansion={
                    "bug": ["BUG: Critical issue found", "Bug identified in", "Defect detected:"],
                    "error": ["ERROR:", "Exception thrown:", "Error condition met:"],
                    "analyze": ["Analysis shows", "Investigating", "Tracing through code:"],
                    "fix": ["Proposed fix:", "Solution implemented:", "Patch applied:"],
                    "test": ["Test case:", "Verification step:", "Validating fix:"]
                }
            )
        )
        
        self.thought_count = 0
        self.session_duration = 60
        self.current_phase = 0
    
    def _setup_debugging_personas(self) -> None:
        """Configure debugging-focused personas."""
        personas = [
            {
                "name": "Dev",
                "style": "technical",
                "emg_pattern": EMGPattern.SUBVOCAL,
                "color": "#64aaff",
                "mobility": 0.8,
                "base_vocab": [
                    "code", "function", "variable", "module", "class",
                    "debug", "breakpoint", "inspect", "console", "log"
                ]
            },
            {
                "name": "QA",
                "style": "analytical",
                "emg_pattern": EMGPattern.COMBINED,
                "color": "#ffd864",
                "mobility": 1.0,
                "base_vocab": [
                    "test", "reproduce", "scenario", "edge case", "coverage",
                    "assert", "expected", "actual", "pass", "fail"
                ]
            },
            {
                "name": "Arch",
                "style": "analytical",
                "emg_pattern": EMGPattern.NECK,
                "color": "#ff64a0",
                "mobility": 0.5,
                "base_vocab": [
                    "pattern", "architecture", "component", "interface", "dependency",
                    "design", "system", "layer", "module", "coupling"
                ]
            }
        ]
        
        for i, p in enumerate(personas):
            persona = UserPersona(
                user_id=f"debug_{i}",
                name=p["name"],
                style=p["style"],
                emg_pattern=p["emg_pattern"],
                vocabulary=p["base_vocab"],
                creativity_level=0.3,  # More predictable
                color=p["color"],
                mobility=p["mobility"],
                position=(random.uniform(-5, 5), random.uniform(-3, 3), random.uniform(-1, 1))
            )
            
            self.manager.personas[persona.user_id] = persona
            self.manager._last_thought_time[persona.user_id] = 0
            self.manager._thought_buffer[persona.user_id] = []
    
    def _get_phase_for_time(self, elapsed: float) -> str:
        """Determine current debugging phase based on elapsed time."""
        phase_duration = self.session_duration / len(self.DEBUGGING_PHASES)
        phase_index = int(elapsed / phase_duration)
        return self.DEBUGGING_PHASES[min(phase_index, len(self.DEBUGGING_PHASES) - 1)]
    
    async def run(self) -> Dict[str, Any]:
        """Run the debugging session scenario."""
        print("=" * 70)
        print("🔧 DEBUGGING SESSION SCENARIO")
        print("=" * 70)
        print()
        print("Participants:")
        print("  • Dev (Senior Developer) - Code analysis, implementation")
        print("  • QA (QA Engineer) - Testing, reproduction steps")
        print("  • Arch (System Architect) - Pattern analysis, root cause")
        print()
        print("Session Flow:")
        for i, phase in enumerate(self.DEBUGGING_PHASES):
            print(f"  {i+1}. {phase.replace('_', ' ').title()}")
        print()
        print(f"Duration: {self.session_duration}s")
        print("-" * 70)
        
        self._setup_debugging_personas()
        self.manager._setup_simulators()
        
        # Track by phase
        phase_thoughts: Dict[str, List[str]] = {p: [] for p in self.DEBUGGING_PHASES}
        
        start_time = asyncio.get_event_loop().time()
        
        def on_thought(thought: ThoughtNode, user_id: str):
            self.thought_count += 1
            
            elapsed = asyncio.get_event_loop().time() - start_time
            phase = self._get_phase_for_time(elapsed)
            phase_thoughts[phase].append(thought.text)
            
            # Phase indicator
            phase_num = self.DEBUGGING_PHASES.index(phase) + 1
            persona = self.manager.personas[user_id]
            
            print(f"  [{persona.name:4}] P{phase_num} 🔍 {thought.text[:45]:45} "
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
        
        return {
            "scenario": "debugging_session",
            "duration_seconds": self.session_duration,
            "thoughts_generated": len(all_thoughts),
            "phases": {
                phase: len(thoughts)
                for phase, thoughts in phase_thoughts.items()
            },
            "sample_by_phase": {
                phase: texts[:2] if texts else []
                for phase, texts in phase_thoughts.items()
            }
        }


import random


async def main():
    """Run debugging session demo."""
    scenario = DebuggingSessionScenario()
    results = await scenario.run()
    
    print("\n" + "=" * 70)
    print("Session Complete")
    print("=" * 70)
    print(f"  Total thoughts: {results['thoughts_generated']}")
    print("\n  Thoughts per phase:")
    for phase, count in results['phases'].items():
        print(f"    {phase.replace('_', ' ').title()}: {count}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
