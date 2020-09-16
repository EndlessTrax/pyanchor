from os import link
import typer
import requests
from bs4 import BeautifulSoup
from link_checker import LinkResults


app = typer.Typer()


def print_results(links: dict, verbose: bool):
    """Simple utility function to print to terminal"""
    num_of_failed_links = 0
    for http_code, url_list in links.items():
        if http_code == 200 and verbose == True:
            for link in url_list:
                typer.echo(typer.style(f"[ {http_code} ] - {link}", fg="green"))
        
        if http_code == 500:
            for link in url_list:
                typer.echo(typer.style(f"[ {http_code} ] - {link}", fg="red"))
                num_of_failed_links += 1
        else:
            for link in url_list:
                typer.echo(typer.style(f"[ {http_code} ] - {link}", fg="yellow"))
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
    verbose: bool = typer.Option(
        False, "--verbose", help="By default all 200 responses will be hidden from the final output. Use verbose to view ALL results"
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

        all_results = list()
        for _url in set_of_urls:
            link_results = LinkResults(_url).results
            if len(link_results) > 0:
                all_results.append(link_results)
        
        

        # print_results(all_results, verbose=verbose)

    else:
        results = LinkResults(url).results
        print_results(results, verbose=verbose)


if __name__ == "__main__":
    app()
