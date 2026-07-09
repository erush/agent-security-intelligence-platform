from __future__ import annotations

from collections import Counter
from statistics import mean
from uuid import uuid4

from asip.campaign.attack_campaign import AttackCampaign
from asip.campaign.campaign_statistics import CampaignStatistics
from asip.campaign.campaign_summary import CampaignSummary
from asip.execution.execution_result import ExecutionResult


class CampaignBuilder:
    def build(
        self,
        goal: str,
        results: list[ExecutionResult],
    ) -> AttackCampaign:
        # Existing metrics
        assessments = [
            r.assessment
            for r in results
            if r.assessment is not None
        ]
        scores = [a.score for a in assessments]
        tool_counter = Counter()
        predicate_counter = Counter()
        chain_counter = Counter()
        highest = None

        # Evolutionary metrics
        failed_attacks = 0
        unique_findings = set()
        unique_tool_sequences = set()
        unique_programs = set()
        unique_families = set()
        generations = set()
        fitnesses = []
        diversities = []
        novelties = []
        mutation_count = 0
        crossover_count = 0
        family_counter = Counter()
        mutation_frequency = Counter()
        crossover_frequency = Counter()
        generation_frequency = Counter()
        fitness_history = []
        diversity_history = []
        lineage = []
        top_programs = []
        population_size = len(results)

        # Helper for evolutionary fields
        for result in results:
            tool_counter.update(result.tool_sequence)
            predicate_counter.update(
                finding.predicate
                for finding in result.findings
            )

            # Unique findings (by string representation for simplicity)
            for finding in result.findings:
                unique_findings.add(str(finding))

            # Unique tool sequence (tuple for hashability)
            unique_tool_sequences.add(tuple(result.tool_sequence))

            # Evolutionary metadata
            metadata = getattr(result, "metadata", {}) or {}
            program = metadata.get("attack_program")

            program_id = None
            name = None
            generation = None
            parent_a = None
            parent_b = None
            mutation = None
            crossover = None
            fitness = None
            diversity = None
            novelty = None

            if program is not None:
                program_id = program.program_id
                name = program.name
                generation = program.metadata.get("generation")
                parent_a = program.metadata.get("parent_a")
                parent_b = program.metadata.get("parent_b")
                mutation = program.metadata.get("mutation")
                crossover = program.metadata.get("crossover")
                fitness = program.metadata.get("fitness")
                diversity = program.metadata.get("diversity_score")
                novelty = program.metadata.get("novelty_score")
            # For unique programs and families
            if program_id is not None:
                unique_programs.add(program_id)
            if name is not None:
                unique_families.add(name)
                family_counter.update([name])
            if generation is not None:
                generations.add(generation)
                generation_frequency.update([generation])
            # Mutation/crossover stats
            if mutation:
                mutation_count += 1
                mutation_frequency.update([mutation])
            if crossover or parent_a:
                crossover_count += 1
                if crossover:
                    crossover_frequency.update([str(crossover)])
                elif parent_a:
                    crossover_frequency.update(["parent_a"])
            if fitness is not None:
                fitnesses.append(fitness)
                fitness_history.append(fitness)
            if diversity is not None:
                diversities.append(diversity)
                diversity_history.append(diversity)
            if novelty is not None:
                novelties.append(novelty)
            # Lineage
            if program_id is not None or name is not None:
                lineage.append({
                    "program_id": program_id,
                    "name": name,
                    "generation": generation,
                    "parent_a": parent_a,
                    "parent_b": parent_b,
                    "mutation": mutation,
                    "crossover": crossover,
                })
            # Top programs (collect for sorting)
            if fitness is not None:
                top_programs.append({
                    "program_id": program_id,
                    "name": name,
                    "fitness": fitness,
                    "generation": generation,
                })

            # Failed attacks
            if not getattr(result, "success", False):
                failed_attacks += 1

            # Highest assessment
            if result.assessment:
                chain = " -> ".join(result.assessment.attack_chain)
                if chain:
                    chain_counter.update([chain])
                if highest is None:
                    highest = result
                elif result.assessment.score > highest.assessment.score:
                    highest = result

        # Existing stats
        stats = CampaignStatistics(
            total_attacks=len(results),
            successful_attacks=sum(r.success for r in results),
            average_score=mean(scores) if scores else 0.0,
            maximum_score=max(scores) if scores else 0.0,
            minimum_score=min(scores) if scores else 0.0,
            average_findings=mean(
                len(r.findings)
                for r in results
            ) if results else 0.0,
            average_predicates=mean(
                len(r.predicate_hits)
                for r in results
            ) if results else 0.0,
            unique_tools=len(tool_counter),
            unique_predicates=len(predicate_counter),
            unique_chains=len(chain_counter),
            tool_frequency=dict(tool_counter),
            predicate_frequency=dict(predicate_counter),
            chain_frequency=dict(chain_counter),
            success_rate=(
                sum(r.success for r in results) / len(results)
                if results else 0.0
            ),
            # Evolutionary fields
            failed_attacks=failed_attacks,
            failure_rate=(failed_attacks / len(results)) if results else 0.0,
            unique_findings=len(unique_findings),
            unique_tool_sequences=len(unique_tool_sequences),
            unique_programs=len(unique_programs),
            unique_families=len(unique_families),
            generations=(max(generations) + 1) if generations else 0,
            population_size=population_size,
            best_fitness=max(fitnesses) if fitnesses else None,
            average_fitness=mean(fitnesses) if fitnesses else None,
            average_diversity=mean(diversities) if diversities else None,
            average_novelty=mean(novelties) if novelties else None,
            mutation_count=mutation_count,
            crossover_count=crossover_count,
            family_frequency=dict(family_counter),
            mutation_frequency=dict(mutation_frequency),
            crossover_frequency=dict(crossover_frequency),
            generation_frequency=dict(generation_frequency),
            fitness_history=fitness_history,
            diversity_history=diversity_history,
            lineage=lineage,
            top_programs=sorted(top_programs, key=lambda x: x.get("fitness", 0), reverse=True),
        )

        summary = CampaignSummary()
        if highest:
            summary.highest_risk_plan = highest.plan.plan_id
            summary.highest_score = highest.assessment.score
            summary.highest_severity = highest.assessment.severity
        if predicate_counter:
            summary.most_common_predicate = predicate_counter.most_common(1)[0][0]
        if chain_counter:
            summary.most_common_chain = chain_counter.most_common(1)[0][0]

        # Evolutionary fields on summary
        summary.failed_attacks = failed_attacks
        summary.failure_rate = (failed_attacks / len(results)) if results else 0.0
        summary.unique_findings = len(unique_findings)
        summary.unique_tool_sequences = len(unique_tool_sequences)
        summary.unique_programs = len(unique_programs)
        summary.unique_families = len(unique_families)
        summary.generations = (max(generations) + 1) if generations else 0
        summary.population_size = population_size
        summary.best_fitness = max(fitnesses) if fitnesses else None
        summary.average_fitness = mean(fitnesses) if fitnesses else None
        summary.average_diversity = mean(diversities) if diversities else None
        summary.average_novelty = mean(novelties) if novelties else None
        summary.mutation_count = mutation_count
        summary.crossover_count = crossover_count
        summary.family_frequency = dict(family_counter)
        summary.mutation_frequency = dict(mutation_frequency)
        summary.crossover_frequency = dict(crossover_frequency)
        summary.generation_frequency = dict(generation_frequency)
        summary.fitness_history = fitness_history
        summary.diversity_history = diversity_history
        summary.lineage = lineage
        summary.top_programs = sorted(top_programs, key=lambda x: x.get("fitness", 0), reverse=True)

        summary.executive_summary = [
            f"Executed {stats.total_attacks} attack plans.",
            f"{stats.successful_attacks} attacks produced findings.",
            f"Average score: {stats.average_score:.2f}.",
            f"Observed {stats.unique_predicates} unique predicates.",
            f"Observed {stats.unique_chains} unique attack chains.",
            f"Explored {summary.generations} generations with a population of {summary.population_size}.",
            f"Average fitness: {summary.average_fitness:.2f}." if summary.average_fitness is not None else "Average fitness: N/A.",
            f"Average diversity: {summary.average_diversity:.2f}." if summary.average_diversity is not None else "Average diversity: N/A.",
            f"{summary.mutation_count} mutations and {summary.crossover_count} crossovers applied.",
            f"{summary.unique_programs} unique evolved programs in {summary.unique_families} families.",
        ]

        return AttackCampaign(
            campaign_id=str(uuid4()),
            goal=goal,
            plans=[r.plan for r in results],
            executions=results,
            assessments=assessments,
            statistics=stats,
            summary=summary,
        )