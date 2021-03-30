import typer
import requests
from bs4 import BeautifulSoup
from pyanchor.link_checker import LinkResults


app = typer.Typer()


def print_results(links: dict, verbose: bool) -> int:
    """Simple utility function to print to terminal
    
    Args:
        Dictionary of links from LinkResults.results
    Returns:
        Two integers for the number of successful and unsuccessful links checked.
    """

    num_of_successful_links = 0
    num_of_failed_links = 0
    for http_code, url_list in links.items():
        if http_code == 200:
            for url in url_list:
                num_of_successful_links += 1
                if verbose:
                    typer.echo(typer.style(f"[ {http_code} ] - {url}", fg="green"))
        elif http_code == 500:
            for url in url_list:
                typer.echo(typer.style(f"[ {http_code} ] - {url}", fg="red"))
                num_of_failed_links += 1
        else:
            for url in url_list:
                typer.echo(typer.style(f"[ {http_code} ] - {url}", fg="yellow"))
                num_of_failed_links += 1

    return num_of_successful_links, num_of_failed_links


def print_totals(success: int, failed: int):
    """Prints results to terminal"""
    typer.echo("========================")
    typer.echo(f"TOTAL LINKS CHECKED: {success + failed}")
    typer.echo(f"FAILED: {failed}")


@app.command()
def main(
    url: str,
    sitemap: bool = typer.Option(
        False, "--sitemap", help="Use if the URL is a sitemap.xml link"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="By default all 200 responses will be hidden from the final output. Use verbose to view ALL results",
    ),
):
    """Check for broken links on any given web page. Pass in a sitemap URL to
    check all link on a given website.
    """

    if not url.startswith("http"):
        raise ValueError("Please provide a URL with a valid HTTP scheme")

    if sitemap:
        set_of_urls = set()
        results = {}

        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
            sitemap_links = soup.find_all("loc")

            for sitemap_link in sitemap_links:
                set_of_urls.add(sitemap_link.text)

        all_results = []
        for _url in set_of_urls:
            link_results = LinkResults(_url).results
            if len(link_results) > 0:
                all_results.append(link_results)

        success_totals = 0
        failed_totals = 0
        for results_dict in all_results:
            _success, _failed = print_results(results_dict, verbose=verbose)
            success_totals += _success
            failed_totals += _failed

    else:
        results = LinkResults(url).results
        success_totals, failed_totals = print_results(results, verbose=verbose)

    print_totals(success_totals, failed_totals)


if __name__ == "__main__":
    app()
