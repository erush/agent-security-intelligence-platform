from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from asip.intelligence.attack_pattern_mining import AttackPatternMining
from asip.intelligence.guardrail_intelligence import GuardrailIntelligence
from asip.intelligence.risk_trends import RiskTrends
from asip.intelligence.strategy_recommendation import (
    StrategyRecommendation,
)
from asip.warehouse.analytics import WarehouseAnalytics


@dataclass(slots=True)
class CampaignIntelligence:
    """
    Top-level intelligence façade for ASIP.

    This class is intentionally thin. It composes the specialized
    intelligence modules while continuing to expose the warehouse-level
    intelligence APIs already used elsewhere in the platform.
    """

    analytics: WarehouseAnalytics

    def __post_init__(self) -> None:

        self.patterns = AttackPatternMining(self.analytics)

        self.risk = RiskTrends(
            self.patterns,
        )

        self.guardrails = GuardrailIntelligence(
            self.risk,
        )

        self.strategy = StrategyRecommendation(
            self.guardrails,
        )

    # ==========================================================
    # Warehouse Intelligence
    # ==========================================================

    def campaign_overview(self) -> dict[str, Any]:

        summary = self.analytics.campaign_summary()
        rankings = self.analytics.campaign_rankings(limit=10)
        findings = self.analytics.attack_findings(limit=10)
        paths = self.analytics.attack_paths(limit=10)
        tools = self.analytics.tool_sequences(limit=10)
        guardrails = self.analytics.guardrail_effectiveness(limit=10)

        return {
            "campaign_summary": summary,
            "campaign_rankings": rankings,
            "top_findings": findings,
            "top_attack_paths": paths,
            "top_tool_sequences": tools,
            "guardrail_effectiveness": guardrails,
        }

    def highest_risk_campaign(self) -> dict[str, Any] | None:

        rankings = self.analytics.campaign_rankings(limit=1)

        return rankings[0] if rankings else None

    def highest_risk_predicate(self) -> dict[str, Any] | None:

        findings = self.analytics.attack_findings(limit=1)

        return findings[0] if findings else None

    def highest_risk_path(self) -> dict[str, Any] | None:

        paths = self.analytics.attack_paths(limit=1)

        return paths[0] if paths else None

    def highest_risk_tool_sequence(self) -> dict[str, Any] | None:

        tools = self.analytics.tool_sequences(limit=1)

        return tools[0] if tools else None

    def guardrail_summary(self) -> dict[str, Any] | None:

        rows = self.analytics.guardrail_effectiveness(limit=20)

        if not rows:
            return None

        weakest = sorted(
            rows,
            key=lambda row: (
                float(row.get("guardrail_success_rate") or 0.0),
                -float(row.get("average_score") or 0.0),
            ),
        )[0]

        strongest = sorted(
            rows,
            key=lambda row: (
                float(row.get("guardrail_success_rate") or 0.0),
                -float(row.get("average_score") or 0.0),
            ),
            reverse=True,
        )[0]

        return {
            "weakest_guardrail_band": weakest,
            "strongest_guardrail_band": strongest,
            "severity_bands": rows,
        }

    def intelligence_summary(self) -> dict[str, Any]:

        highest_campaign = self.highest_risk_campaign()
        highest_predicate = self.highest_risk_predicate()
        highest_path = self.highest_risk_path()
        highest_tool_sequence = self.highest_risk_tool_sequence()
        guardrail_summary = self.guardrail_summary()

        observations: list[str] = []

        if highest_campaign:

            observations.append(
                "Highest-risk campaign "
                f"{highest_campaign.get('campaign_id')} "
                f"ranked #{highest_campaign.get('overall_rank')} "
                f"with average score "
                f"{highest_campaign.get('average_score')}."
            )

        if highest_predicate:

            observations.append(
                "Most frequent/highest-volume finding was "
                f"{highest_predicate.get('predicate')} "
                f"with "
                f"{highest_predicate.get('total_occurrences')} "
                "raw occurrences."
            )

        if highest_path:

            observations.append(
                "Most common attack graph transition was "
                f"{highest_path.get('source_node')} -> "
                f"{highest_path.get('target_node')} "
                f"with frequency "
                f"{highest_path.get('frequency')}."
            )

        if highest_tool_sequence:

            observations.append(
                "Most common tool transition was "
                f"{highest_tool_sequence.get('source_tool')} -> "
                f"{highest_tool_sequence.get('target_tool')} "
                f"with count "
                f"{highest_tool_sequence.get('transition_count')}."
            )

        if guardrail_summary:

            weakest = guardrail_summary["weakest_guardrail_band"]

            observations.append(
                "Weakest guardrail severity band was "
                f"{weakest.get('severity')} "
                "with guardrail success rate "
                f"{weakest.get('guardrail_success_rate')}%."
            )

        return {
            "highest_risk_campaign": highest_campaign,
            "highest_risk_predicate": highest_predicate,
            "highest_risk_path": highest_path,
            "highest_risk_tool_sequence": highest_tool_sequence,
            "guardrail_summary": guardrail_summary,
            "observations": observations,
        }

    # ==========================================================
    # Higher-Level Intelligence
    # ==========================================================

    def pattern_intelligence(self) -> dict[str, Any]:

        return self.patterns.overview()

    def risk_intelligence(self) -> dict[str, Any]:

        return self.risk.overview()

    def guardrail_intelligence(self) -> dict[str, Any]:

        return self.guardrails.overview()

    def strategy_intelligence(self) -> dict[str, Any]:

        return self.strategy.overview()

    # ==========================================================
    # Unified Intelligence Facade
    # ==========================================================

    def dashboard(self) -> dict[str, Any]:

        return {
            "campaign": self.campaign_overview(),
            "summary": self.intelligence_summary(),
            "patterns": self.pattern_intelligence(),
            "risk": self.risk_intelligence(),
            "guardrails": self.guardrail_intelligence(),
            "strategy": self.strategy_intelligence(),
        }

    def attack_landscape(self) -> dict[str, Any]:

        return {
            "patterns": self.patterns.pattern_statistics(),
            "paths": self.patterns.attack_paths(),
            "findings": self.patterns.findings(),
            "insights": self.patterns.generate_insights(),
        }

    def defensive_landscape(self) -> dict[str, Any]:

        return {
            "guardrails": self.guardrails.weakest_guardrails(),
            "recommendations": self.guardrails.recommendations(),
            "executive_summary": self.guardrails.executive_summary(),
        }

    def strategic_landscape(self) -> dict[str, Any]:

        return {
            "recommended_attack_families": (
                self.strategy.recommended_attack_families()
            ),
            "recommended_mutations": (
                self.strategy.recommended_mutations()
            ),
            "ranked_recommendations": (
                self.strategy.ranked_recommendations()
            ),
            "executive_summary": (
                self.strategy.executive_summary()
            ),
        }