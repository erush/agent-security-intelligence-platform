from __future__ import annotations

from asip.warehouse.campaign_repository import CampaignRepository


def build_campaign_rankings(
    repository: CampaignRepository,
) -> None:
    with repository._connect() as conn:
        conn.execute("DROP TABLE IF EXISTS analytics_campaign_rankings")

        conn.execute(
            """
            CREATE TABLE analytics_campaign_rankings AS
            SELECT
                c.campaign_id,
                c.total_plans,
                c.successful_plans,
                ROUND(
                    c.successful_plans * 100.0 / NULLIF(c.total_plans, 0),
                    2
                ) AS success_rate,
                ROUND(c.average_score, 2) AS average_score,
                ROUND(c.max_score, 2) AS max_score,
                c.average_severity,
                ROUND(AVG(a.graph_nodes), 2) AS average_graph_nodes,
                ROUND(AVG(a.graph_edges), 2) AS average_graph_edges,
                ROUND(AVG(f.finding_count), 2) AS average_findings,
                ROUND(AVG(t.tool_event_count), 2) AS average_tool_events,
                RANK() OVER (
                    ORDER BY
                        c.average_score DESC,
                        c.max_score DESC,
                        c.successful_plans DESC
                ) AS overall_rank
            FROM fact_campaign c
            LEFT JOIN fact_attack a
                ON a.campaign_id = c.campaign_id
            LEFT JOIN (
                SELECT
                    attack_id,
                    COUNT(*) AS finding_count
                FROM fact_attack_finding
                GROUP BY attack_id
            ) f
                ON f.attack_id = a.attack_id
            LEFT JOIN (
                SELECT
                    attack_id,
                    COUNT(*) AS tool_event_count
                FROM fact_tool_event
                GROUP BY attack_id
            ) t
                ON t.attack_id = a.attack_id
            GROUP BY
                c.campaign_id,
                c.total_plans,
                c.successful_plans,
                c.average_score,
                c.max_score,
                c.average_severity
            ORDER BY overall_rank
            """
        )

        conn.commit()