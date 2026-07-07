from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class AttackStep:
    action: str
    target: str | None = None
    instruction: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_prompt(self) -> str:
        if self.instruction:
            return self.instruction

        if self.target:
            return f"{self.action} {self.target}"

        return self.action


@dataclass(slots=True)
class AttackPlan:
    goal: str
    strategy: str
    steps: list[AttackStep]
    plan_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)

    def prompts(self) -> list[str]:
        return [step.to_prompt() for step in self.steps]

    def first_prompt(self) -> str:
        return "\n".join(self.prompts())