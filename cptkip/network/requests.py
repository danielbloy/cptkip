# This module basically abstracts out getting access to a requests object in
# both Python and CircuitPython. the footprint of those libraries is very
# similar but not identical so care needs to be taken when writing code
# using requests to ensure portability. To get the requests library in your
# code, use `from cptkip.network.requests import requests` as demonstrated
# in the example `6 - network/b_simple_client.py`
#
# Adafruit requests library:
#  * API Documentation: https://docs.circuitpython.org/projects/requests/en/latest/api.html
#
# The requests library itself:
#  * https://requests.readthedocs.io/en/latest/user/quickstart/
from cptkip.core.environment import is_running_on_microcontroller
from cptkip.core.logging import info

# Rather than doing something different based on whether we have pins available or not
# we make the network decision based on whether we are running on a microcontroller or
# not it has a different network stack compared to a desktop.
if is_running_on_microcontroller():
    import ssl
    import wifi
    import socketpool
    import adafruit_requests

    # To set a static IP address
    # import ipaddress
    # ipv4 =  ipaddress.IPv4Address("192.168.1.42")
    # netmask =  ipaddress.IPv4Address("255.255.255.0")
    # gateway =  ipaddress.IPv4Address("192.168.1.1")
    # wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)

    from cptkip.network.settings import connect_wifi

    # Connect to the Wi-Fi (unless already connected) and setup requests. Credentials
    # come from WIFI_SSID/WIFI_PASSWORD or CIRCUITPY_WIFI_SSID/CIRCUITPY_WIFI_PASSWORD.
    connect_wifi(wifi.radio)
    info("Connected to WiFi")

    pool = socketpool.SocketPool(wifi.radio)
    info("IP address: ", wifi.radio.ipv4_address)

    requests = adafruit_requests.Session(pool, ssl.create_default_context())

else:
    # noinspection unused-imports
    import requests
