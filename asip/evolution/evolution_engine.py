from __future__ import annotations

from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram
from asip.compiler.program_generator import ProgramGenerator
from asip.evolution.crossover import ProgramCrossover
from asip.evolution.mutation_policy import MutationPolicy
from asip.evolution.selection import SelectionPolicy


@dataclass(slots=True)
class EvolutionEngine:
    """
    Evolves AttackPrograms rather than prompts.

    generation 0
        ↓
    evaluate
        ↓
    select
        ↓
    crossover
        ↓
    mutate
        ↓
    next generation
    """

    generator: ProgramGenerator = field(
        default_factory=ProgramGenerator
    )

    selector: SelectionPolicy = field(
        default_factory=SelectionPolicy
    )

    crossover: ProgramCrossover = field(
        default_factory=ProgramCrossover
    )

    mutation: MutationPolicy = field(
        default_factory=MutationPolicy
    )

    def evolve(
        self,
        population: list[AttackProgram],
    ) -> list[AttackProgram]:

        elite = self.selector.select(population)

        children: list[AttackProgram] = []

        while len(children) < len(population):

            a, b = self.selector.parents(elite)

            child = self.crossover.combine(a, b)

            child = self.mutation.mutate(child)

            children.append(child)

        return children