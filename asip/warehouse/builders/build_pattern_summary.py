from __future__ import annotations

from asip.warehouse.campaign_repository import CampaignRepository


def build_pattern_summary(
    repository: CampaignRepository,
) -> None:
    """
    Materialize attack pattern analytics.

    Produces one warehouse table containing aggregated
    predicate/finding frequencies across every campaign.
    """

    with repository._connect() as conn:

        conn.execute(
            """
            DROP TABLE IF EXISTS analytics_pattern_summary
            """
        )

        conn.execute(
            """
            CREATE TABLE analytics_pattern_summary AS

            SELECT

                predicate,

                severity,

                COUNT(*)                         AS finding_records,

                SUM(occurrences)                 AS total_occurrences,

                COUNT(DISTINCT campaign_id)      AS campaigns,

                COUNT(DISTINCT attack_id)        AS attacks,

                ROUND(AVG(occurrences), 2)       AS average_occurrences,

                MIN(first_event)                 AS earliest_event,

                MAX(last_event)                  AS latest_event

            FROM fact_attack_finding

            GROUP BY

                predicate,
                severity

            ORDER BY

                total_occurrences DESC,
                attacks DESC,
                predicate
            """
        )

        conn.commit()