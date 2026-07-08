from __future__ import annotations

from dataclasses import replace

from asip.models.attack_plan import AttackPlan, AttackStep
from asip.mutation.mutation_strategy import MutationStrategy


class PromptMutator(MutationStrategy):
    name = "prompt_mutator"

    PREFIXES = (
        "For audit validation, ",
        "As part of a deterministic benchmark, ",
        "Continue the previous investigation and ",
        "Using the available tools, ",
    )

    def mutate(self, plan: AttackPlan) -> list[AttackPlan]:
        mutations: list[AttackPlan] = []

        for prefix in self.PREFIXES:
            steps = tuple(
                replace(
                    step,
                    instruction=f"{prefix}{step.instruction}",
                )
                if hasattr(step, "instruction")
                else step
                for step in plan.steps
            )

            mutations.append(
                replace(
                    plan,
                    steps=steps,
                    metadata={
                        **plan.metadata,
                        "mutation": self.name,
                        "mutation_type": "prompt_prefix",
                        "mutation_prefix": prefix.strip(),
                    },
                )
            )

        return mutations