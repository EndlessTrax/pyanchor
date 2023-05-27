from pyanchor.types import AnchorTag


def filter_for_unsafe_links(anchor_tags: list[AnchorTag]) -> list[AnchorTag]:
    """#TODO: Add docstring"""
    return [atag for atag in anchor_tags if atag.check_is_unsafe()]


def filter_for_obsolete_attrs(anchor_tags: list[AnchorTag]) -> list[AnchorTag]:
    """#TODO: Add docstring"""
    return [atag for atag in anchor_tags if len(atag.check_for_obsolete_attrs()) > 0]


def filter_for_http_not_OK(anchor_tags: list[AnchorTag]) -> list[AnchorTag]:
    """#TODO: Add docstring"""
    return [
        atag
        for atag in anchor_tags
        if atag.status_code != 200 and atag.status_code is not None
    ]
