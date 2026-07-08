from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CampaignSummary:
    highest_risk_plan: str | None = None
    highest_score: float = 0.0

    highest_severity: str = "none"

    most_common_predicate: str | None = None
    most_common_chain: str | None = None

    executive_summary: list[str] = field(default_factory=list)