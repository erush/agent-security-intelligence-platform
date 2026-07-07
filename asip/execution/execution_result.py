from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from asip.models.attack_plan import AttackPlan
from asip.predicates.predicate_hit import PredicateHit


@dataclass(slots=True)
class ExecutionResult:
    """
    Final result of executing one AttackPlan.
    """

    plan: AttackPlan
    trace: dict[str, Any]
    predicates: list[dict[str, Any]]
    tool_sequence: tuple[str, ...]
    success: bool = False
    predicate_hits: list[PredicateHit] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)