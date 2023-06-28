import typer
from rich.progress import Progress

from pyanchor.filters import (
    filter_for_http_not_OK,
    filter_for_obsolete_attrs,
    filter_for_unsafe_links,
)
from pyanchor.outputs import results_table
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
):
    """TODO: Add docstring"""

    with Progress() as progress:
        progress.add_task(f"Checking {url}...", total=None)

        results = PageResults(url).anchor_tags

        # filter results based on options passed in by user
        if unsafe:
            results = filter_for_unsafe_links(results)
        elif obsolete:
            results = filter_for_obsolete_attrs(results)
        elif not show_all:
            results = filter_for_http_not_OK(results)

    results_table(results)


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
):
    links_to_check = SiteMapResults(url).pages
    results = []

    for url in links_to_check:
        with Progress() as progress:
            task = progress.add_task(f"Checking {url}...", total=None)
            results.extend(PageResults(url).anchor_tags)
            progress.update(task, completed=100)

    if unsafe:
        results = filter_for_unsafe_links(results)
    elif obsolete:
        results = filter_for_obsolete_attrs(results)
    elif not show_all:
        results = filter_for_http_not_OK(results)

    results_table(results)


if __name__ == "__main__":
    check_app()
