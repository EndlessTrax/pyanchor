import pytest

from pyanchor.filters import (  
    filter_for_http_not_OK,
    filter_for_obsolete_attrs,
    filter_for_unsafe_links,
)

from pyanchor.parse import PageResults

results = PageResults("http://127.0.0.1:5000").anchor_tags

class TestFilters:
    def test_filter_for_unsafe_links(self):
        filter_for_unsafe_links(results)
        assert len(results) == 1

    def test_filter_for_obsolete_attrs(self):
        filter_for_obsolete_attrs(results)
        assert len(results) == 1

    def test_filter_for_http_not_OK(self):
        filter_for_http_not_OK(results)
        assert len(results) == 1
