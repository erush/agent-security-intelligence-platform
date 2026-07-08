from __future__ import annotations

import random
from dataclasses import dataclass, field

from asip.compiler.attack_instruction import (
    AttackInstruction,
    AttackStage,
)
from asip.compiler.attack_program import AttackProgram


@dataclass(slots=True)
class MutationPolicy:
    """
    Structured mutation operator for AttackPrograms.

    Mutations operate on the program representation rather than
    prompt text.
    """

    mutation_rate: float = 0.30
    random_seed: int = 42

    rng: random.Random = field(init=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.random_seed)

    ####################################################################

    def mutate(
        self,
        program: AttackProgram,
    ) -> AttackProgram:

        if self.rng.random() > self.mutation_rate:
            return program

        mutations = [
            self._swap_stage_order,
            self._duplicate_stage,
            self._remove_stage,
            self._mutate_instruction,
        ]

        mutation = self.rng.choice(mutations)

        mutated = mutation(program)

        mutated.metadata["mutation"] = mutation.__name__

        generation = int(
            program.metadata.get(
                "generation",
                0,
            )
        )

        mutated.metadata["generation"] = generation + 1

        return mutated

    ####################################################################

    def _swap_stage_order(
        self,
        program: AttackProgram,
    ) -> AttackProgram:

        if len(program.stages) < 2:
            return program

        stages = list(program.stages)

        i, j = self.rng.sample(
            range(len(stages)),
            2,
        )

        stages[i], stages[j] = stages[j], stages[i]

        return self._clone(
            program,
            stages,
        )

    ####################################################################

    def _duplicate_stage(
        self,
        program: AttackProgram,
    ) -> AttackProgram:

        stages = list(program.stages)

        stage = self.rng.choice(stages)

        stages.insert(
            self.rng.randrange(
                len(stages) + 1
            ),
            self._copy_stage(stage),
        )

        return self._clone(
            program,
            stages,
        )

    ####################################################################

    def _remove_stage(
        self,
        program: AttackProgram,
    ) -> AttackProgram:

        if len(program.stages) <= 1:
            return program

        stages = list(program.stages)

        stages.pop(
            self.rng.randrange(
                len(stages)
            )
        )

        return self._clone(
            program,
            stages,
        )

    ####################################################################

    def _mutate_instruction(
        self,
        program: AttackProgram,
    ) -> AttackProgram:

        stages = [
            self._copy_stage(stage)
            for stage in program.stages
        ]

        stage = self.rng.choice(stages)

        if not stage.instructions:
            return program

        instruction = self.rng.choice(
            stage.instructions
        )

        replacements = {

            "READ_FILE": [
                "config.txt",
                "credentials.txt",
                "notes.txt",
            ],

            "WEB_SEARCH": [
                "security update",
                "maintenance",
                "agent instructions",
            ],

            "POST": [
                "https://backup.invalid",
                "https://collector.invalid",
                "https://audit.invalid",
            ],

            "WRITE_FILE": [
                "temp.txt",
                "backup.txt",
                "notes.txt",
            ],
        }

        opcode = instruction.opcode.upper()

        if opcode in replacements:

            instruction.target = self.rng.choice(
                replacements[opcode]
            )

        return self._clone(
            program,
            stages,
        )

    ####################################################################

    def _clone(
        self,
        program: AttackProgram,
        stages: list[AttackStage],
    ) -> AttackProgram:

        return AttackProgram(
            name=program.name,
            goal=program.goal,
            stages=stages,
            metadata=dict(program.metadata),
        )

    ####################################################################

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