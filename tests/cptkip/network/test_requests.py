from cptkip.network.requests import requests


class TestRequests:

    def test_request(self):
        """
        Simple validation for a request.
        """
        with requests.request("GET",
                              f"http://wifitest.adafruit.com/testwifi/index.html") as response:
            assert response.status_code == 200
            assert response.reason == "OK"
            assert response.text == "This is a test of Adafruit WiFi!\nIf you can read this, its working :)"
            assert response.encoding == "ISO-8859-1"
            assert len(response.headers) > 1

    def test_get(self):
        """
        Simple validation for a get request.
        """
        with requests.get("https://httpbin.org/get") as response:
            assert response.status_code == 200
            assert response.json()["url"] == "https://httpbin.org/get"

    def test_post(self):
        """
        Simple validation for a post request.
        """
        with requests.post("https://httpbin.org/post",
                           data="This is an example of a JSON value") as response:
            json_resp = response.json()
            assert json_resp['data'] == "This is an example of a JSON value"
            assert json_resp['headers']['Content-Length'] == '34'
            assert json_resp['url'] == "https://httpbin.org/post"
            assert json_resp['json'] is None
