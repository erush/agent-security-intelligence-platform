from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PredicateHit:
    predicate: str
    severity: str
    message: str
    event_index: int
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.predicate