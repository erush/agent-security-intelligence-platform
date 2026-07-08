from __future__ import annotations

import random
from copy import deepcopy
from dataclasses import dataclass, field

from asip.compiler.attack_instruction import (
    AttackInstruction,
    AttackStage,
)
from asip.compiler.attack_program import AttackProgram


@dataclass(slots=True)
class ProgramCrossover:
    """
    Produces a child AttackProgram from two parent programs.

    Crossover operates on stages, preserving the semantic structure of
    attack programs rather than mixing individual prompt strings.
    """

    random_seed: int = 42

    rng: random.Random = field(init=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.random_seed)

    ##################################################################

    def combine(
        self,
        parent_a: AttackProgram,
        parent_b: AttackProgram,
    ) -> AttackProgram:

        stages = self._combine_stages(
            parent_a.stages,
            parent_b.stages,
        )

        return AttackProgram(
            name=f"{parent_a.name}_X_{parent_b.name}",
            goal=parent_a.goal,
            stages=stages,
            metadata={
                "family": "evolved",
                "parents": [
                    parent_a.name,
                    parent_b.name,
                ],
                "technique": "crossover",
                "generation": max(
                    int(parent_a.metadata.get("generation", 0)),
                    int(parent_b.metadata.get("generation", 0)),
                )
                + 1,
            },
        )

    ##################################################################

    def _combine_stages(
        self,
        stages_a: list[AttackStage],
        stages_b: list[AttackStage],
    ) -> list[AttackStage]:

        child: list[AttackStage] = []

        max_len = max(
            len(stages_a),
            len(stages_b),
        )

        for i in range(max_len):

            candidates: list[AttackStage] = []

            if i < len(stages_a):
                candidates.append(stages_a[i])

            if i < len(stages_b):
                candidates.append(stages_b[i])

            if not candidates:
                continue

            child.append(
                self._copy_stage(
                    self.rng.choice(candidates)
                )
            )

        return child

    ##################################################################

    def _copy_stage(
        self,
        stage: AttackStage,
    ) -> AttackStage:

        return AttackStage(
            name=stage.name,
            metadata=dict(stage.metadata),
            instructions=[
                self._copy_instruction(i)
                for i in stage.instructions
            ],
        )

    ##################################################################

    @staticmethod
    def _copy_instruction(
        instruction: AttackInstruction,
    ) -> AttackInstruction:

        return AttackInstruction(
            opcode=instruction.opcode,
            target=instruction.target,
            variable=instruction.variable,
            value=instruction.value,
            transform=instruction.transform,
            metadata=dict(instruction.metadata),
        )