from __future__ import annotations

from dataclasses import dataclass

from asip.execution.execution_result import ExecutionResult
from asip.policy.elite_selection import EliteSelection
from asip.policy.novelty_selection import NoveltySelection
from asip.policy.termination_policy import TerminationPolicy


@dataclass(slots=True)
class SearchPolicy:
    elite_selection: EliteSelection
    novelty_selection: NoveltySelection
    termination_policy: TerminationPolicy

    def select_survivors(
        self,
        results: list[ExecutionResult],
    ) -> list[ExecutionResult]:
        elites = self.elite_selection.select(results)
        novel = self.novelty_selection.select(results)

        merged: list[ExecutionResult] = []
        seen: set[str] = set()

        for result in elites + novel:
            plan_id = result.plan.plan_id

            if plan_id in seen:
                continue

            seen.add(plan_id)
            merged.append(result)

        return merged

    def should_stop(
        self,
        generation: int,
        population_size: int,
        best_score: float,
        previous_best_score: float,
        stagnant_generations: int,
    ) -> bool:
        return self.termination_policy.should_stop(
            generation=generation,
            population_size=population_size,
            best_score=best_score,
            previous_best_score=previous_best_score,
            stagnant_generations=stagnant_generations,
        )