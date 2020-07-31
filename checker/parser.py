import requests
from click.utils import echo
from bs4 import BeautifulSoup
from requests.models import MissingSchema

from .url import check_response_code, check_link_for_http_scheme


def find_all_anchor_tags(url: str):
    """TODO: Scrapes the given url/link for all anchor tags and returns a <class 'bs4.element.ResultSet'>"""

    try:  # Ensure the url link is formatted correctly and involves a http scheme.
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            return soup.find_all("a")

        else:  # If not a 200 response, then an Exception is raised
            raise Exception(f"The requested page is unavailable -> {url}")
    except MissingSchema as e:  # Built in Exception from the requests library.
        echo(e)


def build_dicionary_of_links(base_url, atags) -> dict:
    """TODO: Builds a dictonary containing the full link url as the key, with the response code as the value"""

    results = dict()
    for tag in atags:
        href = tag.get("href")
        parsed_url = check_link_for_http_scheme(base_url, href)
        results[parsed_url] = check_response_code(parsed_url)
        
    return results