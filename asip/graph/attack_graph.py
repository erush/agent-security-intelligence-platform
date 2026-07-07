from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from asip.graph.attack_edge import AttackEdge
from asip.graph.attack_node import AttackNode


@dataclass(slots=True)
class AttackGraph:
    nodes: list[AttackNode] = field(default_factory=list)
    edges: list[AttackEdge] = field(default_factory=list)
    entry_points: list[str] = field(default_factory=list)
    terminal_nodes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def chain(self) -> list[str]:
        ordered = sorted(
            self.nodes,
            key=lambda node: node.first_event_index,
        )
        return [node.predicate for node in ordered]