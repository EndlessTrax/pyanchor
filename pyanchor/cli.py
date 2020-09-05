import typer
import requests
from bs4 import BeautifulSoup
from link_checker import LinkResults


app = typer.Typer()


def print_results(links: dict):
    """Simple utility function to print to terminal"""
    num_of_failed_links = 0
    for k, v in links.items():
        if k == 200:
            for link in v:
                typer.echo(typer.style(f"[ {k} ] - {link}", fg="green"))
        elif k == 500:
            for link in v:
                typer.echo(typer.style(f"[ {k} ] - {link}", fg="red"))
                num_of_failed_links += 1
        else:
            for link in v:
                typer.echo(typer.style(f"[ {k} ] - {link}", fg="yellow"))
                num_of_failed_links += 1

    typer.echo("========================")
    typer.echo(f"TOTAL LINKS CHECKED: {len(links[200]) + num_of_failed_links}")
    typer.echo(f"FAILED: {num_of_failed_links}")


@app.command()
def main(
    url: str,
    sitemap: bool = typer.Option(
        False, "--sitemap", help="Use if the URL is a sitemap.xml link"
    ),
):
    """Check for broken links on any given webpage. Pass in a sitemap URL to 
    check all link on a given website.
    """

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
            link_results = LinkResults(_url).results
            print_results(link_results)

    else:
        results = LinkResults(url).results
        print_results(results)


if __name__ == "__main__":
    app()
