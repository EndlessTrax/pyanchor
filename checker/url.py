import requests


def check_response_code(url: str) -> int:
    """Check the status code of the given url."""
    return requests.get(url).status_code

