"""
ThoughtNode - Spatial data structure for 3D collaborative thoughts.

A thought is not just text - it's a spatial entity with position, momentum,
and relationships in a shared volumetric workspace.
"""

import uuid
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum, auto
import json


class ThoughtType(Enum):
    """Classification of thought types based on cognitive mode."""
    STREAM = auto()      # Fleeting, raw thought
    CONCEPT = auto()   # Structured idea
    QUESTION = auto()  # Inquiry
    CONNECTION = auto()  # Link between thoughts
    CLUSTER = auto()   # Aggregated thought group


@dataclass
class Vector3:
    """3D vector for spatial calculations."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def distance_to(self, other: 'Vector3') -> float:
        """Calculate Euclidean distance to another point."""
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**0.5
    
    def magnitude(self) -> float:
        """Vector magnitude (length)."""
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalize(self) -> 'Vector3':
        """Return unit vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)
    
    @classmethod
    def from_tuple(cls, t: Tuple[float, float, float]) -> 'Vector3':
        return cls(t[0], t[1], t[2])


@dataclass
class ThoughtStyle:
    """Visual styling for thoughts in 3D space."""
    # Color as RGB hex (e.g., "#FF5733")
    color: str = "#6366F1"
    opacity: float = 0.85
    size: float = 1.0  # Base scale
    pulse: bool = False  # Visual pulse animation
    glow: float = 0.0  # Glow intensity
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ThoughtStyle':
        return cls(**data)


@dataclass
class ThoughtPhysics:
    """Physical properties for emergent spatial behavior."""
    mass: float = 1.0  # Affects gravitational pull
    velocity: Vector3 = field(default_factory=Vector3)
    acceleration: Vector3 = field(default_factory=Vector3)
    friction: float = 0.98  # Damping factor
    bounciness: float = 0.3
    is_static: bool = False  # If True, physics doesn't affect it
    
    def update(self, dt: float = 0.016) -> None:
        """Update physics state (default ~60fps)."""
        if self.is_static:
            return
        self.velocity = self.velocity + self.acceleration * dt
        self.velocity = self.velocity * self.friction
        self.acceleration = Vector3(0, 0, 0)  # Reset acceleration
    
    def apply_force(self, force: Vector3) -> None:
        """Apply force (F = ma, so a = F/m)."""
        if self.mass > 0:
            self.acceleration = self.acceleration + force * (1.0 / self.mass)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'mass': self.mass,
            'velocity': asdict(self.velocity),
            'acceleration': asdict(self.acceleration),
            'friction': self.friction,
            'bounciness': self.bounciness,
            'is_static': self.is_static
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ThoughtPhysics':
        return cls(
            mass=data.get('mass', 1.0),
            velocity=Vector3(**data.get('velocity', {})),
            acceleration=Vector3(**data.get('acceleration', {})),
            friction=data.get('friction', 0.98),
            bounciness=data.get('bounciness', 0.3),
            is_static=data.get('is_static', False)
        )


class ThoughtNode:
    """
    A spatial thought entity in the COGNITIVE-SYNC system.
    
    Thoughts exist as first-class objects in 3D space with:
    - Position, velocity, and momentum
    - Connections to other thoughts
    - Visual styling and metadata
    - CRDT-compatible versioning
    """
    
    def __init__(
        self,
        content: str = "",
        position: Optional[Vector3] = None,
        thought_type: ThoughtType = ThoughtType.STREAM,
        author_id: str = "",
        style: Optional[ThoughtStyle] = None,
        physics: Optional[ThoughtPhysics] = None,
        node_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = node_id or str(uuid.uuid4())
        self.content = content
        self.position = position or Vector3()
        self.thought_type = thought_type
        self.author_id = author_id
        self.style = style or ThoughtStyle()
        self.physics = physics or ThoughtPhysics()
        
        # Temporal properties
        self.created_at = time.time_ns()
        self.modified_at = self.created_at
        self.version = 1  # CRDT version counter
        
        # Spatial relationships
        self.parent_id = parent_id  # For hierarchical relationships
        self.connections: Set[str] = set()  # IDs of connected thoughts
        self.connection_strength: Dict[str, float] = {}  # Weight of connections
        
        # Clustering
        self.cluster_id: Optional[str] = None
        
        # Additional metadata
        self.metadata = metadata or {}
        self.tags: Set[str] = set()
        
        # State flags
        self.is_deleted = False
        self.is_archived = False
    
    def update_position(self, new_position: Vector3, increment_version: bool = True) -> None:
        """Update spatial position."""
        self.position = new_position
        self.modified_at = time.time_ns()
        if increment_version:
            self.version += 1
    
    def update_content(self, new_content: str) -> None:
        """Update thought content."""
        self.content = new_content
        self.modified_at = time.time_ns()
        self.version += 1
    
    def add_connection(self, other_id: str, strength: float = 1.0) -> None:
        """Connect this thought to another."""
        self.connections.add(other_id)
        self.connection_strength[other_id] = strength
        self.modified_at = time.time_ns()
        self.version += 1
    
    def remove_connection(self, other_id: str) -> None:
        """Remove connection to another thought."""
        self.connections.discard(other_id)
        self.connection_strength.pop(other_id, None)
        self.modified_at = time.time_ns()
        self.version += 1
    
    def add_tag(self, tag: str) -> None:
        """Add semantic tag."""
        self.tags.add(tag.lower())
        self.modified_at = time.time_ns()
    
    def distance_to(self, other: 'ThoughtNode') -> float:
        """Calculate spatial distance to another thought."""
        return self.position.distance_to(other.position)
    
    def step_physics(self, dt: float = 0.016) -> None:
        """Advance physics simulation."""
        self.physics.update(dt)
        if not self.physics.is_static:
            self.position = self.position + self.physics.velocity * dt
            self.modified_at = time.time_ns()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary (CRDT-friendly)."""
        return {
            'id': self.id,
            'content': self.content,
            'position': asdict(self.position),
            'thought_type': self.thought_type.name,
            'author_id': self.author_id,
            'style': self.style.to_dict(),
            'physics': self.physics.to_dict(),
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'version': self.version,
            'parent_id': self.parent_id,
            'connections': list(self.connections),
            'connection_strength': self.connection_strength,
            'cluster_id': self.cluster_id,
            'metadata': self.metadata,
            'tags': list(self.tags),
            'is_deleted': self.is_deleted,
            'is_archived': self.is_archived
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ThoughtNode':
        """Deserialize from dictionary."""
        node = cls(
            content=data.get('content', ''),
            position=Vector3(**data.get('position', {})),
            thought_type=ThoughtType[data.get('thought_type', 'STREAM')],
            author_id=data.get('author_id', ''),
            style=ThoughtStyle.from_dict(data.get('style', {})),
            physics=ThoughtPhysics.from_dict(data.get('physics', {})),
            node_id=data.get('id'),
            parent_id=data.get('parent_id'),
            metadata=data.get('metadata', {})
        )
        node.created_at = data.get('created_at', time.time_ns())
        node.modified_at = data.get('modified_at', node.created_at)
        node.version = data.get('version', 1)
        node.connections = set(data.get('connections', []))
        node.connection_strength = data.get('connection_strength', {})
        node.cluster_id = data.get('cluster_id')
        node.tags = set(data.get('tags', []))
        node.is_deleted = data.get('is_deleted', False)
        node.is_archived = data.get('is_archived', False)
        return node
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), separators=(',', ':'))
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ThoughtNode':
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))
    
    def __repr__(self) -> str:
        return f"ThoughtNode(id={self.id[:8]}, content='{self.content[:30]}...', pos=({self.position.x:.2f}, {self.position.y:.2f}, {self.position.z:.2f}))"
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ThoughtNode):
            return False
        return self.id == other.id


class ThoughtCluster:
    """
    A cluster of thoughts that have grouped spatially/semantically.
    """
    
    def __init__(self, cluster_id: Optional[str] = None, label: str = ""):
        self.id = cluster_id or str(uuid.uuid4())
        self.label = label
        self.thought_ids: Set[str] = set()
        self.centroid = Vector3()
        self.radius = 0.0
        self.created_at = time.time_ns()
        self.density_score = 0.0
    
    def add_thought(self, thought: ThoughtNode) -> None:
        """Add a thought to this cluster."""
        self.thought_ids.add(thought.id)
        thought.cluster_id = self.id
        self._recalculate_geometry()
    
    def remove_thought(self, thought_id: str) -> None:
        """Remove a thought from this cluster."""
        self.thought_ids.discard(thought_id)
        self._recalculate_geometry()
    
    def _recalculate_geometry(self) -> None:
        """Recalculate cluster centroid and radius."""
        # Simplified - in real implementation would need all thought positions
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'label': self.label,
            'thought_ids': list(self.thought_ids),
            'centroid': asdict(self.centroid),
            'radius': self.radius,
            'created_at': self.created_at,
            'density_score': self.density_score
        }


class SpatialIndex:
    """
    R-tree inspired spatial index for efficient 3D queries.
    Simplified implementation for demonstration.
    """
    
    def __init__(self):
        self._thoughts: Dict[str, ThoughtNode] = {}
        self._clusters: Dict[str, ThoughtCluster] = {}
    
    def insert(self, thought: ThoughtNode) -> None:
        """Add thought to index."""
        self._thoughts[thought.id] = thought
    
    def remove(self, thought_id: str) -> Optional[ThoughtNode]:
        """Remove thought from index."""
        return self._thoughts.pop(thought_id, None)
    
    def get(self, thought_id: str) -> Optional[ThoughtNode]:
        """Get thought by ID."""
        return self._thoughts.get(thought_id)
    
    def get_all(self) -> List[ThoughtNode]:
        """Get all thoughts."""
        return list(self._thoughts.values())
    
    def query_range(
        self,
        center: Vector3,
        radius: float
    ) -> List[Tuple[ThoughtNode, float]]:
        """
        Query thoughts within spherical range.
        Returns list of (thought, distance) tuples.
        """
        results = []
        for thought in self._thoughts.values():
            dist = thought.position.distance_to(center)
            if dist <= radius:
                results.append((thought, dist))
        return sorted(results, key=lambda x: x[1])
    
    def query_nearest(
        self,
        point: Vector3,
        k: int = 5
    ) -> List[Tuple[ThoughtNode, float]]:
        """Get k nearest thoughts to point."""
        all_dists = [
            (thought, thought.position.distance_to(point))
            for thought in self._thoughts.values()
        ]
        return sorted(all_dists, key=lambda x: x[1])[:k]
    
    def find_nearby_for_connection(
        self,
        thought: ThoughtNode,
        max_distance: float = 10.0,
        max_results: int = 3
    ) -> List[ThoughtNode]:
        """Find thoughts that could connect to the given thought."""
        nearby = self.query_range(thought.position, max_distance)
        # Filter out self and already connected
        candidates = [
            t for t, dist in nearby
            if t.id != thought.id and t.id not in thought.connections
        ]
        return candidates[:max_results]
    
    def get_bounding_box(self) -> Optional[Tuple[Vector3, Vector3]]:
        """Get axis-aligned bounding box of all thoughts."""
        if not self._thoughts:
            return None
        
        positions = [t.position for t in self._thoughts.values()]
        min_x = min(p.x for p in positions)
        max_x = max(p.x for p in positions)
        min_y = min(p.y for p in positions)
        max_y = max(p.y for p in positions)
        min_z = min(p.z for p in positions)
        max_z = max(p.z for p in positions)
        
        return Vector3(min_x, min_y, min_z), Vector3(max_x, max_y, max_z)
    
    def clear(self) -> None:
        """Clear all indexed thoughts."""
        self._thoughts.clear()
        self._clusters.clear()
    
    def __len__(self) -> int:
        return len(self._thoughts)


if __name__ == "__main__":
    # Demo usage
    print("=== ThoughtNode Demo ===\n")
    
    # Create thoughts
    t1 = ThoughtNode(
        content="Spatial thinking is the future",
        position=Vector3(0, 0, 0),
        author_id="alice",
        thought_type=ThoughtType.CONCEPT
    )
    
    t2 = ThoughtNode(
        content="Ideas need room to breathe",
        position=Vector3(3, 2, 1),
        author_id="bob",
        thought_type=ThoughtType.STREAM
    )
    
    # Connect them
    t1.add_connection(t2.id, strength=0.8)
    t2.add_connection(t1.id, strength=0.8)
    
    print(f"Thought 1: {t1}")
    print(f"Thought 2: {t2}")
    print(f"Distance: {t1.distance_to(t2):.2f}\n")
    
    # Test spatial index
    index = SpatialIndex()
    index.insert(t1)
    index.insert(t2)
    
    print(f"Index size: {len(index)}")
    
    # Query nearby
    origin = Vector3(0, 0, 0)
    nearby = index.query_range(origin, 5.0)
    print(f"Thoughts within 5 units of origin: {len(nearby)}")
    
    # JSON serialization
    print("\n=== JSON Serialization ===")
    json_data = t1.to_json()
    print(f"Serialized (truncated): {json_data[:200]}...")
    
    t1_restored = ThoughtNode.from_json(json_data)
    print(f"Restored: {t1_restored}")
    print(f"Match: {t1.id == t1_restored.id and t1.content == t1_restored.content}")
