import csv
from pathlib import Path

from rich.console import Console
from rich.table import Table

from pyanchor.types import AnchorTag


def results_table(
    results: list[AnchorTag], show_obsolete: bool = False, show_unsafe: bool = False
):
    """TODO: Add docstring"""
    table = Table(title="Results")
    table.add_column("Status Code", justify="right", style="cyan", no_wrap=True)
    table.add_column("Href", style="magenta")
    table.add_column("Origin", style="green")

    for anchor_tag in results:
        table.add_row(
            str(anchor_tag.status_code),
            anchor_tag.href,
            anchor_tag.origin,
        )

    console = Console()
    console.print(table)


def results_to_csv(
    filename: Path,
    results: list[AnchorTag],
    show_obsolete: bool = False,
    show_unsafe: bool = False,
):
    """TODO: Add docstring"""
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Status Code", "Href", "Origin"])
        for anchor_tag in results:
            writer.writerow(
                [
                    str(anchor_tag.status_code),
                    anchor_tag.href,
                    anchor_tag.origin,
                ]
            )
