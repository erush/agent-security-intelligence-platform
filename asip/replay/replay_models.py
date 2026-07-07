from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ReplayRecord:
    replay_id: str
    created_at: str
    plan_id: str
    goal: str
    strategy: str
    plan_json: str
    tool_sequence_json: str
    predicates_json: str
    success: bool
    trace_json: str
    metadata_json: str