# Shared WiFi settings handling for cptkip.network.
#
# Credentials are read from settings.toml. Both the cptkip names (WIFI_SSID and
# WIFI_PASSWORD) and CircuitPython's standard names (CIRCUITPY_WIFI_SSID and
# CIRCUITPY_WIFI_PASSWORD) are supported. With the standard names CircuitPython
# connects to WiFi automatically at boot, in which case connect_wifi() reuses that
# connection rather than connecting again.
from os import getenv


def wifi_credentials() -> tuple[str, str]:
    """
    Returns the (ssid, password) from settings.toml, preferring WIFI_SSID/WIFI_PASSWORD
    and falling back to CIRCUITPY_WIFI_SSID/CIRCUITPY_WIFI_PASSWORD.
    """
    ssid = getenv("WIFI_SSID") or getenv("CIRCUITPY_WIFI_SSID")
    if not ssid:
        raise ValueError("WIFI_SSID (or CIRCUITPY_WIFI_SSID) must be specified in settings.toml")

    password = getenv("WIFI_PASSWORD") or getenv("CIRCUITPY_WIFI_PASSWORD")
    if not password:
        raise ValueError("WIFI_PASSWORD (or CIRCUITPY_WIFI_PASSWORD) must be specified in settings.toml")

    return ssid, password


def connect_wifi(radio) -> None:
    """
    Connects the given radio (wifi.radio) using the settings.toml credentials, unless
    it is already connected (for example by CircuitPython's automatic connection).
    """
    if radio.ipv4_address:
        return

    ssid, password = wifi_credentials()
    radio.connect(ssid, password)
