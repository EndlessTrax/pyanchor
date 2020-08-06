import pytest
from typer.testing import CliRunner

from link_checker import app
from checker.checker import LinkResults


runner = CliRunner()


def test_exception_on_invalid_url_http_scheme():
    """TODO:"""
    
    result = runner.invoke(app, ['google.com'])
    assert result.exit_code == 1


def test_successful_result_prints():
    """TODO: """

    results = runner.invoke(app, ['https://google.com'])
    assert "200 - https://google.com/services/" in results.output


@pytest.fixture
def example_object():
    return LinkResults("https://google.com")


def test_link_result_class_str(example_object):
    """TODO:"""
    assert str(example_object) == 'All links for https://google.com'
    

def test_results_is_dict(example_object):
    """TODO:"""
    assert isinstance(example_object.results, dict)