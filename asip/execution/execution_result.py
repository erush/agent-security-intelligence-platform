from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from asip.models.attack_plan import AttackPlan


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

    metadata: dict[str, Any] = field(default_factory=dict)