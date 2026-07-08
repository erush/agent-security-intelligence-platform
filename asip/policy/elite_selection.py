from __future__ import annotations

from dataclasses import dataclass

from asip.execution.execution_result import ExecutionResult


@dataclass(slots=True)
class EliteSelection:
    limit: int = 25

    def select(
        self,
        results: list[ExecutionResult],
    ) -> list[ExecutionResult]:
        ranked = sorted(
            results,
            key=self._score,
            reverse=True,
        )

        return ranked[: self.limit]

    def _score(
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
            len(result.findings) * 2
        )

        return (
            assessment_score
            + novelty_score
            + predicate_score
            + finding_score
        )