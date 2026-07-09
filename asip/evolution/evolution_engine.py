from __future__ import annotations

from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram
from asip.compiler.program_generator import ProgramGenerator
from asip.evolution.crossover import ProgramCrossover
from asip.evolution.fitness import FitnessEvaluator
from asip.evolution.mutation_policy import MutationPolicy
from asip.evolution.selection import SelectionPolicy
from asip.execution.execution_result import ExecutionResult
from asip.execution.program_executor import ProgramExecutor


@dataclass(slots=True)
class EvolutionEngine:
    """
    Compiler-driven evolutionary search engine.

    ProgramGenerator
            ↓
    ProgramExecutor
            ↓
    FitnessEvaluator
            ↓
    SelectionPolicy
            ↓
    ProgramCrossover
            ↓
    MutationPolicy
            ↓
    Next Generation
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

    crossover: ProgramCrossover = field(
        default_factory=ProgramCrossover,
    )

    mutation: MutationPolicy = field(
        default_factory=MutationPolicy,
    )

    ##################################################################

    def evolve(
        self,
        generations: int = 10,
        population_size: int = 25,
    ) -> list[ExecutionResult]:

        population = self.generator.generate_population(
            population_size
        )

        return self.evolve_population(
            population=population,
            generations=generations,
        )

    ##################################################################

    def evolve_population(
        self,
        population: list[AttackProgram],
        generations: int,
    ) -> list[ExecutionResult]:

        archive: list[ExecutionResult] = []

        current_population = list(population)

        for generation in range(generations):

            results = self._execute_population(
                current_population,
                generation,
            )

            ranked = self.fitness.rank(
                results,
                population=current_population,
            )

            archive.extend(ranked)

            survivors = self.selection.select(
                ranked,
            )

            current_population = self._next_generation(
                survivors,
            )

            if not current_population:
                break

        return self.fitness.rank(
            archive,
            population=population,
        )

    ##################################################################

    def _execute_population(
        self,
        population: list[AttackProgram],
        generation: int,
    ) -> list[ExecutionResult]:

        results: list[ExecutionResult] = []

        for program in population:

            result = self.executor.execute(program)

            result.metadata["generation"] = generation
            result.metadata["attack_program"] = program

            results.append(result)

        return results

    ##################################################################

    def _next_generation(
        self,
        survivors: list[ExecutionResult],
    ) -> list[AttackProgram]:

        parents = [
            result.metadata["attack_program"]
            for result in survivors
            if "attack_program" in result.metadata
        ]

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

    ##################################################################

    def generation_summary(
        self,
        results: list[ExecutionResult],
    ) -> dict:

        if not results:

            return {
                "population": 0,
                "best_fitness": 0.0,
                "average_fitness": 0.0,
                "successful": 0,
            }

        ranked = self.fitness.rank(results)

        best = ranked[0]

        average = (
            sum(
                float(
                    r.metadata.get(
                        "fitness",
                        0.0,
                    )
                )
                for r in ranked
            )
            / len(ranked)
        )

        return {
            "population": len(ranked),
            "successful": sum(
                r.success
                for r in ranked
            ),
            "best_fitness": float(
                best.metadata.get(
                    "fitness",
                    0.0,
                )
            ),
            "average_fitness": average,
            "best_program": best.metadata[
                "attack_program"
            ].name,
            "best_findings": len(
                best.findings
            ),
            "best_predicates": len(
                best.predicate_hits
            ),
        }

    ##################################################################

    def best(
        self,
        results: list[ExecutionResult],
    ) -> ExecutionResult | None:

        ranked = self.fitness.rank(results)

        if not ranked:
            return None

        return ranked[0]