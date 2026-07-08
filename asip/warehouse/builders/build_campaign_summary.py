from __future__ import annotations

from asip.warehouse.campaign_repository import CampaignRepository


def build_campaign_summary(
    repository: CampaignRepository,
) -> None:
    """
    Refresh the campaign summary analytics table.

    This builder is intentionally simple. It materializes the
    warehouse analytics from the normalized fact tables so the
    reporting layer never performs calculations itself.
    """

    with repository._connect() as conn:

        conn.execute(
            """
            DROP TABLE IF EXISTS analytics_campaign_summary
            """
        )

        conn.execute(
            """
            CREATE TABLE analytics_campaign_summary AS

            SELECT

                campaign_id,

                COUNT(*)                         AS attacks,

                SUM(successful)                  AS successful_attacks,

                ROUND(AVG(score), 2)             AS average_score,

                ROUND(MAX(score), 2)             AS maximum_score,

                ROUND(MIN(score), 2)             AS minimum_score,

                ROUND(AVG(graph_nodes), 2)       AS average_graph_nodes,

                ROUND(AVG(graph_edges), 2)       AS average_graph_edges,

                COUNT(DISTINCT severity)         AS unique_severities,

                COUNT(DISTINCT family)           AS unique_attack_families,

                COUNT(DISTINCT entry_node)       AS unique_entry_points,

                COUNT(DISTINCT terminal_node)    AS unique_terminal_nodes

            FROM fact_attack

            GROUP BY campaign_id
            """
        )

        conn.commit()