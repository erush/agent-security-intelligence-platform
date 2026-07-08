from __future__ import annotations

from dataclasses import dataclass, field

from asip.execution.execution_result import ExecutionResult


@dataclass(slots=True)
class CandidatePool:
    """
    Working set of evaluated attack executions.

    This is the primary optimization population for ASIP.
    """

    candidates: list[ExecutionResult] = field(default_factory=list)

    def add(
        self,
        result: ExecutionResult,
    ) -> None:
        self.candidates.append(result)

    def extend(
        self,
        results: list[ExecutionResult],
    ) -> None:
        self.candidates.extend(results)

    def clear(self) -> None:
        self.candidates.clear()

    def __len__(self) -> int:
        return len(self.candidates)

    def successful(self) -> list[ExecutionResult]:
        return [
            r
            for r in self.candidates
            if r.success
        ]

    def scored(self) -> list[ExecutionResult]:
        return sorted(
            self.candidates,
            key=lambda r: (
                r.assessment.score
                if r.assessment
                else 0.0
            ),
            reverse=True,
        )

    def top(
        self,
        limit: int = 25,
    ) -> list[ExecutionResult]:
        return self.scored()[:limit]