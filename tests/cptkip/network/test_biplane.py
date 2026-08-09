from collections.abc import Callable
from threading import Thread

# noinspection protected-member
from cptkip.network.biplane import get_host as get_host, get_port as get_port, Server, Response
from cptkip.network.requests import requests


def run_biplane_test(server: Server, test_func: Callable[[str, int], None]):
    """
    Runs a test on a biplane server. the Server is run on a separate thread to process
    requests whilst the test function runs on this thread. they are then joined together
    to complete the test.
    """
    host = get_host()
    port = get_port()
    task = server.create_task((host, port), lambda: running)

    def run_server():
        while task():
            pass

    running = True
    thread = Thread(target=run_server)
    try:
        thread.start()
        test_func(host, port)

    finally:
        running = False
        thread.join()


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
            assert 5001 <= get_port() <= 9000

    def test_create_task(self):
        """
        Validates that we can start the server and receive requests.
        This tests both test_create_task() and python_start_wifi_station() as it
        is simply not worth testing them separately.
        """

        def test_no_routes(host, port):
            response = requests.get(f"http://{host}:{port}")
            assert response.status_code == 404

        server = Server()
        run_biplane_test(server, test_no_routes)

        @server.route("/", "GET")
        def main(query_parameters, headers, body):
            return Response("<b>Hello, world!</b>", content_type="text/html")

        def test_one_route(host, port):
            response = requests.get(f"http://{host}:{port}/")
            assert response.status_code == 200
            assert response.text == "<b>Hello, world!</b>"

        run_biplane_test(server, test_one_route)
