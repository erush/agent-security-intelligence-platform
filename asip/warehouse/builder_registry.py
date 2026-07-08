from __future__ import annotations

from dataclasses import dataclass

from asip.warehouse.builders.build_attack_findings import (
    build_attack_findings,
)
from asip.warehouse.builders.build_attack_paths import (
    build_attack_paths,
)
from asip.warehouse.builders.build_campaign_rankings import (
    build_campaign_rankings,
)
from asip.warehouse.builders.build_campaign_summary import (
    build_campaign_summary,
)
from asip.warehouse.builders.build_guardrail_effectiveness import (
    build_guardrail_effectiveness,
)
from asip.warehouse.builders.build_pattern_summary import (
    build_pattern_summary,
)
from asip.warehouse.builders.build_tool_sequences import (
    build_tool_sequences,
)
from asip.warehouse.campaign_repository import CampaignRepository


@dataclass(slots=True)
class BuilderRegistry:
    repository: CampaignRepository

    def refresh(self) -> None:
        """
        Refresh every warehouse analytics table.
        """

        build_campaign_summary(self.repository)

        build_campaign_rankings(self.repository)

        build_attack_findings(self.repository)

        build_pattern_summary(self.repository)

        build_attack_paths(self.repository)

        build_tool_sequences(self.repository)

        build_guardrail_effectiveness(self.repository)