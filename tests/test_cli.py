import pytest

from typer.testing import CliRunner
from pyanchor.cli import app


runner = CliRunner()


@pytest.mark.usefixtures("server")
class TestCli:
    def test_exception_on_invalid_url_http_scheme(self):
        result = runner.invoke(app, ["main", "google.com"])
        assert result.exit_code == 1

    def test_successful_result_prints(self):
        results = runner.invoke(app, ["main", "http://127.0.0.1:5000/", "--verbose"])
        assert "[ 200 ] - http://127.0.0.1:5000/about" in results.output

    def test_failing_result_prints(self):
        results = runner.invoke(app, ["main", "http://127.0.0.1:5000/"])
        assert "[ 500 ] - http://127.0.0.1:5000/500" in results.output

    def test_sitemap_successful_result_prints(self):
        results = runner.invoke(
            app, ["main", "http://127.0.0.1:5000/sitemap.xml", "--sitemap", "--verbose"]
        )
        assert "[ 200 ] - http://127.0.0.1:5000/about" in results.output

    def test_sitemap_failing_result_prints(self):
        results = runner.invoke(app, ["main", "http://127.0.0.1:5000/sitemap.xml", "--sitemap"])
        assert "[ 500 ] - http://127.0.0.1:5000/500" in results.output

    def test_not_start_with_http(self):
        results = runner.invoke(app, ["analysis", "mailto:@x.com"])
        assert "Please provide a URL" in results.output

    def test_analysis_obsolete_attr(self):
        results = runner.invoke(app, ["analysis", "http://127.0.0.1:5000/"])
        assert "/about/link-2 - ['name']" in results.output

    def test_analysis_obsolete_attr_with_type(self):
        results = runner.invoke(app, ["analysis", "http://127.0.0.1:5000/", "--type=github"])
        assert results.output.startswith("|")
        assert results.output.endswith("|\n")

    def test_analysis_unsafe_attr(self):
        results = runner.invoke(app, ["analysis", "http://127.0.0.1:5000/", "--target"])
        assert "==========" in results.output
        assert "Safe - [" in results.output
        assert "Unsafe - [" in results.output

    def test_analysis_unsafe_attr_with_type(self):
        results = runner.invoke(app, ["analysis", "http://127.0.0.1:5000/", "--target", "--type=github"])
        assert results.output.startswith("|")
        assert results.output.endswith("|\n")
