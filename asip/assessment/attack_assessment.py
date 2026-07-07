from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from asip.findings.attack_finding import AttackFinding
from asip.graph.attack_graph import AttackGraph


@dataclass(slots=True)
class AttackAssessment:
    severity: str
    score: float
    success: bool
    attack_chain: list[str]
    findings: list[AttackFinding]
    attack_graph: AttackGraph | None = None
    rationale: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)