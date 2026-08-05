import sys
from pathlib import Path

import cptkip.core.logging as logging

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


class TestConfiguration:
    # noinspection PyUnresolvedReferences
    def test_config_is_loaded(self, monkeypatch) -> None:
        """
        Validates configuration defaults are loaded as well as the local overrides
        contained in config.py and device.py.
        """
        monkeypatch.syspath_prepend(_FIXTURE_DIR)
        for name in _MODULES_TO_RELOAD:
            monkeypatch.delitem(sys.modules, name, raising=False)

        import cptkip.config.configuration as configuration

        try:
            # These are just random configuration values from the config.
            assert configuration.TRIGGER_DISTANCE == 99999
            assert configuration.TEST_STRING == "Hello world!"
            assert configuration.TEST_VALUE == 123.456
            assert configuration.VALUE_TO_OVERRIDE_IN_DEVICE == 456
            assert configuration.VALUE_ONLY_IN_DEVICE == "This is only in device.py"

            # device.py overrides LOG_LEVEL to DEBUG (see tests/cptkip/config/device.py).
            assert configuration.LOG_LEVEL == logging.DEBUG
        finally:
            for name in _MODULES_TO_RELOAD:
                monkeypatch.delitem(sys.modules, name, raising=False)
