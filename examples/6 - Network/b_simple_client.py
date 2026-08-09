#
# For more examples, see: https://learn.adafruit.com/networking-in-circuitpython/making-http-andhttps-requests
#
from cptkip.core.memory import report_memory_usage_and_free
from cptkip.network.requests import requests

report_memory_usage_and_free()

queries = [
    {"protocol": "http", "host": "wifitest.adafruit.com", "path": "testwifi/index.html"},
    {"protocol": "https", "host": "www.adafruit.com", "path": "api/quotes.php"},
]

for _ in range(3):
    for query in queries:
        report_memory_usage_and_free()
        protocol = query["protocol"]
        host = query["host"]
        path = query["path"]
        print(f"Calling {protocol}://{host}/{path}...")
        with requests.request("GET", f"{protocol}://{host}/{path}") as response:
            print(f"Status ..... : {response.status_code}")
            print(f"Reason ..... : {response.reason}")
            print(f"Text ....... : {response.text}")
            print(f"Encoding ... : {response.encoding}")
            print(f"Headers .... : {response.headers}\n")

report_memory_usage_and_free()
