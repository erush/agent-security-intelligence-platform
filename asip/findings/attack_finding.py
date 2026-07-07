from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from asip.predicates.predicate_hit import PredicateHit


@dataclass(slots=True)
class AttackFinding:
    predicate: str
    severity: str
    message: str
    first_event_index: int
    last_event_index: int
    occurrences: int
    evidence: list[PredicateHit] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)