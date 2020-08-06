import typer

from checker.checker import LinkResults

app = typer.Typer()

@app.command()
def main(url: str):
    """TODO: """

    if not url.startswith('http'):
        raise ValueError('Please provide a URL with a valid HTTP scheme')

    results = LinkResults(url).results

    for k, v in results.items():
        if v == 200:
            typer.echo(typer.style(f"{v} - {k}", fg="green"))
        else:
            typer.echo(typer.style(f"{v} - {k}", fg="yellow"))


if __name__ == "__main__":
    app()