import cptkip.config.configuration as configuration
import cptkip.core.logging as logging


class TestNode:
    def test_config_is_loaded(self) -> None:
        """
        Validates configuration defaults are loaded as well as the local overrides
        contained in config.py.
        """

        # These are just random configuration values from the config.
        # noinspection PyUnresolvedReferences
        assert configuration.TRIGGER_DISTANCE == 99999
        assert configuration.TEST_STRING == "Hello world!"
        assert configuration.TEST_VALUE == 123.456
        assert configuration.LOG_LEVEL == logging.WARNING
