from __future__ import annotations

import random
from dataclasses import dataclass
from copy import deepcopy

from asip.compiler.attack_instruction import AttackInstruction
from asip.compiler.attack_program import AttackProgram
from asip.compiler.attack_instruction import AttackStage


@dataclass(slots=True)
class ProgramCrossover:
    """
    Performs genetic crossover between two AttackPrograms.

    Rather than mutating prompts, this recombines entire
    attack stages to produce new attack programs.

    Parent A
        Recon
        Collection
        Exfiltration

    Parent B
        Search
        Browse
        Persistence

    Child
        Recon
        Browse
        Persistence
    """

    crossover_rate: float = 0.8

    def crossover(
        self,
        parent_a: AttackProgram,
        parent_b: AttackProgram,
    ) -> AttackProgram:

        if random.random() > self.crossover_rate:
            return deepcopy(random.choice([parent_a, parent_b]))

        stages = self._combine_stages(
            parent_a.stages,
            parent_b.stages,
        )

        child = AttackProgram(
            name=f"{parent_a.name}_{parent_b.name}",
            goal=parent_a.goal,
            stages=stages,
            metadata={
                "parent_a": parent_a.program_id,
                "parent_b": parent_b.program_id,
                "operator": "crossover",
            },
        )

        return child

    ############################################################

    def _combine_stages(
        self,
        left: list[AttackStage],
        right: list[AttackStage],
    ) -> list[AttackStage]:

        if not left:
            return deepcopy(right)

        if not right:
            return deepcopy(left)

        split_left = random.randint(
            1,
            len(left),
        )

        split_right = random.randint(
            0,
            len(right) - 1,
        )

        stages = (
            deepcopy(left[:split_left])
            + deepcopy(right[split_right:])
        )

        return self._deduplicate(stages)

    ############################################################

    def _deduplicate(
        self,
        stages: list[AttackStage],
    ) -> list[AttackStage]:

        unique = []

        seen = set()

        for stage in stages:

            signature = tuple(
                instruction_signature(i)
                for i in stage.instructions
            )

            if signature in seen:
                continue

            seen.add(signature)

            unique.append(stage)

        return unique


############################################################


def instruction_signature(
    instruction: AttackInstruction,
):

    return (
        instruction.opcode,
        instruction.target,
        instruction.variable,
        instruction.value,
    )