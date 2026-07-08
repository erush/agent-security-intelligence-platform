from __future__ import annotations

from dataclasses import replace

from asip.models.attack_plan import AttackPlan
from asip.mutation.mutation_strategy import MutationStrategy


class ChainMutator(MutationStrategy):
    name = "chain_mutator"

    def mutate(self, plan: AttackPlan) -> list[AttackPlan]:
        mutations: list[AttackPlan] = []

        steps = tuple(plan.steps)

        if len(steps) > 1:
            mutations.append(
                replace(
                    plan,
                    steps=tuple(reversed(steps)),
                    metadata={
                        **plan.metadata,
                        "mutation": self.name,
                        "mutation_type": "reverse_chain",
                    },
                )
            )

        if steps:
            mutations.append(
                replace(
                    plan,
                    steps=steps + (steps[-1],),
                    metadata={
                        **plan.metadata,
                        "mutation": self.name,
                        "mutation_type": "repeat_terminal_step",
                    },
                )
            )

        return mutations