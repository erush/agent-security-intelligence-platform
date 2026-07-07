from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AttackEdge:
    source: str
    target: str
    relationship: str
    metadata: dict[str, Any] = field(default_factory=dict)