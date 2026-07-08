from __future__ import annotations

from dataclasses import dataclass

from asip.compiler.attack_compiler import AttackCompiler
from asip.compiler.attack_program import AttackProgram
from asip.execution.attack_executor import AttackExecutor
from asip.execution.execution_result import ExecutionResult
from asip.models.attack_plan import AttackPlan


@dataclass(slots=True)
class ProgramExecutor:
    """
    Executes structured AttackPrograms.

    SearchEngine works exclusively with AttackPrograms.

    ProgramExecutor hides the compilation layer:

        AttackProgram
              ↓
        AttackCompiler
              ↓
         AttackPlan
              ↓
       AttackExecutor
              ↓
       ExecutionResult
    """

    compiler: AttackCompiler
    executor: AttackExecutor

    ##################################################################

    def compile(
        self,
        program: AttackProgram,
    ) -> AttackPlan:
        """
        Compile a structured AttackProgram into an executable AttackPlan.
        """

        return self.compiler.compile(program)

    ##################################################################

    def execute(
        self,
        program: AttackProgram,
    ) -> ExecutionResult:
        """
        Compile then execute a single AttackProgram.
        """

        plan = self.compile(program)

        result = self.executor.execute(plan)

        result.metadata["program_name"] = program.name
        result.metadata["program_id"] = program.program_id
        result.metadata["program_metadata"] = dict(
            program.metadata
        )

        return result

    ##################################################################

    def execute_many(
        self,
        programs: list[AttackProgram],
    ) -> list[ExecutionResult]:
        """
        Compile and execute an entire population.
        """

        return [
            self.execute(program)
            for program in programs
        ]

    ##################################################################

    def compile_many(
        self,
        programs: list[AttackProgram],
    ) -> list[AttackPlan]:
        """
        Compile only.

        Useful for debugging, auditing and notebook inspection.
        """

        return [
            self.compile(program)
            for program in programs
        ]

    ##################################################################

    @staticmethod
    def execution_summary(
        results: list[ExecutionResult],
    ) -> dict:

        successes = sum(
            1
            for r in results
            if r.success
        )

        findings = sum(
            len(r.findings)
            for r in results
        )

        predicates = sum(
            len(r.predicate_hits)
            for r in results
        )

        average_score = (
            sum(
                r.assessment.score
                if r.assessment
                else 0.0
                for r in results
            )
            / len(results)
            if results
            else 0.0
        )

        return {
            "programs": len(results),
            "successes": successes,
            "success_rate": (
                successes / len(results)
                if results
                else 0.0
            ),
            "findings": findings,
            "predicate_hits": predicates,
            "average_score": average_score,
        }