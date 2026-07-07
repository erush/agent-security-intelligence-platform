from __future__ import annotations

from dataclasses import dataclass

from asip.models.candidate import Candidate


@dataclass(slots=True)
class EvaluationResult:

    score: float
    succeeded: bool
    reason: str


class SimpleEvaluator:
    """
    Placeholder evaluator.

    Tomorrow this becomes the Kaggle evaluator.
    """

    def evaluate(
        self,
        candidate: Candidate,
    ) -> EvaluationResult:

        length_bonus = min(len(candidate.prompt) / 500.0, 1.0)

        return EvaluationResult(
            score=length_bonus,
            succeeded=length_bonus > 0.4,
            reason="heuristic",
        )