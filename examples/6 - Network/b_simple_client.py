#
# For the complete example, see: https://learn.adafruit.com/networking-in-circuitpython/making-http-andhttps-requests
#
from cptkip.core.memory import report_memory_usage_and_free
from cptkip.network.requests import requests

queries = [
    {"protocol": "http", "host": "wifitest.adafruit.com", "path": "testwifi/index.html"},
    {"protocol": "https", "host": "www.adafruit.com", "path": "api/quotes.php"},
]
print("\n")

for query in queries:
    report_memory_usage_and_free()
    protocol = query["protocol"]
    host = query["host"]
    path = query["path"]
    print(f"Calling {protocol}://{host}/{path}...")
    with requests.request("GET", f"{protocol}://{host}/{path}") as response:
        print(f"Status .................. : {response.status_code}")
        print(f"Reason .................. : {response.reason}")
        if response.status_code != 200:
            continue
        print(f"Text .................... : {response.text}")
        print(f"Encoding ................ : {response.encoding}")
        print(f"Headers ................. : {response.headers}\n")

report_memory_usage_and_free()

# Now send some post and other types of messages.
print("\n", "-" * 80, "\n")

JSON_GET_URL = "https://httpbin.org/get"
JSON_POST_URL = "https://httpbin.org/post"

with requests.get(JSON_GET_URL) as response:
    print(f"Status .................. : {response.status_code}")
    print(f"Reason .................. : {response.reason}")
    if response.status_code == 200:
        print(f"Unparsed JSON Response .. : {response.json()}\n")

DATA = "This is an example of a JSON value"
with requests.post(JSON_POST_URL, data=DATA) as response:
    print(f"Status .................. : {response.status_code}")
    print(f"Reason .................. : {response.reason}")
    if response.status_code == 200:
        # Parse out the 'data' key from json_resp dict.
        json_resp = response.json()
        print(f"JSON 'value' Response ... : {json_resp['data']}\n")

report_memory_usage_and_free()
