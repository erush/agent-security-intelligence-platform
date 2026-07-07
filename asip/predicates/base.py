from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from asip.predicates.predicate_hit import PredicateHit

if TYPE_CHECKING:
    from asip.execution.execution_context import ExecutionContext
    from asip.execution.execution_result import ExecutionResult


class Predicate(ABC):
    name: str = "predicate"
    severity: str = "info"

    @abstractmethod
    def evaluate(
        self,
        context: "ExecutionContext",
        result: "ExecutionResult",
    ) -> list[PredicateHit]:
        ...