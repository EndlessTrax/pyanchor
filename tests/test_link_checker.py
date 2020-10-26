import pytest

from pyanchor.link_checker import LinkAnalysis, LinkResults


@pytest.fixture
def example_LinkResults_object():
    return LinkResults("http://127.0.0.1:5000/")


@pytest.fixture
def example_LinkAnalysis_object():
    return LinkAnalysis("http://127.0.0.1:5000/")


class TestLinkResults:
    def test_results_is_dict(self, example_LinkResults_object):
        assert isinstance(example_LinkResults_object.results, dict)

    def test_link_result_class_str(self, example_LinkResults_object):
        assert str(example_LinkResults_object) == "All links for http://127.0.0.1:5000/"

    def test_successful_parse_relative_links(self, example_LinkResults_object):
        assert "http://127.0.0.1:5000/rel" in example_LinkResults_object.results[200]
        assert "http://127.0.0.1:5000/rel2" in example_LinkResults_object.results[200]


class TestLinkAnalysis:
    def test_obsolete_attrs_returns_dict(self, example_LinkAnalysis_object):
        assert isinstance(example_LinkAnalysis_object.obsolete_attrs, dict)

    def test_obsolete_attrs_on_tag(self, example_LinkAnalysis_object):
        attr_list = example_LinkAnalysis_object.obsolete_attrs
        assert attr_list["/about/link-1"][0] == "charset"
        assert attr_list["/about/link-2"][0] == "name"

    def test_unsafe_attrs_returns_dict(self, example_LinkAnalysis_object):
        assert isinstance(example_LinkAnalysis_object.unsafe_attrs, dict)
