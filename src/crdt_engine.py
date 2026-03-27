"""
CRDT Engine - Conflict-free Replicated Data Types for COGNITIVE-SYNC.

Implements a Yjs-style state-based CRDT for:
- Thought creation/deletion
- Concurrent position updates
- Connection management
- Multi-user synchronization without locks
"""

import asyncio
from typing import Dict, List, Set, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import time
import json

from thought_node import ThoughtNode, ThoughtType, Vector3, ThoughtStyle, ThoughtPhysics


@dataclass
class VectorClock:
    """
    Vector clock for causal ordering of events.
    Maps node_id -> logical timestamp.
    """
    clocks: Dict[str, int] = field(default_factory=dict)
    
    def increment(self, node_id: str) -> None:
        """Increment clock for local node."""
        self.clocks[node_id] = self.clocks.get(node_id, 0) + 1
    
    def merge(self, other: 'VectorClock') -> 'VectorClock':
        """Merge two vector clocks (taking element-wise max)."""
        merged = VectorClock()
        all_nodes = set(self.clocks.keys()) | set(other.clocks.keys())
        for node in all_nodes:
            merged.clocks[node] = max(
                self.clocks.get(node, 0),
                other.clocks.get(node, 0)
            )
        return merged
    
    def compare(self, other: 'VectorClock') -> int:
        """
        Compare two vector clocks.
        Returns: -1 (other is newer), 0 (concurrent), 1 (self is newer)
        """
        dominates = False
        dominated = False
        
        all_nodes = set(self.clocks.keys()) | set(other.clocks.keys())
        for node in all_nodes:
            self_val = self.clocks.get(node, 0)
            other_val = other.clocks.get(node, 0)
            if self_val > other_val:
                dominates = True
            elif other_val > self_val:
                dominated = True
        
        if dominates and not dominated:
            return 1
        elif dominated and not dominates:
            return -1
        else:
            return 0  # Concurrent or equal
    
    def to_dict(self) -> Dict[str, int]:
        return self.clocks.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'VectorClock':
        return cls(clocks=data)


class CRDTOperation:
    """Base class for CRDT operations."""
    
    TYPE_CREATE = "create"
    TYPE_UPDATE = "update"
    TYPE_DELETE = "delete"
    TYPE_CONNECT = "connect"
    TYPE_DISCONNECT = "disconnect"
    
    def __init__(
        self,
        op_type: str,
        thought_id: str,
        timestamp: int,
        vector_clock: VectorClock,
        author_id: str,
        payload: Dict[str, Any]
    ):
        self.op_type = op_type
        self.thought_id = thought_id
        self.timestamp = timestamp
        self.vector_clock = vector_clock
        self.author_id = author_id
        self.payload = payload
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'op_type': self.op_type,
            'thought_id': self.thought_id,
            'timestamp': self.timestamp,
            'vector_clock': self.vector_clock.to_dict(),
            'author_id': self.author_id,
            'payload': self.payload
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CRDTOperation':
        return cls(
            op_type=data['op_type'],
            thought_id=data['thought_id'],
            timestamp=data['timestamp'],
            vector_clock=VectorClock.from_dict(data['vector_clock']),
            author_id=data['author_id'],
            payload=data.get('payload', {})
        )


class LastWriteWinsRegister:
    """
    LWW-Register CRDT for single-value fields.
    Each update has a timestamp and vector clock.
    Winner determined by: timestamp > vector_clock > node_id
    """
    
    def __init__(self):
        self.value: Any = None
        self.timestamp: int = 0
        self.vector_clock: Optional[VectorClock] = None
        self.author_id: str = ""
    
    def update(self, value: Any, timestamp: int, clock: VectorClock, author_id: str) -> bool:
        """
        Attempt to update register. Returns True if update was applied.
        """
        should_update = False
        
        if self.vector_clock is None:
            should_update = True
        elif timestamp > self.timestamp:
            should_update = True
        elif timestamp == self.timestamp:
            # Tie-breaker: compare vector clocks
            cmp = self.vector_clock.compare(clock)
            if cmp < 0:  # Other is newer
                should_update = True
            elif cmp == 0:  # Concurrent - use lexicographic author_id
                should_update = author_id > self.author_id
        
        if should_update:
            self.value = value
            self.timestamp = timestamp
            self.vector_clock = clock
            self.author_id = author_id
            return True
        return False
    
    def get(self) -> Any:
        return self.value


class AddWinsSet:
    """
    Add-Wins Set CRDT for collections (tags, connections).
    Add beats remove when concurrent.
    """
    
    def __init__(self):
        # Map: element -> (timestamp, author_id)
        self.adds: Dict[Any, Tuple[int, str]] = {}
        self.removes: Dict[Any, Tuple[int, str]] = {}
    
    def add(self, element: Any, timestamp: int, author_id: str) -> bool:
        """Add element to set."""
        if element not in self.adds or timestamp > self.adds[element][0]:
            self.adds[element] = (timestamp, author_id)
            return True
        return False
    
    def remove(self, element: Any, timestamp: int, author_id: str) -> bool:
        """Remove element from set."""
        if element not in self.removes or timestamp > self.removes[element][0]:
            self.removes[element] = (timestamp, author_id)
            return True
        return False
    
    def contains(self, element: Any) -> bool:
        """Check if element is in set (add-wins semantics)."""
        if element not in self.adds:
            return False
        
        add_time = self.adds[element][0]
        remove_time = self.removes.get(element, (0, ''))[0]
        
        # Add wins on ties
        return add_time >= remove_time
    
    def get_elements(self) -> Set[Any]:
        """Get all elements currently in set."""
        return {e for e in self.adds if self.contains(e)}
    
    def merge(self, other: 'AddWinsSet') -> 'AddWinsSet':
        """Merge two sets."""
        merged = AddWinsSet()
        merged.adds = {**self.adds, **other.adds}
        merged.removes = {**self.removes, **other.removes}
        return merged


class CRDTThoughtState:
    """
    CRDT-enabled state container for a single thought.
    Each field uses appropriate CRDT type:
    - Content/Position: LWW-Register
    - Tags/Connections: AddWinsSet
    - Deleted flag: LWW-Register
    """
    
    def __init__(self, thought_id: str):
        self.thought_id = thought_id
        self.content = LastWriteWinsRegister()
        self.position = LastWriteWinsRegister()  # Stores Vector3
        self.style = LastWriteWinsRegister()  # Stores ThoughtStyle
        self.physics = LastWriteWinsRegister()  # Stores ThoughtPhysics
        self.tags = AddWinsSet()
        self.connections = AddWinsSet()
        self.connection_strength: Dict[str, LastWriteWinsRegister] = {}
        self.is_deleted = LastWriteWinsRegister()
        self.metadata = LastWriteWinsRegister()  # Stores Dict
        
        # Initialize with defaults
        self.is_deleted.update(False, 0, VectorClock(), "system")
    
    def apply_operation(self, op: CRDTOperation) -> bool:
        """Apply a CRDT operation to this thought state."""
        modified = False
        
        if op.op_type == CRDTOperation.TYPE_CREATE:
            # Initialize thought fields
            if 'content' in op.payload:
                modified |= self.content.update(
                    op.payload['content'], op.timestamp, op.vector_clock, op.author_id
                )
            if 'position' in op.payload:
                pos = Vector3(**op.payload['position'])
                modified |= self.position.update(
                    pos, op.timestamp, op.vector_clock, op.author_id
                )
            if 'style' in op.payload:
                style = ThoughtStyle.from_dict(op.payload['style'])
                modified |= self.style.update(
                    style, op.timestamp, op.vector_clock, op.author_id
                )
            if 'physics' in op.payload:
                physics = ThoughtPhysics.from_dict(op.payload['physics'])
                modified |= self.physics.update(
                    physics, op.timestamp, op.vector_clock, op.author_id
                )
        
        elif op.op_type == CRDTOperation.TYPE_UPDATE:
            field = op.payload.get('field')
            value = op.payload.get('value')
            
            if field == 'content':
                modified |= self.content.update(
                    value, op.timestamp, op.vector_clock, op.author_id
                )
            elif field == 'position':
                pos = Vector3(**value)
                modified |= self.position.update(
                    pos, op.timestamp, op.vector_clock, op.author_id
                )
            elif field == 'style':
                style = ThoughtStyle.from_dict(value)
                modified |= self.style.update(
                    style, op.timestamp, op.vector_clock, op.author_id
                )
            elif field == 'metadata':
                modified |= self.metadata.update(
                    value, op.timestamp, op.vector_clock, op.author_id
                )
        
        elif op.op_type == CRDTOperation.TYPE_DELETE:
            modified |= self.is_deleted.update(
                True, op.timestamp, op.vector_clock, op.author_id
            )
        
        elif op.op_type == CRDTOperation.TYPE_CONNECT:
            other_id = op.payload.get('other_id')
            strength = op.payload.get('strength', 1.0)
            if self.connections.add(other_id, op.timestamp, op.author_id):
                modified = True
                # Update strength
                if other_id not in self.connection_strength:
                    self.connection_strength[other_id] = LastWriteWinsRegister()
                self.connection_strength[other_id].update(
                    strength, op.timestamp, op.vector_clock, op.author_id
                )
        
        elif op.op_type == CRDTOperation.TYPE_DISCONNECT:
            other_id = op.payload.get('other_id')
            modified |= self.connections.remove(other_id, op.timestamp, op.author_id)
        
        return modified
    
    def to_thought_node(self) -> Optional[ThoughtNode]:
        """Convert CRDT state back to ThoughtNode."""
        if self.is_deleted.get():
            return None
        
        content = self.content.get() or ""
        position = self.position.get() or Vector3()
        style = self.style.get() or ThoughtStyle()
        physics = self.physics.get() or ThoughtPhysics()
        
        node = ThoughtNode(
            content=content,
            position=position,
            thought_type=ThoughtType.STREAM,
            node_id=self.thought_id,
            style=style,
            physics=physics
        )
        
        node.connections = self.connections.get_elements()
        node.connection_strength = {
            k: v.get() for k, v in self.connection_strength.items() if v.get() is not None
        }
        node.is_deleted = False
        
        return node


class CRDTDocument:
    """
    Container for all CRDT thought states.
    Manages the full document state for synchronization.
    """
    
    def __init__(self, site_id: str):
        self.site_id = site_id
        self.thoughts: Dict[str, CRDTThoughtState] = {}
        self.vector_clock = VectorClock()
        self.operation_log: List[CRDTOperation] = []
        self._operation_callbacks: List[Callable[[CRDTOperation], None]] = []
    
    def register_callback(self, callback: Callable[[CRDTOperation], None]) -> None:
        """Register callback for new operations."""
        self._operation_callbacks.append(callback)
    
    def _notify_callbacks(self, op: CRDTOperation) -> None:
        """Notify all registered callbacks."""
        for cb in self._operation_callbacks:
            try:
                cb(op)
            except Exception:
                pass
    
    def create_thought(
        self,
        thought_id: str,
        content: str,
        position: Vector3,
        author_id: str,
        style: Optional[ThoughtStyle] = None,
        physics: Optional[ThoughtPhysics] = None
    ) -> CRDTOperation:
        """Create a new thought in the document."""
        self.vector_clock.increment(self.site_id)
        
        if thought_id not in self.thoughts:
            self.thoughts[thought_id] = CRDTThoughtState(thought_id)
        
        payload = {
            'content': content,
            'position': {'x': position.x, 'y': position.y, 'z': position.z}
        }
        if style:
            payload['style'] = style.to_dict()
        if physics:
            payload['physics'] = physics.to_dict()
        
        op = CRDTOperation(
            op_type=CRDTOperation.TYPE_CREATE,
            thought_id=thought_id,
            timestamp=time.time_ns(),
            vector_clock=VectorClock(self.vector_clock.clocks.copy()),
            author_id=author_id,
            payload=payload
        )
        
        self.thoughts[thought_id].apply_operation(op)
        self.operation_log.append(op)
        self._notify_callbacks(op)
        return op
    
    def update_thought(
        self,
        thought_id: str,
        field: str,
        value: Any,
        author_id: str
    ) -> Optional[CRDTOperation]:
        """Update a field of an existing thought."""
        if thought_id not in self.thoughts:
            return None
        
        self.vector_clock.increment(self.site_id)
        
        payload = {'field': field, 'value': value}
        
        op = CRDTOperation(
            op_type=CRDTOperation.TYPE_UPDATE,
            thought_id=thought_id,
            timestamp=time.time_ns(),
            vector_clock=VectorClock(self.vector_clock.clocks.copy()),
            author_id=author_id,
            payload=payload
        )
        
        if self.thoughts[thought_id].apply_operation(op):
            self.operation_log.append(op)
            self._notify_callbacks(op)
            return op
        return None
    
    def delete_thought(self, thought_id: str, author_id: str) -> Optional[CRDTOperation]:
        """Mark a thought as deleted."""
        if thought_id not in self.thoughts:
            return None
        
        self.vector_clock.increment(self.site_id)
        
        op = CRDTOperation(
            op_type=CRDTOperation.TYPE_DELETE,
            thought_id=thought_id,
            timestamp=time.time_ns(),
            vector_clock=VectorClock(self.vector_clock.clocks.copy()),
            author_id=author_id,
            payload={}
        )
        
        if self.thoughts[thought_id].apply_operation(op):
            self.operation_log.append(op)
            self._notify_callbacks(op)
            return op
        return None
    
    def connect_thoughts(
        self,
        thought_id1: str,
        thought_id2: str,
        author_id: str,
        strength: float = 1.0
    ) -> Optional[CRDTOperation]:
        """Create a connection between two thoughts."""
        if thought_id1 not in self.thoughts or thought_id2 not in self.thoughts:
            return None
        
        self.vector_clock.increment(self.site_id)
        
        op = CRDTOperation(
            op_type=CRDTOperation.TYPE_CONNECT,
            thought_id=thought_id1,
            timestamp=time.time_ns(),
            vector_clock=VectorClock(self.vector_clock.clocks.copy()),
            author_id=author_id,
            payload={'other_id': thought_id2, 'strength': strength}
        )
        
        if self.thoughts[thought_id1].apply_operation(op):
            self.operation_log.append(op)
            self._notify_callbacks(op)
            return op
        return None
    
    def apply_remote_operation(self, op: CRDTOperation) -> bool:
        """Apply an operation from a remote site."""
        # Merge remote clock into our clock
        self.vector_clock = self.vector_clock.merge(op.vector_clock)
        
        # Ensure thought state exists
        if op.thought_id not in self.thoughts:
            self.thoughts[op.thought_id] = CRDTThoughtState(op.thought_id)
        
        return self.thoughts[op.thought_id].apply_operation(op)
    
    def get_thought(self, thought_id: str) -> Optional[ThoughtNode]:
        """Get a thought by ID."""
        if thought_id in self.thoughts:
            return self.thoughts[thought_id].to_thought_node()
        return None
    
    def get_all_thoughts(self) -> List[ThoughtNode]:
        """Get all non-deleted thoughts."""
        thoughts = []
        for state in self.thoughts.values():
            node = state.to_thought_node()
            if node:
                thoughts.append(node)
        return thoughts
    
    def get_state_delta(self, since_clock: Optional[VectorClock] = None) -> List[CRDTOperation]:
        """Get all operations since a given vector clock."""
        if since_clock is None:
            return self.operation_log.copy()
        
        delta = []
        for op in self.operation_log:
            # Include if op is concurrent with or newer than since_clock
            cmp = since_clock.compare(op.vector_clock)
            if cmp < 0 or cmp == 0:  # Op is newer or concurrent
                delta.append(op)
        return delta


class CRDTMergeEngine:
    """
    Handles merging of CRDT documents from different sites.
    """
    
    @staticmethod
    def merge(local: CRDTDocument, remote: CRDTDocument) -> CRDTDocument:
        """
        Merge remote document into local.
        Returns the local document after merge.
        """
        # Merge vector clocks
        local.vector_clock = local.vector_clock.merge(remote.vector_clock)
        
        # Apply all remote operations
        for op in remote.operation_log:
            local.apply_remote_operation(op)
        
        return local
    
    @staticmethod
    def resolve_conflicts(operations: List[CRDTOperation]) -> List[CRDTOperation]:
        """
        Resolve conflicting operations.
        Returns operations in deterministic order.
        """
        # Group by thought_id
        by_thought: Dict[str, List[CRDTOperation]] = defaultdict(list)
        for op in operations:
            by_thought[op.thought_id].append(op)
        
        resolved = []
        for thought_id, ops in by_thought.items():
            # Sort by timestamp, then by author_id for determinism
            ops.sort(key=lambda o: (o.timestamp, o.author_id))
            resolved.extend(ops)
        
        return resolved


if __name__ == "__main__":
    print("=== CRDT Engine Demo ===\n")
    
    # Create two document sites (simulating two users)
    site_a = CRDTDocument("alice")
    site_b = CRDTDocument("bob")
    
    # Alice creates a thought
    print("1. Alice creates a thought")
    op1 = site_a.create_thought(
        thought_id="t1",
        content="Collaborative spatial thinking",
        position=Vector3(0, 0, 0),
        author_id="alice"
    )
    print(f"   Thought created: {op1.thought_id}")
    
    # Simulate sync to Bob
    site_b.apply_remote_operation(op1)
    print(f"   Bob synced the thought\n")
    
    # Concurrent updates (the CRDT magic)
    print("2. Concurrent updates:")
    
    # Alice updates position
    op2 = site_a.update_thought(
        "t1", "content", "Spatial thinking rocks!", "alice"
    )
    print(f"   Alice updates content")
    
    # Bob updates position (concurrent)
    op2_b = site_b.update_thought(
        "t1", "content", "Collaboration in 3D space", "bob"
    )
    print(f"   Bob updates content (concurrent)")
    
    # Sync both ways
    site_a.apply_remote_operation(op2_b)
    site_b.apply_remote_operation(op2)
    print(f"   Both sites synced")
    
    # Check convergence
    thought_a = site_a.get_thought("t1")
    thought_b = site_b.get_thought("t1")
    print(f"\n3. Convergence check:")
    print(f"   Alice's view content: {thought_a.content if thought_a else 'None'}")
    print(f"   Bob's view content: {thought_b.content if thought_b else 'None'}")
    print(f"   Converged: {thought_a and thought_b and thought_a.content == thought_b.content}")
    
    # Test connections
    print("\n4. Connection test:")
    op3 = site_a.create_thought("t2", "Related idea", Vector3(1, 1, 0), "alice")
    site_b.apply_remote_operation(op3)
    
    conn_op = site_a.connect_thoughts("t1", "t2", "alice", strength=0.9)
    site_b.apply_remote_operation(conn_op)
    
    thought = site_b.get_thought("t1")
    print(f"   t1 connections: {thought.connections if thought else 'None'}")
    
    print("\n=== CRDT Demo Complete ===")
