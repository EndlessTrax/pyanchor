from pyanchor.types import AnchorTag


def filter_for_unsafe_links(anchor_tags: list[AnchorTag]) -> list[AnchorTag]:
    """Filter a list of AnchorTags for unsafe links."""
    return [atag for atag in anchor_tags if atag.check_is_unsafe()]


def filter_for_obsolete_attrs(anchor_tags: list[AnchorTag]) -> list[AnchorTag]:
    """Filter a list of AnchorTags for obsolete attributes."""
    return [atag for atag in anchor_tags if len(atag.check_for_obsolete_attrs()) > 0]


def filter_for_http_not_OK(anchor_tags: list[AnchorTag]) -> list[AnchorTag]:
    """Filter a list of AnchorTags for HTTP status codes that are not 200."""
    return [
        atag
        for atag in anchor_tags
        if atag.status_code != 200 and atag.status_code is not None
    ]

def filter_final_results(anchor_tags: list[AnchorTag], unsafe: bool, obsolete: bool, show_all: bool) -> list[AnchorTag]:
    """Filter a list of AnchorTags for final results based on user options."""
    if unsafe:
        anchor_tags = filter_for_unsafe_links(anchor_tags)
    elif obsolete:
        anchor_tags = filter_for_obsolete_attrs(anchor_tags)
    elif not show_all:
        anchor_tags = filter_for_http_not_OK(anchor_tags)
    return anchor_tags
