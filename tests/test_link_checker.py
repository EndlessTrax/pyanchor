import pytest
from typer.testing import CliRunner

from link_checker import app

runner = CliRunner()

def test_exception_on_invalid_url_http_scheme():
    """TODO:"""
    
    result = runner.invoke(app, ['google.com'])
    assert result.exit_code == 1


def test_successful_result_prints():
    """TODO: """

    results = runner.invoke(app, ['https://google.com'])
    assert "200 - https://google.com/services/" in results.output