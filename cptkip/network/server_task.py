import os
from random import randint

from cptkip.core.environment import is_running_on_desktop, is_running_under_test
from cptkip.network.biplane import Server

# collections.abc is not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable


def _get_port() -> int:
    if is_running_under_test():
        return randint(5001, 50000)
    elif is_running_on_desktop():
        from cptkip.core.control import NETWORK_PORT_DESKTOP
        return NETWORK_PORT_DESKTOP
    else:
        from cptkip.core.control import NETWORK_PORT_MICROCONTROLLER
        return NETWORK_PORT_MICROCONTROLLER


def _get_host():
    if is_running_under_test():
        return "127.0.0.1"
    elif is_running_on_desktop():
        import socket
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
    else:
        return "0.0.0.0"


def get_address() -> str:
    """
    Returns the address of this node including the port that is being
    listened on.
    """
    return f"{_get_host()}:{_get_port()}"


def create(
        server: Server,
        continue_func: Callable[[], bool] | None = None) -> Callable[[], bool]:
    """
    TODO: Comments

    :param server:
    :param continue_func:
    :return:
    """
    if is_running_on_desktop():
        import socket
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen = server.start(server_socket, listen_on=(_get_host(), _get_port()))
        print(f"starting on IP address {_get_host()}:{_get_port()}")
    else:
        listen = server.circuitpython_start_wifi_station(
            os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'), "app")  # TODO: Proper hostname

    def monitor() -> bool:
        listen.__next__()
        return not continue_func or continue_func()

    return monitor
