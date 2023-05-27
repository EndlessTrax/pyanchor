from rich.console import Console
from rich.table import Table

from pyanchor.types import AnchorTag


def results_table(
    results: list[AnchorTag], how_obsolete: bool = False, show_unsafe: bool = False
):
    table = Table(title="Anchor Status Code Check", show_footer=True)
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
