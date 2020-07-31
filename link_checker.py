import click

from checker.parser import find_all_anchor_tags, build_dicionary_of_links


@click.command()
@click.argument('url')
def main(url: str):
    """TODO: """
    page_links = find_all_anchor_tags(url)
    results = build_dicionary_of_links(url, page_links)

    for k, v in results.items():
        if v == 200:
            click.echo(click.style(f"{v} - {k}", fg="green"))
        else:
            click.echo(click.style(f"{v} - {k}", fg="yellow"))


if __name__ == "__main__":
    main()