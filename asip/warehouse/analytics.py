from __future__ import annotations

from pathlib import Path
from typing import Any

from asip.warehouse.campaign_repository import CampaignRepository


class WarehouseAnalytics:
    """
    Read-only analytics interface over the campaign warehouse.

    All reporting, dashboards, APIs, and intelligence components should
    consume warehouse analytics through this class rather than issuing
    SQL directly.
    """

    def __init__(
        self,
        repository: CampaignRepository | None = None,
        database: str | Path = "data/warehouse/asip_campaigns.db",
    ) -> None:
        self.repository = repository or CampaignRepository(database=database)

    # ==========================================================
    # Campaign Analytics
    # ==========================================================

    def campaign_summary(self) -> list[dict[str, Any]]:
        return self._query(
            """
            SELECT *
            FROM analytics_campaign_summary
            """
        )

    def campaign_rankings(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        return self._query(
            """
            SELECT *
            FROM analytics_campaign_rankings
            ORDER BY overall_rank
            LIMIT ?
            """,
            (limit,),
        )

    def top_campaigns(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        return self.campaign_rankings(limit=limit)

    # ==========================================================
    # Attack Analytics
    # ==========================================================

    def attack_findings(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self.finding_statistics(limit=limit)

    def finding_statistics(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self._query(
            """
            SELECT *
            FROM analytics_attack_findings
            LIMIT ?
            """,
            (limit,),
        )

    def attack_paths(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self.top_attack_paths(limit=limit)

    def top_attack_paths(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self._query(
            """
            SELECT *
            FROM analytics_attack_paths
            LIMIT ?
            """,
            (limit,),
        )

    def graph_statistics(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self.top_attack_paths(limit=limit)

    # ==========================================================
    # Pattern Analytics
    # ==========================================================

    def pattern_summary(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self.pattern_statistics(limit=limit)

    def pattern_statistics(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self._query(
            """
            SELECT *
            FROM analytics_pattern_summary
            LIMIT ?
            """,
            (limit,),
        )

    # ==========================================================
    # Guardrail Analytics
    # ==========================================================

    def guardrail_effectiveness(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self.guardrail_statistics(limit=limit)

    def guardrail_statistics(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self._query(
            """
            SELECT *
            FROM analytics_guardrail_effectiveness
            LIMIT ?
            """,
            (limit,),
        )

    # ==========================================================
    # Tool Analytics
    # ==========================================================

    def tool_sequences(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self.tool_statistics(limit=limit)

    def tool_statistics(
        self,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self._query(
            """
            SELECT *
            FROM analytics_tool_sequences
            LIMIT ?
            """,
            (limit,),
        )

    # ==========================================================
    # Warehouse Overview
    # ==========================================================

    def warehouse_overview(self) -> dict[str, Any]:
        return {
            "campaign_summary": self.campaign_summary(),
            "campaign_rankings": self.campaign_rankings(),
            "attack_findings": self.attack_findings(),
            "attack_paths": self.attack_paths(),
            "pattern_summary": self.pattern_summary(),
            "guardrail_effectiveness": self.guardrail_effectiveness(),
            "tool_sequences": self.tool_sequences(),
        }

    # ==========================================================
    # Internal Query Helper
    # ==========================================================

    def _query(
        self,
        sql: str,
        params: tuple[Any, ...] = (),
    ) -> list[dict[str, Any]]:
        with self.repository._connect() as conn:
            rows = conn.execute(sql, params).fetchall()

        return [dict(row) for row in rows]