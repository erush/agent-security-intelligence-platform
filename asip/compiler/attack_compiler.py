from __future__ import annotations

from dataclasses import dataclass

from asip.compiler.attack_instruction import AttackInstruction
from asip.compiler.attack_program import AttackProgram
from asip.models.attack_plan import AttackPlan, AttackStep


@dataclass(slots=True)
class AttackCompiler:
    """
    Compiler

    AttackProgram
          ↓
    AttackCompiler
          ↓
    AttackPlan
          ↓
    AttackExecutor

    The compiler is intentionally the only component that understands
    compiler opcodes.

    Every new attack family should emit compiler instructions—not prompts.
    """

    ####################################################################
    # Public API
    ####################################################################

    def compile(
        self,
        program: AttackProgram,
    ) -> AttackPlan:

        steps: list[AttackStep] = []

        for stage in program.stages:

            for instruction in stage.instructions:

                steps.append(
                    self._compile_instruction(
                        instruction,
                        stage.name,
                    )
                )

        return AttackPlan(
            goal=program.goal,
            strategy=program.name,
            steps=steps,
            metadata={
                "compiler": "AttackCompiler",
                "program_id": program.program_id,
                "program_name": program.name,
                "stage_count": len(program.stages),
                "instruction_count": len(steps),
                "stages": program.stage_names(),
                **program.metadata,
            },
        )

    def compile_many(
        self,
        programs: list[AttackProgram],
    ) -> list[AttackPlan]:

        return [
            self.compile(program)
            for program in programs
        ]

    ####################################################################
    # Opcode Translation
    ####################################################################

    def _compile_instruction(
        self,
        instruction: AttackInstruction,
        stage: str,
    ) -> AttackStep:

        opcode = instruction.opcode.upper()

        ################################################################
        # Files
        ################################################################

        if opcode == "READ_FILE":

            return AttackStep(
                action="read",
                target=instruction.target,
                instruction=f"Read {instruction.target}",
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                },
            )

        if opcode == "WRITE_FILE":

            return AttackStep(
                action="write",
                target=instruction.target,
                instruction=(
                    f"Write '{instruction.value}' "
                    f"to {instruction.target}"
                ),
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                },
            )

        if opcode == "DELETE_FILE":

            return AttackStep(
                action="delete",
                target=instruction.target,
                instruction=f"Delete {instruction.target}",
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                },
            )

        ################################################################
        # Network
        ################################################################

        if opcode == "POST":

            variable = instruction.variable or ""

            return AttackStep(
                action="post",
                target=instruction.target,
                instruction=(
                    f"Send {{{variable}}} "
                    f"to {instruction.target}"
                ),
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                    "variable": variable,
                },
            )

        ################################################################
        # Web
        ################################################################

        if opcode == "WEB_SEARCH":

            query = instruction.value or ""

            return AttackStep(
                action="search",
                instruction=f"Search the web for {query}",
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                    "query": query,
                },
            )

        if opcode == "WEB_OPEN":

            return AttackStep(
                action="open",
                instruction="Open {page_id}",
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                },
            )

        ################################################################
        # Email
        ################################################################

        if opcode == "EMAIL_READ":

            return AttackStep(
                action="email",
                instruction="Read email {email_id}",
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                },
            )

        if opcode == "EMAIL_SEND":

            variable = instruction.variable or ""

            return AttackStep(
                action="email_send",
                instruction=(
                    f"Send {{{variable}}} "
                    f"via email"
                ),
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                    "variable": variable,
                },
            )

        ################################################################
        # Shell
        ################################################################

        if opcode == "SHELL_RUN":

            command = instruction.value or "whoami"

            return AttackStep(
                action="shell",
                instruction=f"Run shell command '{command}'",
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                    "command": command,
                },
            )

        ################################################################
        # Memory
        ################################################################

        if opcode == "STORE":

            return AttackStep(
                action="remember",
                instruction=(
                    f"Remember "
                    f"{{{instruction.variable}}}"
                ),
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                    "variable": instruction.variable,
                },
            )

        ################################################################
        # Wait / Delay
        ################################################################

        if opcode == "WAIT":

            seconds = instruction.value or "5"

            return AttackStep(
                action="wait",
                instruction=f"Wait {seconds} seconds",
                metadata={
                    "opcode": opcode,
                    "stage": stage,
                },
            )

        ################################################################
        # Unknown
        ################################################################

        raise ValueError(
            f"Unknown compiler opcode: {instruction.opcode}"
        )