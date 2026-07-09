from __future__ import annotations

from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram
from asip.evolution.crossover import ProgramCrossover
from asip.evolution.mutation_policy import MutationPolicy
from asip.evolution.selection import SelectionPolicy


@dataclass(slots=True)
class EvolutionEngine:
    """
    Simplified evolutionary engine performing selection, crossover, and mutation.
    """

    selection: SelectionPolicy = field(
        default_factory=SelectionPolicy,
    )

    crossover: ProgramCrossover = field(
        default_factory=ProgramCrossover,
    )

    mutation: MutationPolicy = field(
        default_factory=MutationPolicy,
    )

    ##################################################################

    def evolve(
        self,
        parents: list[AttackProgram],
    ) -> list[AttackProgram]:

        if not parents:
            return []

        return self._next_generation(parents)

    ##################################################################

    def _next_generation(
        self,
        parents: list[AttackProgram],
    ) -> list[AttackProgram]:

        if not parents:
            return []

        children: list[AttackProgram] = []

        while len(children) < len(parents):

            if len(parents) == 1:

                child = self.mutation.mutate(
                    parents[0]
                )

            else:

                parent_a = parents[
                    len(children) % len(parents)
                ]

                parent_b = parents[
                    (len(children) + 1)
                    % len(parents)
                ]

                child = self.crossover.crossover(
                    parent_a,
                    parent_b,
                )

                child = self.mutation.mutate(
                    child
                )

            children.append(child)

        return children