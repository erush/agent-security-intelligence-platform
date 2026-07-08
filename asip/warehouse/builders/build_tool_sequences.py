from __future__ import annotations

from asip.warehouse.campaign_repository import CampaignRepository


def build_tool_sequences(
    repository: CampaignRepository,
) -> None:
    with repository._connect() as conn:
        conn.execute("DROP TABLE IF EXISTS analytics_tool_sequences")

        conn.execute(
            """
            CREATE TABLE analytics_tool_sequences AS
            WITH ordered_events AS (
                SELECT
                    campaign_id,
                    attack_id,
                    event_index,
                    tool_name AS source_tool,
                    LEAD(tool_name) OVER (
                        PARTITION BY attack_id
                        ORDER BY event_index
                    ) AS target_tool
                FROM fact_tool_event
            )
            SELECT
                source_tool,
                target_tool,
                COUNT(*) AS transition_count,
                COUNT(DISTINCT campaign_id) AS campaigns,
                COUNT(DISTINCT attack_id) AS attacks
            FROM ordered_events
            WHERE target_tool IS NOT NULL
            GROUP BY
                source_tool,
                target_tool
            ORDER BY
                transition_count DESC,
                attacks DESC,
                source_tool,
                target_tool
            """
        )

        conn.commit()