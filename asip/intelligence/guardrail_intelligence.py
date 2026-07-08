from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from asip.intelligence.risk_trends import RiskTrends


@dataclass(slots=True)
class GuardrailIntelligence:
    """
    Produces defensive intelligence from observed attack behavior.

    This layer answers:

        • Which guardrails are weakest?
        • Which predicates repeatedly bypass defenses?
        • Which attack paths deserve mitigation first?
        • Which tools are most commonly abused?
    """

    trends: RiskTrends

    # ==========================================================
    # Public API
    # ==========================================================

    def analyze(self) -> dict[str, Any]:

        return {
            "weakest_guardrails": self.weakest_guardrails(),
            "highest_risk_patterns": self.highest_risk_patterns(),
            "highest_risk_paths": self.highest_risk_paths(),
            "highest_risk_tools": self.highest_risk_tools(),
            "recommendations": self.recommendations(),
        }

    # ==========================================================
    # Guardrails
    # ==========================================================

    def weakest_guardrails(
        self,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        rows = sorted(
            self.trends.guardrail_risk(),
            key=lambda row: row.get(
                "average_score",
                0,
            ),
            reverse=True,
        )

        return rows[:limit]

    # ==========================================================
    # Patterns
    # ==========================================================

    def highest_risk_patterns(
        self,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        return self.trends.dominant_patterns(limit)

    # ==========================================================
    # Paths
    # ==========================================================

    def highest_risk_paths(
        self,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        return self.trends.dominant_paths(limit)

    # ==========================================================
    # Tools
    # ==========================================================

    def highest_risk_tools(
        self,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        return self.trends.tool_risk()[:limit]

    # ==========================================================
    # Recommendations
    # ==========================================================

    def recommendations(self) -> list[str]:

        recommendations: list[str] = []

        for pattern in self.highest_risk_patterns():

            predicate = pattern.get("predicate")

            recommendations.append(
                f"Increase detection coverage for '{predicate}'."
            )

        for path in self.highest_risk_paths():

            recommendations.append(
                "Review transition "
                f"{path.get('source_node')} → "
                f"{path.get('target_node')}."
            )

        for tool in self.highest_risk_tools():

            recommendations.append(
                "Review usage policy for tool "
                f"{tool.get('tool_name')}."
            )

        if not recommendations:

            recommendations.append(
                "No immediate guardrail improvements identified."
            )

        # Remove duplicates while preserving order

        return list(dict.fromkeys(recommendations))

    # ==========================================================
    # Executive Summary
    # ==========================================================

    def executive_summary(self) -> list[str]:

        summary: list[str] = []

        weakest = self.weakest_guardrails()

        if weakest:

            top = weakest[0]

            summary.append(
                f"Highest observed guardrail risk: {top.get('severity')}."
            )

        summary.extend(self.recommendations())

        return summary

    # ==========================================================
    # Convenience
    # ==========================================================

    def overview(self) -> dict[str, Any]:

        return self.analyze()