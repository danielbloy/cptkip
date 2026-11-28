from threading import Thread
from typing import Callable

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
    task = server.create_task(lambda: running, (host, port))

    def run_server():
        while task():
            pass

    running = True
    # Run the server once on this thread first: that binds and starts listening, so the
    # test cannot connect before the server is ready (which intermittently gave
    # ConnectionRefusedError in CI).
    task()
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
            assert 5001 <= get_port() <= 30000

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


def raw_request(host: str, port: int, data: bytes, timeout: float = 5) -> bytes:
    """
    Sends raw bytes to the server and returns everything received until the server
    closes the connection. Used for requests that a normal HTTP client won't send.
    """
    import socket
    received = []
    with socket.create_connection((host, port), timeout=timeout) as s:
        if data:
            s.sendall(data)
        while True:
            try:
                chunk = s.recv(4096)
            except OSError:  # e.g. connection reset when the server gives up
                break
            if not chunk:
                break
            received.append(chunk)
    return b"".join(received)


class TestBiPlaneErrorHandling:

    def test_response_headers_are_not_shared(self):
        """
        Responses created without explicit headers must not share a headers dict,
        and a headers dict passed in must not be modified.
        """
        first = Response("a")
        first.headers["x-custom"] = "1"
        second = Response("b")
        assert "x-custom" not in second.headers
        assert first.headers is not second.headers

        supplied = {"x-supplied": "yes"}
        response = Response("c", headers=supplied)
        assert response.headers["x-supplied"] == "yes"
        assert supplied == {"x-supplied": "yes"}

    def test_listen_on_defaults_are_evaluated_per_call(self, monkeypatch):
        """
        The default host/port must be looked up when the server is started, not once
        at import time.
        """
        import cptkip.network.biplane as biplane
        calls = []
        monkeypatch.setattr(biplane, "get_host", lambda: calls.append("host") or "127.0.0.1")
        monkeypatch.setattr(biplane, "get_port", lambda: calls.append("port") or 5999)

        listen = Server().python_start_wifi_station()
        listen.close()
        assert calls == ["host", "port"]

    def test_body_too_large_returns_413(self):
        def check(host, port):
            response = raw_request(host, port, b"POST / HTTP/1.1\r\ncontent-length: 10\r\n\r\n0123456789")
            assert response.startswith(b"HTTP/1.1 413")

        run_biplane_test(Server(max_body_bytes=4), check)

    def test_wrong_method_returns_404(self):
        server = Server()

        @server.route("/", "GET")
        def main(query_parameters, headers, body):
            return Response("ok")

        def check(host, port):
            assert requests.post(f"http://{host}:{port}/").status_code == 404
            assert requests.get(f"http://{host}:{port}/").status_code == 200

        run_biplane_test(server, check)

    def test_over_long_start_line_is_rejected(self):
        """
        A start line longer than max_request_line_size is truncated by the reader. The
        server must give up rather than carry on with the truncated line (which used
        to produce a 404 response here).
        """

        def check(host, port):
            assert raw_request(host, port, b"GET /abcd HTTP/1\r\n\r\n") == b""

        run_biplane_test(Server(max_request_line_size=16), check)

    def test_malformed_start_line_is_rejected(self):
        def check(host, port):
            assert raw_request(host, port, b"NONSENSE\r\n\r\n") == b""

        run_biplane_test(Server(), check)

    def test_malformed_header_is_rejected(self):
        def check(host, port):
            assert raw_request(host, port, b"GET / HTTP/1.1\r\nno-colon-here\r\n\r\n") == b""

        run_biplane_test(Server(), check)

    def test_too_many_headers_are_rejected(self):
        def check(host, port):
            request = b"GET / HTTP/1.1\r\na: 1\r\nb: 2\r\nc: 3\r\n\r\n"
            assert raw_request(host, port, request) == b""

        run_biplane_test(Server(max_header_count=1), check)

    def test_malformed_content_length_is_rejected(self):
        def check(host, port):
            assert raw_request(host, port, b"POST / HTTP/1.1\r\ncontent-length: abc\r\n\r\n") == b""

        run_biplane_test(Server(), check)

    def test_idle_connection_times_out(self):
        """
        A client that connects but never sends anything is disconnected after
        request_timeout_seconds.
        """
        import time

        def check(host, port):
            start = time.monotonic()
            assert raw_request(host, port, b"") == b""
            assert time.monotonic() - start < 3

        run_biplane_test(Server(request_timeout_seconds=0.2), check)
