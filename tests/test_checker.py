from checker.url import check_response_code


def test_200_response():
    resp_code = check_response_code("https://google.com")
    assert resp_code == 200


def test_404_response():
    resp_code = check_response_code("https://google.com/blah-blah")
    assert resp_code == 404
