import pytest

from pyanchor.link_checker import LinkResults


@pytest.fixture
def example_object():
    return LinkResults("http://127.0.0.1:5000/")


class TestLinkChecker:
    def test_results_is_dict(self, example_object):
        assert isinstance(example_object.results, dict)

    def test_link_result_class_str(self, example_object):
        assert str(example_object) == "All links for http://127.0.0.1:5000/"

    def test_successful_parse_relative_links(self, example_object):
        assert "http://127.0.0.1:5000/rel" in example_object.results[200]
        assert "http://127.0.0.1:5000/rel2" in example_object.results[200]
