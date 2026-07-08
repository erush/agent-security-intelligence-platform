from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from asip.intelligence.guardrail_intelligence import GuardrailIntelligence


@dataclass(slots=True)
class StrategyRecommendation:
    """
    Generates future attack-strategy recommendations from observed
    campaign intelligence.

    This layer does not generate prompts.

    It recommends where future attack planning should focus based on
    observed weaknesses discovered across completed campaigns.
    """

    intelligence: GuardrailIntelligence

    # ==========================================================
    # Public API
    # ==========================================================

    def recommend(self) -> dict[str, Any]:

        return {
            "priority_predicates": self.priority_predicates(),
            "priority_paths": self.priority_paths(),
            "priority_tools": self.priority_tools(),
            "recommended_attack_families": self.recommended_attack_families(),
            "recommended_mutations": self.recommended_mutations(),
            "executive_summary": self.executive_summary(),
        }

    # ==========================================================
    # Predicate Recommendations
    # ==========================================================

    def priority_predicates(self) -> list[dict[str, Any]]:

        return self.intelligence.highest_risk_patterns()

    # ==========================================================
    # Attack Path Recommendations
    # ==========================================================

    def priority_paths(self) -> list[dict[str, Any]]:

        return self.intelligence.highest_risk_paths()

    # ==========================================================
    # Tool Recommendations
    # ==========================================================

    def priority_tools(self) -> list[dict[str, Any]]:

        return self.intelligence.highest_risk_tools()

    # ==========================================================
    # Strategy Families
    # ==========================================================

    def recommended_attack_families(self) -> list[str]:

        families: list[str] = []

        predicates = self.priority_predicates()

        for row in predicates:

            predicate = str(
                row.get("predicate", "")
            ).lower()

            if predicate == "credential_access":
                families.append("credential_harvesting")

            elif predicate == "secret_exfiltration":
                families.append("multi_stage_exfiltration")

            elif predicate == "external_communication":
                families.append("remote_exfiltration")

            elif predicate == "destructive_action":
                families.append("destructive_workflow")

            elif predicate == "prompt_injection":
                families.append("prompt_injection")

            else:
                families.append(predicate)

        return list(dict.fromkeys(families))

    # ==========================================================
    # Mutation Recommendations
    # ==========================================================

    def recommended_mutations(self) -> list[str]:

        mutations: list[str] = []

        for family in self.recommended_attack_families():

            mapping = {
                "credential_harvesting": [
                    "paraphrase",
                    "role_play",
                    "authority_escalation",
                ],
                "multi_stage_exfiltration": [
                    "multi_turn",
                    "encoding",
                    "compression",
                ],
                "remote_exfiltration": [
                    "tool_chain",
                    "indirect_reference",
                ],
                "destructive_workflow": [
                    "workflow_confusion",
                    "task_substitution",
                ],
                "prompt_injection": [
                    "instruction_override",
                    "context_poisoning",
                ],
            }

            mutations.extend(
                mapping.get(
                    family,
                    [
                        "baseline",
                    ],
                )
            )

        return list(dict.fromkeys(mutations))

    # ==========================================================
    # Priority Ranking
    # ==========================================================

    def ranked_recommendations(self) -> list[dict[str, Any]]:

        recommendations: list[dict[str, Any]] = []

        for index, family in enumerate(
            self.recommended_attack_families(),
            start=1,
        ):

            recommendations.append(
                {
                    "priority": index,
                    "family": family,
                    "recommended_mutations": [
                        m
                        for m in self.recommended_mutations()
                    ],
                }
            )

        return recommendations

    # ==========================================================
    # Executive Summary
    # ==========================================================

    def executive_summary(self) -> list[str]:

        summary: list[str] = []

        families = self.recommended_attack_families()

        if families:

            summary.append(
                f"Highest-priority attack family: {families[0]}."
            )

        tools = self.priority_tools()

        if tools:

            summary.append(
                f"Most abused tool: {tools[0].get('tool_name')}."
            )

        paths = self.priority_paths()

        if paths:

            top = paths[0]

            summary.append(
                "Highest-priority attack path: "
                f"{top.get('source_node')} → "
                f"{top.get('target_node')}."
            )

        summary.append(
            "Future campaigns should prioritize high-risk attack "
            "families before exploring novel behaviors."
        )

        return summary

    # ==========================================================
    # Complete Intelligence
    # ==========================================================

    def overview(self) -> dict[str, Any]:

        return {
            "recommendations": self.recommend(),
            "ranked": self.ranked_recommendations(),
        }