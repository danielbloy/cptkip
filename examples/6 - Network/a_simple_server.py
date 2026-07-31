import os
import time

import biplane
import board
import digitalio

SSID = os.getenv('WIFI_SSID')
PASSWORD = os.getenv('WIFI_PASSWORD')
NAME = "app"

server = biplane.Server()
from cptkip.network.test_routes import routes

routes(server)


@server.route("/", "GET")
def main(query_parameters, headers, body):
    return biplane.Response("<b>Hello, world!</b>", content_type="text/html")


def asyncio_sleep(
        seconds):  # minimal implementation of asyncio.sleep() as a generator
    start_time = time.monotonic()
    while time.monotonic() - start_time < seconds:
        yield


def blink_builtin_led():
    with digitalio.DigitalInOut(board.LED) as led:
        led.switch_to_output(value=False)
        while True:
            led.value = not led.value
            yield from asyncio_sleep(0.05)


#for _ in zip(blink_builtin_led(),
#             server.circuitpython_start_wifi_station(SSID, PASSWORD, NAME)):
#    pass

blink = blink_builtin_led()
listen = server.circuitpython_start_wifi_station(SSID, PASSWORD, NAME)
while True:
    blink.__next__()
    listen.__next__()
