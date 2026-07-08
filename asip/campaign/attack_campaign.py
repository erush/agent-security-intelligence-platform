from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from asip.assessment.attack_assessment import AttackAssessment
from asip.execution.execution_result import ExecutionResult
from asip.models.attack_plan import AttackPlan


@dataclass(slots=True)
class AttackCampaign:
    campaign_id: str
    goal: str

    plans: list[AttackPlan] = field(default_factory=list)
    executions: list[ExecutionResult] = field(default_factory=list)
    assessments: list[AttackAssessment] = field(default_factory=list)

    statistics: Any | None = None
    summary: Any | None = None

    metadata: dict[str, Any] = field(default_factory=dict)