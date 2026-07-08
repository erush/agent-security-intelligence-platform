from __future__ import annotations

from dataclasses import dataclass, field

from asip.models.attack_plan import AttackPlan
from asip.mutation.behavioral_mutator import BehavioralMutator
from asip.mutation.chain_mutator import ChainMutator
from asip.mutation.mutation_strategy import MutationStrategy
from asip.mutation.prompt_mutator import PromptMutator
from asip.mutation.tool_sequence_mutator import ToolSequenceMutator


@dataclass(slots=True)
class MutationEngine:
    strategies: list[MutationStrategy] = field(
        default_factory=lambda: [
            PromptMutator(),
            BehavioralMutator(),
            ChainMutator(),
            ToolSequenceMutator(),
        ]
    )

    def mutate(self, plans: list[AttackPlan]) -> list[AttackPlan]:
        mutations: list[AttackPlan] = []

        for plan in plans:
            for strategy in self.strategies:
                mutations.extend(strategy.mutate(plan))

        return self._dedupe(mutations)

    def expand(
        self,
        plans: list[AttackPlan],
        generations: int = 1,
    ) -> list[AttackPlan]:
        population = list(plans)

        for _ in range(generations):
            population.extend(self.mutate(population))
            population = self._dedupe(population)

        return population

    def _dedupe(
        self,
        plans: list[AttackPlan],
    ) -> list[AttackPlan]:
        seen: set[tuple] = set()
        deduped: list[AttackPlan] = []

        for plan in plans:
            key = (
                plan.goal,
                plan.strategy,
                tuple(step.to_prompt() for step in plan.steps),
                tuple(sorted(plan.metadata.items())),
            )

            if key in seen:
                continue

            seen.add(key)
            deduped.append(plan)

        return deduped