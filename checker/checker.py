import requests
from bs4 import BeautifulSoup


class LinkResults():
    """TODO:"""

    def __init__(self, url: str):
        self.base_url = url
        self.results = self.build_results_dictionary(url)


    def __str__(self) -> str:
        """TODO:"""
        return 


    def check_link_for_http_scheme(self, href: str) -> str:
        """TODO: """
        if href.startswith(self.base_url):
            return href
        elif href.startswith("/"):
            href = self.base_url + href
            return href
        else:
            return href  # TODO: Deal with ./ or ../ relative links. And #links


    def build_results_dictionary(self, url: str) -> dict:
        """TODO:"""
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            self.all_atags = soup.find_all("a")

        else:  # If not a 200 response, then an Exception is raised
            raise Exception(f"The requested page is unavailable -> {url}") #TODO: Find better exception type/create custom Exception

        results = dict()
        for tag in self.all_atags:
            href = tag.get("href")
            parsed_url = self.check_link_for_http_scheme(href)
            results[parsed_url] = requests.get(parsed_url).status_code
            
        return results
