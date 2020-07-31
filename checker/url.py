import requests


def check_response_code(url: str) -> int:
    """Check the status code of the given url."""
    return requests.get(url).status_code


def check_link_for_http_scheme(base_url: str, href: str) -> str:
    if href.startswith(base_url):
        return href
    elif href.startswith("/"):
        href = base_url + href
        return href
    else:
        return href  # TODO: Deal with ./ or ../ relative links. And #links