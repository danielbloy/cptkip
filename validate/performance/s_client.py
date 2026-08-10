from cptkip.network.requests import requests
from validate.performance.task_runner import execute


def task():
    with requests.request("GET", "http://www.adafruit.com/api/quotes.php") as response:
        print(f"Status ..... : {response.status_code}")
        print(f"Reason ..... : {response.reason}")
        print(f"Text ....... : {response.json()[0]['text']}")


execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
