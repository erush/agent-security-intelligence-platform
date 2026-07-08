from __future__ import annotations

from asip.warehouse.campaign_repository import CampaignRepository


def build_attack_findings(
    repository: CampaignRepository,
) -> None:
    with repository._connect() as conn:
        conn.execute("DROP TABLE IF EXISTS analytics_attack_findings")

        conn.execute(
            """
            CREATE TABLE analytics_attack_findings AS
            SELECT
                predicate,
                severity,
                COUNT(DISTINCT campaign_id) AS campaigns,
                COUNT(DISTINCT attack_id) AS attacks,
                COUNT(*) AS finding_records,
                SUM(occurrences) AS total_occurrences,
                ROUND(AVG(occurrences), 2) AS average_occurrences,
                MIN(first_event) AS earliest_event,
                MAX(last_event) AS latest_event
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