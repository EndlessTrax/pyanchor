import typer

from pyanchor.cli.commands.check import check_app

app = typer.Typer()
app.add_typer(check_app, name="check")


if __name__ == "__main__":
    app()
