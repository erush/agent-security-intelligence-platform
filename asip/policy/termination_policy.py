from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TerminationPolicy:
    max_generations: int = 3
    max_population: int = 500
    patience: int = 2
    min_improvement: float = 0.01

    def should_stop(
        self,
        generation: int,
        population_size: int,
        best_score: float,
        previous_best_score: float,
        stagnant_generations: int,
    ) -> bool:
        if generation >= self.max_generations:
            return True

        if population_size >= self.max_population:
            return True

        improvement = best_score - previous_best_score

        if improvement < self.min_improvement:
            if stagnant_generations >= self.patience:
                return True

        return False