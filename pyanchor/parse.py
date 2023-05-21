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
                href=atag.get("href"),
                origin=url,
                text=atag.text,
            )
            for atag in atags
        ]
