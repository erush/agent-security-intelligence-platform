from __future__ import annotations

from dataclasses import dataclass

from asip.execution.execution_result import ExecutionResult


@dataclass(slots=True)
class FitnessEvaluator:
    """
    Central scoring policy for evolutionary attack search.

    Higher fitness means the execution is more valuable for the next generation.
    """

    assessment_weight: float = 1.0
    novelty_weight: float = 1.0
    predicate_weight: float = 1.0
    finding_weight: float = 2.0
    success_bonus: float = 5.0

    def evaluate(
        self,
        result: ExecutionResult,
    ) -> float:
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
            len(result.findings)
        )

        success_score = (
            self.success_bonus
            if result.success
            else 0.0
        )

        fitness = (
            assessment_score * self.assessment_weight
            + novelty_score * self.novelty_weight
            + predicate_score * self.predicate_weight
            + finding_score * self.finding_weight
            + success_score
        )

        result.metadata["fitness"] = fitness

        program = result.metadata.get("attack_program")

        if program is not None:
            program.metadata["fitness"] = fitness
            program.metadata["last_score"] = assessment_score
            program.metadata["last_success"] = result.success
            program.metadata["last_predicates"] = len(result.predicate_hits)
            program.metadata["last_findings"] = len(result.findings)

        return fitness

    def evaluate_many(
        self,
        results: list[ExecutionResult],
    ) -> list[float]:
        return [
            self.evaluate(result)
            for result in results
        ]

    def best(
        self,
        results: list[ExecutionResult],
    ) -> ExecutionResult | None:
        if not results:
            return None

        for result in results:
            if "fitness" not in result.metadata:
                self.evaluate(result)

        return max(
            results,
            key=lambda r: float(
                r.metadata.get("fitness", 0.0)
            ),
        )