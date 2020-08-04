from sys import builtin_module_names
import pytest
from bs4.element import ResultSet

from checker.url import check_response_code, check_link_for_http_scheme
from checker.parser import find_all_anchor_tags, build_dicionary_of_links


def test_200_response():
    """TODO: """
    resp_code = check_response_code("https://google.com")
    assert resp_code == 200


def test_404_response():
    """TODO: """
    resp_code = check_response_code("https://google.com/blah-blah")
    assert resp_code == 404


def test_link_http_scheme():
    """TODO:"""

    base_url = "https://google.com"
    href = "https://google.com/services"
    assert check_link_for_http_scheme(base_url, href) == "https://google.com/services"


def test_relative_link_http_scheme():
    """TODO:"""

    base_url = "https://google.com"
    href = "/services"
    assert check_link_for_http_scheme(base_url, href) == "https://google.com/services"

# TODO: Add tests for checking http when ./, ../, # links have been addressed 


def test_find_all_anchor_tags_returns_bs4_object():
    """TODO:"""

    url = "https://google.com"
    all_atags = find_all_anchor_tags(url)
    assert isinstance(all_atags, ResultSet)

def test_find_all_anchor_tags_hits_exception():
    with pytest.raises(Exception):
        assert find_all_anchor_tags("https://google.com/404")


def test_build_dictionary_of_links_returns_dict():
    base_url = "https://google.com"
    all_atags = find_all_anchor_tags(base_url)
    results = build_dicionary_of_links(base_url, all_atags)
    assert isinstance(results, dict)


#TODO: Add test to check that a dictionary that is built is as expected based on given list of tags.