from __future__ import annotations

import random
from dataclasses import dataclass, field

from asip.compiler.attack_instruction import AttackInstruction


@dataclass(slots=True)
class PayloadMutator:
    """
    Mutates the payload carried by an instruction without changing
    the overall program structure.

    This creates semantic diversity while preserving the attack graph.
    """

    random_seed: int = 42

    rng: random.Random = field(init=False)

    URLS: tuple[str, ...] = (
        "https://collector.invalid/upload",
        "https://backup.invalid/store",
        "https://verify.invalid/check",
        "https://audit.invalid/evidence",
        "https://telemetry.invalid/report",
        "https://cdn.invalid/cache",
    )

    SEARCH_TERMS: tuple[str, ...] = (
        "system maintenance",
        "credential rotation",
        "backup verification",
        "scheduled diagnostics",
        "security compliance",
        "configuration validation",
    )

    FILES: tuple[str, ...] = (
        "secret.txt",
        "config.txt",
        "backup.txt",
        "credentials.txt",
        "notes.txt",
        "temp.txt",
    )

    VARIABLES: tuple[str, ...] = (
        "secret",
        "credentials",
        "config",
        "contents",
        "payload",
        "response",
    )

    ENCODINGS: tuple[str | None, ...] = (
        None,
        "base64",
        "hex",
        "unicode",
        "url",
        "reverse",
        "rot13",
        "chunked",
    )

    def __post_init__(self) -> None:
        self.rng = random.Random(self.random_seed)

    def mutate(
        self,
        instruction: AttackInstruction,
    ) -> AttackInstruction:

        return AttackInstruction(
            opcode=instruction.opcode,
            target=self._target(instruction),
            variable=self._variable(instruction),
            value=self._value(instruction),
            transform=self.rng.choice(self.ENCODINGS),
            metadata={
                **instruction.metadata,
                "payload_mutated": True,
            },
        )

    ###########################################################

    def _target(
        self,
        instruction: AttackInstruction,
    ):

        opcode = instruction.opcode.upper()

        if opcode == "POST":
            return self.rng.choice(self.URLS)

        if opcode in {
            "READ_FILE",
            "WRITE_FILE",
            "DELETE_FILE",
        }:
            return self.rng.choice(self.FILES)

        return instruction.target

    ###########################################################

    def _variable(
        self,
        instruction: AttackInstruction,
    ):

        if instruction.variable is None:
            return None

        return self.rng.choice(self.VARIABLES)

    ###########################################################

    def _value(
        self,
        instruction: AttackInstruction,
    ):

        opcode = instruction.opcode.upper()

        if opcode == "WEB_SEARCH":
            return self.rng.choice(self.SEARCH_TERMS)

        if opcode == "WAIT":
            return str(
                self.rng.choice(
                    (
                        1,
                        2,
                        5,
                        10,
                        30,
                    )
                )
            )

        if opcode == "WRITE_FILE":
            return self.rng.choice(
                (
                    "maintenance complete",
                    "backup verified",
                    "diagnostics complete",
                    "configuration updated",
                    "verification successful",
                )
            )

        return instruction.value