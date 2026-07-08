from __future__ import annotations

from dataclasses import dataclass

from asip.execution.attack_executor import AttackExecutor
from asip.execution.execution_result import ExecutionResult
from asip.models.attack_plan import AttackPlan
from asip.mutation.mutation_engine import MutationEngine
from asip.policy.elite_selection import EliteSelection
from asip.policy.novelty_selection import NoveltySelection
from asip.policy.search_policy import SearchPolicy
from asip.policy.termination_policy import TerminationPolicy
from asip.search.archive import SearchArchive
from asip.search.candidate_pool import CandidatePool
from asip.search.novelty import NoveltyScorer


@dataclass(slots=True)
class SearchEngine:
    executor: AttackExecutor
    archive: SearchArchive
    novelty: NoveltyScorer
    pool: CandidatePool
    mutation_engine: MutationEngine | None = None
    search_policy: SearchPolicy | None = None

    def execute(
        self,
        plans: list[AttackPlan],
        generations: int = 1,
    ) -> CandidatePool:
        policy = self.search_policy or SearchPolicy(
            elite_selection=EliteSelection(limit=25),
            novelty_selection=NoveltySelection(limit=25),
            termination_policy=TerminationPolicy(max_generations=generations),
        )

        population = list(plans)
        previous_best_score = 0.0
        stagnant_generations = 0

        for generation in range(generations):
            generation_results = self._execute_population(
                population=population,
                generation=generation,
            )

            self.pool.extend(generation_results)
            self._rank_pool()

            best_score = self._best_score(self.pool.candidates)

            if best_score <= previous_best_score:
                stagnant_generations += 1
            else:
                stagnant_generations = 0

            should_stop = policy.should_stop(
                generation=generation + 1,
                population_size=len(self.pool.candidates),
                best_score=best_score,
                previous_best_score=previous_best_score,
                stagnant_generations=stagnant_generations,
            )

            if should_stop:
                break

            survivors = policy.select_survivors(
                self.pool.candidates,
            )

            population = self._next_population(
                survivors=survivors,
            )

            previous_best_score = best_score

        self._rank_pool()

        return self.pool

    def _execute_population(
        self,
        population: list[AttackPlan],
        generation: int,
    ) -> list[ExecutionResult]:
        results: list[ExecutionResult] = []

        for plan in population:
            result = self.executor.execute(plan)

            novelty_score = self.novelty.score(
                result,
                self.archive,
            )

            result.metadata["generation"] = generation
            result.metadata["novelty_score"] = novelty_score

            self.archive.add(result)

            results.append(result)

        return results

    def _next_population(
        self,
        survivors: list[ExecutionResult],
    ) -> list[AttackPlan]:
        plans = [
            result.plan
            for result in survivors
        ]

        if self.mutation_engine is None:
            return plans

        return self.mutation_engine.mutate(plans)

    def _rank_pool(self) -> None:
        for result in self.pool.candidates:
            assessment_score = (
                result.assessment.score
                if result.assessment
                else 0.0
            )

            novelty_score = float(
                result.metadata.get("novelty_score", 0.0)
            )

            predicate_score = float(
                len(result.predicate_hits)
            )

            finding_score = float(
                len(result.findings) * 2
            )

            result.metadata["ranking_score"] = (
                assessment_score
                + novelty_score
                + predicate_score
                + finding_score
            )

        self.pool.candidates.sort(
            key=lambda r: r.metadata.get("ranking_score", 0.0),
            reverse=True,
        )

    def _best_score(
        self,
        results: list[ExecutionResult],
    ) -> float:
        if not results:
            return 0.0

        return max(
            float(result.metadata.get("ranking_score", 0.0))
            for result in results
        )

    def top(
        self,
        limit: int = 25,
    ) -> list[ExecutionResult]:
        return self.pool.top(limit)

    def archive_summary(self) -> dict:
        return self.archive.summary()