from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class WarehouseMetadata:
    """
    Metadata describing the current warehouse.
    """

    warehouse_name: str = "ASIP Campaign Intelligence Warehouse"

    warehouse_version: str = "1.0.0"

    schema_version: str = "1.0.0"

    analytics_version: str = "1.0.0"

    refreshed_at: datetime = field(default_factory=datetime.utcnow)

    campaign_count: int = 0

    attack_count: int = 0

    finding_count: int = 0

    tool_event_count: int = 0

    graph_edge_count: int = 0

    analytics_tables: tuple[str, ...] = (
        "analytics_campaign_summary",
        "analytics_campaign_rankings",
        "analytics_attack_findings",
        "analytics_pattern_summary",
        "analytics_attack_paths",
        "analytics_tool_sequences",
        "analytics_guardrail_effectiveness",
    )

    fact_tables: tuple[str, ...] = (
        "fact_campaign",
        "fact_attack",
        "fact_attack_finding",
        "fact_attack_edge",
        "fact_tool_event",
    )

    dimension_tables: tuple[str, ...] = (
        "dim_attack_pattern",
    )