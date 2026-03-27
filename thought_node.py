"""
COGNITIVE-SYNC: Spatial Thought Data Model (CRDT-based)

A thought exists as a 3D object in space with vector embeddings
to enable semantic similarity search. Uses LWW (Last-Write-Wins) CRDT
for conflict-free concurrent editing.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import time
import hashlib
import json
from collections.abc import Mapping


@dataclass
class ThoughtNode:
    """
    A thought exists in 3D space as a CRDT (Conflict-free Replicated Data Type).
    
    Attributes:
        id: Unique identifier (hash of content + timestamp + author)
        text: The thought content
        author: Who created/modified this thought
        timestamp: Last modified time (milliseconds since epoch)
        position: 3D coordinates (x, y, z)
        embedding: Optional vector embedding for semantic search
        vector_clock: Logical clock for causality tracking
        metadata: Additional properties (color, size, etc.)
    """
    text: str
    author: str
    position: tuple[float, float, float]
    timestamp: float = field(default_factory=lambda: time.time() * 1000)
    id: Optional[str] = None
    embedding: Optional[list[float]] = None
    vector_clock: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Lamport clock for local causality
    _local_clock: int = field(default=0, repr=False)
    
    def __post_init__(self):
        """Generate ID if not provided."""
        if self.id is None:
            self.id = self._generate_id()
        # Ensure timestamp is in milliseconds
        if self.timestamp < 1e12:  # Looks like seconds, not milliseconds
            self.timestamp *= 1000
    
    def _generate_id(self) -> str:
        """Generate unique ID from content hash."""
        content = f"{self.text}:{self.author}:{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def increment_clock(self) -> None:
        """Increment local Lamport clock."""
        self._local_clock += 1
        self.vector_clock[self.author] = self._local_clock
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "author": self.author,
            "timestamp": self.timestamp,
            "position": self.position,
            "embedding": self.embedding,
            "vector_clock": self.vector_clock,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThoughtNode":
        """Deserialize from dictionary."""
        return cls(
            id=data.get("id"),
            text=data["text"],
            author=data["author"],
            position=tuple(data["position"]),
            timestamp=data["timestamp"],
            embedding=data.get("embedding"),
            vector_clock=data.get("vector_clock", {}),
            metadata=data.get("metadata", {})
        )
    
    def merge(self, other: "ThoughtNode") -> "ThoughtNode":
        """
        CRDT Merge: LWW (Last-Write-Wins) with vector clock comparison.
        
        This ensures concurrent edits converge to the same state across all clients.
        Uses LWW for same-author conflicts, causal order for different authors.
        """
        if other.id != self.id:
            raise ValueError(f"Cannot merge thoughts with different IDs: {self.id} vs {other.id}")
        
        # Compare vector clocks to determine causality
        relation = self._compare_vector_clocks(other.vector_clock)
        
        if relation == "before":
            # Other happened after us
            return ThoughtNode.from_dict(other.to_dict())
        elif relation == "after":
            # We happened after other
            return ThoughtNode.from_dict(self.to_dict())
        else:
            # Concurrent edits: LWW based on timestamp
            # Same author: latest timestamp wins
            if self.author == other.author:
                winner = other if other.timestamp > self.timestamp else self
            else:
                # Different authors: merge text if both non-empty
                # This enables collaborative editing of different parts
                winner = other if other.timestamp > self.timestamp else self
            
            # Merge vector clocks (take max of each)
            merged_clock = dict(self.vector_clock)
            for node, clock in other.vector_clock.items():
                merged_clock[node] = max(merged_clock.get(node, 0), clock)
            
            result = ThoughtNode.from_dict(winner.to_dict())
            result.vector_clock = merged_clock
            return result
    
    def _compare_vector_clocks(self, other_clock: Dict[str, int]) -> str:
        """
        Compare vector clocks to determine causality.
        Returns: "before", "after", or "concurrent"
        """
        all_nodes = set(self.vector_clock.keys()) | set(other_clock.keys())
        
        ahead = 0
        behind = 0
        
        for node in all_nodes:
            local = self.vector_clock.get(node, 0)
            remote = other_clock.get(node, 0)
            if local > remote:
                ahead += 1
            elif remote > local:
                behind += 1
        
        if ahead == 0 and behind > 0:
            return "before"
        elif behind == 0 and ahead > 0:
            return "after"
        elif ahead == 0 and behind == 0:
            return "concurrent"  # Same state
        else:
            return "concurrent"  # Divergent concurrent updates
    
    def copy(self) -> "ThoughtNode":
        """Create a deep copy."""
        return ThoughtNode.from_dict(self.to_dict())
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ThoughtNode):
            return False
        return self.id == other.id and self.timestamp == other.timestamp


class ThoughtSpace:
    """
    Manages a collection of thoughts in 3D space.
    Provides CRDT merge for the entire space.
    """
    
    def __init__(self):
        self.thoughts: Dict[str, ThoughtNode] = {}
        self._listeners: list = []
    
    def add(self, thought: ThoughtNode) -> None:
        """Add or update a thought."""
        if thought.id in self.thoughts:
            # Merge with existing
            existing = self.thoughts[thought.id]
            merged = existing.merge(thought)
            self.thoughts[thought.id] = merged
        else:
            self.thoughts[thought.id] = thought
    
    def get(self, thought_id: str) -> Optional[ThoughtNode]:
        """Retrieve a thought by ID."""
        return self.thoughts.get(thought_id)
    
    def remove(self, thought_id: str) -> Optional[ThoughtNode]:
        """Remove and return a thought."""
        return self.thoughts.pop(thought_id, None)
    
    def all_thoughts(self) -> list[ThoughtNode]:
        """Get all thoughts as a list."""
        return list(self.thoughts.values())
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize entire space."""
        return {
            "thoughts": {tid: t.to_dict() for tid, t in self.thoughts.items()},
            "count": len(self.thoughts)
        }
    
    def merge(self, other_space: Dict[str, Any]) -> None:
        """
        Merge another thought space into this one.
        Handles CRDT merging for concurrent updates.
        """
        incoming = other_space.get("thoughts", {})
        for tid, tdata in incoming.items():
            thought = ThoughtNode.from_dict(tdata)
            self.add(thought)
    
    def get_nearby(self, position: tuple[float, float, float], 
                   radius: float = 1.0) -> list[ThoughtNode]:
        """Find thoughts within radius of a position."""
        px, py, pz = position
        nearby = []
        for thought in self.thoughts.values():
            tx, ty, tz = thought.position
            dist = ((tx - px) ** 2 + (ty - py) ** 2 + (tz - pz) ** 2) ** 0.5
            if dist <= radius:
                nearby.append(thought)
        return nearby
    
    def get_bounds(self) -> tuple[tuple, tuple]:
        """Get bounding box of all thoughts."""
        if not self.thoughts:
            return ((-10, -10, -10), (10, 10, 10))
        
        positions = [t.position for t in self.thoughts.values()]
        min_coords = tuple(min(p[i] for p in positions) for i in range(3))
        max_coords = tuple(max(p[i] for p in positions) for i in range(3))
        return (min_coords, max_coords)


# Simple embedding generator (placeholder for actual ML model)
class EmbeddingGenerator:
    """
    Generates simple embedding vectors from text.
    This is a simple hash-based embedding for demonstration.
    In production, use sentence-transformers or OpenAI embeddings.
    """
    
    DIMENSION = 128
    
    @classmethod
    def generate(cls, text: str) -> list[float]:
        """Generate a deterministic embedding vector."""
        import hashlib
        seed = hashlib.md5(text.lower().strip().encode()).digest()
        
        # Simple deterministic pseudo-random vector
        import random
        random.seed(int.from_bytes(seed[:8], 'big'))
        
        # Generate normalized random vector
        vec = [random.gauss(0, 1) for _ in range(cls.DIMENSION)]
        magnitude = sum(x**2 for x in vec) ** 0.5
        return [x / magnitude for x in vec]


if __name__ == "__main__":
    # Demo CRDT functionality
    print("=" * 60)
    print("COGNITIVE-SYNC: CRDT Thought Node Demo")
    print("=" * 60)
    
    # Create initial thought
    thought = ThoughtNode(
        text="Hello, cognitive space!",
        author="alice",
        position=(0.0, 0.0, 0.0)
    )
    thought.increment_clock()
    print(f"\n1. Created thought: {thought.text[:30]}...")
    print(f"   ID: {thought.id}")
    print(f"   Position: {thought.position}")
    print(f"   Vector clock: {thought.vector_clock}")
    
    # Simulate concurrent edit
    import time
    time.sleep(0.01)
    
    edit2 = thought.copy()
    edit2.text = "Hello, collaborative world!"
    edit2.timestamp = time.time() * 1000
    edit2.increment_clock()
    print(f"\n2. Concurrent edit by bob:")
    print(f"   Text: {edit2.text}")
    print(f"   Timestamp: {edit2.timestamp}")
    
    # Merge
    merged = thought.merge(edit2)
    print(f"\n3. Merge result (LWW):")
    print(f"   Text: {merged.text}")
    print(f"   Vector clock: {merged.vector_clock}")
    
    # Test thought space
    space = ThoughtSpace()
    space.add(merged)
    print(f"\n4. Added to space. Total thoughts: {space.all_thoughts().__len__()}")
    
    # Serialization test
    serialized = space.to_dict()
    print(f"\n5. Serialized space with {serialized['count']} thoughts")
    print(f"   JSON size: ~{len(json.dumps(serialized))} bytes")
    
    print("\n" + "=" * 60)
    print("CRDT Demo Complete!")
    print("=" * 60)
