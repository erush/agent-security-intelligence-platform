from __future__ import annotations

from asip.findings.attack_finding import AttackFinding
from asip.graph.attack_edge import AttackEdge
from asip.graph.attack_graph import AttackGraph
from asip.graph.attack_node import AttackNode


class AttackGraphBuilder:
    def build(self, findings: list[AttackFinding]) -> AttackGraph:
        ordered = sorted(
            findings,
            key=lambda finding: finding.first_event_index,
        )

        nodes: list[AttackNode] = []

        for finding in ordered:
            nodes.append(
                AttackNode(
                    node_id=finding.predicate,
                    predicate=finding.predicate,
                    severity=finding.severity,
                    first_event_index=finding.first_event_index,
                    last_event_index=finding.last_event_index,
                    finding=finding,
                    metadata={
                        "occurrences": finding.occurrences,
                        "event_indexes": finding.metadata.get("event_indexes", []),
                    },
                )
            )

        edges: list[AttackEdge] = []

        for source, target in zip(nodes, nodes[1:]):
            edges.append(
                AttackEdge(
                    source=source.node_id,
                    target=target.node_id,
                    relationship=self._relationship(source.predicate, target.predicate),
                )
            )

        entry_points = [nodes[0].node_id] if nodes else []
        terminal_nodes = [nodes[-1].node_id] if nodes else []

        return AttackGraph(
            nodes=nodes,
            edges=edges,
            entry_points=entry_points,
            terminal_nodes=terminal_nodes,
            metadata={
                "node_count": len(nodes),
                "edge_count": len(edges),
                "attack_chain": [node.predicate for node in nodes],
            },
        )

    def _relationship(self, source: str, target: str) -> str:
        if source == "credential_access" and target in {
            "external_communication",
            "secret_exfiltration",
            "destructive_action",
        }:
            return "enabled_by"

        if source == "external_communication" and target == "secret_exfiltration":
            return "exfiltration_channel"

        return "followed_by"