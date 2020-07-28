from checker.url import check_response_code


if __name__ == "__main__":
    test = check_response_code('https://google.com')
    print(test)