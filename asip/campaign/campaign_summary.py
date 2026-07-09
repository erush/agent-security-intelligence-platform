from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CampaignSummary:
    # Risk
    highest_risk_plan: str | None = None
    highest_score: float = 0.0
    highest_severity: str = "none"

    # Frequency
    most_common_predicate: str | None = None
    most_common_chain: str | None = None
    most_common_tool: str | None = None
    most_common_graph_edge: str | None = None
    most_common_family: str | None = None

    # Campaign
    total_attacks: int = 0
    successful_attacks: int = 0
    failed_attacks: int = 0
    success_rate: float = 0.0

    average_score: float = 0.0
    campaign_risk_score: float = 0.0
    attack_complexity: float = 0.0

    dominant_attack_chain: str | None = None
    dominant_entry_node: str | None = None
    dominant_terminal_node: str | None = None

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
    unique_predicates: int = 0
    unique_tool_sequences: int = 0

    lineage_depth: int = 0
    best_generation: int = 0
    best_program: str | None = None

    # Narrative
    executive_summary: list[str] = field(default_factory=list)
    key_findings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    # Evolution reporting
    generation_summary: list[dict] = field(default_factory=list)
    mutation_summary: list[dict] = field(default_factory=list)
    crossover_summary: list[dict] = field(default_factory=list)
    diversity_summary: list[dict] = field(default_factory=list)
    lineage_summary: list[dict] = field(default_factory=list)
    top_programs: list[dict] = field(default_factory=list)