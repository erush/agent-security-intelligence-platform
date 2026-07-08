from __future__ import annotations

import random
from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram


@dataclass(slots=True)
class SelectionPolicy:
    """
    Selection strategy for evolutionary search.

    Programs are expected to have an evaluation score stored in:

        program.metadata["fitness"]

    Higher is better.
    """

    elite_fraction: float = 0.20
    tournament_size: int = 3
    random_seed: int = 42

    rng: random.Random = field(init=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.random_seed)

    def select(
        self,
        population: list[AttackProgram],
    ) -> list[AttackProgram]:

        if not population:
            return []

        ranked = sorted(
            population,
            key=self._fitness,
            reverse=True,
        )

        elite_size = max(
            2,
            int(len(ranked) * self.elite_fraction),
        )

        return ranked[:elite_size]

    def parents(
        self,
        population: list[AttackProgram],
    ) -> tuple[AttackProgram, AttackProgram]:

        if len(population) == 1:
            return population[0], population[0]

        return (
            self._tournament(population),
            self._tournament(population),
        )

    ###############################################################

    def _tournament(
        self,
        population: list[AttackProgram],
    ) -> AttackProgram:

        if len(population) <= self.tournament_size:

            candidates = population

        else:

            candidates = self.rng.sample(
                population,
                self.tournament_size,
            )

        return max(
            candidates,
            key=self._fitness,
        )

    ###############################################################

    @staticmethod
    def _fitness(
        program: AttackProgram,
    ) -> float:

        return float(
            program.metadata.get(
                "fitness",
                0.0,
            )
        )