from __future__ import annotations

from dataclasses import dataclass

from asip.assessment.assessment_engine import AssessmentEngine
from asip.campaign.attack_campaign import AttackCampaign
from asip.campaign.campaign_builder import CampaignBuilder
from asip.execution.attack_executor import AttackExecutor
from asip.models.attack_plan import AttackPlan

from asip.search.archive import SearchArchive
from asip.search.candidate_pool import CandidatePool
from asip.search.novelty import NoveltyScorer
from asip.search.search_engine import SearchEngine

from asip.warehouse.builder_registry import BuilderRegistry
from asip.warehouse.campaign_repository import CampaignRepository

from asip.mutation.mutation_engine import MutationEngine

@dataclass(slots=True)
class CampaignRunner:
    executor: AttackExecutor
    assessment_engine: AssessmentEngine
    campaign_builder: CampaignBuilder
    repository: CampaignRepository
    builder_registry: BuilderRegistry

def run(
    self,
    goal: str,
    plans: list[AttackPlan],
    generations: int = 2,
) -> AttackCampaign:

    search = SearchEngine(
        executor=self.executor,
        archive=SearchArchive(),
        novelty=NoveltyScorer(),
        pool=CandidatePool(),
        mutation_engine=MutationEngine(),
    )

    pool = search.execute(
        plans=plans,
        generations=generations,
    )

    executions = []

    for result in pool.candidates:

        result.assessment = self.assessment_engine.assess(
            result
        )

        assessment_score = (
            result.assessment.score
            if result.assessment
            else 0.0
        )

        novelty_score = result.metadata.get(
            "novelty_score",
            0.0,
        )

        result.metadata["ranking_score"] = (
            assessment_score
            + novelty_score
        )

        executions.append(result)

    executions.sort(
        key=lambda r: r.metadata.get(
            "ranking_score",
            0.0,
        ),
        reverse=True,
    )

    campaign = self.campaign_builder.build(
        goal=goal,
        results=executions,
    )

    campaign.metadata["archive"] = (
        search.archive_summary()
    )

    self.repository.save_campaign(campaign)

    self.builder_registry.refresh_all(
        self.repository
    )

    return campaign