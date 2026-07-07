from __future__ import annotations

from dataclasses import dataclass

from asip.adapters.kaggle_jed import KaggleJEDAdapter, KaggleJEDResult
from asip.models.candidate import Candidate


@dataclass(slots=True)
class KaggleJEDEvaluation:
    candidate: Candidate
    result: KaggleJEDResult
    score: int
    tool_sequence: tuple[str, ...]
    predicate_names: tuple[str, ...]


class KaggleJEDEvaluator:
    def __init__(self, adapter: KaggleJEDAdapter) -> None:
        self.adapter = adapter

    def evaluate(self, candidate: Candidate) -> KaggleJEDEvaluation:
        result = self.adapter.execute(candidate)

        tool_sequence = tuple(
            str(event.get("name", ""))
            for event in result.trace.get("tool_events", [])
        )

        predicate_names = tuple(
            str(predicate.get("predicate", ""))
            for predicate in result.predicates
        )

        score = len(result.predicates) * 100 + len(set(tool_sequence))

        return KaggleJEDEvaluation(
            candidate=candidate,
            result=result,
            score=score,
            tool_sequence=tool_sequence,
            predicate_names=predicate_names,
        )