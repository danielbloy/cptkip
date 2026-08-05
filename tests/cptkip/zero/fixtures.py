import sys
from pathlib import Path

import pytest

# cptkip.config.configuration only reads config.py/device.py once, at first
# import, and caches the result in sys.modules. Since this directory's own
# config.py/device.py fixtures are what we want it to load, we must prepend
# this directory to sys.path and force a fresh import here, then undo both
# so this fixture config.py/device.py can't leak into any other test that
# imports cptkip.config.configuration later in the session. This code needs
# to be kept in sync with:
#   * tests/cptkip/config/test_configuration.py
#   * tests/cptkip/zero/fixtures.py
#
_FIXTURE_DIR = str(Path(__file__).parent)
_MODULES_TO_RELOAD = ("config", "device", "cptkip.config.configuration")


@pytest.fixture(scope="package", autouse=True)
def smtp_connection(monkeypatch):
    monkeypatch.syspath_prepend(_FIXTURE_DIR)
    for name in _MODULES_TO_RELOAD:
        monkeypatch.delitem(sys.modules, name, raising=False)

    yield

    for name in _MODULES_TO_RELOAD:
        monkeypatch.delitem(sys.modules, name, raising=False)
