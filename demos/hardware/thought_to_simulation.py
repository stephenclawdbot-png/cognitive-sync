"""
COGNITIVE-SYNC v1.2: Thought-to-Simulation Exporter

Exports COGNITIVE-SYNC thought graphs as particle targets for AETHER_SIMULATOR.
Converts semantic thought structures into volumetric display coordinates.

Features:
- Thought graph to particle cloud conversion
- Semantic clustering of related thoughts
- Dynamic particle target generation
- Real-time synchronization with AETHER volume
- Thought proximity visualization
"""

import asyncio
import json
import time
import math
import logging
from typing import Optional, Dict, Any, List, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("thought_to_simulation")

# Add paths for imports
WORKSPACE = Path("/Users/clawdbot/.openclaw/workspace")
COGNITIVE_PATH = WORKSPACE / "COGNITIVE-SYNC"
HARDWARE_PATH = WORKSPACE / "hardware-simulator"

sys.path.insert(0, str(COGNITIVE_PATH))
sys.path.insert(0, str(HARDWARE_PATH))

from thought_node import ThoughtNode, ThoughtSpace
from aether_sim import AetherSimulator, Particle, VolumeConfig


@dataclass
class ParticleTarget:
    """Target position for AETHER particle."""
    x: float
    y: float
    z: float
    intensity: float = 1.0
    hue: float = 0.0
    lifetime: float = 10.0
    thought_id: str = ""
    thought_text: str = ""
    cluster_id: Optional[str] = None


@dataclass
class ClusterConfig:
    """Configuration for thought clustering."""
    cluster_radius: float = 5.0
    min_cluster_size: int = 2
    attraction_strength: float = 0.5
    repulsion_strength: float = 0.3
    max_particles_per_thought: int = 50
    particle_density: float = 1.0


class ThoughtGraphConverter:
    """
    Converts COGNITIVE-SYNC thought graphs to AETHER particle systems.
    
    Algorithm:
    1. Extract thought positions from ThoughtSpace
    2. Cluster semantically related thoughts
    3. Generate particle targets for cluster centers
    4. Create particle trails for thought connections
    5. Scale to AETHER volume coordinates
    """
    
    def __init__(
        self,
        volume_config: Optional[VolumeConfig] = None,
        cluster_config: Optional[ClusterConfig] = None
    ):
        self.volume_config = volume_config or VolumeConfig()
        self.cluster_config = cluster_config or ClusterConfig()
        
        # Coordinate mapping
        self.thought_bounds = ((-15, -10, -5), (15, 10, 5))
        self.aether_bounds = (
            (0, 0, 0),
            (self.volume_config.width_mm,
             self.volume_config.height_mm,
             self.volume_config.depth_mm)
        )
        
        # State
        self.thought_clusters: Dict[str, List[str]] = {}
        self.cluster_centers: Dict[str, Tuple[float, float, float]] = {}
        self.particle_targets: Dict[str, ParticleTarget] = {}
        
        # Statistics
        self.stats = {
            "thoughts_processed": 0,
            "clusters_formed": 0,
            "particles_generated": 0
        }
        
        logger.info("ThoughtGraphConverter initialized")
    
    def convert_thought(
        self,
        thought: ThoughtNode,
        scale_to_volume: bool = True
    ) -> List[ParticleTarget]:
        """Convert a single thought to particle targets."""
        targets = []
        
        # Map thought position to AETHER volume
        if scale_to_volume:
            pos = self._map_to_volume(thought.position)
        else:
            pos = thought.position
        
        # Extract hue from metadata or generate from text
        hue = self._extract_hue(thought)
        
        # Create primary particle target at thought position
        primary = ParticleTarget(
            x=pos[0],
            y=pos[1],
            z=pos[2],
            intensity=self._calculate_intensity(thought),
            hue=hue,
            lifetime=30.0,
            thought_id=thought.id,
            thought_text=thought.text[:20]  # Truncate for display
        )
        targets.append(primary)
        
        # Generate orbiting particles for visual interest
        orbiting = self._generate_orbiting_particles(primary, thought)
        targets.extend(orbiting)
        
        # Generate trail particles if thought has momentum
        if self._has_momentum(thought):
            trailing = self._generate_trail_particles(primary, thought)
            targets.extend(trailing)
        
        self.stats["thoughts_processed"] += 1
        self.stats["particles_generated"] += len(targets)
        
        return targets
    
    def convert_thought_space(
        self,
        thought_space: ThoughtSpace
    ) -> Dict[str, List[ParticleTarget]]:
        """Convert entire thought space to particle targets."""
        all_targets: Dict[str, List[ParticleTarget]] = {}
        
        # Get all thoughts
        thoughts = thought_space.all_thoughts()
        
        # Clear old clusters
        self.thought_clusters.clear()
        self.cluster_centers.clear()
        
        # Form clusters
        clusters = self._cluster_thoughts(thoughts)
        self.stats["clusters_formed"] = len(clusters)
        
        # Convert each thought
        for thought in thoughts:
            targets = self.convert_thought(thought)
            
            # Assign to cluster
            cluster_id = self._find_cluster_for_thought(thought, clusters)
            for target in targets:
                target.cluster_id = cluster_id
            
            all_targets[thought.id] = targets
        
        # Add cluster center targets
        cluster_targets = self._generate_cluster_targets(clusters)
        all_targets["__clusters__"] = cluster_targets
        
        self.particle_targets = {
            t.thought_id: t for targets in all_targets.values() for t in targets
        }
        
        return all_targets
    
    def _map_to_volume(
        self,
        thought_pos: Tuple[float, float, float]
    ) -> Tuple[float, float, float]:
        """Map thought coordinates to AETHER volume coordinates."""
        thought_min, thought_max = self.thought_bounds
        aether_min, aether_max = self.aether_bounds
        
        # Linear mapping
        def map_coord(val, t_min, t_max, a_min, a_max):
            if t_max == t_min:
                return (a_min + a_max) / 2
            ratio = (val - t_min) / (t_max - t_min)
            return a_min + ratio * (a_max - a_min)
        
        return (
            map_coord(thought_pos[0], thought_min[0], thought_max[0], 
                     aether_min[0], aether_max[0]),
            map_coord(thought_pos[1], thought_min[1], thought_max[1], 
                     aether_min[1], aether_max[1]),
            map_coord(thought_pos[2], thought_min[2], thought_max[2], 
                     aether_min[2], aether_max[2])
        )
    
    def _extract_hue(self, thought: ThoughtNode) -> float:
        """Extract or generate color hue from thought."""
        # Check metadata
        if "color" in thought.metadata:
            color = thought.metadata["color"]
            return self._hex_to_hue(color)
        
        # Generate from text
        return self._text_to_hue(thought.text)
    
    def _hex_to_hue(self, hex_color: str) -> float:
        """Convert hex color to HSL hue."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        
        mx = max(r, g, b)
        mn = min(r, g, b)
        
        if mx == mn:
            return 0
        
        d = mx - mn
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        
        return (h * 60) % 360
    
    def _text_to_hue(self, text: str) -> float:
        """Generate deterministic hue from text."""
        # Hash text to generate consistent hue
        hash_val = hash(text) % 360
        return float(hash_val)
    
    def _calculate_intensity(self, thought: ThoughtNode) -> float:
        """Calculate particle intensity from thought metadata."""
        base = thought.metadata.get("emg_confidence", 0.7)
        
        # Boost intensity for certain states
        boost = 0.0
        if thought.metadata.get("emg_state") == "word_detected":
            boost = 0.2
        
        return min(1.0, base + boost)
    
    def _generate_orbiting_particles(
        self,
        center: ParticleTarget,
        thought: ThoughtNode,
        count: Optional[int] = None
    ) -> List[ParticleTarget]:
        """Generate orbiting particles around a thought."""
        count = count or int(self.cluster_config.particle_density * 8)
        targets = []
        
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = 10 + random.uniform(0, 5)
            
            targets.append(ParticleTarget(
                x=center.x + radius * math.cos(angle),
                y=center.y + radius * math.sin(angle),
                z=center.z + random.uniform(-5, 5),
                intensity=center.intensity * 0.7,
                hue=(center.hue + i * 10) % 360,
                lifetime=center.lifetime * 0.8,
                thought_id=thought.id,
                thought_text=""
            ))
        
        return targets
    
    def _has_momentum(self, thought: ThoughtNode) -> bool:
        """Check if thought has momentum for trail generation."""
        return "velocity" in thought.metadata
    
    def _generate_trail_particles(
        self,
        center: ParticleTarget,
        thought: ThoughtNode
    ) -> List[ParticleTarget]:
        """Generate trail particles behind moving thoughts."""
        targets = []
        velocity = thought.metadata.get("velocity", (0, 0, 0))
        speed = math.sqrt(sum(v**2 for v in velocity))
        
        if speed < 0.1:
            return targets
        
        # Generate trail in direction opposite to velocity
        for i in range(5):
            t = i / 5.0
            targets.append(ParticleTarget(
                x=center.x - velocity[0] * t * 2,
                y=center.y - velocity[1] * t * 2,
                z=center.z - velocity[2] * t * 2,
                intensity=center.intensity * (1 - t * 0.5),
                hue=center.hue,
                lifetime=center.lifetime * 0.5,
                thought_id=thought.id,
                thought_text=""
            ))
        
        return targets
    
    def _cluster_thoughts(
        self,
        thoughts: List[ThoughtNode]
    ) -> Dict[str, List[ThoughtNode]]:
        """Cluster thoughts based on spatial proximity."""
        clusters: Dict[str, List[ThoughtNode]] = {}
        unassigned = set(thoughts)
        cluster_id = 0
        
        while unassigned:
            # Start new cluster with first unassigned thought
            seed = unassigned.pop()
            cluster = [seed]
            cluster_center = seed.position
            
            # Find nearby thoughts
            for thought in list(unassigned):
                dist = self._distance(thought.position, cluster_center)
                if dist < self.cluster_config.cluster_radius:
                    cluster.append(thought)
                    unassigned.remove(thought)
                    # Update center
                    cluster_center = self._centroid([t.position for t in cluster])
            
            # Keep clusters above minimum size
            if len(cluster) >= self.cluster_config.min_cluster_size:
                c_id = f"cluster_{cluster_id}"
                clusters[c_id] = cluster
                self.thought_clusters[c_id] = [t.id for t in cluster]
                self.cluster_centers[c_id] = cluster_center
                cluster_id += 1
            else:
                # Add thoughts back to unassigned
                unassigned.update(cluster)
        
        return clusters
    
    def _find_cluster_for_thought(
        self,
        thought: ThoughtNode,
        clusters: Dict[str, List[ThoughtNode]]
    ) -> Optional[str]:
        """Find which cluster a thought belongs to."""
        for cluster_id, cluster_thoughts in clusters.items():
            if thought in cluster_thoughts:
                return cluster_id
        return None
    
    def _generate_cluster_targets(
        self,
        clusters: Dict[str, List[ThoughtNode]]
    ) -> List[ParticleTarget]:
        """Generate special particle targets for cluster centers."""
        targets = []
        
        for cluster_id, center in self.cluster_centers.items():
            # Map to volume
            pos = self._map_to_volume(center)
            
            # Get thoughts in cluster for color blending
            cluster_thoughts = clusters.get(cluster_id, [])
            avg_hue = sum(self._extract_hue(t) for t in cluster_thoughts) / len(cluster_thoughts) if cluster_thoughts else 180
            
            # Create cluster marker
            targets.append(ParticleTarget(
                x=pos[0],
                y=pos[1],
                z=pos[2],
                intensity=0.5,
                hue=avg_hue,
                lifetime=60.0,
                thought_id="__cluster_marker__",
                thought_text=f"Cluster {cluster_id}",
                cluster_id=cluster_id
            ))
        
        return targets
    
    def _distance(
        self,
        p1: Tuple[float, float, float],
        p2: Tuple[float, float, float]
    ) -> float:
        """Calculate Euclidean distance between positions."""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
    
    def _centroid(
        self,
        positions: List[Tuple[float, float, float]]
    ) -> Tuple[float, float, float]:
        """Calculate centroid of positions."""
        if not positions:
            return (0, 0, 0)
        
        return tuple(
            sum(p[i] for p in positions) / len(positions)
            for i in range(3)
        )
    
    def export_to_aether(
        self,
        aether_sim: AetherSimulator
    ) -> Dict[str, Any]:
        """Export particle targets to AETHER simulator."""
        particles_spawned = 0
        
        for target in self.particle_targets.values():
            # Spawn burst at target
            if target.thought_id != "__cluster_marker__":
                burst_size = int(target.intensity * 30)
                aether_sim.spawn_particle_burst(
                    count=burst_size,
                    position=(target.x, target.y, target.z)
                )
                particles_spawned += burst_size
            
            # Create swarm behavior
            aether_sim.create_swarm_behavior(
                center=(target.x, target.y, target.z),
                radius=20.0
            )
        
        return {
            "particles_spawned": particles_spawned,
            "swarms_created": len(self.particle_targets),
            "thoughts_visualized": len(set(t.thought_id for t in self.particle_targets.values()))
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get conversion statistics."""
        return self.stats.copy()


class RealtimeThoughtExporter:
    """
    Real-time exporter for streaming thoughts to AETHER.
    
    Uses async updates to maintain <100ms latency from
    thought creation to display.
    """
    
    def __init__(
        self,
        aether_sim: AetherSimulator,
        converter: Optional[ThoughtGraphConverter] = None
    ):
        self.aether = aether_sim
        self.converter = converter or ThoughtGraphConverter()
        
        self.buffered_thoughts: List[ThoughtNode] = []
        self.last_export_time = 0
        self.export_interval_ms = 50  # 50ms = 20Hz
        
        self.stats = {
            "exports": 0,
            "thoughts_exported": 0,
            "total_latency_ms": 0
        }
    
    async def update(self, thought_space: ThoughtSpace) -> None:
        """Update AETHER with latest thoughts."""
        now = time.time() * 1000
        
        if now - self.last_export_time < self.export_interval_ms:
            return
        
        self.last_export_time = now
        
        # Convert and export
        targets_dict = self.converter.convert_thought_space(thought_space)
        
        # Update AETHER
        for thought_id, targets in targets_dict.items():
            if thought_id == "__clusters__":
                continue
            
            for target in targets[:3]:  # Limit particles per thought
                burst_size = int(target.intensity * 20)
                self.aether.spawn_particle_burst(
                    count=burst_size,
                    position=(target.x, target.y, target.z)
                )
        
        self.stats["exports"] += 1
        self.stats["thoughts_exported"] += len(thought_space.all_thoughts())
    
    def get_latency_ms(self) -> float:
        """Get average export latency."""
        if self.stats["exports"] == 0:
            return 0
        return self.stats["total_latency_ms"] / self.stats["exports"]


def demo():
    """Run conversion demo."""
    print("=" * 70)
    print("COGNITIVE-SYNC v1.2: Thought-to-Simulation Demo")
    print("=" * 70)
    print()
    
    # Create sample thoughts
    thought_space = ThoughtSpace()
    
    sample_thoughts = [
        ("Explore new ideas", "user1", (5, 3, 1)),
        ("Analyze patterns", "user1", (6, 4, 1)),
        ("Connect concepts", "user1", (5, 5, 2)),
        ("Create solutions", "user2", (-5, -3, 0)),
        ("Design interface", "user2", (-6, -4, 1)),
        ("Build prototype", "user3", (0, 0, 0))
    ]
    
    for text, author, pos in sample_thoughts:
        thought = ThoughtNode(
            text=text,
            author=author,
            position=pos,
            metadata={"emg_confidence": 0.85}
        )
        thought_space.add(thought)
    
    print(f"Created {len(sample_thoughts)} sample thoughts")
    
    # Convert to particle targets
    converter = ThoughtGraphConverter()
    
    print("\nConverting to particle targets...")
    targets = converter.convert_thought_space(thought_space)
    
    print(f"\n{'='*70}")
    print("Conversion Results:")
    print(f"  Thoughts processed: {converter.stats['thoughts_processed']}")
    print(f"  Clusters formed: {converter.stats['clusters_formed']}")
    print(f"  Particle targets: {converter.stats['particles_generated']}")
    
    print(f"\nSample targets:")
    for thought_id, t_list in list(targets.items())[:3]:
        print(f"  {thought_id}: {len(t_list)} particles")
        for t in t_list[:2]:
            print(f"    @{t.x:.1f},{t.y:.1f},{t.z:.1f} hue={t.hue:.0f}")
    
    print(f"{'='*70}")


if __name__ == "__main__":
    demo()
