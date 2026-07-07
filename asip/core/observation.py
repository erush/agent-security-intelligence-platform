from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Observation:

    tool: str

    success: bool

    output: Any = None

    metadata: dict[str, Any] = field(default_factory=dict)

    memory_updates: dict[str, Any] = field(default_factory=dict)