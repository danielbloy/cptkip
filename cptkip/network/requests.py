# HTTPServer Library documentation: https://docs.circuitpython.org/projects/httpserver/en/latest/index.html
# API Documentation: https://docs.circuitpython.org/projects/httpserver/en/latest/api.html
#
# Examples of using HTTPServer:
#  * https://learn.adafruit.com/pico-w-http-server-with-circuitpython/code-the-pico-w-http-server
#  * https://learn.adafruit.com/pico-w-wifi-with-circuitpython/pico-w-json-feed-openweathermap
#
# Adafruit requests library:
#  * API Documentation: https://docs.circuitpython.org/projects/requests/en/latest/api.html
#
# The requests library itself:
#  * https://requests.readthedocs.io/en/latest/user/quickstart/

import os
import ssl

from cptkip.core.control import SEND_MESSAGE_TIMEOUT
from cptkip.core.environment import is_running_on_microcontroller

# TODO: This is for sending requests and needs much more thought.

# TODO: We could also probably add get/put/post etc. in here.

# Rather than doing something different based on whether we have pins available or not
# we make the network decision based on whether we are running on a microcontroller or
# not it has a different network stack compared to a desktop.
if is_running_on_microcontroller():
    import wifi
    import socketpool
    import adafruit_requests

    # To set a static IP address
    # import ipaddress
    # ipv4 =  ipaddress.IPv4Address("192.168.1.42")
    # netmask =  ipaddress.IPv4Address("255.255.255.0")
    # gateway =  ipaddress.IPv4Address("192.168.1.1")
    # wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)

    # Connect to the WiFi and setup requests
    wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
    print("Connected to WiFi")

    pool = socketpool.SocketPool(wifi.radio)
    print("IP address: ", wifi.radio.ipv4_address)

    requests = adafruit_requests.Session(pool, ssl.create_default_context())

else:
    # noinspection unused-imports
    import requests

HEADER_NAME = 'name'  # Name of the sender.
HEADER_ROLE = 'role'  # Role of the sender.

HEADERS = {
    HEADER_NAME: "configuration.NODE_NAME",  # TODO: FIXME
    HEADER_ROLE: "configuration.NODE_ROLE",  # TODO: FIXME
}


# TODO: Come up with a better name.
def send_message(path: str, host: str,
                 protocol: str = "http", method="GET",
                 data=None, json=None):
    """
    Sends a message with the provided payload to the specified node, ensuring headers are included.
    """
    return requests.request(method, f"{protocol}://{host}/{path}",
                            headers=HEADERS, data=data, json=json,
                            timeout=SEND_MESSAGE_TIMEOUT)
