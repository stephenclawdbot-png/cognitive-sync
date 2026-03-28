"""
COGNITIVE-SYNC v1.1: Real-Time Thought Graph Renderer

Handles:
- 3D graph layout calculation
- Thought connectivity analysis
- Force-directed positioning
- Spatial clustering and region detection

This module provides the backend logic for visualization;
the actual rendering is done in the frontend using Three.js
"""

import math
import random
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np


@dataclass
class GraphNode:
    """A node in the thought graph."""
    id: str
    position: Tuple[float, float, float]
    velocity: Tuple[float, float, float] = field(default_factory=lambda: (0.0, 0.0, 0.0))
    mass: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Visualization properties
    size: float = 1.0
    glow: float = 0.5
    pulse_phase: float = 0.0


@dataclass
class GraphEdge:
    """A connection between thoughts."""
    source_id: str
    target_id: str
    strength: float = 1.0
    
    # Temporal distance (for chronological connections)
    temporal_weight: float = 0.0


class ForceDirectedLayout:
    """
    Force-directed graph layout for 3D thought visualization.
    
    Forces applied:
    - Repulsion: Nodes push away from each other
    - Attraction: Edges pull connected nodes together
    - Centering: Gravity toward center of space
    - Temporal: Time-adjacent thoughts attract
    """
    
    def __init__(
        self,
        repulsion_strength: float = 100.0,
        attraction_strength: float = 0.05,
        centering_strength: float = 0.01,
        damping: float = 0.9,
        min_distance: float = 2.0
    ):
        self.repulsion = repulsion_strength
        self.attraction = attraction_strength
        self.centering = centering_strength
        self.damping = damping
        self.min_distance = min_distance
        
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self.temperature = 1.0
    
    def add_node(self, node_id: str, position: Tuple[float, float, float], **kwargs) -> None:
        """Add a node to the graph."""
        if node_id not in self.nodes:
            self.nodes[node_id] = GraphNode(
                id=node_id,
                position=position,
                metadata=kwargs
            )
    
    def add_edge(self, source_id: str, target_id: str, strength: float = 1.0) -> None:
        """Add an edge between two nodes."""
        if source_id in self.nodes and target_id in self.nodes:
            self.edges.append(GraphEdge(source_id, target_id, strength))
    
    def step(self, dt: float = 0.016) -> float:
        """
        Perform one simulation step.
        Returns average movement magnitude.
        """
        total_movement = 0.0
        
        # Calculate forces for each node
        forces = {nid: np.array([0.0, 0.0, 0.0]) for nid in self.nodes}
        
        # Repulsion (all pairs)
        node_ids = list(self.nodes.keys())
        for i, nid1 in enumerate(node_ids):
            for nid2 in node_ids[i+1:]:
                n1 = self.nodes[nid1]
                n2 = self.nodes[nid2]
                
                pos1 = np.array(n1.position)
                pos2 = np.array(n2.position)
                
                diff = pos1 - pos2
                dist = np.linalg.norm(diff)
                
                if dist < 0.1:
                    diff = np.random.randn(3) * 0.1
                    dist = 0.1
                
                if dist < self.min_distance * 3:
                    force = self.repulsion / (dist ** 2)
                    direction = diff / dist
                    
                    forces[nid1] += direction * force
                    forces[nid2] -= direction * force
        
        # Attraction (edges)
        for edge in self.edges:
            n1 = self.nodes.get(edge.source_id)
            n2 = self.nodes.get(edge.target_id)
            
            if n1 and n2:
                pos1 = np.array(n1.position)
                pos2 = np.array(n2.position)
                
                diff = pos2 - pos1
                dist = np.linalg.norm(diff)
                
                if dist > 0:
                    force = self.attraction * edge.strength * dist
                    direction = diff / dist
                    
                    forces[edge.source_id] += direction * force
                    forces[edge.target_id] -= direction * force
        
        # Centering gravity
        if self.nodes:
            center = np.mean([np.array(n.position) for n in self.nodes.values()], axis=0)
            for nid, node in self.nodes.items():
                to_center = center - np.array(node.position)
                forces[nid] += to_center * self.centering
        
        # Apply forces with temperature cooling
        self.temperature = max(0.1, self.temperature * 0.995)
        
        for nid, node in self.nodes.items():
            force = forces[nid]
            
            # Update velocity
            vx, vy, vz = node.velocity
            vx = (vx + force[0] * dt) * self.damping
            vy = (vy + force[1] * dt) * self.damping
            vz = (vz + force[2] * dt) * self.damping
            
            node.velocity = (vx, vy, vz)
            
            # Update position
            old_pos = np.array(node.position)
            new_pos = old_pos + np.array([vx, vy, vz]) * self.temperature * dt
            
            # Constrain to reasonable bounds
            new_pos = np.clip(new_pos, -50, 50)
            
            node.position = tuple(new_pos)
            
            # Track movement
            movement = np.linalg.norm(new_pos - old_pos)
            total_movement += movement
        
        return total_movement / len(self.nodes) if self.nodes else 0.0


class ThoughtClusterer:
    """
    Spatial clustering of thoughts for region detection.
    """
    
    def __init__(self, cluster_radius: float = 5.0):
        self.radius = cluster_radius
        self.clusters: List[Dict] = []
    
    def cluster_thoughts(self, thoughts: List[Dict]) -> List[Dict]:
        """
        Group thoughts into spatial clusters using simple DBSCAN-like algorithm.
        """
        if not thoughts:
            return []
        
        clusters = []
        visited = set()
        
        for i, thought in enumerate(thoughts):
            if i in visited:
                continue
            
            # Find all thoughts within radius
            cluster_thoughts = [thought]
            visited.add(i)
            
            for j, other in enumerate(thoughts):
                if j in visited:
                    continue
                
                pos1 = thought.get("position", (0, 0, 0))
                pos2 = other.get("position", (0, 0, 0))
                
                dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
                
                if dist <= self.radius:
                    cluster_thoughts.append(other)
                    visited.add(j)
            
            if len(cluster_thoughts) >= 2:
                # Calculate cluster center
                positions = [t.get("position", (0, 0, 0)) for t in cluster_thoughts]
                center = tuple(sum(p[i] for p in positions) / len(positions) for i in range(3))
                
                # Extract common keywords
                texts = [t.get("text", "") for t in cluster_thoughts]
                
                clusters.append({
                    "id": f"cluster_{len(clusters)}",
                    "center": center,
                    "thoughts": cluster_thoughts,
                    "count": len(cluster_thoughts),
                    "keywords": self._extract_keywords(texts)
                })
        
        self.clusters = clusters
        return clusters
    
    def _extract_keywords(self, texts: List[str]) -> List[str]:
        """Extract common keywords from text."""
        words = []
        for text in texts:
            words.extend(text.lower().split())
        
        word_counts = defaultdict(int)
        for word in words:
            if len(word) > 2:
                word_counts[word] += 1
        
        # Return top 3
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [w for w, c in sorted_words[:3]]


class ThoughtVisualizer:
    """
    Main visualization controller that coordinates
    layout, clustering, and rendering preparation.
    """
    
    def __init__(self):
        self.layout = ForceDirectedLayout()
        self.clusterer = ThoughtClusterer()
        self.thoughts: Dict[str, Dict] = {}
        self.user_positions: Dict[str, Tuple] = {}
        
        # Animation state
        self.time = 0.0
        self.pulse_speed = 2.0
    
    def add_thought(self, thought_data: Dict) -> None:
        """Add a thought to the visualization."""
        thought_id = thought_data.get("thought_id")
        if not thought_id:
            return
        
        position = thought_data.get("position", (0, 0, 0))
        emg_state = thought_data.get("emg_state", "rest")
        
        # Map EMG state to visual properties
        visual_props = self._get_state_visuals(emg_state)
        
        self.thoughts[thought_id] = {
            **thought_data,
            "visual_props": visual_props,
            "added_time": time.time()
        }
        
        # Add to force-directed layout
        self.layout.add_node(thought_id, position, **thought_data)
    
    def _get_state_visuals(self, emg_state: str) -> Dict:
        """Get visual properties based on EMG state."""
        visuals = {
            "rest": {
                "color": [0.3, 0.8, 0.6],
                "size": 0.8,
                "glow": 0.2,
                "pulse": False
            },
            "thinking": {
                "color": [0.9, 0.7, 0.3],
                "size": 1.0,
                "glow": 0.6,
                "pulse": True,
                "pulse_speed": 2.0
            },
            "word_detected": {
                "color": [1.0, 0.4, 0.8],
                "size": 1.3,
                "glow": 1.0,
                "pulse": True,
                "pulse_speed": 4.0
            }
        }
        return visuals.get(emg_state, visuals["rest"])
    
    def update_user_position(self, user_id: str, position: Tuple) -> None:
        """Update user position."""
        self.user_positions[user_id] = position
    
    def update(self, dt: float = 0.016) -> None:
        """Update visualization state."""
        self.time += dt
        
        # Update force-directed layout
        self.layout.step(dt)
        
        # Update thought positions from layout
        for thought_id, node in self.layout.nodes.items():
            if thought_id in self.thoughts:
                self.thoughts[thought_id]["position"] = node.position
    
    def get_render_data(self) -> Dict:
        """
        Get data formatted for frontend rendering.
        """
        thoughts_list = []
        for thought_id, data in self.thoughts.items():
            visual = data.get("visual_props", {})
            
            # Calculate pulse
            pulse = 0.0
            if visual.get("pulse"):
                pulse = (math.sin(self.time * visual.get("pulse_speed", 2.0)) + 1) / 2
            
            thoughts_list.append({
                "id": thought_id,
                "text": data.get("text", ""),
                "position": data.get("position", (0, 0, 0)),
                "color": data.get("color", "#ffffff"),
                "emg_state": data.get("emg_state", "rest"),
                "confidence": data.get("confidence", 0.5),
                "user_name": data.get("metadata", {}).get("user_name", "Anonymous"),
                "size": visual.get("size", 1.0) * (1 + pulse * 0.2),
                "glow": visual.get("glow", 0.5) * (0.5 + pulse * 0.5),
                "age": time.time() - data.get("added_time", time.time())
            })
        
        # Add users
        users_list = []
        for user_id, pos in self.user_positions.items():
            users_list.append({
                "id": user_id,
                "position": pos,
                "type": "user"
            })
        
        # Generate connections based on proximity
        connections = self._generate_connections(thoughts_list)
        
        return {
            "thoughts": thoughts_list,
            "users": users_list,
            "connections": connections,
            "timestamp": time.time(),
            "count": len(thoughts_list)
        }
    
    def _generate_connections(self, thoughts: List[Dict]) -> List[Dict]:
        """Generate connections between nearby thoughts."""
        connections = []
        
        for i, t1 in enumerate(thoughts):
            for t2 in thoughts[i+1:]:
                p1 = t1["position"]
                p2 = t2["position"]
                
                dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
                
                if dist < 8:  # Connect nearby thoughts
                    connections.append({
                        "source": t1["id"],
                        "target": t2["id"],
                        "distance": dist,
                        "opacity": 1.0 - (dist / 8)
                    })
        
        return connections
    
    def get_clusters(self) -> List[Dict]:
        """Get current spatial clusters."""
        thoughts_list = list(self.thoughts.values())
        return self.clusterer.cluster_thoughts(thoughts_list)
    
    def export_frame(self) -> Dict:
        """Export current frame for recording/playback."""
        return {
            "timestamp": time.time(),
            "thoughts": self.get_render_data(),
            "clusters": self.get_clusters()
        }


class SessionRecorder:
    """
    Records visualization sessions for later replay.
    """
    
    def __init__(self, visualizer: ThoughtVisualizer):
        self.visualizer = visualizer
        self.frames: List[Dict] = []
        self.recording = False
        self.fps = 30
    
    def start(self) -> None:
        """Start recording."""
        self.frames = []
        self.recording = True
        print("Session recording started")
    
    def stop(self) -> Dict:
        """Stop recording and return recorded data."""
        self.recording = False
        return {
            "frame_count": len(self.frames),
            "duration": len(self.frames) / self.fps,
            "frames": self.frames
        }
    
    def record_frame(self) -> None:
        """Record current frame if recording."""
        if self.recording:
            self.frames.append(self.visualizer.export_frame())
    
    def save(self, filepath: str) -> None:
        """Save recorded session to file."""
        import json
        data = self.stop()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Session saved to {filepath}")


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("ThoughtVisualizer Demo")
    print("=" * 60)
    
    visualizer = ThoughtVisualizer()
    
    # Add sample thoughts
    for i in range(20):
        visualizer.add_thought({
            "thought_id": f"thought_{i}",
            "text": f"Thought {i}",
            "position": (
                random.uniform(-10, 10),
                random.uniform(-10, 10),
                random.uniform(-5, 5)
            ),
            "emg_state": random.choice(["rest", "thinking", "word_detected"]),
            "confidence": random.uniform(0.5, 0.95),
            "color": random.choice(["#64ffd8", "#ff64d8", "#64aaff"]),
            "metadata": {"user_name": f"User_{i % 3}"}
        })
    
    # Run simulation
    print("\nRunning layout simulation...")
    for step in range(100):
        visualizer.update(dt=0.016)
    
    # Get render data
    data = visualizer.get_render_data()
    print(f"\nGenerated render data:")
    print(f"  Thoughts: {data['count']}")
    print(f"  Connections: {len(data['connections'])}")
    
    clusters = visualizer.get_clusters()
    print(f"  Clusters: {len(clusters)}")
    
    print("\nDemo complete!")
