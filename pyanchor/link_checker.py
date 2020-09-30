"""The main parser for finding and checking links

The LinkResults class expects a URL as it's only argument. It will return a 
dictionary of all links on the given html page which is stores in the object.results 
attribute. The returning dictionary consists of the link (dict value) and the http 
response (dict key).

    Typical usage example:

    results = LinkResults(url).results
"""

import requests
from bs4 import BeautifulSoup


class LinkResults:
    def __init__(self, url: str):
        if url.endswith("/"):
            self.base_url = url
        else:
            self.base_url = url + "/"

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
        
        elif href.startswith("./"):
            import re   #using re.sub to remove all instances ./
            href=self.base_url +re.sub("./","",href)
            return href

        elif href.startswith("../"):
            import re #using re.sub to remove all instances of ../
            href=self.base_url + re.sub("../","",href)
            return href

        elif href.startswith("#"):
            if "#" not in self.base_url:
                hrefList=list(self.base_url) '''if relative link starts with #, checks if # already exists in base url. I not, then adds the # followed by the relative url to base url'''
                href= "".join(hrefList.pop(-1)) + href
                return href
            else:
                return None
        elif href.startswith("http"):
            return href
        else:
            return self.base_url + href #Some websites such as https://www.debian.org/ have relative urls that don't start with a /

    def find_all_atags(self, url: str):
        """Find all anchor tags on a given URL.
        
        Args:
            url: A URL string

        Returns:
            A bs4.element.ResultSet object
        """

        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            return soup.find_all("a")

    def build_results_dictionary(self) -> dict:
        """Build the final results dictionary.
        
        Once all_tags has been populated, the final results dictionary is build by 
        testing each link. 

        Returns:
            A dictionary with the key = the HTTP response, 
            and the value = a List of URLs that achieved that response code.
        """

        results = dict()

        try:
            for tag in self.all_atags:
                href = tag.get("href")
                parsed_url = self.check_link_for_http_scheme(href)
                if parsed_url is not None:
                    parsed_url_status_code = requests.get(parsed_url).status_code

                    if parsed_url_status_code in results:
                        results[parsed_url_status_code].append(parsed_url)
                    else:
                        results[parsed_url_status_code] = [parsed_url]
        except:
            pass

        return results
