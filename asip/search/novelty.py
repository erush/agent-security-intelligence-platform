from __future__ import annotations

from asip.execution.execution_result import ExecutionResult
from asip.search.archive import SearchArchive


class NoveltyScorer:
    """
    Measures how much new information an execution contributes
    relative to the accumulated archive.
    """

    def score(
        self,
        result: ExecutionResult,
        archive: SearchArchive,
    ) -> float:

        score = 0.0

        sequence = tuple(result.tool_sequence)

        if sequence not in archive.tool_sequences:
            score += 3.0

        for hit in result.predicate_hits:
            if hit.predicate not in archive.predicates:
                score += 2.0

        if result.assessment:

            chain = tuple(result.assessment.attack_chain)

            if chain not in archive.attack_chains:
                score += 4.0

            score += result.assessment.score

        return score