# TODO: MockServer with custom ports and endpoints.
import asyncio
from threading import Thread

# noinspection protected-member
from cptkip.network.biplane import get_host as get_host, get_port as get_port, Server
from network.requests import requests


def python_start_wifi_station(param):
    pass


class TestBiPlane:

    def test_get_host(self):
        """
        Validates that _get_host() works as expected.
        This is a very basic test that only tests the functionality in
        the CI environment.
        """
        assert get_host() == '127.0.0.1'

    def test_get_port(self):
        """
        Validates that _get_host() works as expected.
        This is a very basic test that only tests the functionality in
        the CI environment.
        """
        for _ in range(100):
            assert 5001 <= get_port() <= 50000

    def test_python_start_wifi_station(self):
        """
        Validates that we can start the server and receive requests.
        """
        host = get_host()
        port = get_port()
        server = Server()
        listen = server.python_start_wifi_station((host, port))

        running = False

        # TODO: This does not need to be async at all, we can do it on our thread.
        async def run_server():
            print("a")
            while running:
                listen.__next__()
                await asyncio.sleep(0)
            print("b")

        def test():
            nonlocal running
            print("c")
            x = requests.get(f"http://{host}:{port}/")
            print("d")

        # print(f"http://{host}:{port}/")
        # requests.get(f"http://{host}:{port}/")
        # print("got")
        asyncio.run(run_server())

        thread = Thread(target=test)
        thread.start()
        thread.join()
        running = False
        print("g")

    def test_create_task(self):
        """
        Validates that we can create a server task and run with it.
        """
        # TODO: Implement
        assert True
