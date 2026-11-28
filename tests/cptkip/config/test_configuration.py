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

    def test_log_level_and_defaults_are_applied(self, monkeypatch, capsys) -> None:
        """
        Validates the final LOG_LEVEL (after device.py overrides config.py) is applied to
        the logger, hardware settings missing from config.py get defaults, and the
        configuration report is printed at INFO or above.
        """
        monkeypatch.syspath_prepend(_FIXTURE_DIR)
        for name in _MODULES_TO_RELOAD:
            monkeypatch.delitem(sys.modules, name, raising=False)

        original_level = logging.LEVEL
        try:
            import cptkip.config.configuration as configuration
            assert logging.LEVEL == logging.DEBUG

            # The fixture config.py/device.py do not define any hardware settings.
            assert configuration.LED_PIN is None
            assert configuration.LED_INVERT is False
            assert configuration.BUTTON_PIN is None
            assert configuration.BUTTON_PULLUP is True
            assert configuration.BUZZER_PIN is None
            assert configuration.PIXELS_PIN is None
            assert configuration.PIXELS_COUNT == 1
            assert configuration.I2S_DATA is None

            output = capsys.readouterr().out
            assert "Config file loaded." in output
            assert "Device file loaded." in output
            assert "LED not configured" in output
        finally:
            logging.set_log_level(original_level)
            for name in _MODULES_TO_RELOAD:
                monkeypatch.delitem(sys.modules, name, raising=False)

    def test_report_is_not_printed_below_info(self, monkeypatch, capsys, tmp_path) -> None:
        """
        Validates nothing is printed when the configured LOG_LEVEL is below INFO.
        """
        (tmp_path / "config.py").write_text("from cptkip.core.logging import WARNING\nLOG_LEVEL = WARNING\n")
        # Shadow the fixture device.py (which sets DEBUG); pytest puts this test
        # directory on sys.path.
        (tmp_path / "device.py").write_text("")
        monkeypatch.syspath_prepend(str(tmp_path))
        for name in _MODULES_TO_RELOAD:
            monkeypatch.delitem(sys.modules, name, raising=False)

        original_level = logging.LEVEL
        try:
            capsys.readouterr()
            import cptkip.config.configuration as configuration
            assert configuration.LOG_LEVEL == logging.WARNING
            assert capsys.readouterr().out == ""
        finally:
            logging.set_log_level(original_level)
            for name in _MODULES_TO_RELOAD:
                monkeypatch.delitem(sys.modules, name, raising=False)
