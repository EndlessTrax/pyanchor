from pyanchor.types import AnchorTag
from pyanchor.filters import (
    filter_for_unsafe_links,
    filter_for_obsolete_attrs,
    filter_for_http_not_OK,
)


class TestFilters:
    def test_filter_for_unsafe_links(self):
        unsafe = [
            AnchorTag(
                '<a href="/link-1 target="_blank">Safe Link</a>',
                {"href": "link-1", "text": "Safe Link", "target": "_blank"},
                "http://example.com",
                "/link-1",
            ),
            AnchorTag(
                '<a href="/link-2" target="_blank" rel="noreferrer noopener">Unsafe Link</a>',
                {
                    "href": "link-2",
                    "text": "Unsafe Link",
                    "target": "_blank",
                    "rel": ["noreferrer", "noopener"],
                },
                "http://example.com",
                "/link-2",
            ),
        ]
        filter_for_unsafe_links(unsafe)
        assert len(unsafe) == 1


    def test_filter_for_obsolete_attrs(self):
        obsolete = [
            AnchorTag(
                '<a href="/link-1" name="test">Link 1</a>',
                {"href": "/link-1", "text": "Link 1", "name": "test"},
                "http://example.com",
                "/link-1",
            ),
            AnchorTag(
                '<a href="/link-2" rev="test" coords="testing">Link 2</a>',
                {
                    "href": "/link-2",
                    "text": "Link 2",
                    "rev": "test",
                    "coords": "testing",
                },
                "http://example.com",
                "/link-2",
            ),
        ]
        filter_for_obsolete_attrs(obsolete)
        assert len(obsolete) == 1


    def test_filter_for_http_not_OK(self):
        not_okay = [
            AnchorTag(
                '<a href="/link-1">Link 1</a>',
                {"href": "/link-1", "text": "Link 1"},
                "http://example.com",
                "/link-1",
            ),
            AnchorTag(
                '<a href="/dhjaow">Failing Link</a>',
                {"href": "/dhjaow", "text": "Failing Link"},
                "http://example.com",
                "/dhjaow",
            ),
        ]
        not_okay[0].status_code = 200
        not_okay[1].status_code = 404
        filter_for_http_not_OK(not_okay)
        assert len(not_okay) == 1
