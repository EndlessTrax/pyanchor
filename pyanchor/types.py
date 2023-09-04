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
    attributes: dict
    href: str
    origin: str
    raw_tag: str
    obsolete_attrs: Optional[list] = None
    status_code: Optional[int] = None

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
        """Build a qualified URL from the origin and href."""

        if not self.origin.endswith("/"):
            self.origin = self.origin + "/"

        if self.href.startswith("http"):
            return self.href
        elif self.href.startswith(("/", "./", "../")):
            return urljoin(self.origin, self.href)
        else:
            # Catch anchor tags with # or no href
            return None

    def check_for_obsolete_attrs(self) -> list[str]:
        """Return a list of obsolete attributes."""
        self.obsolete_attrs = [
            attr
            for attr in self.attributes
            if attr in ObsoleteAttrs.__members__.values()
        ]
        return self.obsolete_attrs

    def check_is_unsafe(self) -> bool:
        """Return True if the anchor tag is unsafe, False if it is safe."""
        if self.attributes.get("target"):
            if self.attributes.get("rel") and "noopener" in self.attributes.get("rel"):  # type: ignore  # noqa: E501
                return True
        return False
