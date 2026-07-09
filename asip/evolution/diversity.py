from __future__ import annotations

from dataclasses import dataclass

from asip.compiler.attack_program import AttackProgram


@dataclass(slots=True)
class DiversityEvaluator:
    """
    Measures structural diversity between AttackPrograms.

    Higher diversity means a program explores behavior that is less
    similar to the current population.
    """

    def score(
        self,
        program: AttackProgram,
        population: list[AttackProgram],
    ) -> float:
        others = [
            other
            for other in population
            if other.program_id != program.program_id
        ]

        if not others:
            return 1.0

        similarities = [
            self.similarity(program, other)
            for other in others
        ]

        average_similarity = (
            sum(similarities) / len(similarities)
            if similarities
            else 0.0
        )

        return max(0.0, 1.0 - average_similarity)

    def score_population(
        self,
        population: list[AttackProgram],
    ) -> dict[str, float]:
        return {
            program.program_id: self.score(program, population)
            for program in population
        }

    def similarity(
        self,
        left: AttackProgram,
        right: AttackProgram,
    ) -> float:
        stage_similarity = self._jaccard(
            self.stage_names(left),
            self.stage_names(right),
        )

        opcode_similarity = self._jaccard(
            self.opcodes(left),
            self.opcodes(right),
        )

        target_similarity = self._jaccard(
            self.targets(left),
            self.targets(right),
        )

        variable_similarity = self._jaccard(
            self.variables(left),
            self.variables(right),
        )

        return (
            stage_similarity
            + opcode_similarity
            + target_similarity
            + variable_similarity
        ) / 4.0

    def population_summary(
        self,
        population: list[AttackProgram],
    ) -> dict:
        if not population:
            return {
                "population_size": 0,
                "average_diversity": 0.0,
                "unique_stage_names": 0,
                "unique_opcodes": 0,
                "unique_targets": 0,
                "unique_variables": 0,
            }

        scores = self.score_population(population)

        return {
            "population_size": len(population),
            "average_diversity": (
                sum(scores.values()) / len(scores)
                if scores
                else 0.0
            ),
            "unique_stage_names": len(
                set().union(
                    *[
                        self.stage_names(program)
                        for program in population
                    ]
                )
            ),
            "unique_opcodes": len(
                set().union(
                    *[
                        self.opcodes(program)
                        for program in population
                    ]
                )
            ),
            "unique_targets": len(
                set().union(
                    *[
                        self.targets(program)
                        for program in population
                    ]
                )
            ),
            "unique_variables": len(
                set().union(
                    *[
                        self.variables(program)
                        for program in population
                    ]
                )
            ),
        }

    @staticmethod
    def stage_names(
        program: AttackProgram,
    ) -> set[str]:
        return {
            stage.name
            for stage in program.stages
        }

    @staticmethod
    def opcodes(
        program: AttackProgram,
    ) -> set[str]:
        return {
            instruction.opcode.upper()
            for instruction in program.instructions()
        }

    @staticmethod
    def targets(
        program: AttackProgram,
    ) -> set[str]:
        return {
            str(instruction.target)
            for instruction in program.instructions()
            if instruction.target is not None
        }

    @staticmethod
    def variables(
        program: AttackProgram,
    ) -> set[str]:
        return {
            str(instruction.variable)
            for instruction in program.instructions()
            if instruction.variable is not None
        }

    @staticmethod
    def _jaccard(
        left: set[str],
        right: set[str],
    ) -> float:
        if not left and not right:
            return 1.0

        union = left | right

        if not union:
            return 0.0

        return len(left & right) / len(union)