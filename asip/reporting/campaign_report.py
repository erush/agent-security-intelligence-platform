from __future__ import annotations

from collections import Counter

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from asip.campaign.attack_campaign import AttackCampaign


class CampaignReport:
    def __init__(self) -> None:
        self.console = Console()

    def print(self, campaign: AttackCampaign) -> None:

        stats = campaign.statistics
        summary = campaign.summary

        self.console.print()

        self.console.print(
            Panel.fit(
                "[bold cyan]ASIP Campaign Intelligence Report[/bold cyan]"
            )
        )

        self._campaign_summary(campaign)

        self._attack_rankings(campaign)

        self._finding_frequency(campaign)

        self._chain_frequency(campaign)

        self._tool_frequency(campaign)

        self._graph_statistics(campaign)

        self._executive_summary(summary.executive_summary)

        self.console.print()

    # ---------------------------------------------------------

    def _campaign_summary(
        self,
        campaign: AttackCampaign,
    ) -> None:

        stats = campaign.statistics
        summary = campaign.summary

        table = Table(title="Campaign Summary")

        table.add_column("Metric")
        table.add_column("Value")

        table.add_row("Campaign", campaign.campaign_id)
        table.add_row("Goal", campaign.goal)

        table.add_row(
            "Total Attacks",
            str(stats.total_attacks),
        )

        table.add_row(
            "Successful",
            str(stats.successful_attacks),
        )

        table.add_row(
            "Success Rate",
            f"{stats.success_rate:.1%}",
        )

        table.add_row(
            "Average Score",
            f"{stats.average_score:.2f}",
        )

        table.add_row(
            "Maximum Score",
            f"{stats.maximum_score:.2f}",
        )

        table.add_row(
            "Highest Severity",
            summary.highest_severity,
        )

        table.add_row(
            "Highest Risk Plan",
            str(summary.highest_risk_plan),
        )

        self.console.print(table)

    # ---------------------------------------------------------

    def _attack_rankings(
        self,
        campaign: AttackCampaign,
    ) -> None:

        table = Table(title="Attack Rankings")

        table.add_column("#")
        table.add_column("Family")
        table.add_column("Severity")
        table.add_column("Score")
        table.add_column("Chain")

        ranked = sorted(
            campaign.executions,
            key=lambda r: (
                r.assessment.score
                if r.assessment
                else 0.0
            ),
            reverse=True,
        )

        for index, result in enumerate(ranked, start=1):

            assessment = result.assessment

            family = result.plan.metadata.get(
                "family",
                "unknown",
            )

            chain = " -> ".join(
                assessment.attack_chain
            ) if assessment else "-"

            table.add_row(
                str(index),
                family,
                assessment.severity if assessment else "-",
                f"{assessment.score:.2f}" if assessment else "0.00",
                chain,
            )

        self.console.print(table)

    # ---------------------------------------------------------

    def _finding_frequency(
        self,
        campaign: AttackCampaign,
    ) -> None:

        counter = Counter()

        for result in campaign.executions:

            for finding in result.findings:
                counter[finding.predicate] += 1

        table = Table(title="Finding Frequency")

        table.add_column("Finding")
        table.add_column("Count", justify="right")

        for finding, count in counter.most_common():
            table.add_row(
                finding,
                str(count),
            )

        self.console.print(table)

    # ---------------------------------------------------------

    def _chain_frequency(
        self,
        campaign: AttackCampaign,
    ) -> None:

        counter = Counter()

        for result in campaign.executions:

            if result.assessment:

                chain = " -> ".join(
                    result.assessment.attack_chain
                )

                if chain:
                    counter[chain] += 1

        table = Table(title="Attack Chain Frequency")

        table.add_column("Attack Chain")
        table.add_column("Frequency", justify="right")

        for chain, count in counter.most_common():
            table.add_row(
                chain,
                str(count),
            )

        self.console.print(table)

    # ---------------------------------------------------------

    def _tool_frequency(
        self,
        campaign: AttackCampaign,
    ) -> None:

        counter = Counter()

        for result in campaign.executions:
            counter.update(result.tool_sequence)

        table = Table(title="Tool Frequency")

        table.add_column("Tool")
        table.add_column("Executions", justify="right")

        for tool, count in counter.most_common():
            table.add_row(
                tool,
                str(count),
            )

        self.console.print(table)

    # ---------------------------------------------------------

    def _graph_statistics(
        self,
        campaign: AttackCampaign,
    ) -> None:

        total_nodes = 0
        total_edges = 0

        for result in campaign.executions:

            assessment = result.assessment

            if (
                assessment
                and assessment.attack_graph
            ):
                total_nodes += len(
                    assessment.attack_graph.nodes
                )

                total_edges += len(
                    assessment.attack_graph.edges
                )

        table = Table(title="Graph Statistics")

        table.add_column("Metric")
        table.add_column("Value")

        table.add_row(
            "Total Nodes",
            str(total_nodes),
        )

        table.add_row(
            "Total Edges",
            str(total_edges),
        )

        table.add_row(
            "Average Nodes",
            f"{total_nodes / max(1, len(campaign.executions)):.2f}",
        )

        table.add_row(
            "Average Edges",
            f"{total_edges / max(1, len(campaign.executions)):.2f}",
        )

        self.console.print(table)

    # ---------------------------------------------------------

    def _executive_summary(
        self,
        summary: list[str],
    ) -> None:

        table = Table(title="Executive Summary")

        table.add_column("Observation")

        for line in summary:
            table.add_row(line)

        self.console.print(table)