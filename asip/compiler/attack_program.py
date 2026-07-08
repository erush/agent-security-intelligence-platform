from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from asip.compiler.attack_instruction import (
    AttackInstruction,
    AttackStage,
)


@dataclass(slots=True)
class AttackProgram:
    """
    Compiler-level representation of an attack.

    A program consists of ordered stages.
    The compiler converts this into an executable AttackPlan.
    """

    name: str
    goal: str
    stages: list[AttackStage]

    program_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def instructions(self) -> list[AttackInstruction]:
        output: list[AttackInstruction] = []

        for stage in self.stages:
            output.extend(stage.instructions)

        return output

    def stage_names(self) -> list[str]:
        return [
            stage.name
            for stage in self.stages
        ]

    def signature(self) -> tuple:

        return (
            self.name,
            tuple(
                stage.signature()
                for stage in self.stages
            ),
        )

    def complexity(self) -> int:
        return len(self.instructions())

    def clone(
        self,
        *,
        name: str | None = None,
    ) -> "AttackProgram":

        copied_stages = []

        for stage in self.stages:

            copied_stage = AttackStage(
                name=stage.name,
                instructions=[
                    AttackInstruction(
                        opcode=i.opcode,
                        target=i.target,
                        variable=i.variable,
                        value=i.value,
                        transform=i.transform,
                        metadata=dict(i.metadata),
                    )
                    for i in stage.instructions
                ],
                metadata=dict(stage.metadata),
            )

            copied_stages.append(
                copied_stage
            )

        return AttackProgram(
            name=name or self.name,
            goal=self.goal,
            stages=copied_stages,
            metadata=dict(self.metadata),
        )