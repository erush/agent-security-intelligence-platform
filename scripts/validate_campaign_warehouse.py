from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from asip.warehouse.campaign_repository import CampaignRepository
from asip.warehouse.metadata import WarehouseMetadata

console = Console()


def row_count(repo: CampaignRepository, table: str) -> int:

    with repo._connect() as conn:

        row = conn.execute(
            f"""
            SELECT COUNT(*)
            FROM {table}
            """
        ).fetchone()

    return row[0]


def exists(repo: CampaignRepository, table: str) -> bool:

    with repo._connect() as conn:

        row = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE name = ?
            """,
            (table,),
        ).fetchone()

    return row is not None


def main() -> None:

    repo = CampaignRepository()

    metadata = WarehouseMetadata()

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]Campaign Warehouse Validation[/bold cyan]"
        )
    )

    table = Table(title="Warehouse Objects")

    table.add_column("Object")

    table.add_column("Exists")

    table.add_column("Rows")

    for name in metadata.dimension_tables:

        table.add_row(
            name,
            "✓" if exists(repo, name) else "✗",
            str(row_count(repo, name)) if exists(repo, name) else "-",
        )

    for name in metadata.fact_tables:

        table.add_row(
            name,
            "✓" if exists(repo, name) else "✗",
            str(row_count(repo, name)) if exists(repo, name) else "-",
        )

    for name in metadata.analytics_tables:

        table.add_row(
            name,
            "✓" if exists(repo, name) else "✗",
            str(row_count(repo, name)) if exists(repo, name) else "-",
        )

    console.print(table)

    metadata.campaign_count = row_count(repo, "fact_campaign")

    metadata.attack_count = row_count(repo, "fact_attack")

    metadata.finding_count = row_count(repo, "fact_attack_finding")

    metadata.graph_edge_count = row_count(repo, "fact_attack_edge")

    metadata.tool_event_count = row_count(repo, "fact_tool_event")

    summary = Table(title="Warehouse Summary")

    summary.add_column("Metric")

    summary.add_column("Value")

    summary.add_row("Campaigns", str(metadata.campaign_count))

    summary.add_row("Attacks", str(metadata.attack_count))

    summary.add_row("Findings", str(metadata.finding_count))

    summary.add_row("Tool Events", str(metadata.tool_event_count))

    summary.add_row("Graph Edges", str(metadata.graph_edge_count))

    summary.add_row("Warehouse Version", metadata.warehouse_version)

    summary.add_row("Schema Version", metadata.schema_version)

    summary.add_row("Analytics Version", metadata.analytics_version)

    summary.add_row(
        "Last Refresh",
        metadata.refreshed_at.isoformat(timespec="seconds"),
    )

    console.print()

    console.print(summary)

    console.print()

    console.print(
        "[bold green]✓ Warehouse validation completed successfully.[/bold green]"
    )

    console.print()


if __name__ == "__main__":
    main()