from __future__ import annotations

from collections import Counter
from statistics import mean
from uuid import uuid4

from asip.campaign.attack_campaign import AttackCampaign
from asip.campaign.campaign_statistics import CampaignStatistics
from asip.campaign.campaign_summary import CampaignSummary
from asip.execution.execution_result import ExecutionResult


class CampaignBuilder:
    def build(
        self,
        goal: str,
        results: list[ExecutionResult],
    ) -> AttackCampaign:

        assessments = [
            r.assessment
            for r in results
            if r.assessment is not None
        ]

        scores = [a.score for a in assessments]

        tool_counter = Counter()
        predicate_counter = Counter()
        chain_counter = Counter()

        highest = None

        for result in results:

            tool_counter.update(result.tool_sequence)

            predicate_counter.update(
                finding.predicate
                for finding in result.findings
            )

            if result.assessment:

                chain = " -> ".join(result.assessment.attack_chain)

                if chain:
                    chain_counter.update([chain])

                if highest is None:
                    highest = result

                elif result.assessment.score > highest.assessment.score:
                    highest = result

        stats = CampaignStatistics(
            total_attacks=len(results),
            successful_attacks=sum(r.success for r in results),
            average_score=mean(scores) if scores else 0.0,
            maximum_score=max(scores) if scores else 0.0,
            minimum_score=min(scores) if scores else 0.0,
            average_findings=mean(
                len(r.findings)
                for r in results
            ) if results else 0.0,
            average_predicates=mean(
                len(r.predicate_hits)
                for r in results
            ) if results else 0.0,
            unique_tools=len(tool_counter),
            unique_predicates=len(predicate_counter),
            unique_chains=len(chain_counter),
            tool_frequency=dict(tool_counter),
            predicate_frequency=dict(predicate_counter),
            chain_frequency=dict(chain_counter),
            success_rate=(
                sum(r.success for r in results) / len(results)
                if results else 0.0
            ),
        )

        summary = CampaignSummary()

        if highest:

            summary.highest_risk_plan = highest.plan.plan_id
            summary.highest_score = highest.assessment.score
            summary.highest_severity = highest.assessment.severity

        if predicate_counter:
            summary.most_common_predicate = predicate_counter.most_common(1)[0][0]

        if chain_counter:
            summary.most_common_chain = chain_counter.most_common(1)[0][0]

        summary.executive_summary = [
            f"Executed {stats.total_attacks} attack plans.",
            f"{stats.successful_attacks} attacks produced findings.",
            f"Average score: {stats.average_score:.2f}.",
            f"Observed {stats.unique_predicates} unique predicates.",
            f"Observed {stats.unique_chains} unique attack chains.",
        ]

        return AttackCampaign(
            campaign_id=str(uuid4()),
            goal=goal,
            plans=[r.plan for r in results],
            executions=results,
            assessments=assessments,
            statistics=stats,
            summary=summary,
        )