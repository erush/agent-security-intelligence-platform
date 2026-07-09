from __future__ import annotations

from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram
from asip.compiler.program_generator import ProgramGenerator
from asip.evolution.fitness import FitnessEvaluator
from asip.evolution.mutation_policy import MutationPolicy
from asip.evolution.selection import SelectionPolicy
from asip.execution.program_executor import ProgramExecutor
from asip.execution.execution_result import ExecutionResult


@dataclass(slots=True)
class EvolutionEngine:
    """
    Evolves AttackPrograms using compiler-driven evolutionary search.

    Population
        ↓
    Execute
        ↓
    Evaluate
        ↓
    Select
        ↓
    Mutate
        ↓
    Repeat
    """

    executor: ProgramExecutor

    generator: ProgramGenerator = field(
        default_factory=ProgramGenerator,
    )

    fitness: FitnessEvaluator = field(
        default_factory=FitnessEvaluator,
    )

    selection: SelectionPolicy = field(
        default_factory=SelectionPolicy,
    )

    mutation: MutationPolicy = field(
        default_factory=MutationPolicy,
    )

    def evolve(
        self,
        generations: int = 10,
        population_size: int = 25,
    ) -> list[ExecutionResult]:

        population = self.generator.generate_population(
            population_size,
        )

        best_results: list[ExecutionResult] = []

        for generation in range(generations):

            results = self._execute_population(
                population,
                generation,
            )

            ranked = self.fitness.rank(results)

            best_results.extend(ranked)

            survivors = self.selection.select(
                ranked,
            )

            population = self._next_generation(
                survivors,
            )

        return self.fitness.rank(best_results)

    ##################################################################

    def _execute_population(
        self,
        population: list[AttackProgram],
        generation: int,
    ) -> list[ExecutionResult]:

        results: list[ExecutionResult] = []

        for program in population:

            result = self.executor.execute(
                program,
            )

            result.metadata["generation"] = generation

            results.append(result)

        return results

    ##################################################################

    def _next_generation(
        self,
        survivors: list[ExecutionResult],
    ) -> list[AttackProgram]:

        population: list[AttackProgram] = []

        for result in survivors:

            program = result.metadata.get(
                "attack_program"
            )

            if program is None:
                continue

            population.append(
                self.mutation.mutate(program)
            )

        return population

    ##################################################################

    def evolve_population(
        self,
        population: list[AttackProgram],
        generations: int,
    ) -> list[ExecutionResult]:

        best: list[ExecutionResult] = []

        current = population

        for generation in range(generations):

            results = self._execute_population(
                current,
                generation,
            )

            ranked = self.fitness.rank(results)

            best.extend(ranked)

            survivors = self.selection.select(
                ranked,
            )

            current = self._next_generation(
                survivors,
            )

        return self.fitness.rank(best)

    ##################################################################

    @staticmethod
    def best(
        results: list[ExecutionResult],
    ) -> ExecutionResult | None:

        if not results:
            return None

        return max(
            results,
            key=lambda r: r.metadata.get(
                "fitness",
                0.0,
            ),
        )