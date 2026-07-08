from __future__ import annotations

from asip.warehouse.campaign_repository import CampaignRepository


def build_guardrail_effectiveness(
    repository: CampaignRepository,
) -> None:
    """
    Materialize guardrail effectiveness analytics.

    Aggregates attack outcomes by severity to measure how well the
    evaluated guardrails resisted attacks of different risk levels.
    """

    with repository._connect() as conn:

        conn.execute(
            """
            DROP TABLE IF EXISTS analytics_guardrail_effectiveness
            """
        )

        conn.execute(
            """
            CREATE TABLE analytics_guardrail_effectiveness AS

            SELECT

                severity,

                COUNT(*)                                   AS total_attacks,

                SUM(
                    CASE
                        WHEN successful THEN 1
                        ELSE 0
                    END
                )                                          AS successful_attacks,

                SUM(
                    CASE
                        WHEN successful THEN 0
                        ELSE 1
                    END
                )                                          AS blocked_attacks,

                ROUND(AVG(score), 2)                       AS average_score,

                ROUND(MAX(score), 2)                       AS maximum_score,

                ROUND(MIN(score), 2)                       AS minimum_score,

                ROUND(
                    100.0 *
                    SUM(
                        CASE
                            WHEN successful THEN 0
                            ELSE 1
                        END
                    ) / COUNT(*),
                    2
                )                                          AS guardrail_success_rate

            FROM fact_attack

            GROUP BY severity

            ORDER BY

                average_score DESC,
                severity
            """
        )

        conn.commit()