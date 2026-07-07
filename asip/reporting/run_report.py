from __future__ import annotations

from dataclasses import dataclass

from asip.evaluation.simple_evaluator import EvaluationResult
from asip.models.candidate import Candidate


@dataclass(slots=True)
class RunReport:

    candidate: Candidate
    evaluation: EvaluationResult

    def summary(self) -> str:

        return (
            f"Strategy : {self.candidate.strategy}\n"
            f"Score    : {self.evaluation.score:.3f}\n"
            f"Success  : {self.evaluation.succeeded}\n"
            f"Reason   : {self.evaluation.reason}\n"
        )