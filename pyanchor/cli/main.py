import typer

from pyanchor.cli.commands.check import check_app

app = typer.Typer()
app.add_typer(check_app, name="check")


if __name__ == "__main__":
    app()

"""
anchors check url <url> [options]

anchors check sitemap <file> [options]

Options:
  -v, --version				output the version number
  -o, --output <file>		output results to a file
  -a, --all					Show all results, includes HTTP OK
  -u, --unsafe				Show unsafe and unsupported attributes
  -h, --help				output usage information
"""
