import pytest

from typer.testing import CliRunner
from pyanchor.cli import app
import os


runner = CliRunner()


@pytest.mark.usefixtures("server")
class TestCli:
    def test_exception_on_invalid_url_http_scheme(self):
        result = runner.invoke(app, ["google.com"])
        assert result.exit_code == 1

    def test_successful_result_prints(self):
        results = runner.invoke(app, ["http://127.0.0.1:5000/", "--verbose"])
        assert "[ 200 ] - http://127.0.0.1:5000/about" in results.output

    def test_failing_result_prints(self):
        results = runner.invoke(app, ["http://127.0.0.1:5000/"])
        assert "[ 500 ] - http://127.0.0.1:5000/500" in results.output

    def test_sitemap_successful_result_prints(self):
        results = runner.invoke(
            app, ["http://127.0.0.1:5000/sitemap.xml", "--sitemap", "--verbose"]
        )
        assert "[ 200 ] - http://127.0.0.1:5000/about" in results.output

    def test_sitemap_failing_result_prints(self):
        results = runner.invoke(app, ["http://127.0.0.1:5000/sitemap.xml", "--sitemap"])
        assert "[ 500 ] - http://127.0.0.1:5000/500" in results.output

    def test_output_to_csv(self):
        csv_file = "test_output.csv"
        results = runner.invoke(app, ["http://127.0.0.1:5000/", "--output-csv", csv_file])
        assert results.exit_code == 0
        assert os.path.exists(csv_file)
        with open(csv_file, 'r') as file:
            content = file.read()
            assert "HTTP Code,URL" in content
            assert "200,http://127.0.0.1:5000/about" in content
        os.remove(csv_file)