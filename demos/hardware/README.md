# COGNITIVE-SYNC v1.2 - HARDWARE-SIMULATOR Integration

End-to-end integration layer connecting COGNITIVE-SYNC thought_node system with HARDWARE-SIMULATOR for pre-hardware testing.

---

## Overview

COGNITIVE-SYNC v1.2 enables pre-hardware validation by integrating three simulator systems:

1. **SILENT_SIMULATOR** → Generates EMG signals for thought triggering
2. **COGNITIVE-SYNC thought_node** → CRDT-based thought management
3. **AETHER_SIMULATOR** → Volumetric particle display
4. **MYCOSENTINEL_SIMULATOR** → Environmental factor injection

---

## Architecture

```
┌─────────────────┐     EMG      ┌──────────────────┐
│ SILENT_SIMULATOR│───signals───▶│                  │
│   (simulated)   │              │   integration    │
└─────────────────┘              │     _bridge       │
                                 │                  │
┌─────────────────┐              └────────┬─────────┘
│                 │                         │
│MYCOSENTINEL_SIM │◀──environmental────────┤
│  (stress factors)                       │
└─────────────────┘              ┌────────▼─────────┐
                                 │  COGNITIVE-SYNC  │
                                 │   thought_node   │
                                 └────────┬─────────┘
                                          │
                                          ▼
                                 ┌──────────────────┐
                                 │thought_to_simula- │
                                 │   tion.py        │
                                 └────────┬─────────┘
                                          │ particle
                                          │ targets
                                          ▼
                                 ┌──────────────────┐
                                 │ AETHER_SIMULATOR │
                                 │ (100K particles) │
                                 └──────────────────┘
```

---

## Components

### 1. integration_bridge.py
**Main integration bridge** connecting all subsystems.

- **WebSocket pipeline** for real-time sync
- **Latency monitoring** (<100ms target)
- **Bidirectional data flow**
- **MYCOSENTINEL integration** for environmental factors

```python
from v1_2.integration_bridge import IntegrationBridge

bridge = IntegrationBridge(ws_port=8765)
await bridge.initialize()
await bridge.start()
```

### 2. simulated_input.py
**EMG→Thought conversion** using SILENT_SIMULATOR.

- **Multi-user simulation** with distinct personas
- **Pattern-specific EMG** (subvocal, facial, neck)
- **Vocabulary expansion** for realistic thought text
- **Temporal smoothing** for natural flow

```python
from v1_2.simulated_input import SimulatedInputManager

manager = SimulatedInputManager(num_users=3)
await manager.start()
```

### 3. thought_to_simulation.py
**Thought→Particle export** for AETHER display.

- **Spatial clustering** of related thoughts
- **Particle target generation** (orbiting particles, trails)
- **Coordinate mapping** to AETHER volume
- **Semantic color encoding**

```python
from v1_2.thought_to_simulation import ThoughtGraphConverter

converter = ThoughtGraphConverter()
targets = converter.convert_thought_space(thought_space)
```

### 4. end_to_end_test.py
**Complete pipeline validation** with performance benchmarks.

```bash
python v1_2/end_to_end_test.py
```

Tests:
- EMG→Thought conversion latency
- Thought→Particle conversion latency
- Total pipeline latency (<100ms requirement)
- AETHER rendering performance
- MYCOSENTINEL integration

---

## Demo Scenarios

### Scenario 1: Creative Flow (`demo_scenarios/creative_flow.py`)

**Participants:** Designer, Writer, Architect  
**Focus:** Visual thinking, narrative, spatial concepts

```bash
python v1_2/demo_scenarios/creative_flow.py
```

### Scenario 2: Debugging Session (`demo_scenarios/debugging_session.py`)

**Participants:** Dev, QA, Architect  
**Focus:** Technical debugging, analysis phases

```bash
python v1_2/demo_scenarios/debugging_session.py
```

### Scenario 3: Planning Meeting (`demo_scenarios/planning_meeting.py`)

**Participants:** PM, Tech Lead, Designer, Stakeholder  
**Focus:** Collaborative project planning

```bash
python v1_2/demo_scenarios/planning_meeting.py
```

---

## Performance Benchmarks

| Metric | Target | Achieved |
|--------|--------|----------|
| EMG→Thought | <50ms | ~35ms |
| Thought→Particle | <40ms | ~28ms |
| **Total Pipeline** | **<100ms** | **~63ms** |
| WebSocket Sync | <100ms | ~15ms |

See `PERFORMANCE_RESULTS.md` for detailed analysis.

---

## WebSocket Protocol

### Connection
```javascript
ws://localhost:8765
```

### Messages

**Subscribe to state:**
```json
{"command": "get_state"}
```

**Run scenario:**
```json
{"command": "run_scenario", "scenario": "creative"}
```

**Receive state update:**
```json
{
  "type": "state_update",
  "data": {
    "thought_count": 42,
    "particle_count": 1024,
    "metrics": {
      "total_pipeline_avg_ms": 63.4
    }
  }
}
```

---

## UI Integration

The demo_app has been updated with **Simulation Mode toggle**:

1. Click **[Simulation Mode: OFF]** to enable
2. Select scenario from dropdown
3. Click **Run Scenario**
4. Watch real-time latency metrics

The toggle connects to `integration_bridge.py` WebSocket server on port 8765.

---

## Quick Start

```bash
# 1. Start the integration bridge
cd COGNITIVE-SYNC/v1.2
python integration_bridge.py

# 2. In another terminal, run a scenario
python demo_scenarios/creative_flow.py

# 3. Or open demo_app in browser
cd ../demo_app
python server.py
# Open http://localhost:8000
# Click "Simulation Mode" toggle
```

---

## File Structure

```
COGNITIVE-SYNC/v1.2/
├── integration_bridge.py      # Main bridge
├── simulated_input.py         # EMG input simulation
├── thought_to_simulation.py   # Particle export
├── end_to_end_test.py         # Validation tests
├── PERFORMANCE_RESULTS.md     # Benchmark report
├── README.md                  # This file
├── __init__.py
└── demo_scenarios/
    ├── creative_flow.py
    ├── debugging_session.py
    ├── planning_meeting.py
    └── __init__.py
```

---

## Requirements

```
# See hardware-simulator/requirements.txt
asyncio
websockets
numpy
```

---

## Next Steps

1. ✅ Run end-to-end tests: `python end_to_end_test.py`
2. ✅ Review performance: `cat PERFORMANCE_RESULTS.md`
3. ✅ Try scenarios: `python demo_scenarios/creative_flow.py`
4. 🔄 Deploy to staging for user testing
5. 🔄 Implement GPU acceleration for 100K+ particles

---

## License

MIT - See LICENSE file for details.
