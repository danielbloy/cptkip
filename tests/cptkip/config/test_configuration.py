import cptkip.config.configuration as configuration
import cptkip.core.logging as logging


class TestNode:
    # noinspection PyUnresolvedReferences
    def test_config_is_loaded(self) -> None:
        """
        Validates configuration defaults are loaded as well as the local overrides
        contained in config.py and device.py.
        """

        # These are just random configuration values from the config.
        assert configuration.TRIGGER_DISTANCE == 99999
        assert configuration.TEST_STRING == "Hello world!"
        assert configuration.TEST_VALUE == 123.456
        assert configuration.VALUE_TO_OVERRIDE_IN_DEVICE == 456
        assert configuration.VALUE_ONLY_IN_DEVICE == "This is only in device.py"

        # device.py overrides LOG_LEVEL to DEBUG (see tests/cptkip/config/device.py).
        assert configuration.LOG_LEVEL == logging.DEBUG
