try:
    import wifi
except ImportError:
    print("WiFi not available, skipping script")
    from validate.performance.script_runner import execute_next_script

    execute_next_script(__file__)

from cptkip.network.requests import requests
from validate.performance.task_runner import execute


from time import monotonic

next_request = 0


def task():
    # At most one request per second so as not to hammer a public service.
    global next_request
    if monotonic() < next_request:
        return
    next_request = monotonic() + 1

    with requests.request("GET", "https://httpbin.org/get") as response:
        print(f"Status ..... : {response.status_code}")
        print(f"Reason ..... : {response.reason}")
        print(f"Text ....... : {response.json()}")


execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
