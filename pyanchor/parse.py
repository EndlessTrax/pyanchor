import requests
from bs4 import BeautifulSoup

from pyanchor.types import AnchorTag


class PageResults:
    def __init__(self, url: str):
        self.url = url
        self.anchor_tags = self.parse_page_for_anchor_tags(url)

    def parse_page_for_anchor_tags(self, url: str) -> list[AnchorTag]:
        """#TODO: Add docstring"""
        atags = BeautifulSoup(requests.get(url).text, "lxml").find_all("a")
        return [
            AnchorTag(
                raw_tag=str(atag),
                attributes=atag.attrs,
                origin=url,
                href=atag.get("href"),
            )
            for atag in atags
        ]


class SiteMapResults:
    def __init__(self, url: str):
        self.url = url
        self.pages = self.parse_sitemap_for_all_page_urls(url)

    def parse_sitemap_for_all_page_urls(self, url: str) -> list[str]:
        sitemap = BeautifulSoup(requests.get(url).text, "lxml-xml").find_all("loc")
        return [url.text for url in sitemap]
