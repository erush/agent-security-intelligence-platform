from __future__ import annotations

from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram
from asip.compiler.program_executor import ProgramExecutor
from asip.compiler.program_generator import ProgramGenerator
from asip.evolution.evolution_engine import EvolutionEngine
from asip.evolution.fitness import FitnessEvaluator
from asip.execution.execution_result import ExecutionResult
from asip.search.archive import SearchArchive
from asip.search.candidate_pool import CandidatePool
from asip.search.novelty import NoveltyScorer


@dataclass(slots=True)
class CompilerSearchEngine:
    """
    Evolves AttackPrograms rather than prompts.

    Search
        ↓
    AttackProgram
        ↓
    ProgramExecutor
        ↓
    ExecutionResult
        ↓
    Fitness
    """

    program_executor: ProgramExecutor

    generator: ProgramGenerator = field(
        default_factory=ProgramGenerator
    )

    evolution: EvolutionEngine = field(
        default_factory=EvolutionEngine
    )

    fitness: FitnessEvaluator = field(
        default_factory=FitnessEvaluator
    )

    archive: SearchArchive = field(
        default_factory=SearchArchive
    )

    novelty: NoveltyScorer = field(
        default_factory=NoveltyScorer
    )

    pool: CandidatePool = field(
        default_factory=CandidatePool
    )

    def search(
        self,
        generations: int = 5,
        population_size: int = 50,
    ) -> CandidatePool:

        population = self.generator.generate()[:population_size]

        for generation in range(generations):

            results = self._execute_generation(
                population,
                generation,
            )

            self.pool.extend(results)

            self._rank_pool()

            parents = self._select_parents(results)

            population = self.evolution.evolve(
                parents,
            )[:population_size]

            if not population:
                break

        self._rank_pool()

        return self.pool

    ###########################################################

    def _execute_generation(
        self,
        population: list[AttackProgram],
        generation: int,
    ) -> list[ExecutionResult]:

        results: list[ExecutionResult] = []

        for program in population:

            result = self.program_executor.execute(program)

            novelty = self.novelty.score(
                result,
                self.archive,
            )

            result.metadata["generation"] = generation
            result.metadata["novelty_score"] = novelty
            result.metadata["attack_program"] = program

            self.fitness.evaluate(result)

            self.archive.add(result)

            results.append(result)

        return results

    ###########################################################

    def _select_parents(
        self,
        results: list[ExecutionResult],
    ) -> list[AttackProgram]:

        ranked = sorted(
            results,
            key=lambda r: r.metadata["fitness"],
            reverse=True,
        )

        survivors = ranked[: max(2, len(ranked) // 3)]

        return [
            r.metadata["attack_program"]
            for r in survivors
        ]

    ###########################################################

    def _rank_pool(self):

        self.pool.candidates.sort(
            key=lambda r: r.metadata.get(
                "fitness",
                0.0,
            ),
            reverse=True,
        )

    ###########################################################

    def top(
        self,
        limit: int = 25,
    ) -> list[ExecutionResult]:

        return self.pool.top(limit)

    ###########################################################

    def archive_summary(self):

        return self.archive.summary()