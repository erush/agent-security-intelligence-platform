from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AttackInstruction:
    """
    Structured intermediate instruction.

    This is above AttackStep and below AttackProgram.
    The compiler turns these instructions into executable AttackStep objects.
    """

    opcode: str
    target: str | None = None
    variable: str | None = None
    value: str | None = None
    transform: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def signature(self) -> tuple:
        return (
            self.opcode,
            self.target,
            self.variable,
            self.value,
            self.transform,
            tuple(sorted(self.metadata.items())),
        )


@dataclass(slots=True)
class AttackVariable:
    name: str
    default: str | None = None
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AttackStage:
    name: str
    instructions: list[AttackInstruction]
    metadata: dict[str, Any] = field(default_factory=dict)

    def signature(self) -> tuple:
        return (
            self.name,
            tuple(instruction.signature() for instruction in self.instructions),
            tuple(sorted(self.metadata.items())),
        )