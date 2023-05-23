from http.client import responses

from pyanchor.types import AnchorTag


def filter_for_unsafe_links(anchor_tags: list[AnchorTag]) -> None:
    for atag in anchor_tags:
        if not atag.check_is_unsafe():
            anchor_tags.remove(atag)


def filter_for_obsolete_attrs(anchor_tags: list[AnchorTag]) -> None:
    for atag in anchor_tags:
        if not len(atag.check_for_obsolete_attrs()) > 0:
            anchor_tags.remove(atag)


def filter_for_http_not_OK(anchor_tags: list[AnchorTag]) -> None:
    for atag in anchor_tags:
        if atag.status_code and responses[atag.status_code] == "OK":
            anchor_tags.remove(atag)
