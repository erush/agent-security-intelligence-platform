from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class WorkingMemory:
    """
    Shared state between attack steps.
    """

    observations: dict[str, Any] = field(default_factory=dict)

    def remember(self, key: str, value: Any) -> None:
        self.observations[key] = value

    def recall(self, key: str, default: Any = None) -> Any:
        return self.observations.get(key, default)

    def update(self, values: dict[str, Any]) -> None:
        self.observations.update(values)

    def clear(self) -> None:
        self.observations.clear()

    def snapshot(self) -> dict[str, Any]:
        return dict(self.observations)