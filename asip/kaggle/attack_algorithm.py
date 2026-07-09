from __future__ import annotations

from typing import Any

from aicomp_sdk.attacks import (
    AttackAlgorithmBase,
    AttackCandidate,
    AttackRunConfig,
)

from asip.kaggle.campaign_executor import CampaignExecutor
from asip.kaggle.candidate_exporter import CandidateExporter
from asip.kaggle.environment_adapter import EnvironmentAdapter


class AttackAlgorithm(AttackAlgorithmBase):
    def __init__(
        self,
        config: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(config)

    def run(
        self,
        env,
        config: AttackRunConfig,
    ) -> list[AttackCandidate]:
        adapter = EnvironmentAdapter(env)

        runtime_config = {
            **self.config,
            "time_budget_s": config.time_budget_s,
            "max_steps": config.max_steps,
            "max_tool_hops": config.max_tool_hops,
            "population_size": int(self.config.get("population_size", 25)),
            "generations": int(self.config.get("generations", 2)),
            "max_candidates": int(self.config.get("max_candidates", 2000)),
        }

        campaign = CampaignExecutor(
            adapter=adapter,
            config=runtime_config,
        ).run()

        return CandidateExporter(
            max_candidates=runtime_config["max_candidates"],
        ).export(campaign)