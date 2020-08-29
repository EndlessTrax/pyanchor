"""The main parser for finding and checking links

The LinkResults class expects a URL as it's only argument. It will return a 
dictionary of all links on the given html page which is stores in the object.results 
attribute. The returning dictionary consists of the link (dict key) and the http 
response (dict value).

    Typical usage example:

    results = LinkResults(url).results
"""

import requests
from bs4 import BeautifulSoup


class LinkResults:
    def __init__(self, url: str):
        self.base_url = url
        self.all_atags = self.find_all_atags(self.base_url)
        self.results = self.build_results_dictionary()

    def __str__(self) -> str:
        return f"All links for {self.base_url}"

    def check_link_for_http_scheme(self, href: str) -> str:
        """Checks a link for http scheme.
        
        If a qualified URL, nothing is done. If a relative link, then a full URL 
        is built using the base URL.

        Args:
            href: The hypertext reference of a give anchor tag.

        Returns:
            A full qualifying URL
         """

        if href.startswith(self.base_url):
            return href
        elif href.startswith("/"):
            href = self.base_url + href
            return href
        else:  # This catches any href set to '#'
            return None  # TODO: Deal with ./ or ../ relative links.

    def find_all_atags(self, url: str):  # Returns -> bs4.element.ResultSet
        """Find all anchor tags on a given URL.
        
        Args:
            url: A URL string

        Returns:
            A bs4.element.ResultSet object
        Raises:
            An exception is the page returns anything other than a 200 HTTP response
        """

        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            return soup.find_all("a")

        else:
            # TODO: Find better exception type/create custom Exception
            raise Exception(f"The requested page is unavailable -> {url}")

    def build_results_dictionary(self) -> dict:
        """Build the final results dictionary. 
        
        Once all_tags has been populated, the final results dictionary is build by 
        testing each link. 

        Returns:
            A dictionary with the key = the URL, and the value = the HTTP response.
        """

        results = dict()
        for tag in self.all_atags:
            href = tag.get("href")
            parsed_url = self.check_link_for_http_scheme(href)

            if parsed_url is not None:
                results[parsed_url] = requests.get(parsed_url).status_code
            else:
                pass

        return results

    # @property
    # def check_anchor_tags_attributes(self, tags):
    #     """TODO:"""
    #     return
