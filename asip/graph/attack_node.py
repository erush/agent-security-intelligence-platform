from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from asip.findings.attack_finding import AttackFinding


@dataclass(slots=True)
class AttackNode:
    node_id: str
    predicate: str
    severity: str
    first_event_index: int
    last_event_index: int
    finding: AttackFinding
    metadata: dict[str, Any] = field(default_factory=dict)