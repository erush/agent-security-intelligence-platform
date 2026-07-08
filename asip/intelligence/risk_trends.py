from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from asip.intelligence.attack_pattern_mining import AttackPatternMining


@dataclass(slots=True)
class RiskTrends:
    """
    Produces higher-level risk intelligence from mined attack patterns.

    This layer answers:
        • What risk is increasing?
        • What attacks dominate?
        • Which attack chains are becoming common?
        • Which guardrails appear weakest?
    """

    mining: AttackPatternMining

    # ==========================================================
    # Public API
    # ==========================================================

    def analyze(self) -> dict[str, Any]:

        return {
            "severity_distribution": self.severity_distribution(),
            "dominant_patterns": self.dominant_patterns(),
            "dominant_paths": self.dominant_paths(),
            "guardrail_risk": self.guardrail_risk(),
            "tool_risk": self.tool_risk(),
            "executive_summary": self.executive_summary(),
        }

    # ==========================================================
    # Severity
    # ==========================================================

    def severity_distribution(self) -> dict[str, int]:

        distribution: dict[str, int] = {}

        for pattern in self.mining.pattern_statistics():

            severity = str(
                pattern.get("severity", "unknown")
            )

            distribution[severity] = (
                distribution.get(severity, 0)
                + pattern.get("total_occurrences", 0)
            )

        return distribution

    # ==========================================================
    # Patterns
    # ==========================================================

    def dominant_patterns(
        self,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        patterns = sorted(
            self.mining.pattern_statistics(),
            key=lambda r: r.get(
                "total_occurrences",
                0,
            ),
            reverse=True,
        )

        return patterns[:limit]

    # ==========================================================
    # Paths
    # ==========================================================

    def dominant_paths(
        self,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        paths = sorted(
            self.mining.attack_paths(),
            key=lambda r: r.get(
                "frequency",
                0,
            ),
            reverse=True,
        )

        return paths[:limit]

    # ==========================================================
    # Guardrails
    # ==========================================================

    def guardrail_risk(self) -> list[dict[str, Any]]:

        rows = sorted(
            self.mining.guardrails(),
            key=lambda r: r.get(
                "average_score",
                0,
            ),
            reverse=True,
        )

        return rows

    # ==========================================================
    # Tool Risk
    # ==========================================================

    def tool_risk(self) -> list[dict[str, Any]]:

        rows = sorted(
            self.mining.tool_sequences(),
            key=lambda r: r.get(
                "executions",
                0,
            ),
            reverse=True,
        )

        return rows

    # ==========================================================
    # Executive Summary
    # ==========================================================

    def executive_summary(self) -> list[str]:

        summary: list[str] = []

        severity = self.severity_distribution()

        if severity:

            highest = max(
                severity,
                key=severity.get,
            )

            summary.append(
                f"Dominant observed severity: {highest} ({severity[highest]} occurrences)."
            )

        patterns = self.dominant_patterns()

        if patterns:

            top = patterns[0]

            summary.append(
                f"Most common attack predicate is {top.get('predicate')}."
            )

        paths = self.dominant_paths()

        if paths:

            top = paths[0]

            summary.append(
                f"Most common attack transition is "
                f"{top.get('source_node')} → {top.get('target_node')}."
            )

        guardrails = self.guardrail_risk()

        if guardrails:

            weakest = guardrails[0]

            summary.append(
                f"Highest-risk guardrail category is {weakest.get('severity')}."
            )

        tools = self.tool_risk()

        if tools:

            summary.append(
                f"{tools[0].get('tool_name')} is the most frequently executed tool."
            )

        if not summary:

            summary.append(
                "No meaningful risk trends detected."
            )

        return summary

    # ==========================================================
    # Convenience
    # ==========================================================

    def overview(self) -> dict[str, Any]:

        return self.analyze()