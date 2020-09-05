import pytest
from typer.testing import CliRunner

from pyanchor.cli import app
from pyanchor.link_checker import LinkResults


runner = CliRunner()


@pytest.fixture
def example_object():
    return LinkResults("http://127.0.0.1:5000/")


def test_exception_on_invalid_url_http_scheme():
    result = runner.invoke(app, ["google.com"])
    assert result.exit_code == 1


def test_successful_result_prints():
    results = runner.invoke(app, ["http://127.0.0.1:5000/"])
    assert "[ 200 ] - http://127.0.0.1:5000/about" in results.output


def test_failing_result_prints():
    results = runner.invoke(app, ["http://127.0.0.1:5000/"])
    assert "[ 500 ] - http://127.0.0.1:5000/500" in results.output


def test_link_result_class_str(example_object):
    assert str(example_object) == "All links for http://127.0.0.1:5000/"


def test_results_is_dict(example_object):
    assert isinstance(example_object.results, dict)


def test_sitemap_successful_result_prints():
    results = runner.invoke(app, ["http://127.0.0.1:5000/sitemap.xml", "--sitemap"])
    assert "[ 200 ] - http://127.0.0.1:5000/about" in results.output


def test_sitemap_failing_result_prints():
    results = runner.invoke(app, ["http://127.0.0.1:5000/sitemap.xml", "--sitemap"])
    assert "[ 500 ] - http://127.0.0.1:5000/500" in results.output
