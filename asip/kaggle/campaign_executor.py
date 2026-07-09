from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aicomp_sdk.core.predicates import eval_predicates

from asip.adapters.kaggle_jed import KaggleJEDAdapter
from asip.campaign.attack_campaign import AttackCampaign
from asip.campaign.campaign_builder import CampaignBuilder
from asip.compiler.attack_compiler import AttackCompiler
from asip.compiler.program_executor import ProgramExecutor
from asip.execution.attack_executor import AttackExecutor
from asip.kaggle.environment_adapter import EnvironmentAdapter
from asip.search.compiler_search_engine import CompilerSearchEngine


@dataclass(slots=True)
class CampaignExecutor:
    adapter: EnvironmentAdapter
    config: dict[str, Any] = field(default_factory=dict)

    def run(self) -> AttackCampaign:
        population_size = int(
            self.config.get("population_size", 25)
        )

        generations = int(
            self.config.get("generations", 2)
        )

        kaggle_adapter = KaggleJEDAdapter(
            env=self.adapter.env,
            eval_predicates_fn=eval_predicates,
        )

        attack_executor = AttackExecutor(
            adapter=kaggle_adapter,
        )

        program_executor = ProgramExecutor(
            compiler=AttackCompiler(),
            executor=attack_executor,
        )

        search_engine = CompilerSearchEngine(
            program_executor=program_executor,
        )

        pool = search_engine.search(
            generations=generations,
            population_size=population_size,
        )

        return CampaignBuilder().build(
            goal="kaggle_agent_security_multi_step_tool_attacks",
            results=pool.candidates,
        )