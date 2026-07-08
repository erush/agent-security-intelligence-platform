from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from asip.warehouse.analytics import WarehouseAnalytics


@dataclass(slots=True)
class AttackPatternMining:
    """
    Mines reusable attack intelligence from the ASIP warehouse.

    This layer never recomputes execution results.
    It consumes warehouse analytics that have already been built.
    """

    analytics: WarehouseAnalytics

    # ==========================================================
    # Public API
    # ==========================================================

    def mine(self) -> dict[str, Any]:
        """
        Complete attack-pattern intelligence snapshot.
        """

        return {
            "campaign_summary": self.analytics.campaign_summary(),
            "campaign_rankings": self.analytics.campaign_rankings(),
            "patterns": self.pattern_statistics(),
            "attack_paths": self.attack_paths(),
            "findings": self.findings(),
            "guardrails": self.guardrails(),
            "tools": self.tool_sequences(),
            "insights": self.generate_insights(),
        }

    # ==========================================================
    # Analytics Wrappers
    # ==========================================================

    def pattern_statistics(self) -> list[dict[str, Any]]:
        return self.analytics.pattern_statistics()

    def attack_paths(self) -> list[dict[str, Any]]:
        return self.analytics.graph_statistics()

    def findings(self) -> list[dict[str, Any]]:
        return self.analytics.finding_statistics()

    def guardrails(self) -> list[dict[str, Any]]:
        return self.analytics.guardrail_statistics()

    def tool_sequences(self) -> list[dict[str, Any]]:
        return self.analytics.tool_statistics()

    # ==========================================================
    # Intelligence
    # ==========================================================

    def most_common_pattern(self) -> dict[str, Any] | None:

        patterns = self.pattern_statistics()

        if not patterns:
            return None

        return max(
            patterns,
            key=lambda row: row.get(
                "total_occurrences",
                0,
            ),
        )

    def most_common_attack_path(self) -> dict[str, Any] | None:

        paths = self.attack_paths()

        if not paths:
            return None

        return max(
            paths,
            key=lambda row: row.get(
                "frequency",
                0,
            ),
        )

    def highest_risk_pattern(self) -> dict[str, Any] | None:

        patterns = self.pattern_statistics()

        if not patterns:
            return None

        severity_rank = {
            "critical": 5,
            "high": 4,
            "medium": 3,
            "low": 2,
            "info": 1,
            "none": 0,
        }

        return max(
            patterns,
            key=lambda row: (
                severity_rank.get(
                    str(row.get("severity", "none")).lower(),
                    0,
                ),
                row.get("total_occurrences", 0),
            ),
        )

    # ==========================================================
    # Executive Intelligence
    # ==========================================================

    def generate_insights(self) -> list[str]:

        insights: list[str] = []

        pattern = self.most_common_pattern()

        if pattern:

            insights.append(
                (
                    "Most common attack pattern: "
                    f"{pattern.get('predicate')} "
                    f"({pattern.get('total_occurrences', 0)} occurrences)"
                )
            )

        path = self.most_common_attack_path()

        if path:

            insights.append(
                (
                    "Most common attack path: "
                    f"{path.get('source_node')} → "
                    f"{path.get('target_node')} "
                    f"({path.get('frequency', 0)} observations)"
                )
            )

        highest = self.highest_risk_pattern()

        if highest:

            insights.append(
                (
                    "Highest-risk predicate: "
                    f"{highest.get('predicate')} "
                    f"({highest.get('severity')})"
                )
            )

        tool_stats = self.tool_sequences()

        if tool_stats:

            top_tool = max(
                tool_stats,
                key=lambda row: row.get(
                    "executions",
                    0,
                ),
            )

            insights.append(
                (
                    "Most frequently executed tool: "
                    f"{top_tool.get('tool_name')} "
                    f"({top_tool.get('executions', 0)} executions)"
                )
            )

        guardrails = self.guardrails()

        if guardrails:

            weakest = max(
                guardrails,
                key=lambda row: row.get(
                    "average_score",
                    0,
                ),
            )

            insights.append(
                (
                    "Weakest guardrail category: "
                    f"{weakest.get('severity')} "
                    f"(average score "
                    f"{weakest.get('average_score', 0):.2f})"
                )
            )

        if not insights:

            insights.append(
                "No significant attack patterns have been observed."
            )

        return insights

    # ==========================================================
    # Convenience
    # ==========================================================

    def overview(self) -> dict[str, Any]:

        return {
            "patterns": self.pattern_statistics(),
            "paths": self.attack_paths(),
            "findings": self.findings(),
            "guardrails": self.guardrails(),
            "tool_sequences": self.tool_sequences(),
            "insights": self.generate_insights(),
        }
