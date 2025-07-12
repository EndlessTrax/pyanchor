"""The main parser for finding and checking links

The LinkResults class expects a URL as its only argument. It will return a 
dictionary of all links on the given html page which is stores in the object.results 
attribute. The returning dictionary consists of the link (dict value) and the http 
response (dict key).

    Typical usage example:

    results = LinkResults(url).results

The LinkAnalysis class expects a URL as its only argument, also. It returns a 
dictionary of all links that have the `target` attribute, and then analyzes to 
see if they are safe links (i.e. have a `rel` attribute, too). Links are also 
checked for obsolote attributes.

    Typical usage example:

    obsolete = LinkAnalysis(url).obsolete_attrs
    or
    unsafe = LinkAnalysis(url).unsafe_attrs
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional


class AllTags:
    def __init__(self, url: str):
        self.base_url = url if url.endswith("/") else url + "/"
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

    def check_link_for_http_scheme(self, href: Optional[str]) -> Optional[str]:
        """Checks a link for http scheme.
        
        If a qualified URL, nothing is done. If a relative link, then a full URL 
        is built using the base URL.

        Args:
            href: The hypertext reference of a give anchor tag.

        Returns:
            A full qualifying URL
        """

        if href is None:
            return None

        if href.startswith(self.base_url):
            return href

        elif href.startswith("/"):
            href = self.base_url + href.lstrip("/")
            return href

        elif href.startswith("./"):
            return self.base_url + href.lstrip("./")

        elif href.startswith("../"):
            return self.base_url + href.lstrip("../")

        else:
            return None  # Catches any links starting with hash(#)

    def build_results_dictionary(self) -> dict:
        """Build the final results dictionary.
        
        Once all_tags has been populated in the AllTags base class, the final 
        results dictionary is build by testing each link.

        Returns:
            A dictionary with the key = the HTTP response,
            and the value = a List of URLs that achieved that response code.
        """

        results = {}

        try:
            for tag in self.all_atags: # type: ignore
                href = tag.get("href") # type: ignore
                parsed_url = self.check_link_for_http_scheme(href) # type: ignore
                if parsed_url is not None:
                    parsed_url_status_code = requests.get(parsed_url).status_code

                    if parsed_url_status_code in results:
                        results[parsed_url_status_code].append(parsed_url)
                    else:
                        results[parsed_url_status_code] = [parsed_url]
        except Exception:
            pass

        return results


class LinkAnalysis(AllTags):
    def __init__(self, url: str):
        super().__init__(url)
        self.obsolete_attrs = self.obsolete_attributes(self.all_atags)
        self.unsafe_attrs = self.unsafe_attributes(self.all_atags)

    def obsolete_attributes(self, links) -> dict:
        """ Check links for the presence of obsolete attributes
        
        Args:
            links: Takes a bs4 ResultSet which is returned from AllTags in self.all_atags

        Returns:
            Returns a dictionary with the key being the `href` of the link, 
            and the value being a `List` of obsolete attributes that the link has. 
            Any link with zero obsolete attributes is ingnored.

        """

        OBSOLETE_ATTRS = ("charset", "coords", "name", "rev", "shape")

        return_dict = {}
        for link in links:
            obs_link_attrs = [
                attribute for attribute in OBSOLETE_ATTRS if link.get(attribute)
            ]

            if obs_link_attrs:
                href = link["href"]
                if href in return_dict:
                    for _attr in obs_link_attrs:
                        return_dict[href].append(_attr)
                else:
                    return_dict[href] = obs_link_attrs

        return return_dict

    def unsafe_attributes(self, links) -> dict:
        """ Checks to see if links are unsafe.

        All links with the `target` attribute are checked for the presence/absence
        of a `rel="noopener"`. This should be present on all anchor tags with the
        `target` attribute to ensure the linked site does not have access to 
        window.opener property.
        
        For more details: https://developer.mozilla.org/en-US/docs/Web/HTML/Link_types/noopener 

        Args:
            links: Takes a bs4 ResultSet which is returned from AllTags in self.all_atags

        Returns:
            Returns a dictionary with the key being the full anchor tag checked, 
            and the value being a `Bool`. False = safe link, True = unsafe.
        """
        return_dict = {}
        for link in links:
            if link.get("target"):
                if link.get("rel") and "noopener" in link.get("rel"):
                    return_dict[link] = False
                else:
                    return_dict[link] = True

        return return_dict
