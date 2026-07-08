from __future__ import annotations

from asip.warehouse.campaign_repository import CampaignRepository


def build_attack_paths(
    repository: CampaignRepository,
) -> None:
    """
    Materialize attack graph analytics.

    Aggregates attack graph edges across every executed attack to
    identify the most common transitions between attack findings.
    """

    with repository._connect() as conn:

        conn.execute(
            """
            DROP TABLE IF EXISTS analytics_attack_paths
            """
        )

        conn.execute(
            """
            CREATE TABLE analytics_attack_paths AS

            SELECT

                source_node,

                target_node,

                relationship,

                COUNT(*) AS frequency,

                COUNT(DISTINCT attack_id) AS attacks

            FROM fact_attack_edge

            GROUP BY

                source_node,
                target_node,
                relationship

            ORDER BY

                frequency DESC,
                attacks DESC,
                source_node,
                target_node
            """
        )

        conn.commit()