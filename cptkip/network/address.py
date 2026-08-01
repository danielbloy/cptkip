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

# TODO: This might need a better name.
import os
from random import randint

from cptkip.core.environment import is_running_on_microcontroller, is_running_under_test

# Rather than doing something different based on whether we have pins available or not
# we make the network decision based on whether we are running on a microcontroller or
# not it has a different network stack compared to a desktop.
if is_running_on_microcontroller():
    import wifi
    import socketpool

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


    def get_ip():
        return wifi.radio.ipv4_address


else:
    import socket
    import toml

    # TODO: Can this be removed?
    if os.path.isfile('settings.toml'):
        with open('settings.toml') as f:
            config = toml.load(f)


    def get_ip():
        # from https://stackoverflow.com/a/28950776
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


def _get_port() -> int:
    if is_running_under_test():
        return randint(5001, 50000)
    elif is_running_on_microcontroller():
        from cptkip.core.control import NETWORK_PORT_MICROCONTROLLER
        return NETWORK_PORT_MICROCONTROLLER
    else:
        from cptkip.core.control import NETWORK_PORT_DESKTOP
        return NETWORK_PORT_DESKTOP


def _get_host():
    if is_running_under_test():
        return "127.0.0.1"
    elif is_running_on_microcontroller():
        return "0.0.0.0"
    else:
        return get_ip()


def get_address() -> str:
    """
    Returns the address of this node including the port that is being listened on.
    """
    return f"{_get_host()}:{_get_port()}"
