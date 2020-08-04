import typer

from checker.parser import find_all_anchor_tags, build_dicionary_of_links

app = typer.Typer()

@app.command()
def main(url: str):
    """TODO: """

    if not url.startswith('http'):
        raise ValueError('Please provide a URL with a valid HTTP scheme')

    page_links = find_all_anchor_tags(url)
    results = build_dicionary_of_links(url, page_links)

    for k, v in results.items():
        if v == 200:
            typer.echo(typer.style(f"{v} - {k}", fg="green"))
        else:
            typer.echo(typer.style(f"{v} - {k}", fg="yellow"))


if __name__ == "__main__":
    app()