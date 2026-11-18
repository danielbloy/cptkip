def execute():
    from cptkip.network.requests import requests
    import validate.utils as utils

    def task():
        with requests.request("GET", "https://httpbin.org/get") as response:
            print(f"Status ..... : {response.status_code}")
            print(f"Reason ..... : {response.reason}")
            if response.status_code == 200:
                print(f"Text ....... : {response.json()}")

    utils.execute(task)


if __name__ == '__main__':
    execute()
