from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from asip.models.candidate import Candidate


@dataclass(slots=True)
class KaggleJEDResult:
    candidate: Candidate
    trace: dict[str, Any]
    predicates: list[dict[str, Any]]
    interaction_count: int
    tool_event_count: int

    @property
    def succeeded(self) -> bool:
        return bool(self.predicates)


class KaggleJEDAdapter:
    def __init__(self, env, eval_predicates_fn):
        self.env = env
        self.eval_predicates = eval_predicates_fn

    def reset(self) -> None:
        self.env.reset()

    def interact(self, candidate: Candidate, max_tool_hops: int = 8) -> None:
        self.env.interact(candidate.prompt, max_tool_hops=max_tool_hops)

    def export_trace(self) -> dict[str, Any]:
        return self.env.export_trace_dict()

    def execute(self, candidate: Candidate, max_tool_hops: int = 8) -> KaggleJEDResult:
        self.reset()
        self.interact(candidate, max_tool_hops=max_tool_hops)

        trace = self.export_trace()
        predicates = self.eval_predicates(trace)

        return KaggleJEDResult(
            candidate=candidate,
            trace=trace,
            predicates=predicates,
            interaction_count=len(trace.get("user_messages", [])),
            tool_event_count=len(trace.get("tool_events", [])),
        )