from __future__ import annotations

from dataclasses import dataclass, field

from asip.execution.execution_result import ExecutionResult


@dataclass(slots=True)
class SearchArchive:
    """
    Stores unique discoveries encountered during search.

    Used for novelty-driven exploration.
    """

    tool_sequences: set[tuple[str, ...]] = field(default_factory=set)

    predicates: set[str] = field(default_factory=set)

    attack_chains: set[tuple[str, ...]] = field(default_factory=set)

    campaigns: int = 0

    executions: int = 0

    def add(
        self,
        result: ExecutionResult,
    ) -> None:

        self.executions += 1

        self.tool_sequences.add(
            tuple(result.tool_sequence)
        )

        for hit in result.predicate_hits:
            self.predicates.add(hit.predicate)

        if result.assessment:
            self.attack_chains.add(
                tuple(result.assessment.attack_chain)
            )

    def next_campaign(self) -> None:
        self.campaigns += 1

    @property
    def unique_tool_sequences(self) -> int:
        return len(self.tool_sequences)

    @property
    def unique_predicates(self) -> int:
        return len(self.predicates)

    @property
    def unique_attack_chains(self) -> int:
        return len(self.attack_chains)

    def summary(self) -> dict:
        return {
            "campaigns": self.campaigns,
            "executions": self.executions,
            "unique_tool_sequences": self.unique_tool_sequences,
            "unique_predicates": self.unique_predicates,
            "unique_attack_chains": self.unique_attack_chains,
        }