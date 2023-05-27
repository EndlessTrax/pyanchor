import typer

from pyanchor.filters import (
    filter_for_http_not_OK,
    filter_for_obsolete_attrs,
    filter_for_unsafe_links,
)
from pyanchor.outputs import results_table
from pyanchor.parse import PageResults

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

    results = PageResults(url).anchor_tags

    # filter results based on options passed in by user
    if unsafe:
        results = filter_for_unsafe_links(results)
    elif obsolete:
        results = filter_for_obsolete_attrs(results)
    elif not show_all:
        results = filter_for_http_not_OK(results)

    # print results
    results_table(results)


if __name__ == "__main__":
    check_app()
