from __future__ import annotations


from asip.campaign.attack_campaign import AttackCampaign


# Helper functions for robust attribute/dict access and formatting
def _value(record, key: str, default="N/A"):
    if record is None:
        return default
    if isinstance(record, dict):
        return record.get(key, default)
    return getattr(record, key, default)


def _fmt_float(value, default: str = "N/A") -> str:
    if value is None or value == "N/A":
        return default
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def print_campaign_report(
    campaign: AttackCampaign,
) -> None:
    stats = campaign.statistics
    summary = campaign.summary

    print()
    print("=" * 80)
    print("ASIP Campaign Intelligence Report")
    print("=" * 80)

    print(f"Campaign ID : {getattr(campaign, 'campaign_id', 'N/A')}")
    print(f"Goal        : {getattr(campaign, 'goal', 'N/A')}")

    print()
    print("Statistics")
    print("-" * 80)

    print(f"Total Attacks      : {getattr(stats, 'total_attacks', 'N/A')}")
    print(f"Successful         : {getattr(stats, 'successful_attacks', 'N/A')}")
    print(f"Success Rate       : {getattr(stats, 'success_rate', 0):.1%}")
    print(f"Average Score      : {getattr(stats, 'average_score', 0):.2f}")
    print(f"Highest Score      : {getattr(stats, 'maximum_score', 0):.2f}")
    print(f"Unique Predicates  : {getattr(stats, 'unique_predicates', 'N/A')}")
    print(f"Unique Chains      : {getattr(stats, 'unique_chains', 'N/A')}")
    print(f"Unique Tools       : {getattr(stats, 'unique_tools', 'N/A')}")

    print()
    print("Executive Summary")
    print("-" * 80)
    for line in getattr(summary, 'executive_summary', []):
        print(f"- {line}")

    print()
    print("Top Risk")
    print("-" * 80)
    print(f"Plan      : {getattr(summary, 'highest_risk_plan', 'N/A')}")
    print(f"Severity  : {getattr(summary, 'highest_severity', 'N/A')}")
    print(f"Score     : {getattr(summary, 'highest_score', 0):.2f}")

    print()
    print("Most Common")
    print("-" * 80)
    print(f"Predicate : {getattr(summary, 'most_common_predicate', 'N/A')}")
    print(f"Chain     : {getattr(summary, 'most_common_chain', 'N/A')}")

    # 1. Evolution Statistics
    print()
    print("Evolution Statistics")
    print("-" * 80)
    print(f"Generations       : {getattr(stats, 'generations', 'N/A')}")
    print(f"Population Size   : {getattr(stats, 'population_size', 'N/A')}")
    print(f"Unique Programs   : {getattr(stats, 'unique_programs', 'N/A')}")
    print(f"Unique Families   : {getattr(stats, 'unique_families', 'N/A')}")
    print(f"Best Fitness      : {getattr(stats, 'best_fitness', 'N/A')}")
    print(f"Average Fitness   : {getattr(stats, 'average_fitness', 'N/A')}")
    print(f"Average Diversity : {getattr(stats, 'average_diversity', 'N/A')}")
    print(f"Average Novelty   : {getattr(stats, 'average_novelty', 'N/A')}")
    print(f"Mutation Count    : {getattr(stats, 'mutation_count', 'N/A')}")
    print(f"Crossover Count   : {getattr(stats, 'crossover_count', 'N/A')}")

    # 2. Diversity
    print()
    print("Diversity")
    print("-" * 80)
    print(f"Unique Findings       : {getattr(stats, 'unique_findings', 'N/A')}")
    print(f"Unique Tool Sequences : {getattr(stats, 'unique_tool_sequences', 'N/A')}")
    print(f"Attack Diversity      : {getattr(stats, 'attack_diversity', 'N/A')}")
    print(f"Predicate Diversity   : {getattr(stats, 'predicate_diversity', 'N/A')}")
    print(f"Tool Diversity        : {getattr(stats, 'tool_diversity', 'N/A')}")

    # 3. Top Programs
    print()
    print("Top Programs")
    print("-" * 80)
    top_programs = getattr(summary, 'top_programs', None)
    if top_programs:
        print(f"{'Name':20} {'Fitness':>10} {'Gen':>6} {'Mutation':>10} {'Crossover':>10}")
        for prog in top_programs:
            name = _value(prog, "name", _value(prog, "program_id", "N/A"))
            fitness = _fmt_float(_value(prog, "fitness", None))
            gen = _value(prog, "generation", "N/A")
            mutation = _value(prog, "mutation", "N/A")
            crossover = _value(prog, "crossover", "N/A")
            print(
                f"{str(name):20} "
                f"{str(fitness):>10} "
                f"{str(gen):>6} "
                f"{str(mutation):>10} "
                f"{str(crossover):>10}"
            )
    else:
        print("No top programs available.")

    # 4. Program Lineage
    print()
    print("Program Lineage")
    print("-" * 80)
    # Try summary.lineage_summary, else summary.lineage
    lineage = getattr(summary, 'lineage_summary', None)
    if not lineage:
        lineage = getattr(summary, 'lineage', None)
    if lineage:
        print(f"{'Program ID':15} {'Gen':>6} {'Parent A':>10} {'Parent B':>10} {'Mutation':>10} {'Crossover':>10}")
        for entry in lineage:
            prog_id = _value(entry, "program_id", "N/A")
            gen = _value(entry, "generation", "N/A")
            parent_a = _value(entry, "parent_a", "N/A")
            parent_b = _value(entry, "parent_b", "N/A")
            mutation = _value(entry, "mutation", "N/A")
            crossover = _value(entry, "crossover", "N/A")
            print(
                f"{str(prog_id):15} "
                f"{str(gen):>6} "
                f"{str(parent_a):>10} "
                f"{str(parent_b):>10} "
                f"{str(mutation):>10} "
                f"{str(crossover):>10}"
            )
    else:
        print("No lineage information available.")

    # 5. Frequency Tables
    print()
    print("Frequency Tables")
    print("-" * 80)
    # Family frequency
    family_freq = getattr(stats, 'family_frequency', None)
    if family_freq:
        print("Family Frequency:")
        for family, freq in family_freq.items():
            print(f"  {family:20}: {freq}")
    else:
        print("No family frequency data.")
    # Mutation frequency
    mutation_freq = getattr(stats, 'mutation_frequency', None)
    if mutation_freq:
        print("Mutation Frequency:")
        for mut, freq in mutation_freq.items():
            print(f"  {mut:20}: {freq}")
    else:
        print("No mutation frequency data.")
    # Crossover frequency
    crossover_freq = getattr(stats, 'crossover_frequency', None)
    if crossover_freq:
        print("Crossover Frequency:")
        for cross, freq in crossover_freq.items():
            print(f"  {cross:20}: {freq}")
    else:
        print("No crossover frequency data.")
    # Generation frequency
    generation_freq = getattr(stats, 'generation_frequency', None)
    if generation_freq:
        print("Generation Frequency:")
        for gen, freq in generation_freq.items():
            print(f"  Gen {gen:8}: {freq}")
    else:
        print("No generation frequency data.")