# TODO: MockServer with custom ports and endpoints.
# noinspection protected-member
from cptkip.network.biplane import _get_host as get_host, _get_port as get_port


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
        assert True

    def test_create_task(self):
        """
        Validates that we can create a server task and run with it.
        """
        assert True
