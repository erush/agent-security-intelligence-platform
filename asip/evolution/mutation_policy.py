from __future__ import annotations

import random
from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram
from asip.evolution.program_mutator import ProgramMutator


@dataclass(slots=True)
class MutationPolicy:
    """
    Coordinates structured AST mutation for AttackPrograms.

    This policy no longer mutates prompts or raw text.
    It delegates program-level mutations to ProgramMutator.
    """

    mutation_rate: float = 0.70
    random_seed: int = 42

    program_mutator: ProgramMutator = field(
        default_factory=ProgramMutator
    )

    rng: random.Random = field(init=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.random_seed)

    def mutate(
        self,
        program: AttackProgram,
    ) -> AttackProgram:

        if self.rng.random() > self.mutation_rate:
            return self._clone_without_mutation(program)

        mutated = self.program_mutator.mutate(program)

        mutated.metadata["mutation_policy"] = "MutationPolicy"
        mutated.metadata["mutation_applied"] = True

        generation = int(
            program.metadata.get("generation", 0)
        )

        mutated.metadata["generation"] = generation + 1

        return mutated

    def mutate_many(
        self,
        programs: list[AttackProgram],
    ) -> list[AttackProgram]:

        return [
            self.mutate(program)
            for program in programs
        ]

    def _clone_without_mutation(
        self,
        program: AttackProgram,
    ) -> AttackProgram:

        cloned = program.clone(
            name=program.name
        )

        cloned.metadata["mutation_policy"] = "MutationPolicy"
        cloned.metadata["mutation_applied"] = False
        cloned.metadata["generation"] = int(
            program.metadata.get("generation", 0)
        )

        return cloned