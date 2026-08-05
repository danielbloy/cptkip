import sys
from pathlib import Path

import pytest

_FIXTURE_DIR = str(Path(__file__).parent)
_MODULES_TO_RELOAD = ("config", "device", "cptkip.config.configuration")


@pytest.fixture(scope="package", autouse=True)
def smtp_connection(monkeypatch):
    monkeypatch.syspath_prepend(_FIXTURE_DIR)
    print("monkey patching...")
    for name in _MODULES_TO_RELOAD:
        monkeypatch.delitem(sys.modules, name, raising=False)
    yield

    print("un-monkey patching...")

    for name in _MODULES_TO_RELOAD:
        monkeypatch.delitem(sys.modules, name, raising=False)
