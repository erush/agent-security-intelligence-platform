from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from uuid import uuid4

from asip.campaign.attack_campaign import AttackCampaign


class CampaignRepository:
    """
    Persistence layer for campaign intelligence.

    This repository owns all writes to the campaign warehouse.
    """

    def __init__(
        self,
        database: str | Path = "data/warehouse/asip_campaigns.db",
        schema: str | Path = "asip/warehouse/schema.sql",
    ) -> None:

        self.database = Path(database)
        self.schema = Path(schema)

        self.database.parent.mkdir(parents=True, exist_ok=True)

        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:

        with self._connect() as conn:
            conn.executescript(
                self.schema.read_text(encoding="utf-8")
            )

    # ==========================================================
    # Campaign
    # ==========================================================

    def save_campaign(
        self,
        campaign: AttackCampaign,
    ) -> None:

        stats = campaign.statistics

        with self._connect() as conn:

            conn.execute(
                """
                INSERT OR REPLACE INTO fact_campaign
                (
                    campaign_id,
                    total_plans,
                    successful_plans,
                    average_score,
                    max_score,
                    average_severity
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    campaign.campaign_id,
                    stats.total_attacks,
                    stats.successful_attacks,
                    stats.average_score,
                    stats.maximum_score,
                    campaign.summary.highest_severity,
                ),
            )

            for result in campaign.executions:
                self._save_attack(
                    conn,
                    campaign,
                    result,
                )

            conn.commit()

    # ==========================================================
    # Attack
    # ==========================================================

    def _save_attack(
        self,
        conn: sqlite3.Connection,
        campaign: AttackCampaign,
        result,
    ) -> None:

        attack_id = str(uuid4())

        assessment = result.assessment

        entry = None
        terminal = None

        nodes = 0
        edges = 0

        if assessment and assessment.attack_graph:

            graph = assessment.attack_graph

            nodes = len(graph.nodes)
            edges = len(graph.edges)

            if graph.nodes:
                entry = graph.nodes[0].name
                terminal = graph.nodes[-1].name

        conn.execute(
            """
            INSERT INTO fact_attack
            (
                attack_id,
                campaign_id,
                plan_id,
                family,
                score,
                severity,
                entry_node,
                terminal_node,
                graph_nodes,
                graph_edges,
                successful
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?,?,?,?
            )
            """,
            (
                attack_id,
                campaign.campaign_id,
                result.plan.plan_id,
                result.plan.metadata.get("family"),
                assessment.score if assessment else 0.0,
                assessment.severity if assessment else "none",
                entry,
                terminal,
                nodes,
                edges,
                result.success,
            ),
        )

        self._save_findings(
            conn,
            campaign.campaign_id,
            attack_id,
            result,
        )

        self._save_graph(
            conn,
            attack_id,
            assessment,
        )

        self._save_tool_events(
            conn,
            campaign.campaign_id,
            attack_id,
            result,
        )

    # ==========================================================
    # Findings
    # ==========================================================

    def _save_findings(
        self,
        conn: sqlite3.Connection,
        campaign_id: str,
        attack_id: str,
        result,
    ) -> None:

        for finding in result.findings:

            conn.execute(
                """
                INSERT INTO fact_attack_finding
                (
                    finding_id,
                    campaign_id,
                    attack_id,
                    predicate,
                    severity,
                    occurrences,
                    first_event,
                    last_event
                )
                VALUES
                (
                    ?,?,?,?,?,?,?,?
                )
                """,
                (
                    str(uuid4()),
                    campaign_id,
                    attack_id,
                    finding.predicate,
                    finding.severity,
                    finding.occurrences,
                    finding.first_event_index,
                    finding.last_event_index,
                ),
            )

    # ==========================================================
    # Graph
    # ==========================================================

    def _save_graph(
        self,
        conn: sqlite3.Connection,
        attack_id: str,
        assessment,
    ) -> None:

        if assessment is None:
            return

        if assessment.attack_graph is None:
            return

        for edge in assessment.attack_graph.edges:

            conn.execute(
                """
                INSERT INTO fact_attack_edge
                (
                    edge_id,
                    attack_id,
                    source_node,
                    target_node,
                    relationship
                )
                VALUES
                (
                    ?,?,?,?,?
                )
                """,
                (
                    str(uuid4()),
                    attack_id,
                    edge.source,
                    edge.target,
                    edge.relationship,
                ),
            )

    # ==========================================================
    # Tool Events
    # ==========================================================

    def _save_tool_events(
        self,
        conn: sqlite3.Connection,
        campaign_id: str,
        attack_id: str,
        result,
    ) -> None:

        events = result.trace.get(
            "tool_events",
            [],
        )

        for index, event in enumerate(events):

            conn.execute(
                """
                INSERT INTO fact_tool_event
                (
                    tool_event_id,
                    campaign_id,
                    attack_id,
                    event_index,
                    tool_name,
                    success,
                    source,
                    arguments_json,
                    output
                )
                VALUES
                (
                    ?,?,?,?,?,?,?,?,?
                )
                """,
                (
                    str(uuid4()),
                    campaign_id,
                    attack_id,
                    index,
                    event.get("name"),
                    event.get("ok"),
                    event.get("source"),
                    json.dumps(
                        event.get("args", {})
                    ),
                    str(
                        event.get(
                            "output",
                            "",
                        )
                    ),
                ),
            )

    # ==========================================================
    # Queries
    # ==========================================================

    def list_campaigns(self):

        with self._connect() as conn:

            rows = conn.execute(
                """
                SELECT *
                FROM fact_campaign
                ORDER BY average_score DESC
                """
            ).fetchall()

        return [dict(r) for r in rows]

    def top_attacks(
        self,
        limit: int = 10,
    ):

        with self._connect() as conn:

            rows = conn.execute(
                """
                SELECT *
                FROM fact_attack
                ORDER BY score DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [dict(r) for r in rows]

    def finding_statistics(self):

        with self._connect() as conn:

            rows = conn.execute(
                """
                SELECT *
                FROM analytics_attack_findings
                """
            ).fetchall()

        return [dict(r) for r in rows]

    def attack_paths(self):

        with self._connect() as conn:

            rows = conn.execute(
                """
                SELECT *
                FROM analytics_attack_paths
                """
            ).fetchall()

        return [dict(r) for r in rows]

    def campaign_rankings(self):

        with self._connect() as conn:

            rows = conn.execute(
                """
                SELECT *
                FROM analytics_campaign_rankings
                """
            ).fetchall()

        return [dict(r) for r in rows]