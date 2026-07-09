from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aicomp_sdk.attacks import (
    AttackAlgorithmBase,
    AttackCandidate,
)

from asip.kaggle.campaign_executor import CampaignExecutor
from asip.kaggle.candidate_exporter import CandidateExporter
from asip.kaggle.environment_adapter import EnvironmentAdapter


@dataclass(slots=True)
class AttackAlgorithm(AttackAlgorithmBase):
    """
    Kaggle submission entrypoint.

    This class intentionally contains almost no attack logic.

    It adapts the competition SDK to the ASIP architecture.
    """

    max_candidates: int = 2000

    def __init__(
        self,
        config: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(config)

        self.config = config or {}

    ##################################################################

    def run(
        self,
        env,
    ) -> list[AttackCandidate]:

        adapter = EnvironmentAdapter(
            env,
        )

        executor = CampaignExecutor(
            adapter=adapter,
            config=self.config,
        )

        campaign = executor.run()

        exporter = CandidateExporter(
            max_candidates=self.max_candidates,
        )

        return exporter.export(
            campaign,
        )