import typer

from pyanchor.parse import PageResults

check_app = typer.Typer()

@check_app.command("url")
def check_url(
    url: str, 
    show_all: bool = typer.Option(False, "--all", "-a", help="Show all results, includes HTTP OK"), # noqa
    unsafe: bool = typer.Option(False, "--unsafe", "-u", help="Show unsafe and unsupported attributes"), # noqa   
):
    results = PageResults(url)

    # filter results based on options passed in by user
    if unsafe:
        for atag in results.anchor_tags:
            atag.check_is_unsafe()
            atag.check_for_obsolete_attrs()
            
            if atag.is_unsafe:
                typer.echo(atag.href)

    if show_all:
        for atag in results.anchor_tags:
            typer.echo(atag.href)
    else:
        for atag in results.anchor_tags:
            if atag.status_code != 200:
                typer.echo(atag.href)



if __name__ == "__main__":
    check_app()