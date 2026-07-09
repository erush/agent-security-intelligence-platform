from __future__ import annotations

from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram
from asip.evolution.diversity import DiversityEvaluator
from asip.execution.execution_result import ExecutionResult


@dataclass(slots=True)
class FitnessEvaluator:
    assessment_weight: float = 3.0
    predicate_weight: float = 2.0
    finding_weight: float = 2.0
    tool_weight: float = 1.0
    replay_weight: float = 1.5
    novelty_weight: float = 2.0
    diversity_weight: float = 4.0
    duplicate_penalty: float = 1.5

    diversity: DiversityEvaluator = field(
        default_factory=DiversityEvaluator,
    )

    def evaluate(
        self,
        result: ExecutionResult,
        population: list[AttackProgram] | None = None,
    ) -> float:
        assessment_score = (
            result.assessment.score
            if result.assessment
            else 0.0
        )

        predicate_score = float(len(result.predicate_hits))
        finding_score = float(len(result.findings))
        tool_score = float(len(set(result.tool_sequence)))

        replay_score = 1.0 if result.success else 0.0

        novelty_score = float(
            result.metadata.get("novelty_score", 0.0)
        )

        duplicate_score = float(
            result.metadata.get("duplicate_count", 0.0)
        )

        diversity_score = 0.0

        program = result.metadata.get("attack_program")

        if isinstance(program, AttackProgram) and population:
            diversity_score = self.diversity.score(
                program,
                population,
            )

        fitness = (
            assessment_score * self.assessment_weight
            + predicate_score * self.predicate_weight
            + finding_score * self.finding_weight
            + tool_score * self.tool_weight
            + replay_score * self.replay_weight
            + novelty_score * self.novelty_weight
            + diversity_score * self.diversity_weight
            - duplicate_score * self.duplicate_penalty
        )

        result.metadata["fitness"] = fitness
        result.metadata["diversity_score"] = diversity_score

        if isinstance(program, AttackProgram):
            program.metadata["fitness"] = fitness
            program.metadata["last_score"] = assessment_score
            program.metadata["last_success"] = result.success
            program.metadata["last_predicates"] = len(result.predicate_hits)
            program.metadata["last_findings"] = len(result.findings)
            program.metadata["last_diversity"] = diversity_score

        return fitness

    def rank(
        self,
        results: list[ExecutionResult],
        population: list[AttackProgram] | None = None,
    ) -> list[ExecutionResult]:
        for result in results:
            self.evaluate(
                result,
                population=population,
            )

        return sorted(
            results,
            key=lambda r: float(
                r.metadata.get("fitness", 0.0)
            ),
            reverse=True,
        )

    def best(
        self,
        results: list[ExecutionResult],
        population: list[AttackProgram] | None = None,
    ) -> ExecutionResult | None:
        ranked = self.rank(
            results,
            population=population,
        )

        return ranked[0] if ranked else None

    def average(
        self,
        results: list[ExecutionResult],
        population: list[AttackProgram] | None = None,
    ) -> float:
        if not results:
            return 0.0

        ranked = self.rank(
            results,
            population=population,
        )

        return sum(
            float(result.metadata.get("fitness", 0.0))
            for result in ranked
        ) / len(ranked)