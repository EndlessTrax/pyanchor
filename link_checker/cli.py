import typer
import requests
from bs4 import BeautifulSoup
from link_checker import LinkResults


app = typer.Typer()


def print_result(link: dict):
    """TODO:"""
    for k, v in link.items():
        if v == 200:
            typer.echo(typer.style(f"[ {v} ] - {k}", fg="green"))
        else:
            typer.echo(typer.style(f"[ {v} ] - {k}", fg="yellow"))


@app.command()
def main(
    url: str,
    sitemap: bool = typer.Option(
        False, "--sitemap", help="Use if URL is a sitemap.xml link"
    ),
):
    """TODO: """

    if not url.startswith("http"):
        raise ValueError("Please provide a URL with a valid HTTP scheme")

    if sitemap is True:
        set_of_urls = set()
        results = dict()

        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
            sitemap_links = soup.find_all("loc")

            for sitemap_link in sitemap_links:
                set_of_urls.add(sitemap_link.text)

        for _url in set_of_urls:
            link_result = LinkResults(_url).results

            for k, v in link_result.items():
                results[k] = v

        print_result(results)

    else:
        results = LinkResults(url).results
        print_result(results)


if __name__ == "__main__":
    app()
