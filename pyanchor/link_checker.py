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
import re

class AllTags:

    def __init__(self, url: str):
        if url.endswith("/"):
            self.base_url = url
        else:
            self.base_url = url + "/"

        self.all_atags = self.find_all_atags(self.base_url)

    def __str__(self) -> str:
        return f"All links for {self.base_url}"

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


class LinkResults(AllTags):
    def __init__(self, url: str):
        super().__init__(url)
        self.results = self.build_results_dictionary()


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
            href = self.base_url + href.lstrip("/")
            return href

        elif href.startswith("./"):
            return self.base_url + re.sub("./", "", href)

        elif href.startswith("../"):
            return self.base_url + re.sub("../", "", href)

        else:
            return None # Catches any links starting with #


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


class LinkAnalysis(AllTags):
    """
    Check the anchor tag for:
        taget attr of any kind:
            check to see if rel="noreferrer noopener"
        missing Title attr
        Check for obsolete attrs
            charset
            coords
            name
            rev 
            shape

    Print output to user
    """

    def __init__(self, url: str):
        super().__init__(url)
        self.obsolete_attrs = self.obsolete_attrs(self.all_atags)


    def obsolete_attrs(self, links) -> dict:
        OBSOLETE_ATTRS = ('charset', 'coords', 'name', 'rev', 'shape')
        
        return_dict = dict()
        for link in links:
            obs_link_attrs = []
            for attribute in OBSOLETE_ATTRS:
                if link.get(attribute):
                    obs_link_attrs.append(attribute)

            if len(obs_link_attrs) > 0:
                href = link["href"]
                if href in return_dict:
                    return_dict[href].append(*obs_link_attrs)
                else: 
                    return_dict[href] = obs_link_attrs
        
        return return_dict


    def missing_attrs(self):
        pass

    def unsafe_attrs(self):
        pass
