from __future__ import annotations

from dataclasses import dataclass

from asip.assessment.assessment_engine import AssessmentEngine
from asip.campaign.attack_campaign import AttackCampaign
from asip.campaign.campaign_builder import CampaignBuilder
from asip.execution.attack_executor import AttackExecutor
from asip.models.attack_plan import AttackPlan
from asip.warehouse.builder_registry import BuilderRegistry
from asip.warehouse.campaign_repository import CampaignRepository


@dataclass(slots=True)
class CampaignRunner:
    """
    Executes an entire attack campaign.

    Responsibilities
    ----------------
    1. Execute every attack plan.
    2. Assess each execution.
    3. Build campaign-level intelligence.
    4. Persist campaign to the warehouse.
    5. Refresh warehouse analytics.
    """

    executor: AttackExecutor
    assessment_engine: AssessmentEngine
    campaign_builder: CampaignBuilder
    repository: CampaignRepository

    def __post_init__(self) -> None:
        self.builder_registry = BuilderRegistry(self.repository)

    def run(
        self,
        goal: str,
        plans: list[AttackPlan],
    ) -> AttackCampaign:

        executions = []

        for plan in plans:

            result = self.executor.execute(plan)

            result.assessment = self.assessment_engine.assess(
                result
            )

            executions.append(result)

        campaign = self.campaign_builder.build(
            goal=goal,
            results=executions,
        )

        self.repository.save_campaign(campaign)

        self.refresh_warehouse()

        return campaign

    def refresh_warehouse(self) -> None:
        """
        Refresh every warehouse analytics table.

        CampaignRunner should not know individual builders.
        The BuilderRegistry owns analytics orchestration.
        """

        self.builder_registry.refresh()