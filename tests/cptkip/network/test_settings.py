import pytest

from cptkip.network.settings import connect_wifi, wifi_credentials

_NAMES = ("WIFI_SSID", "WIFI_PASSWORD", "CIRCUITPY_WIFI_SSID", "CIRCUITPY_WIFI_PASSWORD")


class FakeRadio:
    def __init__(self, ipv4_address=None):
        self.ipv4_address = ipv4_address
        self.connected_with = None

    def connect(self, ssid, password):
        self.connected_with = (ssid, password)
        self.ipv4_address = "192.168.1.2"


@pytest.fixture
def clean_env(monkeypatch):
    for name in _NAMES:
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


class TestSettings:

    def test_cptkip_names(self, clean_env):
        clean_env.setenv("WIFI_SSID", "ssid")
        clean_env.setenv("WIFI_PASSWORD", "password")
        assert wifi_credentials() == ("ssid", "password")

    def test_circuitpython_names(self, clean_env):
        clean_env.setenv("CIRCUITPY_WIFI_SSID", "cp-ssid")
        clean_env.setenv("CIRCUITPY_WIFI_PASSWORD", "cp-password")
        assert wifi_credentials() == ("cp-ssid", "cp-password")

    def test_cptkip_names_take_precedence(self, clean_env):
        for name in _NAMES:
            clean_env.setenv(name, name.lower())
        assert wifi_credentials() == ("wifi_ssid", "wifi_password")

    def test_missing_values_raise(self, clean_env):
        with pytest.raises(ValueError):
            wifi_credentials()

        clean_env.setenv("WIFI_SSID", "ssid")
        with pytest.raises(ValueError):
            wifi_credentials()

    def test_connect_wifi_connects_when_not_connected(self, clean_env):
        clean_env.setenv("CIRCUITPY_WIFI_SSID", "ssid")
        clean_env.setenv("CIRCUITPY_WIFI_PASSWORD", "password")
        radio = FakeRadio()
        connect_wifi(radio)
        assert radio.connected_with == ("ssid", "password")

    def test_connect_wifi_reuses_existing_connection(self, clean_env):
        """
        If CircuitPython has already connected (e.g. automatically at boot), no
        credentials are needed and connect() is not called again.
        """
        radio = FakeRadio(ipv4_address="192.168.1.5")
        connect_wifi(radio)
        assert radio.connected_with is None
