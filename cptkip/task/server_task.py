import os

from biplane import Server

from cptkip.core.environment import is_running_on_desktop
from cptkip.core.logging import error

# collections.abc is not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable


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
        # TODO: Address and port need extracting out
        listen = server.start(server_socket, listen_on=('127.0.0.1', 8000))
    else:
        listen = server.circuitpython_start_wifi_station(
            os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'), "app")  # TODO: Proper hostname

    def monitor() -> bool:
        nonlocal listen
        try:
            listen.__next__()

        except OSError as err:
            # Because on Windows we get annoying BlockingIOErrors when running the network,
            # we swallow those here as they make all other output difficult to see.
            ignore = is_running_on_desktop() and type(err) is BlockingIOError
            if not ignore:
                error(str(err))
                raise err

        return not continue_func or continue_func()

    return monitor
