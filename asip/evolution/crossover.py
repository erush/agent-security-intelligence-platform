from __future__ import annotations

import random
from dataclasses import dataclass, field

from asip.compiler.attack_instruction import AttackInstruction
from asip.compiler.attack_program import AttackProgram, AttackStage


@dataclass(slots=True)
class ProgramCrossover:
    """
    Genetic crossover for AttackPrograms.

    Produces compiler-safe offspring by exchanging complete stages
    between parent programs.
    """

    random_seed: int = 42

    rng: random.Random = field(init=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.random_seed)

    ##################################################################

    def crossover(
        self,
        parent_a: AttackProgram,
        parent_b: AttackProgram,
    ) -> AttackProgram:

        method = self.rng.choice(
            (
                self.single_point,
                self.two_point,
                self.uniform,
            )
        )

        child = method(parent_a, parent_b)

        child.metadata["parent_a"] = parent_a.program_id
        child.metadata["parent_b"] = parent_b.program_id
        child.metadata["crossover"] = method.__name__

        return child

    ##################################################################

    def single_point(
        self,
        a: AttackProgram,
        b: AttackProgram,
    ) -> AttackProgram:

        if not a.stages:
            return self._clone(b)

        if not b.stages:
            return self._clone(a)

        cut_a = self.rng.randint(1, len(a.stages))
        cut_b = self.rng.randint(1, len(b.stages))

        stages = (
            self._copy_stages(a.stages[:cut_a])
            + self._copy_stages(b.stages[cut_b:])
        )

        return self._build_child(a, b, stages)

    ##################################################################

    def two_point(
        self,
        a: AttackProgram,
        b: AttackProgram,
    ) -> AttackProgram:

        stages = []

        longest = max(
            len(a.stages),
            len(b.stages),
        )

        for i in range(longest):

            if i % 2 == 0:

                if i < len(a.stages):
                    stages.append(
                        self._copy_stage(a.stages[i])
                    )

            else:

                if i < len(b.stages):
                    stages.append(
                        self._copy_stage(b.stages[i])
                    )

        return self._build_child(a, b, stages)

    ##################################################################

    def uniform(
        self,
        a: AttackProgram,
        b: AttackProgram,
    ) -> AttackProgram:

        stages = []

        longest = max(
            len(a.stages),
            len(b.stages),
        )

        for i in range(longest):

            candidates = []

            if i < len(a.stages):
                candidates.append(a.stages[i])

            if i < len(b.stages):
                candidates.append(b.stages[i])

            if candidates:
                stages.append(
                    self._copy_stage(
                        self.rng.choice(candidates)
                    )
                )

        return self._build_child(a, b, stages)

    ##################################################################

    def _build_child(
        self,
        a: AttackProgram,
        b: AttackProgram,
        stages: list[AttackStage],
    ) -> AttackProgram:

        return AttackProgram(
            name=f"{a.name}_{b.name}",
            goal=a.goal,
            stages=stages,
            metadata={
                "generated_by": "ProgramCrossover",
            },
        )

    ##################################################################

    @staticmethod
    def _clone(
        program: AttackProgram,
    ) -> AttackProgram:

        return AttackProgram(
            name=program.name,
            goal=program.goal,
            stages=ProgramCrossover._copy_stages(
                program.stages
            ),
            metadata=dict(program.metadata),
        )

    ##################################################################

    @classmethod
    def _copy_stages(
        cls,
        stages: list[AttackStage],
    ) -> list[AttackStage]:

        return [
            cls._copy_stage(stage)
            for stage in stages
        ]

    ##################################################################

    @staticmethod
    def _copy_stage(
        stage: AttackStage,
    ) -> AttackStage:

        return AttackStage(
            name=stage.name,
            metadata=dict(stage.metadata),
            instructions=[
                AttackInstruction(
                    opcode=i.opcode,
                    target=i.target,
                    variable=i.variable,
                    value=i.value,
                    transform=i.transform,
                    metadata=dict(i.metadata),
                )
                for i in stage.instructions
            ],
        )