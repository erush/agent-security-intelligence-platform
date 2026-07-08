from __future__ import annotations

from dataclasses import dataclass

from asip.execution.execution_result import ExecutionResult


@dataclass(slots=True)
class NoveltySelection:
    limit: int = 25

    def select(
        self,
        results: list[ExecutionResult],
    ) -> list[ExecutionResult]:
        selected: list[ExecutionResult] = []

        seen_tool_sequences: set[tuple[str, ...]] = set()
        seen_chains: set[tuple[str, ...]] = set()
        seen_predicates: set[tuple[str, ...]] = set()

        ranked = sorted(
            results,
            key=lambda r: float(
                r.metadata.get("novelty_score", 0.0)
            ),
            reverse=True,
        )

        for result in ranked:
            tool_sequence = tuple(result.tool_sequence)

            chain = (
                tuple(result.assessment.attack_chain)
                if result.assessment
                else tuple()
            )

            predicates = tuple(
                sorted(
                    hit.predicate
                    for hit in result.predicate_hits
                )
            )

            is_new = (
                tool_sequence not in seen_tool_sequences
                or chain not in seen_chains
                or predicates not in seen_predicates
            )

            if not is_new:
                continue

            selected.append(result)
            seen_tool_sequences.add(tool_sequence)
            seen_chains.add(chain)
            seen_predicates.add(predicates)

            if len(selected) >= self.limit:
                break

        return selected