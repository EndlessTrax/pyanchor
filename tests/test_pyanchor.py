from pyanchor.filters import (
    filter_for_http_not_OK,
    filter_for_obsolete_attrs,
    filter_for_unsafe_links,
)
from pyanchor.types import AnchorTag


class TestAnchorTag:
    def test_str(self):
        anchor = AnchorTag(
            '<a href="/link-1">Link 1</a>',
            {"href": "/link-1", "text": "Link 1"},
            "http://example.com",
            "/link-1",
        )
        assert str(anchor) == '<a href="/link-1">Link 1</a>'

    def test_build_qualified_url(self):
        anchor_tags = [
            AnchorTag(
                '<a href="/link-1">Link 1</a>',
                {"href": "/link-1", "text": "Link 1"},
                "http://example.com",
                "/link-1",
            ),
            AnchorTag(
                '<a href="http://example.com/link-2">Link 2</a>',
                {"href": "http://example.com/link-2", "text": "Link 2"},
                "http://example.com",
                "http://example.com/link-2",
            ),
            AnchorTag(
                '<a href="./link-3">Link 3</a>',
                {"href": "./link-3", "text": "Link 3"},
                "http://example.com",
                "./link-3",
            ),
            AnchorTag(
                '<a href="../link-4">Link 4</a>',
                {"href": "../link-4", "text": "Link 4"},
                "http://example.com",
                "../link-4",
            ),
            AnchorTag(
                '<a href="#">Link 5</a>',
                {"href": "#", "text": "Link 5"},
                "http://example.com",
                "#",
            ),
        ]
        assert anchor_tags[0].qualified_url == "http://example.com/link-1"
        assert anchor_tags[1].qualified_url == "http://example.com/link-2"
        assert anchor_tags[2].qualified_url == "http://example.com/link-3"
        assert anchor_tags[3].qualified_url == "http://example.com/link-4"
        assert anchor_tags[4].qualified_url is None


class TestFilters:
    def test_filter_for_unsafe_links(self):
        atags = [
            AnchorTag(
                '<a href="/link-1 target="_blank">Safe Link</a>',
                {"href": "link-1", "text": "Safe Link", "target": "_blank"},
                "http://example.com",
                "/link-1",
            ),
            AnchorTag(
                '<a href="/link-2" target="_blank" rel="noreferrer noopener">Unsafe Link</a>',  # noqa
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
        unsafe = filter_for_unsafe_links(atags)
        assert len(unsafe) == 1

    def test_filter_for_obsolete_attrs(self):
        atags = [
            AnchorTag(
                '<a href="/link-1">Link 1</a>',
                {"href": "/link-1", "text": "Link 1"},
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
        obsolete = filter_for_obsolete_attrs(atags)
        assert len(obsolete) == 1

    def test_filter_for_http_not_OK(self):
        atags = [
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
        atags[0].status_code = 200
        atags[1].status_code = 404
        not_okay = filter_for_http_not_OK(atags)
        assert len(not_okay) == 1