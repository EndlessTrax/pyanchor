from pyanchor.types import AnchorTag
from pyanchor.filters import (
    filter_for_unsafe_links,
    filter_for_obsolete_attrs,
    filter_for_http_not_OK,
)


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
