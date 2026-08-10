def execute():
    from cptkip.network.requests import requests
    import validate.utils as utils

    def task():
        with requests.request("GET", "http://www.adafruit.com/api/quotes.php") as response:
            print(f"Status ..... : {response.status_code}")
            print(f"Reason ..... : {response.reason}")
            print(f"Text ....... : {response.json()[0]['text']}")

    utils.execute(task)


if __name__ == '__main__':
    execute()
