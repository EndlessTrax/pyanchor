from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional
from urllib.parse import urljoin

import requests


class ObsoleteAttrs(StrEnum):
    CHARSET = auto()
    COORDS = auto()
    NAME = auto()
    REV = auto()
    SHAPE = auto()


@dataclass
class AnchorTag:
    raw_tag: str
    attributes: dict
    origin: str
    href: str
    status_code: Optional[int] = None
    obsolete_attrs: Optional[list] = None
    # TODO: Find out best method for ordering dataclass fields

    def __post_init__(self) -> None:
        self.qualified_url = self.build_qualified_url()
        if self.qualified_url:
            try:
                self.status_code = requests.get(
                    self.qualified_url, allow_redirects=True
                ).status_code
            except requests.exceptions.ConnectionError:
                self.status_code = None

    def __str__(self) -> str:
        return f"{self.raw_tag}"

    def build_qualified_url(self) -> str or None:
        """#TODO: Add docstring"""

        if not self.origin.endswith("/"):
            self.origin = self.origin + "/"

        if self.href.startswith("http"):
            return self.href
        elif self.href.startswith(("/", "./", "../")):
            return urljoin(self.origin, self.href)
        else:
            # Catch anchor tags with # or no href
            return None  # TODO: Deal with exceptions better

    def check_for_obsolete_attrs(self) -> list[str]:
        """#TODO Add docstring"""
        self.obsolete_attrs = [
            attr
            for attr in self.attributes
            if attr in ObsoleteAttrs.__members__.values()
        ]
        return self.obsolete_attrs

    def check_is_unsafe(self) -> bool:
        """#TODO Add docstring"""
        if self.attributes.get("target"):
            if self.attributes.get("rel") and "noopener" in self.attributes.get("rel"):  # type: ignore  # noqa: E501
                return True
        return False
