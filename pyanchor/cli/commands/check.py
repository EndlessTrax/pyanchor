import typer
from rich import print as rprint
from rich.progress import Progress

from pyanchor.filters import (
    filter_final_results
)
from pyanchor.outputs import results_table, results_to_csv
from pyanchor.parse import PageResults, SiteMapResults

check_app = typer.Typer()


@check_app.command("url")
def check_url(
    url: str,
    show_all: bool = typer.Option(
        False, "--all", "-A", help="Show all - includes HTTP OK"
    ),
    unsafe: bool = typer.Option(False, "--unsafe", "-U", help="Show unsafe links"),
    obsolete: bool = typer.Option(
        False, "--obsolete", "-O", help="Show links with obsolete attributes"
    ),
    output: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Output results to a csv file.",
    ),
):
    """Check the anchor tags on a single URL."""

    with Progress() as progress:
        progress.add_task(f"Checking {url}...", total=None)

        results = PageResults(url).anchor_tags

    rprint(f"Found {len(results)} links.")

    # filter results based on options passed in by user
    filtered_results = filter_final_results(results, unsafe, obsolete, show_all)

    if output:
        results_to_csv(output, filtered_results)
        rprint(f"Complete - results written to [green]{output}[/green]")
    else:
        results_table(filtered_results)


@check_app.command("sitemap")
def check_sitemap(
    url: str,
    show_all: bool = typer.Option(
        False, "--all", "-A", help="Show all - includes HTTP OK"
    ),
    unsafe: bool = typer.Option(False, "--unsafe", "-U", help="Show unsafe links"),
    obsolete: bool = typer.Option(
        False, "--obsolete", "-O", help="Show links with obsolete attributes"
    ),
    output: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Output results to a csv file.",
    ),
):
    """Check the anchor tags from all URLs on a sitemap.xml file."""
    pages_to_check = SiteMapResults(url).pages
    results = []

    rprint(f"Found {len(pages_to_check)} pages to check.")
    for url in pages_to_check:
        with Progress() as progress:
            task = progress.add_task(f"Checking {url}...", total=None)
            results.extend(PageResults(url).anchor_tags)
            progress.update(task, completed=100)

    rprint(f"Found {len(results)} links.")

    filtered_results = filter_final_results(results, unsafe, obsolete, show_all)

    if output:
        results_to_csv(output, filtered_results)
        rprint(f"Complete - results written to [green]{output}[/green]")
    else:
        results_table(filtered_results)


if __name__ == "__main__":
    check_app()
