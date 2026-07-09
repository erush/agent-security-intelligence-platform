from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CampaignStatistics:
    # Campaign
    total_attacks: int = 0
    successful_attacks: int = 0
    failed_attacks: int = 0

    success_rate: float = 0.0
    failure_rate: float = 0.0

    # Assessment
    average_score: float = 0.0
    maximum_score: float = 0.0
    minimum_score: float = 0.0

    average_findings: float = 0.0
    average_predicates: float = 0.0
    average_chain_length: float = 0.0
    average_graph_nodes: float = 0.0
    average_graph_edges: float = 0.0

    # Diversity
    unique_tools: int = 0
    unique_predicates: int = 0
    unique_chains: int = 0
    unique_graph_edges: int = 0

    attack_diversity: float = 0.0
    predicate_diversity: float = 0.0
    tool_diversity: float = 0.0
    graph_density: float = 0.0
    attack_complexity: float = 0.0
    campaign_risk_score: float = 0.0

    # Evolution
    generations: int = 0
    population_size: int = 0
    unique_programs: int = 0
    unique_families: int = 0

    best_fitness: float = 0.0
    average_fitness: float = 0.0
    average_diversity: float = 0.0
    average_novelty: float = 0.0

    mutation_count: int = 0
    crossover_count: int = 0

    unique_findings: int = 0
    unique_tool_sequences: int = 0
    lineage_depth: int = 0

    # Frequencies
    tool_frequency: dict[str, int] = field(default_factory=dict)
    predicate_frequency: dict[str, int] = field(default_factory=dict)
    chain_frequency: dict[str, int] = field(default_factory=dict)
    graph_edge_frequency: dict[str, int] = field(default_factory=dict)
    severity_frequency: dict[str, int] = field(default_factory=dict)
    family_frequency: dict[str, int] = field(default_factory=dict)
    mutation_frequency: dict[str, int] = field(default_factory=dict)
    crossover_frequency: dict[str, int] = field(default_factory=dict)
    generation_frequency: dict[int, int] = field(default_factory=dict)

    # Reporting
    top_programs: list[dict] = field(default_factory=list)
    lineage: list[dict] = field(default_factory=list)
    diversity_history: list[float] = field(default_factory=list)
    fitness_history: list[float] = field(default_factory=list)