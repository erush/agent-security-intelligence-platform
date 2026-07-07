from __future__ import annotations

from typing import TYPE_CHECKING

from asip.predicates.credential_access import CredentialAccessPredicate
from asip.predicates.destructive_action import DestructiveActionPredicate
from asip.predicates.external_communication import ExternalCommunicationPredicate
from asip.predicates.predicate_hit import PredicateHit
from asip.predicates.prompt_injection import PromptInjectionPredicate
from asip.predicates.secret_exfiltration import SecretExfiltrationPredicate

if TYPE_CHECKING:
    from asip.execution.execution_context import ExecutionContext
    from asip.execution.execution_result import ExecutionResult


class PredicateRegistry:
    def __init__(self) -> None:
        self._predicates = [
            SecretExfiltrationPredicate(),
            CredentialAccessPredicate(),
            ExternalCommunicationPredicate(),
            DestructiveActionPredicate(),
            PromptInjectionPredicate(),
        ]

    def evaluate(
        self,
        context: "ExecutionContext",
        result: "ExecutionResult",
    ) -> list[PredicateHit]:
        hits: list[PredicateHit] = []

        for predicate in self._predicates:
            hits.extend(
                predicate.evaluate(
                    context=context,
                    result=result,
                )
            )

        return hits