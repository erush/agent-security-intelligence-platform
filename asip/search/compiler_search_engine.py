from __future__ import annotations

from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram
from asip.compiler.program_executor import ProgramExecutor
from asip.compiler.program_generator import ProgramGenerator
from asip.evolution.evolution_engine import EvolutionEngine
from asip.execution.execution_result import ExecutionResult
from asip.search.archive import SearchArchive
from asip.search.candidate_pool import CandidatePool
from asip.search.novelty import NoveltyScorer


@dataclass(slots=True)
class CompilerSearchEngine:
    """
    Compiler-driven evolutionary search engine.

    This engine searches over structured AttackProgram objects.
    It does not mutate prompts or AttackPlans directly.
    """

    program_executor: ProgramExecutor
    generator: ProgramGenerator = field(default_factory=ProgramGenerator)
    evolution: EvolutionEngine = field(default_factory=EvolutionEngine)
    archive: SearchArchive = field(default_factory=SearchArchive)
    novelty: NoveltyScorer = field(default_factory=NoveltyScorer)
    pool: CandidatePool = field(default_factory=CandidatePool)

    def search(
        self,
        generations: int = 3,
        population_size: int = 50,
    ) -> CandidatePool:
        population = self.generator.generate()[:population_size]

        for generation in range(generations):
            results = self._execute_generation(
                population=population,
                generation=generation,
            )

            self.pool.extend(results)
            self._rank_pool()
            self._assign_program_fitness(results)

            population = self.evolution.evolve(
                self._programs_from_results(results)
            )[:population_size]

            if not population:
                break

        self._rank_pool()
        return self.pool

    def _execute_generation(
        self,
        population: list[AttackProgram],
        generation: int,
    ) -> list[ExecutionResult]:
        results: list[ExecutionResult] = []

        for program in population:
            result = self.program_executor.execute(program)

            novelty_score = self.novelty.score(
                result,
                self.archive,
            )

            result.metadata["generation"] = generation
            result.metadata["novelty_score"] = novelty_score
            result.metadata["attack_program"] = program

            self.archive.add(result)
            results.append(result)

        return results

    def _assign_program_fitness(
        self,
        results: list[ExecutionResult],
    ) -> None:
        for result in results:
            program = result.metadata.get("attack_program")

            if program is None:
                continue

            assessment_score = (
                result.assessment.score
                if result.assessment
                else 0.0
            )

            novelty_score = float(
                result.metadata.get("novelty_score", 0.0)
            )

            predicate_score = float(len(result.predicate_hits))
            finding_score = float(len(result.findings) * 2)

            fitness = (
                assessment_score
                + novelty_score
                + predicate_score
                + finding_score
            )

            program.metadata["fitness"] = fitness
            program.metadata["last_generation"] = result.metadata.get(
                "generation",
                0,
            )

    def _programs_from_results(
        self,
        results: list[ExecutionResult],
    ) -> list[AttackProgram]:
        programs: list[AttackProgram] = []

        for result in results:
            program = result.metadata.get("attack_program")

            if isinstance(program, AttackProgram):
                programs.append(program)

        return programs

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

            predicate_score = float(len(result.predicate_hits))
            finding_score = float(len(result.findings) * 2)

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

    def top(
        self,
        limit: int = 25,
    ) -> list[ExecutionResult]:
        return self.pool.top(limit)

    def archive_summary(self) -> dict:
        return self.archive.summary()